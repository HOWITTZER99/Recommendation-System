import json
from flask import Flask, request, jsonify, render_template
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Initialize Flask application
app = Flask(__name__)

# Load the movie dataset from a JSON file
with open('movie.json', 'r') as f:
    movie_dict = json.load(f)

# Convert the movie dictionary to a Pandas DataFrame
movies = pd.DataFrame(movie_dict)

# Create a CountVectorizer object with max_features of 5000 and remove stop words
cv = CountVectorizer(max_features=5000, stop_words='english')

# Use CountVectorizer to create vectors for the movie tags
vectors = cv.fit_transform(movies['tags']).toarray()

# Calculate cosine similarity between the movie tag vectors
similar = cosine_similarity(vectors)

# Define a route for the home page
@app.route('/')
def home():
    # Render the index.html template
    return render_template('index.html')

# Define a route for recommending similar movies
@app.route('/recommend', methods=['POST'])
def recommend_content():
    # Get the name of the selected movie from the request data
    movie = request.json['movie']
    # Get the index of the selected movie in the DataFrame
    movie_index = movies[movies['title']== movie].index[0]
    # Calculate the cosine similarity between the selected movie and all other movies
    dist = similar[movie_index]
    # Get the indices and similarities of the top 5 similar movies
    movie_list = sorted(list(enumerate(dist)),reverse=True, key=lambda x:x[1])[1:6]
    # Get the titles of the top 5 similar movies
    movie_name = []
    for i in movie_list:
        movie_name.append(movies.iloc[i[0]].title)
    # Return the titles of the top 5 similar movies as a JSON response
    return jsonify(movie_name)

# Start the Flask application in debug mode
if __name__ == '__main__':
    app.run(debug=True)
