import pyodbc, yagmail, os
from dotenv import load_dotenv
from datetime import datetime, date

load_dotenv(".env")
yag = yagmail.SMTP(os.getenv("SENDER"), os.getenv("PASSWORD"))

db_template = (
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=103.224.240.107,1433;"
    "Database=yourdatabase;"
    f"UID={os.getenv('DBUSER')};"
    f"PWD={os.getenv('DBPASSWORD')};"
)

def get_dates():
    with pyodbc.connect(db_template) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT DomainName, RenewalDate FROM Domains")
        return {row[0]: row[1] for row in cursor.fetchall()}

def email_template(title, description):
    full_title = f"{title} [{datetime.now().strftime('%Y-%m-%d %H:%M')}]"
    yag.send(
        to = "example@gmail.com",
        subject = full_title,
        contents = description
    )

def send_email():
    today = date.today()
    site_renewal = get_dates()
    near_expiration = []
    expired_domains = []

    for domain_name, renewal_date in site_renewal.items():
        remaining =  renewal_date - today
        days_left = remaining.days

        if days_left < 0:
            expired_domains.append(f"{domain_name} on {renewal_date}")

        if 0 <= days_left <= 7:
            near_expiration.append(f"{domain_name} ({days_left} days remaining)")

    if not expired_domains and not near_expiration:
        return

    expired_list = "\n".join([f"• {domain}" for domain in expired_domains]) if expired_domains else "🧹 None at the moment"
    nearex_list = "\n".join([f"• {domain}" for domain in near_expiration]) if near_expiration else "🧹 None at the moment"

    email_template(
            "🌐 DOMAIN SUMMARY",
            f"""🚨 THE FOLLOWING DOMAINS HAVE EXPIRED \n{expired_list}
            \n⚠️ THE FOLLOWING DOMAINS ARE NEARING EXPIRATION \n{nearex_list}"""
        )

if __name__ == "__main__":
    send_email()
    yag.close()