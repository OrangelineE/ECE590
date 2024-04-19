from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user

# # Assuming you have models for Slots, Pills, and Reminders
# from .models import Slot, Pill, Reminder

bp = Blueprint('reminders', __name__)

# @bp.route('/add-reminder', methods=['GET', 'POST'])
# # @login_required
# def add_reminder():
#     if request.method == 'POST':
#         # Retrieve form data
#         slot_data = request.form.getlist('slot')
#         doses_data = request.form.getlist('doses')
#         pills_per_dose_data = request.form.getlist('pills-per-dose')
#         times_data = request.form.getlist('time')

#         # Assuming there are 5 slots for the pillbox
#         for i in range(5):
#             slot_id = int(slot_data[i])
#             doses = int(doses_data[i])
#             pills_per_dose = int(pills_per_dose_data[i])
#             time = times_data[i]

#             # Create or update the Reminder in the database
#             # This is a simplistic approach; you'll need to adapt it to how your models and database are set up.
#             # Error handling and data validation should also be implemented.

#             # Fetch the Slot based on slot_id and current_user
#             slot = Slot.query.filter_by(id=slot_id, user_id=current_user.id).first()
            
#             # Create a new reminder object and add it to the session
#             # Here we are creating a single reminder for simplicity, but you might want to create multiple
#             # based on the doses per day.
#             reminder = Reminder(slot_id=slot.id, alarm_time=time, quantity=pills_per_dose)
#             db.session.add(reminder)
        
#         # Commit all reminders to the database
#         db.session.commit()
        
#         flash('Reminders have been set successfully.', 'success')
#         return redirect(url_for('index'))
#     else:
#         # GET request: Display the form
#         slots = Slot.query.filter_by(user_id=current_user.id).all()
#         return render_template('reminder.html', slots=slots)

# A mock function to simulate database query
def mock_query_slots():
    # Simulating slots with just IDs and names
    return [{'id': i, 'name': f'Pill {i}'} for i in range(1, 6)]

@bp.route('/reminder', methods=['GET', 'POST'])
# @login_required
def reminder():
    if request.method == 'POST':
        # Mock form data handling
        slot_data = request.form.getlist('slot')
        doses_data = request.form.getlist('doses')
        pills_per_dose_data = request.form.getlist('pills-per-dose')
        times_data = request.form.getlist('time')

        reminders = []

        for i in range(len(slot_data)):
            reminders.append({
                'slot_id': slot_data[i],
                'doses': doses_data[i],
                'pills_per_dose': pills_per_dose_data[i],
                'time': times_data[i]
            })

        # Normally, you would commit to the database here, but instead, we'll just print or flash the reminders
        for reminder in reminders:
            print(reminder)  # or use flash(f"Reminder for slot {reminder['slot_id']} added.", 'info')

        flash('Reminders have been set successfully.', 'success')
        return redirect(url_for('index.index'))
    else:
        # GET request: Display the form
        slots = mock_query_slots()
        return render_template('reminder.html', slots=slots)

# Add mock session handling if you want to keep track of reminders in the session
@bp.route('/clear-reminders', methods=['POST'])
def clear_reminders():
    bp.session.pop('reminders', None)
    flash('All reminders have been cleared.', 'success')
    return redirect(url_for('index.index'))
