from flask import Flask, render_template, request, redirect
import csv
import smtplib
from email.message import EmailMessage

# instantiating Flask app
app = Flask(__name__)


# Landing page route
@app.route('/')
def my_home():
    return render_template('index.html')


# Generic handler for extra pages that may be added in the future
@app.route('/<string:page_name>')
def html_page(page_name):
    return render_template(page_name)


# Form submission handler. Uses POST request for the information.
# Then, all the data is stored in a dictionary for later use
# Redirects to a Thank you page!
@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
        try:
            data = request.form.to_dict()
            write_to_csv(data)
            return redirect('/#thankyou')
        except OSError as err:
            return write_to_log(err)
    else:
        return 'Something went wrong. Try again in a while'


def write_to_log(error):
    with open('errorLog.txt') as log:
        log.write(error)


# When a form is submitted, this appends the information into a text file
def write_to_file(data):
    with open('database.txt', 'a') as file:
        name = data.get('name')
        email = data.get('email')
        message = data.get('message')
        file.write(f'Name: {name}\n'
                   f'Email: {email}\n'
                   f'Message: {message}\n')


# Writes form content into a CSV file
def write_to_csv(data):
    with open('database.csv', mode='a', newline='') as database:
        name = data.get('name')
        email = data.get('email')
        message = data.get('message')
        send_email(name, email, message)
        csv_writer = csv.writer(database, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([name, email, message])


# Function that will send email to me with all information contained in the form
def send_email(name, email_address, message):
    email = EmailMessage()
    email['from'] = name
    email['to'] = 'montufar.albert@gmail.com'
    email['subject'] = f'{name} contacted. Email is {email_address}'
    email.set_content(message)

    with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login('montufar.albert@gmail.com', '')
        smtp.send_message(email)


if __name__ == "__main__":
    app.run(port=5000, debug=True, use_reloader=True)

# Commands needed for the terminal
# Run in terminal
# set FLASK_APP=server.py
# $env:FLASK_APP = "server.py"
# python -m flask run

# If set enables the debug mode
# $env:FLASK_ENV = "development"
