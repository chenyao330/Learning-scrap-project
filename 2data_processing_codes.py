"""
Data processing program is to clean the scrape data, then to export a modified 
.csv file, so that we can use it whenever we want to do analysis
Author: Yao Chen
Edite Date: 16/05/2019
"""


import pandas as pd
import os


os.chdir('H:/1ads/COSC480-19S1/project/')


def new_column(df, column_1, column_2, character, new_name):
    """This function is to merge similar columns to form a new column, and drop
       the old two column.
       Parameters:
       column_1 and column_2 are similar ones that represent the same feature.
       character is always the missing value of column_1 or column_2.
       new_name is the new column name merged from column_1 and column_2.
    """
    new_column = []
    for i, row in df.iterrows():
        if row[column_1] == character:
            new_column.append(row[column_2])
        else:
            new_column.append(row[column_1])
    df[new_name] = new_column
    df_new = df.drop([column_1, column_2], axis = 1)
    return df_new


def remove_character(df,column_dict):
    """Remove special character.
       Parameters:
       df: the dataframe need to be modified.
       column_dict: a dictionary, e.g.,
         {key=column:value=[character need to be removed]}
    """
    for key,value in column_dict.items():
        for item in value:
            df[key] = df[key].str.replace(item, "")
    return df


def main():
    """Clean the raw data, by using the new_column function and remove_character
       function, change target columns to float, and save the cleaned 
       dataframe into a new .csv file.  
       """
    #read the raw_data_scraped
    filename = '1_raw_data_scraped.csv'
    df_raw = pd.read_csv(filename, encoding='gbk')
    
    # choose columns needed to be analyzed
    usecols = ['buy_now', 'asking_price', 'start_price', 'Kilometres', 'Body',
           'Seats', 'Fuel type', 'Engine size', 'Transmission', 'Model detail',
           'Engine', 'History', 'Import history','location','item_url']
    df_modified = pd.DataFrame(df_raw, columns=usecols)    
    
    # use new_column() function to integrate these columns 
    df_modified = new_column(df_modified, "History","Import history", "NaN", "is_import")
    df_modified = new_column(df_modified, "Engine size", "Engine", "NaN", "enginesize")
    df_modified = new_column(df_modified, "buy_now", "asking_price", "[]", "price1")
    df_modified = new_column(df_modified, "price1", "start_price", "[]", "price")
    
    #remove some characters, prepare the columns to be changed into float
    columns_dict={'price':[","],
                  'Kilometres':[","],
                  'location':["[","'","]"]
                  }
    df_modified = remove_character(df_modified, columns_dict)
    
    #transfer str columns to float, to make them able to be calculated    
    df_modified['price'] = df_modified['price'].str.extract('(\d+)', expand = False).astype('float')
    df_modified.ix[df_modified['Kilometres']=="less than 1000", 'Kilometres'] = 999
    df_modified.ix[df_modified['Kilometres']=="more than 1000000", 'Kilometres'] = 1000000
    df_modified['Kilometres'] = df_modified['Kilometres'].astype('float')
    
    #split the 'location' column to 'district' and 'city'
    df_modified['district'] = df_modified['location'].str.split(',', expand = False).str[1]
    df_modified['city'] = df_modified['location'].str.split(',', expand = False).str[0]
    
    # export it to a .csv file to use later whenever need
    df_modified.to_csv('H:/1ads/COSC480-19S1/project/2_modified_data.csv', index=False, sep=',')
    
    print("Modified data has been successfully exported!")   


# Call the main function to run the program
main()
    
    



