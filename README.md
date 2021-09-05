move to edgify folder
docker build -t edgify_docker .
sudo docker run -it edgify-docker edgify_server.py - to execute the REST server


POST: 127.0.0.1:5000/api/trade
add file as a key and add the CSV as attachment.
For your ease, use the edgify.csv in the folder.

