from get_data import read_params
import pandas as pd
import argparse
import datetime

import csv
# import pymsql

import MySQLdb
import sqlalchemy
from sqlalchemy import create_engine

from urllib.parse import quote



### creating dummy data for timestamp for situation where we are getting a new data point everyday.
def insert_data_to_db(config_path):
    config = read_params(config_path)
    data_path = config['data_source']['source']
    df = pd.read_csv(data_path, sep = ',', encoding='utf-8')
    rows = df.shape[0]
    cols = df.shape[1]
    timestamp = []
    ids = []
    for i in reversed(range(rows)):
        d = datetime.datetime.now() - datetime.timedelta(hours=i)
        timestamp.append(d.strftime('%Y-%m-%d %H:%M:%S'))
        ids.append(rows - i)

    df['id'] = ids
    df['timestamp'] = timestamp
    new_cols = [col.replace(" ", "_") for col in df.columns]
    df.columns = new_cols
    # new_cols = [col.replace(" ", "_") for col in df.columns]
    cols = ['id', 'timestamp', 'fixed_acidity', 'volatile_acidity', 'citric_acid', 'residual_sugar',
       'chlorides', 'free_sulfur_dioxide', 'total_sulfur_dioxide', 'density',
       'pH', 'sulphates', 'alcohol', 'TARGET']

    # cols = [ 'timestamp', 'fixed_acidity', 'volatile_acidity', 'citric_acid', 'residual_sugar',
    #         'chlorides', 'free_sulfur_dioxide', 'total_sulfur_dioxide', 'density',
    #         'pH', 'sulphates', 'alcohol', 'TARGET']

    # print(df[cols].tail(1))
    # print(df.columns)
    # print(new_cols)

    # insert data to mysql
    df_info = config['db_info']
    db_string = 'mysql+mysqldb://' + df_info['username'] + ':' + quote(df_info['password']) + '@' + df_info['ip'] + ':' + str(df_info['port']) + '/' + df_info['database']
    engine = create_engine(db_string)
    conn = engine.connect()
    leave_rows = rows - 10
    df[cols][:leave_rows].to_sql(name=df_info['table'], con=engine, method="multi",index=False, if_exists="replace")
    # conn.commit()

    conn.close()
    #
    # # db = MySQLdb.connect(host=config['ip'],
    # #                      user=config['username'],
    # #                      passwd=config['password'],
    # #                      db=config['database'])
    # # cursor = db.cursor()
    #
    query = "INSERT INTO table_name('id', 'timestamp', 'fixed_acidity', 'volatile_acidity', 'citric_acid', 'residual_sugar', 'chlorides', 'free_sulfur_dioxide', 'total_sulfur_dioxide', 'density', 'pH', 'sulphates', 'alcohol', 'TARGET' ) VALUES( %s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s, %s, %s, %s)".replace('table_name', config['table']) \
    #
    #
    #
    #
    # my_data = []
    # for row in csv_data:
    #     my_data.append(tuple(row))
    #
    # cursor.executemany(query, my_data)
    # cursor.close()





if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument('--config', default='params.yaml')
    parsed_args = args.parse_args()
    insert_data_to_db(parsed_args.config)
