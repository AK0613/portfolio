from flask import Flask, render_template, send_from_directory, request, redirect, url_for
import csv

app = Flask(__name__)
app.debug = True


@app.route('/')
def my_home():
    return render_template('index.html')


@app.route('/<string:page_name>')
def html_page(page_name):
    return render_template(page_name)


def write_to_file(data):
    with open('database.txt', 'a') as file:
        name = data.get('name')
        email = data.get('email')
        message = data.get('message')
        file.write(f'Name: {name}\n'
                   f'Email: {email}\n'
                   f'Message: {message}\n')


def write_to_csv(data):
    with open('database.csv', mode='a', newline='') as database:
        name = data.get('name')
        email = data.get('email')
        message = data.get('message')
        csv_writer = csv.writer(database, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([name, email, message])


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

    # Run in terminal
    # set FLASK_APP=server.py
    # $env:FLASK_APP = "server.py"
    # python -m flask run

    # If set FLASK_ENV=development enables the debug mode
