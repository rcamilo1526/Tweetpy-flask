from flask import Flask,render_template,request
import twitter
import numpy as np
import scipy as stats
import matplotlib.pyplot as plt
app = Flask(__name__)
archivo = open("dataframetable.html", 'r')
textlist= archivo.readlines()
archivo.close()
text=''
for i in textlist:
    text=text+i
@app.route('/send', methods=['GET','POST'])
def send():
    if request.method == 'POST':
        x=request.form['x']#query
        y=int(request.form['y'])#num tweets
        df=twitter.runall(x,y)
        promedio=np.mean(df['len'])
        mediana = np.median(df['Words'])
        maximo=max(df.retweets)
        # moda=stats.mode(df['sentiment'])[0][0]
        # if moda==0:
        #     sentiment='Neutras'
        # elif moda==1:
        #     sentiment='positivas'
        # elif moda==-1:
        #     sentiment='negativas'
        return render_template('dashboard.html',
                                promedio=promedio,
                               sentiment='neutro',
                               mediana=mediana,
                               maximo=maximo)

    return render_template('dashboard.html')

@app.route('/index.html')
def dashboard():

    return render_template('index.html')

@app.route('/tables.html')
def tables():

    return render_template('tables.html',tt=text)

if __name__ == '__main__':
    app.run()
