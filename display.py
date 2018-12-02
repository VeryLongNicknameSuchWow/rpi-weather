import pymysql.cursors
import platform
from luma.core.interface.serial import i2c, spi
from luma.core.render import canvas
from luma.oled.device import sh1106

hostname = platform.node()


def get_data():
    answers = {}
    queries = {
        "outside": "SELECT `temperature` FROM `outside` ORDER BY `id` DESC LIMIT 1",
        "downstairs": "SELECT `temperature`, `humidity` FROM `downstairs` ORDER BY `id` DESC LIMIT 1",
        "upstairs": "SELECT `temperature`, `humidity`, `pressure` FROM `upstairs` ORDER BY `id` DESC LIMIT 1"
    }
    connection = pymysql.connect(host='rPi-01',
                                 user='weather',
                                 password='letmein',
                                 db='weather')
    try:
        with connection.cursor() as cursor:
            for q in queries:
                cursor.execute(queries[q])
                answers[q] = cursor.fetchone()
    finally:
        connection.close()
        return answers


def oled_object():
    if hostname == "rPi-02":
        return sh1106(serial_interface=spi(), width=128, height=64, rotate=0)
    elif hostname == "rPi-03":
        return sh1106(serial_interface=i2c(), width=128, height=64, rotate=0)


def display_data():
    data = get_data()
    oled = oled_object()
    oled.cleanup = None
    with canvas(oled) as draw:
        draw.rectangle(oled.bounding_box, outline="white", fill="black")
        draw.text((10, 3), "Gora: {0:0.1f}C {1}%".format(data["upstairs"][0], data["upstairs"][1]), fill="gray")
        draw.text((10, 23), "Dol:  {0:0.1f}C {1}%".format(data["downstairs"][0], data["downstairs"][1]), fill="gray")
        draw.text((10, 43), "{0:0.1f}C {1}hPa".format(data["outside"][0], data["upstairs"][2]), fill="gray")


if __name__ == '__main__':
    display_data()
