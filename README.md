# pao_survey

*A. What does this project do?*
This project uses Machine Learning and Mathematical Programming techniques to solve a data-dependent Newsvendor Problem. 
We aim to find near-optimal quantity orders for different items using a real-world dataset of sales.

*B. Why is this project useful?*
Instead of separating the Machine Learning to the Mathematical Programming solver, we leverage recent techniques that combine both Recent methods.
We show through this notebook that, on average, the combination of both methods can provide better decision-making through the Optimization Problem

*C. How to run this code?*
1. Download the data from https://www.kaggle.com/competitions/m5-forecasting-accuracy/data
2. You will have 5 .csv files: calendar.csv ; sales_train_evaluation.csv ; sales_train_validation.csv ; sample_submission.csv ; sell_prices.csv
3. Put all those .csv files in the /data folder in this project
4. Run the notebook "inventory_optimization_KKT.ipynb", try different initial parameters
5. Run the notebook "lgbm_pao.ipynb"
6. The notebooks are commented
