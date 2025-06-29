import numpy as np

class Tableau:
    # Update the __init__ signature to accept var_info
    def __init__(self, initial_matrix: np.ndarray, basic_vars: list[int], var_info: dict):
        self.matrix = initial_matrix
        self.basic_vars = basic_vars
        self.var_info = var_info

    def _get_var_name(self, var_index: int) -> str:
        """Helper to convert a variable's column index to its name."""
        if var_index < self.var_info['num_decision']:
            return f"x_{var_index + 1}"
        
        # Check if it's a slack, surplus, or artificial variable by its column index
        # This could be made faster with sets, but is clear for now
        if var_index in self.var_info['slack_cols']:
            return f"s_{self.var_info['slack_cols'].index(var_index) + 1}"
        if var_index in self.var_info['surplus_cols']:
            return f"e_{self.var_info['surplus_cols'].index(var_index) + 1}"
        if var_index in self.var_info['artificial_cols']:
            return f"a_{self.var_info['artificial_cols'].index(var_index) + 1}"
        return f"unknown_{var_index}"

    # The pivot method does not need to change.
    def pivot(self, entering_col: int, leaving_row_idx: int):
        # ... (implementation from previous step is correct)
        pivot_element = self.matrix[leaving_row_idx, entering_col]
        self.matrix[leaving_row_idx, :] /= pivot_element
        for i in range(self.matrix.shape[0]):
            if i != leaving_row_idx:
                factor = self.matrix[i, entering_col]
                self.matrix[i, :] -= factor * self.matrix[leaving_row_idx, :]
        self.basic_vars[leaving_row_idx - 1] = entering_col

    def get_solution(self) -> dict:
        # This method needs to be updated to categorize all variable types
        all_var_indices = set(range(self.var_info['total_vars']))
        basic_var_indices = set(self.basic_vars)
        non_basic_var_indices = all_var_indices - basic_var_indices

        vars_by_type = {
            "decision_vars": {}, "slack_vars": {}, "surplus_vars": {}, "artificial_vars": {}
        }
        
        # Helper to place variable in the right dictionary
        def assign_var(var_idx, value):
            name = self._get_var_name(var_idx)
            if var_idx < self.var_info['num_decision']: vars_by_type['decision_vars'][name] = value
            elif var_idx in self.var_info['slack_cols']: vars_by_type['slack_vars'][name] = value
            elif var_idx in self.var_info['surplus_cols']: vars_by_type['surplus_vars'][name] = value
            elif var_idx in self.var_info['artificial_cols']: vars_by_type['artificial_vars'][name] = value

        for row_idx, var_idx in enumerate(self.basic_vars):
            assign_var(var_idx, self.matrix[row_idx + 1, -1])

        for var_idx in non_basic_var_indices:
            assign_var(var_idx, 0.0)

        return {
            "status": "Optimal",
            "objective_value": self.matrix[0, -1],
            "decision_vars": vars_by_type['decision_vars'],
            "slack_vars": vars_by_type['slack_vars'],
            "surplus_vars": vars_by_type['surplus_vars'],
            "basic_vars_list": [self._get_var_name(i) for i in sorted(list(basic_var_indices))],
            "non_basic_vars_list": [self._get_var_name(i) for i in sorted(list(non_basic_var_indices))]
        }