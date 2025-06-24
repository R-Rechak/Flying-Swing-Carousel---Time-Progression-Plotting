from math import *
import matplotlib.pyplot as p
import time

start =time.time()
x0 = 0
dt = 0.01
w0 = 0.000001

x = x0
w = w0
t = 0

timestamp = [t]
velo_stamp = [w]
ang_stamp = [x]

high = False

while t < 120:
    A = 5+3*sin(x)
    if not high:    
        Re = 53039 * (5+3*sin(x)) * w
        if Re<10:
            Cd = 24/Re
        elif Re<27000:
            Cd = (24/Re)*(1+(0.15*(Re**0.687))) + (0.42/(1+(42500*(Re**(-1.16)))))
        else:
            Cd = 0.47
            high = True

    w = dt*(13913-((A)**2)*35.51*Cd*tan(x))/(41054+840*(A)**2) + w
    x = atan((A)*(w**2)/9.81)
    t+=dt

    timestamp.append(t)
    velo_stamp.append(w)
    ang_stamp.append(x)

end = time.time()
print(f"Runtime is:{end-start} seconds")


p.subplot(1, 2, 1)
p.plot(timestamp, velo_stamp)
p.title("Angular Velocity (rad/s) vs. Time (s)")
p.xlabel("Time (s)")
p.ylabel("Angular Velocity (rad/s)")
p.xlim(0,120)
p.ylim(0,4.5)
p.axhline(y=4, color='red', linestyle='--', linewidth=1, label="Terminal Angular Velocity")
p.legend()

p.subplot(1, 2, 2)
p.plot(timestamp, ang_stamp)
p.title("Angular Elevation (rad) vs. Time (s)")
p.xlabel("Time (s)")
p.ylabel("Angular Elevation (rad)")
p.xlim(0,120)
p.ylim(0,1.6)
p.axhline(y=1.494, color='red', linestyle='--', linewidth=1, label="Terminal Angular Elevation")
p.legend()

p.show()