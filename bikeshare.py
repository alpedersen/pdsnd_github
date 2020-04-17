import time
import pandas as pd
import numpy as np
import datetime as dt
import click

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = ('january', 'february', 'march', 'april', 'may', 'june')

weekdays = ('sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday',
            'saturday')

def choice(prompt, choices=('yes', 'no')):
    """Return a valid input from the user given an array of possible answers.
    """

    while True:
        choice = input(prompt).lower().strip()
        # terminate the program if the input is end
        if choice == 'end':
            raise SystemExit
        # triggers if the input has only one name
        elif ',' not in choice:
            if choice in choices:
                break
        # triggers if the input has more than one name
        elif ',' in choice:
            choice = [i.strip().lower() for i in choice.split(',')]
            if list(filter(lambda x: x in choices, choice)) == choice:
                break

        prompt = ("\nThe choice you have entered is not valid. Please try again:\n>")

    return choice

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print("\n\nWelcome to the database for US bikeshare data.\n")

print("If you would like to exit this program, please type end at anytime.\n")

while True:
        city = choice("\nFor what city or cities do you want to see data from, New York City, Chicago or Washington? Use commas if there is more than one city.\n>", CITY_DATA.keys())
        month = choice("\nWhich month or months would you like to look at? Your choices are January - June. Add commas between names if there is more than one.\n>", months)
        day = choice("\nWhat day or days of the week would you like to examine? Please add a comma inbetween names if more than one.\n>", weekdays)

        # confirm the user input
        confirmation = choice("\nPlease confirm that you would like to apply the following filter(s) to the bikeshare data."
                              "\n\n City(ies): {}\n Month(s): {}\n Weekday(s)"
                              ": {}\n\n [y] Yes\n [n] No\n\n>"
                              .format(city, month, day))
        if confirmation == 'y':
            break
        else:
            print("\nOK, Let's start over.")

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """


    print("\nPlease wait as the program loads the data for your filtered criteria.")
    start_time = time.time()

    # filter the data according to the selected city filters
    if isinstance(city, list):
        df = pd.concat(map(lambda city: pd.read_csv(CITY_DATA[city]), city),
                       sort=True)
        # reorganize DataFrame columns after a city concat
        try:
            df = df.reindex(columns=['Unnamed: 0', 'Start Time', 'End Time',
                                     'Trip Duration', 'Start Station',
                                     'End Station', 'User Type', 'Gender',
                                     'Birth Year'])
        except:
            pass
    else:
        df = pd.read_csv(CITY_DATA[city])

    # create columns to display useful statistics
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month
    df['Weekday'] = df['Start Time'].dt.weekday_name
    df['Start Hour'] = df['Start Time'].dt.hour

    # filter the data according to month and weekday into two new DataFrames
    if isinstance(month, list):
        df = pd.concat(map(lambda month: df[df['Month'] ==
                           (months.index(month)+1)], month))
    else:
        df = df[df['Month'] == (months.index(month)+1)]

    if isinstance(day, list):
        df = pd.concat(map(lambda day: df[df['Weekday'] ==
                           (day.title())], day))
    else:
        df = df[df['Weekday'] == day.title()]

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print("\nCalculating The Most Frequent Times of Travel...\n")
    start_time = time.time()

most_common_month = df['Month'].mode()[0]
    print("For your current filter, the most popular month was: " +
          str(months[most_common_month-1]).title() + '.')

most_common_day = df['Weekday'].mode()[0]
    print("For your current filter, the most popular day was: " +
          str(most_common_day) + '.')

most_common_hour = df['Start Hour'].mode()[0]
    print("For your current filter, the most popular hour was: ": ' +
          str(most_common_hour) + '.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print("\nCalculating The Most Popular Stations and Trip...\n")
    start_time = time.time()

most_common_start_station = str(df['Start Station'].mode()[0])
    print("For your current filter, the most common start station is: " +
          most_common_start_station)

most_common_end_station = str(df['End Station'].mode()[0])
    print("For your current filter, the most common end station is: " +
          most_common_end_station)

df['Start-End Combination'] = (df['Start Station'] + ' - ' + df['End Station'])
most_common_start_end_combination = str(df['Start-End Combination'].mode()[0])
    print("For your current filter, the most common start-end combination of stations is: " +
          most_common_start_end_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print("\nCalculating Trip Duration...\n")
    start_time = time.time()

total_travel_time = df['Trip Duration'].sum()
    total_travel_time = (str(int(total_travel_time//86400)) +
                         'd ' +
                         str(int((total_travel_time % 86400)//3600)) +
                         'h ' +
                         str(int(((total_travel_time % 86400) % 3600)//60)) +
                         'm ' +
                         str(int(((total_travel_time % 86400) % 3600) % 60)) +
                         's')
    print("For your current filter, the total travel time is : " +
          total_travel_time + ".")

mean_travel_time = df['Trip Duration'].mean()
    mean_travel_time = (str(int(mean_travel_time//60)) + 'm ' +
                        str(int(mean_travel_time % 60)) + 's')
    print("For your current filter, the mean travel time is : " +
          mean_travel_time + ".")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print("\nCalculating User Stats...\n")
    start_time = time.time()

user_types = df['User Type'].value_counts().to_string()
    print("Distribution by user:")
    print(user_types)

try:
        gender_distribution = df['Gender'].value_counts().to_string()
        print("\nDistribution by gender:")
        print(gender_distribution)
    except KeyError:
        print("Unfortunately, there is no data of user genders for {}."
              .format(city.title()))

try:
        earliest_birth_year = str(int(df['Birth Year'].min()))
        print("\nFor your current filter, the oldest person to ride was born in: " + earliest_birth_year + ".")
        most_recent_birth_year = str(int(df['Birth Year'].max()))
        print("\nFor your current filter, the youngest person to ride was born in: " + most_recent_birth_year + ".")
        most_common_birth_year = str(int(df['Birth Year'].mode()[0]))
        print("For your current filter, the most common birth year amongst riders was: " + most_common_birth_year + ".")
    except:
        print("Unfortunately, there is no data for birth year in {}."
              .format(city.title()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df, mark_place):
    """Display 5 line of sorted raw data each time."""

    print("\nYou have chosen to view the raw data.")

    # this variable holds where the user last stopped
    if mark_place > 0:
        last_place = choice("\nWould you like to continue from where you stopped last time? \n [y] Yes\n [n] No\n\n>")
        if last_place == 'n':
            mark_place = 0

    # sort data by column
    if mark_place == 0:
        sort_df = choice("\nHow would you like to sort the way the data is displayed in the dataframe? Hit Enter to view unsorted.\n \n [st] Start Time\n [et] End Time\n [td] Trip Duration\n [ss] Start Station\n "
                         "[es] End Station\n\n>", ('st', 'et', 'td', 'ss', 'es', ''))

        asc_or_desc = choice("\nWould you like it to be sorted ascending or descending? \n [a] Ascending\n [d] Descending\n\n>", ('a', 'd'))

        if asc_or_desc == 'a':
            asc_or_desc = True
        elif asc_or_desc == 'd':
            asc_or_desc = False

        if sort_df == 'st':
            df = df.sort_values(['Start Time'], ascending=asc_or_desc)
        elif sort_df == 'et':
            df = df.sort_values(['End Time'], ascending=asc_or_desc)
        elif sort_df == 'td':
            df = df.sort_values(['Trip Duration'], ascending=asc_or_desc)
        elif sort_df == 'ss':
            df = df.sort_values(['Start Station'], ascending=asc_or_desc)
        elif sort_df == 'es':
            df = df.sort_values(['End Station'], ascending=asc_or_desc)
        elif sort_df == '':
            pass

    # each loop displays 5 lines of raw data
    while True:
        for i in range(mark_place, len(df.index)):
            print("\n")
            print(df.iloc[mark_place:mark_place+5].to_string())
            print("\n")
            mark_place += 5

            if choice("Do you want to keep printing raw data?\n\n[y]Yes\n[n]No\n\n>") == 'y':
                continue
            else:
                break
        break

    return mark_place

def main():
    while True:
        click.clear()
        city, month, day = get_filters()
        df = load_data(city, month, day)

        mark_place = 0
        while True:
            select_data = choice("\nPlease select the stats you would like to see.\n\n [ts] Time\n [ss] Station\n [tds] Trip Duration\n "
                                 "[us] User\n [rd] Display Raw Data\n [r] Restart\n\n>", ('ts', 'ss', 'tds', 'us', 'rd', 'r'))
            click.clear()
            if select_data == 'ts':
                time_stats(df)
            elif select_data == 'ss':
                station_stats(df)
            elif select_data == 'tds':
                trip_duration_stats(df)
            elif select_data == 'us':
                user_stats(df, city)
            elif select_data == 'rd':
                mark_place = raw_data(df, mark_place)
            elif select_data == 'r':
                break

        restart = choice("\nWould you like to restart?\n\n[y]Yes\n[n]No\n\n>")
        if restart.lower() != 'y':
            break

if __name__ == "__main__":
	main()
