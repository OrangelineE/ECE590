# notification.py
import paho.mqtt.client as mqtt
import json
import atexit
import logging
import time
from datetime import datetime, timedelta
from flask_login import current_user, login_required
from .models.reminder import Reminder
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from .models.reminder import Reminder
from flask import current_app
from .models.patient import Patient
import os

logging.basicConfig(level=logging.DEBUG)

MQTT_BROKER_URL = 'broker.emqx.io'
MQTT_BROKER_PORT = 1883
MQTT_TOPIC = 'ECE590_Final_Project_G2/S1/'

def setup_scheduler(app):
    if os.environ.get("SCHEDULER_RUNNING"):
        logging.warning("Scheduler already running.")
        return

    scheduler = BackgroundScheduler()

    def job_function():
        logging.info("Job function is running...")
        with app.app_context():
            check_and_send_reminders()

    job = scheduler.add_job(func=job_function, trigger='interval', minutes=1, id='unique_job_id')
    scheduler.start()
    os.environ["SCHEDULER_RUNNING"] = "True"

    logging.info(f"Job {job.id} scheduled to run every {job.trigger.interval_length} seconds.")

def remove_past_reminders():
    current_time = datetime.now()
    reminders = Reminder.get_all()  # This function would need to be defined in your Reminder model

    for reminder in reminders:
        if reminder.alarm_time < current_time:
            reminder.delete(reminder.reminder_id)

def on_connect(client, userdata, flags, rc):
    logging.info(f"Connected to MQTT broker with result code {rc}")

def on_publish(client, userdata, mid):
    logging.info(f"Message {mid} has been published.")

client = None  # Define this at a higher scope, such as module level

def get_mqtt_client():
    global client
    if client is None or not client.is_connected():
        client = mqtt.Client(protocol=mqtt.MQTTv311)
        client.on_connect = on_connect
        client.on_publish = on_publish
        client.connect(MQTT_BROKER_URL, MQTT_BROKER_PORT, 60)
        client.loop_start()
    return client

def send_mqtt_message(slot_data):
    try:
        client = get_mqtt_client()
        payload = json.dumps(slot_data)
        msg_info = client.publish(MQTT_TOPIC, payload, qos=1)
        msg_info.wait_for_publish()
        logging.info("Message published successfully.")
    except Exception as e:
        logging.error(f"Failed to publish to MQTT broker: {e}")
    finally:
        client.loop_stop()  # Consider when and how to stop the loop appropriately
        client.disconnect()

def check_and_send_reminders():
    logging.info("Checking reminders for all users...")
    remove_past_reminders()
    current_time = datetime.now()
    
    all_patients = Patient.get_all_patients()  # Ensure this is correctly fetching all patient objects
    if not all_patients:
        logging.warning("No patients found. Skipping reminder checks.")
        return

    for patient in all_patients:
        user_reminders = Reminder.get_by_user_id(patient.patient_id)
        slot_data = {f"Slot{i+1}": False for i in range(5)}  # Assuming 5 slots
        pill_data = {f"PillNum{i+1}": 0 for i in range(5)}

        send_message = False  # Flag to track if any reminders are due

        if not user_reminders:
            logging.info(f"No reminders for user {patient.patient_id}")
            continue

        for slot_id, reminders in user_reminders.items():
            if reminders is not None:
                for reminder in reminders:
                    # Convert reminder['alarm_time'] from string to datetime
                    reminder_alarm_time = datetime.strptime(reminder['alarm_time'], '%Y-%m-%dT%H:%M:%S')
                    if reminder_alarm_time - timedelta(minutes=1) <= current_time < reminder_alarm_time:
                        slot_data[f"Slot{reminder['slot_id']}"] = True
                        pill_data[f"PillNum{reminder['slot_id']}"] = reminder['quantity']
                        send_message = True

        if send_message:
            payload = {**slot_data, **pill_data}
            print(payload) 
            send_mqtt_message(payload)
            logging.info("Reminder sent successfully.")

