from flask import Flask, render_template, request, redirect
import csv

# Flags to enable the debug mode so I can make changes without having to restart the flask server.
app = Flask(__name__)
app.debug = True


# Landing page route
@app.route('/')
def my_home():
    return render_template('index.html')


# Generic handler for extra pages that may be added in the future
@app.route('/<string:page_name>')
def html_page(page_name):
    return render_template(page_name)


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
        csv_writer = csv.writer(database, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([name, email, message])


# Form submission handler. Uses POST request for the information. Then, all the data is stored in a dictionary for later use
# Redirects to a Thank You page!
@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
        try:
            data = request.form.to_dict()
            write_to_csv(data)
            return redirect('/#thankyou')
        except:
            return 'did not save to database'
    else:
        return 'Something went wrong. Try again in a while'


if __name__ == "__main__":
    app.run(port=5000, debug=True, use_reloader=True)

# Commmands needed for the terminal
# Run in terminal
# set FLASK_APP=server.py
# $env:FLASK_APP = "server.py"
# python -m flask run

# If set FLASK_ENV=development enables the debug mode
