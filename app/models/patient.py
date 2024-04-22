from flask import current_app as app
from sqlalchemy import text
from sqlalchemy.orm import scoped_session, sessionmaker
from .box import Box

class Patient:
    def __init__(self, patient_id, email, name, password, age):
        self.patient_id = patient_id
        self.email = email
        self.name = name
        self.password = password
        self.age = age

    # Define methods required by Flask-Login
    def get_id(self):
        return str(self.patient_id)

    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False
    
    def get_boxes(self):
        return Box.get_by_patient_id(self.patient_id)

    @staticmethod
    def create(email, name, password, age):
        sql = '''
            INSERT INTO patients (p_email, p_name, p_password, p_age)
            VALUES (:email, :name, :password, :age)
            RETURNING p_patientid
        '''
        result = app.db.execute(sql, email=email, name=name, password=password, age=age)
        patient_id = result.fetchone()[0]
        return patient_id

    @staticmethod
    def get_by_email(email):
        sql = '''
            SELECT p_patientid, p_email, p_name, p_password, p_age
            FROM patients
            WHERE p_email = :email
        '''
        result = app.db.execute(text(sql), {'email': email})
        row = result.fetchone()
        return Patient(*row) if row else None

    @staticmethod
    def get_by_id(patient_id):
        sql = '''
            SELECT p_patientid, p_email, p_name, p_password, p_age
            FROM patients
            WHERE p_patientid = :patient_id
        '''
        result = app.db.execute(sql, patient_id=patient_id)
        row = result.fetchone()
        return Patient(*row) if row else None

    @staticmethod
    def update(patient_id, email, name, password, age):
        sql = '''
            UPDATE patients
            SET p_email = :email, p_name = :name, p_password = :password, p_age = :age
            WHERE p_patientid = :patient_id
        '''
        app.db.execute(sql, email=email, name=name, password=password, age=age, patient_id=patient_id)

    @staticmethod
    def delete(patient_id):
        sql = '''
            DELETE FROM patients
            WHERE p_patientid = :patient_id
        '''
        app.db.execute(sql, {'patient_id': patient_id})

    @staticmethod
    def authenticate(email, password):
        sql = "SELECT * FROM patients WHERE p_email = :email AND p_password = :password"
        result = app.db.execute(sql, email=email, password=password)
        row = result.fetchone()
        if row:
            return Patient(*row)
        else:
            return None
