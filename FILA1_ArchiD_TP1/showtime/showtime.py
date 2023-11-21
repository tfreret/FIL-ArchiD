from flask import Flask, render_template, request, jsonify, make_response
import json
from werkzeug.exceptions import NotFound

# create flask app
app = Flask(__name__)
PORT = 3202
HOST = '0.0.0.0'

# load schedules from json file
with open('{}/databases/times.json'.format("."), "r") as jsf:
   schedules = json.load(jsf)["schedule"]


# API routes
# default route
@app.route("/", methods=['GET'])
def home():
   return "<h1 style='color:blue'>Welcome to the Showtime service!</h1>"

# get all schedules
@app.route("/showtimes", methods=['GET'])
def get_json():
    res = make_response(jsonify(schedules), 200)
    return res

# get schedule by date
@app.route("/showmovies/<date>", methods=['GET'])
def get_schedule_by_date(date):
    for schedule in schedules:
        if str(schedule["date"]) == str(date):
            res = make_response(jsonify(schedule),200)
            return res
    return make_response(jsonify({"error":"bad input parameter"}),400)


# Start the server
if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
