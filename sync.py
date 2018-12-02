import subprocess


def sync():
    subprocess.call(["rsync", "-ravzhe", "ssh", "/home/pi/rpi-weather/", "rpi-02:/home/pi/rpi-weather", "--delete"])
    subprocess.call(["rsync", "-ravzhe", "ssh", "/home/pi/rpi-weather/", "rpi-03:/home/pi/rpi-weather", "--delete"])


if __name__ == '__main__':
    sync()
