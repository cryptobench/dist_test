import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics



def main():
    df = pd.read_csv('/Golem/input/USA_Housing.csv')
    X = df[['Avg. Area Income', 'Avg. Area House Age', 'Avg. Area Number of Rooms',
               'Avg. Area Number of Bedrooms', 'Area Population']]
    y = df['Price']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=101)
    lm = LinearRegression()
    lm.fit(X_train,y_train)
    coeff_df = pd.DataFrame(lm.coef_,X.columns,columns=['Coefficient'])
    predictions = lm.predict(X_test)
    data_dict = {"MAE":metrics.mean_absolute_error(y_test, predictions),"MSE":metrics.mean_squared_error(y_test, predictions),"RMSE":np.sqrt(metrics.mean_squared_error(y_test, predictions))}
    data_df = pd.DataFrame(data_dict,index=[0])
    data_df.to_csv(f'/code/output/mse_data.csv')
    coeff_df.to_csv(f'/code/output/coefficient_data.csv')  


main()

