# -*- Mode: Python; coding: utf-8 -*-
from app import app as application
# import initialize_db
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip = s.getsockname()[0]

if str(ip) == '192.168.20.5':
    application.run(debug=True, host=ip, port=8090)
    
else:
    application.run(debug=True, host="127.0.0.1", port=8090)
