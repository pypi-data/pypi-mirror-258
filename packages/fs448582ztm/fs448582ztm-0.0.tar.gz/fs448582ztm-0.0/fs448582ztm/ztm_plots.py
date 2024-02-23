import pandas
from pandas import DataFrame, Series
import plotly.express as px
import ztm_api_wrapper
import os.path
from ztm_classes import ZTM
from datetime import datetime
from typing import Callable, Dict, List, Tuple
from geopy.geocoders import Nominatim
import argparse

MAX_REASONABLE_SPEED: float = 170


class ZtmPlots:
    def __init__(self, api_key: str):
        """
        Initializes the ZtmPlots object.

        Args:
            api_key (str): The API key for accessing ZTM data.
        """
        self.get_save = ztm_api_wrapper.GetSaveApiZtmData(api_key)

    def all_bus_stop_plot(self, file_path: os.path, to_file: bool = False) -> None:
        """
        Generates a scatter plot of all bus stops.

        Args:
            file_path (os.path): The path to save the plot file.
            to_file (bool, optional): If True, saves the plot as an image file otherwise to html file. Defaults to False.
        """
        print("FETCH BUS STOP LOCATIONS")
        pd: DataFrame = self.get_save.get_all_stops(ret_as_data_frame=True).astype(
            {"szer_geo": "float", "dlug_geo": "float"})

        print("VISUALIZE")

        fig = px.scatter_mapbox(pd, lat='szer_geo', lon='dlug_geo', color_discrete_sequence=["#D2122E"],
                                hover_data=['nazwa_zespolu', 'slupek', 'kierunek'], zoom=10, width=1980, height=1080)
        fig = fig.update_traces(marker={"size": 4})
        fig.update_layout(mapbox_style="open-street-map")
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

        if to_file:
            fig.write_image(file_path + ".png", format='png', engine='kaleido')
        else:
            fig.write_html(file_path + ".html")

    def current_bus_loc_plot(self, file_path: os.path, to_file: bool = False) -> None:
        """
        Generates a scatter plot of current bus locations.

        Args:
            file_path (os.path): The path to save the plot file.
            to_file (bool, optional): If True, saves the plot as an image file otherwise to html file. Defaults to False.
        """
        print("FETCH ONLINE LOCATIONS")
        pd_busses: DataFrame = self.get_save.get_online_location(1, ret_as_data_frame=True)
        pd_trams: DataFrame = self.get_save.get_online_location(2, ret_as_data_frame=True)
        pd: DataFrame = pandas.concat([pd_busses, pd_trams])

        print("VISUALIZE")
        pd = pd.astype(dtype={"Lat": 'float', "Lon": float})

        fig = px.scatter_mapbox(pd, lat='Lat', lon='Lon', color_discrete_sequence=["#D2122E"],
                                hover_data=['Lines', 'VehicleNumber', 'Brigade', 'Time'], zoom=10,
                                width=1980, height=1080)
        fig = fig.update_traces(marker={"size": 4})
        fig.update_layout(mapbox_style="open-street-map")
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

        if to_file:
            fig.write_image(file_path + ".png", format='png', engine='kaleido')
        else:
            fig.write_html(file_path + ".html")

    def busses_speeding_plot(self, start: datetime, stop: datetime, file_path, to_file: bool = False,
                             custom_filter_speed: Callable[[float], bool] = None) -> None:
        """
        Generates a density map plot showing buses speeding between the specified start and stop times.

        Args:
            start (datetime): The start time of the data analysis.
            stop (datetime): The stop time of the data analysis.
            file_path (str): The path to save the plot file.
            to_file (bool, optional): If True, saves the plot as an image file otherwise to html file. Defaults to False.
            custom_filter_speed (Callable[[float], bool], optional): A custom filter function for bus speeds.
                Defaults to None.
        """
        if start.date() != stop.date():
            raise ValueError("Can analise only data during one day")

        if custom_filter_speed is None:
            custom_filter_speed = lambda s: ((s > 50) & (s < MAX_REASONABLE_SPEED))

        print("FETCHING DATA FROM DRIVE/INTERNET")
        my_ztm = ZTM(start.date(), self.get_save, read_meta=False)

        print("START OF CALCULATIONS")
        my_ztm.add_all_loc_period(start, stop)
        df: DataFrame = my_ztm.all_busses_speed(filter_speed=custom_filter_speed)
        print("END OF CALCULATIONS")

        print("START OF VISUALISATION")

        fig = px.density_mapbox(df, lat="Lat", lon="Lon", z="Speed(km/h)", radius=6, mapbox_style="open-street-map",
                                hover_data=['Time', 'Line', 'Brigade', 'Vehicle_number'])
        if to_file:
            fig.write_image(file_path + ".png", format='png', engine='kaleido')
        else:
            fig.write_html(file_path + ".html")

        print("END OF VISUALISATION")

    def most_speeding_places(self, start: datetime, stop: datetime, file_path, to_file: bool = False,
                             custom_filter_speed: Callable[[float], bool] = None) -> None:
        """
        Generates a bar plot showing the places where buses are most frequently speeding between the
        specified start and stop times.

        Args:
            start (datetime): The start time of the data analysis.
            stop (datetime): The stop time of the data analysis.
            file_path (str): The path to save the plot file.
            to_file (bool, optional): If True, saves the plot as an image file otherwise to html file. Defaults to False.
            custom_filter_speed (Callable[[float], bool], optional): A custom filter function for bus speeds.
                Defaults to None.
        """
        if start.date() != stop.date():
            raise ValueError("Can analise only data during one day")

        if custom_filter_speed is None:
            custom_filter_speed = lambda s: ((s > 50) & (s < MAX_REASONABLE_SPEED))

        print("FETCHING DATA FROM DRIVE/INTERNET")
        my_ztm = ZTM(start.date(), self.get_save, read_meta=False)
        my_ztm.add_all_loc_period(start, stop)

        print("START OF CALCULATIONS")
        print("GET_SPEED INFO")
        speed_info: DataFrame = my_ztm.all_busses_speed(filter_speed=custom_filter_speed)

        number_of_speeding: Dict[str, int] = dict()
        geolocator = Nominatim(user_agent="Warsaw_api_apt")
        print("CONTINUE CALCULATIONS")

        def count_speeding(series: Series) -> None:
            lon: str = str(series["Lon"])
            lat: str = str(series["Lat"])

            location = geolocator.reverse(lat + ", " + lon)

            street_or_location: str
            if "road" in location.raw["address"]:
                street_or_location = location.raw["address"]["road"]
            else:
                street_or_location = list(location.raw["address"].keys())[0]

            if street_or_location in number_of_speeding:
                number_of_speeding[street_or_location] += 1
            else:
                number_of_speeding[street_or_location] = 1

        speed_info.apply(count_speeding, axis=1)

        print("END OF CALCULATIONS")

        fig = px.bar(Series(number_of_speeding))

        if to_file:
            fig.write_image(file_path + ".png", format='png', engine='kaleido')
        else:
            fig.write_html(file_path + ".html")

    def speeding_percent(self, start: datetime, stop: datetime, file_path, to_file: bool = False) -> None:
        """
        Generates a density map plot showing the percentage of buses speeding at different locations between the
        specified start and stop times.

        Args:
            start (datetime): The start time of the data analysis.
            stop (datetime): The stop time of the data analysis.
            to_file (bool, optional): If True, saves the plot as an image file otherwise to html file. Defaults to False.
            file_path (str): The path to save the plot file.
        """
        if start.date() != stop.date():
            raise ValueError("Can analise only data during one day")

        print("FETCHING DATA FROM DRIVE/INTERNET")
        my_ztm = ZTM(start.date(), self.get_save, read_meta=False)
        my_ztm.add_all_loc_period(start, stop)

        print("START OF CALCULATIONS")
        speed_info: DataFrame = my_ztm.all_busses_speed()

        number_of_speeding: Dict[Tuple[float, float], List[int]] = dict()

        def count_speeding(series: Series) -> None:
            lon: float = series["Lon"]
            lat: float = series["Lat"]
            speed: float = series["Speed(km/h)"]

            lon = round(lon, 2)
            lat = round(lat, 2)

            tup: Tuple[float, float] = (lat, lon)

            if tup not in number_of_speeding:
                number_of_speeding[tup] = [0, 0]

            number_of_speeding[tup][0] += 1

            if 50 < speed < MAX_REASONABLE_SPEED:
                number_of_speeding[tup][1] += 1

        speed_info.apply(count_speeding, axis=1)

        percent_dict: List[dict[str, float]] = []

        for tup_lat_lon, list_all_spd in number_of_speeding.items():
            percent_dict.append({'Lat': tup_lat_lon[0], 'Lon': tup_lat_lon[1],
                                 'percent': float(list_all_spd[1]) / list_all_spd[0]})

        print("END OF CALCULATIONS")

        fig = px.density_mapbox(DataFrame(percent_dict, dtype=float), lon='Lon', lat="Lat", z='percent',
                                mapbox_style="open-street-map", radius=10)

        if to_file:
            fig.write_image(file_path + ".png", format='png', engine='kaleido')
        else:
            fig.write_html(file_path + ".html")

    def plot_how_long_to_travel(self, start: datetime, stop: datetime, starting_complex_id: str,
                                file_path: str, to_file: bool = False) -> None:
        """
        Generates a scatter plot showing the time it takes for buses to travel from a specified starting complex
        to other locations.

        Args:
            start (datetime): The start time of the data analysis.
            stop (datetime): The maximal time specifying how deep dijkstra will go
            starting_complex_id (str): The ID of the starting complex.
            file_path (str): The path to save the plot file.
            to_file (bool, optional): If True, saves the plot as an image file. Defaults to False.

        """
        print("FETCHING DATA FROM DRIVE/INTERNET")
        my_ztm = ZTM(start.date(), self.get_save)

        print("START OF CALCULATIONS")
        how_long_info: DataFrame = my_ztm.how_long_travel(start, stop, starting_complex_id)
        print("END OF CALCULATIONS")

        how_long_info = how_long_info.astype({"Lon": float, "Lat": float, "Time_from_source": float})
        how_long_info = how_long_info.query('Time_from_source != 1000000')

        fig = px.scatter_mapbox(how_long_info, lat='Lat', lon='Lon', color='Time_from_source',
                                hover_data=['complex', 'name_of_complex'], zoom=10,
                                width=1980, height=1080, color_continuous_scale='Reds', range_color=[0, 140])
        fig.update_layout(mapbox_style="open-street-map")
        fig = fig.update_traces(marker={"size": 12})

        if to_file:
            fig.write_image(file_path + ".png", format='png', engine='kaleido')
        else:
            fig.write_html(file_path + ".html")

    def plot_lateness(self, start: datetime, stop: datetime, file_path: str, to_file: bool = False) -> None:
        print("FETCHING DATA FROM DRIVE/INTERNET")
        my_ztm = ZTM(start.date(), self.get_save)

        print("START OF CALCULATIONS")
        avg_lateness_info: DataFrame = my_ztm.check_lateness(start, stop)
        print("END OF CALCULATIONS")

        avg_lateness_info = avg_lateness_info.astype({"Lon": float, "Lat": float, "mean_lateness": float})

        fig = px.scatter_mapbox(avg_lateness_info, lat='Lat', lon='Lon', color='mean_lateness',
                                hover_data=['complex_name', 'Complex', 'stop_nr'], zoom=10,
                                width=1980, height=1080, color_continuous_scale='Reds', range_color=[0, 20])
        fig.update_layout(mapbox_style="open-street-map")
        fig = fig.update_traces(marker={"size": 12})

        if to_file:
            fig.write_image(file_path + ".png", format='png', engine='kaleido')
        else:
            fig.write_html(file_path + ".html")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("plot", help="plot time to produce should be in [lateness, speeding_percent,"
                                     + "most_speeding_places, busses_speeding_plot, current_bus_loc_plot,"
                                     + "all_bus_stop_plot, travel_long]")
    parser.add_argument("path_file", help="specify path to file")

    parser.add_argument("-a", nargs=1,
                        help="if flag then api needs to be added as second argument."
                             + "If not then api_key will be read from .api_key file")

    parser.add_argument("--start", nargs=1,
                        help="obligatory argument if plot is not in [current_bus_loc_plot,"
                             + "all_bus_stop_plot]. specify start time (format: YY-mm-dd/HH:MM:SS) (default: now)")
    parser.add_argument("--stop", nargs=1,
                        help="obligatory argument if plot is not in [current_bus_loc_plot,"
                             + "all_bus_stop_plot]. If plot is 'travel_long' then stop will be treated like maximal_time"
                             + ". specify stop time (format: YY-mm-dd/HH:MM:SS) (default: now)")
    parser.add_argument("-p", action="store_true", help="if specified then plot will be save as .png file")

    parser.add_argument("-x", help="this flag precedes value of starting_complex_id if plot"
                                   + "is set to 'travel_long'. Then this flag is obligatory.")

    args = parser.parse_args()

    api_key: str
    if args.a is None:
        api_key = ztm_api_wrapper.read_api_key()
    else:
        api_key = args.a[0]

    start: datetime = datetime.strptime(args.start[0], "%Y-%m-%d/%H:%M:%S")
    stop: datetime = datetime.strptime(args.stop[0], "%Y-%m-%d/%H:%M:%S")

    ztm_plots = ZtmPlots(api_key)

    if args.plot == 'lateness':
        ztm_plots.plot_lateness(start, stop, args.path_file, to_file=args.p)
    elif args.plot == 'speeding_percent':
        ztm_plots.speeding_percent(start, stop, args.path_file, to_file=args.p)
    elif args.plot == 'busses_speeding_plot':
        ztm_plots.busses_speeding_plot(start, stop, args.path_file, to_file=args.p)
    elif args.plot == 'most_speeding_places':
        ztm_plots.most_speeding_places(start, stop, args.path_file, to_file=args.p)
    elif args.plot == 'current_bus_loc_plot':
        ztm_plots.current_bus_loc_plot(args.path_file, to_file=args.p)
    elif args.plot == 'all_bus_stop_plot':
        ztm_plots.all_bus_stop_plot(args.path_file, to_file=args.p)
    elif args.plot == 'travel_long':
        ztm_plots.plot_how_long_to_travel(start, stop, args.x, args.path_file, to_file=args.p)
    else:
        raise ValueError("plot is forbidden value")
