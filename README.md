# Window Size Calculator

A Python tool for calculating window frame dimensions based on glass sizes and configurable rules.

## Features
- Calculate frame dimensions from window glass sizes
- Configurable rules via Excel file
- Input validation and error handling
- Comprehensive output with all frame measurements

## Installation

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Install Dependencies
```bash
pip install pandas openpyxl
```

## Usage

### Basic Usage
```bash
python window_size_calculator.py
```
Then enter the window width and height when prompted.

### Using Custom Rules
1. Create an Excel file with your rules (see `example_rules.xlsx`)
2. Modify the script to load your rules:
```python
calculator = WindowSizeCalculator("your_rules.xlsx")
```

### Programmatic Usage
```python
from window_size_calculator import WindowSizeCalculator

# Initialize calculator
calc = WindowSizeCalculator()  # or WindowSizeCalculator("your_rules.xlsx")

# Calculate frame dimensions
result = calc.calculate_sides(800, 1200)  # width, height in mm

print(f"Frame width: {result['total_frame_width']:.2f} mm")
print(f"Frame height: {result['total_frame_height']:.2f} mm")
```

## Excel Rules Format

Create an Excel file with two columns:

| Parameter          | Value  |
|--------------------|--------|
| min_width          | 300    |
| max_width          | 2000   |
| min_height         | 300    |
| max_height         | 2000   |
| side_ratio         | 0.15   |
| min_side_thickness | 20     |
| max_side_thickness | 100    |

## Example Rules File

An example file `example_rules.xlsx` is included with default values.

## Output Explanation

The calculator returns a dictionary with these measurements:
- `original_width`, `original_height`: Input glass dimensions
- `side_thickness`: Calculated frame thickness
- `top_side`, `bottom_side`: Total top/bottom frame lengths
- `left_side`, `right_side`: Total left/right frame lengths
- `total_frame_width`, `total_frame_height`: Overall frame dimensions

## License
MIT License - Free to use and modify.

## Contributing
Pull requests are welcome. For major changes, please open an issue first.
