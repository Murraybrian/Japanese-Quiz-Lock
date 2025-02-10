import tkinter as tk
from tkinter import messagebox
from tkinter import ttk  # ttk for modern widgets
import random
import json
import os


class JapaneseLanguageProgram:
    DATA_FILE = "japanese_data.json"

    def __init__(self, root):
        """Initialize the application."""
        self.root = root
        self.root.title("Japanese Quiz Lock")
        self.data = self.load_data()

        # Checks theme load
        try:
            self.root.tk.call("source", "forest-dark.tcl")
            self.style = ttk.Style()
            self.style.theme_use("forest-dark")
        except tk.TclError:
            messagebox.showerror("Theme Error", "Could not load 'forest-dark.tcl'. Ensure the file exists.")

        self.root.geometry("600x500")
        self.setup_main_page()

    def load_data(self):
        """Load saved data from a JSON file if it exists."""
        if os.path.exists(self.DATA_FILE):
            with open(self.DATA_FILE, "r", encoding="utf-8") as file:
                return json.load(file)
        return {}

    def save_data(self):
        """Save the current data to a JSON file."""
        with open(self.DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(self.data, file, ensure_ascii=False, indent=4)

    def setup_main_page(self):
        """Set up the main page of the application."""
        self.clear_window()

        ttk.Label(self.root, text="Use Input to add to the database", font=("Arial", 20)).pack(pady=20)

        ttk.Button(self.root, text="Input", command=self.setup_input_page).pack(pady=10)
        ttk.Button(self.root, text="Quiz", command=self.setup_output_page).pack(pady=10)
        ttk.Button(self.root, text="Exit", command=self.root.quit).pack(pady=10)

    def setup_input_page(self):
        """Set up the input page."""
        self.clear_window()

        ttk.Label(self.root, text="Input", font=("Arial", 20)).pack(pady=20)

        ttk.Label(self.root, text="Hiragana/Katakana:", font=("Arial", 16)).pack(pady=5)
        hiragana_entry = ttk.Entry(self.root)
        hiragana_entry.pack(pady=5)

        ttk.Label(self.root, text="Romanji:", font=("Arial", 16)).pack(pady=5)
        romanji_entry = ttk.Entry(self.root)
        romanji_entry.pack(pady=5)

        ttk.Label(self.root, text="English:", font=("Arial", 16)).pack(pady=5)
        english_entry = ttk.Entry(self.root)
        english_entry.pack(pady=5)

        def save_input():
            jp_input = hiragana_entry.get().strip().lower()
            romanji_input = romanji_entry.get().strip().lower()
            english_input = english_entry.get().strip().lower()

            if jp_input and romanji_input and english_input:
                self.data[jp_input] = {"romanji": romanji_input, "english": english_input}
                self.save_data()
                messagebox.showinfo("Success", f"Saved: {jp_input} -> {romanji_input} -> {english_input}")
                hiragana_entry.delete(0, tk.END)
                romanji_entry.delete(0, tk.END)
                english_entry.delete(0, tk.END)
            else:
                messagebox.showerror("Error", "All fields must be filled!")

        ttk.Button(self.root, text="Save", command=save_input).pack(pady=10)
        ttk.Button(self.root, text="Back to Main Menu", command=self.setup_main_page).pack(pady=10)

    def setup_output_page(self):
        """Set up the output page."""
        self.clear_window()

        if not self.data:
            messagebox.showerror("Error", "No data available! Please add some pairs first.")
            self.setup_main_page()
            return

        ttk.Label(self.root, text="Quiz", font=("Arial", 20)).pack(pady=20)

        jp_word = random.choice(list(self.data.keys()))

        ttk.Label(self.root, text=f"What is the Romanji for: \n'{jp_word}'",
                  font=("Arial", 16), justify="center").pack(pady=10)
        romanji_entry = ttk.Entry(self.root)
        romanji_entry.pack(pady=10)

        ttk.Label(self.root, text=f"What is the English translation?", font=("Arial", 16)).pack(pady=10)
        english_entry = ttk.Entry(self.root)
        english_entry.pack(pady=10)

        # feedback label for check
        feedback_label = ttk.Label(self.root, font=("Arial", 16))
        feedback_label.pack_forget()

        def check_answer():
            user_input1 = romanji_entry.get().strip().lower()
            user_input2 = english_entry.get().strip().lower()

            correct_romanji = self.data[jp_word]["romanji"]
            correct_english = self.data[jp_word]["english"]

            if user_input1 == correct_romanji and user_input2 == correct_english:
                feedback_label.config(text="Correct!", foreground="green")
            else:
                feedback_label.config(text=f"Wrong!\nRomanji: {correct_romanji}\nEnglish: {correct_english}",
                                      foreground="red")

            feedback_label.pack(pady=10)

            # delay for reload
            self.root.after(3000, self.setup_output_page)

        ttk.Button(self.root, text="Check", command=check_answer).pack(pady=10)
        ttk.Button(self.root, text="Back to Main Menu", command=self.setup_main_page).pack(pady=10)

    def clear_window(self):
        """Clear all widgets from the root window."""
        for widget in self.root.winfo_children():
            widget.destroy()


# Main program execution
if __name__ == "__main__":
    root = tk.Tk()
    app = JapaneseLanguageProgram(root)
    root.mainloop()
