# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import re
import pandas as pd


FILEPATH = '/home/kim/Documents/SWUS/WSLOGDec2023.csv'

OUTPUT_FILEPATH_TEMP = '/home/kim/Documents/SWUS/stats_temp.csv'
OUTPUT_FILEPATH_DIST = '/home/kim/Documents/SWUS/stats_dist.csv'
OUTPUT_COLUMNS = ['month', 'mean', 'min', 'max', 'count']


def print_df(df, num_rows=None):
    if num_rows:
        print(df[:num_rows].to_string())
    else:
        print(df.to_string())


# this isn't working yet
def fix_file_spacing():
    # the file is annoying and has no delimiter between the date and time values
    # so we need to add a delimiter using a regex expression
    newlines = []
    with open(FILEPATH, 'r') as f:
        for line in f:
            newline = re.sub(r'/(?<=[0-9]{4}/[0-9]{2}/[0-9]{2})(?=\S)', ' ', line, 1)
            newlines.append(newline)

    with open(FILEPATH, 'w') as f:
        for line in newlines:
            f.writelines(line)


def get_stats_row(df, column_name):
    stats = df[column_name].describe()
    date = df.iloc[0]['Date']
    # corresponds exactly to OUTPUT_COLUMNS
    # 'month', 'mean', 'min', 'max', 'count'
    return [
        f"{date.year}-{date.month}",
        round(stats['mean'], 1),
        int(stats['min']),
        int(stats['max']),
        int(stats['count']),
    ]


def do_stuff():
    # fix_file_spacing()

    # Load data from a space-separated text file
    df = pd.read_csv(
        FILEPATH,
        # the file is actually space-delimited so this argument will interpret it correctly
        delim_whitespace=True,
    )

    # convert to datetime
    df['Date'] = pd.to_datetime(df['Date'], format='%Y/%m/%d')

    print("First 10 rows:")
    print_df(df, 10)
    print()

    first_year = df['Date'].min().year
    last_year = df['Date'].max().year

    dist_stats = []
    temp_stats = []

    for year in range(first_year, last_year+1):
        for month in range(1, 13):
            month_data = df[(df['Date'].dt.year == year) & (df['Date'].dt.month == month)]
            if not month_data.empty:
                dist_stats.append(get_stats_row(month_data, 'Dist'))
                temp_stats.append(get_stats_row(month_data, 'Temp'))

    dist_stats_df = pd.DataFrame(dist_stats, columns=OUTPUT_COLUMNS)
    temp_stats_df = pd.DataFrame(temp_stats, columns=OUTPUT_COLUMNS)

    print_df(dist_stats_df, 10)
    print()
    print_df(temp_stats_df, 10)
    print()

    dist_stats_df.to_csv(OUTPUT_FILEPATH_DIST, index=False)
    temp_stats_df.to_csv(OUTPUT_FILEPATH_TEMP, index=False)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    do_stuff()
