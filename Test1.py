import tkinter as tk
from tkinter import ttk
import requests
from PIL import Image, ImageTk
import csv
import tkinter.messagebox as messagebox
from tabulate import tabulate  # Import tabulate
import datetime
from tkinter import Scrollbar


class MovieSearchApp:
    def __init__(self, root):
        self.root = root
        self.api_key = "45edf973"
        self.search_count = 0
        self.last_search_time = None
        self.load_search_count()
        self.id_counter = 0  # Initialize the ID counter
        self.detail_labels = [  # Define detail labels here
            "Title", "Genre", "Runtime", "Year", "Director",
            "IMDB Rating", "IMDB Votes", "Rotten Tomatoes",
            "Actors", "IMDB ID", "Type", "Rated", "Released",
            "Writer", "Country", "Awards", "Plot"
        ]
        self.dblabels = [  # Define detail labels here
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

        # Create the third tab for Analyzed Data
        analyzed_data_tab = ttk.Frame(self.notebook)
        self.notebook.add(analyzed_data_tab, text="Analyzed Data")
        self.create_analyzed_data_ui(analyzed_data_tab)

    def create_analyzed_data_ui(self, parent):
        self.analyzed_tree = ttk.Treeview(parent, columns=["Date", "Count"], show="headings")
        self.analyzed_tree.pack(padx=10, pady=10, fill="both", expand=False)

        self.analyzed_tree.heading("Date", text="Date")
        self.analyzed_tree.column("Date", width=10)

        self.analyzed_tree.heading("Count", text="Search Count")
        self.analyzed_tree.column("Count", width=10)

        self.update_analyzed_data_ui()

    def update_analyzed_data_ui(self):
        self.analyzed_tree.delete(*self.analyzed_tree.get_children())  # Clear existing table rows

        try:
            with open("analyze.csv", "r") as csv_file:
                csv_reader = csv.reader(csv_file)
                next(csv_reader)  # Skip header row
                for row in csv_reader:
                    self.analyzed_tree.insert("", "end", values=row)
        except FileNotFoundError:
            pass




    def load_search_count(self):
        # Load the search count and date from the analyze.csv file
        try:
            with open("analyze.csv", "r") as csv_file:
                csv_reader = csv.reader(csv_file)
                last_row = list(csv_reader)[-1]
                date_str, count_str = last_row
                self.last_search_date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
                self.search_count = int(count_str)
        except (FileNotFoundError, IndexError, ValueError):
            self.last_search_date = None
            self.search_count = 0

    def update_database_ui(self):
        self.database_tree.delete(*self.database_tree.get_children())  # Clear existing table rows

        try:
            with open("movie_results.csv", "r") as csv_file:
                csv_reader = csv.reader(csv_file)
                header = next(csv_reader)
                i = 1
                for row in csv_reader:
                    row.insert(0, str(i))
                    i += 1
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
        self.database_tree = ttk.Treeview(parent, columns=self.dblabels, show="headings")
        self.database_tree.pack(padx=10, pady=10, fill="both", expand=False)

        for label in self.dblabels:
            self.database_tree.heading(label, text=label)
            self.database_tree.column(label, width=150)

        self.update_database_ui()
        # Create a horizontal scrollbar
        horizontal_scrollbar = ttk.Scrollbar(parent, orient="horizontal", command=self.database_tree.xview)
        horizontal_scrollbar.pack(side="bottom", fill="x")
        # Create a vertical scrollbar
        vertical_scrollbar = ttk.Scrollbar(parent, orient="vertical", command=self.database_tree.yview)
        vertical_scrollbar.pack(side="bottom", fill="y")

        # Configure Treeview to use the horizontal scrollbar
        self.database_tree.configure(xscrollcommand=horizontal_scrollbar.set, yscrollcommand=vertical_scrollbar.set)
        # Place the scrollbars where you want them
        vertical_scrollbar.place(relx=1, rely=0, relheight=1, anchor="ne")
        horizontal_scrollbar.place(relx=0, rely=1, relwidth=1, anchor="sw")



    def save_search_count(self):
        filename = 'analyze.csv'
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        counter_updated = False

        try:
            with open(filename, 'r') as csv_file:
                csv_reader = csv.reader(csv_file)
                rows = list(csv_reader)

            for row in rows:
                if row[0] == current_date:
                    row[1] = str(int(row[1]) + 1)
                    counter_updated = True
                    break

            if not counter_updated:
                rows.append([current_date, '1'])

            with open(filename, 'w', newline='') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(['Date', 'Count'])
                csv_writer.writerows(rows[1:])  # Write all rows except the header

        except FileNotFoundError:
            with open(filename, 'w', newline='') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(['Date', 'Count'])
                csv_writer.writerow([current_date, '1'])

    def search_movie(self):
        self.id_counter += 1
        movie_name = self.movie_name_entry.get()
        movie_year = self.movie_year_entry.get()
        movie_type = self.movie_type_combo.get()

        url = f"http://www.omdbapi.com/?apikey={self.api_key}&t={movie_name}&y={movie_year}&type={movie_type}"
        response = requests.get(url)
        movie_data = response.json()
        self.update_ui(movie_data)
        self.save_search_count()  # Update the search count
        self.update_database_ui()
        self.update_analyzed_data_ui()  # Update the Analyzed Data tab

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

            table = tabulate(movie_details, tablefmt="grid")
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

    def save_analyze_data(self, count):
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        analyze_data = [current_date, count]

        try:
            with open("analyze.csv", "a", newline="") as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(analyze_data)
        except Exception as e:
            print("Error saving analyze data:", e)

    def save_result(self):
        watched = 'yes' if self.watched_var.get() == 'yes' else 'no'
        want_to_watch = 'yes' if self.want_to_watch_var.get() == 'yes' else 'no'

        title = self.detail_values[0]

        # Check if the title already exists in the CSV file
        is_title_exists = False
        try:
            with open("movie_results.csv", 'r', newline='') as csv_file:
                csv_reader = csv.reader(csv_file)
                for row in csv_reader:
                    if row and row[0] == title:
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
                    csv_writer.writerow(self.dblabels[1:] + ["Watched", "I Want to Watch"])  # Add new columns

            # Append the data to the CSV file
            with open("movie_results.csv", 'a', newline='') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(self.detail_values[0:] + [watched, want_to_watch])  # Append data

            # Show success message box
            messagebox.showinfo("Success", "Data has been saved")

        else:
            # Show warning message box
            messagebox.showwarning("Warning", f"Title '{title}' already exists")

        self.update_database_ui()



if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1000x600")
    app = MovieSearchApp(root)
    root.mainloop()