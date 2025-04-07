#!/usr/bin/env python3

import csv
import math
import matplotlib.pyplot as plt

jj_vals = [3000,2600,2200,1800,1700,1600,1500,1400,1350,1300,1250,1200,1150,
           1100,1050,1000,950,900,875,850,800,780,760,740,720,700,
           680,660,640,620,600,590,580,560,550,540,530,520,510,
           500,490,480,470,460,450,440,430,420,410,400,390,380,
           370,360,350,340,330,320,310,300,292,284,276,270,265,
           260,255,250,245,240,235,230,225,220,215,210,205,200,
           195,190,185,180,175,170,165,160,155,150,145,140,136,
           132,128,124,120,116,112,108,104,100,100,96,92,88,86,
           84,82,80,78,76,74,72,70,68,66,64,62,
           60,58,56,54,52,50,49,48,47,46,45,44,
           43,42,41,40,39.5,39,38.5,38,37.5,37,
           36.5,36,35.5,35,34.5,34,33.5,33,32.6,
           32.3,31.8,31.4,31,30.6,30.2,29.8,39.4,
           29,28.6,28.2,27.8,27.4,27,26.6,26.2,25.8,
           25.4,25,24.6,24.2,23.8,23.4,23,22.6,22.2,
           21.8,21.4,21,20.6,19.8,19.4,19,18.6,18.2,17.8,
           17.4,17,16.6,16.2,15.8,15.4,15,14.6,14.2,13.8,
           13.4,13,12.6,12.2,11.8,11.4,11,10.6,10.2,9.8,
           9.4,9,8.6,8.2,7.8,7.4,7,6.6,6.2,5.8,5.4,5,4.6,
           4.2,3.8,3,2.6,2.3,2,1.8,1.6,1.4,1.2,1,1,1,1,1,
           1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
           1,1
           ]

def massey_thaler_value(pick, lam, beta):
    """
    Computes the exponential decay value for a given pick position,
    following v(n) = exp(-lam * (n - 1)^beta).
    """
    return math.exp(-lam * ((pick - 1) ** beta))

def plot(picks, l1_values, l2_values, jj_values):
    plt.figure(figsize=(10, 6))
    plt.plot(picks, l1_values, label="L1 Value")
    plt.plot(picks, l2_values, label="L2 Value")
    plt.plot(picks, jj_values, label="Jimmy Johnson value")
    plt.xlabel("Pick")
    plt.ylabel("Value")
    plt.title("Comparison of L1, L2, and Jimmy Johnson Values")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("comparison_plot.png")

def main():
    # -------- Non-CI Parameters for L1 & L2 Norms --------
    lambda_l1 = 0.001007
    beta_l1   = 1.445350

    lambda_l2 = 0.000010
    beta_l2   = 2.371845

    # We'll go up to pick #257 now
    num_picks = 257

    # --- Calculate v(1) for each norm (should be ~1.0) ---
    v1_l1 = massey_thaler_value(1, lambda_l1, beta_l1)
    v1_l2 = massey_thaler_value(1, lambda_l2, beta_l2)

    # Prepare lists to store values for plotting
    picks = []
    l1_values = []
    l2_values = []
    jj_values_plot = []

    # Write CSV file with an extra column for Jimmy Johnson values
    with open("compare_jj.csv", mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Pick", "L1_Value", "L2_Value", "Jimmy_Johnson"])

        for pick in range(1, num_picks + 1):
            raw_val_l1 = massey_thaler_value(pick, lambda_l1, beta_l1)
            raw_val_l2 = massey_thaler_value(pick, lambda_l2, beta_l2)

            scaled_l1 = round((raw_val_l1 / v1_l1) * 3000.0,2)
            scaled_l2 = round((raw_val_l2 / v1_l2) * 3000.0,2)

            # Use the Jimmy Johnson value from jj_vals (indexed from 0)
            jj_val = jj_vals[pick - 1]

            writer.writerow([pick, scaled_l1, scaled_l2, jj_val])

            picks.append(pick)
            l1_values.append(scaled_l1)
            l2_values.append(scaled_l2)
            jj_values_plot.append(jj_val)

    plot(picks, l1_values, l2_values, jj_values_plot)

if __name__ == "__main__":
    main()