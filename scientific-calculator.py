import tkinter as tk
from tkinter import ttk, messagebox
import math
import cmath
from decimal import Decimal, getcontext
import re

class ModernScientificCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Scientific Calculator")
        self.root.geometry("720x580")
        self.root.resizable(True, True)
        self.root.configure(bg="#2c3e50")
        
        # Set app icon
        try:
            self.root.iconbitmap("calculator.ico")
        except:
            pass
        
        # Set higher precision for calculations
        getcontext().prec = 16
        
        # Variables
        self.current_expression = ""
        self.total_expression = ""
        self.last_answer = "0"
        self.is_degree_mode = True
        self.history = []
        self.theme = "dark"  # Default theme
        
        # Create themed styles
        self.create_styles()
        
        # Create main frames
        self.create_display_frame()
        self.create_buttons_frame()
        self.create_history_frame()
        
        # Configure grid weights
        self.root.grid_columnconfigure(0, weight=3)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        
        # Bind keyboard events
        self.root.bind("<Key>", self.key_press)
        
    def create_styles(self):
        self.style = ttk.Style()
        
        # Configure dark theme
        self.style.theme_use('clam')
        
        # Main background
        self.style.configure('Main.TFrame', background="#2c3e50")
        
        # Display frame
        self.style.configure('Display.TFrame', background="#1e2b38")
        self.style.configure('Display.TLabel', 
                            background="#1e2b38", 
                            foreground="#ecf0f1", 
                            font=("Segoe UI", 12))
        self.style.configure('BigDisplay.TLabel', 
                            background="#1e2b38", 
                            foreground="#ecf0f1", 
                            font=("Segoe UI", 24, "bold"))
        self.style.configure('ModeDisplay.TLabel', 
                            background="#1e2b38", 
                            foreground="#3498db", 
                            font=("Segoe UI", 10))
        
        # Buttons
        self.style.configure('NumButton.TButton', 
                            font=("Segoe UI", 12),
                            background="#34495e",
                            foreground="#ecf0f1")
        self.style.map('NumButton.TButton',
                      background=[('active', '#2c3e50')],
                      relief=[('pressed', 'sunken')])
        
        self.style.configure('OpButton.TButton', 
                            font=("Segoe UI", 12),
                            background="#3498db",
                            foreground="#ecf0f1")
        self.style.map('OpButton.TButton',
                      background=[('active', '#2980b9')],
                      relief=[('pressed', 'sunken')])
        
        self.style.configure('FuncButton.TButton', 
                            font=("Segoe UI", 11),
                            background="#2c3e50",
                            foreground="#ecf0f1")
        self.style.map('FuncButton.TButton',
                      background=[('active', '#233140')],
                      relief=[('pressed', 'sunken')])
        
        self.style.configure('SpecialButton.TButton', 
                            font=("Segoe UI", 12),
                            background="#e74c3c",
                            foreground="#ecf0f1")
        self.style.map('SpecialButton.TButton',
                      background=[('active', '#c0392b')],
                      relief=[('pressed', 'sunken')])
        
        self.style.configure('EqualButton.TButton', 
                            font=("Segoe UI", 14, "bold"),
                            background="#2ecc71",
                            foreground="#ecf0f1")
        self.style.map('EqualButton.TButton',
                      background=[('active', '#27ae60')],
                      relief=[('pressed', 'sunken')])
        
        # History frame
        self.style.configure('History.TFrame', background="#1e2b38")
        self.style.configure('History.TLabel', 
                            background="#1e2b38", 
                            foreground="#ecf0f1", 
                            font=("Segoe UI", 12, "bold"))
        
    def create_display_frame(self):
        self.display_frame = ttk.Frame(self.root, style='Display.TFrame')
        self.display_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.display_frame.configure(padding=(15, 15))
        
        # Title and mode display in a sub-frame
        title_frame = ttk.Frame(self.display_frame, style='Display.TFrame')
        title_frame.pack(fill="x", pady=(0, 10))
        
        calc_title = ttk.Label(title_frame, text="Scientific Calculator", style='Display.TLabel')
        calc_title.pack(side="left")
        
        # Mode display (RAD/DEG)
        self.mode_display = ttk.Label(title_frame, text="DEG", style='ModeDisplay.TLabel')
        self.mode_display.pack(side="right")
        
        # Theme toggle button
        self.theme_button = ttk.Button(
            title_frame, 
            text="☀️", 
            command=self.toggle_theme,
            style='FuncButton.TButton',
            width=3
        )
        self.theme_button.pack(side="right", padx=10)
        
        # Total expression display (shows the full calculation)
        self.total_expression_label = ttk.Label(
            self.display_frame, 
            text="", 
            style='Display.TLabel',
            anchor="e"
        )
        self.total_expression_label.pack(fill="x", pady=5)
        
        # Current expression display (shows current input/result)
        self.current_expression_label = ttk.Label(
            self.display_frame, 
            text="0", 
            style='BigDisplay.TLabel',
            anchor="e"
        )
        self.current_expression_label.pack(fill="x", pady=5)
    
    def create_history_frame(self):
        self.history_frame = ttk.Frame(self.root, style='History.TFrame')
        self.history_frame.grid(row=0, column=1, rowspan=2, sticky="nsew", padx=10, pady=10)
        
        history_title_frame = ttk.Frame(self.history_frame, style='History.TFrame')
        history_title_frame.pack(fill="x", pady=5, padx=10)
        
        history_label = ttk.Label(history_title_frame, text="History", style='History.TLabel')
        history_label.pack(side="left")
        
        clear_history_btn = ttk.Button(
            history_title_frame, 
            text="Clear", 
            command=self.clear_history,
            style='SpecialButton.TButton',
            width=6
        )
        clear_history_btn.pack(side="right")
        
        # History display with custom colors
        self.history_text = tk.Text(
            self.history_frame, 
            width=25, 
            height=22, 
            font=("Segoe UI", 10),
            bg="#1e2b38",
            fg="#ecf0f1",
            bd=0,
            padx=10,
            pady=5
        )
        self.history_text.pack(fill="both", expand=True, padx=5, pady=5)
        self.history_text.config(state="disabled")
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.history_text)
        scrollbar.pack(side="right", fill="y")
        self.history_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.history_text.yview)
        
    def create_buttons_frame(self):
        self.buttons_frame = ttk.Frame(self.root, style='Main.TFrame')
        self.buttons_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        
        # Configure grid for buttons
        for i in range(7):
            self.buttons_frame.grid_columnconfigure(i, weight=1)
        for i in range(6):
            self.buttons_frame.grid_rowconfigure(i, weight=1)
        
        # Define button layout
        self.create_scientific_buttons()
        self.create_number_buttons()
        self.create_operator_buttons()
        self.create_special_buttons()
        
    def create_scientific_buttons(self):
        scientific_functions = [
            # First row - Trigonometric
            ("sin", 0, 0, 'FuncButton.TButton'), 
            ("cos", 0, 1, 'FuncButton.TButton'), 
            ("tan", 0, 2, 'FuncButton.TButton'),
            # Second row - Inverse Trigonometric
            ("asin", 1, 0, 'FuncButton.TButton'), 
            ("acos", 1, 1, 'FuncButton.TButton'), 
            ("atan", 1, 2, 'FuncButton.TButton'),
            # Third row - Logarithmic and exponential
            ("log", 2, 0, 'FuncButton.TButton'), 
            ("ln", 2, 1, 'FuncButton.TButton'), 
            ("e^x", 2, 2, 'FuncButton.TButton'),
            # Fourth row - Powers
            ("x²", 3, 0, 'FuncButton.TButton'), 
            ("x³", 3, 1, 'FuncButton.TButton'), 
            ("xʸ", 3, 2, 'FuncButton.TButton'),
            # Fifth row - Roots
            ("√x", 4, 0, 'FuncButton.TButton'), 
            ("∛x", 4, 1, 'FuncButton.TButton'), 
            ("10ˣ", 4, 2, 'FuncButton.TButton'),
            # Sixth row - Constants and functions
            ("π", 5, 0, 'FuncButton.TButton'), 
            ("e", 5, 1, 'FuncButton.TButton'), 
            ("abs", 5, 2, 'FuncButton.TButton'),
            # Additional row - Mode and parentheses
            ("DEG/RAD", 0, 3, 'FuncButton.TButton'),
            ("(", 0, 4, 'FuncButton.TButton'), 
            (")", 0, 5, 'FuncButton.TButton'),
            # Memory functions
            ("MC", 1, 3, 'FuncButton.TButton'),
            ("MR", 1, 4, 'FuncButton.TButton'),
            ("M+", 1, 5, 'FuncButton.TButton'),
            # Advanced functions
            ("%", 2, 3, 'FuncButton.TButton'),
            ("1/x", 2, 4, 'FuncButton.TButton'),
            ("n!", 2, 5, 'FuncButton.TButton'),
        ]
        
        for function_text, row, col, style in scientific_functions:
            button = ttk.Button(
                self.buttons_frame, 
                text=function_text,
                command=lambda f=function_text: self.add_scientific_function(f),
                style=style,
                width=3
            )
            button.grid(row=row, column=col, padx=3, pady=3, sticky="nsew")
    
    def create_number_buttons(self):
        # Create buttons for digits 0-9
        digit_style = 'NumButton.TButton'
        
        for digit in range(1, 10):
            row = 2 + (9 - digit) // 3
            col = (digit - 1) % 3 + 3
            button = ttk.Button(
                self.buttons_frame,
                text=str(digit),
                command=lambda d=digit: self.add_to_expression(str(d)),
                style=digit_style,
                width=3
            )
            button.grid(row=row, column=col, padx=3, pady=3, sticky="nsew")
        
        # Zero button
        button = ttk.Button(
            self.buttons_frame,
            text="0",
            command=lambda: self.add_to_expression("0"),
            style=digit_style,
            width=3
        )
        button.grid(row=5, column=4, padx=3, pady=3, sticky="nsew")
        
        # Decimal point
        decimal_button = ttk.Button(
            self.buttons_frame,
            text=".",
            command=lambda: self.add_to_expression("."),
            style=digit_style,
            width=3
        )
        decimal_button.grid(row=5, column=5, padx=3, pady=3, sticky="nsew")
        
        # Plus/minus toggle
        pm_button = ttk.Button(
            self.buttons_frame,
            text="±",
            command=self.toggle_sign,
            style=digit_style,
            width=3
        )
        pm_button.grid(row=5, column=3, padx=3, pady=3, sticky="nsew")
        
    def create_operator_buttons(self):
        operators = [
            ("+", 3, 6, 'OpButton.TButton'), 
            ("-", 4, 6, 'OpButton.TButton'), 
            ("×", 5, 6, 'OpButton.TButton'), 
            ("÷", 2, 6, 'OpButton.TButton')
        ]
        
        for operator, row, col, style in operators:
            button = ttk.Button(
                self.buttons_frame,
                text=operator,
                command=lambda o=operator: self.add_to_expression(self.get_operator_symbol(o)),
                style=style,
                width=3
            )
            button.grid(row=row, column=col, padx=3, pady=3, sticky="nsew")
    
    def create_special_buttons(self):
        # Clear button (C)
        clear_button = ttk.Button(
            self.buttons_frame,
            text="C",
            command=self.clear,
            style='SpecialButton.TButton',
            width=3
        )
        clear_button.grid(row=0, column=6, padx=3, pady=3, sticky="nsew")
        
        # Backspace button (⌫)
        backspace_button = ttk.Button(
            self.buttons_frame,
            text="⌫",
            command=self.backspace,
            style='SpecialButton.TButton',
            width=3
        )
        backspace_button.grid(row=1, column=6, padx=3, pady=3, sticky="nsew")
        
        # Answer button (Ans)
        ans_button = ttk.Button(
            self.buttons_frame,
            text="Ans",
            command=lambda: self.add_to_expression("Ans"),
            style='FuncButton.TButton',
            width=3
        )
        ans_button.grid(row=5, column=6, padx=3, pady=3, sticky="nsew")
        
        # Equal button (=)
        equal_button = ttk.Button(
            self.buttons_frame,
            text="=",
            command=self.evaluate,
            style='EqualButton.TButton',
            width=3
        )
        equal_button.grid(row=6, column=3, columnspan=4, padx=3, pady=3, sticky="nsew")
    
    def get_operator_symbol(self, op):
        if op == "×":
            return "*"
        elif op == "÷":
            return "/"
        else:
            return op
    
    def add_to_expression(self, value):
        self.current_expression += value
        self.update_display()
    
    def add_scientific_function(self, function):
        if function == "sin":
            self.current_expression += "sin("
        elif function == "cos":
            self.current_expression += "cos("
        elif function == "tan":
            self.current_expression += "tan("
        elif function == "asin":
            self.current_expression += "asin("
        elif function == "acos":
            self.current_expression += "acos("
        elif function == "atan":
            self.current_expression += "atan("
        elif function == "log":
            self.current_expression += "log10("
        elif function == "ln":
            self.current_expression += "log("
        elif function == "e^x":
            self.current_expression += "exp("
        elif function == "x²":
            self.current_expression += "^2"
        elif function == "x³":
            self.current_expression += "^3"
        elif function == "xʸ":
            self.current_expression += "^"
        elif function == "√x":
            self.current_expression += "sqrt("
        elif function == "∛x":
            self.current_expression += "cbrt("
        elif function == "10ˣ":
            self.current_expression += "10^"
        elif function == "π":
            self.current_expression += "pi"
        elif function == "e":
            self.current_expression += "e"
        elif function == "abs":
            self.current_expression += "abs("
        elif function == "(":
            self.current_expression += "("
        elif function == ")":
            self.current_expression += ")"
        elif function == "%":
            self.current_expression += "%"
        elif function == "1/x":
            self.current_expression += "1/"
        elif function == "n!":
            self.current_expression += "fact("
        elif function == "DEG/RAD":
            self.toggle_angle_mode()
            return
        elif function == "MC":
            self.memory_clear()
            return
        elif function == "MR":
            self.memory_recall()
            return
        elif function == "M+":
            self.memory_add()
            return
            
        self.update_display()
    
    def toggle_angle_mode(self):
        self.is_degree_mode = not self.is_degree_mode
        mode_text = "DEG" if self.is_degree_mode else "RAD"
        self.mode_display.config(text=mode_text)
    
    def toggle_sign(self):
        if self.current_expression and self.current_expression[0] == "-":
            self.current_expression = self.current_expression[1:]
        else:
            self.current_expression = "-" + self.current_expression
        self.update_display()
    
    def memory_clear(self):
        self.memory_value = "0"
        messagebox.showinfo("Memory", "Memory cleared")
    
    def memory_recall(self):
        if hasattr(self, 'memory_value'):
            self.current_expression += self.memory_value
            self.update_display()
        else:
            messagebox.showinfo("Memory", "Memory is empty")
    
    def memory_add(self):
        if self.current_expression:
            try:
                value = self.evaluate_expression(self.current_expression)
                if hasattr(self, 'memory_value'):
                    self.memory_value = str(float(self.memory_value) + float(value))
                else:
                    self.memory_value = value
                messagebox.showinfo("Memory", f"Value {value} added to memory")
            except:
                messagebox.showerror("Error", "Cannot add current expression to memory")
    
    def clear(self):
        self.current_expression = ""
        self.total_expression = ""
        self.update_display()
    
    def clear_history(self):
        self.history = []
        self.history_text.config(state="normal")
        self.history_text.delete(1.0, tk.END)
        self.history_text.config(state="disabled")
    
    def backspace(self):
        self.current_expression = self.current_expression[:-1]
        self.update_display()
    
    def update_display(self):
        if not self.current_expression:
            self.current_expression_label.config(text="0")
        else:
            # Convert internal representation to display representation
            display_text = self.current_expression
            display_text = display_text.replace("*", "×")
            display_text = display_text.replace("/", "÷")
            display_text = display_text.replace("pi", "π")
            display_text = display_text.replace("log10(", "log(")
            display_text = display_text.replace("log(", "ln(")
            display_text = display_text.replace("exp(", "e^(")
            display_text = display_text.replace("sqrt(", "√(")
            display_text = display_text.replace("cbrt(", "∛(")
            display_text = display_text.replace("^2", "²")
            display_text = display_text.replace("^3", "³")
            display_text = display_text.replace("fact(", "!")
            display_text = display_text.replace("Ans", self.last_answer)
            
            self.current_expression_label.config(text=display_text)
        
        self.total_expression_label.config(text=self.total_expression)
    
    def toggle_theme(self):
        if self.theme == "dark":
            # Switch to light theme
            self.theme = "light"
            self.theme_button.config(text="🌙")
            self.root.configure(bg="#ecf0f1")
            
            # Update styles for light theme
            self.style.configure('Main.TFrame', background="#ecf0f1")
            self.style.configure('Display.TFrame', background="#f8f9fa")
            self.style.configure('Display.TLabel', background="#f8f9fa", foreground="#2c3e50")
            self.style.configure('BigDisplay.TLabel', background="#f8f9fa", foreground="#2c3e50")
            self.style.configure('ModeDisplay.TLabel', background="#f8f9fa", foreground="#3498db")
            
            self.style.configure('History.TFrame', background="#f8f9fa")
            self.style.configure('History.TLabel', background="#f8f9fa", foreground="#2c3e50")
            
            # Update text widget colors
            self.history_text.config(bg="#f8f9fa", fg="#2c3e50")
            
        else:
            # Switch to dark theme
            self.theme = "dark"
            self.theme_button.config(text="☀️")
            self.root.configure(bg="#2c3e50")
            
            # Update styles for dark theme
            self.style.configure('Main.TFrame', background="#2c3e50")
            self.style.configure('Display.TFrame', background="#1e2b38")
            self.style.configure('Display.TLabel', background="#1e2b38", foreground="#ecf0f1")
            self.style.configure('BigDisplay.TLabel', background="#1e2b38", foreground="#ecf0f1")
            self.style.configure('ModeDisplay.TLabel', background="#1e2b38", foreground="#3498db")
            
            self.style.configure('History.TFrame', background="#1e2b38")
            self.style.configure('History.TLabel', background="#1e2b38", foreground="#ecf0f1")
            
            # Update text widget colors
            self.history_text.config(bg="#1e2b38", fg="#ecf0f1")
    
    def evaluate(self):
        if not self.current_expression:
            return
        
        # Save the current expression for history
        expression_to_evaluate = self.current_expression
        
        try:
            # Evaluate the expression
            result = self.evaluate_expression(expression_to_evaluate)
            
            # Display the expression in history
            display_expression = self.current_expression
            display_expression = display_expression.replace("*", "×")
            display_expression = display_expression.replace("/", "÷")
            
            # Update the display
            self.total_expression = display_expression
            self.current_expression = ""
            self.current_expression_label.config(text=result)
            self.last_answer = result
            
            # Add to history
            self.add_to_history(display_expression, result)
            
        except Exception as e:
            self.current_expression_label.config(text="Error")
            messagebox.showerror("Error", f"Invalid expression: {str(e)}")
    
    def evaluate_expression(self, expression):
        # Replace display representation with computable representation
        expression = expression.replace("pi", "math.pi")
        expression = expression.replace("e", "math.e")
        expression = expression.replace("^", "**")
        expression = expression.replace("log10(", "math.log10(")
        expression = expression.replace("log(", "math.log(")
        expression = expression.replace("exp(", "math.exp(")
        expression = expression.replace("sin(", "self.calculate_sin(")
        expression = expression.replace("cos(", "self.calculate_cos(")
        expression = expression.replace("tan(", "self.calculate_tan(")
        expression = expression.replace("asin(", "self.calculate_asin(")
        expression = expression.replace("acos(", "self.calculate_acos(")
        expression = expression.replace("atan(", "self.calculate_atan(")
        expression = expression.replace("sqrt(", "math.sqrt(")
        expression = expression.replace("cbrt(", "self.cbrt(")
        expression = expression.replace("abs(", "abs(")
        expression = expression.replace("fact(", "math.factorial(")
        expression = expression.replace("%", "/100")
        expression = expression.replace("Ans", self.last_answer)
        
        # Evaluate the expression
        result = eval(expression)
        
        # Format the result
        if isinstance(result, (int, float, complex)):
            if isinstance(result, complex):
                formatted_result = str(result)
            else:
                # Handle very large or very small numbers with scientific notation
                if abs(result) > 1e10 or (abs(result) < 1e-10 and result != 0):
                    formatted_result = f"{result:.10e}"
                else:
                    # For regular numbers, limit decimal places
                    formatted_result = f"{result:.10g}"
        else:
            formatted_result = str(result)
            
        return formatted_result
    
    def add_to_history(self, expression, result):
        history_entry = f"{expression} = {result}\n"
        self.history.append(history_entry)
        
        # Update history display
        self.history_text.config(state="normal")
        self.history_text.insert(tk.END, history_entry)
        self.history_text.see(tk.END)  # Scroll to the bottom
        self.history_text.config(state="disabled")
    
    # Trigonometric functions that handle degrees/radians conversion
    def calculate_sin(self, x):
        if self.is_degree_mode:
            return math.sin(math.radians(x))
        return math.sin(x)
        
    def calculate_cos(self, x):
        if self.is_degree_mode:
            return math.cos(math.radians(x))
        return math.cos(x)
        
    def calculate_tan(self, x):
        if self.is_degree_mode:
            return math.tan(math.radians(x))
        return math.tan(x)
        
    def calculate_asin(self, x):
        result = math.asin(x)
        if self.is_degree_mode:
            return math.degrees(result)
        return result
        
    def calculate_acos(self, x):
        result = math.acos(x)
        if self.is_degree_mode:
            return math.degrees(result)
        return result
        
    def calculate_atan(self, x):
        result = math.atan(x)
        if self.is_degree_mode:
            return math.degrees(result)
        return result
    
    def cbrt(self, x):
        # Cube root function
        if x >= 0:
            return math.pow(x, 1/3)
        else:
            return -math.pow(abs(x), 1/3)
    
    def key_press(self, event):
        key = event.char
        
        if key in "0123456789.":
            self.add_to_expression(key)
        elif key in "+-*/":
            self.add_to_expression(key)
        elif key == "=":
            self.evaluate()
        elif key == "\r":  # Enter key
            self.evaluate()
        elif key == "\x08":  # Backspace
            self.backspace()

if __name__ == "__main__":
    root = tk.Tk()
    calculator = ModernScientificCalculator(root)
    root.mainloop()