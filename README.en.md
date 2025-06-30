# Simplex Solver
## Overview
This project is a computational implementation of the Simplex method for solving Linear Programming Problems (LPPs), developed as a practical part of an Operations Research course. The solver is written in Python and built from scratch, without using external mathematical optimization libraries (such as SciPy's linprog).

The implementation uses the Two-Phase Simplex Method, allowing the solution of maximization problems with a mix of constraints of types less than or equal (<=), greater than or equal (>=), and equal (=). The code is modular and easy to maintain, with clear separation between input parsing, standardization, and the main solver logic.

## Features
- Solves Maximization Problems: The main algorithm is tailored for standard maximization problems.
- Supports All Types of Constraints: Properly handles ≤, ≥, and = constraints by adding slack, surplus, and artificial variables as needed.
- Two-Phase Simplex Method: Automatically detects when an initial feasible basis is not evident and executes Phase I before proceeding to Phase II.
- Degeneracy Handling: Includes logic to manage degenerate cases, where an artificial variable remains in the basis with value zero at the end of Phase I.
- File-Based Input: LPP models are defined using simple and readable text files.
- Detailed Output: The final solution displays a complete summary including status, optimal value of the objective function, and values of all variables (decision, slack, surplus, and artificial).

## Project Structure
The project is organized modularly, aiming for code clarity and separation of responsibilities.

```
simplex_project/
│
├── main.py                 # Main entry point of the solver.
│
├── core/
│   ├── __init__.py
│   ├── model_parser.py     # Parses the input file.
│   ├── standardizer.py     # Converts the model to standard form.
│   ├── tableau.py          # Class representing and operating on the Simplex tableau.
│   ├── pivoting.py         # Logic for choosing entering and leaving variables.
│   └── solver.py           # Core resolution algorithm (two-phase method).
│
├── examples/
│   ├── 001_simple-feasible.txt   # Simple LPP not requiring Phase I.
│   └── 002_dual_phase.txt        # More complex LPP requiring two-phase method.
│   └── ...                       # Other test LPPs
│
└── README.md               # This documentation file.
```

## Requirements
- Python 3.8 or higher
- NumPy library

## Installation
1. Clone the repository:

```bash
git clone <your-repository-url>
cd simplex_project
```

2. Create and activate a virtual environment (recommended):

- On macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

- On Windows:

```powershell
python -m venv venv
.env\Scriptsctivate
```

3. Install dependencies:

```bash
pip install numpy
```

## Usage
The solver is run via command line, passing the path to the input file containing the LPP model.

- Command

```bash
python main.py path/to/your_lpp_file.txt
```

## Input File Format
The input file should follow a simple keyword-based format. Blank lines and comments (starting with #) are ignored.

Required sections include:

- NUM_VARS: Number of decision variables (e.g., x_1, x_2, ...).
- OBJECTIVE: Objective function expression, which is always a maximization.
- CONSTRAINTS: List of constraints, one per line.

#### Variable and Coefficient Notation
Variables should be written in the format x_1, x_2, etc.
Each term must follow the form <coefficient>x_<index>, such as 3x_2, 1x_1, etc.

- The coefficient should be written before the variable when different from 1. Correct example: 4x_1 + 2x_2 <= 10
- If the coefficient is 1, it may be omitted or included:
    - Valid: x_1 + x_2 <= 10
    - Also valid: 1x_1 + 1x_2 <= 10

#### Full Example:

```makefile
# Linear Programming Problem
# Maximize P = 2x_1 + 3x_2
# Subject to:
#   x_1 + x_2 >= 4
#   2x_1 + 5x_2 <= 15
#   4x_1 + 3x_2 = 18

NUM_VARS: 2

OBJECTIVE:
2x_1 + 3x_2

CONSTRAINTS:
1x_1 + 1x_2 >= 4
2x_1 + 5x_2 <= 15
4x_1 + 3x_2 = 18
```

## Expected Output

```
--- Solving LPP from file: examples/example_lpp_2.txt ---

--- Solution ---
Status: Optimal
Optimal Value: 11.5714

Variable Values (originals):
  x_1 = 3.2143
  x_2 = 1.7143

Slack / Surplus / Artificial Variables:
  e_1 = 0.9286
  s_1 = 0.0000

Basic Variables: ['e_1', 'x_1', 'x_2']
Non-Basic Variables: ['s_1']
```

## Limitations

- Tie-Breaking Criterion: The current implementation does not use sophisticated tie-breaking rules (like Bland's Rule) to select entering/leaving variables. It uses NumPy's argmin behavior, which may cause cycling in rare pathological cases.
- Limited Input Validation: Error handling for malformed input files is basic. Incorrectly structured files may produce unexpected errors.
- Redundancy Detection: While the solver can handle redundant constraints, it does not explicitly analyze redundancy, which may affect performance or produce unnecessarily large tableaux.