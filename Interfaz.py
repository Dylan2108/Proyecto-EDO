import tkinter
import simpy as sp
import numpy as np
import matplotlib.pyplot as plt
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Compiler.GetFunction import GetFunction
from Compiler.ParseFunction import EvaluateFunction
def euler_method(func,xIni,yo,xFin,h):
    x_values = []
    y_values = []
    x = xIni
    y = yo
    x_values.append(x)
    y_values.append(y)
    while(x < xFin):
         x = x + h
         lastX = x_values[-1]
         yAux = y_values[-1] + h * EvaluateFunction(func,x_values[-1],y_values[-1])
         y = y_values[-1] + h * ((EvaluateFunction(func,x_values[-1],y_values[-1]) + EvaluateFunction(func,x,yAux))/2)
         x_values.append(x)
         y_values.append(y)
    return y
def solveEdo():
    try:
        x0 = float(entry_x0.get())
        y0 = float(entry_y0.get())
        h = float(entry_h.get())
        f = float(entry_f.get())
        func = GetFunction(entry_func.get())
        value = euler_method(func,x0,y0,f,h)
        messagebox.showinfo("Solucion",f"y en {f} es {value}")
    except Exception:
        messagebox.showerror("Error","Error inesperado.Vuelva a introducir los datos")
def plot_isoclines(func):
    x_range = np.linspace(-10,10,400)
    y_range = np.linspace(-10,10,400)
    X , Y = np.meshgrid(x_range,y_range)
    Z = EvaluateFunction(func,X,Y)
    plt.figure(figsize=(8,6))
    for k in range(-5,6):
        plt.contour(X,Y,Z,levels = [k],colors = 'blue',alpha=0.5)
    plt.title("Isoclinas")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid()
    plt.axhline(0,color = 'black',linewidth = 0.5)
    plt.axvline(0,color = 'black',linewidth = 0.5)
def direction_field(func,x_range,y_range,step =1):
    X , Y = np.meshgrid(np.arange(x_range[0],x_range[1],step),np.arange(y_range[0],y_range[1],step))
    U = 1
    V = EvaluateFunction(func,X,Y)
    N = np.sqrt(U**2 + V**2)
    U2,V2 = U/N , V/N
    plt.quiver(X,Y,U2,V2,angles='xy')
def Graficate():
     try:
        func = GetFunction(entry_func.get())
        plot_isoclines(func)
        direction_field(func,x_range=(-10,10),y_range=(-10,10))
        plt.legend()
        plt.show()
     except Exception:
        messagebox.showerror("Error","Error inesperado. Vuelva a introducir los datos")
app = tkinter.Tk()
app.geometry("1920x1080")
app.title("Calculadora de EDO")
app.columnconfigure(1,weight=1)
for i in range(7):
    app.rowconfigure(i,weight=1)
tkinter.Label(app,text="Ecuacion").grid(row=0,column=0,sticky="e")
entry_func = tkinter.Entry(app,width=30)
entry_func.grid(row=0,column=1,padx=10,pady=5,sticky="we")
tkinter.Label(app,text="x0").grid(row=1,column=0,sticky="e")
entry_x0 = tkinter.Entry(app,width=10)
entry_x0.grid(row=1,column=1,padx=5,pady= 5,sticky="we")
tkinter.Label(app,text="y0").grid(row=2,column=0,sticky="e")
entry_y0 = tkinter.Entry(app,width=10)
entry_y0.grid(row=2,column=1,sticky="we")
tkinter.Label(app,text="Calcular y en x").grid(row=3,column=0,sticky="e")
entry_f = tkinter.Entry(app,width=10)
entry_f.grid(row=3,column=1,padx=5,pady=10,sticky="we")
tkinter.Label(app,text="h").grid(row=4,column=0,sticky="e")
entry_h = tkinter.Entry(app,width=10)
entry_h.grid(row=4,column=1,padx=5,pady=10,sticky="we")
btn_solve = tkinter.Button(app,text="Resolver",command=solveEdo)
btn_solve.grid(row=5,column=0,columnspan=2,pady=10,padx=5,sticky="nsew")
btn_graphicate = tkinter.Button(app,text="Graficar",command=Graficate)
btn_graphicate.grid(row=6,column=0,columnspan=2,pady=10,padx=5,sticky="nsew")
app.mainloop()