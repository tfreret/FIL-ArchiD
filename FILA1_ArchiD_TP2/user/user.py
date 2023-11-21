# REST API
from flask import Flask, render_template, request, jsonify, make_response
import requests
import json
import random
from werkzeug.exceptions import NotFound

# CALLING gRPC requests
import grpc
from concurrent import futures
import booking_pb2
import booking_pb2_grpc

app = Flask(__name__)

PORT = 3203
HOST = '0.0.0.0'

# GRPC methods
def get_bookings_by_user(stub, id):
    booking = stub.GetBookingByUser(booking_pb2.UserID(id=id))
    booking_dict = {
            "userid": booking.userid,
            "dates": [
                {"date": date.date, "movies": list(date.movies)}
                for date in booking.dates
            ]
    }
    return booking_dict
def post_booking_by_user(stub, userid, movie, date):
    booking = stub.PostBookingByUser(booking_pb2.NewBooking(userid=userid, date=date, movieid=movie))
    
    booking_dict = {
            "userid": booking.userid,
            "dates": [
                {"date": date.date, "movies": list(date.movies)}
                for date in booking.dates
            ]
    }
    return booking_dict

# Open a gRPC channel to the booking service
channel = grpc.insecure_channel('booking:3201')
stub = booking_pb2_grpc.BookingStub(channel)

# Calling GraphQL requests
def get_movie_with_id(movie_id):

    # GraphQL query structure
    graphql_query = """
      query GetMovieWithID($movieId: String!) {
        movie_with_id(_id: $movieId) {
          id
          title
          rating
          director
        }
      }
    """
    graphql_variables = {"movieId": movie_id}
    # Send the query
    response = requests.post("http://movie:3200/graphql", json={"query": graphql_query, "variables": graphql_variables})

    if response.status_code == 200:
        movie_data = response.json().get("data", {}).get("movie_with_id", {})
        return movie_data
    return Error("Movie not found")


# load users from json file
with open('{}/data/users.json'.format("."), "r") as jsf:
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
            # get bookings from the user
            getBookings = get_bookings_by_user(stub, str(userid))
            return make_response(jsonify(getBookings),200)
    return make_response(jsonify({"error":"bad input parameter"}),400)

# add booking for user
@app.route("/booking/<userid>", methods=['POST'])
def add_booking(userid):
    for user in users:
        if str(user["id"]) == str(userid):
            req = request.get_json()
            # add a booking to a user
            getBookings = post_booking_by_user(stub, userid, req["movieid"], req["date"])
            print(getBookings)
            res = make_response(jsonify(getBookings),200)
            return res
    return make_response(jsonify({"error":"bad input parameter"}),400)

# get last booking from a user
@app.route("/lastbooking/<userid>", methods=['GET'])
def get_last_booking_for_user(userid):
    for user in users:
        if str(user["id"]) == str(userid):
            # get bookings from the user
            getBookings = get_bookings_by_user(stub, str(userid))
            lastBooking = ""
            for booking in getBookings["dates"]:
                print(booking)
                if lastBooking == "" or int(lastBooking["date"]) < int(booking["date"]) :
                    lastBooking = booking
            res = make_response(jsonify(lastBooking),200)
            return res
    return make_response(jsonify({"error":"bad input parameter"}),400)

# get all movies from an user
@app.route("/movies/<userid>", methods=['GET'])
def get_movies_for_user(userid):
    for user in users:
        if str(user["id"]) == str(userid):
            # get bookings from the user
            bookings = get_bookings_by_user(stub, str(userid))
            movies_id = []
            for booking in bookings["dates"]:
                for movie in booking["movies"]:
                    movies_id.append(movie)
            movies = []
            for movie_id in movies_id:
                # get movie with graphql request
                movies.append(get_movie_with_id(movie_id))
            res = make_response(jsonify(movies),200)
            return res
    return make_response(jsonify({"error":"bad input parameter"}),400)

# get last movie from a user
@app.route("/lastMovie/<userid>", methods=['GET'])
def get_last_movie_for_user(userid):
    for user in users:
        if str(user["id"]) == str(userid):
            # get bookings from the user
            bookings = get_bookings_by_user(stub, str(userid))
            if len(bookings["dates"]) != 0:
                print(bookings["dates"][0]["movies"][0])
                # get last movie with graphql request
                movie = get_movie_with_id(bookings["dates"][0]["movies"][0])
                print(movie)
                res = make_response(jsonify(movie),200)
                return res
            else:
                return make_response(jsonify({"error":"bad input parameter"}),400)            
    return make_response(jsonify({"error":"bad input parameter"}),400)

if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)