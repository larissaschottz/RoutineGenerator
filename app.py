import tkinter as tk
from tkinter import ttk
import pandas as pd
import random

class RoutineGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Routine Generator")

        self.activities = []
        self.include_weekend = tk.BooleanVar()

        self.create_interface()

    def create_interface(self):
        # Frame for settings
        config_frame = ttk.Frame(self.root, padding="10")
        config_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        ttk.Checkbutton(config_frame, text="Include weekend", variable=self.include_weekend).grid(row=0, column=0, padx=5, pady=5)

        # Frame for entering activities
        activities_frame = ttk.Frame(self.root, padding="10")
        activities_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        ttk.Label(activities_frame, text="Activity:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_activity = ttk.Entry(activities_frame, width=30)
        self.entry_activity.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(activities_frame, text="Hours per week:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_hours = ttk.Entry(activities_frame, width=10)
        self.entry_hours.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(activities_frame, text="Add Activity", command=self.add_activity).grid(row=2, column=0, columnspan=2, pady=10)

        # Button to generate routine
        ttk.Button(activities_frame, text="Generate Routine", command=self.display_routine).grid(row=3, column=0, columnspan=2, pady=10)

        # Frame for displaying routine
        self.frame_routine = ttk.Frame(self.root, padding="10")
        self.frame_routine.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        # Adjust row and column weights for resizable interface
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

    def add_activity(self):
        activity = self.entry_activity.get()
        hours = self.entry_hours.get()

        if activity and hours:
            self.activities.append({"Activity": activity, "Hours per week": int(hours)})

            self.entry_activity.delete(0, tk.END)
            self.entry_hours.delete(0, tk.END)

    def display_routine(self):
        if not self.activities:
            tk.messagebox.showwarning("Warning", "Add at least one activity.")
            return

        # Create a DataFrame with activities
        df = pd.DataFrame(self.activities)

        # Add a column for weekdays
        weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        if self.include_weekend.get():
            weekdays.extend(["Saturday", "Sunday"])

        for day in weekdays:
            df[day] = 0

        # Distribute hours randomly across weekdays
        for _, activity in df.iterrows():
            remaining_hours = activity["Hours per week"]
            while remaining_hours > 0:
                random_day = random.choice(weekdays)
                hours_day = min(random.randint(1, 4), remaining_hours)  # Limit to 4 hours per day
                df.at[_, random_day] += hours_day
                remaining_hours -= hours_day

        # Display the routine on the screen
        routine_text = df.to_string(index=False)
        routine_label = ttk.Label(self.frame_routine, text=routine_text, justify="left", font=("Courier", 10))
        routine_label.grid(row=0, column=0, padx=5, pady=5)

if __name__ == "__main__":
    root = tk.Tk()
    app = RoutineGeneratorApp(root)
    root.mainloop()
