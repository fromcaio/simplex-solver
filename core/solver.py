import numpy as np
from . import standardizer, tableau, pivoting

def solve(lpp_model: dict) -> dict:
    """
    Main orchestrator for the Simplex method.
    """
    constraint_matrix, initial_basis, var_info = standardizer.standardize(lpp_model)
    
    if var_info['num_artificial'] > 0:
        # Phase I is required
        final_phase1_tableau = _solve_phase1(constraint_matrix, initial_basis, var_info)
        phase2_tableau = _prepare_for_phase2(final_phase1_tableau, lpp_model)
    else:
        # Phase I is not needed, proceed directly to Phase II
        phase2_tableau = _create_phase2_tableau_directly(constraint_matrix, initial_basis, var_info, lpp_model)

    # Solve Phase II using the standard simplex loop.
    final_tableau = _run_simplex(phase2_tableau, "Phase II")
    return final_tableau.get_solution()

def _run_simplex(tableau_obj: tableau.Tableau, phase_name: str) -> tableau.Tableau:
    """A generic simplex solver loop that pivots until an optimal tableau is found."""
    while True:
        entering_col = pivoting.select_entering_variable(tableau_obj.matrix[0, :])
        
        if entering_col is None:
            return tableau_obj # Optimal

        leaving_row = pivoting.select_leaving_variable(tableau_obj.matrix, entering_col)
        
        if leaving_row is None:
            raise ValueError(f"Problem is unbounded (detected in {phase_name}).")
            
        tableau_obj.pivot(entering_col, leaving_row)

def _solve_phase1(constraint_matrix, initial_basis, var_info) -> tableau.Tableau:
    """Sets up and solves Phase I to find a basic feasible solution."""
    # The objective is to Maximize W' = -a1 -a2 ..., so the equation is z + a1 + a2... = 0.
    # The coefficients for a1, a2.. in the objective row are initially +1.
    phase1_obj_row = np.zeros(var_info['total_vars'] + 1)
    for col in var_info['artificial_cols']:
        phase1_obj_row[col] = 1.0 # Set coefficient to +1
    
    matrix = np.vstack([phase1_obj_row, constraint_matrix])
    
    # Make canonical: To eliminate the +1 for a basic variable, we SUBTRACT its row.
    for i, basis_col in enumerate(initial_basis):
        if basis_col in var_info['artificial_cols']:
            matrix[0, :] -= matrix[i + 1, :]
            
    phase1_tableau = tableau.Tableau(matrix, initial_basis, var_info)
    final_phase1 = _run_simplex(phase1_tableau, "Phase I")
    
    if not np.isclose(final_phase1.matrix[0, -1], 0):
        raise ValueError("Problem is infeasible.")
        
    return final_phase1

def _prepare_for_phase2(final_phase1_tableau, lpp_model) -> tableau.Tableau:
    """Prepares the initial tableau for Phase II from a completed Phase I."""
    matrix = final_phase1_tableau.matrix.copy()
    basis = list(final_phase1_tableau.basic_vars)
    var_info = final_phase1_tableau.var_info

    # Step 1: Clean the Basis by pivoting out any basic artificial variables
    for row_idx, basis_col in enumerate(basis):
        if basis_col in var_info['artificial_cols']:
            pivot_row_in_matrix = row_idx + 1
            pivot_row_content = matrix[pivot_row_in_matrix, :]
            # Find a non-artificial variable in this row to enter the basis
            entering_col = next((c for c in range(var_info['total_vars']) if c not in var_info['artificial_cols'] and not np.isclose(pivot_row_content[c], 0)), None)
            if entering_col is not None:
                temp_tableau = tableau.Tableau(matrix, basis, var_info)
                temp_tableau.pivot(entering_col, pivot_row_in_matrix)
                # Update local state with the results of the pivot
                matrix, basis = temp_tableau.matrix, temp_tableau.basic_vars

    # Step 2: Build Phase II Tableau (Matrix-level operations)
    # Replace objective row and delete artificial columns
    matrix[0, :] = 0.0
    matrix[0, :var_info['num_decision']] = -np.array(lpp_model['objective_coeffs'])

    deleted_cols = sorted(var_info['artificial_cols'], reverse=True)
    for col in deleted_cols:
        matrix = np.delete(matrix, col, axis=1)

    # Step 3: Update Data Structures (Index-level operations)
    sorted_deleted_cols_asc = sorted(deleted_cols, reverse=False)
    
    # Update the list of basic variable indices
    updated_basis = []
    for b_col in basis:
        shift = sum(1 for d_col in sorted_deleted_cols_asc if d_col < b_col)
        updated_basis.append(b_col - shift)

    # <<< FIX: Create a new, fully updated var_info for Phase II >>>
    # This block corrects the `unknown_` variable naming bug.
    phase2_var_info = {}
    phase2_var_info['num_decision'] = var_info['num_decision']
    
    # Apply the same index-shifting logic to the slack and surplus column lists
    new_slack_cols = [s - sum(1 for d in sorted_deleted_cols_asc if d < s) for s in var_info['slack_cols']]
    new_surplus_cols = [e - sum(1 for d in sorted_deleted_cols_asc if d < e) for e in var_info['surplus_cols']]

    phase2_var_info['slack_cols'] = new_slack_cols
    phase2_var_info['surplus_cols'] = new_surplus_cols
    phase2_var_info['num_slack'] = len(new_slack_cols)
    phase2_var_info['num_surplus'] = len(new_surplus_cols)

    # Artificial variables are gone for Phase II
    phase2_var_info['num_artificial'] = 0
    phase2_var_info['artificial_cols'] = []
    phase2_var_info['total_vars'] = var_info['total_vars'] - len(deleted_cols)
    # <<< END FIX >>>

    # Step 4: Make the final tableau canonical
    for i, basis_col in enumerate(updated_basis):
        if not np.isclose(matrix[0, basis_col], 0):
            factor = matrix[0, basis_col]
            matrix[0, :] -= factor * matrix[i + 1, :]
            
    # Return the final, corrected tableau for Phase II
    return tableau.Tableau(matrix, updated_basis, phase2_var_info)

def _create_phase2_tableau_directly(constraint_matrix, initial_basis, var_info, lpp_model):
    """Builds the tableau when Phase I is not needed."""
    obj_row = np.zeros(var_info['total_vars'] + 1)
    obj_row[:var_info['num_decision']] = -np.array(lpp_model['objective_coeffs'])
    matrix = np.vstack([obj_row, constraint_matrix])
    return tableau.Tableau(matrix, initial_basis, var_info)