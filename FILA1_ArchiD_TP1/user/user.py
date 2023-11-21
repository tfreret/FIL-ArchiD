from flask import Flask, render_template, request, jsonify, make_response
import requests
import json
import random
from werkzeug.exceptions import NotFound

# create flask app
app = Flask(__name__)
PORT = 3203
HOST = '0.0.0.0'

# load users from json file
with open('{}/databases/users.json'.format("."), "r") as jsf:
   users = json.load(jsf)["users"]


# API routes
# default route
@app.route("/", methods=['GET'])
def home():
   return "<h1 style='color:blue'>Welcome to the User service!</h1>"

# get all users 
@app.route("/users", methods=['GET'])
def get_users():
    res = make_response(jsonify(users), 200)
    return res

# get user by id
@app.route("/users/<userid>", methods=['GET'])
def get_user_by_id(userid):
    for user in users:
        if str(user["id"]) == str(userid):
            res = make_response(jsonify(user),200)
            return res
    return make_response(jsonify({"error":"User ID not found"}),400)

# add user
@app.route("/users/<userid>", methods=['POST'])
def add_user(userid):
    req = request.get_json()
    for user in users:
        if str(userid) in user["id"]:
            return make_response(jsonify({"error":"an existing item already exists"}),409)
    newUser = {"id": userid, "name": req["name"], "last_active": ''.join([str(random.randint(0, 9)) for _ in range(10)])}
    users.append(newUser)
    res = make_response(jsonify(newUser),200)
    return res

# get bookings for user
@app.route("/booking/<userid>", methods=['GET'])
def get_booking_for_user(userid):
    for user in users:
        if str(user["id"]) == str(userid):
            getBookings = requests.get("http://booking:3201/bookings/" + userid).json()
            res = make_response(jsonify(getBookings),200)
            return res
    return make_response(jsonify({"error":"bad input parameter"}),400)

# add booking for user
@app.route("/booking/<userid>", methods=['POST'])
def add_booking(userid):
    for user in users:
        if str(user["id"]) == str(userid):
            getBookings = requests.post("http://booking:3201/bookings/" + userid, json = request.get_json()).json()
            res = make_response(jsonify(getBookings),200)
            return res
    return make_response(jsonify({"error":"bad input parameter"}),400)

# get last booking for user
@app.route("/lastbooking/<userid>", methods=['GET'])
def get_last_booking_for_user(userid):
    for user in users:
        if str(user["id"]) == str(userid):
            getBookings = requests.get("http://booking:3201/bookings/" + userid).json()
            lastBooking = ""
            for booking in getBookings["dates"]:
                print(booking)
                if lastBooking == "" or int(lastBooking["date"]) < int(booking["date"]) :
                    lastBooking = booking
            res = make_response(jsonify(lastBooking),200)
            return res
    return make_response(jsonify({"error":"bad input parameter"}),400)

# get all movies watched by the user
@app.route("/movies/<userid>", methods=['GET'])
def get_movies_for_user(userid):
    for user in users:
        if str(user["id"]) == str(userid):
            bookings = requests.get("http://booking:3201/bookings/" + userid).json()
            movies_id = []
            for booking in bookings["dates"]:
                for movie in booking["movies"]:
                    movies_id.append(movie)
            movies = []
            for movie_id in movies_id:
                movies.append(requests.get("http://movie:3200/movies/" + movie_id).json())
            res = make_response(jsonify(movies),200)
            return res
    return make_response(jsonify({"error":"bad input parameter"}),400)

# get last movie watched by the user
@app.route("/lastmovie/<userid>", methods=['GET'])
def get_last_movie_for_user(userid): #TODO BETTER ALGO
    for user in users:
        if str(user["id"]) == str(userid):
            bookings = requests.get("http://booking:3201/bookings/" + userid).json()
            if len(bookings["dates"]) != 0: 
                movie = requests.get("http://movie:3200/movies/" + bookings["dates"][0]["movies"][0]).json()

                res = make_response(jsonify(movie),200)
                return res
            else:
                return make_response(jsonify({"error":"bad input parameter"}),400)            
    return make_response(jsonify({"error":"bad input parameter"}),400)


# Start the flask server
if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
