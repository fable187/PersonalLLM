from datetime import datetime as dt
import time
import pytz

def utc_to_central(utc_timestamp):
    """
    Converts a UTC timestamp to US Central Time.

    Args:
        utc_timestamp (int or float): The UTC timestamp.

    Returns:
        datetime.datetime or str: The datetime object in US Central Time, or an error string.
    """
    try:
        utc_dt = dt.fromtimestamp(utc_timestamp, tz=pytz.utc)
        central_tz = pytz.timezone('US/Central')
        central_dt = utc_dt.astimezone(central_tz)
        return central_dt
    except (TypeError, ValueError) as e:
        return f"Error: Invalid timestamp - {e}"
    except pytz.exceptions.UnknownTimeZoneError:
        return "Error: Could not find timezone US/Central"

def unix_to_datetime_str(unix_timestamp, format_str="%Y-%m-%d %H:%M:%S"):
    """
    Converts a Unix timestamp to a datetime string.

    Args:
        unix_timestamp (int or float): The Unix timestamp.
        format_str (str): The desired datetime string format.

    Returns:
        str: The datetime string.
    """
    try:
        dt_object = dt.fromtimestamp(unix_timestamp)
        return dt_object.strftime(format_str)
    except (TypeError, ValueError) as e:
        return f"Error: Invalid timestamp or format - {e}"

def datetime_str_to_unix(datetime_str, format_str="%Y-%m-%d %H:%M:%S"):
    """
    Converts a datetime string to a Unix timestamp.

    Args:
        datetime_str (str): The datetime string.
        format_str (str): The format of the datetime string.

    Returns:
        int: The Unix timestamp.
    """
    try:
        dt_object = dt.strptime(datetime_str, format_str)
        return int(dt_object.timestamp())
    except (TypeError, ValueError) as e:
        return f"Error: Invalid datetime string or format - {e}"
    
def datetime_to_str(dt_object, format_str="%Y-%m-%d %H:%M:%S"):
    """
    Converts a datetime object to a string.

    Args:
        dt_object (datetime): The datetime object.
        format_str (str): The desired string format.

    Returns:
        str: The string representation of the datetime object.
        """
    return dt_object.strftime(format_str)