from routes import app
from services.auth import check_for_token
from flask import Flask, jsonify, request, session, render_template, make_response
import json
from bson import json_util, ObjectId
import services.machine as sm
