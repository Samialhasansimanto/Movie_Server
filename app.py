from flask import Flask, render_template, request, jsonify
import json
import os


app = Flask(__name__, template_folder='templates') # root path track rakhar jnno template_folder 

def load_movie_database():
    db_path = os.path.join(os.path.dirname(__file__), 'movies.json')
    if os.path.exists(db_path):
        with open(db_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    return []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.json or {}
    
    genre = data.get('genre')
    movie_type = data.get('type')
    min_rating_raw = data.get('rating')

    # Rating value 
    min_rating = None
    if min_rating_raw:
        try:
            min_rating = float(min_rating_raw)
        except ValueError:
            pass

    movies_list = load_movie_database()
    filtered_movies = []

    # Helper Functin
    def matches_rating(movie_obj):
        if min_rating is None:
            return True
        try:
            return float(movie_obj.get('rating', 0)) >= min_rating
        except ValueError:
            return True  # convert error but true

    # Genre & Type Match Condition
    for movie in movies_list:
        if movie.get('genre') == genre and movie.get('type') == movie_type:
            if matches_rating(movie):
                filtered_movies.append(movie)

    # fallback 
    if not filtered_movies:
        for movie in movies_list:
            if movie.get('genre') == genre:
                if matches_rating(movie):
                    filtered_movies.append(movie)

    # Decending order for Rating
    try:
        filtered_movies.sort(key=lambda x: float(x.get('rating', 0)), reverse=True)
    except (ValueError, TypeError):
        pass

    return jsonify(filtered_movies[:12])

if __name__ == '__main__':
    #for local network use tai host 0.0.0.0 dewa
    app.run(debug=True, port=5000)
