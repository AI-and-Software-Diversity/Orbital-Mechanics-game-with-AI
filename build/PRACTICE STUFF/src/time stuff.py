import time
# import datetime
# t1 = time.time().real.__round__(2)
# t2 = time.time().real
# print(t1)

def current_time():
    # return time.time().real.__round__(2)
    return round(time.time().real, 2)

while True:
    if time.time().real.is_integer():
        print(time.time().real)

