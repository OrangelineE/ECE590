# notification.py
import paho.mqtt.client as mqtt
import json
import atexit
import logging
import time
from datetime import datetime, timedelta
from flask_login import current_user
from .models.reminder import Reminder
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from .models.reminder import Reminder


logging.basicConfig(level=logging.INFO)

MQTT_BROKER_URL = 'broker.emqx.io'
MQTT_BROKER_PORT = 1883
MQTT_TOPIC = 'ECE590_Final_Project_G2/S1/'

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

def send_mqtt_message(slot_data):

    try:
        unacked_publish = set()
        client = mqtt.Client(protocol=mqtt.MQTTv311)

        client.on_connect = on_connect
        client.on_publish = on_publish
        client.connect(MQTT_BROKER_URL, MQTT_BROKER_PORT, 60)
        client.loop_start()

        payload = json.dumps(slot_data)
        
        # Publish and keep track of the returned message info
        msg_info = client.publish(MQTT_TOPIC, payload, qos=1)
        unacked_publish.add(msg_info.mid)  # Keep track of the message ID
        
        # Wait for the message to be published
        msg_info.wait_for_publish()
        
        # Check for any unacknowledged publishes due to race conditions
        while unacked_publish:
            time.sleep(0.1)
            unacked_publish.discard(msg_info.mid)  # Safely remove the acknowledged mid

        logging.info("All messages have been published and acknowledged.")

    except Exception as e:
        logging.error(f"Failed to publish to MQTT broker: {e}")
    finally:
        if client is not None:
            client.loop_stop()
            client.disconnect()


def check_and_send_reminders():
    logging.info("Checking reminders...")
    remove_past_reminders()
    current_time = datetime.now()

    # Check if a user is logged in and authenticated
    if current_user and current_user.is_authenticated:
        reminders = Reminder.get_by_user_id(current_user.patient_id)

        slot_data = {f"Slot{i+1}": False for i in range(5)}  # Assuming 5 slots
        pill_data = {f"PillNum{i+1}": 0 for i in range(5)}

        # Flag to track if any reminders are due
        send_message = False

        for reminder in reminders:
            if reminder.alarm_time - timedelta(minutes=1) <= current_time <= reminder.alarm_time:
                slot_data[f"Slot{reminder.slot_id}"] = True
                pill_data[f"PillNum{reminder.slot_id}"] = reminder.quantity
                send_message = True  # Set the flag since we have a reminder due

        # Only send message if at least one reminder is due
        if send_message:
            payload = {**slot_data, **pill_data}
            send_mqtt_message(payload)
            logging.info("Reminder sent successfully.")
        else:
            logging.info("No reminders due at this time.")
    else:
        logging.warning("No user logged in or user is not authenticated. Skipping reminder check.")

def setup_scheduler(app):
    scheduler = BackgroundScheduler()

    def job_function():
        with app.app_context():
            check_and_send_reminders()

    scheduler.add_job(func=job_function, trigger='interval', minutes=1)
    scheduler.start()

    atexit.register(lambda: scheduler.shutdown(wait=False))
