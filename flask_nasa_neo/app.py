"""
    flask-nasa-neo

    A website to display information from NASA's Near Earth Object API.

"""

from flask import (
    Flask,
    render_template,
    abort,
)

import neoapi

app = Flask(__name__)
app.config.update(dict(
    DEBUG=False,
))


@app.route('/')
def show_approaches_today():
    neos = neoapi.today()
    return render_template('today.html', neos=neos)


@app.route('/details/<int:neo_id>')
def show_details(neo_id):
    neo = neoapi.details(neo_id)
    if neo is None:
        abort(404)
    return render_template('details.html', neo=neo)


if __name__ == '__main__':
    app.run()
