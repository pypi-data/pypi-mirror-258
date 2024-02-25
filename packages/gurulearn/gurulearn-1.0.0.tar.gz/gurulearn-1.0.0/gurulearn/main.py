import pandas as pd
import numpy as np
import plotly.graph_objs as go
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

def plot_linear_regression(csv_file, x_name, y_name, x_element, y_element):
    # Load data
    t = pd.read_csv(csv_file)


    if x_element == 'Date':
        t['Date'] = pd.to_datetime(t['Date'])

    # Plotly layout
    layout = go.Layout(
        title=f'{y_name} vs. {x_name}',
        xaxis=dict(title=x_name, titlefont=dict(family='Courier New, monospace', size=18, color='#7f7f7f')),
        yaxis=dict(title=y_name, titlefont=dict(family='Courier New, monospace', size=18, color='#7f7f7f'))
    )


    X = np.array(t[x_element]).reshape(-1, 1)
    Y = t[y_element]
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3, random_state=101)


    scaler = StandardScaler().fit(X_train)
    X_train_scaled = scaler.transform(X_train)
    X_test_scaled = scaler.transform(X_test)


    lm = LinearRegression()
    lm.fit(X_train_scaled, Y_train)


    trace0 = go.Scatter(x=X_train.flatten(), y=Y_train, mode='markers', name='Actual')
    trace1 = go.Scatter(x=X_train.flatten(), y=lm.predict(X_train_scaled), mode='lines', name='Predicted')
    t_data = [trace0, trace1]
    layout.xaxis.title.text = x_name
    layout.yaxis.title.text = y_name
    fig = go.Figure(data=t_data, layout=layout)

    
    fig.show()



from sklearn.metrics import r2_score, mean_squared_error

def linear_regression_accuracy(csv_file, x_name, y_name, x_element, y_element):
    # Load data
    t = pd.read_csv(csv_file)

    # Convert 'Date' column to pandas datetime object if used as X-axis element
    if x_element == 'Date':
        t['Date'] = pd.to_datetime(t['Date'])

    # Prepare data for regression
    X = np.array(t[x_element]).reshape(-1, 1)
    Y = t[y_element]
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3, random_state=101)

    # Standardize features
    scaler = StandardScaler().fit(X_train)
    X_train_scaled = scaler.transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Linear regression
    lm = LinearRegression()
    lm.fit(X_train_scaled, Y_train)

    # Predictions
    Y_train_pred = lm.predict(X_train_scaled)
    Y_test_pred = lm.predict(X_test_scaled)

    # Calculate accuracy metrics
    train_r2 = r2_score(Y_train, Y_train_pred)
    test_r2 = r2_score(Y_test, Y_test_pred)
    train_mse = mean_squared_error(Y_train, Y_train_pred)
    test_mse = mean_squared_error(Y_test, Y_test_pred)

    # Print accuracy metrics
    print(f'Train R-squared score: {train_r2}')
    print(f'Test R-squared score: {test_r2}')
    print(f'Train Mean Squared Error: {train_mse}')
    print(f'Test Mean Squared Error: {test_mse}')