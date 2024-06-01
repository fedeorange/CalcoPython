import tkinter as tk
from tkinter import simpledialog
import re

# Global variable to keep track of the number of open calculators
num_calculators = 0

# Global variable to track if the equal button was pressed
equal_pressed = False

# Function to handle button clicks
def button_click(char):
    global equal_pressed
    if equal_pressed:
        equal_pressed = False
        text_widget.config(state=tk.NORMAL)
        text_widget.delete("1.0", tk.END)
    current = text_widget.get("1.0", tk.END).strip()
    if current == "Error":
        current = ""
    text_widget.delete("1.0", tk.END)
    text_widget.insert(tk.END, current + str(char))

# Function to clear the text widget
def button_clear():
    text_widget.config(state=tk.NORMAL)
    text_widget.delete("1.0", tk.END)

# Function to handle the equal button
def button_equal(event=None):
    global equal_pressed
    expression = text_widget.get("1.0", tk.END).strip()
    expression = preprocess_expression(expression)
    try:
        result = eval(expression)
        text_widget.delete("1.0", tk.END)
        text_widget.insert(tk.END, result)
        text_widget.config(state=tk.DISABLED)
        equal_pressed = True
    except Exception as e:  # Catch any exception and print error
        print(e)
        text_widget.delete("1.0", tk.END)
        text_widget.insert(tk.END, "Error")

# Function to preprocess the expression for percentage handling
def preprocess_expression(expression):
    # Find all occurrences of percentage and replace appropriately
    def replace_percentage(match):
        number = match.group(1)
        percentage = match.group(2)
        return f'({number} * (1 - {percentage} / 100))'
    
    expression = re.sub(r'(\d+)\s*-\s*(\d+)%', replace_percentage, expression)
    return expression.replace('÷', '/')

# Function to create a new calculator
def create_new_calculator():
    global num_calculators
    if num_calculators < 8:
        new_window = tk.Toplevel(window)
        new_window.title("Calcolatrice")

        # Ask for title input
        title = simpledialog.askstring("Input", "Enter a title for this calculator:", parent=new_window)
        if title:
            new_window.title(title)

        new_text_widget = tk.Text(new_window, width=30, height=3, font=('Arial', 14))
        new_text_widget.grid(row=0, columnspan=6, padx=10, pady=10)
        new_text_widget.bind("<Return>", lambda event: button_equal_entry(new_text_widget))
        create_buttons(new_window, new_text_widget)

        num_calculators += 1

# Function to create buttons
def create_buttons(root, text_widget):
    numbers = [
        ('7', 1, 0), ('8', 1, 1), ('9', 1, 2),
        ('4', 2, 0), ('5', 2, 1), ('6', 2, 2),
        ('1', 3, 0), ('2', 3, 1), ('3', 3, 2),
        ('0', 4, 1), ('.', 4, 2)
    ]

    for (text, row, col) in numbers:
        button = tk.Button(root, text=text, command=lambda t=text: button_click_entry(text_widget, t))
        button.grid(row=row, column=col)

    operators = [
        ('+', 1, 3), ('-', 2, 3), ('*', 3, 3), ('÷', 4, 3),
        ('=', 4, 4), ('C', 4, 0), ('%', 5, 3)
    ]

    for (text, row, col) in operators:
        if text == '=':
            button = tk.Button(root, text=text, command=lambda: button_equal_entry(text_widget))
        elif text == 'C':
            button = tk.Button(root, text=text, command=lambda: button_clear_entry(text_widget))
        elif text == '%':
            button = tk.Button(root, text=text, command=lambda: button_click_entry(text_widget, text))
        else:
            button = tk.Button(root, text=text, command=lambda t=text: button_click_entry(text_widget, t))
        button.grid(row=row, column=col)

    # Separate 'New Calc' button
    new_calc_button = tk.Button(root, text='New Calc', command=create_new_calculator)
    new_calc_button.grid(row=5, column=4)

# Function to handle button clicks for specific text widget
def button_click_entry(text_widget, char):
    global equal_pressed
    if equal_pressed:
        equal_pressed = False
        text_widget.config(state=tk.NORMAL)
        text_widget.delete("1.0", tk.END)
    current = text_widget.get("1.0", tk.END).strip()
    if current == "Error":
        text_widget.delete("1.0", tk.END)
        current = ""
    text_widget.delete("1.0", tk.END)
    text_widget.insert(tk.END, current + str(char))

# Function to handle the equal button for specific text widget
def button_equal_entry(text_widget):
    global equal_pressed
    expression = text_widget.get("1.0", tk.END).strip()
    expression = preprocess_expression(expression)
    try:
        result = eval(expression)
        text_widget.delete("1.0", tk.END)
        text_widget.insert(tk.END, result)
        text_widget.config(state=tk.DISABLED)
        equal_pressed = True
    except Exception as e:  # Catch any exception and print error
        print(e)
        text_widget.delete("1.0", tk.END)
        text_widget.insert(tk.END, "Error")

# Function to clear specific text widget
def button_clear_entry(text_widget):
   text_widget.config(state=tk.NORMAL)
   text_widget.delete("1.0", tk.END)

# Function to handle keyboard input
def handle_keypress(event):
    if event.char.isdigit() or event.char in '+-*/.':
        button_click(event.char)
    elif event.keysym == 'Return':
        button_equal()
    elif event.keysym == 'BackSpace':
        current = text_widget.get("1.0", tk.END).strip()
        text_widget.delete("1.0", tk.END)
        text_widget.insert(tk.END, current[:-1])
    elif event.keysym == 'Delete':
        button_clear()

# Create the main window
window = tk.Tk()
window.title("Calcolatrice")

# Text widget for displaying numbers
text_widget = tk.Text(window, width=30, height=3, font=('Arial', 14))
text_widget.grid(row=0, columnspan=6, padx=10, pady=10)

# Bind keypress events to the main window
window.bind("<Key>", handle_keypress)

# Call function to create buttons
create_buttons(window, text_widget)

# Start the event loop to display the GUI
window.mainloop()
