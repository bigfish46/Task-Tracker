import tkinter as tk
from tkinter import ttk, messagebox
from task_tracker_oop import Task, TaskManager
from datetime import datetime, date
import os

class TaskTrackerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Tracker")
        
        # Set color scheme - Windows 11 inspired
        self.bg_color = "#202020"           # Darker background
        self.fg_color = "#E0E0E0"           # Light grey text
        self.accent_color = "#303030"       # Slightly lighter than background
        self.button_bg = "#0078D4"          # Windows blue
        self.button_fg = "#000000"          # Black text for buttons
        self.hover_color = "#1082D9"        # Lighter blue for hover
        self.entry_bg = "#2D2D2D"           # Slightly lighter than background for inputs
        self.selection_color = "#0078D4"    # Windows blue for selections
        self.header_bg = "#D0D0D0"          # Light grey background for headers
        self.header_fg = "#000000"          # Black text for headers
        
        # Configure root window colors
        self.root.configure(bg=self.bg_color)
        
        # Configure ttk styles
        self.style = ttk.Style()
        
        # General styling
        self.style.configure(".", 
                           background=self.bg_color, 
                           foreground=self.fg_color, 
                           font=('Segoe UI', 9))
        
        # Frame styling
        self.style.configure("TFrame", background=self.bg_color)
        
        # Label styling
        self.style.configure("TLabel", 
                           background=self.bg_color, 
                           foreground=self.fg_color,
                           font=('Segoe UI', 9))
        
        # LabelFrame styling
        self.style.configure("TLabelframe", 
                           background=self.bg_color, 
                           foreground=self.fg_color)
        self.style.configure("TLabelframe.Label", 
                           background=self.bg_color, 
                           foreground=self.fg_color,
                           font=('Segoe UI', 10, 'bold'))
        
        # Treeview styling
        self.style.configure("Treeview", 
                           background=self.entry_bg,
                           foreground=self.fg_color, 
                           fieldbackground=self.entry_bg,
                           font=('Segoe UI', 9),
                           rowheight=25)  # Increased row height
        
        self.style.configure("Treeview.Heading", 
                           background=self.header_bg,
                           foreground=self.header_fg,
                           font=('Segoe UI', 9, 'bold'))
        
        # Map colors for Treeview selection
        self.style.map("Treeview",
                      background=[('selected', self.selection_color)],
                      foreground=[('selected', 'white')])
        
        self.style.map("Treeview.Heading",
                      background=[('active', '#E0E0E0')],  # Lighter grey on hover
                      foreground=[('active', 'black')])    # Keep text black on hover
        
        # Button styling - modern flat look with black text
        self.style.configure("TButton", 
                           background=self.button_bg,
                           foreground=self.button_fg,
                           font=('Segoe UI', 9, 'bold'),
                           padding=(15, 8))  # Wider padding
        
        # Map colors for button states - keeping text black for all states
        self.style.map("TButton",
                      background=[('active', self.hover_color),
                                ('pressed', self.button_bg)],
                      foreground=[('active', 'black'),
                                ('pressed', 'black')])
        
        # Entry styling
        self.style.configure("TEntry", 
                           fieldbackground=self.entry_bg,
                           foreground='black',  # Ensure text is black
                           padding=8)  # Added padding
        
        # Configure root grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Create main frame with padding
        self.main_frame = ttk.Frame(root, padding="20")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure main frame grid
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(1, weight=1)
        
        # Initialize task manager
        self.manager = TaskManager("tasks.json")
        
        # Create and pack widgets
        self.create_input_frame()
        self.create_task_list()
        self.create_buttons()
        
        # Load tasks
        self.refresh_task_list()

    def create_input_frame(self):
        # Input frame with more padding
        input_frame = ttk.LabelFrame(self.main_frame, text="Add New Task", padding="15")
        input_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        # Configure input frame grid
        input_frame.columnconfigure(1, weight=3)
        input_frame.columnconfigure(3, weight=1)
        
        # Task name input with padding
        ttk.Label(input_frame, text="Task:").grid(row=0, column=0, padx=10, pady=5)
        self.task_name = ttk.Entry(input_frame)
        self.task_name.grid(row=0, column=1, padx=10, pady=5, sticky=(tk.W, tk.E))
        
        # Due date input
        ttk.Label(input_frame, text="Due Date (YYYY-MM-DD):").grid(row=0, column=2, padx=10, pady=5)
        self.due_date = ttk.Entry(input_frame)
        self.due_date.grid(row=0, column=3, padx=10, pady=5, sticky=(tk.W, tk.E))
        
        # Add button
        ttk.Button(input_frame, text="Add Task", command=self.add_task).grid(row=0, column=4, padx=10, pady=5)

    def create_task_list(self):
        # Create treeview for tasks with adjusted column widths
        columns = ("Status", "Task", "Due Date", "Days Left")
        self.tree = ttk.Treeview(self.main_frame, columns=columns, show="headings")
        
        # Set column headings and proportions
        self.tree.heading("Status", text="Status")
        self.tree.heading("Task", text="Task")
        self.tree.heading("Due Date", text="Due Date")
        self.tree.heading("Days Left", text="Days Left")
        
        # Adjust column widths
        self.tree.column("Status", width=80, minwidth=80)
        self.tree.column("Task", width=300, minwidth=200)
        self.tree.column("Due Date", width=120, minwidth=120)
        self.tree.column("Days Left", width=100, minwidth=100)
        
        # Add scrollbar with matching style
        scrollbar = ttk.Scrollbar(self.main_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Grid the treeview and scrollbar with padding
        self.tree.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        scrollbar.grid(row=1, column=1, sticky=(tk.N, tk.S), pady=10)

    def create_buttons(self):
        # Button frame with padding
        button_frame = ttk.Frame(self.main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10, sticky=(tk.W, tk.E))
        
        # Center the buttons
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(4, weight=1)  # Changed back to 4
        
        # Buttons with consistent spacing
        ttk.Button(button_frame, text="Mark Complete", command=self.mark_complete).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Remove Task", command=self.remove_task).grid(row=0, column=2, padx=5)
        ttk.Button(button_frame, text="Refresh", command=self.refresh_task_list).grid(row=0, column=3, padx=5)

    def add_task(self):
        name = self.task_name.get().strip()
        due_date = self.due_date.get().strip()
        
        if not name or not due_date:
            messagebox.showerror("Error", "Please enter both task name and due date")
            return
            
        try:
            # Validate date format
            if not Task.is_valid_date_format(due_date):
                messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD")
                return
                
            # Add task
            self.manager.add_task(name, due_date)
            
            # Clear inputs
            self.task_name.delete(0, tk.END)
            self.due_date.delete(0, tk.END)
            
            # Refresh display immediately
            self.refresh_task_list()
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def mark_complete(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showinfo("Info", "Please select a task to mark complete")
            return
            
        item_id = selection[0]
        task_idx = self.tree.index(item_id)
        
        if self.manager.mark_complete(task_idx):
            self.refresh_task_list()

    def remove_task(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showinfo("Info", "Please select a task to remove")
            return
            
        if messagebox.askyesno("Confirm", "Are you sure you want to remove this task?"):
            item_id = selection[0]
            task_idx = self.tree.index(item_id)
            
            removed_task = self.manager.remove_task(task_idx)
            if removed_task:
                # Refresh display immediately
                self.refresh_task_list()

    def refresh_task_list(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Add sorted tasks
        for task in self.manager.sort_tasks():
            days_left = (task.due - date.today()).days
            status = "✓" if task.done else " "
            
            if task.done:
                days_left_text = "Completed"
            elif days_left < 0:
                days_left_text = "Overdue!"
            else:
                days_left_text = f"{days_left} days"
                
            self.tree.insert("", tk.END, values=(
                status,
                task.name,
                task.due.strftime("%Y-%m-%d"),
                days_left_text
            ))

def main():
    root = tk.Tk()
    app = TaskTrackerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 