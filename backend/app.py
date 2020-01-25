from datetime import datetime, timedelta
from os import path, getcwd
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text, functions
from common.config import conf_database, conf_debug
from common.models import Base, Device, Service, Fingerprint, Heartbeat, Vulnerability
from common.utils import acquire_file_lock
from .serializers import *

# count heartbeats of a specific device for every hour of the day
HEARTBEATS_HOURS_QUERY = """
SELECT strftime('%H', timestamp), COUNT(1)
FROM heartbeats
WHERE device_id = :device_id AND timestamp >= :timestamp
GROUP BY strftime('%H', timestamp)
"""

# count heartbeats of a specific device for every weekday
HEARTBEATS_WEEKDAYS_QUERY = """
SELECT strftime('%w', timestamp), COUNT(1)
FROM heartbeats
WHERE device_id = :device_id AND timestamp >= :timestamp
GROUP BY strftime('%w', timestamp)
"""

# query the services for a specific device from within the last 24h
# (duplicates are removed)
SERVICES_QUERY = """
SELECT *
FROM services
WHERE id IN (
    SELECT MAX(id)
    FROM services
    WHERE device_id = :device_id AND timestamp >= :timestamp
    GROUP BY type, address
)
ORDER BY type, address
"""

# query the fingerprints for a specific device from within the last 24h
# (duplicates are removed)
FINGERPRINTS_QUERY = """
SELECT *
FROM fingerprints
WHERE id IN (
    SELECT MAX(id)
    FROM fingerprints
    WHERE device_id = :device_id AND timestamp >= :timestamp
    GROUP BY type
)
ORDER BY type
"""

# query the vulnerabilities for a specific device from within the last 24h
# (duplicates are removed)
VULNERABILITIES_QUERY = """
SELECT *
FROM vulnerabilities
WHERE id IN (
    SELECT MAX(id)
    FROM vulnerabilities
    WHERE device_id = :device_id AND timestamp >= :timestamp
    GROUP BY type
)
ORDER BY type
"""

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + path.join(getcwd(), conf_database)

with acquire_file_lock(path.join(getcwd(), conf_database) + ".lock") as lock:
    db = SQLAlchemy(app)
    db.create_all()

# allow all origins when debugging
# from https://stackoverflow.com/a/45818284
@app.after_request
def after_request(response):
    header = response.headers
    if conf_debug:
        header["Access-Control-Allow-Origin"] = "*"
        header["Access-Control-Allow-Methods"] = "GET, POST"
        header["Access-Control-Allow-Headers"] = "Content-Type"
    return response

@app.route("/api/devices", methods=["GET"])
def get_devices():
    devices = db.session.query(Device) \
        .all()

    return {
        "devices": list(map(serialize_device, devices))
    }

@app.route("/api/devices/<device_id>", methods=["GET"])
def get_device(device_id):
    start_ts = datetime.now() - timedelta(hours=24)
    heartbeat_ts = datetime.now() - timedelta(weeks=4)
    
    device = db.session.query(Device).get(device_id)

    services = db.session.query(Service) \
        .from_statement(text(SERVICES_QUERY)) \
        .params(device_id = device_id, timestamp = start_ts)
    
    fingerprints = db.session.query(Fingerprint) \
        .from_statement(text(FINGERPRINTS_QUERY)) \
        .params(device_id = device_id, timestamp = start_ts)

    vulnerabilities = db.session.query(Vulnerability) \
        .from_statement(text(VULNERABILITIES_QUERY)) \
        .params(device_id = device_id, timestamp = start_ts)

    last_heartbeat = db.session.query(Heartbeat) \
        .filter(Heartbeat.device_id == device.id) \
        .order_by(Heartbeat.timestamp.desc()) \
        .first()

    hours_heartbeats = db.session.execute(text(HEARTBEATS_HOURS_QUERY), \
        {"device_id": device_id, "timestamp": heartbeat_ts}).fetchall()
    activity_hours = [0] * 24
    for (hour, count) in hours_heartbeats:
        activity_hours[int(hour)] = count
    
    weekdays_heartbeats = db.session.execute(text(HEARTBEATS_WEEKDAYS_QUERY), \
        {"device_id": device_id, "timestamp": heartbeat_ts}).fetchall()
    activity_weekdays = [0] * 7
    for (weekday, count) in weekdays_heartbeats:
        activity_weekdays[int(weekday)] = count

    return serialize_device_details(
        device, services, fingerprints, vulnerabilities,
        last_heartbeat, activity_hours, activity_weekdays)

@app.route("/api/devices/<device_id>", methods=["POST"])
def update_device(device_id):
    if "label" in request.json:
        label = request.json["label"]

        device = db.session.query(Device).get(device_id)
        device.label = label
        db.session.commit()
    
    return {}
