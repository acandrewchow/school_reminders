import os
import sqlite3
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime

# Creates a table containing all of the due dates for a given assignment in a course
# Run the script to reset the DB
def create_due_dates_table():
    try:
        conn = sqlite3.connect("due_dates.db")
        cursor = conn.cursor()
        
        cursor.execute("DROP TABLE IF EXISTS due_dates")
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS due_dates (
                            id INTEGER PRIMARY KEY,
                            course TEXT,
                            task TEXT,
                            assignment_type TEXT,
                            due_date DATETIME,
                            weight REAL
                        )''')
        conn.commit()
        print("Due Dates Table created or reset successfully")
    except sqlite3.Error as e:
        print("Error creating or resetting table:", e)
    finally:
        conn.close()

def insert_data_from_spreadsheet(file_path):
    try:
        conn = sqlite3.connect("due_dates.db")
        cursor = conn.cursor()

        df = pd.read_csv(file_path) 

        for index, row in df.iterrows():
            course = row['course']
            task = row['task']
            assignment_type = row['assignment_type']
            due_date_str = row['due_date'] # 2023-09-08 13:05:00
            weight = row['weight']

            # Convert due_date_str to a datetime object
            due_date = datetime.strptime(due_date_str, "%Y-%m-%d %H:%M:%S")

            cursor.execute("INSERT INTO due_dates (course, task, assignment_type, due_date, weight) VALUES (?, ?, ?, ?, ?)",
                           (course, task, assignment_type, due_date, weight))

        conn.commit()
        print("Dates have been added")
    except sqlite3.Error as e:
        print("Error inserting data:", e)
    except Exception as e:
        print("Error sending SMS:", e)
    finally:
        conn.close()

if __name__ == "__main__":
    if len(os.sys.argv) != 2:
        print("python3 reminder.py <csv_file>")
        exit(1)

    load_dotenv()

    csv_file = os.sys.argv[1]

    create_due_dates_table()

    insert_data_from_spreadsheet(csv_file)
