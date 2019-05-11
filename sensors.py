from urllib.request import urlopen
from urllib.error import URLError
from datetime import datetime
import bme280
import am2302
import ds18b20
import dht11
import pymysql
import sys

action = sys.argv[1]


def get_time():
    try:
        res = urlopen('http://just-the-time.appspot.com/')
    except URLError:
        return None
    result = res.read().strip().decode('utf-8')
    return datetime.strptime(result, '%Y-%m-%d %H:%M:%S')


def get_data():
    data = None

    if action == "ds18b20":
        data = ds18b20.get_data()["ds18b20"]
    elif action == "am2302":
        data = am2302.get_data()["am2302"]
    elif action == "dht11":
        data = dht11.get_data()["dht11"]
    elif action == "bme280":
        data = bme280.get_data()["bme280"]

    return data


def sql_record():
    if action == "ds18b20":
        return "INSERT INTO `outside` (`temperature`, `datetime`) VALUES (%s, %s)"

    elif action == "bme280":
        return "INSERT INTO `upstairs` (`pressure`, `humidity`, `temperature`, `datetime`) VALUES (%s, %s, %s, %s)"

    else:
        return "INSERT INTO `downstairs` (`humidity`, `temperature`, `datetime`) VALUES (%s, %s, %s)"


def save_data():
    data = get_data()
    utc = None
    retries = 0
    while utc is None and retries < 10:
        utc = get_time()
    if utc is not None:
        connection = pymysql.connect(host='weather-01',
                                     user='weather',
                                     password='letmein',
                                     db='weather')
        try:
            with connection.cursor() as cursor:
                if action == "ds18b20":
                    cursor.execute(sql_record(), (str(data["temperature"]),
                                                  utc.strftime('%Y-%m-%d %H:%M:%S')))

                elif action == "bme280":
                    cursor.execute(sql_record(), (str(data["pressure"]),
                                                  str(data["humidity"]),
                                                  str(data["temperature"]),
                                                  utc.strftime('%Y-%m-%d %H:%M:%S')))

                else:
                    cursor.execute(sql_record(), (str(data["humidity"]),
                                                  str(data["temperature"]),
                                                  utc.strftime('%Y-%m-%d %H:%M:%S')))

            connection.commit()
        finally:
            connection.close()


if __name__ == '__main__':
    save_data()
