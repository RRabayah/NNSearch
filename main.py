import pandas as pd
import numpy as np
from collections import Counter
import math
from math import dist
import sys, getopt

# Auxilliary Helper Functions
# flatten an array
def flatten(l):
    return [item for sublist in l for item in sublist]

#flattens a 2d-array
def get_flat_list(list1):
    unique_elements = []
    for x in list1:
        unique_elements.append(x.split(','))
    unique_elements = flatten(unique_elements)
    for x in range(len(unique_elements)):
        unique_elements[x] = unique_elements[x].strip()
    return unique_elements

#tranforms a string of comma-separated values into a list
def transform_into_list(list1):
    unique_elements = list1.split(',')
    for x in range(len(unique_elements)):
        unique_elements[x] = unique_elements[x].strip()
    return unique_elements

#basic range-scaling to get values between 0-1
def range_scaling(df_col):
    max_col_val = df_col.max()
    min_col_val = df_col.min()

    df_col = df_col.apply(lambda x: ((x-min_col_val)/(max_col_val-min_col_val)))
    return df_col

#simple one_hot_encoding, works on lists and strings
def one_hot_encode(df1, column):
    #Slight generalization - works only on lists and strings -- there is probably a better prebuilt method of doing this.
    all_material_occurences = df1[column].tolist()
    flat_unique_list = []

    #Remove duplicates, check if datatype of argument is a list or not
    if(isinstance(all_material_occurences[0],list)):
        flat_unique_list = list(set(flatten(all_material_occurences)))
    else:
        flat_unique_list = list(set(all_material_occurences))
    
    #Create new column for each item in the list - implement categorical variables
    for col in flat_unique_list:
        df1[col] = 0

    #Convert Material Groups into a binary 0-1 classifier (either 0 or 1)
    #TODO: The way I did this is probably wrong - Look into vectorization or list comp. or something
    for index, row in df1.iterrows():
        list_check = row[column]
        if(isinstance(list_check, list)):
            for x in list_check:
                df1.at[index, x] = 1
        else:
            df1.at[index, list_check] = 1

def process_data(df1):
    #Get all possible material groups as one long list
    all_occurances = df1['MATERIAL GROUP'].tolist()

    #Transform str of elements into a list for each row
    df1['MATERIAL GROUP'] = df1['MATERIAL GROUP'].apply(lambda x: transform_into_list(x))

    #Remove rare items from all the lists in each row, reduces data dimensionality
    key_count_dict = Counter(get_flat_list(all_occurances))
    elements_to_remove = [k for k, v in key_count_dict.items() if v < 2]
    df1['MATERIAL GROUP'] = df1['MATERIAL GROUP'].apply(lambda x: list(set(x) - set(elements_to_remove)))

    #Scale numeric values to be 0-1
    df1['NO. OF EMPLOYEES'] = range_scaling(df1['NO. OF EMPLOYEES'])
    df1['NO. OF SERVICED FACILITIES'] = range_scaling(df1['NO. OF SERVICED FACILTIIES'])

    #Encode categorical variables
    one_hot_encode(df1, 'MATERIAL GROUP')
    one_hot_encode(df1, 'SECTOR')

    #Drop unneeded columns
    useless_columns = ['MATERIAL GROUP', 'SECTOR', 'NO. OF SERVICED FACILTIIES']
    for x in useless_columns:
        df1.drop([x], axis = 1, inplace = True)

    return df1

def find_similar(df1):

    #Initialize a new dataframe in which all similarity info. will be stored
    distances = pd.DataFrame()
    distances['from'] = ""
    distances['to'] = ""
    distances['distance'] = ""

    #Iterate through the businesses dataframe
    for index1, row1 in df1.iterrows():
        #Select one row to exclude
        dataframe_excluded = df1.drop(index1, axis = 0)
        #Select features independently
        row1_features = row1.drop(labels=['FACILITY NAME'])
        row1_name = row1['FACILITY NAME']
        row1f_list = row1_features.tolist()
        
        for index2, row2 in dataframe_excluded.iterrows():
            #Go through each other row of the dataframe, extract features for each
            row2_name = row2['FACILITY NAME']
            row2_features = row2.drop(labels = ['FACILITY NAME'])
            row2f_list = row2_features.tolist()

            #Locate the distance between the features, and add to the dataframe
            distance = math.dist(row1f_list, row2f_list)
            distances.loc[len(distances.index)] = [row1_name, row2_name, distance] 

    return distances

#Pipeline to generate all the distances
def complete_pipeline():
    b2b_clients_df = pd.read_csv('./Data/List_B2B.csv')
    clean_data = process_data(b2b_clients_df)
    similarities = find_similar(clean_data)
    similarities.to_csv('./Data/distances.csv')

#Find n most similar businesses
def find_n_most_similar(business, n):
    business_dist_df = pd.read_csv('./Data/distances.csv')
    business_dist_df.loc[business_dist_df['from'] == business]
    sorted_business = business_dist_df.sort_values('distance',ascending = True).groupby('from').head(n)
    print(sorted_business.loc[sorted_business['from'] == business])

def main(argv):

    business = ''
    n = 0
    csv = False

    opts, args = getopt.getopt(argv,"hc:b:n:",["csv=","business=","number="])
    for opt, arg in opts:
        if opt == '-h':
            print ('main.py -c <recalculate distance matrix T/F> -b <business name> -n <number of similar businesses>')
            sys.exit()
        if opt in ("-c", "--csv"):
            csv = arg
            if(csv):
                complete_pipeline()
        if opt in ("-b", "--business"):
            business = arg

        if opt in ("-n", "--number"):
            n = arg
            find_n_most_similar(business, int(n))

if __name__ == "__main__":
   main(sys.argv[1:])
