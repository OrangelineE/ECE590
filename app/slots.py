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
        # Process form data and update the database
        for i in range(1, 6):  # Assuming 5 slots
            pill_name = request.form.get(f'pill-name-{i}')
            pill_count = request.form.get(f'pill-count-{i}', type=int, default=0)  # Handle empty fields gracefully
            Slot.update_slot(i, pill_name, pill_count)

        flash('Slot configurations have been saved successfully.', 'success')
        return redirect(url_for('slots.manage_slots'))

    return render_template('config.html', slots=slots)

