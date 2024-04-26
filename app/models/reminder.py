from flask import current_app as app
from sqlalchemy import text
class Reminder:
    def __init__(self, reminder_id, slot_id, alarm_time, frequency, quantity):
        self.reminder_id = reminder_id
        self.slot_id = slot_id
        self.alarm_time = alarm_time
        self.frequency = frequency
        self.quantity = quantity

    def to_dict(self):
        return {
            'reminder_id': self.reminder_id,
            'slot_id': self.slot_id,
            'alarm_time': self.alarm_time.isoformat(),  # Convert datetime to string
            'frequency': self.frequency,
            'quantity': self.quantity
        }

    @staticmethod
    def create(slot_id, alarm_time, frequency, quantity):
        sql = '''
            INSERT INTO reminders (r_slotid, r_alarm, r_frequency, r_quantity)
            VALUES (:slot_id, :alarm_time, :frequency, :quantity)
            RETURNING r_reminderid
        '''
        result = app.db.execute(sql, slot_id=slot_id, alarm_time=alarm_time, frequency=frequency, quantity=quantity)
        reminder_id = result.fetchone()[0]
        return reminder_id

    @staticmethod
    def get_by_slot_id(slot_id):
        sql = '''
            SELECT r_reminderid, r_slotid, r_alarm, r_frequency, r_quantity
            FROM reminders
            WHERE r_slotid = :slot_id
        '''
        result = app.db.execute(sql, slot_id=slot_id)
        return [Reminder(*row) for row in result.fetchall()]

    @staticmethod
    def get_all():
        sql = '''
            SELECT r_reminderid, r_slotid, r_alarm, r_frequency, r_quantity
            FROM reminders
        '''
        result = app.db.execute(sql)
        return [Reminder(*row) for row in result.fetchall()]

    @staticmethod
    def delete(reminder_id):
        try:
            # Prepare your SQL statement wrapped in text() for SQLAlchemy processing
            sql = text('''
                DELETE FROM reminders
                WHERE r_reminderid = :reminder_id
            ''')

            # Execute the SQL statement with a named placeholder
            result = app.db.session.execute(sql, {'reminder_id': reminder_id})
            app.db.session.commit()  # Commit the transaction to finalize the deletion
            return result.rowcount  # Return the number of rows affected
        except Exception as e:
            app.db.session.rollback()  # Roll back the transaction on error
            app.logger.error(f"Error deleting reminder: {e}")
            return 0

    @staticmethod
    def update(reminder_id, alarm_time=None, frequency=None, quantity=None):
        updates = []
        params = {'reminder_id': reminder_id}
        if alarm_time:
            updates.append("r_alarm = :alarm_time")
            params['alarm_time'] = alarm_time
        if frequency:
            updates.append("r_frequency = :frequency")
            params['frequency'] = frequency
        if quantity:
            updates.append("r_quantity = :quantity")
            params['quantity'] = quantity

        if updates:
            sql = f'''
                UPDATE reminders
                SET {', '.join(updates)}
                WHERE r_reminderid = :reminder_id
            '''
            try:
                result = app.db.execute(sql, **params)
                app.db.session.commit()
                return result.rowcount
            except Exception as e:
                app.db.session.rollback()
                app.logger.error(f"Error updating reminder: {e}")
                return 0

    @staticmethod
    def get_by_user_id(user_id):
        sql = '''
            SELECT rem.r_reminderid, rem.r_slotid, rem.r_alarm, rem.r_frequency, rem.r_quantity
            FROM reminders rem
            JOIN slots s ON rem.r_slotid = s.s_slotid
            JOIN boxes b ON s.s_boxid = b.b_boxid
            WHERE b.b_patientid = :user_id
        '''
        result = app.db.execute(sql, user_id=user_id)
        fetched_reminders = result.fetchall()

        # Initialize a dictionary to store reminders, divided by slots
        slot_reminders = {slot_id: [] for slot_id in range(1, 6)}

        # Populate the dictionary with fetched reminders
        for reminder_row in fetched_reminders:
            slot_id = reminder_row[1]
            reminder = Reminder(*reminder_row)  # Create a Reminder object
            slot_reminders[slot_id].append(reminder.to_dict())  # Append the dictionary representation

        # Replace empty lists with None for slots that have no reminders
        for slot_id, reminders in slot_reminders.items():
            if not reminders:  # If the list is empty
                slot_reminders[slot_id] = None  # Set to None

        return slot_reminders
