import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from collections import deque

def dUdt(K, uX_norm, uY_norm, xY_norm):
    xY_norm2 = np.square(xY_norm)
    return (-K * uX_norm * uY_norm / xY_norm2), (K * uX_norm * uX_norm / xY_norm2)
def dUdt_del(K, G, uX_norm, uY_norm, xY_norm, dUxdt, dUydt):
    xY_norm2_ = np.square(xY_norm - (2 * G * uY_norm) - (2 * dUydt * np.square(xY_norm)))
    uY_norm_ = uY_norm - (2 * dUydt * xY_norm)
    uX_norm_ = uX_norm - (2 * dUxdt * xY_norm)
    return (-K * uX_norm_ * uY_norm_ / xY_norm2_), (K * uX_norm_ * uX_norm_ / xY_norm2_)

uX_norm = np.float128(0.5656)
uY_norm = np.float128(-0.5656)

charge = np.float128(1.602176634e-19)
m0 = np.float128(1.6726e-27)

sp_mod = np.sqrt(np.square(uX_norm) + np.square(uY_norm)) * np.float128(299792458)
minApproach_nr = -np.float128(1e-7) * np.square(charge) / (4 * m0 * np.log(uX_norm * np.float128(299792458) / sp_mod))
# minApproach_nr = np.float128(1e-9)
gamma = 1 / np.sqrt(1 - (np.square(uX_norm) + np.square(uY_norm)))

# xX_norm = np.float128(-1e-12) / minApproach_nr
# xY_norm = np.float128(1e-12) / minApproach_nr
xX_norm = -5000
xY_norm = 5000
edgeX_norm = -xX_norm

K = np.float128(1e-7) * np.square(charge)  / (4 * minApproach_nr * m0 * gamma)
G = np.float128(299792458) / minApproach_nr

print("speed: " + str(sp_mod) + " m/s")
print("momentum: " + str(1.871e21 * m0 * sp_mod / np.sqrt(1 - np.square(sp_mod / np.float128(299792458)))) + " MeV/c")
print("approach distance: " + str(minApproach_nr) + " m")
df = pd.DataFrame(columns=['pX', 'pY', 'aX', 'aY'])


# Taking information delay into account
tick = 0
lowestY = xY_norm
highestuY = uY_norm
history = deque()
time_norm = 0
while xX_norm < edgeX_norm and tick <= 50000000:
    dt = 0.0005
    if tick > 4000 * xY_norm:
        dUxdt, dUydt = dUdt(K, uX_norm, uY_norm, xY_norm)
        dUxdt, dUydt = dUdt(K, uX_norm + (dUxdt * dt * 0.5), uY_norm + (dUydt * dt * 0.5), history[-(4000 * xY_norm).astype(int)])#tick - (2 * xY_norm)/dt
        uX_norm += dUxdt * dt
        uY_norm += dUydt * dt
        xX_norm += uX_norm * dt
        xY_norm += uY_norm * dt
        history.append(xY_norm)
        history.popleft()
        if xY_norm < 1:
            df.loc[len(df)] = {'pX': xX_norm, 'pY': xY_norm, 'aX': dUxdt, 'aY': dUydt}
    else:
        dUxdt, dUydt = dUdt(K, uX_norm, uY_norm, xY_norm)
        dUxdt, dUydt = dUdt(K, uX_norm + (dUxdt * dt * 0.5), uY_norm + (dUydt * dt * 0.5), xY_norm + (uY_norm * dt * 0.5))
        uX_norm += dUxdt * dt
        uY_norm += dUydt * dt
        xX_norm += uX_norm * dt
        xY_norm += uY_norm * dt
        history.append(xY_norm)
    tick += 1