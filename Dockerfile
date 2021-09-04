FROM python:3
WORKDIR /usr/src/app
COPY . .
RUN pip install flask requests pandas
CMD ["edgify_server.py"]
ENTRYPOINT ["python3"]