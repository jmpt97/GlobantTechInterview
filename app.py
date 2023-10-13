import os
import sys
from json import loads, dumps
from flask_swagger_ui import get_swaggerui_blueprint
import pandas as pd
import joblib
import urllib
from flask import Flask, request, redirect, jsonify
from sqlalchemy import create_engine
sys.path.append(os.path.join(os.path.dirname(__file__), "static"))

app = Flask(__name__)

SERVER = 'globant-tech.chsprj1nr44a.us-east-1.rds.amazonaws.com'
PORT = '1433'
DATABASE = 'GlobantTech'
USERNAME = 'admin'
PASSWORD = 'Future314!'
DRIVER = '{ODBC Driver 17 for SQL Server}'

connection_string = f"DRIVER={DRIVER};SERVER={SERVER};PORT={PORT};" \
                    f"DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD};"
quoted = urllib.parse.quote_plus(connection_string)
engine = create_engine(f'mssql+pyodbc:///?odbc_connect={quoted}', fast_executemany=True)

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Precious stone Price Predictor"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)

@app.route('/', methods=["GET", "POST"])
def index():
    """
    Redirects to the Swagger UI.

    Returns:
        Redirect response to the Swagger UI.
    """
    return redirect("/swagger")

@app.route('/dephiringaboveavg', methods=["GET", "POST"])
def aboveaverage():
    """
    Endpoint for predicting prices based on input data.

    Returns:
        JSON response indicating successful test.
    """
    year_selection = request.form.get('year_selection')
    query = f'EXEC [dbo].[GetDepartmentsWithHiringAboveAverage] {year_selection}'
    df = pd.read_sql_query(query, engine)
    print(df)
    return 'osk'#dumps(result, indent=4)

@app.route('/numberemployee', methods=["GET", "POST"])
def predict():
    """
    Endpoint for predicting prices based on input data.

    Returns:
        JSON response indicating successful test.
    """
    year_selection = 2021 if request.form.get('year_selection') is None \
                            else request.form.get('year_selection')
    department_selection =  '' if request.form.get('department_Selection') is None \
                            else request.form.get('department_Selection')
    job_selection =  '' if request.form.get('job_Selection') is None \
                            else request.form.get('job_Selection')
    query = "EXEC [dbo].[GetQuarterlyHiringStatistics]" \
                   f"{year_selection},'{department_selection}','{job_selection}'"
    print(query)
    df = pd.read_sql_query(query, engine)
    print(df)
    return 'ok'#dumps(result, indent=4)

@app.errorhandler(ValueError)
def handle_value_error(error):
    response = jsonify({"error": str(error)})
    response.status_code = 400  # Bad Request
    return response

@app.route('/upload_csv', methods=["GET", "POST"])
def upload_csv():
    file = request.files['Upload File']
    table_input = request.form.get('Select Table')    
    upload_file = True if request.form.get('Save File') == 'true' \
                            else False
    column_dict = {
        "hired_employees":['id', 'name', 'hire_datetime', 'department_id', 'job_id'],
        "departments":['id', 'department'],
        "jobs":['id', 'job']
    }

    dataframe = pd.read_csv(file,names=column_dict[table_input])
    if len(dataframe.columns) != len(column_dict[table_input]):
        raise ValueError("Number of columns in uploaded file doesn't match the expected number.")
    if table_input == 'hired_employees':
        dataframe['hire_datetime'] = pd.to_datetime(dataframe['hire_datetime']
                                                    , format='%Y-%m-%dT%H:%M:%SZ')

    if upload_file:
        dataframe.to_sql(table_input,engine,index=False,if_exists="replace",schema="dbo")
    return f'The file has been Uploaded successfully to: {table_input}'



if __name__ == '__main__':
    app.run(debug=True, port=8080)