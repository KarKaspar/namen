# Window Manufacturing App
#
# This application calculates window manufacturing dimensions based on
# product type and input parameters. It reads manufacturing rules from
# a CSV file and applies formulas to calculate frame, glass, sill, and
# other component dimensions.
#
# Key features:
# - Loads manufacturing rules from CSV file
# - Falls back to test data if CSV file not found
# - Evaluates mathematical formulas from CSV
# - Handles default parameters when no arguments provided
# - Filters out invalid (negative) measurements

import csv

class WindowManufacturingApp:
    def __init__(self, csv_file):
        self.csv_file = csv_file
        self.rules = self.load_rules()

    def load_rules(self):
        rules = {}
        try:
            with open(self.csv_file, mode='r') as file:
                reader = csv.reader(file)
                rows = list(reader)
                
                # Skip header rows
                for i in range(2, len(rows), 2):
                    if len(rows[i]) < 2:
                        continue
                    product_type = rows[i][1]
                    if i + 1 < len(rows):
                        formulas = rows[i+1]
                        # Ensure formulas has enough elements
                        if len(formulas) < 34:
                            formulas += [None] * (34 - len(formulas))
                        rules[product_type] = formulas
        except FileNotFoundError:
            # Use test data if CSV file not found
            print("Using test data - CSV file not found")
            rules = self.get_test_data()
        return rules
    
    def get_test_data(self):
        """
        Return test data when CSV file is not available
        
        Returns a dictionary with product types as keys and formula lists as values.
        Each formula list contains 34 elements corresponding to different measurement
        calculations for frame, glass, sill, and other components.
        
        Formula positions:
        0-5: Unused header positions
        6-8: Frame dimensions (L, H, tk)
        9-11: Glass/KLP dimensions (L, H, tk)
        12: Sill configuration
        13-18: Sill details (ÜH, AH, VERT with tk variants)
        19-28: Frame details (ÜH, AH, VERT, HOR, VERT2 with tk variants)
        29-32: Glass strips (H, VERT with tk variants)
        """
        return {
            '40STAND60x63': [
                None, None, None, None, None, None,  # 0-5
                'L-86', 'K-96', 'tk',  # 6-8 (raam)
                'L-86-100', 'K-96-100', 'tk',  # 9-11 (klaasi)
                'P44-14', None, None, None, None,  # 12-16 (lengi)
                None, None, None, None, None, None,  # 17-22 (raami)
                None, None, None, None, None, None,  # 23-28 (raami)
                None, None, None, None  # 29-32 (klaasiliistud)
            ]
        }

    def calculate_output(self, input_params):
        """
        Calculate all output dimensions based on input parameters and loaded rules.
        
        Args:
            input_params: Dictionary containing:
                - 'toote tyyp': Product type (e.g., '40STAND60x63')
                - 'laius': Width in mm
                - 'kõrgus': Height in mm
                - 'tk tyyptellimusel': Thickness in mm
                - 'käsi': Opening direction (P=right, V=left)
                
        Returns:
            Dictionary with calculated dimensions for all components
            
        Note:
            Uses formulas from the loaded rules CSV file
            Returns None for invalid or negative calculations
        """
        product_type = input_params['toote tyyp']
        if product_type not in self.rules:
            raise ValueError(f"Product type {product_type} not found in rules.")
        
        formulas = self.rules[product_type]
        L = input_params['laius']
        H = input_params['kõrgus']
        tk = input_params['tk tyyptellimusel']
        # In the formulas, K represents height (kõrgus), not thickness
        K = H
        
        output = {}
        
        # Calculate frame details
        output['raam_L'] = self.evaluate_formula(formulas[6], L, H, K, tk)
        output['raam_H'] = self.evaluate_formula(formulas[7], L, H, K, tk)
        output['raam_tk'] = self.evaluate_formula(formulas[8], L, H, K, tk)
        
        # Calculate glass/KLP measurements
        output['klaasi_L'] = self.evaluate_formula(formulas[9], L, H, K, tk)
        output['klaasi_H'] = self.evaluate_formula(formulas[10], L, H, K, tk)
        output['klaasi_tk'] = self.evaluate_formula(formulas[11], L, H, K, tk)
        
        # Calculate sill details
        output['lengi_konfig'] = formulas[12]
        output['lengi_UH'] = self.evaluate_formula(formulas[13], L, H, K, tk)
        output['lengi_UH_tk'] = self.evaluate_formula(formulas[14], L, H, K, tk)
        output['lengi_AH'] = self.evaluate_formula(formulas[15], L, H, K, tk)
        output['lengi_AH_tk'] = self.evaluate_formula(formulas[16], L, H, K, tk)
        output['lengi_VERT'] = self.evaluate_formula(formulas[17], L, H, K, tk)
        output['lengi_VERT_tk'] = self.evaluate_formula(formulas[18], L, H, K, tk)
        
        # Calculate frame details
        output['raami_UH'] = self.evaluate_formula(formulas[19], L, H, K, tk)
        output['raami_UH_tk'] = self.evaluate_formula(formulas[20], L, H, K, tk)
        output['raami_AH'] = self.evaluate_formula(formulas[21], L, H, K, tk)
        output['raami_AH_tk'] = self.evaluate_formula(formulas[22], L, H, K, tk)
        output['raami_VERT'] = self.evaluate_formula(formulas[23], L, H, K, tk)
        output['raami_VERT_tk'] = self.evaluate_formula(formulas[24], L, H, K, tk)
        output['raami_HOR'] = self.evaluate_formula(formulas[25], L, H, K, tk)
        output['raami_HOR_tk'] = self.evaluate_formula(formulas[26], L, H, K, tk)
        output['raami_VERT2'] = self.evaluate_formula(formulas[27], L, H, K, tk)
        output['raami_VERT2_tk'] = self.evaluate_formula(formulas[28], L, H, K, tk)
        
        # Calculate glass strips
        output['klaasiliistud_H'] = self.evaluate_formula(formulas[29], L, H, K, tk)
        output['klaasiliistud_H_tk'] = self.evaluate_formula(formulas[30], L, H, K, tk)
        output['klaasiliistud_VERT'] = self.evaluate_formula(formulas[31], L, H, K, tk)
        output['klaasiliistud_VERT_tk'] = self.evaluate_formula(formulas[32], L, H, K, tk)
        
        return output

    def evaluate_formula(self, formula, L, H, K, tk):
        """
        Evaluate a mathematical formula string with variable substitution.
        
        Args:
            formula: String containing mathematical expression with variables
            L: Width value
            H: Height value  
            K: Height value (alias for H, used in formulas)
            tk: Thickness value
            
        Returns:
            Evaluated result as integer, or None if formula is invalid or produces negative result
            
        Note:
            - Replaces variables L, H, K, tk with their numeric values
            - Handles special patterns like tkx2 (converts to tk*2)
            - Returns None for negative results (invalid measurements)
            - Returns None for empty formulas or 'konfig.' strings
        """
        if not formula or formula == 'konfig.':
            return None
        
        # Replace variables in the formula
        formula = formula.replace('L', str(L))
        formula = formula.replace('H', str(H))
        formula = formula.replace('K', str(K))
        formula = formula.replace('tk', str(tk))
        
        # Handle multiplicative equations like tkx2, tkx4
        formula = formula.replace('tkx2', f'({tk})*2')
        formula = formula.replace('tkx4', f'({tk})*4')
        
        # Handle simple multiplication like 3x2
        formula = formula.replace('x', '*')
        
        # Debug: Print the formula before evaluation
        print(f"Evaluating formula: {formula}")
        
        # Evaluate the formula
        try:
            result = eval(formula)
            # Return None for negative results (invalid measurements)
            return result if result >= 0 else None
        except Exception as e:
            print(f"Error evaluating formula '{formula}': {e}")
            return None

# Example usage
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Window Manufacturing App')
    parser.add_argument('--toote-tyyp', type=str, default='40STAND60x63', help='Product type')
    parser.add_argument('--laius', type=int, default=900, help='Width')
    parser.add_argument('--kõrgus', type=int, default=900, help='Height')
    parser.add_argument('--tk-tyyptellimusel', type=int, default=3, help='Thickness specified in the order')
    parser.add_argument('--käsi', type=str, default='P', help='Direction the window opens (P for right, V for left)')
    
    args = parser.parse_args()
    
    app = WindowManufacturingApp("Tootmisreeglid - Sheet1.csv")
    
    # Input parameters from CLI (or defaults)
    input_params = {
        'toote tyyp': args.toote_tyyp,
        'laius': args.laius,
        'kõrgus': args.kõrgus,
        'tk tyyptellimusel': args.tk_tyyptellimusel,
        'käsi': args.käsi
    }
    
    output = app.calculate_output(input_params)
    print("Output Parameters:")
    for key, value in output.items():
        if value is not None:
            print(f"{key}: {value}")


# CHANGELOG / DEVELOPMENT NOTES
# =============================
#
# v1.1 (Current version) - Fixed calculations and added documentation
# - Fixed formula evaluation: K now correctly represents height (kõrgus) not thickness
# - Added comprehensive docstrings to all major methods
# - Added default parameters for command-line usage (no args needed)
# - Improved formula parsing: handles tkx2, tkx4, and simple multiplication
# - Filters out negative/invalid measurements from output
# - Added fallback to test data when CSV file not found
# - Added detailed comments explaining formula positions and structure
#
# v1.0 (Original) - Basic functionality
# - Loaded rules from CSV file
# - Basic formula evaluation with variable substitution
# - Command-line interface with required parameters
#
# KEY INSIGHTS:
# - In CSV formulas, K represents height (kõrgus), not thickness parameter
# - Formulas use patterns like tkx2 (thickness × 2) and K-96 (height - 96)
# - Negative results are invalid and filtered out
# - Test data provides fallback when CSV file is missing
#
# USAGE:
# python3 app.py                                    # Uses defaults (40STAND60x63, 900x900, tk=3, P)
# python3 app.py --help                             # Show all options
# python3 app.py --toote-tyyp TA --laius 1200 --kõrgus 1000 --tk-tyyptellimusel 5 --käsi V
#
# QUICK REFERENCE:
# --toote-tyyp: Product type (e.g., "40STAND60x63", "77STAND60x70")
# --laius: Width in millimeters
# --kõrgus: Height in millimeters  
# --tk-tyyptellimusel: Thickness in millimeters
# --käsi: Opening direction (P = right, V = left)
#
# All parameters are optional and have sensible defaults for quick testing.


# CHANGELOG / DEVELOPMENT NOTES
# =============================
#
# v1.1 (Current version) - Fixed calculations and added documentation
# - Fixed formula evaluation: K now correctly represents height (kõrgus) not thickness
# - Added comprehensive docstrings to all major methods
# - Added default parameters for command-line usage (no args needed)
# - Improved formula parsing: handles tkx2, tkx4, and simple multiplication
# - Filters out negative/invalid measurements from output
# - Added fallback to test data when CSV file not found
# - Added detailed comments explaining formula positions and structure
#
# v1.0 (Original) - Basic functionality
# - Loaded rules from CSV file
# - Basic formula evaluation with variable substitution
# - Command-line interface with required parameters
