import schedule
import time
import smtplib
from dividend_scraper import exporting_data
from config import *
from dividend_scraper import excel_filepath_xlsx
from email.message import EmailMessage

#define excel to be sent
EXCEL=excel_filepath_xlsx

#define the function to send email
def sendEmail(sender_email, password, recipient_email, subject, content, excel_file):
    try:
        print("Starting sending email")
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg.set_content(content)

        with open(excel_file, 'rb') as f:
            file_data = f.read()
        msg.add_attachment(file_data, maintype="application", subtype="xlsx", filename=excel_file)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender_email, password)
            smtp.send_message(msg)
    except Exception as e:
        print(e)
    finally:
        print("Email Sent")

#define the scheduled job
def job():
    print("starting job")
    exporting_data()
    sendEmail(SENDER_EMAIL, PASSWORD, TO, SUBJECT, MESSAGE, EXCEL)
    print("Finished job.")

#main entry point
if __name__ == "__main__":
    print("Starting program...")
    schedule.every().friday.at("08:45").do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)

    print("Finished running.")


