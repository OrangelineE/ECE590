from flask import render_template, request, Blueprint
from flask_login import login_required, current_user
from .models.slot import Slot
from .models.reminder import Reminder
bp = Blueprint('index', __name__)


@bp.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@bp.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    # Retrieve the boxes associated with the current user
    boxes = current_user.get_boxes()
    
    # Initialize a list to hold all slots from the user's boxes
    slots = []

    # Iterate through each box and collect its slots with pill names
    for box in boxes:
        box_slots = Slot.get_all(box_id=box.box_id)
        slots.extend(box_slots)
    # print(slots)
    reminders = Reminder.get_by_user_id(current_user.patient_id)
    # print(reminders)
    # Pass the collected slots to the template
    return render_template('dashboard.html', slots=slots, reminders_list=reminders)
