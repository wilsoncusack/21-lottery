import os
import json
import random
import psycopg2
import math
import urlparse

# import flask web microframework
from flask import Flask
from flask import request
from flask import render_template


app = Flask(__name__)


# endpoint to get a question from the server
@app.route('/view')
def view():
	urlparse.uses_netloc.append("postgres")
	url = urlparse.urlparse(os.environ["DATABASE_URL"])

	conn = psycopg2.connect(
	    database=url.path[1:],
	    user=url.username,
	    password=url.password,
	    host=url.hostname,
	    port=url.port
	)
	cursor = conn.cursor()
	cursor.execute("SELECT * FROM rounds ORDER BY round_number asc;") # need to modify to not return the most recent
    length = len(result)
    data = [i for i in range(length)]
    for d in result:
        data[d[0] - 1] = [d[0], d[1], d[2]]
    del data[-1] # delete the last one so people can't see it
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0')