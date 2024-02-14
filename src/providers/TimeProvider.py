import time

class TimeProvider():

    def sleep(ms):
        sleepTime = ms / 1000
        time.sleep(sleepTime)
