import grpc
from concurrent import futures
import booking_pb2
import booking_pb2_grpc
import json
import showtime_pb2
import showtime_pb2_grpc

# GRPC methods
def get_showtime_by_date(stub, date):
    showtime = stub.GetScheduleByDate(showtime_pb2.ScheduleDate(date=date))
    return showtime

# Open a gRPC channel to the showtime service
channel = grpc.insecure_channel('showtime:3202')
stub = showtime_pb2_grpc.ShowtimeStub(channel)

class BookingServicer(booking_pb2_grpc.BookingServicer):

    def __init__(self):
        with open('{}/data/bookings.json'.format("."), "r") as jsf:
            self.db = json.load(jsf)["bookings"]
            
    def GetAllBookings(self, request, context):
        for booking in self.db:
            yield booking_pb2.BookingData(userid=booking['userid'], dates=[booking_pb2.Date(date=date['date'],movies=date['movies']) for date in booking['dates']])

    def GetBookingByUser(self, request, context):
        for booking in self.db:
            if booking['userid'] == request.id: 
                return booking_pb2.BookingData(userid=booking['userid'], dates=[booking_pb2.Date(date=date['date'],movies=date['movies']) for date in booking['dates']])
    
    def PostBookingByUser(self, request, context):
        # call showtime service to get movies
        getMovies = get_showtime_by_date(stub, request.date)
        userid = request.userid
        
        # check if movie exists and add a booking if it does also check if date exists
        if request.movieid in getMovies.movies:
            for booking in self.db:
                print(booking)
                if str(booking["userid"]) == str(userid):
                    for date in booking["dates"]:
                        if date["date"] == request.date:
                            if request.movieid in date["movies"]:
                                return booking_pb2.BookingData(userid="-1",dates=[])
                            date["movies"].append(request.movieid)
                            return booking_pb2.BookingData(userid=userid, dates=[booking_pb2.Date(date=date['date'],movies=date['movies']) for date in booking['dates']])
                    booking["dates"].append({"date":request.date,"movies":[request.movieid]})
                    return booking_pb2.BookingData(userid=userid, dates=[booking_pb2.Date(date=date['date'],movies=date['movies']) for date in booking['dates']])
            self.db.append({"userid": userid, "dates":[{"date":request.date,"movies":[request.movieid]}]})
            return booking_pb2.BookingData(userid=userid, dates=[booking_pb2.Date(date=date['date'],movies=date['movies']) for date in booking['dates']])
        return booking_pb2.BookingData(userid="-1",dates=[])
    
    
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    booking_pb2_grpc.add_BookingServicer_to_server(BookingServicer(), server)
    server.add_insecure_port('[::]:3201')
    server.start()
    print("Booking service server started on port 3201")
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
