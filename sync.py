import subprocess


def sync():
    subprocess.call(["rsync", "-ravzhe", "ssh", "/home/pi/rpi-weather/", "weather-02:/home/pi/rpi-weather", "--delete"])


if __name__ == '__main__':
    sync()
