import socket
import argparse
import time
import os

def setup_gpio():
    os.system("sudo pigpiod")  # Launching GPIO library
    time.sleep(1)  # As i said it is too impatient and so if this delay is removed you will get an error
    import pigpio
    ESC = 17
    STEER = 18
    pi = pigpio.pi()
    pi.set_servo_pulsewidth(ESC, 0)
    pi.set_servo_pulsewidth(STEER, 0)
    time.sleep(1)
    # pi.set_servo_pulsewidth(ESC, 1500)
    # time.sleep(1)

    return pi,ESC,STEER

def setup_socket(port):
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('', port)
    sock.bind(server_address)
    sock.listen(1)

    return sock


def get_parameters(sock):
    # Wait for a connection
    print('waiting for a connection')
    connection, client_address = sock.accept()
    try:
        data = connection.recv(32)
        speed, angle = convert_to_signals(data)
        return speed, angle
    except ConnectionError:
        print("connection is empty")
    finally:
        # Clean up the connection
        connection.close()


def convert_to_signals(data):
    data_arr = data.decode().split("/")
    # conn.send(data.upper())
    data_arr = list(map(int, data_arr))
    speed = data_arr[1]
    angle = data_arr[2]
    return speed, angle


def set_to_units(speed,angle):

    pass

def calibrate(pi,ESC):   # Стандартная процедура автокалибровки для esc регулятора
    max_value = 2000  # Максимальное значение шим
    min_value = 700  # Минимальное значение шим
    pi.set_servo_pulsewidth(ESC, 0)
    print("Отключите питание (батарею) и нажмите Enter")
    inp = input()
    if inp == '':
        pi.set_servo_pulsewidth(ESC, max_value)
        print("Подключите батарею прямо сейчас. Вы должны услышать 2 звуквых сигнала. Затем дождитесь окончания сигнала и нажмите Enter")
        inp = input()
        if inp == '':
            pi.set_servo_pulsewidth(ESC, min_value)
            print ("Специальный сигнал скоро будет")
            time.sleep(7)
            print ("Ждите ....")
            time.sleep (5)
            print ("Не беспокойтесь, просто ждите.....")
            pi.set_servo_pulsewidth(ESC, 0)
            time.sleep(2)
            print ("Остановите ESC сейчас...")
            pi.set_servo_pulsewidth(ESC, min_value)
            time.sleep(1)
            print ("Калибровка завершена")
            # control() # You can change this to any other function you want
            pi.set_servo_pulsewidth(ESC, 1500)

def control(pi,ESC,speed,STEER,angle):
    pi.set_servo_pulsewidth(ESC, speed)
    pi.set_servo_pulsewidth(STEER,int(16.6666666*angle))

def stop(pi,ESC): #This will stop every action your Pi is performing for ESC ofcourse.
    pi.set_servo_pulsewidth(ESC, 0)
    pi.stop()

def main():
    # Ввод порта для передачи данных и флага калибровка. По умполчанию порт 1080, калибровка отключена

    # изменить порт можно командой:
    # -p <номер порта> пример: -p 1081

    # включить калибровку можно командой:
    # -с 1

    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--port", required=False,
                    help="choose port: 1080 as default")
    ap.add_argument("-c", "--calibrate", required=False,
                    help="car motor calibration")
    args = vars(ap.parse_args())

    port = 1080
    if args["port"] is not None:
        if int(args["port"]):
            port = (int(args["port"]))
    sock = setup_socket(port)

    pi, ESC, STEER = setup_gpio()
    if args["calibrate"] is not None:
        if int(args["calibrate"])==1:
            calibrate(pi,ESC)
        if int(args["calibrate"])==0:
            pass

    while True:

        speed, angle = get_parameters(sock)
        set_to_units(speed,angle)
        print(speed, angle)

        control(pi, ESC, speed,STEER, angle)
        pass


if __name__ == '__main__':
    main()
