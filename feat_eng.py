import pandas as pd
import numpy as np

#################################################################################
## Feat. Eng. functions #########################################################
#################################################################################

def past_quantities(df):
    df.loc[:, 'qty_d1'] = df.groupby('id').qty.shift(1)
    df.loc[:, 'qty_d2'] = df.groupby('id').qty.shift(2)
    df.loc[:, 'qty_d3'] = df.groupby('id').qty.shift(3)
    df.loc[:, 'qty_d4'] = df.groupby('id').qty.shift(4)
    df.loc[:, 'qty_d5'] = df.groupby('id').qty.shift(5)
    df.loc[:, 'qty_d6'] = df.groupby('id').qty.shift(6)
    df.loc[:, 'qty_d7'] = df.groupby('id').qty.shift(7)
    return df

def build_data(path_data, sales, sku_ids, 
               split_perc, day_train_trsh):
    
    calender = pd.read_csv(path_data + 'calendar.csv')
    sell_prices = pd.read_csv(path_data + 'sell_prices.csv')
    sales = sales[sales['id'].isin(sku_ids)]
    
    holiday = ['NewYear', 'OrthodoxChristmas', 'MartinLutherKingDay', 
           'SuperBowl', 'PresidentsDay', 'StPatricksDay', 'Easter', 
           'Cinco De Mayo', 'IndependenceDay', 'EidAlAdha', 'Thanksgiving', 
           'Christmas']
    weekend = ['Saturday', 'Sunday']
    
    def is_holiday(x):
        if x in holiday:
            return 1
        else:
            return 0

    def is_weekend(x):
        if x in weekend:
            return 1
        else:
            return 0

    calender['is_holiday_1'] = calender['event_name_1'].apply(is_holiday)
    calender['is_holiday_2'] = calender['event_name_2'].apply(is_holiday)
    calender['is_holiday'] = calender[['is_holiday_1','is_holiday_2']].max(axis=1)
    calender['is_weekend'] = calender['weekday'].apply(is_weekend)

    calender = calender.drop(
        ['weekday', 'wday', 'month', 'year', 
         'event_name_1', 'event_type_1', 'event_name_2', 'event_type_2'], 
        axis='columns')

    del_col = []
    for x in range(day_train_trsh):
        del_col.append('d_' + str(x+1))

    sales =sales.drop(del_col, axis='columns')
    
    sales = sales.melt(
        ['id','item_id','dept_id','cat_id','store_id','state_id'], 
        var_name='d', value_name='qty')

    sales = pd.merge(sales, calender, how='left', on='d')
    sales = pd.merge(sales, sell_prices, 
                           how='left', 
                           on=['item_id', 'wm_yr_wk', 'store_id'])
    sales = past_quantities(df = sales)

    sales.drop(['snap_CA', 'snap_TX', 'snap_WI'], axis='columns', inplace=True) 

    n_items = sales['id'].nunique()
    
    sales = pd.get_dummies(
        data=sales, 
        columns=['dept_id', 'cat_id', 'store_id', 'state_id'])

    day_test_trsh = int((1941 - day_train_trsh)*(1-split_perc[-1]) + day_train_trsh)
    day_val_trsh = int((1941 - day_train_trsh)*(split_perc[0]) + day_train_trsh)
    
    data_test = sales[sales['d'].isin(
        [c for c in sales['d'].unique().tolist() if int(
            c.split('d_')[1]) > day_test_trsh])].copy().reset_index(
        drop=True)
    
    data_val = sales[sales['d'].isin(
        [c for c in sales['d'].unique().tolist() if (
           (int(c.split('d_')[1]) <= day_test_trsh)
         & (int(c.split('d_')[1]) > day_val_trsh)
        )])].copy().reset_index(
        drop=True)

    data_train = sales[sales['d'].isin(
        [c for c in sales['d'].unique().tolist() if int(
            c.split('d_')[1]) <= day_val_trsh])].copy().reset_index(
        drop=True)
    
    data_train['day'] = data_train['d'].str.replace('d_','').astype(int)
    data_val['day'] = data_val['d'].str.replace('d_','').astype(int)
    data_test['day'] = data_test['d'].str.replace('d_','').astype(int)
    

    data_train = data_train[data_train['day']>day_train_trsh+7]
    
    data_train = data_train.sort_values(by = ['day','id'])
    data_val = data_val.sort_values(by = ['day','id'])
    data_test = data_test.sort_values(by = ['day','id'])

    data_train = data_train.reset_index(drop=True)
    data_val = data_val.reset_index(drop=True)
    data_test = data_test.reset_index(drop=True)
    
    feat = list(set(data_train.columns) - set(['id','item_id','dept_id','cat_id',
                                                'store_id','state_id','d','qty',
                                                'date','wm_yr_wk', 'day']))
    
    feat.sort()
    
    return data_train, data_val, data_test, feat, n_items