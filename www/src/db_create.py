#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app import db

if __name__ == '__main__':
    try:
        db.drop_all()
    except:
        pass
    db.create_all()
