import pandas as pd
import numpy as np

def select_items(train_sales, start_day=900, window=50):

    train_sales = train_sales.drop(['d_'+str(n) for n in range(1, start_day)], axis=1)

    for i in list(np.arange(start_day, 1942-window, int(window/10)+1)):
        train_sales = train_sales[
            (train_sales[
                ['d_'+str(n) for n in range(i, i + window)]
            ].max(axis=1)>1)
        ]
        

    # Get items which daily sales >> 0 (considering continuous later)
    return train_sales[
        (train_sales.iloc[:,6:].mean(axis=1)>3) 
        & (train_sales.iloc[:,6:].median(axis=1)>2)
        & (train_sales.iloc[:,6:].mean(axis=1)<8)
    ].id.unique().tolist()