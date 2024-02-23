import itertools
import math
import operator
import random
from pandas import Series, DataFrame, concat
from datetime import datetime, date, timedelta
from ztm_api_wrapper import WrapperZtm, GetSaveApiZtmData, NoDataSavedException
from typing import List, Dict, Tuple, Optional, Union, Callable, TypeVar
import numpy as np
import geopy.distance
from geopy.geocoders import Nominatim
from ztm_api_wrapper import WrongMethodException
from functools import partial
from queue import PriorityQueue

Self = TypeVar("Self", bound="object")


class BusStop:
    """Represents a bus stop with its attributes and methods.

    Attributes:
        complex (str): The complex ID of the bus stop.
        stop_nr (str): The stop number of the bus stop.
        complex_name (str): The name of the complex.
        street_id (str): The ID of the street where the bus stop is located.
        lat (float): The latitude coordinate of the bus stop.
        lon (float): The longitude coordinate of the bus stop.
        direction (str): The direction of the bus stop.
        valid_from (datetime): The date and time when the data becomes valid.
        available_lines (List[str]): List of available bus lines at the bus stop.
    """

    def __init__(self, series: Series, time: datetime, get_save: GetSaveApiZtmData):
        """Initializes a BusStop instance.

        Args:
            series (Series): The series containing bus stop data. 
                -> index = ["zespol", "slupek", "nazwa_zespolu", "id_ulicy", "szer_geo", "dlug_geo", "kierunek", "obowiazuje_od"]
            time (datetime): The time from which the data should come.
            get_save (GetSaveApiZtmData): An instance of GetSaveApiZtmData class.
        """
        self.get_save = get_save

        self.complex: str = series["zespol"]
        self.stop_nr: str = series["slupek"]
        self.complex_name: str = series["nazwa_zespolu"]
        self.street_id: str = series["id_ulicy"]
        self.lat: float = float(series["szer_geo"])
        self.lon: float = float(series["dlug_geo"])
        self.direction: str = series["kierunek"]
        try:
            self.valid_from: Optional[datetime] = datetime.strptime(series["obowiazuje_od"], "%Y-%m-%d %H:%M:%S.0")
        except Exception as e:
            print(f"series[obowiazuje_od] = {series['bowiazuje_od']} and some exception occured: {e}")
            self.valid_from = None

        self.available_lines: List[str] = get_save.get_available_lines(self.complex, self.stop_nr,
                                                                       from_date=time)

        self.schedules: Dict[str, DataFrame] = dict()
        for line in self.available_lines:
            self.schedules[line] = get_save.get_schedule(self.complex, self.stop_nr, line,
                                                         from_date=time, ret_as_data_frame=True)


class Bus:
    """Represents a bus with its attributes and methods.

    Attributes:
        line (str): The line of the bus.
        vehicle_number (str): The vehicle number of the bus.
        brigade (str): The brigade of the bus.
        known_location (DataFrame): DataFrame containing known locations of the bus.
    """

    def __init__(self, line: str, vehicle_number: str, brigade: str):
        """Initializes a Bus instance.

        Args:
            line (str): The line of the bus.
            vehicle_number (str): The vehicle number of the bus.
            brigade (str): The brigade of the bus.
        """
        self.line: str = line
        self.vehicle_number: str = vehicle_number
        self.brigade: str = brigade

        # self.known_location: List[Tuple[Tuple[float, float], datetime]] = []
        self.known_location: DataFrame = DataFrame(columns=['Lon', 'Lat', 'Time'], dtype=str)

    def add_known_location(self, pandas_obj: Union[Series, DataFrame]) -> None:
        """Adds a known location to the bus.

        Args:
            pandas_obj (Series | DataFrame): Object containing location data.
                -> columns = ['Lon': str, 'Lat': str 'Time': str]
        """
        self.known_location = concat([self.known_location, pandas_obj], ignore_index=True)

    def get_busses_speed(self) -> DataFrame:
        """Calculates places where the bus exceeds speed limit.

        Returns:
            DataFrame: DataFrame containing locations where the bus exceeds speed limit.
        """

        self.known_location.sort_values(by=['Time', 'Lon', "Lat"])

        shifted: DataFrame = self.known_location.shift(1)
        shifted.rename(mapper={'Lon': 'Lon2', 'Lat': 'Lat2', 'Time': 'Time2'}, axis=1, inplace=True)

        df: DataFrame = concat([self.known_location, shifted], axis=1)

        def calc(series: Series) -> Series:
            if series.isnull().sum() > 0:
                return Series([-1, -1, -1, -1])

            coords_1: Tuple[str, str] = (series["Lon"], series["Lat"])
            coords_2: Tuple[str, str] = (series["Lon2"], series["Lat2"])

            try:
                dist: float = geopy.distance.geodesic(coords_1, coords_2).km
                t1: datetime = datetime.strptime(series["Time"], "%Y-%m-%d %H:%M:%S")
                t2: datetime = datetime.strptime(series["Time2"], "%Y-%m-%d %H:%M:%S")
            except ValueError:
                return Series([-1, -1, -1, -1])

            delta: timedelta = t1 - t2

            if delta.total_seconds() == 0:
                return Series([-1, coords_2[0], coords_2[1], str(t2)])

                # speed in km/h
            speed: float = dist / (delta.total_seconds() / 3600.0)

            if speed < 0:
                return Series([-1, coords_2[0], coords_2[1], str(t2)])

            return Series([speed, coords_2[0], coords_2[1], str(t2)])

        result: DataFrame = df.apply(calc, axis=1)
        result.rename(mapper={0: 'Speed(km/h)', 1: 'Lon', 2: 'Lat', 3: 'Time'}, axis=1, inplace=True)
        result.drop(index=df.index[0], axis=0, inplace=True)
        return result


class ZTM:
    """Represents the environment system with buses and bus stops.

    Attributes:v
        date_dt (datetime): The time from which the data should come.
        get_save (GetSaveApiZtmData): An instance of GetSaveApiZtmData class.
        bus_stops (List[BusStop]): List of bus stops in the ZTM system.
        routes (Dict[str, Dict[str, Dict[str, Dict]]]): Dictionary containing routes information.
        notation_dict (Dict[str, Dict[str, str]]): Dictionary containing notation information.
        buses (Dict[str, Dict[str, Dict[str, Bus]]]): Dictionary containing bus information.
    """

    def __init__(self, date: date, get_save: GetSaveApiZtmData, read_meta: bool = True):
        """Initializes a ZTM instance.

        Args:
            date (date): The time from which the data should come.
            get_save (GetSaveApiZtmData): An instance of GetSaveApiZtmData class.
            read_meta (bool, optional): Whether to read metadata. Defaults to True.
        """
        self.get_save: GetSaveApiZtmData = get_save

        self.date_dt: datetime = datetime(date.year, date.month, date.day)

        self.busses: Dict[str, Dict[str, Dict[str, Bus]]] = dict()

        if read_meta:
            all_stops_df: DataFrame = get_save.get_all_stops(from_date=self.date_dt, ret_as_data_frame=True)
            self.bus_stops = list()

            for index, row in all_stops_df.iterrows():
                self.bus_stops.append(BusStop(row, self.date_dt, get_save))

            self.routes: Dict[str, Dict[str, Dict[str, Dict]]] = get_save.get_routes(from_date=self.date_dt)
            self.notation_dict: Dict[str, Dict[str, str]] = get_save.get_notation_dict(from_date=self.date_dt)

    def add_locations_to_bus(self, line: str, brigade: str, vehicle_number: str, locations: DataFrame) -> None:
        """Adds location data to a specific bus in the environment system.

        Args:
            line (str): The line identifier of the bus.
            brigade (str): The brigade identifier of the bus.
            vehicle_number (str): The vehicle number of the bus.
            locations (DataFrame): DataFrame containing location data.
                It should have the following columns:
                    - 'Time': Timestamp of the location data.
                    - 'Lat': Latitude coordinate of the bus.
                    - 'Lon': Longitude coordinate of the bus.

        """
        locations.drop(labels=['Lines', 'VehicleNumber', 'Brigade'], inplace=True, axis=1)
        if line not in self.busses.keys():
            self.busses[line] = dict()

        if brigade not in self.busses[line].keys():
            self.busses[line][brigade] = dict()

        if vehicle_number not in self.busses[line][brigade].keys():
            self.busses[line][brigade][vehicle_number] = Bus(line, vehicle_number, brigade)

        self.busses[line][brigade][vehicle_number].add_known_location(locations)

    def add_all_loc_period(self, start: datetime, stop: datetime) -> None:
        """Adds all locations within a specified period to the ZTM system.

        Args:
            start (datetime): Start time.
            stop (datetime): Stop time.
        
        Raises:
            ValueError: If the specified period is not within the current date of the environment system.
        """
        if start < self.date_dt or stop > self.date_dt + timedelta(days=1):
            raise ValueError("Can only work with data within a day")

        def round_to_ten_seconds(dt: datetime) -> datetime:
            tim_del = timedelta(seconds=dt.second % 10,
                                microseconds=dt.microsecond)
            return dt - tim_del

        delta: timedelta = timedelta(seconds=10)
        single_date: datetime = round_to_ten_seconds(start)

        list_of_df: List[DataFrame] = []

        while single_date <= stop:
            print(single_date)
            try:
                df: DataFrame = self.get_save.get_online_location(1, from_date=single_date, ret_as_data_frame=True)
                list_of_df.append(df)
            except NoDataSavedException:
                print(f"No data for busses found for f{single_date}")
                pass
            except WrongMethodException as e:
                print(f"WrongMethodException occurred: {e}")

            try:
                df: DataFrame = self.get_save.get_online_location(2, from_date=single_date, ret_as_data_frame=True)
                list_of_df.append(df)
            except NoDataSavedException:
                print(f"no data for trams found for f{single_date}")
                pass
            except WrongMethodException as e:
                print(f"WrongMethodException occurred: {e}")

            single_date += delta

        big_df: DataFrame = concat(list_of_df, ignore_index=True)

        bus: Tuple[str, str, str]
        for bus, rest in big_df.groupby(['Lines', 'Brigade', 'VehicleNumber']):
            self.add_locations_to_bus(bus[0], bus[1], bus[2], rest)

    def all_busses_speed(self, filter_speed: Callable[[float], bool] = None) -> DataFrame:
        """Gets speed data for all buses in the environment system.

        Args:
            filter_speed (Callable[[float], bool], optional): A function to filter speeds.
                If provided, only speeds for which this function returns True will be included.
                Defaults to None.

        Returns:
            DataFrame: DataFrame containing speed data for all buses, including Line,
            Brigade, Vehicle_number, Speed(km/h), Lon, and Lat columns.
        """
        list_of_data_frames: List[DataFrame] = []

        for line in self.busses.keys():
            for brigade in self.busses[line].keys():
                for vehicle_number in self.busses[line][brigade].keys():
                    speeding_df = self.busses[line][brigade][vehicle_number].get_busses_speed()

                    speeding_df['Line'] = line
                    speeding_df['Brigade'] = brigade
                    speeding_df['Vehicle_number'] = vehicle_number
                    list_of_data_frames.append(speeding_df)

        result: DataFrame = concat(list_of_data_frames, ignore_index=True)

        result = result.astype(dtype={'Speed(km/h)': float, 'Lon': float, 'Lat': float})

        if filter_speed is not None:
            cond = filter_speed(result['Speed(km/h)'])
            result = result[cond]

        return result.reset_index()

    def how_long_travel(self, start: datetime, stop: datetime, starting_complex_id: str) -> DataFrame:
        """Calculate the shortest travel time from a starting bus stop to all other bus stops.

           Args:
               start (datetime): The starting time.
               stop (datetime): The ending time.
               starting_complex_id (str): The identifier of the starting bus stop.

           Returns:
               DataFrame: DataFrame containing the shortest travel time from the starting bus stop
                   to all other bus stops.
        """
        if start.date() != self.date_dt.date():
            raise ValueError(f"ZTM object data: {self.date_dt.date()} is not equal {start.date}")

        # round start to whole minutes
        start -= timedelta(seconds=start.second, microseconds=start.microsecond)

        class BusStopNode:
            def __init__(self, bus_stops: List[BusStop], time: datetime,
                         all_busses_dict: Dict[Tuple[str, datetime], Self],
                         my_ztm: ZTM):
                self.bus_stops: List[BusStop] = bus_stops
                self.time: datetime = time
                self.minimal_time: int = int(1e6)
                self.all_busses_dict = all_busses_dict
                self.complex = bus_stops[0].complex
                self.my_ztm: ZTM = my_ztm

            def get_nbh(self) -> List[Tuple[int, Self]]:
                if (self.complex, self.time + timedelta(minutes=1)) not in self.all_busses_dict:
                    return []

                # I can wait at bus_stop for another minute
                result = [(1, self.all_busses_dict[(self.complex, self.time + timedelta(minutes=1))])]

                exact_bus_stop: BusStop
                for exact_bus_stop in self.bus_stops:
                    for line in exact_bus_stop.available_lines:
                        schedule: DataFrame = exact_bus_stop.schedules[line]
                        if schedule.empty:
                            continue
                        routes_leaving: Series = schedule.loc[schedule['czas'] == self.time.strftime("%H:%M:%S")][
                            'trasa']
                        for index, route in routes_leaving.items():
                            for key in self.my_ztm.routes[line][route].keys():
                                if self.my_ztm.routes[line][route][key]["nr_zespolu"] == self.complex:
                                    # jeśli jest następny przystanek 
                                    if str(int(key) + 1) in self.my_ztm.routes[line][route].keys():
                                        next_key: str = str(int(key) + 1)
                                        next_bus_stop_complex: str = self.my_ztm.routes[line][route][next_key][
                                            "nr_zespolu"]
                                        result.append((1, self.all_busses_dict[
                                            (next_bus_stop_complex, self.time + timedelta(minutes=1))]))
                return result

            def to_series_with_result(self) -> Series:
                example: BusStop = self.bus_stops[0]
                return Series({"complex": example.complex, "name_of_complex": example.complex_name,
                               "Lat": example.lat, "Lon": example.lon, "Time_from_source": self.minimal_time})

            def __lt__(self, other) -> bool:
                return self.complex < other.complex

        # generate graph:

        self.bus_stops.sort(key=operator.attrgetter("complex"))

        all_nodes: Dict[Tuple[str, datetime], BusStopNode] = dict()

        moment: datetime = start
        while moment <= stop:
            for k, group in itertools.groupby(self.bus_stops, key=lambda bs: bs.complex):
                all_nodes[(k, moment)] = BusStopNode(list(group), moment, all_nodes, self)
            moment += timedelta(minutes=1)

        # dijkstra algorithm

        all_nodes[(starting_complex_id, start)].minimal_time = 0

        prio_que = PriorityQueue(maxsize=4 * len(all_nodes))
        prio_que.put((0, all_nodes[(starting_complex_id, start)]))

        while not prio_que.empty():
            print(prio_que.qsize())
            element: Tuple[int, BusStopNode] = prio_que.get()
            time_in_minutes = element[0]
            bus_stop_node = element[1]

            time_to_bus: int
            nbh_bus_stops: BusStopNode
            for time_to_bus, nbh_bus_stops in bus_stop_node.get_nbh():
                new_time: int = time_in_minutes + time_to_bus
                if new_time < nbh_bus_stops.minimal_time:
                    nbh_bus_stops.minimal_time = new_time
                    prio_que.put((new_time, nbh_bus_stops))

        # find best results

        dict_of_best_results: Dict[str, BusStopNode] = dict()

        key: Tuple[str, datetime]
        value: BusStopNode
        for key, value in all_nodes.items():
            if key[0] not in dict_of_best_results.keys():
                dict_of_best_results[key[0]] = value
            elif dict_of_best_results[key[0]].minimal_time > value.minimal_time:
                dict_of_best_results[key[0]] = value

        return DataFrame([bus.to_series_with_result() for bus in dict_of_best_results.values()])

    def check_lateness(self, start: datetime, stop: datetime) -> DataFrame:
        """Analyze bus lateness at each bus stop within a specified time range.

            Args:
                start (datetime): The start of the time range.
                stop (datetime): The end of the time range.

            Returns:
                DataFrame: DataFrame containing information about bus lateness at each bus stop.
        """
        class BusStopLateness:
            def __init__(self, bus_stop: BusStop):
                self.bus_stop: BusStop = bus_stop
                self.list_of_late: List[int] = []
                self.busses_arrived: set = set()

            def analize(self, locations: DataFrame) -> None:
                # approximation of distance between points according to:
                # https://blog.mapbox.com/fast-geodesic-approximations-with-cheap-ruler-106f229ad016
                cond = np.sqrt((40075017.0 / 360.0 * np.abs(locations['Lon'] - self.bus_stop.lon) * np.cos(
                    (locations['Lat'] + self.bus_stop.lat) / 2)) ** 2
                               + (20003930.0 / 180.0 * np.abs(locations['Lat'] - self.bus_stop.lat)) ** 2) < 40

                busses_at_stop: DataFrame = locations.loc[cond]

                for index, row in busses_at_stop.iterrows():
                    line: str = row["Lines"]
                    vehicle_number: str = row['VehicleNumber']
                    brigade: str = row["Brigade"]
                    try:
                        time: datetime = datetime.strptime(row['Time'], "%Y-%m-%d %H:%M:%S")
                    except Exception:
                        continue

                    if line not in self.bus_stop.available_lines:
                        continue

                    if (line, vehicle_number, brigade) in self.busses_arrived:
                        continue

                    schedule: DataFrame = self.bus_stop.schedules[line]

                    def filter_fitting(series: Series):
                        scd_brigade = series['brygada']
                        try:
                            scd_time: datetime = datetime.strptime(start.strftime("%Y-%m-%d ") + series['czas'],
                                                                   "%Y-%m-%d %H:%M:%S")
                        except Exception:
                            new_hour: str = '0' + str(int(series['czas'][0:2]) % 24) + series['czas'][2:]
                            try:
                                scd_time: datetime = datetime.strptime(start.strftime("%Y-%m-%d ") + new_hour,
                                                                       "%Y-%m-%d %H:%M:%S")
                            except Exception:
                                return False

                        if scd_brigade != brigade:
                            return False

                        # assumption: buses doesn't departure more than two minute before schedule
                        if scd_time > time + timedelta(minutes=2):
                            return False

                        # assumption: if buss is 50 minutes late he might as well not have come (confusion with another)
                        if time > timedelta(minutes=50) + scd_time:
                            return False

                        return True

                    schedule = schedule[schedule.apply(filter_fitting, axis=1)]

                    if schedule.empty:
                        continue

                    schedule = schedule.sort_values(by='czas')

                    my_scheduled: Series = schedule.iloc[-1]

                    try:
                        my_scheduled_time = datetime.strptime(start.strftime("%Y-%m-%d ") + my_scheduled['czas'],
                                                              "%Y-%m-%d %H:%M:%S")
                    except Exception:
                        continue

                    self.busses_arrived.add((line, vehicle_number, brigade))

                    lateness: int = math.ceil((time - my_scheduled_time).total_seconds() / 60)
                    self.list_of_late.append(lateness)

            def result_series(self) -> Series:
                mean_lateness = 0
                if len(self.list_of_late) != 0:
                    mean_lateness = float(sum(self.list_of_late)) / len(self.list_of_late)

                return Series({'Lat': self.bus_stop.lat, 'Lon': self.bus_stop.lon, 'Complex': self.bus_stop.complex,
                               'stop_nr': self.bus_stop.stop_nr, 'complex_name': self.bus_stop.complex_name,
                               'mean_lateness': mean_lateness})

        bus_stops_late: List[BusStopLateness] = [BusStopLateness(bus_stop) for bus_stop in self.bus_stops]

        def round_to_ten_seconds(dt: datetime) -> datetime:
            tim_del = timedelta(seconds=dt.second % 10,
                                microseconds=dt.microsecond)
            return dt - tim_del

        start = round_to_ten_seconds(start)
        stop = round_to_ten_seconds(stop)

        actual_time: datetime = start
        while actual_time <= stop:
            print(actual_time)
            df1: DataFrame = DataFrame()
            df2: DataFrame = DataFrame()
            try:
                df1: DataFrame = self.get_save.get_online_location(1, from_date=actual_time, ret_as_data_frame=True)
            except Exception:
                pass

            try:
                df2: DataFrame = self.get_save.get_online_location(2, from_date=actual_time, ret_as_data_frame=True)
            except Exception:
                pass

            location_info: DataFrame = concat([df1, df2], ignore_index=True)

            if not location_info.empty:
                location_info = location_info.astype(dtype={"Lat": float, "Lon": float})

                bus_stop_late: BusStopLateness
                for bus_stop_late in bus_stops_late:
                    bus_stop_late.analize(location_info)

            actual_time += timedelta(seconds=10)

        return DataFrame([bus_stop_late.result_series() for bus_stop_late in bus_stops_late])

