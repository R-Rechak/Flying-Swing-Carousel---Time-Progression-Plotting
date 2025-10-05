from math import *
import matplotlib.pyplot as p

x0 = 0
dt = 0.01
w0 = 0

x = x0
w = w0
t = 0
t_max = 120

r = 5
l = 3
w_f = 2
k = 12

structure_inertia = 328.4 * r**3


# lists to store the progression of w and x along with t
timestamp = [t]
velo_stamp = [w]
ang_stamp = [x]

# The value of drag coefficient
Cd = 0.776

#Simple setup for the dichotomy
x_f = pi/4
max_x =pi/2
min_x = 0

# Dichotomy implementation to solve for the terminal angular elevation - Numerical solution to a transcendental equation
for i in range(10):
    if x_f < atan((w_f*w_f/9.81)*(r+l*sin(x_f))):
        min_x = x_f
        x_f = (min_x+max_x)/2
    else:
        max_x = x_f
        x_f = (min_x+max_x)/2

# terminal distance between the seats and the rotation axis
R = r+l*sin(x_f)

# Iterating over time - Euler-forward method implementation to solve the differential equation
while t < t_max:
    A = 5+3*sin(x) # Distance between the seats and the rotation axis
    w = dt*k*0.3004*((R**3)*(w_f**2)-(9.81*A**2)*tan(x))/(structure_inertia+k*70*A**2) + w #equation for the progression of angular velocity
    x = atan((A)*(w**2)/9.81) # equation for the progression of angular elevation
    t+=dt

    # storing new w and x values along with their respective timestamps
    timestamp.append(t)
    velo_stamp.append(w)
    ang_stamp.append(x)

p.figure(figsize=(15, 8))
# Plotting the angular velocity graph
p.subplot(1, 2, 1)
p.plot(timestamp, velo_stamp)
p.title("Angular Velocity (rad/s) vs. Time (s)")
p.xlabel("Time (s)")
p.ylabel("Angular Velocity (rad/s)")
p.xlim(0,t_max)
p.ylim(0,w_f+0.5)
p.axhline(y=w_f, color='red', linestyle='--', linewidth=1, label="Terminal Angular Velocity")
p.legend()

# Plotting the angular elevation graph
p.subplot(1, 2, 2)
p.plot(timestamp, ang_stamp)
p.title("Angular Elevation (rad) vs. Time (s)")
p.xlabel("Time (s)")
p.ylabel("Angular Elevation (rad)")
p.xlim(0,t_max)
p.ylim(0,pi/2)
p.axhline(y=x_f, color='red', linestyle='--', linewidth=1, label="Terminal Angular Elevation")
p.legend()

p.suptitle(f"Power Required: {round(k*0.3004*(R**3)*(w_f**3), 1)} W", fontsize=16)

p.show()
