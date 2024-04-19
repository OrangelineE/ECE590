from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models.slot import Slot  # Ensure correct import path

bp = Blueprint('slots', __name__)

@bp.route('/manage_slots', methods=['GET', 'POST'])
def manage_slots():
    if request.method == 'POST':
        # Process form data and update the database
        for i in range(1, 6):  # Assuming 5 slots
            pill_name = request.form.get(f'pill-name-{i}')
            pill_count = request.form.get(f'pill-count-{i}', type=int, default=0)  # Handle empty fields gracefully
            Slot.update_slot(i, pill_name, pill_count)

        flash('Slot configurations have been saved successfully.', 'success')
        return redirect(url_for('slots.manage_slots'))

    slots = Slot.get_all()  # Retrieve slots data from the database
    return render_template('config.html', slots=slots)
