from flask import Flask,render_template,request
import twitter
import numpy as np
import scipy.stats as stats
import graphics
from bokeh.plotting import save
import matplotlib.pyplot as plt
app = Flask(__name__)
# def sentimiento(df):
#
#     return [neutros,positivos,negativos]
#
# files=twitter.filenames
# filename='graphics/{file}.png'.format(file=files)
# img="{{ url_for('static', filename={file}) }}".format(file=filename)
@app.route('/send', methods=['GET','POST'])
def send():

    if request.method == 'POST':
        x=request.form['x']#query
        y=int(request.form['y'])#num tweets
        df=twitter.runall(x,y)
        promedio=np.mean(df['len'])
        mediana = np.median(df['Words'])
        maximo=max(df.retweets)
        pie=graphics.pieChart(df)
        save(pie)
        if df['sentiment'].value_counts()[0]:
            neutros = df['sentiment'].value_counts()[0]
        else:
            neutros = 0
        if df['sentiment'].value_counts()[1]:
            positivos = df['sentiment'].value_counts()[1]
        else:
            positivos = 0
        if df['sentiment'].value_counts()[-1]:
            negativos = df['sentiment'].value_counts()[-1]
        else:
            negativos = 0
        return render_template('dashboard.html',
                                promedio=promedio,
                               # sentiment=sentiment,
                               mediana=mediana,
                               maximo=maximo,
                               positivos=positivos,
                               negativos=negativos,
                               neutros=neutros,
                               query=x)

    return render_template('dashboard.html')

@app.route('/index.html')
def dashboard():

    return render_template('index.html')

@app.route('/tables.html')
def tables():

    return render_template('tables.html')

if __name__ == '__main__':
    app.debug = True
    app.run()
