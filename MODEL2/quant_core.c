#include <stdlib.h>
#include <math.h>
#include <time.h> // NEW: Required for processing system time

/*
 * Simulates stock price paths using Geometric Brownian Motion (GBM)
 * to calculate the Value at Risk (VaR) via Monte Carlo method.
 */
double calculate_monte_carlo_var(double initial_price, double drift, double volatility, double time_horizon, int num_simulations) {
    // NEW: Seed the Pseudo-Random Number Generator (PRNG) with current Unix time
    srand((unsigned int)time(NULL));
    
    double total_final_price = 0.0;

    for (int i = 0; i < num_simulations; i++) {
        double u1 = (double)rand() / RAND_MAX;
        double u2 = (double)rand() / RAND_MAX;
        
        if (u1 == 0.0) u1 = 0.0000001; 
        
        double z = sqrt(-2.0 * log(u1)) * cos(2.0 * 3.14159265358979323846 * u2);
        double final_price = initial_price * exp((drift - 0.5 * volatility * volatility) * time_horizon + volatility * sqrt(time_horizon) * z);
        
        total_final_price += final_price;
    }

    return total_final_price / num_simulations;
}

// ... (Keep the calculate_covariance_matrix function here exactly as it was) ...
/*
 * Calculates the Covariance Matrix for a given set of asset returns.
 * Demonstrates memory-bound array traversal and dynamic memory allocation.
 * 
 * @param returns: Flattened 2D array of returns (num_assets * num_days).
 * @param num_assets: Number of assets in the portfolio.
 * @param num_days: Number of historical days (observations) per asset.
 * @param out_cov_matrix: Flattened 2D array (num_assets * num_assets) to store the result.
 */
void calculate_covariance_matrix(const double* returns, int num_assets, int num_days, double* out_cov_matrix) {
    // 1. Allocate memory to store the mean return of each asset
    double* means = (double*)malloc(num_assets * sizeof(double));
    
    // 2. Calculate the mean for each asset
    for (int i = 0; i < num_assets; i++) {
        double sum = 0.0;
        for (int t = 0; t < num_days; t++) {
            // Pointer arithmetic to access row 'i' and column 't'
            sum += returns[i * num_days + t];
        }
        means[i] = sum / num_days;
    }

    // 3. Calculate the covariance matrix
    for (int i = 0; i < num_assets; i++) {
        for (int j = 0; j < num_assets; j++) {
            double cov_sum = 0.0;
            for (int t = 0; t < num_days; t++) {
                cov_sum += (returns[i * num_days + t] - means[i]) * (returns[j * num_days + t] - means[j]);
            }
            // Store the result in the output matrix
            out_cov_matrix[i * num_assets + j] = cov_sum / (num_days - 1);
        }
    }
    
    // 4. Free the allocated memory to prevent memory leaks
    free(means);
}