"""
Helper functions for date manipulation
"""

from datetime import date, timedelta
from dateutil.easter import easter

def get_easter(year):
    """
    Returns the date easter occurs on for a given year as (month,day)
    """
    easter_date = easter(year)
    easter_month = easter_date.month
    easter_day = easter_date.day
    return easter_month, easter_day


def get_advent_sunday(year):
    """
    Return date of Advent Sunday, in days relative to Christmas day
    """
    return -(day_of_week(year,12,25) + 3*7)

def date_to_days(year, month, day):
    """
    Convert a date from year,month,day to days since 1st January, 1 AD
    """
    # Define a start date as passed in
    f_date = date(year, month, day)
    epoch = date(1, 1, 1)
    delta = f_date - epoch
    return delta.days

def day_of_week(year, month, day):
    """
    Return day of week for any given date in year,month,day format
    between 0-6 where 0 is Sunday, i.e. the first day of the week
    Compare with:
      weekday() which is 0-6 and 0 is Monday
      isoweekday() which is 1-7 and 1 is Monday
    """

    # Define a start date as passed in
    f_date = date(year, month, day)

    # Get ISO week day, in range 1-7
    weekday = f_date.isoweekday()

    # Rewrite 7=Sunday as 0=Sunday
    return 0 if weekday == 7 else weekday

def add_delta_days(days):
    """
    Convert days since 1st January, 1 AD back to year,month, day
    """
    epoch = date(1, 1, 1)
    end_date = epoch + timedelta(days=days)
    return end_date.year, end_date.month, end_date.day


def colour_code(colour):
    """
    Accept a colour name and return a colour code
    """
    codes = {
        'white': '#ffffff',
        'red': '#ce0002',
        'rose': '#eb597a',
        'purple': '#664fa6',
        'green': '#279942'
    }

    return codes.get(colour)
