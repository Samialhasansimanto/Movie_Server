from flask import Flask, render_template, request, jsonify
import json
import os

# root path ট্র্যাক রাখার জন্য template_folder বলে দেওয়া নিরাপদ
app = Flask(__name__, template_folder='templates')

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

    # রেটিং ভ্যালু লুপের বাইরেই একবার সেফলি ফ্লোটে কনভার্ট করে নেওয়া ভালো
    min_rating = None
    if min_rating_raw:
        try:
            min_rating = float(min_rating_raw)
        except ValueError:
            pass

    movies_list = load_movie_database()
    filtered_movies = []

    # হেল্পার ফাংশন: মুভি রেটিং ক্রাইটেরিয়া ম্যাচ করে কিনা চেক করার জন্য
    def matches_rating(movie_obj):
        if min_rating is None:
            return True
        try:
            return float(movie_obj.get('rating', 0)) >= min_rating
        except ValueError:
            return True  # কনভার্ট না করতে পারলে সেফ সাইডে রাখার জন্য True দেওয়া

    # ১. প্রথম ধাপ: Genre এবং Type দুইটাই ম্যাচ করানো
    for movie in movies_list:
        if movie.get('genre') == genre and movie.get('type') == movie_type:
            if matches_rating(movie):
                filtered_movies.append(movie)

    # ২. ফলব্যাক ধাপ: যদি প্রথম ধাপে কোনো মুভি না পাওয়া যায়, শুধু Genre দিয়ে খুঁজবে
    if not filtered_movies:
        for movie in movies_list:
            if movie.get('genre') == genre:
                if matches_rating(movie):
                    filtered_movies.append(movie)

    # রেটিং অনুযায়ী Descending (বড় থেকে ছোট) অর্ডারে সর্ট করা
    try:
        filtered_movies.sort(key=lambda x: float(x.get('rating', 0)), reverse=True)
    except (ValueError, TypeError):
        pass

    return jsonify(filtered_movies[:12])

if __name__ == '__main__':
    # প্রোডাকশনে বা লোকাল নেটওয়ার্কে টেস্ট করার জন্য host='0.0.0.0' দেওয়া সুবিধাজনক
    app.run(debug=True, port=5000)