from datetime import datetime, timedelta
from flask_login import login_required, current_user
from flask import request, flash, redirect, url_for, Blueprint, render_template, abort
from .models.reminder import Reminder
from flask import jsonify
from .models.slot import Slot
import traceback

bp = Blueprint('reminders', __name__)

def get_user_slots():
    # Assuming `get_boxes` returns a list of box objects for the current user
    boxes = current_user.get_boxes()
    # Initialize a list to hold all slots from the user's boxes
    user_slots = []
    # Iterate through each box and collect its slots with pill names
    for box in boxes:
        box_slots = Slot.get_all(box_id=box.box_id)
        user_slots.extend(box_slots)
    return user_slots



@bp.route('/add_reminder', methods=['POST'])
@login_required
def add_reminder():
    try:
        # Assume data is sent as JSON, parse it from request
        data = request.get_json()
        slot_id = data['slot_id']
        alarm_time_str = data['alarm_time']
        frequency_str = data['frequency']
        quantity = int(data['quantity'])
        
        # Parse the alarm time using datetime
        alarm_time = datetime.strptime(alarm_time_str, '%Y-%m-%dT%H:%M:%S')  # Adjust the format if necessary

        # Assuming Reminder.create() handles database interaction
        reminder_id = Reminder.create(slot_id, alarm_time, frequency_str, quantity)
        
        # Return success response
        return jsonify({
            'status': 'success',
            'message': f'Reminder added with ID {reminder_id}'
        }), 200
    except Exception as e:
        # Log the full traceback to help debug the error
        traceback.print_exc()
        
        # Return JSON error message
        return jsonify({
            'status': 'error',
            'message': f'Failed to add reminder: {str(e)}'
        }), 400



@bp.route('/delete_reminder/<int:reminder_id>', methods=['POST'])
@login_required
def delete_reminder(reminder_id):
    try:
        deleted = Reminder.delete(reminder_id)
        if deleted:
            flash('Reminder successfully deleted.', 'success')
        else:
            flash('Reminder could not be deleted.', 'warning')
    except Exception as e:
        flash(f"Error deleting reminder: {str(e)}", 'danger')
    
    return redirect(url_for('reminders.display_reminders'))

@bp.route('/display_reminders')
@login_required
def display_reminders():
    reminders = Reminder.get_by_user_id(current_user.patient_id)
    slots = get_user_slots()  # Use the revised function to get slots
    # print(slots)
    # print(reminders)
    return render_template('reminder.html', reminders=reminders, slot_info=slots)

@bp.app_template_filter('dateformat')
def dateformat(value, format='%H:%M / %d-%m-%Y'):
    """Format a date string to the given format."""
    if value is None:
        return ""
    try:
        # If the value is a string, parse it to datetime
        if isinstance(value, str):
            value = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S')
        # Now format the datetime object
        return value.strftime(format)
    except ValueError:
        # If there is an error parsing the string, return it as is
        return value
    
@bp.app_template_filter('to_hours')
def to_hours(td):
    if isinstance(td, timedelta):
        total_seconds = int(td.total_seconds())
        hours = total_seconds // 3600
        return f"{hours} hours"
    else:
        return "Invalid duration"