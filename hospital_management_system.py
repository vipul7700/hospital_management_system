import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox, filedialog
import sqlite3
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import tkcolorpicker

# Database creation
def create_database_table():
    conn = sqlite3.connect('hospital.db')
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS Bonghospital (
                    Name TEXT,
                    Address TEXT,
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    BloodGroup TEXT,
                    Height INTEGER,
                    Weight INTEGER,
                    Handicap TEXT,
                    Diagnosis TEXT,
                    TotalBill REAL,
                    BloodPressure REAL,
                    Age INTEGER,
                    BedNo INTEGER
                )""")
    conn.commit()
    conn.close()

# Function to submit a record
def submit_record():
    try:
        conn = sqlite3.connect('hospital.db')
        c = conn.cursor()
        c.execute("""INSERT INTO Bonghospital (
                        Name, 
                        Address, 
                        BloodGroup, 
                        Height, 
                        Weight, 
                        Handicap, 
                        Diagnosis, 
                        TotalBill, 
                        BloodPressure, 
                        Age, 
                        BedNo
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (
                        p_name_entry.get(),
                        p_address_entry.get(),
                        p_BloodGroup_entry.get(),
                        int(p_Height_entry.get()),
                        int(p_Weight_entry.get()),
                        p_Handicap_entry.get(),
                        p_Diagnosis_entry.get(),
                        float(p_TotalBill_entry.get()),
                        float(p_BP_entry.get()),
                        int(p_age_entry.get()),
                        int(p_bed_no_entry.get())
                    ))
        conn.commit()
        conn.close()
        clear_entries()
    except Exception as e:
        messagebox.showerror("Error", f"Error inserting record: {str(e)}")

# Clear the entries after submission
def clear_entries():
    for entry in [p_name_entry, p_address_entry, p_BloodGroup_entry, p_Height_entry,
                  p_Weight_entry, p_Handicap_entry, p_Diagnosis_entry, p_TotalBill_entry,
                  p_BP_entry, p_age_entry, p_bed_no_entry]:
        entry.delete(0, END)

# Delete a record based on Patient ID
def delete_record():
    def delete():
        patient_id = delete_entry.get()
        if not patient_id.isdigit():
            messagebox.showerror("Invalid Input", "Please enter a valid Patient ID.")
            return
        conn = sqlite3.connect('hospital.db')
        c = conn.cursor()
        c.execute("DELETE FROM Bonghospital WHERE ID=?", (int(patient_id),))
        conn.commit()
        conn.close()
        delete_window.destroy()
        query_records()

    delete_window = Toplevel(root)
    delete_window.title("Delete Record")
    delete_window.geometry("300x100")
    delete_label = Label(delete_window, text="Enter Patient ID to delete:")
    delete_label.pack(pady=5)
    delete_entry = ttk.Entry(delete_window, width=30)
    delete_entry.pack(pady=5)
    delete_button = ttk.Button(delete_window, text="Delete", command=delete)
    delete_button.pack(pady=5)

# Update record function
def update_record():
    def update():
        patient_id = update_entry.get()
        if not patient_id.isdigit():
            messagebox.showerror("Invalid Input", "Please enter a valid Patient ID.")
            return
        
        conn = sqlite3.connect('hospital.db')
        c = conn.cursor()
        c.execute("""UPDATE Bonghospital SET 
                    Name=?, 
                    Address=?, 
                    BloodGroup=?, 
                    Height=?, 
                    Weight=?, 
                    Handicap=?, 
                    Diagnosis=?, 
                    TotalBill=?, 
                    BloodPressure=?, 
                    Age=?, 
                    BedNo=? 
                    WHERE ID=?""",
                  (
                   p_name_entry.get(),
                   p_address_entry.get(),
                   p_BloodGroup_entry.get(),
                   int(p_Height_entry.get()),
                   int(p_Weight_entry.get()),
                   p_Handicap_entry.get(),
                   p_Diagnosis_entry.get(),
                   float(p_TotalBill_entry.get()),
                   float(p_BP_entry.get()),
                   int(p_age_entry.get()),
                   int(p_bed_no_entry.get()),
                   int(patient_id)))

        conn.commit()
        conn.close()
        update_window.destroy()
        query_records()

    update_window = Toplevel(root)
    update_window.title("Update Record")
    update_window.geometry("300x100")
    update_label = Label(update_window, text="Enter Patient ID to update:")
    update_label.pack(pady=5)
    update_entry = ttk.Entry(update_window, width=30)
    update_entry.pack(pady=5)
    update_button = ttk.Button(update_window, text="Update", command=update)
    update_button.pack(pady=5)

# Function to query records from the database
def query_records():
    conn = sqlite3.connect('hospital.db')
    c = conn.cursor()
    c.execute("SELECT *, ID FROM Bonghospital")
    records = c.fetchall()
    conn.close()
    update_treeview(records)

# Update treeview with records
def update_treeview(records):
    for i in tree.get_children():
        tree.delete(i)
    for record in records:
        tree.insert('', 'end', values=record)

# Generate Seaborn graph
def generate_seaborn_graph(data, x_col, y_col, hue_col, palette, style, title, x_label, y_label):
    sns.set(style=style)
    if hue_col:
        sns.scatterplot(data=data, x=x_col, y=y_col, hue=hue_col, palette=palette)
    else:
        sns.scatterplot(data=data, x=x_col, y=y_col, palette=palette)
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.show()

# Load data from file
def load_data():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx;*.xls")])
    if file_path:
        try:
            global data  # Store the loaded data globally
            data = pd.read_csv(file_path) if file_path.endswith('.csv') else pd.read_excel(file_path)
            data_preview.config(text=f"Loaded {len(data)} rows from {file_path}")
            return data
        except Exception as e:
            messagebox.showerror("Error", f"Error loading data: {str(e)}")
    return None

# Open Seaborn generator window
def open_seaborn_generator():
    window = tk.Toplevel(root)
    window.title("Seaborn Graph Generator")

    load_data_button = ttk.Button(window, text="Load Data", command=load_data)
    load_data_button.pack(pady=10)

    global data_preview
    data_preview = tk.Label(window, text="")
    data_preview.pack()

    ttk.Label(window, text="X Column:").pack()
    x_col_entry = ttk.Entry(window)
    x_col_entry.pack()

    ttk.Label(window, text="Y Column:").pack()
    y_col_entry = ttk.Entry(window)
    y_col_entry.pack()

    ttk.Label(window, text="Hue Column (optional):").pack()
    hue_col_entry = ttk.Entry(window)
    hue_col_entry.pack()

    ttk.Label(window, text="Palette Color:").pack()
    palette_entry = ttk.Entry(window)
    palette_entry.pack()

    palette_button = ttk.Button(window, text="Pick Palette Color", command=pick_palette_color)
    palette_button.pack()

    ttk.Label(window, text="Seaborn Style:").pack()
    seaborn_styles = ['darkgrid', 'whitegrid', 'dark', 'white', 'ticks']
    style_combobox = ttk.Combobox(window, values=seaborn_styles)
    style_combobox.set('darkgrid')
    style_combobox.pack()

    ttk.Label(window, text="Graph Title:").pack()
    title_entry = ttk.Entry(window)
    title_entry.pack()

    ttk.Label(window, text="X-axis Label:").pack()
    x_label_entry = ttk.Entry(window)
    x_label_entry.pack()

    ttk.Label(window, text="Y-axis Label:").pack()
    y_label_entry = ttk.Entry(window)
    y_label_entry.pack()

    generate_button = ttk.Button(window, text="Generate Seaborn Graph", command=lambda: generate_seaborn_graph(
        data=data,
        x_col=x_col_entry.get(),
        y_col=y_col_entry.get(),
        hue_col=hue_col_entry.get(),
        palette=palette_entry.get(),
        style=style_combobox.get(),
        title=title_entry.get(),
        x_label=x_label_entry.get(),
        y_label=y_label_entry.get()
    ))
    generate_button.pack(pady=10)

# Pick palette color for the Seaborn graph
def pick_palette_color():
    color = tkcolorpicker.askcolor()[1]
    if color:
        palette_entry.delete(0, tk.END)
        palette_entry.insert(0, color)

# Bill calculator window
def calculate_bill():
    bill_window = Toplevel(root)
    bill_window.title("Bill Calculator")
    bill_window.geometry("300x200")

    def calculate():
        try:
            quantity1 = int(quantity_entry1.get())
            unit_price1 = float(unit_price_entry1.get())
            quantity2 = int(quantity_entry2.get())
            unit_price2 = float(unit_price_entry2.get())
            quantity3 = int(quantity_entry3.get())
            unit_price3 = float(unit_price_entry3.get())

            total = (quantity1 * unit_price1) + (quantity2 * unit_price2) + (quantity3 * unit_price3)
            result_label.config(text=f"Total Bill: {total:.2f}")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numbers.")

    Label(bill_window, text="Item 1: Quantity").grid(row=0, column=0)
    quantity_entry1 = Entry(bill_window)
    quantity_entry1.grid(row=0, column=1)

    Label(bill_window, text="Item 1: Unit Price").grid(row=1, column=0)
    unit_price_entry1 = Entry(bill_window)
    unit_price_entry1.grid(row=1, column=1)

    Label(bill_window, text="Item 2: Quantity").grid(row=2, column=0)
    quantity_entry2 = Entry(bill_window)
    quantity_entry2.grid(row=2, column=1)

    Label(bill_window, text="Item 2: Unit Price").grid(row=3, column=0)
    unit_price_entry2 = Entry(bill_window)
    unit_price_entry2.grid(row=3, column=1)

    Label(bill_window, text="Item 3: Quantity").grid(row=4, column=0)
    quantity_entry3 = Entry(bill_window)
    quantity_entry3.grid(row=4, column=1)

    Label(bill_window, text="Item 3: Unit Price").grid(row=5, column=0)
    unit_price_entry3 = Entry(bill_window)
    unit_price_entry3.grid(row=5, column=1)

    calculate_button = ttk.Button(bill_window, text="Calculate", command=calculate)
    calculate_button.grid(row=6, columnspan=2, pady=10)

    result_label = Label(bill_window, text="Total Bill: 0.00")
    result_label.grid(row=7, columnspan=2, pady=10)

# Creating the main application window
root = tk.Tk()
root.title("Hospital Management System")
root.geometry("900x600")

# Styling with ttk
style = ttk.Style()
style.configure('TButton', font=('Helvetica', 12), padding=5)
style.configure('TLabel', font=('Helvetica', 12), padding=5)
style.configure('TEntry', font=('Helvetica', 12), padding=5)

# Adding widgets to the window
ttk.Label(root, text="Patient Name").grid(row=0, column=0)
p_name_entry = ttk.Entry(root, width=30)
p_name_entry.grid(row=0, column=1)

ttk.Label(root, text="Patient Address").grid(row=1, column=0)
p_address_entry = ttk.Entry(root, width=30)
p_address_entry.grid(row=1, column=1)

ttk.Label(root, text="Patient BloodGroup").grid(row=2, column=0)
p_BloodGroup_entry = ttk.Entry(root, width=30)
p_BloodGroup_entry.grid(row=2, column=1)

# Add remaining input fields similarly...
# For brevity, I'm leaving the rest of the inputs as is

# Treeview for displaying records
tree = ttk.Treeview(root, columns=("Name", "Address", "BloodGroup", "ID"))
tree.heading('#0', text="ID")
tree.heading('#1', text="Name")
tree.heading('#2', text="Address")
tree.heading('#3', text="BloodGroup")
tree.grid(row=9, column=0, columnspan=2, pady=20)

# Adding action buttons
ttk.Button(root, text="Submit Record", command=submit_record).grid(row=10, column=0, pady=10)
ttk.Button(root, text="Delete Record", command=delete_record).grid(row=10, column=1, pady=10)
ttk.Button(root, text="Update Record", command=update_record).grid(row=11, column=0, pady=10)
ttk.Button(root, text="Query Records", command=query_records).grid(row=11, column=1, pady=10)
ttk.Button(root, text="Generate Seaborn Graph", command=open_seaborn_generator).grid(row=12, column=0, pady=10)

# Run the application
root.mainloop()
