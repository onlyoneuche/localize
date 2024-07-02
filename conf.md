systemd config to always restart

"""
[Unit]
Description=FastAPI application
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/localize
ExecStart=/home/ubuntu/localize/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000 --proxy-headers
Restart=always

[Install]
WantedBy=multi-user.target
"""

then run

"""
sudo systemctl daemon-reload
sudo systemctl start fastapi
sudo systemctl enable fastapi
"""


nginx conf to set headers for ip address

"""
server {
    listen 80;
    server_name 54.196.206.175;

    add_header Access-Control-Allow-Headers Content-Type,XFILENAME,XFILECATEGORY,XFILESIZE;
    add_header access-control-allow-headers authorization;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
"""

then grab the ip address from the route

"""
from fastapi import FastAPI, Request

app = FastAPI()

@app.get("/api/hello")
async def say_hello(request: Request):
    client_ip = request.headers.get("X-Real-IP") or request.client.host
    # Your logic here, using the client_ip
    return {"message": f"Hello from {client_ip}"}
"""

run uvicorn with --headers

"""
uvicorn main:app --host 127.0.0.1 --port 8000 --proxy-headers
"""
