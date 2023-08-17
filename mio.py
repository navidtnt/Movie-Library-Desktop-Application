import requests
import csv
import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import io  # Add this import statement for the 'io' module
from tkinter import ttk

# Create the main Tk() instance
root = tk.Tk()
root.title("Movie Search and Data Storage")

api_key = "45edf973"  # Replace with your OMDB API key

# Create or open the CSV file
csv_filename = "movie_data.csv"
csv_file_exists = os.path.exists(csv_filename)

# Initialize searched_movies set
searched_movies = set()


# Function to search movie data
def search_movie():
    movie_name = movie_name_entry.get()
    movie_year = movie_year_entry.get()
    movie_rate = movie_rate_var.get()

    url = f"http://www.omdbapi.com/?apikey={api_key}&t={movie_name}&y={movie_year}&type={movie_rate}"

    response = requests.get(url)

    if response.status_code == 200:
        movie_data = response.json()
        if movie_data.get("Response") == "True":
            show_movie_details(movie_data)
        else:
            messagebox.showerror("Movie Not Found", "Movie not found.")
    else:
        messagebox.showerror("Request Error", "Error occurred while making the request.")


# Function to show movie details
def show_movie_details(movie_data):
    title_label.config(text="Title: " + movie_data.get("Title"))
    genre_label.config(text="Genre: " + movie_data.get("Genre"))
    length_label.config(text="Length: " + movie_data.get("Runtime"))
    imdb_rating_label.config(text="IMDB Rating: " + movie_data.get("imdbRating"))
    imdb_votes_label.config(text="Votes: " + movie_data.get("imdbVotes"))
    plot_text.delete(1.0, tk.END)
    plot_text.insert(tk.END, "Plot: " + movie_data.get("Plot"))

    # Show the plot text box
    plot_text.pack()
    rotten_tomatoes_rating_label.config(text="Rotten Tomatoes Rating: " + get_rotten_tomatoes_rating(movie_data))
    imdb_id_label.config(text="IMDB ID: " + movie_data.get("imdbID"))
    type_label.config(text="Type: " + movie_data.get("Type"))
    year_label.config(text="Year: " + movie_data.get("Year"))
    rated_label.config(text="Rated: " + movie_data.get("Rated"))
    released_label.config(text="Released Date: " + movie_data.get("Released"))
    director_label.config(text="Director: " + movie_data.get("Director"))
    writer_label.config(text="Writer: " + movie_data.get("Writer"))
    actors_label.config(text="Actors: " + movie_data.get("Actors"))
    country_label.config(text="Country: " + movie_data.get("Country"))
    awards_label.config(text="Awards: " + movie_data.get("Awards"))
    # poster_url_label.config(text="Poster URL: " + movie_data.get("Poster"))
    # Load and display movie poster
    poster_url = movie_data.get("Poster")
    if poster_url and poster_url != "N/A":
        response = requests.get(poster_url)
        if response.status_code == 200:
            poster_data = response.content
            poster_image = Image.open(io.BytesIO(poster_data))
            poster_photo = ImageTk.PhotoImage(poster_image)
            poster_label.config(image=poster_photo)
            poster_label.image = poster_photo  # Keep a reference to prevent garbage collection
        else:
            poster_label.config(image=None)
    else:
        poster_label.config(image="")


# Create a Label to display the movie poster
poster_label = tk.Label(root)
poster_label.pack(side=tk.RIGHT, padx=10, pady=10)


# Function to get Rotten Tomatoes rating
def get_rotten_tomatoes_rating(movie_data):
    ratings = movie_data.get("Ratings")
    if ratings:
        for rating in ratings:
            if "Rotten Tomatoes" in rating['Source']:
                return rating['Value']
    return "N/A"


# Initialize existing_data set
existing_data = set()

# Load existing data from CSV into memory
if csv_file_exists:
    with open(csv_filename, mode="r", encoding="utf-8") as csv_read_file:
        csv_reader = csv.reader(csv_read_file)
        next(csv_reader, None)  # Skip the header row
        for row in csv_reader:
            existing_data.add(row[0])  # Assuming title is in the first column

# Create BooleanVar variables for checkboxes
watched_var = tk.BooleanVar()
watchlist_var = tk.BooleanVar()


# Function to save movie data
def save_movie():
    global csv_writer, existing_data, watched_var, watchlist_var

    # Get checkbox values as "Yes" or "No"
    watched = "Yes" if watched_var.get() else "No"
    watchlist = "Yes" if watchlist_var.get() else "No"

    # Get movie data from the labels
    movie_title = title_label.cget("text")[7:]

    # Check if the movie title already exists
    if movie_title in existing_data:
        messagebox.showwarning("Duplicate Movie", "Movie data already exists.")
        return

    movie_genre = genre_label.cget("text")[7:]
    movie_length = length_label.cget("text")[8:]
    imdb_rating = imdb_rating_label.cget("text")[13:]
    imdb_votes = imdb_votes_label.cget("text")[7:]
    rotten_tomatoes_rating = rotten_tomatoes_rating_label.cget("text")[25:]
    imdb_id = imdb_id_label.cget("text")[10:]
    movie_type = type_label.cget("text")[6:]
    movie_year = year_label.cget("text")[6:]
    movie_rated = rated_label.cget("text")[7:]
    movie_released = released_label.cget("text")[14:]
    movie_director = director_label.cget("text")[11:]
    movie_writer = writer_label.cget("text")[8:]
    movie_actors = actors_label.cget("text")[9:]
    movie_country = country_label.cget("text")[9:]
    movie_awards = awards_label.cget("text")[8:]
    movie_plot = plot_text.get("1.0", tk.END)
    movie_poster = poster_url_label.cget("text")[12:]

    # Save movie data in CSV file
    csv_writer.writerow([
        movie_title,
        movie_genre,
        movie_length,
        imdb_rating,
        imdb_votes,
        rotten_tomatoes_rating,
        imdb_id,
        movie_type,
        movie_year,
        movie_rated,
        movie_released,
        movie_director,
        movie_writer,
        movie_actors,
        movie_country,
        movie_awards,
        movie_plot,
        movie_poster,
        watched,  # Include watched value
        watchlist,  # Include watchlist value
    ])
    searched_movies.add(movie_title)
    existing_data.add(movie_title)
    messagebox.showinfo("Movie Saved", "Movie data saved successfully!")


# Set up a consistent color palette
PRIMARY_COLOR = "#007BFF"
BACKGROUND_COLOR = "#F4F4F4"

# Create a main frame with a consistent background color
main_frame = tk.Frame(root, bg=BACKGROUND_COLOR)
main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

# Movie Name and Year
movie_name_label = tk.Label(main_frame, text="Movie Name:", bg=BACKGROUND_COLOR)
movie_name_label.grid(row=0, column=0, sticky="w", pady=(0, 5))
movie_name_entry = tk.Entry(main_frame)
movie_name_entry.grid(row=0, column=1, padx=(0, 20), pady=(0, 5))

movie_year_label = tk.Label(main_frame, text="Movie Year:", bg=BACKGROUND_COLOR)
movie_year_label.grid(row=1, column=0, sticky="w", pady=(0, 5))
movie_year_entry = tk.Entry(main_frame)
movie_year_entry.grid(row=1, column=1, padx=(0, 20), pady=(0, 5))

# Movie Type (Rate)
movie_rate_label = tk.Label(main_frame, text="Movie Type:", bg=BACKGROUND_COLOR)
movie_rate_label.grid(row=2, column=0, sticky="w", pady=(0, 5))
movie_rate_var = tk.StringVar()
movie_rate_var.set("movie")

# Use ttk.Combobox for a more stylish dropdown
movie_rate_combobox = ttk.Combobox(main_frame, textvariable=movie_rate_var, state="readonly")
movie_rate_combobox["values"] = ("Movie", "Series", "Episode")
movie_rate_combobox.grid(row=2, column=1, padx=(0, 20), pady=(0, 5))

# Search Button
search_button = tk.Button(main_frame, text="Search", command=search_movie, bg=PRIMARY_COLOR, fg="white")

search_button.grid(row=3, column=1, pady=(10, 0))

# Movie Details Labels
title_label = tk.Label(root, text="")
title_label.pack()
genre_label = tk.Label(root, text="")
genre_label.pack()
length_label = tk.Label(root, text="")
length_label.pack()
imdb_rating_label = tk.Label(root, text="")
imdb_rating_label.pack()
imdb_votes_label = tk.Label(root, text="")
imdb_votes_label.pack()
rotten_tomatoes_rating_label = tk.Label(root, text="")
rotten_tomatoes_rating_label.pack()
imdb_id_label = tk.Label(root, text="")
imdb_id_label.pack()
type_label = tk.Label(root, text="")
type_label.pack()
year_label = tk.Label(root, text="")
year_label.pack()
rated_label = tk.Label(root, text="")
rated_label.pack()
released_label = tk.Label(root, text="")
released_label.pack()
director_label = tk.Label(root, text="")
director_label.pack()
writer_label = tk.Label(root, text="")
writer_label.pack()
actors_label = tk.Label(root, text="")
actors_label.pack()
country_label = tk.Label(root, text="")
country_label.pack()
awards_label = tk.Label(root, text="")
awards_label.pack()

# Plot Text
plot_text = tk.Text(root, width=40, height=6)
plot_text.pack()
plot_text.pack_forget()  # Hide the plot text box initially

# Poster URL Label
poster_url_label = tk.Label(root, text="")
poster_url_label.pack()

# Checkboxes for Watched and Watchlist
watched_checkbox = tk.Checkbutton(root, text="Watched", variable=watched_var)
watched_checkbox.pack()
watchlist_checkbox = tk.Checkbutton(root, text="Watchlist", variable=watchlist_var)
watchlist_checkbox.pack()

# Save Button
save_button = tk.Button(root, text="Save", command=save_movie)
save_button.pack()

# Create or open the CSV file for writing
csv_file = open(csv_filename, mode="a", newline="", encoding="utf-8")
csv_writer = csv.writer(csv_file)


# Add new columns to the header if needed
if not csv_file_exists or csv_file.tell() == 0:
    csv_writer.writerow([
        "Title",
        "Genre",
        "Length",
        "IMDB Rating",
        "Votes",
        "Rotten Tomatoes Rating",
        "IMDB ID",
        "Type",
        "Year",
        "Rated",
        "Released",
        "Director",
        "Writer",
        "Actors",
        "Country",
        "Awards",
        "Plot",
        "Poster URL",
        "Watched",  # New column for watched
        "Watchlist",  # New column for watchlist
    ])

root.mainloop()
