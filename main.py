import numpy as np
from scipy.optimize import minimize
from preprocessing import preprocess_data
from fit import mse_objective, mae_objective, bootstrap_parameters
from plot import plot_curves_with_ci, plot_curves_simple

def main(file_path, post_2013=False):
    """Main function to run the analysis with confidence intervals."""
    # Load and preprocess data
    print("Loading and preprocessing data...")
    up_picks, down_picks = preprocess_data(file_path, post_2013)
    
    # Initial parameter values
    x0 = [0.146, 0.698]
    options = {'maxiter': 1000}
    
    # Initial fits
    print("Performing initial optimization...")
    result_mse = minimize(
        mse_objective, 
        x0,
        args=(up_picks, down_picks),
        method='L-BFGS-B',
        options=options
    )
    
    result_mae = minimize(
        mae_objective, 
        x0,
        args=(up_picks, down_picks),
        method='L-BFGS-B',
        options=options
    )
    
    lambda_mse, beta_mse = result_mse.x
    lambda_mae, beta_mae = result_mae.x
    
    print(f"\nMSE Optimization: λ={lambda_mse:.6f}, β={beta_mse:.6f}")
    print(f"MAE Optimization: λ={lambda_mae:.6f}, β={beta_mae:.6f}")
    
    # Bootstrap analysis
    print("\nPerforming bootstrap analysis...")
    mse_params, mae_params = bootstrap_parameters(up_picks, down_picks)
    
    # Calculate confidence intervals
    mse_mean = np.mean(mse_params, axis=0)
    mse_lower = np.percentile(mse_params, 2.5, axis=0)
    mse_upper = np.percentile(mse_params, 97.5, axis=0)
    
    mae_mean = np.mean(mae_params, axis=0)
    mae_lower = np.percentile(mae_params, 2.5, axis=0)
    mae_upper = np.percentile(mae_params, 97.5, axis=0)
    
    print("\nMSE Parameters with 95% CI:")
    print(f"λ: {mse_mean[0]:.6f} ({mse_lower[0]:.6f}, {mse_upper[0]:.6f})")
    print(f"β: {mse_mean[1]:.6f} ({mse_lower[1]:.6f}, {mse_upper[1]:.6f})")
    
    print("\nMAE Parameters with 95% CI:")
    print(f"λ: {mae_mean[0]:.6f} ({mae_lower[0]:.6f}, {mae_upper[0]:.6f})")
    print(f"β: {mae_mean[1]:.6f} ({mae_lower[1]:.6f}, {mae_upper[1]:.6f})")
    
    # Plot results with confidence intervals
    plot_curves_with_ci(lambda_mse, beta_mse, lambda_mae, beta_mae, 
                       mse_params, mae_params)
    
    plot_curves_simple(lambda_mse, beta_mse, lambda_mae, beta_mae)

if __name__ == "__main__":
    main("data_draft_trades_m24_Chris.csv", post_2013=False)
