import pandas as pd
import numpy as np
import torch

#################################################################################
## OP deterministic parameters ##################################################
#################################################################################

def get_params(n_items, is_discrete, q_factor, seed_number):
    
    np.random.seed(seed_number)
    
    params_name = ['c','cs','cw','pr','si']
    params_list = []
    
    for i in range(0, n_items):
        c = 60 + np.random.randint(-30, 30) # Fixed cost for each item
        cs = 180 + np.random.randint(-80, 80)  # Shortage cost fpr each item
        cw = 120 + np.random.randint(-50, 50) # Excess cost for each item
        
        # constraints of price and size for each item
        pr = int(100000/(c + cs + cw) + np.random.randint(-50, 50))
        si = int(100000/(c + cs + cw) + np.random.randint(-50, 50))

        params_list.append([c, cs, cw, pr, si])

    df_parameters = pd.DataFrame(data=params_list, columns = params_name)

    # Generate a bound for inequalities of Budget and Size
    avg_sales = 0
    if is_discrete:
        avg_sales = 1.3
    else:
        avg_sales = 30 
    B = 400*avg_sales*n_items*np.random.uniform(0.3, 0.6)
    S = 400*avg_sales*n_items*np.random.uniform(0.3, 0.6)
    
    
    # Building the parameters as numpy and torch dictionary
    params = {}
    
    params['q'] = (q_factor*df_parameters['c']).tolist()
    params['qs'] = (q_factor*df_parameters['cs']).tolist()
    params['qw'] = (q_factor*df_parameters['cw']).tolist()
    
    params['c'] = df_parameters['c'].tolist()
    params['cs'] = df_parameters['cs'].tolist()
    params['cw'] = df_parameters['cw'].tolist()
    
    params['pr'] = df_parameters['pr'].tolist()
    params['B'] = [B]
    
    params['si'] = df_parameters['si'].tolist()
    params['S'] = [S]

    for key in params.keys():
        params[key] = torch.Tensor(params[key])
        params_t = params.copy()
        
    for key in params.keys():
        params[key] = np.array(params[key])
        params_np = params.copy()

    return params_t, params_np