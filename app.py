from flask import Flask,render_template,request
import twitter
import numpy as np
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
        x=request.form['x']
        y=int(request.form['y'])
        df=twitter.runall(x,y)
        labels = list(df['source'].unique())
        cant = list(df['source'].value_counts())
        fig1, ax1 = plt.subplots()
        ax1.pie(cant, labels=labels, autopct='%1.1f%%',
                shadow=True, startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        plt.savefig('static/images/foo.png')
        z=np.mean(df['len'])
        return render_template('dashboard.html',
                                mediana=z)

    return render_template('dashboard.html')

@app.route('/')
def dashboard():

    return render_template('index.html',
                           mediana='8415.24')

@app.route('/tables.html')
def tables():

    return render_template('tables.html',tt=text)

if __name__ == '__main__':
    app.run()
