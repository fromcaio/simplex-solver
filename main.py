import sys
from core import model_parser, solver

def run_solver(file_path: str):
    """
    Parses an LPP from a file, solves it, and prints the result.
    """
    print(f"--- Solving LPP from file: {file_path} ---")
    try:
        # 1. Parse the file into a structured, intermediate representation.
        lpp_model = model_parser.parse_from_file(file_path)
        # 2. Pass the model to the solver, which handles everything else.
        solution = solver.solve(lpp_model)

        # 3. Print the results in a user-friendly format.
        print("\n--- Solution ---")
        print(f"Status: {solution['status']}")
        print(f"Optimal Value: {solution['objective_value']:.4f}\n")

        print("Original Decision Variables:")
        for var, value in sorted(solution['decision_vars'].items()):
            print(f"  {var} = {value:.4f}")

        print("\nSlack / Surplus / Artificial Variables:")
        other_vars = {**solution.get('slack_vars', {}), 
                      **solution.get('surplus_vars', {}), 
                      **solution.get('artificial_vars', {})}
        if not other_vars:
            print("  (None)")
        else:
            for var, value in sorted(other_vars.items()):
                print(f"  {var} = {value:.4f}")

        print("\nBasic Variables:", sorted(solution['basic_vars_list']))
        print("Non-Basic Variables:", sorted(solution['non_basic_vars_list']))


    except Exception as e:
        print(f"\nAn error occurred: {e}")

if __name__ == "__main__":
    # A simple way to run from command line: python main.py examples/your_file.txt
    if len(sys.argv) > 1:
        run_solver(sys.argv[1])
    else:
        print("Usage: python main.py <path_to_lpp_file>")
        # As a fallback, run a default example
        run_solver('examples/001_simple-feasible.txt')