from flask import Flask, request
from jinja2 import Template

app = Flask(__name__, static_url_path='/static', static_folder='static')


@app.route("/")
def index():
    with open('index.html') as f:
        template = Template(f.read())
        return template.render(request.args)


if __name__ == '__main__':
    app.run(port=9999)
