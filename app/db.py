from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker

class DB:
    _instance = None

    def __init__(self, app):
        self.engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'],
                                    execution_options={"isolation_level": "SERIALIZABLE"})
        self.session = scoped_session(sessionmaker(bind=self.engine))

    def get_instance(self):
        return self

    def execute(self, sqlstr, **kwargs):
        """
        Executes a SQL statement using a transaction.
        `sqlstr` should be a string that may include placeholders for parameters.
        `kwargs` are the parameters to be substituted into the `sqlstr`.
        
        Returns the result of the query or the number of affected rows for non-query SQL statements.
        """
        with self.engine.begin() as conn:
            result = conn.execute(text(sqlstr), kwargs)
            # if result.returns_rows:
            #     return result.fetchall()
            # else:
            #     return result.rowcount

            if "select" in sqlstr.lower() or "returning" in sqlstr.lower():
                return result  # Returns the result proxy for further fetching in the calling function
            else:
                return result.rowcount  # Returns count of affected rows for non-SELECT statements
    
    def commit(self):
        if self.session:
            self.session.commit()
            self.session.close()
