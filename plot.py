import numpy as np
import matplotlib.pyplot as plt
from fit import weibull_value

def plot_curves_with_ci(lambda_mse, beta_mse, lambda_mae, beta_mae, 
                       mse_params, mae_params):
    """Plot Weibull curves with confidence intervals."""
    picks = np.arange(1, 257)
    
    # Calculate mean curves
    values_mse = [weibull_value(p, lambda_mse, beta_mse) for p in picks]
    values_mae = [weibull_value(p, lambda_mae, beta_mae) for p in picks]
    
    # Calculate confidence intervals
    mse_values = np.array([[weibull_value(p, params[0], params[1]) 
                           for p in picks] for params in mse_params])
    mae_values = np.array([[weibull_value(p, params[0], params[1]) 
                           for p in picks] for params in mae_params])
    
    mse_lower = np.percentile(mse_values, 2.5, axis=0)
    mse_upper = np.percentile(mse_values, 97.5, axis=0)
    mae_lower = np.percentile(mae_values, 2.5, axis=0)
    mae_upper = np.percentile(mae_values, 97.5, axis=0)
    
    plt.figure(figsize=(12, 7))
    
    # Plot MSE curve and confidence interval
    plt.plot(picks, values_mse, 'b-', 
            label=f'MSE (L2-Norm): λ={lambda_mse:.3f}, β={beta_mse:.3f}', 
            linewidth=2)
    plt.fill_between(picks, mse_lower, mse_upper, 
                    color='blue', alpha=0.2, 
                    label='MSE 95% CI')
    
    # Plot MAE curve and confidence interval
    plt.plot(picks, values_mae, 'r--', 
            label=f'MAE (L1-Norm): λ={lambda_mae:.3f}, β={beta_mae:.3f}', 
            linewidth=2)
    plt.fill_between(picks, mae_lower, mae_upper, 
                    color='red', alpha=0.2, 
                    label='MAE 95% CI')
    
    plt.title('Draft Pick Value Curves: MSE vs MAE Optimization\nwith 95% Confidence Intervals')
    plt.xlabel('Pick Number')
    plt.ylabel('Value Relative to First Pick')
    plt.legend()
    plt.grid(True)
    plt.xticks(np.arange(0, 257, 32))
    plt.show()

def plot_curves_simple(lambda_mse, beta_mse, lambda_mae, beta_mae):
    """Plot Weibull curves without confidence intervals for clearer comparison."""
    picks = np.arange(1, 257)
    
    # Calculate curves
    values_mse = [weibull_value(p, lambda_mse, beta_mse) for p in picks]
    values_mae = [weibull_value(p, lambda_mae, beta_mae) for p in picks]
    
    plt.figure(figsize=(12, 7))
    
    # Plot MSE curve
    plt.plot(picks, values_mse, 'b-', 
            label=f'MSE (L2-Norm): λ={lambda_mse:.3f}, β={beta_mse:.3f}', 
            linewidth=2)
    
    # Plot MAE curve
    plt.plot(picks, values_mae, 'r--', 
            label=f'MSE (L1-Norm): λ={lambda_mae:.3f}, β={beta_mae:.3f}', 
            linewidth=2)
    
    plt.title('Draft Pick Value Curves: MSE vs MAE Optimization')
    plt.xlabel('Pick Number')
    plt.ylabel('Value Relative to First Pick')
    plt.legend()
    plt.grid(True)
    plt.xticks(np.arange(0, 257, 32))
    plt.show()