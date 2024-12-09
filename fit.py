import numpy as np
from scipy.optimize import minimize

def weibull_value(t, lambda_, beta_):
    """Calculate value of pick t relative to first pick."""
    return np.exp(-lambda_ * (t-1)**beta_)

def calculate_f(lambda_, beta_, up_picks, down_picks):
    """Calculate f function similar to R implementation."""
    values = []
    
    for up_list, down_list in zip(up_picks, down_picks):
        if np.isnan(up_list[0]) or np.isnan(down_list[0]):
            continue
            
        up_values = sum(weibull_value(p, lambda_, beta_) for p in up_list)
        down_values = sum(weibull_value(p, lambda_, beta_) for p in down_list)
        
        diff = up_values - down_values
        if diff <= 0:
            diff = 1e-5
        
        log_val = -1/lambda_ * np.log(diff)
        transformed = max(0, log_val)**(1/beta_) + 1
        
        values.append(np.log(transformed))
    
    return np.array(values)

def mse_objective(params, up_picks, down_picks):
    """Mean Squared Error objective function."""
    lambda_, beta_ = params
    if lambda_ <= 0 or beta_ <= 0:
        return 1e10
    
    y = np.array([np.log(picks[0]) for picks in down_picks if not np.isnan(picks[0])])
    f_vals = calculate_f(lambda_, beta_, up_picks, down_picks)
    
    return np.mean((y - f_vals)**2)

def mae_objective(params, up_picks, down_picks):
    """Mean Absolute Error objective function."""
    lambda_, beta_ = params
    if lambda_ <= 0 or beta_ <= 0:
        return 1e10
    
    y = np.array([np.log(picks[0]) for picks in down_picks if not np.isnan(picks[0])])
    f_vals = calculate_f(lambda_, beta_, up_picks, down_picks)
    
    return np.mean(np.abs(y - f_vals))

def bootstrap_parameters(up_picks, down_picks, n_bootstrap=100):
    """Perform bootstrap resampling to get confidence intervals."""
    n_samples = len(up_picks)
    mse_params = []
    mae_params = []
    
    x0 = [0.146, 0.698]
    options = {'maxiter': 1000}
    
    for i in range(n_bootstrap):
        indices = np.random.choice(n_samples, n_samples, replace=True)
        boot_up_picks = up_picks.iloc[indices]
        boot_down_picks = down_picks.iloc[indices]
        
        result_mse = minimize(
            mse_objective, 
            x0,
            args=(boot_up_picks, boot_down_picks),
            method='Nelder-Mead',
            options=options
        )
        
        result_mae = minimize(
            mae_objective, 
            x0,
            args=(boot_up_picks, boot_down_picks),
            method='Nelder-Mead',
            options=options
        )
        
        mse_params.append(result_mse.x)
        mae_params.append(result_mae.x)
        
        if (i + 1) % 10 == 0:
            print(f"Completed {i + 1} bootstrap iterations")
    
    return np.array(mse_params), np.array(mae_params)