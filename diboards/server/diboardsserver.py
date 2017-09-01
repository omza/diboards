from flask import current_app as app

import auth

from database import db
from database.models import User, Board, Subscription, QRcode

import os
from datetime import datetime, timedelta
import pyqrcode

""" Serverside classes and functions

    create_qrcode (Board, size in cm)

    send_email(ReceiverUser, SenderUser, SenderBoard, Template)  
    send_mms(ReceiverUser, SenderUser, SenderBoard, Template)



"""
