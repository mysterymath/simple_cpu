import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)

cs = 0
so = 1
si = 2
sck = 3

GPIO.setup(cs, GPIO.OUT)
GPIO.setup(si, GPIO.OUT)
GPIO.setup(sck, GPIO.OUT)
GPIO.setup(so, GPIO.IN)

def send(val):
    bits = []
    for _ in range(8):
        bits.append(val & 1)
        val = val >> 1
    bits.reverse()
    send_bits(bits)

def send_bits(bits):
    for bit in bits:
        GPIO.output(sck, 0)
        GPIO.output(si, bit)
        GPIO.output(sck, 1)
    GPIO.output(sck, 0)

def rcv_bits(size):
    bits = []
    for _ in range(size):
        GPIO.output(sck, 1)
        bits.append(GPIO.input(so))
        GPIO.output(sck, 0)
    return bits

def enable_write():
    GPIO.output(cs, 0)
    send(0b00000110)
    GPIO.output(cs, 1)

def write_bits(bits):
    assert len(bits) == 1024
    for addr in range(0, 128, 16):
        enable_write()
        GPIO.output(cs, 0)
        send(0b00000010)
        send(addr)
        send_bits(bits[addr*8:(addr+16)*8])
        GPIO.output(cs, 1)
        sleep(10/1000)
        assert read_bits(0, 16*8) == bits[:16*8]

def read_bits(addr, size):
    GPIO.output(cs, 0)
    send(0b00000011)
    send(addr)
    bits = rcv_bits(size)
    GPIO.output(cs, 1)
    return bits


r_cs = [1] + [0]*40 + [1] + [0]*72 + [1]*2 + [0]*40 + [1] + [0]*32 + [1]*2 + [0]*48 + [1]
r_cs = r_cs * 4
r_cs = r_cs + [1]*(1024 - len(r_cs))

sio_cs = [0]*114 + [1] + [0]*74 + [1] + [0]*49 + [1]
sio_cs = sio_cs * 4
sio_cs = sio_cs + [1]*(1024 - len(sio_cs))

sio = [0]*7 + [1]*2 + [0]*22 + [1] + [0]*24 + [1]*2 + [0]*14 + [1] + [0]*7 + [1] + [0]*14 + [1]*2 + [0] + [1] + [0]*6 + [1]*2 + [0]*13 + [1] + [0]*2 
sio = sio * 4
sio = sio + [0]*20
sio = sio + sio

sio_hold = [1]*25 + [0]*17 + [1]*24 + [0]*49 + [1]*25 + [0]*17 + [1]*24 + [0]*9 + [1]*25 + [0]*25
sio_hold = sio_hold * 4
sio_hold = sio_hold + [0]*44 + [1]*20

try:
    GPIO.output(cs, 1)
    #write_bits(sio_hold)
    print(read_bits(0, 1024))
finally:
    GPIO.cleanup()
