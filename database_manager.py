# database_manager.py
import pyodbc

# The DatabaseManager class is responsible for handling all interactions with the SQL database.
# It uses the pyodbc library to connect to the database and perform SQL operations.
class DatabaseManager:
    # Accepts a connection string to establish a connection to the database.
    def __init__(self, connection_string):
        # Establishes a connection to the database using the provided connection string.
        self.conn = pyodbc.connect(connection_string)

    # Inserts college data into the NWCCU_Data table in the database.
    # Accepts a list of dictionaries, where each dictionary represents data for one college.
    def insert_college_data(self, colleges_data):
        # SQL statement for inserting data into the NWCCU_Data table.
        insert_statement = '''
            INSERT INTO NWCCU_Data (Name, Website, Accredited, AccreditationPeriod, Type, StatementURL, MostRecentEvaluation, NextEvaluation, DegreeLevels, PublicSanction, ReasonForAccreditation)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        '''
        # Creates a new cursor object to execute SQL commands.
        cursor = self.conn.cursor()

        # Iterates over each college's data and executes the insert statement for each.
        for college in colleges_data:
            # Converts the boolean 'accredited' field to an integer for SQL BIT type compatibility.
            accredited_int = 1 if college['accredited'] else 0

            # Executes the insert statement with the data for the current college.
            cursor.execute(insert_statement, (
                college['name'],
                college['website'],
                accredited_int,
                college['accreditation_period'],
                college['type'],
                college['statement_url'],
                college['most_recent_evaluation'],
                college['next_evaluation'],
                college['degree_levels'],
                college['public_sanction'],
                college['reason_for_accreditation']
            ))

        # Commits the current transaction to the database.
        self.conn.commit()

        # Closes the cursor and the database connection.
        cursor.close()
        self.conn.close()
