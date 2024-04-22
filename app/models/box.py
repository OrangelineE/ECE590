from flask import current_app as app

class Box:
    def __init__(self, box_id, patient_id):
        self.box_id = box_id
        self.patient_id = patient_id

    @staticmethod
    def create(patient_id):
        sql = '''
            INSERT INTO boxes (b_patientid)
            VALUES (:patient_id)
            RETURNING b_boxid
        '''
        result = app.db.execute(sql, patient_id=patient_id)
        box_id = result.fetchone()[0]
        return box_id

    @staticmethod
    def get_by_patient_id(patient_id):
        sql = '''
            SELECT b_boxid, b_patientid
            FROM boxes
            WHERE b_patientid = :patient_id
        '''
        result = app.db.execute(sql, patient_id=patient_id)
        return [Box(*row) for row in result.fetchall()]