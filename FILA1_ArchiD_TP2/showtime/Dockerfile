FROM python:3.8-alpine
WORKDIR /app
COPY requirements.txt /app
COPY showtime_pb2.py /app
COPY showtime_pb2_grpc.py /app
COPY requirements.txt /app
RUN pip install -r requirements.txt
ADD . /app/
CMD ["python","-u","showtime.py"]
