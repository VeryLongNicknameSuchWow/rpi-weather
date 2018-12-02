import Adafruit_DHT


def get_data():
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, 4)
    result = {"temperature": float('{0:0.1f}'.format(temperature)),
              "humidity": int('{0:0.0f}'.format(humidity))}

    return {"dht11": result}
