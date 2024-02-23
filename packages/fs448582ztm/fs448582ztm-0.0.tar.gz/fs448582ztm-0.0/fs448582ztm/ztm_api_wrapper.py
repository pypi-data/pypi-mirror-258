import requests
from typing import TypeVar, Dict, List, Union, Optional, Callable, Any
from datetime import datetime, timedelta
import os
from os import path
import pandas
from functools import partial
from pandas import DataFrame, Series
import json
import time

Url_t = str
Bus_stop_t = Dict
path_t = str
Par_t = Union[int, str]  # requests.get parameter can be both int and string
Wrapper_data = Union[List[Dict[str, str]], List[str], Dict[str, Dict]]
Wrap_data_T = TypeVar('Wrap_data_T', List[Dict[str, str]], List[str], Dict[str, Dict], Dict[str, Dict[str, str]])


def read_api_key() -> str:
    with open(".api_key", "r") as f:
        return f.readline().strip(" \n")


class WrongMethodException(Exception):
    """Exception raised when 'Bledna Metoda' returned from request"""
    pass


class NoDataSavedException(Exception):
    """Exception raised when there is not data saved from demanded time"""
    pass


class WrapperZtm:
    """Wrapper for ZTM (Warsaw Public Transport) API.
    
    Attributes:
        api_key (str): The API key required for accessing the ZTM API.
    """

    def __init__(self, api_key: str):
        """Initialize WrapperZtm with API key.
        
        Parameters:
            api_key (str): The API key required for accessing the ZTM API.
        """
        self.api_key: Par_t = api_key

    URL_STOPS: Url_t = "https://api.um.warszawa.pl/api/action/dbstore_get"
    URL_ROUTES: Url_t = "https://api.um.warszawa.pl/api/action/public_transport_routes/?"
    URL_DICT: Url_t = "https://api.um.warszawa.pl/api/action/public_transport_dictionary/"
    URL_DBTIMETABLE: Url_t = 'https://api.um.warszawa.pl/api/action/dbtimetable_get'
    URL_BUS_STREAM: Url_t = 'https://api.um.warszawa.pl/api/action/busestrams_get'

    @classmethod
    def to_conv_form(cls, dictionary: Dict) -> Dict[str, str]:
        """Convert dictionary from received form to convenient form
        
        Parameters:
            dictionary (Dict): The dictionary in received format.

        Returns:
            Dict[str, str]: The dictionary in a more convenient format.
        """
        result: Dict = dict()
        for small_dict in dictionary['values']:
            result[small_dict['key']] = small_dict['value']
        return result

    @staticmethod
    def fail_retry(timeout: float, retry: int = 3):
        """Retry decorator for failed requests.
        
        Parameters:
            timeout (float): The initial timeout between retries.
            retry (int): The number of times to retry call the function.
        """

        def the_real_decorator(function):
            def wrapper(*args, **kwargs) -> Any:
                local_timeout: float = timeout
                retries = 0
                while retries < retry:
                    try:
                        return function(*args, **kwargs)
                    except WrongMethodException as e:
                        time.sleep(local_timeout)
                        local_timeout *= 1.5
                        retries += 1
                        if retries == retry:
                            raise e

            return wrapper

        return the_real_decorator

    @staticmethod
    def send_request(url: Url_t, params: Optional[Dict[str, Par_t]] = None) -> requests.Response:
        """Send HTTP GET request to the specified URL.
        
        Parameters:
            url (str): The URL to send the request to.
            params (Dict[str, Par_t]): Optional parameters to include in the request.

        Returns:
            requests.Response: The response object containing response of request.
        
        Raises:
            RuntimeError: If the HTTP response status code is not 200 or the response is 'false'.
        """
        if params is None:
            params = dict()

        s = requests.Session()
        s.headers = {
            'cookie': 'swp_token=1529318441:da348e5038f36f4e22e839d6e317852a:c8fe351689c07b18b38cf1bb7e6604ff',
            'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/116.0'
        }

        response: requests.Response = s.get(url, params=params)

        if response.status_code != 200:
            raise RuntimeError((f"status_code returned from requests.get({url}, {params})"
                                f"is not 200 ({response.status_code})"))

        if response.json()['result'] == 'false':
            raise RuntimeError(f"['result'] = false in requests.get({url}, {params})"
                               f"is not 200 ({response.status_code})")

        return response

    def api_get_bus_stop_complex(self, name_of_bus_stop: Par_t) -> List[Dict[str, str]]:
        """Get a list of bus stop complexes as dictionaries in the form:
                {'zespol': <complex_id>, 'nazwa': name_of_bus_stop}
            It is not guaranteed that all bus complexes with the current name will be included.

            Parameters:
                name_of_bus_stop (Par_t): The name of the bus stop.

            Returns:
                List[Dict[str, str]]: A list of bus stop complexes with their IDs and names.

            Raises:
                RuntimeError: If there was an error in the HTTP response.
        """
        params: Dict[str, Par_t] = {'apikey': self.api_key, 'name': name_of_bus_stop,
                                    'id': 'b27f4c17-5c50-4a5b-89dd-236b282bc499'}

        response: requests.Response = WrapperZtm.send_request(self.URL_DBTIMETABLE, params=params)

        return list(map(WrapperZtm.to_conv_form, response.json()['result']))

    def api_get_available_lines(self, bus_stop_id: Par_t, bus_stop_nr: Par_t) -> List[str]:
        """Get list of available lines from a bus stop.

        Parameters:
            bus_stop_id (Par_t): The id of the bus stop.
            bus_stop_nr (Par_t): The stop number of the bus stop.

        Returns:
            List[str]: A list of line numbers available at the specified bus stop.

        Raises:
            RuntimeError: If the API request fails or returns unexpected data.
        """
        params: Dict[str, Par_t] = {'apikey': self.api_key, 'busstopId': bus_stop_id,
                                    'busstopNr': bus_stop_nr,
                                    'id': '88cd555f-6f31-43ca-9de4-66c479ad5942'}

        response = WrapperZtm.send_request(self.URL_DBTIMETABLE, params=params)

        return list(map(lambda dict: dict['values'][0]['value'], response.json()['result']))

    def api_get_schedule(self, bus_stop_id: Par_t, bus_stop_nr: Par_t, line: Par_t) -> List[Dict[str, str]]:
        """Get schedule for a specific line from a bus stop in from of list of directiories: 
                 {'symbol_2': ..., 'symbol_1': ..., 'brygada': ..., 'kierunek': ..., 'trasa': ..., 'czas': 'H:%M:00'}

                 This method fetches the schedule for a given bus stop, line, and direction.

        Parameters:
            bus_stop_id (Par_t): The ID of the bus stop.
            bus_stop_nr (Par_t): The number of the bus stop.
            line (Par_t): The line number.

        Returns:
            List[Dict[str, str]]: A list of dictionaries containing schedule information.

        Raises:
            RuntimeError: If the API request fails or returns unexpected data.
        """
        params: Dict[str, Par_t] = {'apikey': self.api_key, 'busstopId': bus_stop_id,
                                    'busstopNr': bus_stop_nr, 'line': line,
                                    'id': 'e923fa0e-d96c-43f9-ae6e-60518c9f3238'}

        response = WrapperZtm.send_request(self.URL_DBTIMETABLE, params=params)

        return list(map(WrapperZtm.to_conv_form, response.json()['result']))

    @fail_retry(2, retry=3)
    def api_get_online_location(self, bus_or_tram: Par_t, line: Optional[Par_t] = None, brigade: Optional[Par_t] = None,
                                filter_current_data: bool = True, seconds_current: int = 60) -> List[Dict[str, str]]:
        """
            Gets online location of buses or trams.
 
            Parameters:
                bus_or_tram (Par_t): Indicates whether to fetch data for buses (1) or trams (2).
                line (Optional[Par_t], optional): The line number. Defaults to None.
                brigade (Optional[Par_t], optional): The brigade number. Defaults to None.
                filter_current_data (bool, optional): Whether to filter data based on current time. Defaults to True.
                seconds_current (int, optional): The threshold in seconds for considering data as current. Defaults to 60.
 
            Returns:
                List[Dict[str, str]]: A list of dictionaries containing online location data.
                    -> {'Lines': , 'Lon': , 'VehicleNumber':, 'Time': ', 'Lat': 52.26556, 'Brigade':}
 
            Raises:
                WrongMethodException: If the API request returns 'Bledna metoda'.
                RuntimeError: If the API request fails or returns unexpected data.
        """
        params: Dict[str, Par_t] = {'apikey': self.api_key, 'type': bus_or_tram,
                                    'resource_id': 'f2e5503e-927d-4ad3-9500-4ab9e55deb59'}
        if line:
            params['line'] = line

        if brigade:
            params['brigade'] = brigade

        result = self.send_request(self.URL_BUS_STREAM, params=params).json()['result']

        if any(s in result for s in ['Bledna metoda', 'Błędna metoda']):
            raise WrongMethodException('Request returned "Bledna metoda"')

        if filter_current_data:
            def is_time_diff_small(str_time: str) -> bool:
                try:
                    delta_time: timedelta = datetime.now() - datetime.strptime(str_time, "%Y-%m-%d %H:%M:%S")
                except ValueError as e:
                    # data are wrong 
                    return False
                return delta_time.total_seconds() <= seconds_current

            result = list(filter(lambda dct: is_time_diff_small(dct['Time']), result))

        return result

    def api_get_all_stops(self) -> List[Dict[str, str]]:
        """
        This method gets information about all bus stops.

        Returns:
            List[Dict[str, str]]: A list of dictionaries containing information about all bus stops.
                -> {'zespol': , 'slupek': , 'nazwa_zespolu': , 'id_ulicy': ,
                  'szer_geo': , 'dlug_geo': , 'kierunek': , 'obowiazuje_od': '2023-09-16 00:00:00.0'}

        Raises:
            RuntimeError: If the API request fails or returns unexpected data.
        """
        params: Dict[str, Par_t] = {'apikey': self.api_key,
                                    'id': 'ab75c33d-3a26-4342-b36a-6e5fef0a3ac3'}

        response: List[Dict] = WrapperZtm.send_request(self.URL_STOPS, params=params).json()['result']

        return list(map(self.to_conv_form, response))

    # Return nested dictiories,
    # where dict[<number_of_line>][<symbol_of_route>][<number_of_stop_on_route>] is a 
    # dictiorary in form: {'odleglosc': , 'ulica_id': , 'nr_zespolu': , 'typ': , 'nr_przystanku': }
    def api_get_routes(self) -> Dict[str, Dict[str, Dict[str, Dict]]]:
        """
        Get information about bus routes.

        Returns:
            Dict[str, Dict[str, Dict[str, Dict]]]: A nested dictionary containing information about bus routes.
                Where dict[<number_of_line>][<symbol_of_route>][<number_of_stop_on_route>] is a 
                dictiorary in form: {'odleglosc': , 'ulica_id': , 'nr_zespolu': , 'typ': , 'nr_przystanku': }.

        Raises:
            RuntimeError: If the API request fails or returns unexpected data.
        """
        params: Dict = {'apikey': self.api_key}
        return WrapperZtm.send_request(self.URL_ROUTES, params=params).json()['result']

    # Return dictionary has three keys: 'ulice', 'typy_przystankow', 'miejsca'
    # dict['ulice'] is a dictionary in form {<id_ulicy>: <nazwa_ulicy>}
    # dict['typy_przystankow'] is a dictionary in from {<'1' - '8'> : <typ_przystanku>}
    # dict['miejsca'] is a dictionary in from {<dwuliterowy literał> : <nazwa_miejsca>}
    def api_get_notation_dict(self) -> Dict[str, Dict[str, str]]:
        """
        Gets a dictionary of notation definitions.

        Returns:
            Dict[str, Dict[str, str]]: A dictionary containing notation definitions.
                    Return dictionary has three keys: 'ulice', 'typy_przystankow', 'miejsca'.
                    A dict['ulice'] is a dictionary in form {<id_ulicy>: <nazwa_ulicy>}
                    A dict['typy_przystankow'] is a dictionary in from {<'1' - '8'> : <typ_przystanku>}
                    A dict['miejsca'] is a dictionary in from {<dwuliterowy literał> : <nazwa_miejsca>}
            
        Raises:
            RuntimeError: If the API request fails or returns unexpected data.
        """
        params: Dict = {'apikey': self.api_key}
        return WrapperZtm.send_request(self.URL_DICT, params=params).json()['result']


class GetSaveApiZtmData:
    data_folder: path_t = "DATA"
    daily_data_folder: path_t = path.join(data_folder, "DAILY")
    localization_folder: path_t = path.join(data_folder, "LOCALIZATION")

    def __init__(self, api_key: str):
        self.wrapper_ztm: WrapperZtm = WrapperZtm(api_key)

    @staticmethod
    def __cache_data(get_remote_data: Callable[[], Wrap_data_T], file_path: path_t,
                     is_data_actual: Callable[[datetime, datetime], bool],
                     from_date: Optional[datetime] = None, override: bool = False,
                     is_list: bool = False, is_dict_list: bool = False, is_nested_dict: bool = False,
                     return_as_pandas: bool = False) -> Union[Wrap_data_T, Series, DataFrame]:
        if is_list + is_dict_list + is_nested_dict != 1:
            raise ValueError("exacly one of \'is_list\', \'is_dict_list\', \'is_nested_dict\' must be true")

        folder_path: path_t = os.path.dirname(file_path)

        if from_date == None:
            from_date = datetime.now()

        now: datetime = datetime.now()

        if not is_data_actual(now, from_date):
            override = False

        if path.exists(file_path) and not override:
            if is_list:
                result_s: Series = Series()
                try:
                    result_s = pandas.read_csv(file_path, sep=';', dtype=str, na_filter=False,
                                               header=None).squeeze()
                    # If file contain only one line...
                    if type(result_s) is str:
                        result_s = Series([result_s])
                except pandas.errors.EmptyDataError:
                    pass

                if return_as_pandas:
                    return result_s
                else:
                    return result_s.tolist()
            elif is_dict_list:
                result_df: DataFrame = DataFrame()
                try:
                    result_df = pandas.read_csv(file_path, sep=';', dtype=str, keep_default_na=False)
                except pandas.errors.EmptyDataError:
                    pass

                if return_as_pandas:
                    return result_df
                else:
                    return result_df.to_dict(orient="records")
            elif is_nested_dict:
                result: Dict = dict()
                with open(file_path) as json_file:
                    return json.load(json_file)
        else:
            if is_data_actual(now, from_date):
                if is_list:
                    my_list: List[str] = get_remote_data()
                    series: Series = Series(my_list, dtype=str)

                    os.makedirs(folder_path, exist_ok=True)
                    series.to_csv(file_path, sep=';', na_rep="", index=False, header=None)

                    series: Series = pandas.Series(my_list, dtype=str)

                    if return_as_pandas:
                        return series
                    else:
                        return my_list
                elif is_dict_list:
                    my_list: List[Dict[str, str]] = get_remote_data()
                    df: DataFrame = pandas.DataFrame(my_list, dtype=str)

                    os.makedirs(folder_path, exist_ok=True)
                    df.to_csv(file_path, sep=';', index=False)

                    if return_as_pandas:
                        return df
                    else:
                        return my_list
                elif is_nested_dict:
                    nested_dict: Dict[str, Dict[str, str]] = get_remote_data()

                    os.makedirs(folder_path, exist_ok=True)
                    with open(file_path, "w") as outfile:
                        json.dump(nested_dict, outfile)

                    return nested_dict
            else:
                raise NoDataSavedException(f"there is no data for avaliables lines from {from_date}")

    @staticmethod
    def __is_actual_daily(now: datetime, time_to_check: datetime):
        return time_to_check.date() == now.date()

    def get_available_lines(self, bus_stop_id: Par_t, bus_stop_nr: Par_t,
                            from_date: Optional[datetime] = None, override: bool = False,
                            ret_as_series: bool = False) -> Union[List[str], Series]:
        """
        Download available bus lines for a given bus stop from internet or if available from drive.

        Args:
            bus_stop_id (Par_t): The ID of the bus stop.
            bus_stop_nr (Par_t): The number of the bus stop.
            from_date (Optional[datetime], optional): The date from which to retrieve the data.
                Defaults to None (current date).
            override (bool, optional): Whether to override existing cached data. Defaults to False.
            ret_as_series (bool, optional): Whether to return the result as a Pandas Series. Defaults to False.

        Returns:
            Union[List[str], Series]: A list of available bus lines or a Pandas Series if ret_as_series is True.

        Raises:
            NoDataSavedException: If there is no data saved for the requested time period and cant download from internet.
            RuntimeError: If the API request fails or returns unexpected data.
        """
        if from_date == None:
            from_date = datetime.now()

        available_lines_folder: path_t = path.join(self.daily_data_folder, from_date.strftime('%d_%m_%y'), "AVA_LINES")
        available_lines_file: path_t = path.join(available_lines_folder, f"{bus_stop_id}_{bus_stop_nr}.csv")

        return self.__cache_data(partial(self.wrapper_ztm.api_get_available_lines, bus_stop_id, bus_stop_nr),
                                 available_lines_file, self.__is_actual_daily, is_list=True,
                                 return_as_pandas=ret_as_series,
                                 from_date=from_date, override=override)

    def get_all_stops(self, from_date: datetime = None,
                      override: bool = False, ret_as_data_frame: bool = False) -> Union[
        List[Dict[str, str]], DataFrame]:
        """
        Download list of all bus stops from internet or if available from drive.

        Args:
            from_date (Optional[datetime], optional): The date from which to retrieve the data.
                Defaults to None (current date).
            override (bool, optional): Whether to override existing cached data. Defaults to False.
            ret_as_data_frame (bool, optional): Whether to return the result as a Pandas Series. Defaults to False.

        Returns:
            Union[List[Dict[str, str]], DataFrame]: Information about all bus stops,
                either as a list of dictionaries or as a DataFrame.

        Raises:
            NoDataSavedException: If there is no data saved for the requested time period and cant download from internet.
            RuntimeError: If the API request fails or returns unexpected data.
        """
        if from_date is None:
            from_date = datetime.now()

        available_lines_folder: path_t = path.join(self.daily_data_folder, from_date.strftime('%d_%m_%y'))
        available_lines_file: path_t = path.join(available_lines_folder, "ALL_STOPS.csv")

        return self.__cache_data(self.wrapper_ztm.api_get_all_stops,
                                 available_lines_file, self.__is_actual_daily, is_dict_list=True,
                                 return_as_pandas=ret_as_data_frame,
                                 from_date=from_date, override=override)

    def get_bus_stop_complex(self, name_of_bus_stop: Par_t, from_date: datetime = None,
                             override: bool = False, ret_as_data_frame: bool = False) -> Union[
        List[Dict[str, str]], DataFrame]:
        """
        Download list of bus stop complexe from internet or if avaiable from drive.

        Args:
            name_of_bus_stop (Par_t): The name of the bus stop complex.
            from_date (Optional[datetime], optional): The date from which to retrieve the data.
                Defaults to None (current date).
            override (bool, optional): Whether to override existing cached data. Defaults to False.
            ret_as_data_frame (bool, optional): Whether to return the result as a Pandas Series. Defaults to False.

        Returns:
            Union[List[Dict[str, str]], DataFrame]: Information about the bus stop complex,
                either as a list of dictionaries or as a DataFrame.
        Raises:
            NoDataSavedException: If there is no data saved for the requested time period and cant download from internet.
            RuntimeError: If the API request fails or returns unexpected data.
        """
        if from_date == None:
            from_date = datetime.now()

        get_bus_stop_folder: path_t = path.join(self.daily_data_folder, from_date.strftime('%d_%m_%y'),
                                                "BUS_STOP_COMPLEXES")
        get_bus_stop_file: path_t = path.join(get_bus_stop_folder, f"{name_of_bus_stop}.csv")

        return self.__cache_data(partial(self.wrapper_ztm.api_get_bus_stop_complex, name_of_bus_stop),
                                 get_bus_stop_file, self.__is_actual_daily, is_dict_list=True,
                                 return_as_pandas=ret_as_data_frame,
                                 from_date=from_date, override=override)

    def get_online_location(self, bus_or_tram: Par_t, line: Optional[Par_t] = None, brigade: Optional[Par_t] = None,
                            from_date: datetime = None, filter_current_data: bool = True,
                            seconds_current: int = 60, override: bool = False,
                            ret_as_data_frame: bool = False) -> Union[List[Dict[str, str]], DataFrame]:
        """
        Download online location data for buses or trams from internet or if available from drive.

        Args:
            bus_or_tram (Par_t): Indicates whether to retrieve data for buses (1) or trams (2).
            line (Optional[Par_t], optional): The line number. Defaults to None.
            brigade (Optional[Par_t], optional): The brigade number. Defaults to None.
            from_date (datetime, optional): The date from which to retrieve the data. Defaults to None (current date).
            filter_current_data (bool, optional): Whether to filter data based on current time. Defaults to True.
            seconds_current (int, optional): The maximum difference in seconds between the data time and the current time.
                                            Defaults to 60.
            override (bool, optional): Whether to override existing cached data. Defaults to False.
            ret_as_data_frame (bool, optional): Whether to return the result as a Pandas Series. Defaults to False.

        Returns:
            Union[List[Dict[str, str]], DataFrame]: Online location data for buses or trams,
                                                    either as a list of dictionaries or as a DataFrame.

        Raises:
            NoDataSavedException: If there is no data saved for the requested time period and cant download from internet.
            WrongMethodException: If the API request returns 'Bledna metoda'.
            RuntimeError: If the API request fails or returns unexpected data.
        """
        if from_date is None:
            from_date = datetime.now()

        if line is not None or brigade is not None:
            result: List[Dict[str, str]]
            result = self.wrapper_ztm.api_get_online_location(bus_or_tram, line, brigade,
                                                              filter_current_data=filter_current_data,
                                                              seconds_current=seconds_current)
            if ret_as_data_frame:
                return pandas.DataFrame(result, dtype=str)
            else:
                return result

        def round_to_ten_seconds(dt: datetime) -> datetime:
            tim_del = timedelta(seconds=dt.second % 10,
                                microseconds=dt.microsecond)
            return dt - tim_del

        def is_actual_online(now: datetime, time_to_check: datetime):
            return round_to_ten_seconds(now) == round_to_ten_seconds(time_to_check)

        online_loc_folder: path_t = path.join(self.localization_folder,
                                              round_to_ten_seconds(from_date).strftime('%d_%m_%y'), str(bus_or_tram))
        online_loc_file: path_t = path.join(online_loc_folder,
                                            round_to_ten_seconds(from_date).strftime('%H:%M:%S') + '.csv')

        return self.__cache_data(partial(self.wrapper_ztm.api_get_online_location, bus_or_tram, None, None,
                                         filter_current_data=filter_current_data, seconds_current=seconds_current),
                                 online_loc_file, is_actual_online, is_dict_list=True,
                                 return_as_pandas=ret_as_data_frame,
                                 from_date=from_date, override=override)

    def get_schedule(self, bus_stop_id: Par_t, bus_stop_nr: Par_t, line: Par_t,
                     from_date: datetime = None, override: bool = False,
                     ret_as_data_frame: bool = False) -> Union[List[Dict[str, str]], DataFrame]:
        """
        Download schedule information for a specified bus stop and line from internet or if available from drive.

        Args:
            bus_stop_id (Par_t): The ID of the bus stop.
            bus_stop_nr (Par_t): The number of the bus stop.
            line (Par_t): The line number.
            from_date (Optional[datetime], optional): The date from which to retrieve the data.
                Defaults to None (current date).
            override (bool, optional): Whether to override existing cached data. Defaults to False.
            ret_as_data_frame (bool, optional): Whether to return the result as a Pandas Series. Defaults to False.

        Returns:
            Union[List[Dict[str, str]], DataFrame]: Information about the bus stop complex,
                either as a list of dictionaries or as a DataFrame.
        Raises:
            NoDataSavedException: If there is no data saved for the requested time period
                and cant download from internet.
            RuntimeError: If the API request fails or returns unexpected data.
        """
        if from_date is None:
            from_date = datetime.now()

        schedule_folder: path_t = path.join(self.daily_data_folder, from_date.strftime('%d_%m_%y'), "SCHEDULES")
        schedule_file: path_t = path.join(schedule_folder, f"{bus_stop_id}_{bus_stop_nr}_{line}.csv")

        return self.__cache_data(partial(self.wrapper_ztm.api_get_schedule, bus_stop_id=bus_stop_id,
                                         bus_stop_nr=bus_stop_nr, line=line),
                                 schedule_file, self.__is_actual_daily, is_dict_list=True,
                                 return_as_pandas=ret_as_data_frame,
                                 from_date=from_date, override=override)

    def get_routes(self, from_date: datetime = None,
                   override: bool = False) -> Dict[str, Dict[str, Dict[str, Dict]]]:
        """
        Download route information for all lines from internet or if available from drive.

        Args:
            from_date (datetime, optional): The date from which to retrieve the data. Defaults to None (current date).
            override (bool, optional): Whether to override existing cached data. Defaults to False.

        Returns:
            Dict[str, Dict[str, Dict[str, Dict]]]: Route information for all lines.

        Raises:
            NoDataSavedException: If there is no data saved for the requested time period and cant download from internet.
            RuntimeError: If the API request fails or returns unexpected data.
        """
        if from_date is None:
            from_date = datetime.now()

        routes_folder: path_t = path.join(self.daily_data_folder, from_date.strftime('%d_%m_%y'))
        routes_file: path_t = path.join(routes_folder, "ROUTES.json")

        return self.__cache_data(self.wrapper_ztm.api_get_routes,
                                 routes_file, self.__is_actual_daily, is_nested_dict=True,
                                 from_date=from_date, override=override)

    def get_notation_dict(self, from_date: datetime = None, override: bool = False) -> Dict[str, Dict[str, str]]:
        """
        Download a dictionary of notation codes from internet or if available from drive.

        Args:
            from_date (datetime, optional): The date from which to retrieve the data. Defaults to None (current date).
            override (bool, optional): Whether to override existing cached data. Defaults to False.

        Returns:
            Dict[str, Dict[str, str]]: A dictionary of notation codes.

        Raises:
            NoDataSavedException: If there is no data saved for the requested time period and cant download from internet.
            RuntimeError: If the API request fails or returns unexpected data.
        """
        if from_date is None:
            from_date = datetime.now()

        notation_dict_folder: path_t = path.join(self.daily_data_folder, from_date.strftime('%d_%m_%y'))
        notation_dict_file: path_t = path.join(notation_dict_folder, "NOTATNION_DICT.json")

        return self.__cache_data(self.wrapper_ztm.api_get_notation_dict,
                                 notation_dict_file, self.__is_actual_daily,
                                 is_nested_dict=True,
                                 from_date=from_date, override=override)
