import numpy as np
from warnings import warn

def select_entering_variable(objective_row: np.ndarray) -> int | None:
    """
    Finds the entering variable for a maximization problem (most negative coefficient).
    """
    # Exclude the RHS column
    search_space = objective_row[:-1]
    
    most_negative = np.min(search_space)
    
    if most_negative >= 0:
        return None  # Optimal solution found
    
    return np.argmin(search_space)

def select_leaving_variable(tableau_matrix: np.ndarray, entering_col: int) -> int | None:
    """
    Performs the minimum ratio test to find the leaving variable (pivot row).
    Returns the 1-based index of the leaving row.
    """
    rhs_col = tableau_matrix[1:, -1]
    pivot_col = tableau_matrix[1:, entering_col]
    
    # Create a mask for rows where the pivot column element is positive
    mask = pivot_col > 1e-9 # Using a small tolerance for float comparison
    
    if not np.any(mask):
        # --- DEBUGGING PRINT ---
        print("\n--- DEBUG INFO: Unbounded Problem Detected ---")
        print(f"Entering Column Index: {entering_col}")
        print("Pivot Column (Constraints Section):")
        print(pivot_col)
        print("This column has no positive values, leading to an 'Unbounded' error.")
        print("-------------------------------------------\n")
        # --- END DEBUGGING ---
        return None 
    
    # Calculate ratios only for valid rows
    ratios = np.full_like(rhs_col, np.inf)
    np.divide(rhs_col, pivot_col, out=ratios, where=mask)
    
    if np.min(ratios) < 1e-9:
        warn("Degeneracy detected.")
        
    leaving_row_0_based = np.argmin(ratios)
    
    # Return the 1-based index for the tableau matrix
    return leaving_row_0_based + 1