import sqlite3
import os
from twilio.rest import Client
from dotenv import load_dotenv
from datetime import datetime, timedelta

def print_due_dates():
    try:
        conn = sqlite3.connect("due_dates.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM due_dates")
        rows = cursor.fetchall()

        for row in rows:
            print(row)

        conn.commit()
    except sqlite3.Error as e:
        print("SQLite Error:", e)
    finally:
        conn.close()

# send reminders for assignments due within 24 hours
def send_reminders():
    try:
        conn = sqlite3.connect("due_dates.db")
        cursor = conn.cursor()

        load_dotenv()
        
        twilio_account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        twilio_auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        twilio_phone_number = os.getenv("TWILIO_PHONE_NUMBER")
        recipient_phone_number = os.getenv("RECIPIENT_PHONE_NUMBER")

        twilio_client = Client(twilio_account_sid, twilio_auth_token)

        current_datetime = datetime.now()

        # Get assignments due within 24 hours
        cursor.execute("SELECT course, task, assignment_type, due_date, weight FROM due_dates WHERE ? <= due_date AND due_date <= ?",
                    (current_datetime, current_datetime + timedelta(hours=24)))
        assignments = cursor.fetchall()

        for assignment in assignments:
            course, task, assignment_type, due_date_str, weight = assignment

            # Convert due_date_str to a datetime object
            due_date = datetime.strptime(due_date_str, "%Y-%m-%d %H:%M:%S")

            # Send a reminder SMS
            message = twilio_client.messages.create(
                to=recipient_phone_number,
                from_=twilio_phone_number,
                body=f"Reminder: Assignment for {course}: {task} (Type: {assignment_type} {weight}) is due on {due_date.strftime('%Y-%m-%d %I:%M %p')}."
            )

        conn.commit()
        print("Reminders sent successfully.")
    except sqlite3.Error as e:
        print("Error:", e)
    except Exception as e:
        print("Error sending SMS:", e)
    finally:
        conn.close()

if __name__ == "__main__":
    send_reminders()
    # print_due_dates()
