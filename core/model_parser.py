import re

def parse_from_file(file_path: str) -> dict:
    """
    Parses a text file with a specific keyword-based format to define an LPP model.
    Assumes:
        - Maximization problem
        - All variables are non-negative
        - All RHS values (b) are non-negative
    """
    num_vars = None
    obj_expr_lines = []
    constraint_exprs = []
    parsing_mode = None  # 'OBJECTIVE' or 'CONSTRAINTS'

    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            lower_line = line.lower()

            if lower_line.startswith('num_vars:'):
                try:
                    num_vars = int(line.split(':')[1].strip())
                except (IndexError, ValueError):
                    raise ValueError("NUM_VARS must be followed by an integer (e.g., NUM_VARS: 3).")
                parsing_mode = None
            elif lower_line.startswith('objective:'):
                parsing_mode = 'OBJECTIVE'
            elif lower_line.startswith('constraints:'):
                parsing_mode = 'CONSTRAINTS'
            elif parsing_mode == 'OBJECTIVE':
                obj_expr_lines.append(line)
            elif parsing_mode == 'CONSTRAINTS':
                constraint_exprs.append(line)

    if num_vars is None:
        raise ValueError("Missing required section: NUM_VARS.")
    if not obj_expr_lines:
        raise ValueError("Missing required section: OBJECTIVE.")
    if not constraint_exprs:
        raise ValueError("Missing required section: CONSTRAINTS.")

    full_obj_expr = ' '.join(obj_expr_lines)
    return parse_from_strings(num_vars, constraint_exprs, full_obj_expr)


def parse_from_strings(num_vars: int, constraints: list[str], obj_expr: str) -> dict:
    """
    Converts string-based LP components into a structured dictionary of coefficients.
    Assumes non-negative variables and RHS.
    """
    def parse_expression(expr: str, label: str) -> list[float]:
        coeffs = [0.0] * num_vars
        terms = re.findall(r'([+\-]?\s*\d*\.?\d*)\s*\*?\s*(x_?\d+)', expr)

        for coeff_str, var_str in terms:
            var_index_str = var_str.replace('x_', '').replace('x', '')
            if not var_index_str.isdigit():
                raise ValueError(f"Invalid variable format in {label}: '{var_str}'")
            var_index = int(var_index_str) - 1
            if var_index >= num_vars or var_index < 0:
                raise ValueError(f"Variable {var_str} in {label} is out of bounds for num_vars={num_vars}.")

            coeff_str = coeff_str.replace(' ', '')
            if coeff_str == '' or coeff_str == '+':
                coeff_val = 1.0
            elif coeff_str == '-':
                coeff_val = -1.0
            else:
                coeff_val = float(coeff_str)

            coeffs[var_index] += coeff_val

        return coeffs

    parsed_constraints = []
    for const_str in constraints:
        match = re.match(r'(.+?)\s*([<>]=|=)\s*(-?[0-9.]+)', const_str)
        if not match:
            raise ValueError(f"Invalid constraint format: '{const_str}'")

        expr, sign, rhs = match.groups()
        coeffs = parse_expression(expr, label='constraint')
        parsed_constraints.append({'coeffs': coeffs, 'type': sign, 'rhs': float(rhs)})

    obj_coeffs = parse_expression(obj_expr, label='objective')

    return {
        'num_vars': num_vars,
        'objective_coeffs': obj_coeffs,
        'constraints': parsed_constraints
    }