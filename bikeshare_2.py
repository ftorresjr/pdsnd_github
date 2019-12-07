import time
from datetime import date
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!\n')
    # get user input for city (chicago, new york city, washington).
    #HINT: Use a while loop to handle invalid inputs
    print("We have data for three differenct cities; Chicago, New York City, Washington.")
    while True:
        city = input("Which city would you like to explore data for? ").lower()
        if city not in ('chicago', 'new york city', 'washington'):
            print("\nInvalid city. Please choose again.\n")
        else:
            print(f"\nYou selected {city.title()} for the city you would like to view data for.")
            print("If this is not correct, restart program by pressing \"CTRL + C\"")
            break
    while True:
        filters = input(f"""\nWould you like to filter the data for {city.title()} by month\
, day, or not at all?\n(for no filters enter \"none\"):\n""").lower()
        if filters not in ('month', 'day', 'none'):
            print("Not a valid option.")
        else:
            break

    # get user input for month (all, january, february, ... , june)
    if filters == 'month':
        while True:
            month = input("""\nWhich month would you like to filter by:
January, February, March, April, May, June: """).lower()
            print(f"Chosen month is {month.title()}.\n")
            if month not in ('january', 'february', 'march', 'april', 'may'
                             , 'june'):
                print("Invalid month. Please choose a valid month.\n")
            else:
                break
        day = 'all'
    # get user input for day of week (all, monday, tuesday, ... sunday)
    elif filters == 'day':
        while True:
            day = input(f"What day would you like to filter by?").lower()
            #print(f"Chosen day is {day}.")
            if day not in ('sunday', 'monday', 'tuesday', 'wednesday'
                           , 'thursday', 'friday', 'saturday'):
                print("Not a valid day of the week.")
            else:
                break
        month = 'all'
    else:
        month = 'all'
        day = 'all'

    print("\nFilters applied to search:")
    if month == 'all' and day == 'all':
        print(f"City = {city.title()}, Month = None, Day = None\n")
    elif month == 'all' and day != 'all':
        print(f"City = {city.title()}, Month = None, Day = {day.title()}\n")
    else:
        print(f"\nCity = {city.title()}, Month = {month.title()}, Day = None.\n")

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

    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dat
        df = df[df['day_of_week'] == day.title()]
    return df


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if month == 'all' and day == 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        most_common_month_values = df['month'].value_counts()
        #print(most_common_month_values)
        most_common_month = most_common_month_values.idxmax()
        month_count = most_common_month_values.max()
        #print("\nCheckpoint. Value of most common month is:", most_common_month)
        most_common_month = months[most_common_month - 1].title()
        print(f"The most traveled month: {most_common_month}")
        print(f"Total trips during {most_common_month}: {month_count}")

        # display the most common day of week
        most_common_dow_values = df['day_of_week'].value_counts()
        most_common_dow = most_common_dow_values.idxmax()
        dow_count = most_common_dow_values.max()
        print(f"\nThe most traveled day of the week: {most_common_dow}")
        print(f"Total trips during {most_common_dow}: {dow_count}.")

    elif month == 'all' and day != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        most_common_month_values = df['month'].value_counts()

        #print(most_common_month_values)
        most_common_month = most_common_month_values.idxmax()
        month_count = most_common_month_values.max()
        #print("\nCheckpoint. Value of most common month is:", most_common_month)
        most_common_month = months[most_common_month - 1].title()
        print(f"The most traveled month: {most_common_month}")
        print(f"Total trips during {most_common_month}: {month_count}")

    elif month != 'all' and day == 'all':
        # display the most common day of week
        most_common_dow_values = df['day_of_week'].value_counts()
        most_common_dow = most_common_dow_values.idxmax()
        dow_count = most_common_dow_values.max()
        print(f"\nThe most traveled day of the week: {most_common_dow}")
        print(f"Total trips during {most_common_dow}: {dow_count}.")

    # display the most common start hour
    most_common_hour_values = df['hour'].value_counts()
    #print("\nCheckpoint. Most common hour values:\n", most_common_hour_values)
    most_common_hour = most_common_hour_values.idxmax()
    hour_count = most_common_hour_values.max()
    #print("\nCheckpoint. Most traveled hour: ", most_common_hour)
    if most_common_hour < 12:
        print(f"\nThe most popular hour to start a trip: {most_common_hour} AM.")
        print(f"Total trips started during {most_common_hour} AM: {hour_count}")
    elif most_common_hour == 12:
        print(f"\nThe most popular hour to start a trip: Noon")
        print(f"Total trips started during Noon: {hour_count}")
    else:
        most_common_hour = most_common_hour - 12
        print(f"\nThe most popular hour to start a trip: {most_common_hour} PM.")
        print(f"Total trips started during {most_common_hour} PM: {hour_count}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("")
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    mc_st_station_values = df['Start Station'].value_counts()
    mc_st_station = mc_st_station_values.idxmax()
    mc_st_station_count = mc_st_station_values.max()
    print(f"Most popular start station: {mc_st_station}")
    print(f"Total trips started at {mc_st_station}: {mc_st_station_count}")
    # display most commonly used end station
    mc_en_station_values = df['End Station'].value_counts()
    mc_en_station = mc_en_station_values.idxmax()
    mc_en_station_count = mc_en_station_values.max()
    print(f"\nMost popular end station: {mc_en_station}")
    print(f"Total trips ended at {mc_en_station}: {mc_en_station_count}")

    # display most frequent combination of start station and end station trip
    print("\nMost popular trip from start to end")
    stat = df.groupby(['Start Station'])['End Station'].value_counts().idxmax()
    print(stat)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("")
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print(f"Total travel time of all trips (in minutes): {int(total_travel_time)}")

    #Display longest  trip
    longest_trip = df['Trip Duration'].max()
    print(f"\nLongest trip (in minutes): {int(longest_trip)}")

    #Display shortest  trip
    shortest_trip = df['Trip Duration'].min()
    print(f"\nShortest trip (in minutes): {int(shortest_trip)}")

    # display mean travel time
    avg_travel_time = int(df['Trip Duration'].mean())
    print(f"\nAverage length of a trip (in minutes): {avg_travel_time} ")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("")
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("Type of rider:")
    print(user_types.to_string())

    # Display counts of gender
    print("\nGender of rider:")
    gender_column = 'Gender' in df
    if gender_column:
        gender_count = df['Gender'].value_counts()
        print(gender_count.to_string())
    else:
        city = city.title()
        print(f"No Gender information is available for {city.title()}.")

    # Display earliest, most recent, and most common year of birth
    print("\nBirth Year:")
    birth = 'Birth Year' in df
    if birth:
        earliest = int(df['Birth Year'].max())
        oldest = int(df['Birth Year'].min())
        average = int(df['Birth Year'].mean())
        print(f"Youngest birth year of riders: {earliest}")
        print(f"Oldest birth year of riders: {oldest}")
        print(f"Average birth year of riders: {average}")
    #Display most common ages
        male = df[df['Gender'] == 'Male']
        female = df[df['Gender'] == 'Female']
        mode_male = male['Birth Year'].mode()
        mode_female = female['Birth Year'].mode()
        today = date.today()
        print(f"\nMost reoccuring age:\nMale subscribers: {today.year - int(mode_male)}")
        print(f"Female subscribers: {today.year - int(mode_female)}")
    else:
        print(f"No Birth Year information available for {city.title()}.")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print("")
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        df = pd.read_csv(CITY_DATA[city], na_filter=False)
        print(f"Below is some individual trip data for {city}.\n")
        index = 0
        nrows = 5
        print(df.iloc[index * nrows:(index+1) * nrows])
        index += 1
        while True:
            more_data = input("\nWould you like to view 5 more lines of rider data? Enter yes or no.? ")
            print("\n")
            if more_data.lower() != 'yes':
                break
            else:
                print(df.iloc[index * nrows:(index+1) * nrows])
                index += 1
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
