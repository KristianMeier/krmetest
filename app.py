from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import psycopg2


app = Flask(__name__)

ENV = 'prod' #Skift denne til f.eks. "Production". Ellers vil den lave DB på vores local host. Det fejler nok, hvis den ikke er åben.

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost/lexus' # user:pw@adress/dbNavn
    
    conn = psycopg2.connect(database="lexus", user="postgres", password="root", host="localhost")
    mycursor =conn.cursor()
    
else:
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://rdtcsnvneueqrr:f7239f1149d0435a3e99b31a3013f07a2bfc6effa98b85120f6804d6dd93a34f@ec2-3-237-55-96.compute-1.amazonaws.com:5432/d78mgkrhaqjbe8'

    conn = psycopg2.connect(database="d78mgkrhaqjbe8", user="rdtcsnvneueqrr", password="f7239f1149d0435a3e99b31a3013f07a2bfc6effa98b85120f6804d6dd93a34f", host="ec2-3-237-55-96.compute-1.amazonaws.com")
    mycursor =conn.cursor()

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Feedback(db.Model):
    __tablename__ = 'kal'  # Denne kan ændres til det TABELNAVN man ønsker
    id = db.Column(db.Integer, primary_key=True)
    kalorier = db.Column(db.Integer)
    dato = db.Column(db.Date, default=datetime.now().date())

    def __init__(self, kalorier):
        self.kalorier = kalorier # ID og dato kommer auto (default og au)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/min_data')
def min_data():
    mycursor.execute("SELECT dato, sum(kalorier) FROM public.kal group by dato order by dato")
    data = mycursor.fetchall()
    return render_template('min_data.html', data=data)

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        kalorier = request.form['kalorier']  # id kommer fra autoincrement og dato fra default value.
        if kalorier == '':
            return render_template('index.html')
             #  Ovenstående 2 linjer fungerer ikke. Jeg har sat default checked på radiobuttons, så det ikke fejler når der submittets tom værdi.
        if db.session.query(Feedback):
            data = Feedback(kalorier)
            db.session.add(data)
            db.session.commit()
            return render_template('index.html')

if __name__ == '__main__':
    app.run()
