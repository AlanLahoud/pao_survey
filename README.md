# pao_survey

This repository provides a tutorial on Predict-and-Optimize methods connected to the survey "Predict-and-Optimize: A survey on problem variations and approaches".

*A. What does this project do?*
This project uses Machine Learning and Mathematical Programming techniques to solve a data-dependent Newsvendor Problem. We aim to find near-optimal quantity orders for different items using a real-world dataset of sales.

*B. Why is this project useful?*
Instead of only separating the Machine Learning to the Mathematical Programming solver, we also explore recent techniques that combine both.
We show through this notebook that, on average, the combination of both methods can provide better decision-making through the Optimization Problem, but the training time is usually higher.

*C. How to run?*
1. Download the data from https://www.kaggle.com/competitions/m5-forecasting-accuracy/data
2. You will have 5 .csv files: calendar.csv ; sales_train_evaluation.csv ; sales_train_validation.csv ; sample_submission.csv ; sell_prices.csv. Put all those .csv files in the /data folder in this project
3. Install the libraries from requirements.txt (Python 3)
4. Read and run the notebook "predict_and_optimize_tutorial.ipynb".
