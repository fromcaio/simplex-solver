# Simplex Solver

## Overview
This project is a computational implementation of the Simplex Method for solving Linear Programming Problems (LPPs), developed as a practical component of an Operations Research course. The solver is written in Python and built from scratch, with no reliance on external mathematical optimization libraries (such as SciPy's `linprog`).

It uses the **Two-Phase Simplex Method**, allowing it to solve maximization problems with a combination of constraints of type less than or equal to (≤), greater than or equal to (≥), and equal to (=). The codebase is modular and easy to maintain, with a clear separation between input parsing, standardization, and the core solver logic.

## Features

- **Solves Maximization Problems**: The core algorithm is designed for standard maximization problems.
- **Supports All Constraint Types**: Handles ≤, ≥, and = constraints by adding slack, surplus, and artificial variables as needed.
- **Two-Phase Simplex Method**: Automatically detects when an initial feasible basis is not obvious and runs Phase I before proceeding to Phase II.
- **Degeneracy Handling**: Includes logic to handle degenerate cases where an artificial variable remains in the basis with zero value after Phase I.
- **File-Based Input**: LPP models are defined in simple, human-readable text files.
- **Detailed Output**: The final solution displays a full summary including status, optimal objective function value, and values of all variables (decision, slack, surplus, and artificial).

## Project Structure

The project is organized in a modular way to ensure code clarity and separation of concerns.

```
simplex_project/
│
├── main.py # Main entry point of the solver.
│
├── core/
│ ├── init.py
│ ├── model_parser.py # Parses the input file.
│ ├── standardizer.py # Converts the model to standard form.
│ ├── tableau.py # Class for representing and manipulating the Simplex tableau.
│ ├── pivoting.py # Logic for selecting entering and leaving variables.
│ └── solver.py # Core of the solving algorithm (two-phase method).
│
├── examples/
│ ├── 001_simple-feasible.txt # Simple LPP that does not require Phase I.
│ └── 002_dual_phase.txt # More complex LPP requiring the two-phase method.
│ └── ... # Other test LPPs
│
└── README.md # This documentation file.
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

```bash
python -m venv venv
.\venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install numpy
```

## Usage
Run the solver from the command line, passing the path to the input file containing the LPP model.

- Command

```bash
python main.py path/to/your_lpp_file.txt
```

## Input File Format
The input file must follow a simple, keyword-based format. Blank lines and comments (lines starting with #) are ignored.

Required sections:

- NUM_VARS: Number of decision variables (e.g., x_1, x_2, ...).
- OBJECTIVE: The objective function expression, which is always a maximization.
- CONSTRAINTS: List of constraints, one per line.

#### Variable and Coefficient Notation
Variables should be written as x_1, x_2, etc.
Each term should follow the format <coefficient>x_<index>, such as 3x_2, 1x_1, etc.

- The coefficient should precede the variable when it is different from 1. Example: 4x_1 + 2x_2 <= 10
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

- Tie-Breaking Criteria: The current implementation does not use advanced tie-breaking rules (like Bland’s Rule) when selecting entering/leaving variables. It uses NumPy’s default argmin behavior, which may allow cycling in rare pathological cases.
- Limited Input Validation: Error handling for malformed input files is still basic. Incorrectly structured files may cause unexpected errors.
- Redundancy Detection: While the solver can handle redundant constraints, it does not explicitly detect or eliminate them, which may affect performance or lead to unnecessarily large tableaus.


## 📜 License
This project is released under an academic-use license. Redistribution or commercial use is not permitted without explicit permission.

### 👥 Author

- [@fromcaio](https://github.com/fromcaio) 
