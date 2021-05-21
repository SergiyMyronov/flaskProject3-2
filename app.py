from flask import Flask, request
from faker import Faker
import csv
import requests

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/requirements/')
def content_of_requirements():
    with open('requirements.txt') as file_handler:
        text = ''
        for line in file_handler:
            text += f'<p>{line}</p>'
    return text


@app.route('/generate-users/')
def generate_users():
    number_of_users = request.args.get('users')

    if number_of_users:
        if number_of_users.isdigit():
            number_of_users = min(int(number_of_users), 200)
        else:
            number_of_users = 100
    else:
        number_of_users = 100

    fake = Faker()
    text = ''
    for i in range(number_of_users):
        name = fake.name()
        text += f'<p>{i+1} {name} {name.lower().replace(" ","_")}@gmail.com</p>'

    return text


@app.route('/mean/')
def mean_weight_height():
    with open("hw.csv", encoding='utf-8') as source_file:
        file_reader = csv.reader(source_file, delimiter=",")
        data = list(file_reader)
        count = 0
        whole_height = 0
        whole_weight = 0
        for row in data:
            if 0 < count < len(data)-1:
                whole_height += float(row[1])
                whole_weight += float(row[2])
            count += 1
        return f'{count} Mean height = {round(whole_height/(count-2)*2.54, 2)} cm. ' \
               f'Mean weight = {round(whole_weight/(count-2)/2.20462, 2)} kg</p> '


@app.route('/space/')
def space():
    r = requests.get('http://api.open-notify.org/astros.json')
    return str(r.json()["number"])


if __name__ == '__main__':
    app.run()
