"""
Data processing program is to clean the scrape data, then to export a modified 
.csv file, so that we can use it whenever we want to do analysis
Author: Yao Chen
Edite Date: 16/05/2019
"""


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import xlsxwriter
import os


os.chdir('H:/1ads/COSC480-19S1/project/') # set a path to sav files



def column_plot(dataframe, column, figure_no):
    """Given the column to plot a counts of bar and price of box_plot 
    then save it as a .png file.
    parameters:
    dataframe:the target dataframe.
    column: the name of the plot column.
    figure_no: number of the figure showed in the report.
    """
    plt.ioff()
    fig, [axes_1, axes_2] = plt.subplots(2, 1, sharex=True)
    
    counts = dataframe[column].value_counts()
    counts.plot(kind='bar', grid=True, rot=60, ax=axes_1, fontsize=10)
    axes_1.set_ylabel("number of cars")
    title = "Firgure{}_counts&price_by_{}".format(figure_no, column)
    
    dataframe.boxplot(column="price", by=column, grid=True, rot=60, ax=axes_2, fontsize=10)
    axes_2.set_ylabel("price")
    axes_2.set_xlabel(column) 
    
    plt.savefig(title, dpi=96, bbox_inches='tight')   
    plt.close() 
    

def group_count_bar_plot(dataframe, column, bin_list, figure_no):
    """Group the specific column and draw a bar plot, save as a .png file.
       Parameters:
       dataframe: the target dataframe.
       column: name of a column need to be grouped.
       bin_list: list of the gaps according to which the column is grouped.
       figure_no: number of the figure showed in the report.
    """
    plt.ioff()
    fig, axes = plt.subplots()    
    group_var = pd.cut(dataframe[column], bin_list)
    counts = dataframe.groupby(group_var)[column].count()
    counts.plot(kind='bar', grid=True, rot=60, ax=axes, fontsize=10)
    axes.set_ylabel("number of cars")
    title = "Firgure{}_counts_by_{}".format(figure_no, column)
    plt.savefig(title, dpi=96, bbox_inches='tight')   
    plt.close()


def group_price_box_plot(dataframe, column, bin_list, figure_no):
    """Group the specific column and draw a box plot, save as a .png file.
       Parameters:
       dataframe: the target dataframe.
       column: name of a column need to be grouped.
       bin_list: list of the gaps according to which the column is grouped.
       figure_no: number of the figure showed in the report.
    """
    plt.ioff()
    fig = plt.figure()   
    group_var = pd.cut(dataframe[column], bin_list)
    grouped = dataframe.groupby(group_var)
    boxplot = grouped.boxplot(column='price', grid=True,fontsize=8)
    title = "Firgure{}_price_by_{}".format(figure_no, column)
    plt.savefig(title, dpi=96, bbox_inches='tight')   
    plt.close()
    

def get_file(extension):
    """Get the list of addresses of files with an specific extension.
       Parameter:
       extension: the type of a file, e.g.,'xlsx','png'.
    """
    file_set = set()
    for path, dirs, filelist in os.walk(".", topdown=False):
        for filename in filelist:
            if filename.endswith(extension):
                file = os.path.join(path, filename)
                file_set.add(file)
    file_list = list(file_set)
    file_list.sort() #order the file according to the name
    return file_list


def main():
    """Prompt to imput a price limit;
       read the modified csv file;
       form a report for the user
    """
    max_value = int(input("Enter the max price: ")) 
    
    # read the modified_data and form target dataframe by the given limit
    filename = '2_modified_data.csv'
    df_modified = pd.read_csv(filename, encoding='gbk')
    df_target = df_modified.loc[df_modified["price"] <= max_value]
    
    # plot of available columns 
    column_plot(df_target, "district", 1)      
    column_plot(df_target, "Seats", 2) 
    column_plot(df_target, "Fuel type", 3)
    
    # plot grouped columns, including enginesize and Kilometres
    engine_max = df_target['enginesize'].max()
    engine_bin = [0, 1200, 1500, 2000, 2500, engine_max]
    group_count_bar_plot(df_target, "enginesize", engine_bin, 4)
    group_price_box_plot(df_target, "enginesize", engine_bin, 5)
    #Kilometres group
    km_max = df_target['Kilometres'].max()
    kilometres_bin = [0, 1000, 10000, 50000, 100000, 200000, km_max]
    group_count_bar_plot(df_target, "Kilometres", kilometres_bin, 6) 
    group_price_box_plot(df_target, "Kilometres", kilometres_bin, 7)
    
    image_list = get_file("png")
    
    workbook = xlsxwriter.Workbook('3_stat_report.xlsx')
    worksheet = workbook.add_worksheet()
    worksheet.hide_gridlines(2)
    start_row = 3   
    for image in image_list:
        position = "C" + str(start_row)
        worksheet.write(position, str(image))
        start_row += 1 
        position = "C" + str(start_row)
        worksheet.insert_image(position, image)
        start_row += 30
    workbook.close() 
    print("Report has been successfully exported!")  


# Call the main function to run the program   
main() 

