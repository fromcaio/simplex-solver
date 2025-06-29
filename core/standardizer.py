import numpy as np

def standardize(lpp_model: dict) -> tuple:
    """
    Converts a parsed LPP model into standard form for the Simplex method.
    Identifies slack, surplus, and artificial variables needed.

    Returns:
        A tuple containing:
        - constraint_matrix (np.ndarray): The matrix of constraints without an objective row.
        - initial_basis (list[int]): Column indices for the initial basic variables (slacks/artificials).
        - var_info (dict): A dictionary mapping variable types to their column indices.
    """
    constraints = lpp_model['constraints']
    num_constraints = len(constraints)
    num_decision_vars = lpp_model['num_vars']

    # --- 1. Count variable types ---
    slack_cols, surplus_cols, artificial_cols = [], [], []
    current_col = num_decision_vars

    for i, const in enumerate(constraints):
        if const['type'] == '<=':
            slack_cols.append(current_col)
            current_col += 1
        elif const['type'] == '>=':
            surplus_cols.append(current_col)
            artificial_cols.append(current_col + 1)
            current_col += 2
        elif const['type'] == '=':
            artificial_cols.append(current_col)
            current_col += 1

    total_vars = current_col
    var_info = {
        'num_decision': num_decision_vars,
        'num_slack': len(slack_cols),
        'num_surplus': len(surplus_cols),
        'num_artificial': len(artificial_cols),
        'total_vars': total_vars,
        'slack_cols': slack_cols,
        'surplus_cols': surplus_cols,
        'artificial_cols': artificial_cols
    }

    # --- 2. Build constraint matrix and initial basis ---
    constraint_matrix = np.zeros((num_constraints, total_vars + 1))
    initial_basis = [0] * num_constraints
    s_idx, e_idx, a_idx = 0, 0, 0 # Pointers for slack, surplus, artificial cols

    for i, const in enumerate(constraints):
        # Coefficients of decision variables and RHS
        constraint_matrix[i, :num_decision_vars] = const['coeffs']
        constraint_matrix[i, -1] = const['rhs']

        if const['type'] == '<=':
            col = var_info['slack_cols'][s_idx]
            constraint_matrix[i, col] = 1.0
            initial_basis[i] = col
            s_idx += 1
        elif const['type'] == '>=':
            surplus_col = var_info['surplus_cols'][e_idx]
            artificial_col = var_info['artificial_cols'][a_idx]
            constraint_matrix[i, surplus_col] = -1.0 # Subtract surplus
            constraint_matrix[i, artificial_col] = 1.0  # Add artificial
            initial_basis[i] = artificial_col
            e_idx += 1
            a_idx += 1
        elif const['type'] == '=':
            col = var_info['artificial_cols'][a_idx]
            constraint_matrix[i, col] = 1.0
            initial_basis[i] = col
            a_idx += 1
            
    return constraint_matrix, initial_basis, var_info