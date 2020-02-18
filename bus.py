import RPi.GPIO as GPIO
import sys
from time import sleep

memory = [0]*65536
end_code = 0

def code8(byte):
    global end_code
    memory[end_code] = byte
    end_code += 1

def code16(addr):
    code8(addr >> 8)
    code8(addr & 0xFF)

def mov(src, dst, jmp=None):
    if jmp is None:
        jmp = end_code + 6
    code16(jmp)
    code16(src)
    code16(dst)

def mov_indir8(src, offset, dst, jmp=None):
    mov(offset, end_code + 6 + 2 + 1)
    mov(src, dst, jmp)

def mov_indir16(hi, lo, dst, jmp=None):
    mov(hi, end_code + 6*2 + 2)
    mov(lo, end_code + 6 + 2 + 1)
    mov(0, dst, jmp)

def merge4(hi, lo, dst, jmp=None):
    mov_indir8(merge_hi, hi, merge4_t)
    mov_indir16(merge4_t, lo, dst, jmp)

def rs4(src, dst, jmp=None):
    mov_indir8(rs4_data, src, dst, jmp)

def add4(a, dst, jmp=None):
    mov_indir8(sum4, a, dst, jmp)

def add4_lo(a, b, dst, jmp=None):
    merge4(a, b, add4_lo_t)
    add4(add4_lo_t, dst, jmp)

def add4_hi(a, b, dst, jmp=None):
    rs4(a, add4_hi_a)
    rs4(b, add4_hi_b)
    add4_lo(add4_hi_a, add4_hi_b, dst, jmp)

def add8(a, b, dst, jmp=None):
    add4_lo(a, b, add8_lo)
    rs4(add8_lo, add8_carry)
    add4_hi(a, b, add8_hi_nocarry)
    add4_lo(add8_carry, add8_hi_nocarry, add8_hi)
    merge4(add8_hi, add8_lo, dst, jmp)

def cond8(test, t, f, dst, jmp=None):
    mov(t, cond8_t)
    mov(f, cond8_f)
    mov_indir8(cond8_data, test, cond8_lo)
    mov_indir8(cond8_f & 0xFF00, cond8_lo, dst, jmp)

def br8(test, t_jmp, f_jmp=None):
    if f_jmp is None:
        f_jmp = end_code + 78
    cond8(test, identity+(t_jmp>>8), identity+(f_jmp>>8), end_code + 72)
    cond8(test, identity+(t_jmp&0xFF), identity+(f_jmp&0xFF), end_code + 36 + 1)
    mov(0, 0, 0)

data = 65536

data -= 1
output = data
data -= 4095

data -= 4096
merge = data
for hi in range(16):
    for lo in range(256):
        memory[merge + (hi << 8 | lo)] = (hi << 4) | (lo & 0x0F)

data -= 256
merge_hi = data
for i in range(256):
    memory[merge_hi + i] = ((merge >> 8) & 0xF0) | (i & 0x0F)

data -= 256
identity = data
for i in range(256):
    memory[identity + i] = i

data -= 256
rs4_data = data
for i in range(256):
    memory[rs4_data + i] = i >> 4

data -= 256
sum4 = data
for i in range(16):
    for j in range(16):
        memory[sum4 + i*16 + j] = i + j

data -= 256
cond8_data = data
data -= 1
cond8_t = data
data -= 1
cond8_f = data
data -= 1
cond8_lo = data
assert cond8_t >> 8 == cond8_f >> 8
assert cond8_t & 0xFF != cond8_f & 0xFF
memory[cond8_data] = cond8_f & 0xFF
for i in range(1, 256):
    memory[cond8_data + i] = cond8_t & 0xFF

data -= 1
merge4_t = data

data -= 1
add4_lo_t = data

data -= 1
add4_hi_a = data
data -= 1
add4_hi_b = data

data -= 1
add8_lo = data
data -= 1
add8_carry = data
data -= 1
add8_hi_nocarry = data
data -= 1
add8_hi = data

data -= 1
count = data
data -= 1
prev = data
data -= 1
cur = data
data -= 1
next_ = data

for m in memory:
    assert 0 <= m < 256

mov(identity+0, prev)
mov(prev, output)
mov(identity+1, cur)
mov(cur, output)
mov(identity+12, count)
loop = end_code
add8(prev, cur, next_)
mov(cur, prev)
mov(next_, cur)
mov(cur, output)
add8(identity+0xFF, count, count)
br8(count, loop)

done = end_code
mov(0, 0, done)

GPIO.setmode(GPIO.BCM)

cs = 0
sio = 1
sclk = 2
hclk = 3
bcs = 4
bsi = 5

rcs = 6

GPIO.setup([cs, sio], GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup([sclk,hclk,bsi], GPIO.OUT, initial=0)
GPIO.setup(bcs, GPIO.OUT, initial=1)

GPIO.setup(rcs, GPIO.IN,pull_up_down=GPIO.PUD_UP)

num_counts = 0
def tick_lo():
    global num_counts
    num_counts += 1
    if len(sys.argv) >= 2:
        sleep(float(sys.argv[1]))
    GPIO.output(sclk, 0)
    GPIO.output(hclk, 0)

def tick_hi():
    if len(sys.argv) >= 2:
        sleep(float(sys.argv[1]))
    GPIO.output(sclk, 1)
    GPIO.output(hclk, 1)

def tick():
    tick_lo()
    tick_hi()

def init():
    GPIO.output(bcs, 0)

    for _ in range(6):
        tick_lo()
        GPIO.output(bsi, 0)
        tick_hi()

    for _ in range(2):
        tick_lo()
        GPIO.output(bsi, 1)
        tick_hi()

    for _ in range(8):
        tick_lo()
        GPIO.output(bsi, 0)
        tick_hi()

def cycle():
    try:
        is_bootstrap = True
        init()

        while True:
            while True:
                tick()
                if not GPIO.input(cs):
                    break

            if GPIO.input(sio):
                #print('Write')

                for _ in range(24):
                    tick()

                addr = ''
                for _ in range(16):
                    tick()
                    addr += '1' if GPIO.input(sio) else '0'
                addr = int(addr, 2)

                value = ''
                while True:
                    tick()
                    if GPIO.input(cs):
                        break
                    value += '1' if GPIO.input(sio) else '0'
                assert len(value) % 8 == 0
                value = [int(value[n:n+8], 2) for n in range(0, len(value), 8)]

                for v in value:
                    #print("Addr: {} Value: {}".format(addr, v))
                    if addr == output:
                        print("Output: {}".format(v))
                    memory[addr] = v
                    addr += 1

            else:
                #print('Read')

                for _ in range(24):
                    tick()

                addr = ''
                for _ in range(16):
                    tick()
                    addr += '1' if GPIO.input(sio) else '0'
                addr = int(addr, 2)

                for _ in range(25):
                    tick()

                is_first = True
                while True:
                    if GPIO.input(cs):
                        GPIO.setup(sio, GPIO.IN)
                        break
                    if is_bootstrap:
                        value = 0
                    else:
                        value = memory[addr]
                    #print('Addr: {} Value: {}'.format(addr, value))
                    value = '{:08b}'.format(value)
                    assert len(value) == 8
                    assert not GPIO.input(cs)
                    tick_lo()
                    if is_first:
                        GPIO.setup(sio, GPIO.OUT, initial=int(value[0]))
                        is_first = False
                    else:
                        GPIO.output(sio, int(value[0]))
                    tick_hi()
                    for v in value[1:]:
                        if GPIO.input(cs):
                            break
                        tick_lo()
                        GPIO.output(sio, int(v))
                        tick_hi()
                    addr += 1
            is_bootstrap = 0
    finally:
        print(num_counts)
        tick_lo()
        GPIO.output(bcs, 1)
        GPIO.cleanup()

cycle()
