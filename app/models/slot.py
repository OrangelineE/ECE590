from flask import current_app as app
from .pill import Pill  

class Slot:
    def __init__(self, slot_id, box_id, pill_id=None, pill_count=0, pill_name=''):
        self.slot_id = slot_id
        self.box_id = box_id
        self.pill_id = pill_id
        self.pill_count = pill_count
        self.pill_name = pill_name

    @staticmethod
    def get_by_id(slot_id):
        sql = '''
            SELECT s_slotid, s_boxid, s_pillid, s_pillnum, p.pillname
            FROM slots s
            JOIN pills p ON s.s_pillid = p.pill_pillid
            WHERE s.s_slotid = :slot_id
        '''
        row = app.db.execute(sql, slot_id=slot_id).fetchone()
        if row:
            return Slot(slot_id=row[0], box_id=row[1], pill_id=row[2], pill_count=row[3], pill_name=row[4])
        return None

    @staticmethod
    def get_by_box_id(box_id):
        sql = '''
            SELECT s_slotid, s_boxid, s_pillid, s_pillnum
            FROM slots
            WHERE s_boxid = :box_id
        '''
        result = app.db.execute(sql, box_id=box_id)
        return [Slot(*row) for row in result.fetchall()]
    
    @staticmethod
    def get_all(box_id=None):
        sql = '''
        SELECT s.s_slotid, s.s_boxid, p.pillname, s.s_pillnum
        FROM slots s
        LEFT JOIN pills p ON s.s_pillid = p.pill_pillid
        '''
        params = {}
        if box_id:
            sql += ' WHERE s.s_boxid = :box_id'
            params['box_id'] = box_id
        sql += ' ORDER BY s.s_slotid ASC'
        results = app.db.execute(sql, **params)
        columns = ["s_slotid", "s_boxid", "pillname", "s_pillnum"]
        fetched_slots = [{columns[i]: row[i] for i in range(len(columns))} for row in results.fetchall()]
        
        # Ensure that there are 5 slots in the list, with data if available
        slots = []
        expected_slot_count = 5
        existing_slots_ids = {slot['s_slotid'] for slot in fetched_slots}
        
        for slot_id in range(1, expected_slot_count + 1):
            if slot_id in existing_slots_ids:
                # Add the existing slot
                slot = next((item for item in fetched_slots if item["s_slotid"] == slot_id), None)
                slots.append(slot)
            else:
                # Create an empty slot placeholder
                slots.append({'s_slotid': slot_id, 's_boxid': box_id, 'pillname': None, 's_pillnum': 0})
        
        return slots

    
    @staticmethod
    def update_slot(slot_id, pill_name, pill_count):
        try:
            pill_id = Pill.get_id_by_name(pill_name) if pill_name else None
            if pill_name and not pill_id:
                # Insert new pill into the pill table and retrieve the new pill_id
                pill_id = Pill.create_new_pill(pill_name)

            # Now update the slot with the pill_id and pill_count
            sql = '''
                UPDATE slots
                SET s_pillid = :pill_id, s_pillnum = :pill_count
                WHERE s_slotid = :slot_id
            '''
            result = app.db.execute(sql, slot_id=slot_id, pill_id=pill_id, pill_count=pill_count)
            app.db.commit()
            return True, "Update successful."
        except Exception as e:
            app.db.rollback()  # Rollback in case of error
            return False, f"Update failed: {e}"

