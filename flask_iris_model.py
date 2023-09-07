# Importa las librerías necesarias:
from flask import Flask, request, jsonify
import pickle
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import os
from datetime import datetime
import ast

from sklearn import datasets

iris = datasets.load_iris()
target_names = iris.target_names

#Carga el modelo desde el archivo pickle:
with open('iris_model.pkl', 'rb') as file:
    model = pickle.load(file)

#Importa la librería sqlite3 en tu script de Python:
# import sqlite3

#Crea una conexión a la base de datos SQLite y un cursor para ejecutar comandos SQL:
# conn = sqlite3.connect('predictions.db')
# cursor = conn.cursor()

#Crea una tabla para almacenar los registros de tus predicciones. Por ejemplo, si quieres almacenar la fecha y hora de la predicción, los datos de entrada y la predicción resultante, puedes crear una tabla con las siguientes columnas:
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS predictions (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         timestamp TEXT,
#         input_data TEXT,
#         prediction TEXT
#     )
# ''')
# conn.commit()

# log.to_sql(name="predict", if_exist="append", con=engine)

#Configura la aplicación Flask y la base de datos SQLAlchemy:
app = Flask(__name__)



# #Define el modelo de la tabla Prediction para almacenar los registros de tus predicciones:
# class Prediction(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     timestamp = db.Column(db.String(20))
#     input_data = db.Column(db.String(50))
#     prediction = db.Column(db.String(50))

# #Crea la tabla Prediction en la base de datos:
# with app.app_context():
#     db.create_all()

#html empieza aquí
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask import render_template, request


@app.route('/')
def home():
    
    return render_template('html_iris_model.html')

#html termina aquí




@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        feature_1 = request.form.get("s_length", None)
        feature_2 = request.form.get("s_width", None)
        feature_3 = request.form.get("p_length", None)
        feature_4 = request.form.get("p_width", None)

        features=[float(feature_1), float(feature_2), float(feature_3), float(feature_4)]
        print(features)

        if None in features:
                return "Error"

        prediction = model.predict(np.array([features]).reshape(1, -1))
        class_name = target_names[int(prediction[0])]

        times = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        input_data = str(features)
        datos={
             "timestamp":times,
             "input_data":input_data,
             "prediction":class_name
        }
        registro = pd.DataFrame([datos])

        engine = create_engine("postgresql://fl0user:dsrot4LeDqW7@ep-jolly-violet-31957181.eu-central-1.aws.neon.tech:5432/Iris-Predictions-DB?sslmode=require")
        registro.to_sql("predictions", con=engine, if_exists='append', index=False)

        return jsonify({'prediction': class_name})
        
    else:
        feature_1 = request.args.get("feature_1", None)
        feature_2 = request.args.get("feature_2", None)
        feature_3 = request.args.get("feature_3", None)
        feature_4 = request.args.get("feature_4", None)

        features=[float(feature_1), float(feature_2), float(feature_3), float(feature_4)]
        print(features)

        if None in features:
                return "Error"

        prediction = model.predict(np.array([features]).reshape(1, -1))
        class_name = target_names[int(prediction[0])]

        times = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        input_data = str(features)
        datos={
             "timestamp":times,
             "input_data":input_data,
             "prediction":class_name
        }
        registro = pd.DataFrame([datos])
        engine = create_engine("postgresql://fl0user:dsrot4LeDqW7@ep-jolly-violet-31957181.eu-central-1.aws.neon.tech:5432/Iris-Predictions-DB?sslmode=require")
        registro.to_sql("predictions", con=engine, if_exists='append', index=False)

        return jsonify({'prediction': class_name})


@app.route('/view_predictions', methods=['GET'])
def view_predictions():
    engine = create_engine("postgresql://fl0user:dsrot4LeDqW7@ep-jolly-violet-31957181.eu-central-1.aws.neon.tech:5432/Iris-Predictions-DB?sslmode=require")
    df = pd.read_sql_query("SELECT * FROM predictions", con=engine).to_dict('records')
    return jsonify(df)  


if __name__ == '__main__':
    app.run(debug=True)

#Ponemos en marcha la aplicación:
"""Ejecutamos la aplicación Flask y envíamos una solicitud 
POST a la ruta /predict con los datos de la muestra en el 
cuerpo de la solicitud para obtener una predicción."""

""" Para enviar una solicitud POST a la ruta http://127.0.0.1:5000/predict de tu aplicación Flask desde Postman, 
puedes seguir los siguientes pasos:
- Abre Postman y crea una nueva solicitud haciendo clic en el botón + en la pestaña de solicitudes.
- Selecciona el método POST en el menú desplegable de métodos HTTP y escribe la URL de tu aplicación Flask seguida 
de la ruta /predict en el campo de URL. Por ejemplo, si tu aplicación Flask se está ejecutando localmente en el 
puerto 5000, la URL sería http://localhost:5000/predict.
- Haz clic en la pestaña Body debajo del campo de URL y selecciona la opción raw. 
Luego, escribe los datos de la muestra en formato JSON en el campo de texto. Por ejemplo, si quieres enviar 
una muestra con cuatro características, los datos podrían verse así:

{
    "features": [5.1, 3.5, 1.4, 0.2]
}

- Haz clic en el botón Send para enviar la solicitud POST a tu aplicación Flask. 
La respuesta de la aplicación aparecerá en la sección de respuesta debajo de la solicitud."""




#Para crear una base de datos SQLite con un registro de los datos que has pasado, 
# las predicciones que has hecho y la fecha y hora, puedes seguir los siguientes pasos:

# #Importa la librería sqlite3 en tu script de Python:
# import sqlite3

# #Crea una conexión a la base de datos SQLite y un cursor para ejecutar comandos SQL:
# conn = sqlite3.connect('predictions.db')
# cursor = conn.cursor()

# #Crea una tabla para almacenar los registros de tus predicciones. Por ejemplo, si quieres almacenar la fecha y hora de la predicción, los datos de entrada y la predicción resultante, puedes crear una tabla con las siguientes columnas:
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS predictions (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         timestamp TEXT,
#         input_data TEXT,
#         prediction TEXT
#     )
# ''')
# conn.commit()

# # Para insertar un registro en la tabla predictions, puedes ejecutar una instrucción INSERT con los valores que quieres almacenar. Por ejemplo, si quieres insertar un registro con la fecha y hora actual, los datos de entrada [5.1, 3.5, 1.4, 0.2] y la predicción resultante 0, puedes hacer lo siguiente:
# from datetime import datetime

# timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
# input_data = '[5.1, 3.5, 1.4, 0.2]'
# prediction = '0'

# cursor.execute('INSERT INTO predictions (timestamp, input_data, prediction) VALUES (?, ?, ?)', (timestamp, input_data, prediction))
# conn.commit()

# # Para consultar los registros almacenados en la tabla predictions, puedes ejecutar una instrucción SELECT. Por ejemplo, para obtener todos los registros ordenados por fecha y hora, puedes hacer lo siguiente:
# cursor.execute('SELECT * FROM predictions ORDER BY timestamp')
# rows = cursor.fetchall()

# for row in rows:
#     print(row)

"""Finalmente, vamos a reentrenar el modelo con los datos que introducimos y las predicciones."""




"""
Para crear un formulario HTML en Flask, puedes usar la extensión Flask-WTF que facilita el trabajo 
con formularios web. Con Flask-WTF, cada formulario se representa a través de una clase que hereda 
el objeto FlaskForm. En esta clase, puedes definir los campos del formulario como variables de clase1.

Aquí tienes un ejemplo de cómo podrías crear un formulario con 4 campos para introducir los valores 
de las características:
"""

