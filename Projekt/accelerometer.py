import smbus
import time
import math

# MPU-6050 Registers
MPU6050_ADDR = 0x68
PWR_MGMT_1 = 0x6B
ACCEL_XOUT_H = 0x3B

bus = smbus.SMBus(1)
bus.write_byte_data(MPU6050_ADDR, PWR_MGMT_1, 0)

def read_raw_data(addr):
    high = bus.read_byte_data(MPU6050_ADDR, addr)
    low = bus.read_byte_data(MPU6050_ADDR, addr + 1)
    value = (high << 8) | low
    if value > 32767:
        value -= 65536
    return value

def get_acceleration():
    acc_x = read_raw_data(ACCEL_XOUT_H)
    acc_y = read_raw_data(ACCEL_XOUT_H + 2)
    acc_z = read_raw_data(ACCEL_XOUT_H + 4)
    return acc_x, acc_y, acc_z

def calibrate(samples=100):
    sum_x = sum_y = sum_z = 0
    for _ in range(samples):
        x, y, z = get_acceleration()
        sum_x += x
        sum_y += y
        sum_z += z
        time.sleep(0.01)
    return sum_x / samples, sum_y / samples, sum_z / samples

def is_moving(baseline, threshold=300):
    x, y, z = get_acceleration()
    dx = x - baseline[0]
    dy = y - baseline[1]
    dz = z - baseline[2]
    deviation = math.sqrt(dx**2 + dy**2 + dz**2)
    return deviation > threshold

# Main
print("Calibrating... Please keep the sensor still.")
baseline = calibrate()
print("Calibration complete. Monitoring for movement for up to 5 minutes...")

start_time = time.time()
timeout = 5 * 60  # 5 minutes in seconds

while time.time() - start_time < timeout:
    if is_moving(baseline):
        print("Movement detected!")
        break
    time.sleep(0.5)
