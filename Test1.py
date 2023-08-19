import tkinter as tk
from tkinter import ttk
import requests
from PIL import Image, ImageTk
import csv
import tkinter.messagebox as messagebox
from tabulate import tabulate  # Import tabulate
import datetime
from tkinter import Scrollbar
from ttkthemes import ThemedStyle



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
        # Create a custom style for the Treeview header
        style = ttk.Style()
        style.theme_use("default")  # Use the default theme as a base
        style.configure("Treeview.Heading", background="gray")  # Set the header background color


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
        input_frame.config(bg="#F5F5DC")
        input_frame.pack(padx=10, pady=10)
        input_frame.place(x=10, y=10, width=980, height=185)
        input_frame.config(borderwidth=1, relief="solid", highlightbackground="gray")


        movie_name_label = tk.Label(input_frame, text="Movie Name", font=("Arial", 12, "bold"))
        movie_name_label.config(bg="#F5F5DC")
        movie_name_label.place(x=10, y=10)

        self.movie_name_entry = tk.Entry(input_frame,font=('Arial 14'))
        self.movie_name_entry.place(x=200, y=11)
        self.movie_name_entry.bind("<Return>", self.search_movie)

        movie_year_label = tk.Label(input_frame, text="Year of Release", font=("Arial", 12, "bold"))
        movie_year_label.config(bg="#F5F5DC")
        movie_year_label.place(x=10, y=50)
        self.movie_year_entry = tk.Entry(input_frame,font=('Arial 14'))
        self.movie_year_entry.place(x=200, y=51)

        movie_type_label = tk.Label(input_frame, text="Type", font=("Arial", 12, "bold"))
        movie_type_label.config(bg="#F5F5DC")
        movie_type_label.place(x=10, y=90)
        self.movie_type_combo = ttk.Combobox(input_frame,font=('Arial 14'), values=["movie", "series", "episode"])
        self.movie_type_combo.place(x=200, y=91)

        # Create a Canvas widget to draw the line
        canvas = tk.Canvas(input_frame, bg="#D9D9D9", width=1, height=110, highlightthickness=0)
        canvas.place(x=180, y=10)
        canvas.create_line(0, 0, 0, 380, fill="black")

        # Apply the "breeze" theme to the button
        style = ThemedStyle(input_frame)
        style.set_theme("breeze")  # Apply the "breeze" theme
        search_button = ttk.Button(input_frame, text="Search", command=self.search_movie)
        search_button.place(x=440, y=11)

        separator = ttk.Separator(parent, orient="horizontal")
        separator.pack(fill="x", padx=10, pady=5)

        self.result_frame = tk.Frame(parent)
        self.result_frame.config(bg="#D9D9D9")
        self.result_frame.pack(padx=10, pady=10)
        # Increase the size of the frame using .place()
        self.result_frame.place(x=10, y=200, width=980, height=480)
        # Add a gray border around the frame
        self.result_frame.config(borderwidth=1, relief="solid", highlightbackground="gray")
        # Create a placeholder label for the poster image
        self.poster_label = tk.Label(self.result_frame, text="Poster", font=("Arial", 12, "bold"),
                                     borderwidth=2, relief="solid", padx=80, pady=150)
        self.poster_label.grid(row=0, column=0, rowspan=16, padx=10, pady=50)
        self.poster_label.config(bg="#00BFFF")

        self.text_widget = tk.Text(self.result_frame, wrap="none", highlightthickness=2, highlightbackground="gray")
        self.text_widget.grid(row=0, column=1, padx=10, pady=5)


        self.initialize_checkboxes_and_button()

    def create_database_ui(self, parent):
        # Create a frame to hold the Treeview widget and the scrollbars
        database_frame = tk.Frame(parent)
        database_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.database_tree = ttk.Treeview(
            database_frame, columns=self.dblabels, show="headings"
        )
        database_frame.config(bg="#D9D9D9")
        self.database_tree.pack(fill="both", expand=False)

        for label in self.dblabels:
            self.database_tree.heading(label, text=label)
            self.database_tree.column(label, width=150)

        # Set the header background color to gray only for self.database_tree
        style = ttk.Style()
        style.configure(
            f"{self.database_tree}._header", background="gray"
        )  # Use the correct style name

        self.update_database_ui()




        horizontal_scrollbar = ttk.Scrollbar(self.database_tree, orient="horizontal", command=self.database_tree.xview)
        horizontal_scrollbar.place(relx=0, rely=0.95, relwidth=0.99, relheight=0.05)
        self.database_tree.config(xscrollcommand=horizontal_scrollbar.set)

        # Create a vertical scrollbar
        vertical_scrollbar = ttk.Scrollbar(self.database_tree, orient="vertical", command=self.database_tree.yview)
        vertical_scrollbar.place(relx=0.98, rely=0, relwidth=0.03, relheight=0.99)
        self.database_tree.config(yscrollcommand=vertical_scrollbar.set)

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

    def search_movie(self, event=None):
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
        self.poster_label.config(image=None, bg="#D9D9D9")
        self.text_widget.config(state="normal")
        self.text_widget.delete("1.0", tk.END)

        if movie_data.get("Response") == "True":
            poster_url = movie_data.get("Poster")
            if poster_url != "N/A":
                image = Image.open(requests.get(poster_url, stream=True).raw)
                image.thumbnail((200, 300))
                self.poster_image = ImageTk.PhotoImage(image)
                self.poster_label.config(image=self.poster_image, bg="#D9D9D9")

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
        watched_radio.config(bg="#D9D9D9")
        watched_radio.place(x=260, y=450, anchor="w")

        I_want_to_watch_radio = tk.Radiobutton(self.result_frame, text="I Want to Watch", variable=self.watched_var,
                                               value=0)
        I_want_to_watch_radio.config(bg="#D9D9D9")
        I_want_to_watch_radio.place(x=360, y=450, anchor="w")

        # Create "Save" button
        save_button = tk.Button(self.result_frame, text="Save", command=self.save_result, width=20, height=2)
        save_button.place(x=530, y=450, anchor="w")

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
    root.config(bg="#D9D9D9")
    root.geometry("1000x750")
    root.resizable(False, False)  # Lock resizing
    app = MovieSearchApp(root)
    root.mainloop()
