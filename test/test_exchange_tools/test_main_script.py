import unittest
from exchange_tools.main_script import main, prepare_time_range_parameters
from common.date_utils import *
from datetime import datetime as dt, timedelta


class TestMainScript(unittest.TestCase):
    
    def test_main(self):
        to_time = dt.now()
        from_time = to_time - timedelta(minutes=1)
        start_unix_timestamp, end_unix_timestamp = prepare_time_range_parameters(datetime_to_str(from_time), datetime_to_str(to_time))
        date_df = main(start_unix_timestamp, end_unix_timestamp)
        print('hold')

    