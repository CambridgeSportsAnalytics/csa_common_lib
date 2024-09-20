import numpy as np
import pandas as pd


def variable_importance(combi_compound:list, X_cols:list):
    """Returns the variable importance table.

    Args:
        combi_compound (list): Weighted matrix
        X_cols (list): Array of variable (column) names

    Returns:
        pd.Dataframe : Table containing variable importance statistics
    """
     
    #turn grid into an array
    combi_compound = np.vstack(combi_compound)
    
    #get medians, standard deviations, and percentiles of each column    
    medians = np.median(combi_compound,axis=0)
    std_devs = np.std(combi_compound,axis=0)
    percentile_05 = np.percentile(combi_compound,5,axis=0)
    percentile_20 = np.percentile(combi_compound,20,axis=0)
    percentile_50 = np.percentile(combi_compound,50,axis=0)
    percentile_80 = np.percentile(combi_compound,80,axis=0)
    percentile_95 = np.percentile(combi_compound,95,axis=0)
    
    #set up dataframe of results sorted by highest medians
    result = {
            'Median': medians,
            'Std Dev': std_devs,
            '5th Percentile': percentile_05,
            '20th Percentile': percentile_20,
            '50th Percentile': percentile_50,
            '80th Percentile': percentile_80,
            '95th Percentile': percentile_95
            }
    variable_importance = pd.DataFrame(result,index=X_cols).sort_values(by='Median',ascending=False)

    return variable_importance


def t_stats_and_betas(yhats:list, y_actuals:pd.Series, y_linear:list, 
                      fits:list, percentile_low:int=20, percentile_high:int=80):
    """Returns the beta and t-stats table at subsamples of high, mid, and low fit

    Args:
        yhats (list): Predictiion values
        y_actuals (pd.Series): Actual values (to be compared to yhats)
        y_linear (list): Prediction value using standard linear regression
        fits (list): Prediction fits
        percentile_low (int, optional): Defaults to 20.
        percentile_high (int, optional): Defaults to 80.

    Returns:
        pd.Dataframe : Table containing t_stats and betas for various levels of fits
    """

    
    #make inputs arrays
    yhats = np.array(yhats)
    y_actuals = np.array(y_actuals)
    y_linear = np.array(y_linear)
    fits = np.array(fits)
    
    #get high, mid, and low fits
    high_fits, mid_fits, low_fits = high_mid_low(fits,percentile_low,percentile_high)
    
    #block 1: full sample
    full_sample = linear_component_analysis(yhats,y_actuals,y_linear)
    
    #block 2: high fit
    high_fit_yhats = yhats[high_fits]
    high_fit_y_linear = y_linear[high_fits]
    high_fit_y_actual = y_actuals[high_fits]
    high_fit = linear_component_analysis(high_fit_yhats,high_fit_y_actual,high_fit_y_linear)
    
    #block 3: mid fit
    mid_fit_yhats = yhats[mid_fits]
    mid_fit_y_linear = y_linear[mid_fits]
    mid_fit_y_actual = y_actuals[mid_fits]
    mid_fit = linear_component_analysis(mid_fit_yhats,mid_fit_y_actual,mid_fit_y_linear)
    
    #block 4: low fit
    low_fit_yhats = yhats[low_fits]
    low_fit_y_linear = y_linear[low_fits]
    low_fit_y_actual = y_actuals[low_fits]
    low_fit = linear_component_analysis(low_fit_yhats,low_fit_y_actual,low_fit_y_linear)
    
    #set up results
    results = {
               'Full Sample Linear Component' : [full_sample['beta_linear'],full_sample['t_linear']],
               'Full Sample Excess RBP Component' : [full_sample['beta_non_linear'],full_sample['t_non_linear']],
               'High Fit Sample Linear Component' : [high_fit['beta_non_linear'],high_fit['t_non_linear']],
               'High Fit Sample Excess RBP Component' : [high_fit['beta_non_linear'],high_fit['t_non_linear']],
               'Mid Fit Sample Linear Component' : [mid_fit['beta_linear'],mid_fit['t_linear']],
               'Mid Fit Sample Excess RBP Component' : [mid_fit['beta_non_linear'],mid_fit['t_non_linear']],
               'Low Fit Sample Linear Component' : [low_fit['beta_linear'],low_fit['t_linear']],
               'Low Fit Sample Excess RBP Component' : [low_fit['beta_non_linear'],low_fit['t_non_linear']]
                }
    
    t_stats_and_betas = pd.DataFrame(results,index=['Beta','T-Statistic'])
    
    return t_stats_and_betas


def y_actual_means(yhats:list, y_actuals:pd.Series, fits:list, 
                   percentile_low:int=20, percentile_high:int=80):
    """Returns the y_actual_means table, containing y_actual mean 
    at values when yhat is high and low and fit is high and low.

    Args:
        yhats (list):Predictiion values
        y_actuals (pd.Series): Actual values (to be compared to yhats)
        fits (list): Prediction fits
        percentile_low (int, optional): Defaults to 20.
        percentile_high (int, optional): Defaults to 80.

    Returns:
        pd.Dataframe : Table containing mean y_actual values at varying 
        level of fit
    """


    #make inputs arrays
    yhats = np.array(yhats)
    y_actuals = np.array(y_actuals)
    fits = np.array(fits)
    
    #set up high and low yhats for block 2 and 3
    high_yhats, _, low_yhats = high_mid_low(yhats,percentile_low, percentile_high)
    
    #block 1: full sample
    full_sample = np.mean(y_actuals)
    
    #block 2: high yhat sample
        #high yhat yactual mean
    y_actuals_high_yhat = y_actuals[high_yhats]
    fits_high_yhat = fits[high_yhats]
    high_pred = np.mean(y_actuals_high_yhat)
    
        #get high and low fits of high yhats
    high_fits, _, low_fits = high_mid_low(fits_high_yhat,percentile_low, percentile_high)
    
        #mean of y_actual at high yhat and high fit
    y_actuals_high_yhat_high_fit = y_actuals_high_yhat[high_fits]
    high_pred_w_high_fit = np.mean(y_actuals_high_yhat_high_fit)
    
        #mean of y_actual at high yhat and low fit
    y_actuals_high_yhat_low_fit = y_actuals_high_yhat[low_fits]
    high_pred_w_low_fit = np.mean(y_actuals_high_yhat_low_fit)
    
    #block 3: low yhat sample
    y_actuals_low_yhat = y_actuals[low_yhats]
    fits_low_yhat = fits[low_yhats]
    low_pred = np.mean(y_actuals_low_yhat)
    
        #get high and low fits of low yhats
    high_fits, _, low_fits = high_mid_low(fits_low_yhat,percentile_low,percentile_high)
    
        #mean of y_actual at low yhat and high fit
    y_actuals_low_yhat_high_fit = y_actuals_low_yhat[high_fits]
    low_pred_w_high_fit = np.mean(y_actuals_low_yhat_high_fit)
    
        #mean of y_actual at low yhat and low fit
    y_actuals_low_yhat_low_fit = y_actuals_low_yhat[low_fits]
    low_pred_w_low_fit = np.mean(y_actuals_low_yhat_low_fit)
    
    #set up result data table
    results = {
                'Full Sample' : full_sample,
                'High Prediction' : high_pred,
                'High Prediction w/ High Fit' : high_pred_w_high_fit,
                'High Prediction w/ Low Fit' : high_pred_w_low_fit,
                'Low Prediction' : low_pred,
                'Low Prediction w/ High Fit' : low_pred_w_high_fit,
                'Low Prediction w/ Low Fit' : low_pred_w_low_fit
                }
    y_actual_means = pd.DataFrame(results,index=['Y Actual Mean']).T
    
    return y_actual_means


def high_mid_low(data:list, percentile_low:list=0, percentile_high:int=1):
    """Takes in an data and returns the high, middle, and low cutoffs 
    for the data.

    Args:
        data (np.ndarray): data whose percentiles we are trying to access
        percentile_low (int, optional): Defaults to 0.
        percentile_high (int, optional): Defaults to 1.

    Returns:
        high_indexes, mid_indexes, low_indexes : each is an data of 
        indices that correspond with values in the passed data 
        (first parameter) based on which percentile range it belongs to 
    """


    high_value = np.percentile(data, percentile_high)
    high_indexes = np.where(np.array(data) >= high_value)[0]
    low_value = np.percentile(data, percentile_low)
    low_indexes = np.where(np.array(data) <= low_value)[0]
    mid_indexes = np.where((np.array(data) > low_value) & (np.array(data) < high_value))[0]
    
    return high_indexes, mid_indexes, low_indexes


def info_weighted_co_occurrence(yhats:list, y_actuals:pd.Series, 
                                m1:int=None, o1:int=None, m2:int=None, o2:int=None):
    """Returns the informativeness weighted co-occurrence of yhat 
    and y_actuals

    Args:
        yhats (list):Predictiion values
        y_actuals (pd.Series): Actual values (to be compared to yhats)
        m1 (int, optional): Mean of yhats. Defaults to None.
        o1 (int, optional): Std. Dev. of yhats. Defaults to None.
        m2 (int, optional): Mean of y_actuals. Defaults to None.
        o2 (int, optional): Std. Dev. of y_actuals. Defaults to None.

    Returns:
        co_occurence : Co-Occurence (int)
    """

    if m1 is None:
        m1 = np.mean(yhats)
    if o1 is None:
        o1 = np.std(yhats)  # Assuming standard deviation as a default
    if m2 is None:
        m2 = np.mean(y_actuals)
    if o2 is None:
        o2 = np.std(y_actuals)  # Assuming standard deviation as a default
    
    #using mean and standard deviation, get an array of z scores for both yhat and y_actuals
    z_yhat = (yhats - m1) / o1
    z_y_actual = (y_actuals - m2) / o2
    
    #calculate the informativeness of the yhat/y_actual pair
    info_yhat_y_actual = 0.5 * (z_yhat**2 + z_y_actual**2)
    
    #calculate the co-occurrence of the yhat/y_actual pair
    co_occurrence_yhat_y_actual = (z_yhat * z_y_actual) / info_yhat_y_actual
    
    #gets the relative weights of each observation based on informativeness
    w_info = info_yhat_y_actual / sum(info_yhat_y_actual)
    
    #calculates weighed co-occurrence by multiplying co-occurrence and informativenss weights
    w_co_occurrence = co_occurrence_yhat_y_actual * w_info
    
    #sum of weighted co-occurrence to get correlation coefficient
    co_occurence = sum(w_co_occurrence)
    
    return co_occurence


def ifwco_table(yhats:list, y_actuals:pd.Series, fits:list, 
                percentile_low:int=20, percentile_high:int=80):
    """Returns the info weighted co occucurence (ifwco) table of yhat 
    and y_actual at high and low fits and values

    Args:
        yhats (list):Predictiion values
        y_actuals (pd.Series): Actual values (to be compared to yhats)
        fits (list): Prediction fits
        percentile_low (int, optional): Defaults to 20.
        percentile_high (int, optional): Defaults to 80.

    Returns:
        ifwco_table: pd.Dataframe containing ifwco values of yhat and y_actual
    """


    #make inputs arrays
    yhats = np.array(yhats)
    y_actuals = np.array(y_actuals)
    fits = np.array(fits)
    
    #set up high and low fits and yhats for blocks 1, 2, and 3
    high_yhats, _, low_yhats = high_mid_low(yhats,percentile_low,percentile_high)
    high_fits, _, low_fits = high_mid_low(fits, percentile_low, percentile_high)
    
    #block 1: full sample, high fit, and low fit
        #calculate means and standard deviations of yhats and y_actuals
    m1 = np.mean(yhats)
    o1 = np.std(yhats)
    m2 = np.mean(y_actuals)
    o2 = np.std(y_actuals)
    
        #iwco of full sample
    full_sample = info_weighted_co_occurrence(yhats, y_actuals, m1, o1, m2, o2)
    
        #iwco of high fit sample
    high_fits_yhats = yhats[high_fits]
    high_fits_y_actuals = y_actuals[high_fits]
    high_fit = info_weighted_co_occurrence(high_fits_yhats, high_fits_y_actuals, m1, o2, m2, o2)
    
        #iwco of low fit sample
    low_fits_yhats = yhats[low_fits]
    low_fits_y_actuals = y_actuals[low_fits]
    low_fit = info_weighted_co_occurrence(low_fits_yhats, low_fits_y_actuals, m1, o1, m2, o2)
    
    #block 2: high yhat sample
        #get high and low fits
    high_yhat_fits = fits[high_yhats]
    high_yhat_high_fits, _, high_yhat_low_fits = high_mid_low(high_yhat_fits,percentile_low,percentile_high)    
    
        #calculate means and standard deviations of yhats and y_actuals when yhat is high
    high_yhat = yhats[high_yhats]
    high_yhat_y_actual = y_actuals[high_yhats]
    m1 = np.mean(high_yhat)
    o1 = np.std(high_yhat)
    m2 = np.mean(high_yhat_y_actual)
    o2 = np.std(high_yhat_y_actual)
    
        #iwco of full high yhat sample
    high_pred = info_weighted_co_occurrence(high_yhat,high_yhat_y_actual, m1, o1, m2, o2)
    
        #iwco of high yhat high fit
    high_yhat_high_fit = high_yhat[high_yhat_high_fits]
    high_yhat_high_fit_y_actual = high_yhat_y_actual[high_yhat_high_fits]
    high_pred_w_high_fit = info_weighted_co_occurrence(high_yhat_high_fit, high_yhat_high_fit_y_actual, m1, o1, m2, o2)
    
        #iwco of high yhat low fit
    high_yhat_low_fit = high_yhat[high_yhat_low_fits]
    high_yhat_low_fit_y_actuals = high_yhat_y_actual[high_yhat_low_fits]
    high_pred_w_low_fit = info_weighted_co_occurrence(high_yhat_low_fit, high_yhat_low_fit_y_actuals, m1, o1, m2, o2)
    
    #block 3: low yhat sample
        #get high and low fits
    low_yhat_fits = fits[low_yhats]
    low_yhat_high_fits, _, low_yhat_low_fits = high_mid_low(low_yhat_fits,percentile_low,percentile_high)    
    
        #calculate means and standard deviations of yhats and y_actuals when yhat is high
    low_yhat = yhats[low_yhats]
    low_yhat_y_actual = y_actuals[low_yhats]
    m1 = np.mean(low_yhat)
    o1 = np.std(low_yhat)
    m2 = np.mean(low_yhat_y_actual)
    o2 = np.std(low_yhat_y_actual)
    
        #iwco of full high yhat sample
    low_pred = info_weighted_co_occurrence(low_yhat,low_yhat_y_actual, m1, o1, m2, o2)
    
        #iwco of high yhat high fit
    low_yhat_high_fit = low_yhat[low_yhat_high_fits]
    low_yhat_high_fit_y_actual = low_yhat_y_actual[low_yhat_high_fits]
    low_pred_w_high_fit = info_weighted_co_occurrence(low_yhat_high_fit, low_yhat_high_fit_y_actual, m1, o1, m2, o2)
    
        #iwco of high yhat low fit
    low_yhat_low_fit = low_yhat[low_yhat_low_fits]
    low_yhat_low_fit_y_actuals = low_yhat_y_actual[low_yhat_low_fits]
    low_pred_w_low_fit = info_weighted_co_occurrence(low_yhat_low_fit, low_yhat_low_fit_y_actuals, m1, o1, m2, o2)
    
    #set up results table
    results = {
               'Full Sample' : full_sample,
               'High Fit' : high_fit,
               'Low Fit' : low_fit,
               'High Prediction' : high_pred,
               'High Prediction w/ High Fit' : high_pred_w_high_fit,
               'High Prediction w/ Low Fit' : high_pred_w_low_fit,
               'Low Prediction' : low_pred,
               'Low Prediction w/ High Fit' : low_pred_w_high_fit,
               'Low Prediction w/ Low Fit' : low_pred_w_low_fit
                }
    ifwco_table = pd.DataFrame(results,index=['Informativeness Weighted Co-Occurrence']).T
    
    return ifwco_table


def linear_component_analysis(yhats:list, y_actuals:pd.Series, y_linear:list):
    """Returns the coefficients and p-values of the linear and 
    non-linear parts of the model.


    Args:
        yhats (list):Predictiion values
        y_actuals (pd.Series): Actual values (to be compared to yhats)
        y_linear (list): Prediction value using standard linear regression

    Returns:
        lin_comp_analyis: dict containing linear component analysis final values
    """


    #set up variable assigments (yhat = B1*y_linear + B2*y_nonlinear)
    x1 = y_linear
    x2 = yhats - y_linear
    y = y_actuals
    
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
    
    #reset names of coefficients and t statistics to return a dict
    lin_comp_analyis = {
            'beta_linear' : b1,
            'beta_non_linear' : b2,
            't_linear' : tx1,
            't_non_linear' : tx2
    }
    
    return lin_comp_analyis


def model_analysis(yhats, y_actuals, y_linear, fits, combi_compound, 
                   X_cols, percentile_low=20, percentile_high=80):
    """Returns a list with the metrics for average Y when Yhat is 
    low/high and fit is low/high, informativeness-weighted co-occurrence
    for yhat and y_actuals, and the betas and p-values of the
    regression of y_actuals on the linear and non-linear components of yhat.

    Args:
        yhats (list): Predictiion values
        y_actuals (pd.Series): Actual values (to be compared to yhats)
        y_linear (list): Prediction value using standard linear regression
        fits (list): Prediction fits
        combi_compound (list): Weighted matrix
        X_cols (list): Array of variable (column) names
        percentile_low (int, optional): Defaults to 20.
        percentile_high (int, optional): Defaults to 80.

    Returns:
        list : Array of pandas tables containing summary statistics for a given prediction
    """


    if X_cols is None:
        X_cols = range(0,len(combi_compound))
    
    #create the three tables needed for output
    y_actual_mean = y_actual_means(yhats,y_actuals,fits,percentile_low,percentile_high)
    ifwco = ifwco_table(yhats,y_actuals,fits,percentile_low,percentile_high)
    lca = t_stats_and_betas(yhats,y_actuals,y_linear,fits,percentile_low,percentile_high)
    var_importance = variable_importance(combi_compound=combi_compound, X_cols=X_cols)
    
    #pack the tables together in a list
    results_list = [y_actual_mean, ifwco, lca, var_importance]
    
    return results_list