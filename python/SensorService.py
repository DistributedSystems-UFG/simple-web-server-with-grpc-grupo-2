from concurrent import futures

import grpc
import SensorService_pb2
import SensorService_pb2_grpc

from time import mktime, strptime

temperatureDataDB = [
    # {
    #     'date': '2022:12:11:10:0:0',
    #     'localization': '78:25',
    #     'temperature': 25.5
    # }
]


def date_to_timestamp(Y, m, d, H, M, S):
    return mktime(strptime('{}-{}-{} {}:{}:{}'.format(Y, m, d, H, M, S), '%Y-%m-%d %H:%M:%S'))


class SensorService(SensorService_pb2_grpc.SensorServiceServicer):
    def AddTemperatureData(self, request, context):
        date = request.date
        localization = request.localization
        temperature = request.temperature
        temperatureData = {
            'date': '{}:{}:{}:{}:{}:{}'.format(date.year, date.month, date.day, date.hour, date.minute, date.second),
            'localization': '{}:{}'.format(localization.x, localization.y),
            'temperature': temperature
        }
        temperatureDataDB.append(temperatureData)

        print("Added {} into Temperature Data DB".format(temperatureData))

        return SensorService_pb2.StatusReply(status='OK')

    def GetTemperatureByDate(self, request, context):
        d1 = request.d1
        timestamp1 = date_to_timestamp(
            d1.year, d1.month, d1.day, d1.hour, d1.minute, d1.second)
        d2 = request.d2
        timestamp2 = date_to_timestamp(
            d2.year, d2.month, d2.day, d2.hour, d2.minute, d2.second)
        date_range = (min(timestamp1, timestamp2), max(timestamp1, timestamp2))

        list = SensorService_pb2.ListTemperatureData()
        for temperatureData in temperatureDataDB:
            Y, m, d, H, M, S = temperatureData['date'].split(':')
            timestamp = date_to_timestamp(Y, m, d, H, M, S)
            if timestamp >= date_range[0] and timestamp <= date_range[1]:
                x, y = temperatureData['localization'].split(':')
                t = temperatureData['temperature']

                list.data.append(SensorService_pb2.TemperatureData(
                    date=SensorService_pb2.Date(year=int(Y), month=int(m), day=int(d),
                                                hour=int(H), minute=int(M), second=int(S)),
                    localization=SensorService_pb2.Localization(x=int(x), y=int(y)),
                    temperature=t
                ))

        return list


def server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    SensorService_pb2_grpc.add_SensorServiceServicer_to_server(
        SensorService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    server()
