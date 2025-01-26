import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from job_tracker_database import view_applications, add_application, update_application, delete_application, export_to_csv, import_from_csv

def load_applications(table):
    table.delete(*table.get_children())
    rows = view_applications()
    for row in rows:
        table.insert('', 'end', values=row)

def open_add_form(table):
    def save_application():
        job_title = job_title_entry.get()
        company = company_entry.get()
        application_date = date_entry.get()
        status = status_var.get()
        notes = notes_entry.get()

        if not job_title or not company or not application_date or not status:
            messagebox.showerror("Error", "All fields except notes are required!")
            return

        add_application(job_title, company, application_date, status, notes)
        load_applications(table)
        add_window.destroy()

    add_window = tk.Toplevel()
    add_window.title("Add Job Application")

    tk.Label(add_window, text="Job Title").grid(row=0, column=0)
    job_title_entry = tk.Entry(add_window)
    job_title_entry.grid(row=0, column=1)

    tk.Label(add_window, text="Company").grid(row=1, column=0)
    company_entry = tk.Entry(add_window)
    company_entry.grid(row=1, column=1)

    tk.Label(add_window, text="Application Date (YYYY-MM-DD)").grid(row=2, column=0)
    date_entry = tk.Entry(add_window)
    date_entry.grid(row=2, column=1)

    tk.Label(add_window, text="Status").grid(row=3, column=0)
    status_var = tk.StringVar(value="Applied")
    status_dropdown = ttk.Combobox(add_window, textvariable=status_var, state="readonly")
    status_dropdown['values'] = ("Applied", "Call Back", "Rejected", "Interview", "Interviewed")
    status_dropdown.grid(row=3, column=1)

    tk.Label(add_window, text="Notes").grid(row=4, column=0)
    notes_entry = tk.Entry(add_window)
    notes_entry.grid(row=4, column=1)

    tk.Button(add_window, text="Save", command=save_application).grid(row=5, column=0, columnspan=2)

def open_edit_form(selected_item, table):
    def save_changes():
        job_title = job_title_entry.get()
        company = company_entry.get()
        application_date = date_entry.get()
        status = status_var.get()
        notes = notes_entry.get()

        if not job_title or not company or not application_date or not status:
            messagebox.showerror("Error", "All fields except notes are required!")
            return

        update_application(app_id, job_title, company, application_date, status, notes)
        load_applications(table)
        edit_window.destroy()

    app_id = selected_item['values'][0]
    job_title, company, application_date, status, notes = selected_item['values'][1:]

    edit_window = tk.Toplevel()
    edit_window.title("Edit Job Application")

    tk.Label(edit_window, text="Job Title").grid(row=0, column=0)
    job_title_entry = tk.Entry(edit_window)
    job_title_entry.insert(0, job_title)
    job_title_entry.grid(row=0, column=1)

    tk.Label(edit_window, text="Company").grid(row=1, column=0)
    company_entry = tk.Entry(edit_window)
    company_entry.insert(0, company)
    company_entry.grid(row=1, column=1)

    tk.Label(edit_window, text="Application Date (YYYY-MM-DD)").grid(row=2, column=0)
    date_entry = tk.Entry(edit_window)
    date_entry.insert(0, application_date)
    date_entry.grid(row=2, column=1)

    tk.Label(edit_window, text="Status").grid(row=3, column=0)
    status_var = tk.StringVar(value=status)
    status_dropdown = ttk.Combobox(edit_window, textvariable=status_var, state="readonly")
    status_dropdown['values'] = ("Applied", "Call Back", "Rejected", "Interview", "Interviewed")
    status_dropdown.grid(row=3, column=1)

    tk.Label(edit_window, text="Notes").grid(row=4, column=0)
    notes_entry = tk.Entry(edit_window)
    notes_entry.insert(0, notes)
    notes_entry.grid(row=4, column=1)

    tk.Button(edit_window, text="Save Changes", command=save_changes).grid(row=5, column=0, columnspan=2)

def delete_selected(table):
    try:
        selected_item = table.selection()[0]
        app_id = table.item(selected_item)['values'][0]
        delete_application(app_id)
        load_applications(table)
    except IndexError:
        messagebox.showerror("Error", "Please select an application to delete.")

def export_data():
    filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
    if filename:
        export_to_csv(filename)

def import_data(table):
    filename = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if filename:
        import_from_csv(filename)
        load_applications(table)

def start_gui():
    root = tk.Tk()
    root.title("Job Application Tracker")

    table = ttk.Treeview(root, columns=("ID", "Job Title", "Company", "Date", "Status", "Notes"), show='headings')
    table.pack(fill=tk.BOTH, expand=True)

    for col in ("ID", "Job Title", "Company", "Date", "Status", "Notes"):
        table.heading(col, text=col)
        table.column(col, width=100)

    vsb = ttk.Scrollbar(root, orient="vertical", command=table.yview)
    vsb.pack(side="right", fill="y")
    table.configure(yscrollcommand=vsb.set)

    hsb = ttk.Scrollbar(root, orient="horizontal", command=table.xview)
    hsb.pack(side="bottom", fill="x")
    table.configure(xscrollcommand=hsb.set)

    load_applications(table)

    tk.Button(root, text="Add Application", command=lambda: open_add_form(table)).pack(pady=5)
    tk.Button(root, text="Edit Selected", command=lambda: open_edit_form(table.item(table.selection()[0]), table)).pack(pady=5)
    tk.Button(root, text="Delete Selected", command=lambda: delete_selected(table)).pack(pady=5)
    tk.Button(root, text="Export to CSV", command=export_data).pack(pady=5)
    tk.Button(root, text="Import from CSV", command=lambda: import_data(table)).pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    start_gui()
