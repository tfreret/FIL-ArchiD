FROM python:3.8-alpine
WORKDIR /app
COPY requirements.txt /app
COPY booking_pb2.py /app
COPY booking_pb2_grpc.py /app
COPY showtime_pb2.py /app
COPY showtime_pb2_grpc.py /app
RUN pip install -r requirements.txt
ADD . /app/
CMD ["python","-u","booking.py"]
