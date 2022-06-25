# Python code to illustrate Sending mail from
# your Gmail account
import smtplib
def SendMail():
     # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)
     # start TLS for security
    s.starttls()
     # Authentication
    s.login("minorproject287@gmail.com", "wieraazbfsqpwqjg")
    # message to be sent
    message = "!!!!!!!ALERT!!!!!!!\n" \
              "!Drowsiness Detected!"
    # sending the mail
    s.sendmail("minorproject287@gmail.com", "minorproject287@gmail.com", message)
    # terminating the session
    s.quit()
