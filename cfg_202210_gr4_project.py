import csv
import os.path
import seaborn as sns
import pandas as pd


def read_data():
    """reads input csv file, get all data in the file into a list of dictionaries, each dictionary is each row"""
    data = []
    with open('transparency_active.csv', 'r') as csv_file:
        spreadsheet = csv.DictReader(csv_file)
        for row in spreadsheet:
            data.append(row)

    # there are some countries with empty score => set value = 0.0,
    # convert the other values to float for later calculating
    optimized_data = []
    for row in data:
        score = row['score']
        if score == '':
            score = 0.0
        else:
            score = float(score)

        up_score = {'score': score}

        # update scores in the original data
        row.update(up_score)

        optimized_data.append(row)

    return optimized_data


def write_csv_file(file_name, field_names, field_data):
    """write data into a csv file"""

    # save file to folder OUTPUT
    save_path = './OUTPUT/'
    file_path = os.path.join(save_path, file_name)

    # if there is no folder OUTPUT, create one
    if not os.path.isdir(save_path):
        os.mkdir(save_path)

    # write data to csv file
    with open(file_path, 'w+') as csv_file:
        spreadsheet = csv.DictWriter(csv_file, fieldnames=field_names)
        spreadsheet.writeheader()
        spreadsheet.writerows(field_data)


def get_country_codes(data):
    """returns different country codes list"""
    codes = []
    for row in data:
        code = row['iso3']
        if code not in codes:
            codes.append(code)
    return codes


def get_region_codes(data):
    """returns different region codes list"""
    codes = []
    for row in data:
        code = row['region']
        if code not in codes:
            codes.append(code)
    return codes


def get_region_name(code):
    """returns name of region from region code"""
    code_name_dict = {'AP': 'Asia Pacific',
                      'WE/EU': 'Western Europe',
                      'AME': 'Americas',
                      'MENA': 'Middle East and North Africa',
                      'SSA': 'Sub Saharan Africa',
                      'ECA': 'Europe and Central Asia'}

    name = code_name_dict[code]
    return name


def get_data_of_year(year, data):
    """returns all rows of all countries in a year"""
    data_year = []
    for row in data:
        if row['year'] == year:
            data_year.append(row)
    return data_year


def get_country_data(country_code, year, data):
    """returns all rows of a country in a year, if year is 'all years' -> returns all rows of a country in all year"""
    country_data = []
    for row in data:
        if row['iso3'] == country_code:
            if (year == 'all years') or (year == row['year']):
                country_data.append(row)
    return country_data


def get_region_data(region_code, year, data):
    """returns all rows of a region in a year, if year is 'all years' -> returns all rows of a region in all year"""
    region_data = []
    for row in data:
        if row['region'] == region_code:
            if (year == 'all years') or (year == row['year']):
                region_data.append(row)
    return region_data


def get_top_or_bottom_region_scores(year, region_code, num_of_countries_in_region, top_scores):
    """returns top / bottom numbers of countries of a region in a year;
    top_scores = True -> returns number of top countries (the highest scores);
    top_scores = False -> returns number of bottom countries (the lowest scores)"""

    data = read_data()

    # get data of a region in a year
    region_year_data = get_region_data(region_code, year, data)

    # create an empty list to store region, countries in the region and scores
    region_country_scores = []
    for row in region_year_data:
        country = row['country']
        score = row['score']

        # create a dictionary to store region, country and score in a year
        region_country_score = {'year': year, 'region': get_region_name(region_code),
                                'country': country, 'score': score}

        # add to the list of all countries of a region in a year
        region_country_scores.append(region_country_score)

    # sort the list of dictionaries increasingly (top_scores = False) or decreasingly (top_scores = True)
    sorted_region_data = sorted(region_country_scores, key=lambda d: d['score'], reverse=top_scores)

    # get the top number of countries and scores
    result = sorted_region_data[:num_of_countries_in_region]

    return result


def get_top_or_bottom_country_scores(year, num_of_countries, top_scores):
    """get number of top or bottom countries in a year,
    top_scores = True -> returns number of top countries (the highest scores);
    top_scores = False -> returns number of bottom countries (the lowest scores)"""

    data = read_data()

    # get data of a year
    data_year = get_data_of_year(year, data)

    # create an empty list to store countries and scores
    country_scores = []
    for row in data_year:
        country = row['country']
        score = row['score']

        # create a dictionary to store country and score
        country_score = {'year': str(year), 'country': str(country), 'score': score}

        # add to the list of all countries and scores
        country_scores.append(country_score)

    # sort the list of dictionaries increasingly (top_scores = False) or decreasingly (top_scores = True)
    sorted_countries = sorted(country_scores, key=lambda d: d['score'], reverse=top_scores)

    # get the top number of countries and scores from the list
    result = sorted_countries[:num_of_countries]

    return result


def calculated_score_of_countries():
    """calculates the average, min, max scores of every country over the past 10 years"""
    # get data from the input resource
    data = read_data()

    # create a list to store codes of all countries.
    # the input file from Kaggle has 184 different country names but 182 different country codes
    country_codes = get_country_codes(data)

    # create a list to store the countries with their names, code and average scores
    country_scores = []

    # get country nane, min, max and average score for each country code
    for code in country_codes:
        # get rows of a country with code of all year
        country_data = get_country_data(code, 'all years', data)

        # create a list to store scores of a country over the past 10 years
        # this list will be used to identify the min, max and average score of a country
        scores = []
        country_name = ''
        for row in country_data:
            country_name = row['country']
            score = row['score']
            scores.append(score)

        # calculate min, max and average score
        average = round(sum(scores) / len(scores), 2)
        min_score = min(scores)
        max_score = max(scores)

        # create a dictionary to store the name, code, average, min, max score of a country
        country_score = {'country': country_name, 'iso3': code, 'average': average,
                         'min score': min_score, 'max score': max_score}

        # add to the list of countries with name, code, min, max and average score
        country_scores.append(country_score)

    return country_scores


def calculated_score_of_regions():
    """calculates the average, min, max scores over the past 10 years"""
    # get data from the input resource
    data = read_data()

    # create a list to store codes of all regions.
    region_codes = get_region_codes(data)

    # create a list to store regions with their names, code, min, max and average scores
    region_scores = []

    # calculate min, max and average score for each region with region code
    for code in region_codes:
        # get rows of a region of all year
        region_data = get_region_data(code, 'all years', data)

        # create a list to store scores of a region over the past 10 years
        # this list will be used to identify the min, max and average score of a region
        scores = []
        for row in region_data:
            score = row['score']
            scores.append(score)

        # calculate min, max and average score
        average = round(sum(scores) / len(scores), 2)
        min_score = min(scores)
        max_score = max(scores)

        region_name = get_region_name(code)
        # create a dictionary to store the name, code and average score of a region
        region_score = {'region': region_name, 'region code': code, 'average': average,
                        'min score': min_score, 'max score': max_score}

        # add to the list of all regions
        region_scores.append(region_score)

    return region_scores


def run_project():
    print('WELCOME TO CFG PROJECT - PYTHON, SEPTEMBER 2022 !!!')
    print('GROUP 4 - SPREADSHEET ANALYSIS. Group members: Bernice, Margherita, Thao')
    print('We provide information about Corruption Indicator Data of 182 Governments over the past 10 years, such as:')
    print('[1] Number of top highest or lowest corrupted governments in a year.')
    print('[2] Min, max and average scores of 182 Governments over the past 10 years.')
    print('[3] Min, max and average scores of all regions over the past 10 years.')
    print('[4] Number of countries in a region with top highest or lowest scores in a year.')
    print('[5] Display all regions with average scores over the past 10 years by graph')
    print('[6] Display score changes of a country over the past 10 years in graph')

    choice = input('Which option do you want to request?[1 | 2 | 3 | 4 | 5 | 6]')

    if choice == '1':
        year = input('Which year do you want to get the data?(2012-2021)')
        top_lowest = input('Do you want to get the top lowest [1] or top highest [0] corrupted governments?')
        num_of_countries = int(input('Top number of how many countries? (maximum: 182)'))

        output_file_name = ''
        if top_lowest == '1':
            output_file_name = 'top_{}_lowest_corrupted_gov_in_{}.csv'.format(num_of_countries, year)
            top_lowest = True

        if top_lowest == '0':
            output_file_name = 'top_{}_highest_corrupted_gov_in_{}.csv'.format(num_of_countries, year)
            top_lowest = False

        # get top number of lowest or highest corrupted countries in a year
        countries_data = get_top_or_bottom_country_scores(year, num_of_countries, top_lowest)

        # create field names for csv file
        field_names = ['year', 'country', 'score']

        write_csv_file(output_file_name, field_names, countries_data)
        print('REQUESTED SUCCESSFULLY. PLEASE READ THE OUTPUT IN CSV FILE: {}.'.format(output_file_name))

    elif choice == '2':
        # get data from function
        average_data = calculated_score_of_countries()

        # create field names for csv file
        field_names = ['country', 'iso3', 'average', 'min score', 'max score']

        # call the function to write data to csv file
        write_csv_file('calculated_score_governments.csv', field_names, average_data)

        print('REQUESTED SUCCESSFULLY. PLEASE READ THE OUTPUT IN CSV FILE calculated_score_governments.csv')

    elif choice == '3':
        # get data from function
        region_data = calculated_score_of_regions()

        # create field names for csv file
        field_names = ['region', 'region code', 'average', 'min score', 'max score']

        # create csv file name
        file_name = 'calculated_score_regions.csv'

        # write data to csv file
        write_csv_file(file_name, field_names, region_data)

        print('REQUESTED SUCCESSFULLY. PLEASE READ THE OUTPUT IN CSV FILE calculated_score_regions.csv')

    elif choice == '4':
        year = input('Which year do you want to get the data?(2012-2021)')
        print('Which region?', 'blue')
        print('AP (Asia Pacific: 32 countries)')
        print('SSA (Sub Saharan Africa: 49 countries)')
        print('ECA (Europe and Central Asia: 19 countries)')
        print('MENA (Middle East and North Africa: 18 countries)')
        print('AME (America: 33 countries)')
        print('WE/EU (Western Europe: 31 countries)')
        region_code = input('Enter a region code:').upper()
        top_lowest = input('Do you want to get the top lowest [1] or top highest [0] corrupted countries?')
        num_of_countries = input('How many countries in the list?')

        # in case region code is WE/EU -> change character '/' to '_' to fit the csv file name, else get error
        if region_code == 'WE/EU':
            optimized_region_code = 'WE_EU'
        else:
            optimized_region_code = region_code

        # create csv file name
        file_name = ''
        if top_lowest == '1':
            file_name = 'top_{}_lowest_gov_in_{}_in_{}.csv'.format(num_of_countries, optimized_region_code, year)
            top_lowest = True

        if top_lowest == '0':
            file_name = 'top_{}_highest_gov_in_{}_in_{}.csv'.format(num_of_countries, optimized_region_code, year)
            top_lowest = False

        # get data by calling function
        region_data = get_top_or_bottom_region_scores(year, region_code, int(num_of_countries), top_lowest)

        # create field names
        field_names = ['year', 'region', 'country', 'score']

        # write data to csv file
        write_csv_file(file_name, field_names, region_data)
        print('REQUESTED SUCCESSFULLY. PLEASE READ THE OUTPUT IN CSV FILE {}'.format(file_name))

    elif choice == '5':
        # get data from function
        region_data = calculated_score_of_regions()

        # create field names for csv file
        field_names = ['region', 'region code', 'average', 'min score', 'max score']

        # create csv file name
        file_name = 'calculated_score_regions.csv'

        # write data to csv file
        write_csv_file(file_name, field_names, region_data)

        # read data from csv file, then use Seaborn library to make data visualization by graph
        df = pd.read_csv('./OUTPUT/calculated_score_regions.csv')

        # call function barplot in Seaborn library to create a barplot graph
        sns_plot = sns.barplot(x='region code', y='average', data=df, palette='plasma')

        # set labels for axis x, y
        sns_plot.set(xlabel='region', ylabel='average score')

        # save output graph to a PNG file
        sns_plot.figure.savefig("./OUTPUT/regions_scores_graph.png")

        print('REQUESTED SUCCESSFULLY. PLEASE CHECK FILE regions_scores_graph.png')

    elif choice == '6':
        data = read_data()
        country_code = input('Enter the country code:')
        country_code = country_code.upper()
        country_data = get_country_data(country_code, 'all years', data)

        field_names = ['', 'country', 'iso3', 'region', 'year', 'score', 'rank', 'sources', 'standardError']
        file_name = 'country_{}_all_year.csv'.format(country_code)

        write_csv_file(file_name, field_names, country_data)
        # read data from csv file, then use Seaborn library to make data visualization by graph

        file_path = './OUTPUT/country_{}_all_year.csv'.format(country_code)

        df = pd.read_csv(file_path)

        # call function barplot in Seaborn library to create a barplot graph
        sns_plot = sns.barplot(x='year', y='score', data=df, palette='plasma')

        # set labels for axis x, y
        sns_plot.set(xlabel='year', ylabel='score')

        # save output graph to a PNG file
        out_file_path = './OUTPUT/country_{}_all_year.png'.format(country_code)
        sns_plot.figure.savefig(out_file_path)

        print('REQUESTED SUCCESSFULLY. PLEASE CHECK FILE country_{}_all_year.png'.format(country_code))

    else:
        cred = '\033[91m'
        cend = '\033[0m'
        print(cred + 'Please choose a correct option.' + cend)


# RUN PROJECT HERE
run_project()
