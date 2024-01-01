import requests
from flask import Flask, request
from jinja2 import Template

app = Flask(__name__)


@app.route("/")
def index():
    template = Template(requests.get('https://fuel-bills.github.io/Driver%20Salary/index.html#/').text)
    return template.render(request.args)


if __name__ == '__main__':
    app.run(port=9999)
