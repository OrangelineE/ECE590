from flask import current_app as app
from .pill import Pill  # Correct import as per your project structure

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
    def get_all():
        sql = '''
            SELECT s.s_slotid, s.s_boxid, p.pillname, s.s_pillnum
            FROM slots s
            LEFT JOIN pills p ON s.s_pillid = p.pill_pillid
        '''
        rows = app.db.execute(sql).fetchall()
        return [Slot(slot_id=row[0], box_id=row[1], pill_name=row[2] if row[2] else '', pill_count=row[3]) for row in rows]

    @staticmethod
    def update_slot(slot_id, pill_name, pill_count):
        pill_id = Pill.get_id_by_name(pill_name) if pill_name else None
        sql = '''
            UPDATE slots
            SET s_pillid = :pill_id, s_pillnum = :pill_count
            WHERE s_slotid = :slot_id
        '''
        app.db.execute(sql, slot_id=slot_id, pill_id=pill_id, pill_count=pill_count)
        app.db.commit()
