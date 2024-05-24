from flask import Flask, render_template
from sqlalchemy import create_engine, MetaData, Table, select
import pandas as pd
import json

app = Flask(__name__)

# Connect to MySQL database
connection_string = "mysql+mysqlconnector://root:1234@localhost:3306/ems_db_11"
engine = create_engine(connection_string)
metadata = MetaData()

meter_data_100 = Table('meter_data_100', metadata, autoload_with=engine)

@app.route('/')
def index():
    # Query columns using pandas
    df = pd.read_sql("SELECT tt, V1, V2, V3, V4, V12 FROM meter_data_100 LIMIT 1000", engine)
    # df = pd.read_sql("SELECT tt, V1, V2, V3, V4, V12 FROM meter_data_100", engine)
    data_list = df.to_dict(orient='records')
    # print(data_list)
    return render_template('plots.html', data=data_list)


@app.route('/single-plot')
def one():
    # Query the necessary columns using pandas
    df = pd.read_sql("SELECT tt, V1, V2, V3, V4, V12 FROM meter_data_100 LIMIT 1000", engine)
    data_list = df.to_dict(orient='records')
    return render_template('plot.html', data=data_list)

@app.route('/list')
def list():
    # Create a connection
    with engine.connect() as connection:
        # Query the necessary columns
        query = select(
            meter_data_100.c.tt,
            meter_data_100.c.V1,
            meter_data_100.c.V2,
            meter_data_100.c.V3,
            meter_data_100.c.V4,
            meter_data_100.c.V12
        )
        result = connection.execute(query)
        rows = result.fetchall()
        # Convert to a list of dictionaries
        data_list = [dict(row._mapping) for row in rows]

    return render_template('list.html', data=data_list)

if __name__ == '__main__':
    app.run(debug=True)