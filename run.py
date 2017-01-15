# -*- Mode: Python; coding: utf-8 -*-
from app import app as application
import initialize_db

application.run(debug=True, port=8090)