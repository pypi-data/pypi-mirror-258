import ztm_api_wrapper
from datetime import datetime, timedelta
from typing import Callable, List
import time
from threading import Thread
from pandas import DataFrame
import argparse


class Fetcher:
    """A class for fetching ZTM data using API calls."""
    def __init__(self, api_key: str):
        self.get_save = ztm_api_wrapper.GetSaveApiZtmData(api_key)

    @staticmethod
    def run_interval(save_function: Callable[[], None], start: datetime, stop: datetime,
                     delta_time: timedelta) -> None:
        """Run a function at regular intervals within a specified time range.

        Args:
            save_function (Callable[[], None]): The function to run at each interval.
            start (datetime): The start time of the interval.
            stop (datetime): The stop time of the interval.
            delta_time (timedelta): The time interval between function calls.
        """
        def sleep_till(till: datetime) -> None:
            seconds: float = (till - datetime.now()).total_seconds()
            if seconds > 0:
                time.sleep(seconds)

        if start < datetime.now():
            start = datetime.now()

        count_last_fails: int = 0
        next_call: datetime = start

        while next_call < stop:
            sleep_till(next_call)

            if not save_function():
                count_last_fails += 1
            else:
                count_last_fails = 0

            next_call = next_call + delta_time

            # If fetching data fails more than three times in row
            # I wait for another 10 seconds more. 
            if count_last_fails >= 3:
                print(f"waiting another {10 * (count_last_fails - 2)} seconds, couse failed 3 times in row")
                next_call += delta_time * (count_last_fails - 2)

    def fetch_period(self, start: datetime, stop: datetime, fetch_busses: bool = True,
                     fetch_trams: bool = True, fetch_meta_data: bool = True) -> None:
        """Fetch ZTM data for a specified time period.

        Args:
            start (datetime): The start time of the data fetching period.
            stop (datetime): The stop time of the data fetching period.
            fetch_busses (bool, optional): Whether to fetch bus location data. Defaults to True.
            fetch_trams (bool, optional): Whether to fetch tram location data. Defaults to True.
            fetch_meta_data (bool, optional): Whether to fetch metadata. Defaults to True.
        """
        if datetime.now() > start:
            start = datetime.now()

        def save_daily() -> bool:
            self.get_save.get_notation_dict()
            self.get_save.get_routes()

            all_stops: DataFrame = self.get_save.get_all_stops(ret_as_data_frame=True)
            all_stops.drop_duplicates(subset=["zespol", 'slupek'])

            for index, row in all_stops.iterrows():
                lines: List[str] = self.get_save.get_available_lines(row["zespol"], row["slupek"])
                for line in lines:
                    self.get_save.get_schedule(row["zespol"], row["slupek"], line)

            return True

        def save_busses_loc() -> bool:
            try:
                self.get_save.get_online_location(1)
            except ztm_api_wrapper.WrongMethodException:
                print(f"when fetching busses loc WrongMethodException occurred to many times time:{datetime.now()}")
                return False
            return True

        def save_tram_loc() -> bool:
            try:
                self.get_save.get_online_location(2)
            except ztm_api_wrapper.WrongMethodException:
                print(f"when fetching trams loc WrongMethodException occurred to many times time:{datetime.now()}")
                return False
            return True

        t_busses: Thread = Thread(target=self.run_interval, args=(save_busses_loc, start, stop, timedelta(seconds=20)))
        t_trams: Thread = Thread(target=self.run_interval, args=(save_tram_loc, start, stop, timedelta(seconds=20)))
        t_meta_data: Thread = Thread(target=self.run_interval, args=(save_daily, start, stop, timedelta(days=1)))

        if fetch_busses:
            t_busses.start()

        if fetch_trams:
            t_trams.start()

        if fetch_meta_data:
            t_meta_data.start()

        if fetch_busses:
            t_busses.join()

        if fetch_trams:
            t_trams.join()

        if fetch_meta_data:
            t_meta_data.join()


# example api key: "916c4bfe-396c-4203-b87b-5a68889e9dd5"
if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-a", nargs=1,
                        help="if flag then api needs to be added as second argument."
                             + "If not then api_key will be read from .api_key file")

    parser.add_argument("--start", nargs='?', const=None, default=None,
                        help="lets specify start date (format: YY-mm-dd/HH:MM:SS) (default: now)")
    parser.add_argument("--stop", nargs='?', const=None, default=None,
                        help="lets specify stop date (format: YY-mm-dd/HH:MM:SS) (default: now + 1 minute)")
    parser.add_argument("--no_busses", action="store_true", help="optional argument: turn off fetching busses")
    parser.add_argument("--no_trams", action="store_true", help="optional argument: turn off fetching trams")
    parser.add_argument("--no_meta", action="store_true", help="optional argument: turn off fetching metadata")

    args = parser.parse_args()

    api_key: str
    if args.a is None:
        api_key = ztm_api_wrapper.read_api_key()
    else:
        api_key = args.a[0]

    if args.start is None:
        args.start = datetime.now()
    else:
        args.start = datetime.strptime(args.start[0], "%Y-%m-%d/%H:%M:%S")

    if args.stop is None:
        args.stop = datetime.now() + timedelta(minutes=1)
    else:
        args.stop = datetime.strptime(args.stop[0], "%Y-%m-%d/%H:%M:%S")

    fetcher = Fetcher(api_key)
    fetcher.fetch_period(start=args.start, stop=args.stop, fetch_busses=(not args.no_busses),
                         fetch_trams=(not args.no_trams), fetch_meta_data=(not args.no_meta))
