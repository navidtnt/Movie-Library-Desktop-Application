import tkinter as tk
from tkinter import ttk
import requests
from PIL import Image, ImageTk
import csv
import tkinter.messagebox as messagebox
from tabulate import tabulate  # Import tabulate

class MovieSearchApp:
    def __init__(self, root):
        self.root = root
        self.api_key = "45edf973"
        self.id_counter = 0  # Initialize the ID counter
        self.detail_labels = [  # Define detail labels here
            "ID", "Title", "Genre", "Runtime", "Year", "Director",
            "IMDB Rating", "IMDB Votes", "Rotten Tomatoes",
            "Actors", "IMDB ID", "Type", "Rated", "Released",
            "Writer", "Country", "Awards", "Plot"
        ]
        self.initialize_ui()

    def initialize_ui(self):
        self.root.title("Movie Search App")

        # Create a notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)

        # Create the first tab for New Search
        new_search_tab = ttk.Frame(self.notebook)
        self.notebook.add(new_search_tab, text="New Search")
        self.create_search_ui(new_search_tab)

        # Create the second tab for Database
        database_tab = ttk.Frame(self.notebook)
        self.notebook.add(database_tab, text="Database")
        self.create_database_ui(database_tab)


    def update_database_ui(self):
        self.database_tree.delete(*self.database_tree.get_children())  # Clear existing table rows

        try:
            with open("movie_results.csv", "r") as csv_file:
                csv_reader = csv.reader(csv_file)
                header = next(csv_reader)
                for row in csv_reader:
                    self.database_tree.insert("", "end", values=row)
        except FileNotFoundError:
            pass

    def create_search_ui(self, parent):
        input_frame = tk.Frame(parent)
        input_frame.pack(padx=10, pady=10)

        movie_name_label = tk.Label(input_frame, text="Movie Name:")
        movie_name_label.grid(row=0, column=0, sticky="e")
        self.movie_name_entry = tk.Entry(input_frame)
        self.movie_name_entry.grid(row=0, column=1, padx=5)

        movie_year_label = tk.Label(input_frame, text="Year of Release:")
        movie_year_label.grid(row=0, column=2, sticky="e")
        self.movie_year_entry = tk.Entry(input_frame)
        self.movie_year_entry.grid(row=0, column=3, padx=5)

        movie_type_label = tk.Label(input_frame, text="Type:")
        movie_type_label.grid(row=0, column=4, sticky="e")
        self.movie_type_combo = ttk.Combobox(input_frame, values=["movie", "series", "episode"])
        self.movie_type_combo.grid(row=0, column=5, padx=5)

        search_button = tk.Button(input_frame, text="Search", command=self.search_movie)
        search_button.grid(row=0, column=6, padx=10)

        separator = ttk.Separator(parent, orient="horizontal")
        separator.pack(fill="x", padx=10, pady=5)

        self.result_frame = tk.Frame(parent)
        self.result_frame.pack(padx=10, pady=10)
        # Create a placeholder label for the poster image
        self.poster_label = tk.Label(self.result_frame, text="Poster", font=("Arial", 12, "bold"),
                                     borderwidth=2, relief="solid", padx=80, pady=150)
        self.poster_label.grid(row=0, column=0, rowspan=16, padx=10, pady=50)

        self.text_widget = tk.Text(self.result_frame, wrap="none")
        self.text_widget.grid(row=0, column=1, padx=10, pady=5)

        self.initialize_checkboxes_and_button()

    def create_database_ui(self, parent):
        self.database_tree = ttk.Treeview(parent, columns=self.detail_labels, show="headings")
        self.database_tree.pack(padx=10, pady=10, fill="both", expand=True)

        for label in self.detail_labels:
            self.database_tree.heading(label, text=label)
            self.database_tree.column(label, width=150)

        try:
            with open("movie_results.csv", "r") as csv_file:
                csv_reader = csv.reader(csv_file)
                header = next(csv_reader)
                for row in csv_reader:
                    self.database_tree.insert("", "end", values=row)
        except FileNotFoundError:
            pass



    def search_movie(self):
        self.id_counter += 1
        movie_name = self.movie_name_entry.get()
        movie_year = self.movie_year_entry.get()
        movie_type = self.movie_type_combo.get()

        url = f"http://www.omdbapi.com/?apikey={self.api_key}&t={movie_name}&y={movie_year}&type={movie_type}"
        response = requests.get(url)
        movie_data = response.json()

        self.update_ui(movie_data)
        self.update_database_ui()

    def update_ui(self, movie_data):
        # Clear previous data from the table and poster image
        self.poster_label.config(image=None)
        self.text_widget.config(state="normal")
        self.text_widget.delete("1.0", tk.END)

        if movie_data.get("Response") == "True":
            poster_url = movie_data.get("Poster")
            if poster_url != "N/A":
                image = Image.open(requests.get(poster_url, stream=True).raw)
                image.thumbnail((200, 300))
                self.poster_image = ImageTk.PhotoImage(image)
                self.poster_label.config(image=self.poster_image)

            self.detail_values = [
                self.id_counter,
                movie_data.get("Title"), movie_data.get("Genre"), movie_data.get("Runtime"),
                movie_data.get("Year"), movie_data.get("Director"), movie_data.get("imdbRating"),
                movie_data.get("imdbVotes"), self.get_rotten_tomatoes_rating(movie_data),
                movie_data.get("Actors"), movie_data.get("imdbID"), movie_data.get("Type"),
                movie_data.get("Rated"), movie_data.get("Released"), movie_data.get("Writer"),
                movie_data.get("Country"), movie_data.get("Awards"), movie_data.get("Plot")
            ]

            movie_details = [
                [label.strip(":"), value] for label, value in zip(self.detail_labels, self.detail_values)
            ]

            table = tabulate(movie_details, headers=["Name", "Details"], tablefmt="grid")
            self.text_widget.config(state="normal", bg="#FFFFE0")
            self.text_widget.delete("1.0", tk.END)
            self.text_widget.insert(tk.END, table)
            self.text_widget.config(state="disabled")

        else:
            error_message = "Movie data not found."
            self.text_widget.insert(tk.END, error_message)

        # Update the UI of the Database tab
        self.update_database_ui()

        self.initialize_checkboxes_and_button()

    def get_rotten_tomatoes_rating(self, movie_data):
        ratings = movie_data.get("Ratings")
        if ratings:
            for rating in ratings:
                if "Rotten Tomatoes" in rating['Source']:
                    return rating['Value']
        return "N/A"

    def initialize_checkboxes_and_button(self):
        self.watched_var = tk.IntVar(value=0)
        self.want_to_watch_var = tk.IntVar(value=0)

        # Create radio buttons for "Watched" and "I Want to Watch"
        watched_radio = tk.Radiobutton(self.result_frame, text="Watched", variable=self.watched_var, value=1)
        watched_radio.grid(row=17, column=0, padx=10, pady=5, sticky="w")

        want_to_watch_radio = tk.Radiobutton(self.result_frame, text="I Want to Watch", variable=self.watched_var,
                                             value=0)
        want_to_watch_radio.grid(row=17, column=1, padx=10, pady=5, sticky="w")

        # Create "Save" button
        save_button = tk.Button(self.result_frame, text="Save", command=self.save_result)
        save_button.grid(row=18, column=0, columnspan=2, padx=10, pady=10, sticky="we")

    def save_result(self):
        # Get the next available ID from the CSV file

        highest_id = 0
        try:
            with open("movie_results.csv", 'r', newline='') as csv_file:
                csv_reader = csv.reader(csv_file)
                next(csv_reader)  # Skip the header row
                for row in csv_reader:
                    if row:
                        row_id = int(row[0])  # Assuming ID is the first column
                        highest_id = max(highest_id, row_id)
        except FileNotFoundError:
            pass

        next_id = highest_id + 1

        watched = 1 if self.watched_var.get() == 1 else 0
        want_to_watch = 1 if self.want_to_watch_var.get() == 1 else 0

        title = self.detail_values[1]

        # Check if the title already exists in the CSV file
        is_title_exists = False
        try:
            with open("movie_results.csv", 'r', newline='') as csv_file:
                csv_reader = csv.reader(csv_file)
                for row in csv_reader:
                    if row and row[1] == title:
                        is_title_exists = True
                        break
        except FileNotFoundError:
            pass

        if not is_title_exists:
            # Write header row if the file is empty
            is_file_empty = False
            try:
                with open("movie_results.csv", 'r') as csv_file:
                    is_file_empty = csv_file.read().strip() == ''
            except FileNotFoundError:
                is_file_empty = True

            if is_file_empty:
                with open("movie_results.csv", 'a', newline='') as csv_file:
                    csv_writer = csv.writer(csv_file)
                    csv_writer.writerow(self.detail_labels[1:] + ["Watched", "I Want to Watch"])  # Add new columns

            # Append the data to the CSV file
            with open("movie_results.csv", 'a', newline='') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow([next_id] + self.detail_values[1:] + [watched, want_to_watch])  # Append data

            # Show success message box
            messagebox.showinfo("Success", "Data has been saved")

        else:
            # Show warning message box
            messagebox.showwarning("Warning", f"Title '{title}' already exists")

        self.update_database_ui()



if __name__ == "__main__":
    root = tk.Tk()
    app = MovieSearchApp(root)
    root.mainloop()