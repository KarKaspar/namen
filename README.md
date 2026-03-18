# NTR0670_Praks4_WindowApp
Tunnis tehtud akna parameetrite app, loodud Mistral Vibe kasutades

# Window Manufacturing Business Logic

## Overview
This document outlines the business logic for calculating window dimensions and components based on client-provided input parameters.

## Input Parameters
The client provides the following parameters:
- **A/U**: Type of window (A for single window, TA for double window).
- **toote tyyp**: Product type (e.g., 40STAND60x63, 77STAND60x70).
- **laius**: Width of the window.
- **kõrgus**: Height of the window.
- **tk tyyptellimusel**: Thickness specified in the order.
- **käsi**: Direction the window opens (P for right, V for left).

## Output Parameters
The app calculates the following output parameters:
- **raam**: Frame details (L, H, tk).
- **klaasi/KLP mõõt**: Glass/KLP measurements (L, H, tk).
- **lengi detailid**: Details for the sill (konfig, ÜH, AH, VERT with tk variants).
- **raami detailid**: Details for the frame (ÜH, AH, VERT, HOR, VERT2 with tk variants).
- **klaasiliistud**: Glass strips (H, VERT with tk variants).

## Formulas
The formulas for calculating the output parameters are provided in the CSV file. Here are some examples:

### For Product Type 40STAND60x63
- **Frame Width**: `L-86`
- **Frame Height**: `K-96` (where K = height)
- **Glass Width**: `L-86-100`
- **Glass Height**: `K-96-100`
- **Sill VERT**: `K-50`
- **Sill VERT tk**: `tkx2` (thickness × 2)

### For Product Type 77STAND60x70
- **Frame Width**: `(L-80)/2`
- **Frame Height**: `K-96` (where K = height)
- **Glass Width**: `((L-80)/2)-100`
- **Glass Height**: `K-96-100`
- **Frame VERT tk**: `tkx4` (thickness × 4)

## Key Implementation Details

### Variable Mapping
- **L**: Width (laius) from input parameters
- **H**: Height (kõrgus) from input parameters  
- **K**: Height (kõrgus) - same as H, used in formulas
- **tk**: Thickness (tk tyyptellimusel) from input parameters

### Formula Patterns
- `tkx2`, `tkx4`: Multiplicative patterns (e.g., `tkx2` = thickness × 2)
- Simple `x`: Multiplication (e.g., `3x2` = 3 × 2)
- Negative results: Filtered out as invalid measurements

## App Structure
The app consists of the following components:
1. **Input Module**: Command-line interface with default parameters.
2. **Processing Module**: Formula evaluation and calculation engine.
3. **Output Module**: Filtered display of valid measurements only.

## Implementation Steps
1. **Load Rules**: Read manufacturing rules from CSV file or use test data fallback.
2. **Parse Input**: Receive client parameters with defaults for easy testing.
3. **Apply Formulas**: Evaluate mathematical expressions with variable substitution.
4. **Filter Results**: Remove negative/invalid measurements.
5. **Display Output**: Show only valid calculated parameters.

## Testing
The app has been tested with:
- Default parameters (40STAND60x63, 900×900, tk=3, P)
- Various product types from the CSV
- Edge cases (missing CSV file, invalid formulas)
- Verification against expected output values

## How to Run the Application

### Basic Usage (with defaults)
```bash
python3 app.py
```
This runs the app with default parameters:
- Product type: 40STAND60x63
- Width: 900 mm
- Height: 900 mm
- Thickness: 3 mm
- Direction: P (right)

### Custom Parameters
```bash
python3 app.py --toote-tyyp "77STAND60x70" --laius 1250 --kõrgus 956 --tk-tyyptellimusel 10 --käsi P
```

### Parameter Descriptions
- `--toote-tyyp`: Product type (e.g., "40STAND60x63", "77STAND60x70")
- `--laius`: Width in millimeters
- `--kõrgus`: Height in millimeters
- `--tk-tyyptellimusel`: Thickness in millimeters
- `--käsi`: Opening direction (P = right, V = left)

### View Help
```bash
python3 app.py --help
```

### Expected Output Format
The app displays calculated measurements in the format:
```
Output Parameters:
raam_L: 814
raam_H: 804
raam_tk: 3
klaasi_L: 714
klaasi_H: 704
...
```

## Recent Improvements (v1.1)
- Fixed formula evaluation: K now correctly represents height
- Added comprehensive documentation and docstrings
- Default parameters for easy testing (no arguments needed)
- Improved formula parsing for multiplication patterns
- Test data fallback when CSV file not found
- Clean output filtering (only valid measurements shown)
