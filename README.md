# 🧮 Advanced Scientific Calculator

A feature-rich scientific calculator designed specifically for B.Tech students, built with Python and Tkinter.

![Calculator Preview](/scin.png)

## ✨ Features

### Core Functionality
- **Basic Operations:** Addition, subtraction, multiplication, division
- **Scientific Functions:** 
  - Trigonometric (sin, cos, tan) and their inverses
  - Logarithmic functions (log, ln)
  - Exponential functions (e^x, 10^x)
  - Powers and roots (x², x³, √x, ∛x)
- **Memory Functions:** Store and recall values with MC, MR, and M+
- **Constants:** π, e for mathematical calculations

### Enhanced UX/UI
- **Dual Themes:** Switch between dark and light modes
- **Calculation History:** Track previous calculations in a scrollable panel
- **Keyboard Support:** Use your keyboard for swift data entry
- **DEG/RAD Toggle:** Easily switch between degree and radian modes
- **Clean, Modern Interface:** Color-coded buttons and intuitive layout

## 🚀 Getting Started

### Prerequisites
- Python 3.6 or higher
- Tkinter (usually comes with Python installation)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/scientific-calculator.git
   cd scientific-calculator
   ```

2. Run the calculator:
   ```bash
   python calculator.py
   ```

## 📋 Usage Guide

### Basic Operations
- Click number buttons or use keyboard to input values
- Use operation buttons (+, -, ×, ÷) for arithmetic operations
- Press "=" or Enter key to calculate results

### Scientific Functions
- **Trigonometric:** sin, cos, tan, and their inverses
- **Logarithmic:** log (base 10), ln (natural logarithm)
- **Powers:** x², x³, or xʸ for custom powers
- **Roots:** √x for square root, ∛x for cube root

### Additional Features
- **Toggle +/-:** Change sign of the current number
- **DEG/RAD:** Switch between degree and radian modes for trigonometric calculations
- **Theme Switch:** Use the sun/moon button to toggle between dark and light themes
- **History Panel:** View your calculation history on the right side
- **Memory Functions:**
  - MC: Clear memory
  - MR: Recall memory value
  - M+: Add current value to memory

## 🔧 Keyboard Shortcuts

- **Numbers & Operators:** Type directly using keyboard
- **Enter:** Calculate result (same as "=")
- **Backspace:** Remove last character
- **Escape:** Clear all (same as "C")

## 🛠️ Technical Details

### Architecture
The calculator is built using an object-oriented approach with:
- Main calculator class managing the application state
- Custom mathematical functions for specialized operations
- Responsive Tkinter UI with ttk styling for modern appearance

### Mathematical Implementation
- Handles complex expressions with proper operator precedence
- Converts between degrees and radians automatically
- Provides high precision calculations

## 📝 For Developers

### Extending the Calculator
The modular design makes it easy to add new functions:

1. Add a new button in the `create_scientific_buttons` method
2. Implement the function handler in `add_scientific_function`
3. Add the evaluation logic in `evaluate_expression`

### Customizing the UI
Modify the `create_styles` method to change:
- Color schemes
- Button appearances
- Font styles and sizes

## 📜 License

This project is licensed under the MIT License

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

Created with ❤️ for engineering students
