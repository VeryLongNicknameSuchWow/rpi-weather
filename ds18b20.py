import w1thermsensor


def get_data():
    temperature = w1thermsensor.W1ThermSensor().get_temperature()
    return {"ds18b20": {"temperature": float('{0:0.1f}'.format(temperature))}}
