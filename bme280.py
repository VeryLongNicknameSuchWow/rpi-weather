import board
import busio
import adafruit_bme280


def get_data(address):
    i2c = busio.I2C(board.SCL, board.SDA)
    bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c, address=address)

    result = {"temperature": float('{0:0.1f}'.format(bme280.temperature)),
              "humidity": int('{0:0.0f}'.format(bme280.humidity)),
              "pressure": int('{0:0.0f}'.format(bme280.pressure))}

    return {"bme280": result}
