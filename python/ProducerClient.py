from random import randint, random
from time import time, gmtime

import grpc
import SensorService_pb2
import SensorService_pb2_grpc

import const


def run():
    for i in range(100):
        with grpc.insecure_channel(const.IP + ':' + const.PORT) as channel:
            stub = SensorService_pb2_grpc.SensorServiceStub(channel)

            # compute a random time in the range [5 years in the past, now)
            now = time()
            secondsInYear =  31_536_000
            random_time = now - 5*secondsInYear*random()
            rt = gmtime(random_time)

            # compute a random localization
            x = randint(1, 100)
            y = randint(1, 100)

            # compute a random temperature
            t = -20.0 + random()*60.0
            response = stub.AddTemperatureData(SensorService_pb2.TemperatureData(
                date=SensorService_pb2.Date(year=rt.tm_year, month=rt.tm_mon, day=rt.tm_mday,
                                            hour=rt.tm_hour, minute=rt.tm_min, second=rt.tm_sec),
                localization=SensorService_pb2.Localization(x=x, y=y),
                temperature=t
            ))
            print('Added new temperature ' + response.status)


if __name__ == '__main__':
    run()
