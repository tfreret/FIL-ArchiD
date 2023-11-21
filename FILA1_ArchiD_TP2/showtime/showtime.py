import grpc
from concurrent import futures
import showtime_pb2
import showtime_pb2_grpc
import json

class ShowtimeServicer(showtime_pb2_grpc.ShowtimeServicer):

    # load data from json file in constructor
    def __init__(self):
        with open('{}/data/times.json'.format("."), "r") as jsf:
            self.db = json.load(jsf)["schedule"]

    # GRPC methods implementation
    # Get schedule by date
    def GetScheduleByDate(self, request, context):
        for schedule in self.db:
            if schedule["date"] == request.date:
                return showtime_pb2.Schedule(date=schedule["date"],movies=schedule["movies"])
    
    # Get all schedules
    def GetAllSchedules(self, request, context):
        for schedule in self.db:
            yield showtime_pb2.Schedules(schedule=[showtime_pb2.Schedule(movies=schedule["movies"], date=schedule["date"])])

# Start the gRPC server
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    showtime_pb2_grpc.add_ShowtimeServicer_to_server(ShowtimeServicer(), server)
    server.add_insecure_port('[::]:3202')
    server.start()
    print("Showtime service server started on port 3202")
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
