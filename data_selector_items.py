import pandas as pd
import numpy as np

def select_items(train_sales, is_discrete, start_day=900, window=50):

    train_sales = train_sales.drop(['d_'+str(n) for n in range(1, start_day)], axis=1)

    for i in list(np.arange(start_day, 1942-window, int(window/10)+1)):
        train_sales = train_sales[
            (train_sales[
                ['d_'+str(n) for n in range(i, i + window)]
            ].max(axis=1)>1)
        ]
        
    if is_discrete:
        # Get items which daily sales near 0 (considering discrete later)
        return train_sales[
            (train_sales.iloc[:,6:].mean(axis=1)<5) 
            & (train_sales.iloc[:,6:].mean(axis=1)>0.5) 
            & (train_sales.iloc[:,6:].median(axis=1)<5)
        ].id.unique().tolist()
    
    else:
        # Get items which daily sales >> 0 (considering continuous later)
        return train_sales[
            (train_sales.iloc[:,6:].mean(axis=1)>15) 
            & (train_sales.iloc[:,6:].median(axis=1)>15)
        ].id.unique().tolist()