from math import *
import matplotlib.pyplot as p

x0 = 0
dt = 0.01
w0 = 0

x = x0
w = w0
t = 0

r = 5
l = 3
w_f = 2
k = 12

# lists to store the progression of w and x along with t
timestamp = [t]
velo_stamp = [w]
ang_stamp = [x]

#Simple setup for the dichotomy
x_f = pi/4
max_x =pi/2
min_x = 0

# Dichotomy implementation to solve for the terminal angular elevation - Numerical solution to a transcendental equation
for i in range(20):
    if x_f < atan((w_f*w_f/9.81)*(r+l*sin(x_f))):
        min_x = x_f
        x_f = (min_x+max_x)/2
    else:
        max_x = x_f
        x_f = (min_x+max_x)/2

# terminal distance between the seats and the rotation axis
A_f = r+l*sin(x_f)

# Parameters:
g = 9.81
C_b = 1.28
C_p = 0.776
rhoAir = 1.225
rho = 7930
Area_p = 0.632
h = 0.1
m = 70

D_p = 1/2 * C_p * rhoAir * Area_p
D_b = C_b * rhoAir

I_s = 5/192 * rho * h * r**4 # to avoid recalculationg a constant each iteration

# lists to store the progression of w and x along with t
engine_torque = k * (D_p * (A_f**3) * (w_f**2) + 3/320 * D_b * (r**5) * (w_f**2))
torque_eff = D_p * (A_f**3) * (w_f**2) + 3/320 * D_b * (r**5) * (w_f**2)

timestamp = [0]
velo_stamp = [0]
ang_stamp = [0]
power_stamp = [0]

A_n_1 = r
A_n = r

capped =False
# Iterating over time - Euler-forward method implementation to solve the differential equation. 
# Stops when w is virtually equal to w_f
while w < w_f*0.999:
    inertia = I_s +m*A_n**2 
    w += (dt*(torque_eff - D_p*(A_n**3)*(w**2) - 3/320 * D_b*(r**5)*(w**2)) - w*2*m*A_n*(A_n - A_n_1))/(inertia) #equation for the progression of angular velocity
    x = atan((A_n)*(w**2)/9.81) # equation for the progression of angular elevation

    A_n_1 = A_n
    A_n = r+l*sin(x)
    
    if (not capped) and w > w_f*0.99: 
        n_N = t
        capped =True #recording when w = 0.99 * w_f

    t+=dt
    # storing new w and x values along with their respective timestamps
    timestamp.append(t)
    velo_stamp.append(w)
    ang_stamp.append(x)
    power_stamp.append(w*engine_torque)


p.figure(figsize=(20, 10))
# Plotting the angular velocity graph
p.subplot(1, 3, 1)
p.plot(timestamp, velo_stamp)
p.title("Angular Velocity (rad/s) vs. Time (s)")
p.xlabel("Time (s)")
p.ylabel("Angular Velocity (rad/s)")
p.xlim(0,timestamp[-1])
p.ylim(0,w_f*1.2)
p.axhline(y=w_f, color='red', linestyle='--', linewidth=1, label="Terminal Angular Velocity")
p.legend()

# Plotting the angular elevation graph
p.subplot(1, 3, 2)
p.plot(timestamp, ang_stamp)
p.title("Angular Elevation (rad) vs. Time (s)")
p.xlabel("Time (s)")
p.ylabel("Angular Elevation (rad)")
p.xlim(0,timestamp[-1])
p.ylim(0,x_f*1.2)
p.axhline(y=x_f, color='red', linestyle='--', linewidth=1, label="Terminal Angular Elevation")
p.legend()

# Plotting the power consumption graph
p.subplot(1, 3, 3)
p.plot(timestamp, power_stamp)
p.title("Power (W) vs. Time (s)")
p.xlabel("Time (s)")
p.ylabel("Power (W)")
p.xlim(0,timestamp[-1])
p.ylim(0, 1.2 * k *(D_p * (A_f**3) * (w_f**3) + 3/320 * D_b * r**5 * w_f**3))
p.axhline(y=w_f*engine_torque, color='red', linestyle='--', linewidth=1, label="Terminal Power Consumption")
p.legend()

p.suptitle(f"Total Energy Required (To reach 99.9% terminal angular velocity): {round(sum(power_stamp)*dt/1000, 4)} kJ \n Average Power Required (To reach 99.9% terminal angular velocity): {round(sum(power_stamp)*dt/1000/timestamp[-1], 5)} kW \n Time to 99% of ω_f: {round(n_N, 1)} s; Time to 99.9% of ω_f: {round(timestamp[-1], 1)} s", fontsize=16)

p.show()
