import ctypes
import os

class QuantCoreBridge:
    """
    Bridge class to interface with the C-compiled quantitative engine.
    """
    def __init__(self):
        lib_path = os.path.join(os.path.dirname(__file__), 'libquant_core.so')
        try:
            self.quant_lib = ctypes.CDLL(lib_path)
        except OSError:
            raise RuntimeError(f"Could not load library at {lib_path}. Did you compile it?")

        # --- Monte Carlo VaR Binding ---
        self.quant_lib.calculate_monte_carlo_var.argtypes = [
            ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_int
        ]
        self.quant_lib.calculate_monte_carlo_var.restype = ctypes.c_double

        # --- Covariance Matrix Binding ---
        # C signature: void calculate_covariance_matrix(const double* returns, int num_assets, int num_days, double* out_cov_matrix)
        self.quant_lib.calculate_covariance_matrix.argtypes = [
            ctypes.POINTER(ctypes.c_double), # returns array
            ctypes.c_int,                    # num_assets
            ctypes.c_int,                    # num_days
            ctypes.POINTER(ctypes.c_double)  # out_cov_matrix array
        ]
        self.quant_lib.calculate_covariance_matrix.restype = None

    def run_monte_carlo(self, initial_price: float, drift: float, volatility: float, time_horizon: float = 1.0, num_simulations: int = 1000000) -> float:
        return self.quant_lib.calculate_monte_carlo_var(initial_price, drift, volatility, time_horizon, num_simulations)

    def get_covariance_matrix(self, returns_data, num_assets: int, num_days: int):
        """
        Calculates the covariance matrix in C.
        """
        # 1. Flatten the input data and convert to C array
        flat_returns = [item for sublist in returns_data for item in sublist]
        c_returns = (ctypes.c_double * len(flat_returns))(*flat_returns)
        
        # 2. Prepare an empty C array to store the output (num_assets * num_assets)
        output_size = num_assets * num_assets
        c_out_matrix = (ctypes.c_double * output_size)()
        
        # 3. Call the C function
        self.quant_lib.calculate_covariance_matrix(c_returns, num_assets, num_days, c_out_matrix)
        
        # 4. Convert the flat output array back to a 2D Python list
        result_matrix = []
        for i in range(num_assets):
            row = [c_out_matrix[i * num_assets + j] for j in range(num_assets)]
            result_matrix.append(row)
            
        return result_matrix

# Test block
if __name__ == "__main__":
    engine = QuantCoreBridge()
    
    # Mock data: Returns for 3 assets over 4 days
    mock_returns = [
        [0.01, -0.02, 0.03, 0.01],  # Asset A (e.g., Apple)
        [0.02, -0.01, 0.02, 0.00],  # Asset B (e.g., Microsoft)
        [-0.01, 0.03, -0.02, -0.01] # Asset C (e.g., Gold)
    ]
    num_assets = len(mock_returns)
    num_days = len(mock_returns[0])
    
    print("Calculating Covariance Matrix in C...")
    cov_matrix = engine.get_covariance_matrix(mock_returns, num_assets, num_days)
    
    print("\nResulting Covariance Matrix:")
    for row in cov_matrix:
        formatted_row = [f"{val:8.4f}" for val in row]
        print(f"[{', '.join(formatted_row)}]")