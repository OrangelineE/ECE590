from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models.slot import Slot  # Ensure correct import path
from flask_login import login_required, current_user
from flask import jsonify
bp = Blueprint('slots', __name__)

@bp.route('/manage_slots', methods=['GET', 'POST'])
@login_required
def manage_slots():
    boxes = current_user.get_boxes()
    # Initialize a list to hold all slots from the user's boxes
    slots = []
    # Iterate through each box and collect its slots with pill names
    for box in boxes:
        box_slots = Slot.get_all(box_id=box.box_id)
        slots.extend(box_slots)
    
    if request.method == 'POST':
        success_messages = []
        error_messages = []
        for slot in slots:
            pill_name = request.form[f'pill-name-{slot["s_slotid"]}']
            pill_count = int(request.form[f'pill-count-{slot["s_slotid"]}'])
            success, message = Slot.update_slot(slot_id=slot['s_slotid'], pill_name=pill_name, pill_count=pill_count)
            if success:
                success_messages.append(message)
            else:
                error_messages.append(message)
        
        for message in success_messages:
            flash(message, 'success')
        for message in error_messages:
            flash(message, 'danger')
        
        return redirect(url_for('slots.manage_slots'))

    else:
        slots = Slot.get_all()  # Retrieve slots data
        return render_template('config.html', slots=slots)

