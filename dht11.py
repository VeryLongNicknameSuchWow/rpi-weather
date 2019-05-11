import Adafruit_DHT


def get_data(pin):
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, pin)
    result = {"temperature": float('{0:0.1f}'.format(temperature)),
              "humidity": int('{0:0.0f}'.format(humidity))}

    return {"dht11": result}
