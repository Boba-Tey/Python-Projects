### This script sends email reminders for domain renewal
- Domain Name and Renewal Date fields are fetched as a dictionary from your database.
- Days remaining are calculated by subtracting the Renewal Date from the Current Day.
- If Days Left is less than 0, those domains are added to the Expired Domains list.
- If Days Left is less than 7, those domains are added to the Nearing Expiration list.
- This threshold number is configurable within the script.
- After both lists are created, the email will be sent to the provided email using the Yagmail module.
- If both lists are empty, no email would be sent on that day.
- You can automate this task either by using a task scheduler, cron job, or your choice of Function as a Service (FAAS) platform.
