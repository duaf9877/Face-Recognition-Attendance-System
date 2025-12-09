import tkinter as tk
from tkinter import ttk
from database_handler import get_all_attendance

# --- UI SETUP ---
class AttendanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Attendance Log Viewer")
        self.root.geometry("650x400") # Set initial window size

        # --- Style Configuration ---
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Calibri", 12, "bold"))
        style.configure("Treeview", font=("Calibri", 11), rowheight=25)

        # --- Main Frame ---
        main_frame = ttk.Frame(root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- Title Label ---
        title_label = ttk.Label(main_frame, text="Student Attendance Records", font=("Calibri", 16, "bold"))
        title_label.pack(pady=5)
        
        # --- Treeview (for the table) ---
        # Define the columns for the table
        columns = ("name", "date", "time", "status")
        self.tree = ttk.Treeview(main_frame, columns=columns, show="headings", style="Treeview")

        # Define the headings
        self.tree.heading("name", text="Student Name")
        self.tree.heading("date", text="Date")
        self.tree.heading("time", text="Time")
        self.tree.heading("status", text="Status")
        
        # Adjust column widths
        self.tree.column("name", width=200)
        self.tree.column("date", width=100)
        self.tree.column("time", width=100)
        self.tree.column("status", width=80)

        self.tree.pack(pady=10, fill=tk.BOTH, expand=True)

        # --- Buttons ---
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=10)

        refresh_button = ttk.Button(button_frame, text="Refresh Data", command=self.populate_table)
        refresh_button.pack(side=tk.LEFT, padx=10)

        quit_button = ttk.Button(button_frame, text="Quit", command=root.destroy)
        quit_button.pack(side=tk.LEFT, padx=10)
        
        # --- Load initial data ---
        self.populate_table()

    def populate_table(self):
        """Fetches data from the database and populates the table."""
        # Clear existing data from the table first
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        # Fetch new data
        records = get_all_attendance()
        
        # Insert new data into the table
        for record in records:
            self.tree.insert("", tk.END, values=record)

# --- Run the Application ---
if __name__ == "__main__":
    app_root = tk.Tk()
    app = AttendanceApp(app_root)
    app_root.mainloop()
