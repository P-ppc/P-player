#!/usr/bin/env python
# -*- coding: utf-8 -*-
from app import app
from werkzeug.contrib.fixers import ProxyFix

app.wsgi_app = ProxyFix(app.wsgi_app)

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5000, debug = True, threaded = False)
else:
    pass
