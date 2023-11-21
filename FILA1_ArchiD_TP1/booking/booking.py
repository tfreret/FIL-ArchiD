from flask import Flask, render_template, request, jsonify, make_response
import requests
import json
from werkzeug.exceptions import NotFound

# create flask app
app = Flask(__name__)
PORT = 3201
HOST = '0.0.0.0'


# load bookings from json file
with open('{}/databases/bookings.json'.format("."), "r") as jsf:
   bookings = json.load(jsf)["bookings"]


# API routes
# default route
@app.route("/", methods=['GET'])
def home():
   return "<h1 style='color:blue'>Welcome to the Showtime service!</h1>"

# get all bookings
@app.route("/bookings", methods=['GET'])
def get_json():
    res = make_response(jsonify(bookings), 200)
    return res

# get booking by user id
@app.route("/bookings/<userid>", methods=['GET'])
def get_booking_for_user(userid):
    for booking in bookings:
        if str(booking["userid"]) == str(userid):
            res = make_response(jsonify(booking),200)
            return res
    return make_response(jsonify({"error":"bad input parameter"}),400)
 
# add booking by user id
@app.route("/bookings/<userid>", methods=['POST'])
def add_booking_by_user(userid):
    req = request.get_json()
    
    # call showtime service to get movies
    getMovies = requests.get("http://showtime:3202/showmovies/" + req["date"]).json()
    if getMovies["movies"] == []:
        return make_response(jsonify({"error":"bad input parameter"}),400)
    
    # check if movie exists and add a booking if it does also check if date exists
    if req["movieid"] not in getMovies["movies"]:
        for booking in bookings:
            if str(booking["userid"]) == str(userid):
                for date in booking["dates"]:
                    if date["date"] == req["date"]:
                        if req["movieid"] in date["movies"]:
                            return make_response(jsonify({"error":"an existing item already exists"}),409)
                        date["movies"].append(req["movieid"])
                        return make_response(jsonify(booking),200)
                booking["dates"].append({"date":req["date"],"movies":[req["movieid"]]})
                return make_response(jsonify(booking),200)
    return make_response(jsonify({"error":"bad input parameter"}),400)

# Start the server
if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
