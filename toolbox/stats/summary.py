import numpy as np
import pandas as pd


def rbp_linear_component(y_linear:list, yhats:list, y_actuals):
    """"Generates a summary of the influence of linear and non linear components
    in the prediction results

    Args:
        y_linear (list): list of y_linear predictions for given thetas
        yhats (list): list of yhat prediction for given thetas
        y_actuals (pandas series): Pandas series of correct prediction results 
            extracted from initial dataset to assess accuracy of the predictions

    Returns:
        data: Dataframe containing component influences
    """
    

    df = pd.DataFrame({
            'yhat': yhats,
            'y_linear': y_linear,
            'y_actuals': y_actuals
        })

    
    x1 = df['y_linear']
    x2 = df['yhat'] - x1
    y = df['y_actuals']
    
    #get the sum of squares and sum of products needed for regression calculations
    ssx1 = sum(x1**2)
    ssx2 = sum(x2**2)
    sx1x2 = sum(x1*x2)
    syx1 = sum(y*x1)
    syx2 = sum(y*x2)
    
    #set up the xTx matrix and find its determinant, use this to set up xTx inverse
    xTx = np.array([ssx1,sx1x2,sx1x2,ssx2]).reshape(2,2)
    detxTx = np.linalg.det(xTx)
    xTx_inverse = (np.array([ssx2, -1*(sx1x2), -1*(sx1x2), ssx1]) / (detxTx)).reshape(2,2)
    
    #calculate b1 and b2 using xTx and its determinant
    b1 = ((ssx2*syx1) - (sx1x2*syx2)) / detxTx
    b2 = ((ssx1*syx2) - (sx1x2*syx1)) / detxTx
    
    #degrees of freedom = N - number of predictors
    df = y.shape[0] - 2
    
    #get predicted values and residuals, calculate error term variance
    pred_values = b1*x1 + b2*x2
    residuals = y - pred_values
    rss = sum(residuals**2)
    error_variance = rss / df
    
    #set up variance/covariance matrix
    varcovar = error_variance * xTx_inverse
    
    #use betas and varcovar to get T statistics
    tx1 = b1 / np.sqrt(varcovar[0,0])
    tx2 = b2 / np.sqrt(varcovar[1,1])
    
    #reset names of coefficients and p-values to return a dict
    dict = {
            'beta_linear' : b1,
            'beta_non_linear' : b2,
            't_linear' : tx1,
            't_non_linear' : tx2
    }
    
    data = pd.DataFrame([dict])

    return data