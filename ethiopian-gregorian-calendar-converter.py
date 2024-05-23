import logging
from typing import List, Tuple

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

GREGORIAN_MONTHS = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

# Ethiopian month names mapping for Julian and Gregorian calendars
ETHIOPIAN_MONTHS_JULIAN = [
    "Tir-Yekatit", "Yekatit-Megabit", "Megabit-Meyazia", "Meyazia-Ginbot",
    "Ginbot-Sene", "Sene-Hamle", "Hamle-Nehase", "Nehase-Pagume-Meskerem",
    "Meskerem-Tikimt", "Tikimt-Hidar", "Hidar-Tahisas", "Tahisas-Tir"
]

ETHIOPIAN_MONTHS_GREGORIAN = [
    "Tahisas-Tir", "Tir-Yekatit", "Yekatit-Megabit", "Megabit-Meyazia",
    "Meyazia-Ginbot", "Ginbot-Sene", "Sene-Hamle", "Hamle-Nehase",
    "Nehase-Pagume-Meskerem", "Meskerem-Tikimt", "Tikimt-Hidar", "Hidar-Tahisas"
]

def main():
    while True:
        try:
            input_year = int(input("Enter a year (Julian or Gregorian / 0 to exit): "))
        except ValueError:
            print("Invalid input! Please enter a valid year.")
            continue
        
        if input_year == 0:
            break
        
        if input_year <= 0:
            print("You entered an invalid year!")
            continue

        leap_year_offset = get_leap_year_offset(input_year)
        is_julian_calendar, is_leap_year, is_ethiopian_leap_year = determine_leap_years(input_year)
        ethiopian_current_month, ethiopian_current_day = get_initial_ethiopian_date(is_leap_year, is_julian_calendar, leap_year_offset)
        
        gregorian_months_length = get_gregorian_months_length(is_leap_year, input_year)
        ethiopian_months = get_ethiopian_months(is_julian_calendar, input_year)

        start_days_of_month = calculate_start_days_of_month(input_year, is_julian_calendar, is_leap_year)
        ethiopian_days_of_year = fill_ethiopian_calendar(ethiopian_current_month, ethiopian_current_day, is_ethiopian_leap_year)

        display_calendars(input_year, GREGORIAN_MONTHS, ethiopian_months, gregorian_months_length, start_days_of_month, ethiopian_days_of_year)


def get_leap_year_offset(input_year: int) -> int:
    logging.debug(f"Calculating leap year offset for year: {input_year}")
    if input_year < 1900:
        return 1
    if input_year > 2100:
        return -1
    return 0


def determine_leap_years(input_year: int) -> Tuple[bool, bool, bool]:
    logging.debug(f"Determining leap year status for year: {input_year}")
    is_julian_calendar = (input_year <= 1752)
    is_leap_year = (input_year % 4 == 0) and (input_year % 100 != 0 or input_year % 400 == 0)
    is_ethiopian_leap_year = ((input_year + 1) % 4 == 0) and ((input_year + 1) % 100 != 0 or (input_year + 1) % 400 == 0)
    
    if is_julian_calendar:
        is_leap_year = input_year % 4 == 0
        is_ethiopian_leap_year = ((input_year + 1) % 4) == 0
    
    logging.debug(f"isJulianCalendar: {is_julian_calendar}, isLeapYear: {is_leap_year}, isEthiopianLeapYear: {is_ethiopian_leap_year}")
    return is_julian_calendar, is_leap_year, is_ethiopian_leap_year


def get_initial_ethiopian_date(is_leap_year: bool, is_julian_calendar: bool, leap_year_offset: int) -> Tuple[int, int]:
    logging.debug("Calculating initial Ethiopian date")
    ethiopian_current_month = 4
    ethiopian_current_day = 23 + leap_year_offset
    if is_leap_year and not is_julian_calendar:
        ethiopian_current_day = 22 + leap_year_offset
    if is_julian_calendar:
        ethiopian_current_month = 5
        ethiopian_current_day = 6
    return ethiopian_current_month, ethiopian_current_day


def get_gregorian_months_length(is_leap_year: bool, input_year: int) -> List[int]:
    logging.debug(f"Getting lengths of Gregorian months for year: {input_year}")
    months_length = [31, 29 if is_leap_year else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if input_year == 1752:
        months_length[8] = 19
    return months_length


def get_ethiopian_months(is_julian_calendar: bool, input_year: int) -> List[str]:
    logging.debug("Getting Ethiopian month names")
    if input_year == 1752:
        return ["Meskerem"]
    return ETHIOPIAN_MONTHS_JULIAN if is_julian_calendar else ETHIOPIAN_MONTHS_GREGORIAN


def calculate_start_days_of_month(input_year: int, is_julian_calendar: bool, is_leap_year: bool) -> List[int]:
    logging.debug("Calculating start days of each month")
    start_year_century = input_year // 100
    end_year_century = input_year % 100
    year_code = (end_year_century + (end_year_century // 4)) % 7
    century_code = (18 - start_year_century) % 7 if is_julian_calendar else (3 - (start_year_century % 4)) * 2
    month_codes = [0, 3, 3, 6, 1, 4, 6, 2, 5, 0, 3, 5]
    start_days_of_month = []

    for i in range(12):
        leap_year_code = -1 if is_leap_year and i < 2 else 0
        start_day = (year_code + month_codes[i] + century_code + 1 + leap_year_code) % 7
        start_days_of_month.append(start_day)

    logging.debug(f"Start days of the month: {start_days_of_month}")
    return start_days_of_month


def fill_ethiopian_calendar(ethiopian_current_month: int, ethiopian_current_day: int, is_ethiopian_leap_year: bool) -> List[int]:
    logging.debug("Filling Ethiopian calendar array")
    ethiopian_days_of_year = []
    for _ in range(366):
        ethiopian_days_of_year.append(ethiopian_current_day)
        ethiopian_current_day += 1

        if ethiopian_current_month == 13 and ethiopian_current_day == (7 if is_ethiopian_leap_year else 6):
            ethiopian_current_day = 1
            ethiopian_current_month = 1

        if ethiopian_current_day > 30:
            ethiopian_current_day = 1
            ethiopian_current_month += 1

    logging.debug(f"Ethiopian days of the year: {ethiopian_days_of_year[:12]}...")  # Displaying first 12 for brevity
    return ethiopian_days_of_year


def display_calendars(input_year: int, gregorian_months: List[str], ethiopian_months: List[str], 
                      gregorian_months_length: List[int], start_days_of_month: List[int], ethiopian_days_of_year: List[int]):
    logging.debug("Displaying calendars")
    total_days_passed = 0

    for month_index in range(12):
        print(f"\nGregorian Year: {input_year}")
        if input_year > 8:
            print(f"\tEthiopian Years: {input_year - 8} - {input_year - 7}")
        print(f"{gregorian_months[month_index]}\t\t{ethiopian_months[month_index] if input_year > 8 else ''}")
        print("|-------------------------------------------------------|")
        print("|Sun    |Mon    |Tue    |Wed    |Thu    |Fri    |Sat    |")
        print("|-------------------------------------------------------|")

        if month_index > 0:
            total_days_passed += gregorian_months_length[month_index - 1]
        
        day = 1
        first_day_of_month = start_days_of_month[month_index]
        days_in_month = gregorian_months_length[month_index]
        weeks_in_month = (first_day_of_month + days_in_month + 6) // 7
        reset_days = 7

        for week_index in range(weeks_in_month):
            if week_index == (weeks_in_month - 1):
                reset_days = ((first_day_of_month + days_in_month - 1) % 7) + 1

            print("|", end="")

            for day_of_week in range(7):
                if (week_index == 0 and day_of_week < first_day_of_month) or day > days_in_month:
                    print("       |", end="")
                else:
                    if input_year == 1752 and month_index == 8 and day >= 3:
                        print(f"{day + 11:>7}|", end="")
                    else:
                        print(f"{day:>7}|", end="")
                    day += 1
            print()
            if input_year > 8:
                print("|", end="")
                day -= reset_days
                for day_of_week in range(7):
                    if (week_index == 0 and day_of_week < first_day_of_month):
                        print("       |", end="")
                        day += 1
                    elif day > days_in_month:
                        print("       |", end="")
                    else:
                        print(f"{ethiopian_days_of_year[total_days_passed + day - 1]:<7}|", end="")
                        day += 1
                print()
            print("|-------------------------------------------------------|")

if __name__ == "__main__":
    main()
