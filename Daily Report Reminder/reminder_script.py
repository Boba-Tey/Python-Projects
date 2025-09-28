import pyodbc, yagmail, os
import time as t
from datetime import date, datetime
from dotenv import load_dotenv

load_dotenv(".env")
yag = yagmail.SMTP(os.getenv("SENDER"), os.getenv("PASSWORD"))

db_template = (
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=103.224.240.107,1433;"
    "Database=yourdatabase;"
    f"UID={os.getenv('DBUSER')};"
    f"PWD={os.getenv('DBPASSWORD')};"
)

current_date = date.today()
current_day = current_date.strftime("%A")
current_hour = datetime.now().hour

class DBQueries: 
    def query(self, your_query):
        sql, parameters = your_query
        with pyodbc.connect(db_template) as conn:
            cursor = conn.cursor()
            cursor.execute(sql, parameters) if parameters else cursor.execute(sql)
            return [row[0] for row in cursor.fetchall()]
        
    def insert_items(self, user_id, your_date, your_bool):
        with pyodbc.connect(db_template) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO DailyRecord (staffuserid, RecordDate, reported) VALUES (?, ?, ?)", 
                (user_id, your_date, your_bool))
            conn.commit()

    def add_record(self):
        staff_query = (f"SELECT staffuserid FROM StaffSchedule WHERE {current_day} = ?", (True,))
        report_query = ("SELECT staffuserid FROM DailyReports WHERE ReportDate = ?", (current_date,))

        for staff in self.query(staff_query):
            record_query = ("SELECT 1 FROM DailyRecord WHERE staffuserid = ? AND RecordDate = ?", (staff, current_date))
            if self.query(record_query):
                continue
            
            if staff in self.query(report_query):
                self.insert_items(staff, current_date, True)
            else:
                self.insert_items(staff, current_date, False)

    def get_info(self):
        date_info = {}
        email_info = {}
        staff_query = (f"SELECT staffuserid FROM StaffSchedule", None)
        
        for staff in self.query(staff_query):
            dates_query = ("SELECT RecordDate FROM DailyRecord WHERE staffuserid = ? AND reported = ?", 
                (staff, False,))
            
            if self.query(dates_query):
                date_info[staff] = self.query(dates_query)
        
        for staff in date_info.keys():
            staff_name = (f"SELECT staffname FROM Staff_Info WHERE staffuserid = ?", (staff,))
            email_query = (f"SELECT email FROM Staff_Info WHERE staffuserid = ?", (staff,))

            if (self.query(email_query) and self.query(staff_name)):
                email_info[self.query(email_query)[0]] = self.query(staff_name)[0]

        return date_info, email_info

    def send_email(self):
        date_info, email_info = self.get_info()

        for raw_date, (email, name) in zip(date_info.values(), email_info.items()):
            date_format = "\n• ".join([i.strftime("%Y-%m-%d") for i in raw_date])
            yag.send(
                to = email,
                subject = f"Daily Report Reminder [{datetime.now().strftime('%Y-%m-%d %H:%M')}]",
                contents = f"Hey {name}, you forgot to do your daily reports on:\n\n• {date_format}\n\nPlease fill it ASAP."
            )
            t.sleep(2)

if __name__ == "__main__":
    report = DBQueries()
    
    if current_hour == 8:
        report.send_email()

    if current_hour == 17:
        report.add_record()

    yag.close()