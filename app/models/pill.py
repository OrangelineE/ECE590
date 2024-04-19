from flask import current_app as app

class Pill:
    def __init__(self, pill_id, pill_name, description):
        self.pill_id = pill_id
        self.pill_name = pill_name
        self.description = description

    @staticmethod
    def get_by_id(pill_id):
        sql = '''
            SELECT pill_pillid, pillname, pill_description
            FROM pills
            WHERE pill_pillid = :pill_id
        '''
        row = app.db.execute(sql, pill_id=pill_id).fetchone()
        return Pill(*row) if row else None

    @staticmethod
    def get_id_by_name(pill_name):
        sql = '''
            SELECT pill_pillid
            FROM pills
            WHERE pillname = :pill_name
        '''
        row = app.db.execute(sql, pill_name=pill_name).fetchone()
        if row:
            return row[0]
        else:
            return Pill.add_new_pill(pill_name)

    @staticmethod
    def add_new_pill(pill_name):
        sql = '''
            INSERT INTO pills (pillname)
            VALUES (:pill_name)
            RETURNING pill_pillid
        '''
        result = app.db.execute(sql, pill_name=pill_name).fetchone()
        return result[0] if result else None

    @staticmethod
    def get_all():
        sql = '''
            SELECT pill_pillid, pillname, pill_description
            FROM pills
        '''
        rows = app.db.execute(sql)
        return [Pill(*row) for row in rows]

    @staticmethod
    def add_pill(pill_id, pill_name, description):
        sql = '''
            INSERT INTO pills (pill_pillid, pillname, pill_description)
            VALUES (:pill_id, :pill_name, :description)
        '''
        app.db.execute(sql, pill_id=pill_id, pill_name=pill_name, description=description)
        app.db.commit()

    @staticmethod
    def update_pill(pill_id, pill_name, description):
        sql = '''
            UPDATE pills
            SET pillname = :pill_name, pill_description = :description
            WHERE pill_pillid = :pill_id
        '''
        app.db.execute(sql, pill_id=pill_id, pill_name=pill_name, description=description)
        app.db.commit()

    @staticmethod
    def delete_pill(pill_id):
        sql = '''
            DELETE FROM pills
            WHERE pill_pillid = :pill_id
        '''
        app.db.execute(sql, pill_id=pill_id)
        app.db.commit()
