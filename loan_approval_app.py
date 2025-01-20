import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import pickle
import numpy as np

# Load models
with open('random_forest_model.pkl', 'rb') as file:
    rf_model = pickle.load(file)

with open('svm_model.pkl', 'rb') as file:
    svm_model = pickle.load(file)

with open('logistic_regression_model.pkl', 'rb') as file:
    logreg_model = pickle.load(file)

with open('decision_tree_model.pkl', 'rb') as file:
    dt_model = pickle.load(file)

# Function to predict loan approval
def predict_loan():
    try:
        # Get user input and validate
        input_values = []
        fields = [
            "Income", "Credit Score", "Loan Amount", "Employment Status (1=Employed, 0=Unemployed)",
            "Marital Status (1=Married, 0=Single)", "Age", "Loan Term", "Previous Loan History",
            "Education Level (1=Graduate, 0=Non-Graduate)", "Gender (1=Male, 0=Female)", 
            "Residence Type (1=Urban, 0=Rural)", "Dependents", "Current Debt", "Annual Income Growth Rate"
        ]
        
        for idx, field in enumerate(fields):
            value = input_entries[idx].get()
            if not value:
                messagebox.showerror("Error", f"Please fill in the {field}.")
                return
            input_values.append(float(value) if idx != 4 and idx != 9 else int(value))  # Convert to float for numerical fields
        
        # Convert the input to a numpy array
        user_input = np.array([input_values])
        
        # Choose the selected model
        model_choice = model_var.get()
        if model_choice == "Random Forest":
            model = rf_model
        elif model_choice == "SVM":
            model = svm_model
        elif model_choice == "Logistic Regression":
            model = logreg_model
        elif model_choice == "Decision Tree":
            model = dt_model
        else:
            messagebox.showerror("Error", "Invalid model choice")
            return

        # Show loading message
        status_label.config(text="Predicting... Please wait.")
        
        # Make the prediction
        prediction = model.predict(user_input)
        result = "Approved" if prediction[0] == 1 else "Rejected"
        
        # Update result on the UI
        status_label.config(text=f"Prediction Complete: Loan status - {result}")
        messagebox.showinfo("Prediction Result", f"Loan status: {result}")

    except ValueError:
        messagebox.showerror("Error", "Please enter valid numerical values for all fields.")
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")

# Function to clear input fields
def clear_input():
    for entry in input_entries:
        entry.delete(0, tk.END)
    model_var.set("Random Forest")  # Reset dropdown to default
    status_label.config(text="")

# Create Tkinter window
root = tk.Tk()
root.title("Loan Approval Predictor")
root.geometry("500x550")
root.config(bg="#f0f0f0")

# Add input fields for loan prediction
input_entries = []
fields = [
    "Income", "Credit Score", "Loan Amount", "Employment Status (1=Employed, 0=Unemployed)",
    "Marital Status (1=Married, 0=Single)", "Age", "Loan Term", "Previous Loan History",
    "Education Level (1=Graduate, 0=Non-Graduate)", "Gender (1=Male, 0=Female)", 
    "Residence Type (1=Urban, 0=Rural)", "Dependents", "Current Debt", "Annual Income Growth Rate"
]

# Creating the input fields with labels
for idx, field in enumerate(fields):
    tk.Label(root, text=field, bg="#f0f0f0", anchor='w', width=40).grid(row=idx, column=0, padx=10, pady=5)
    entry = tk.Entry(root, width=30, relief="solid", borderwidth=1)
    entry.grid(row=idx, column=1, padx=10, pady=5)
    input_entries.append(entry)

# Add dropdown for model selection
tk.Label(root, text="Select Model", bg="#f0f0f0", anchor='w', width=40).grid(row=len(fields), column=0, padx=10, pady=5)
model_var = tk.StringVar()
model_dropdown = tk.OptionMenu(root, model_var, "Random Forest", "SVM", "Logistic Regression", "Decision Tree")
model_dropdown.grid(row=len(fields), column=1, padx=10, pady=5)
model_var.set("Random Forest")  # Default value

# Add prediction button
predict_button = tk.Button(root, text="Predict", command=predict_loan, bg="#4CAF50", fg="white", width=20)
predict_button.grid(row=len(fields) + 1, column=0, columnspan=2, pady=10)

# Add clear button
clear_button = tk.Button(root, text="Clear", command=clear_input, bg="#FF6347", fg="white", width=20)
clear_button.grid(row=len(fields) + 2, column=0, columnspan=2, pady=5)

# Add status label
status_label = tk.Label(root, text="", bg="#f0f0f0", fg="blue", width=40)
status_label.grid(row=len(fields) + 3, column=0, columnspan=2, pady=10)

# Start the Tkinter event loop
root.mainloop()
