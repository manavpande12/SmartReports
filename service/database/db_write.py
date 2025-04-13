from database.db_connect import ConnectDB

class WriteDB:
    def __init__(self, db_params):
        self.db_params = db_params
        self.conn = None
        self.cursor = None

    def open_connection(self):
        """Open database connection"""
        db = ConnectDB(**self.db_params)
        self.conn = db.connect()
        if self.conn:
            self.cursor = self.conn.cursor()

    def create_table(self):
        """Create table if not exists"""
        self.open_connection()
        if self.cursor:
            query = """
            CREATE TABLE IF NOT EXISTS batch_data (
                batch_no SERIAL PRIMARY KEY,
                start_time TIME,
                end_time TIME,
                date DATE,
                set_qty INT,
                act_qty INT,
                destination VARCHAR(255),
                error INT GENERATED ALWAYS AS (act_qty - set_qty) STORED
            )
            """
            self.cursor.execute(query)
            self.conn.commit()
            print("Table ensured in PostgreSQL")
            self.close_connection()

    def insert_data(self, start_time, end_time, date, set_qty, act_qty, destination):
        """Insert batch data into the table"""
        self.open_connection()
        if self.cursor:
            query = """
            INSERT INTO batch_data (start_time, end_time, date, set_qty, act_qty, destination)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            values = (start_time, end_time, date, set_qty, act_qty, destination)
            self.cursor.execute(query, values)
            self.conn.commit()
            print("Batch data inserted into PostgreSQL")
            self.close_connection()

    def close_connection(self):
        """Close database connection"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        print("Database connection closed")
