"""Run this file on your computer to open the Heart Health Insights window."""
import tkinter as tk
from tkinter import messagebox
from pathlib import Path
import pandas as pd


def show_results():
    # Read the text entered by the user and check that the age is valid.
    age_text = age_entry.get().strip()
    if not age_text.isdigit():
        messagebox.showerror("Invalid age", "Please enter your age as a whole number.")
        return

    age = int(age_text)
    if age < 29 or age > 80:
        messagebox.showerror("Age outside dataset", "Please enter an age from 29 to 80, the range in our dataset.")
        return

    # Use the same age groups as the project analysis.
    if age < 40:
        minimum, maximum = 29, 39
    elif age < 55:
        minimum, maximum = 40, 54
    elif age < 65:
        minimum, maximum = 55, 64
    else:
        minimum, maximum = 65, 80

    smoking = smoking_choice.get()
    activity = activity_choice.get()
    peers = data[(data["age"] >= minimum) & (data["age"] <= maximum)]

    # The mean of a 0/1 column is the proportion with heart disease.
    report = f"Age group: {minimum}-{maximum}\n"
    report += f"Your selections: {smoking}; {activity}\n\n"
    report += "SMOKING STATUS\n"
    for category in ["Never", "Former", "Current"]:
        group = peers[peers["smoking_status"] == category]
        if len(group) > 0:
            rate = group["heart_disease"].mean() * 100
            marker = "  <-- selected" if category == smoking else ""
            report += f"{category}: {rate:.1f}% ({len(group):,} records){marker}\n"
        else:
            report += f"{category}: no records\n"

    report += "\nPHYSICAL ACTIVITY\n"
    for category in ["Sedentary", "Light", "Active", "Very Active"]:
        group = peers[peers["physical_activity"] == category]
        if len(group) > 0:
            rate = group["heart_disease"].mean() * 100
            marker = "  <-- selected" if category == activity else ""
            report += f"{category}: {rate:.1f}% ({len(group):,} records){marker}\n"
        else:
            report += f"{category}: no records\n"

    report += "\nEach table compares one factor within your age group.\n"
    report += "These are separate comparisons, not a matched personal profile.\n\n"
    report += "This project treats the data as synthetic teaching data.\n"
    report += "Percentages describe this dataset, not your personal risk.\n"
    report += "Other factors may explain differences between categories.\n"
    report += "For personal prevention advice, consult a healthcare professional."
    results_box.config(state="normal")
    results_box.delete("1.0", tk.END)
    results_box.insert(tk.END, report)
    results_box.config(state="disabled")


def reset_form():
    age_entry.delete(0, tk.END)
    smoking_choice.set("Never")
    activity_choice.set("Sedentary")
    results_box.config(state="normal")
    results_box.delete("1.0", tk.END)
    results_box.insert(
        tk.END,
        "Your dataset comparisons will appear here."
    )
    results_box.config(state="disabled")

if __name__ == "__main__":
    # Keep the CSV beside this Python file.
    if "__file__" in globals():
        csv_path = Path(__file__).with_name("heart_disease_prediction_2026.csv")
    else:
        csv_path = Path("heart_disease_prediction_2026.csv")

    # Create the main window, following the class example.
    window = tk.Tk()
    window.title("Heart Health Insights App")
    window.geometry("850x780")
    window.configure(bg="lightblue")

    try:
        data = pd.read_csv(csv_path)
    except (OSError, pd.errors.ParserError) as error:
        messagebox.showerror("Dataset could not be loaded", str(error))
        window.destroy()
    else:
        tk.Label(window, text="Heart Health Insights App", font=("Arial", 20, "bold"), bg="lightblue").pack(pady=12)
        tk.Label(window, text="Explore smoking and activity categories in the dataset.", bg="lightblue").pack()

        tk.Label(window, text="Enter your age (29-80)", bg="lightblue").pack(pady=(12, 2))
        age_entry = tk.Entry(window, width=20)
        age_entry.pack()

        tk.Label(window, text="Smoking status", bg="lightblue").pack(pady=(8, 2))
        smoking_choice = tk.StringVar(value="Never")
        tk.OptionMenu(window, smoking_choice, "Never", "Former", "Current").pack()

        tk.Label(window, text="Physical activity", bg="lightblue").pack(pady=(8, 2))
        activity_choice = tk.StringVar(value="Sedentary")
        tk.OptionMenu(window, activity_choice, "Sedentary", "Light", "Active", "Very Active").pack()

        buttons = tk.Frame(window, bg="lightblue")
        buttons.pack(pady=12)
        tk.Button(buttons, text="Show insights", command=show_results).pack(side=tk.LEFT, padx=5)
        tk.Button(buttons, text="Reset", command=reset_form).pack(side=tk.LEFT, padx=5)

       
        # Create a scrollable results area
        results_frame = tk.Frame(window)
        results_frame.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0, 15)
        )

        scrollbar = tk.Scrollbar(results_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        results_box = tk.Text(
            results_frame,
            wrap="word",
            font=("Arial", 12),
            padx=12,
            pady=12,
            yscrollcommand=scrollbar.set
        )

        results_box.pack(side=tk.LEFT, fill="both", expand=True)

        scrollbar.config(command=results_box.yview)

        results_box.insert(
            tk.END,
            "Your dataset comparisons will appear here."
        )

        results_box.config(state="disabled")

        window.mainloop()




import tkinter as tk
from tkinter import messagebox
import pandas as pd


# 1. Load the dataset
# Keep the CSV in the same folder as this notebook.
data = pd.read_csv("heart_disease_prediction_2026.csv")


# 2. Create the function for the Show Insights button
def show_results():

    # Check the age entered by the user
    age_text = age_entry.get().strip()

    if not age_text.isdigit():
        messagebox.showerror(
            "Invalid age",
            "Please enter your age as a whole number."
        )
        return

    age = int(age_text)

    if age < 29 or age > 80:
        messagebox.showerror(
            "Age outside dataset",
            "Please enter an age between 29 and 80."
        )
        return

    # Select the age group
    if age < 40:
        minimum = 29
        maximum = 39
    elif age < 55:
        minimum = 40
        maximum = 54
    elif age < 65:
        minimum = 55
        maximum = 64
    else:
        minimum = 65
        maximum = 80

    # Read the selected categories
    smoking = smoking_choice.get()
    activity = activity_choice.get()

    # Keep records within the selected age group
    age_data = data[
        (data["age"] >= minimum) &
        (data["age"] <= maximum)
    ]

    # Start the results message
    report = "HEART HEALTH INSIGHTS\n\n"
    report += f"Age group: {minimum}–{maximum}\n"
    report += f"Smoking status: {smoking}\n"
    report += f"Physical activity: {activity}\n\n"

    report += "Percentages show records with heart disease.\n"
    report += "Each comparison uses the selected age group.\n\n"

    # Compare smoking categories
    report += "SMOKING STATUS\n"

    for category in ["Never", "Former", "Current"]:

        group = age_data[
            age_data["smoking_status"] == category
        ]

        if len(group) > 0:
            # The mean of a 0/1 column gives the proportion.
            rate = group["heart_disease"].mean() * 100

            report += (
                f"{category}: {rate:.1f}% "
                f"({len(group):,} records)"
            )

            if category == smoking:
                report += "  ← Your selection"

            report += "\n"

        else:
            report += f"{category}: no records\n"

    # Compare physical activity categories
    report += "\nPHYSICAL ACTIVITY\n"

    for category in [
        "Sedentary", "Light", "Active", "Very Active"
    ]:

        group = age_data[
            age_data["physical_activity"] == category
        ]

        if len(group) > 0:
            rate = group["heart_disease"].mean() * 100

            report += (
                f"{category}: {rate:.1f}% "
                f"({len(group):,} records)"
            )

            if category == activity:
                report += "  ← Your selection"

            report += "\n"

        else:
            report += f"{category}: no records\n"

    # Explain how to interpret the results
    report += "\nHOW TO READ THESE RESULTS\n"
    report += "Smoking and activity are compared separately.\n"
    report += "The groups are not an exact match for you.\n"
    report += "Other factors may explain the differences.\n\n"

    report += "This project treats the dataset as synthetic.\n"
    report += "These percentages are not your personal risk "
    report += "or a medical diagnosis.\n"
    report += "For personal prevention advice, speak with "
    report += "a healthcare professional."

    # Display the report in the results area
    results_box.config(state="normal")
    results_box.delete("1.0", tk.END)
    results_box.insert(tk.END, report)
    results_box.config(state="disabled")


# 3. Create the function for the Reset button
def reset_form():

    age_entry.delete(0, tk.END)
    smoking_choice.set("Never")
    activity_choice.set("Sedentary")

    results_box.config(state="normal")
    results_box.delete("1.0", tk.END)
    results_box.insert(
        tk.END,
        "Your dataset comparisons will appear here."
    )
    results_box.config(state="disabled")

    age_entry.focus_set()


# 4. Create the main window
window = tk.Tk()
window.title("Heart Health Insights App")
window.geometry("800x800")
window.configure(bg="lightblue")


# 5. Add the title and introduction
title_label = tk.Label(
    window,
    text="Heart Health Insights App",
    font=("Arial", 22, "bold"),
    bg="lightblue"
)
title_label.pack(pady=12)

intro_label = tk.Label(
    window,
    text="Explore smoking and physical activity in our dataset.",
    font=("Arial", 12),
    bg="lightblue"
)
intro_label.pack(pady=5)


# 6. Add the age input
age_label = tk.Label(
    window,
    text="Enter your age (29–80):",
    bg="lightblue"
)
age_label.pack(pady=(10, 3))

age_entry = tk.Entry(window, width=20)
age_entry.pack()


# 7. Add the smoking menu
smoking_label = tk.Label(
    window,
    text="Smoking status:",
    bg="lightblue"
)
smoking_label.pack(pady=(10, 3))

smoking_choice = tk.StringVar(window)
smoking_choice.set("Never")

smoking_menu = tk.OptionMenu(
    window,
    smoking_choice,
    "Never",
    "Former",
    "Current"
)
smoking_menu.pack()


# 8. Add the physical activity menu
activity_label = tk.Label(
    window,
    text="Physical activity:",
    bg="lightblue"
)
activity_label.pack(pady=(10, 3))

activity_choice = tk.StringVar(window)
activity_choice.set("Sedentary")

activity_menu = tk.OptionMenu(
    window,
    activity_choice,
    "Sedentary",
    "Light",
    "Active",
    "Very Active"
)
activity_menu.pack()


# 9. Add the buttons
button_frame = tk.Frame(window, bg="lightblue")
button_frame.pack(pady=12)

show_button = tk.Button(
    button_frame,
    text="Show Insights",
    command=show_results
)
show_button.pack(side=tk.LEFT, padx=5)

reset_button = tk.Button(
    button_frame,
    text="Reset",
    command=reset_form
)
reset_button.pack(side=tk.LEFT, padx=5)


# 10. Add a scrollable results area
results_frame = tk.Frame(window)
results_frame.pack(
    fill=tk.BOTH,
    expand=True,
    padx=15,
    pady=(0, 15)
)

scrollbar = tk.Scrollbar(results_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

results_box = tk.Text(
    results_frame,
    wrap="word",
    font=("Arial", 12),
    padx=12,
    pady=12,
    yscrollcommand=scrollbar.set
)
results_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar.config(command=results_box.yview)

results_box.insert(
    tk.END,
    "Your dataset comparisons will appear here."
)
results_box.config(state="disabled")


# 11. Keep the window open
window.mainloop()