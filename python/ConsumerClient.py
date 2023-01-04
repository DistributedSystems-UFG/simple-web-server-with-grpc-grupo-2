import grpc
import SensorService_pb2
import SensorService_pb2_grpc

import const

from sys import argv, exit


def error_msg():
    print("ERRO! Seguir um dos seguintes comandos:")
    print(">>> python .\\ConsumerClient.py date Y1:m1:d1:H1:M1:S1 Y2:m2:d2:H2:M2:S2")
    print(">>> python .\\ConsumerClient.py localization x1:y1 x2:y2")


def run():
    if len(argv) < 4:
        error_msg()
        exit(1)

    if argv[1].lower() == 'date':
        try:
            Y1, m1, d1, H1, M1, S1 = argv[2].split(':')
            Y2, m2, d2, H2, M2, S2 = argv[3].split(':')
        except:
            error_msg()
            exit(1)
    elif argv[1].lower() == 'localization':
        x1, y1 = argv[2].split(':')
        x2, y2 = argv[3].split(':')
    else:
        error_msg()
        exit(1)

    with grpc.insecure_channel(const.IP + ':' + const.PORT) as channel:
        stub = SensorService_pb2_grpc.SensorServiceStub(channel)

        if argv[1].lower() == 'date':
            response = stub.GetTemperatureByDate(SensorService_pb2.DateRange(
                d1=SensorService_pb2.Date(year=int(Y1), month=int(m1), day=int(d1),
                                          hour=int(H1), minute=int(M1), second=int(S1)),
                d2=SensorService_pb2.Date(year=int(Y2), month=int(m2), day=int(d2),
                                          hour=int(H2), minute=int(M2), second=int(S2))
            ))
            print(response.data)
        elif argv[1].lower() == 'localization':
            response = stub.GetTemperatureByLocalization(SensorService_pb2.LocalizationRange(
                l1=SensorService_pb2.Localization(x=int(x1), y=int(y1)),
                l2=SensorService_pb2.Localization(x=int(x2), y=int(y2))
            ))
            print(response.data)


if __name__ == '__main__':
    run()
