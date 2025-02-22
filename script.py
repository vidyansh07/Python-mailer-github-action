import os
import smtplib
from email.mime.text import MIMEText # MIMEText is used to create the message body
from email.mime.multipart import MIMEMultipart # MIMEMultipart is a class that is used to create the message

def send_mail(workflow_name, repo_name, workflow_run_id):
    # SMTP server settings
    sender_email = os.getenv('SENDER_EMAIL')
    password = os.getenv('SENDER_PASSWORD')
    reciever_email = os.getenv('RECIEVER_EMAIL')
    
    subject = f'Workflow {workflow_name} has failed'
    body = f'Workflow {workflow_name} has failed in repository {repo_name} more details can be found in the workflow run page \n  Run Id: {workflow_run_id}'
    
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = reciever_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    # send mail
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        text = msg.as_string()
        server.sendmail(sender_email, reciever_email, text)
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error while sending email: {e}")
        
if __name__ == '__main__':
    send_mail(os.getenv('WORKFLOW_NAME'), os.getenv('REPO_NAME'), os.getenv('WORKFLOW_RUN_ID'))