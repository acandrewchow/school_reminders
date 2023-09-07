# school_reminders

Python script that utilizes Twilio's SMS messaging system to send reminders for assignments that are due within 24 hours

Runs a cron job every day at midnight to query assignments that are due within 24 hours

```bash
0 0 * * * /bin/bash /Users/andrewchow/Desktop/school_date_reminder/run_reminder.sh
```
