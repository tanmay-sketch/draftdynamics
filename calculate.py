from fit import weibull_value

# Teams' traded pick numbers
team_x_picks = [5, 78]
team_y_picks = [12, 33, 101]

# Optimized Weibull parameters from L1 and L2 norm fitting
params_l1 = (0.001007, 1.44)
params_l2 = (0.000010, 2.371845)

# Function to compute total draft value for a set of picks under given Weibull parameters
def compute_total_value(picks, lambda_val, beta_val):
    return sum(weibull_value(pick, lambda_val, beta_val) for pick in picks)

# Compute values under L1 norm
x_val_l1 = compute_total_value(team_x_picks, *params_l1)
y_val_l1 = compute_total_value(team_y_picks, *params_l1)

# Compute values under L2 norm
x_val_l2 = compute_total_value(team_x_picks, *params_l2)
y_val_l2 = compute_total_value(team_y_picks, *params_l2)

# Function to evaluate and print trade outcome
def evaluate_trade(x_value, y_value, norm_label):
    diff = x_value - y_value
    print(f"\n[{norm_label} Norm]")
    print(f"Team X value: {x_value:.4f}")
    print(f"Team Y value: {y_value:.4f}")
    print(f"Trade value difference: {diff:.4f}")

    if diff > 0:
        print("→ Winner: Team X")
    elif diff < 0:
        print("→ Winner: Team Y")
    else:
        print("→ Result: Fair Trade")

# Evaluate trade under both norms
evaluate_trade(x_val_l1, y_val_l1, "L1")
evaluate_trade(x_val_l2, y_val_l2, "L2")