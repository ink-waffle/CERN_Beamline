import numpy as np
import pandas as pd
import plotly.express as px

c = np.float128(299792458)
velocityDir = np.array([1, -1], dtype=np.float128)
velocityDir /= np.linalg.norm(velocityDir)
speed = 0.96 * c * velocityDir
mm = 1e3

position = np.array([-10, 10], dtype=np.float128)
charge = np.float128(1.602176634e-19)
charge2 = np.square(charge)
kE = np.float128(1.602e-10)
m0 = np.float128(1.6726e-27)


def lorentz_fac(speed_):
    return 1/np.sqrt(1 - np.square(np.linalg.norm(speed_)/299792458))
def sc_force(charge2_, speed_, position_):
    sp_mag = np.linalg.norm(speed_)
    return 10e-7 * charge2_ * sp_mag * np.sin(np.arccos(speed_[1]/sp_mag)) / (4 * np.square(position_[1]))
def get_acc_from_force(m0_, lorentz_fac_, force_, speed_):
    return (1/(m0_ * lorentz_fac_)) * (force_ - (speed_ * np.dot(force_, speed_)/np.square(c)))


maxacc = np.array([0, 0])
while position[0] < 10:
    dt = np.float128(1e-14) + (1 - np.abs(position[0] / 10)) * np.float128(-9.999999999999999978e-15)
    lorentz = lorentz_fac(speed)
    force = np.array([-speed[1], speed[0]]) * sc_force(charge2, speed, position / mm)
    acceleration = get_acc_from_force(m0, lorentz, force, speed)
    speed += acceleration * dt
    position += speed * mm * dt
    if acceleration[1] > maxacc[1]:
        maxacc = acceleration


print(maxacc)
print(position)
print(speed)
