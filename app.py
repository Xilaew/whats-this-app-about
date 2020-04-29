import io

import google_play_scraper
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import playstore
from flask import Flask, Response
from flask import request
import flask
app = Flask(__name__)


@app.route('/')
def homepage():
    play_id = request.args.get('app_id')
    play_id = 'tech.jonas.travelbudget' if play_id is None else play_id

    return """
    <h1>Whats this app about</h1>
    <form action='/' method='get'>
      <input type='text' name='app_id'></input>
      <input type='submit'></input>
    </form>
    <img src="/png/{play_id}">
    """.format(play_id=play_id)


@app.route('/png/<string:app_id>')
def tagcloud_image(app_id):
    try:
        fig = playstore.create_appcloud(app_id, 'en', 'us')
        output = io.BytesIO()
        FigureCanvas(fig).print_png(output)
        ret = Response(output.getvalue(), mimetype='image/png')
    except Exception:
        ret = flask.send_file('error.png')
    return ret


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
