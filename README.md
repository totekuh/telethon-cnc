Run in bash:
pip3 install -r requirements.txt
openssl req -new -newkey rsa:4096 -x509 -sha256 -days 365 -nodes -out key.pub -keyout key.priv
uvicorn telethon-cnc-server:app --reload --port 5000 --ssl-keyfile=./key.priv --ssl-certfile=./key.pub
