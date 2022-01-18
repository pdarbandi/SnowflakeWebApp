from flask import Flask, render_template, request
import pandas as pd
from snowflakeConnection import sfconnect

# Flask Web Application
app = Flask("my website")

@app.route('/')
def homepage():
    cur.execute("SELECT COLOR_NAME, COUNT(*) "
                "FROM COLORS "
                "GROUP BY COLOR_NAME "
                "HAVING COUNT(*) > 50 "
                "ORDER BY COUNT(*) DESC;")
    rows = pd.DataFrame(cur.fetchall(), columns=['Color Name', 'Votes'])
    # dataframe as html
    dfhtml = rows.to_html(index=False)
    return render_template('index.html', dfhtml=dfhtml)

@app.route('/submit')
def submitpage():
    return render_template('submit.html')

@app.route('/thanks4submit', methods=["POST"])
def thanks4submit():
    colorname = request.form.get("cname")
    username = request.form.get("uname")
    cnx.cursor().execute("INSERT INTO COLORS(COLOR_UID, COLOR_NAME)" +
                         "SELECT COLOR_UID_SEQ.nextval, '" + colorname + "'")
    return render_template('thanks4submit.html'
                           ,colorname=colorname
                           ,username=username)

@app.route('/coolcharts')
def coolcharts():
    cur = cnx.cursor().execute("SELECT COLOR_NAME, COUNT(*) "
                                "FROM COLORS "
                                "GROUP BY COLOR_NAME ORDER BY COUNT(*) DESC;")
    data4Charts = pd.DataFrame(cur.fetchall(), columns=['color', 'votes'])
    data4ChartsJSON = data4Charts.to_json(orient='records')
    return render_template('coolcharts.html', data4ChartsJSON=data4ChartsJSON)


# Snowflake
cnx = sfconnect()

cur = cnx.cursor()


app.run()

