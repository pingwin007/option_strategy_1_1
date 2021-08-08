import csv

import pandas as pd

import tags


def read_inputs():  # from engine
    # stock data
    data = []
    with open('data/input_data_min_max_ult.csv', 'r') as datafile:
        datareader = csv.reader(datafile, delimiter=',')
        for row in datareader:
            data.append(row)
            # important - converting 2D list into Data Frame-------------------------------------------------------------------
    title_of_columns = data[:][0]  # first row of the list
    data_to_operate = pd.DataFrame(data, columns=title_of_columns)
    data_to_operate = data_to_operate.drop([0], axis=0)  # removing the second row of titles - clean data structure

    # general model parameters
    parameter_df = pd.read_csv(tags.CFG_MODEL, index_col=0)
    # individual stock parameters
    position_matrix_df = pd.read_csv(tags.CFG_STOCK, index_col=False)
    return data_to_operate, parameter_df, position_matrix_df


def write_outputs(open_positions_pf, historical_positions_pf, financial_properties_df):
    writer = pd.ExcelWriter('output/trading_strategy_analysis_v1_3.xlsx', engine='xlsxwriter')
    open_positions_pf.to_excel(writer, sheet_name='open_positions_pf')
    open_positions_pf.to_csv('output/open_positions_pf.csv')
    historical_positions_pf.to_excel(writer, sheet_name='closed_deals')
    historical_positions_pf.to_csv('output/historical_positions_pf.csv')
    financial_properties_df.to_excel(writer, sheet_name='financial_overview')
    financial_properties_df.to_csv('output/financial_properties.csv')
    writer.save()
