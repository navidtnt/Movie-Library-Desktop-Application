import requests

api_key = "45edf973"  # Replace with your OMDB API key

def search_movie():
    movie_name = input("Enter the movie name: ")
    movie_year = input("Enter the movie year: ")
    movie_type = input("Enter the movie type (movie/series/episode): ")

    url = f"http://www.omdbapi.com/?apikey={api_key}&t={movie_name}&y={movie_year}&type={movie_type}"

    response = requests.get(url)

    if response.status_code == 200:
        movie_data = response.json()
        if movie_data.get("Response") == "True":
            print("Movie Details:")
            print("Title:", movie_data.get("Title"))
            print("Genre:", movie_data.get("Genre"))
            print("Length:", movie_data.get("Runtime"))
            print("IMDB Rating:", movie_data.get("imdbRating"))
            print("Votes:", movie_data.get("imdbVotes"))
            print("Plot:", movie_data.get("Plot"))
            print("Rotten Tomatoes Rating:", get_rotten_tomatoes_rating(movie_data))
            print("IMDB ID:", movie_data.get("imdbID"))
            print("Type:", movie_data.get("Type"))
            print("Year:", movie_data.get("Year"))
            print("Rated:", movie_data.get("Rated"))
            print("Released Date:", movie_data.get("Released"))
            print("Director:", movie_data.get("Director"))
            print("Writer:", movie_data.get("Writer"))
            print("Actors:", movie_data.get("Actors"))
            print("Country:", movie_data.get("Country"))
            print("Awards:", movie_data.get("Awards"))
        else:
            print("Movie not found.")
    else:
        print("Error occurred while making the request.")

def get_rotten_tomatoes_rating(movie_data):
    ratings = movie_data.get("Ratings")
    if ratings:
        for rating in ratings:
            if "Rotten Tomatoes" in rating['Source']:
                return rating['Value']
    return "N/A"

search_movie()
