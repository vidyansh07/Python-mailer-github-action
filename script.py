import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_mail(workflow_name, repo_name, workflow_run_id):
    # SMTP server settings
    sender_email = os.getenv('SENDER_EMAIL')
    password = os.getenv('SENDER_PASSWORD')
    receiver_email = os.getenv('RECEIVER_EMAIL')
    
    if not sender_email or not password or not receiver_email:
        print("Error: Missing environment variables for email settings.")
        return
    
    subject = f'Workflow {workflow_name} has failed in repository {repo_name}'
    body = f'Workflow {workflow_name} has failed in repository {repo_name}. More details can be found in the workflow run page.\nRun Id: {workflow_run_id}'
    
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error while sending email: {e}")

if __name__ == '__main__':
    workflow_name = os.getenv('WORKFLOW_NAME')
    repo_name = os.getenv('REPO_NAME')
    workflow_run_id = os.getenv('WORKFLOW_RUN_ID')
    
    if not workflow_name or not repo_name or not workflow_run_id:
        print("Error: Missing environment variables for workflow details.")
    else:
        send_mail(workflow_name, repo_name, workflow_run_id)