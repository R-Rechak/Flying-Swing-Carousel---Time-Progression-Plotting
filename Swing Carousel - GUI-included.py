from math import *
import matplotlib.pyplot as p
import customtkinter as CTK

x0 = 0
dt = 0.001
w0 = 0

x = x0
w = w0
t = 0

r = 5
l = 3
w_f = 2
k = 12

class MainMenu(CTK.CTk): # The GUI implementation
    def __init__(self):
        super().__init__()
        self.title("Swing Carousel Evolution Graphing Tool")
        self.geometry("1200x675")
        mainMenu=CTK.CTkLabel(self, width=600, height=30, font=("Arial", 28), text_color="black", text="Swing Carousel Evolution Graphing Tool")
        mainMenu.place(x=300, y=20)

        radius = CTK.CTkEntry(self, width=500, height=40, font=("Arial", 14), text_color="black", placeholder_text="Enter the desired radius (recommnded: r > 0.6m)")
        radius.place(x=400, y=150); r_label = CTK.CTkLabel(self, width=60, height=40, font=("Arial", 14), text_color="black", text="Radius:"); r_label.place(x=340, y=150)
        length = CTK.CTkEntry(self, width=500, height=40, font=("Arial", 14), text_color="black", placeholder_text="Enter the desired chain length")
        length.place(x=400, y=210); l_label = CTK.CTkLabel(self, width=60, height=40, font=("Arial", 14), text_color="black", text="Length:"); l_label.place(x=340, y=210)
        terminalW = CTK.CTkEntry(self, width=500, height=40, font=("Arial", 14), text_color="black", placeholder_text="Enter the terminal angular velocity")
        terminalW.place(x=400, y=290); tW_label = CTK.CTkLabel(self, width=150, height=40, font=("Arial", 14), text_color="black", text="Terminal Angular Velocity:"); tW_label.place(x=400, y=250)
        seatsCount = CTK.CTkEntry(self, width=500, height=40, font=("Arial", 14), text_color="black", placeholder_text="Enter the desired number of seats")
        seatsCount.place(x=400, y=350); s_label = CTK.CTkLabel(self, width=60, height=40, font=("Arial", 14), text_color="black", text="Number of seats:"); s_label.place(x=284, y=350)

        def Start():
            global r
            global w_f
            global l
            global k
            if radius.get()!="":
                try:
                    if float(radius.get()) > 0:
                        r = float(radius.get())
                    else:    
                        rError = CTK.CTkLabel(self, width=300, height=40, font=("Arial", 10), text_color="red", text="Value has to be strictly positive!"); rError.place(x=900, y=150)
                        self.after(3000, rError.destroy)
                        return None
                except ValueError:
                    rError = CTK.CTkLabel(self, width=300, height=40, font=("Arial", 10), text_color="red", text="Value has to be a number!")
                    rError.place(x=900, y=150)
                    self.after(3000, rError.destroy)
                    return None

            if length.get()!="":
                try:
                    if float(length.get()) > 0:
                        l = float(length.get())
                    else:    
                        lError = CTK.CTkLabel(self, width=300, height=40, font=("Arial", 10), text_color="red", text="Value has to be strictly positive!"); lError.place(x=900, y=210)
                        self.after(3000, lError.destroy)
                        return None
                except ValueError:
                    lError = CTK.CTkLabel(self, width=300, height=40, font=("Arial", 10), text_color="red", text="Value has to be a number!"); lError.place(x=900, y=210)
                    self.after(3000, lError.destroy)
                    return None
                
            if terminalW.get()!="":
                try:
                    if float(terminalW.get()) > 0:
                        w_f = float(terminalW.get())
                    else:    
                        wError = CTK.CTkLabel(self, width=300, height=40, font=("Arial", 10), text_color="red", text="Value has to be strictly positive!"); wError.place(x=900, y=210)
                        self.after(3000, wError.destroy)
                        return None
                except ValueError:
                    wError = CTK.CTkLabel(self, width=300, height=40, font=("Arial", 10), text_color="red", text="Value has to be a number!"); wError.place(x=900, y=210)
                    self.after(3000, wError.destroy)
                    return None
                
            if seatsCount.get().isdigit():
                k = int(seatsCount.get())
            elif seatsCount.get() == "":
                True
            else:
                sError = CTK.CTkLabel(self, width=300, height=40, font=("Arial", 10), text_color="red", text="Value has to be a strictly positive integer!"); sError.place(x=900, y=350)
                self.after(3000, sError.destroy)
                return None
            
            self.destroy()
        
        start = CTK.CTkButton(self, width=200, height=60, font=("Arial", 22), text_color="white", text="Start", command=Start)
        start.place(x=500, y=550)

app = MainMenu()
app.mainloop()

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

