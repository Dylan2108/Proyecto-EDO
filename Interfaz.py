import tkinter
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr
import numpy as np
import matplotlib.pyplot as plt
from tkinter import messagebox ,ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Compiler.GetFunction import GetFunction
from Compiler.ParseFunction import EvaluateFunction
def solve_exact_edo(edo_str, x0, y0, x_eval):
    #Resuelve la EDO y evalúa la solución en x_eval.
    #Devuelve el valor numérico o un mensaje de error.
    try:
        #Configurar símbolos
        x = sp.Symbol('x')
        y = sp.Function('y')(x)
        
        #Parsear la ecuación
        edo = parse_expr(
            edo_str.replace('^', '**').replace('y(x)', 'y'),
            local_dict={'y': y}
        )
        
        # 3. Construir y resolver la EDO
        eq = sp.Eq(y.diff(x), edo)
        sol_general = sp.dsolve(eq, y)
        
        # 4. Aplicar condiciones iniciales
        C1 = sp.Symbol('C1')
        condicion = sol_general.rhs.subs(x, x0) - y0
        constante = sp.solve(condicion, C1)[0]
        sol_exacta = sol_general.rhs.subs(C1, constante)
        
        # 5. Evaluar en x_eval y simplificar
        valor_exacto = sol_exacta.subs(x, x_eval).evalf()
        
        return float(valor_exacto)  # Devolver el valor exacto
        
    except Exception as e:
        return f"Error: {str(e)}"
def euler_method(func,xIni,yo,xFin,h):
    #Devuelve el valor de la solucion evaluada en xFin
    x_values = []
    y_values = []
    x = xIni
    y = yo
    x_values.append(x)
    y_values.append(y)
    n = (xFin - x)/h
    pasos = int(n)
    for i in range(0,pasos):
         x = x + h
         yAux = y_values[-1] + h * EvaluateFunction(func,x_values[-1],y_values[-1])#Prediccion
         y = y_values[-1] + h * ((EvaluateFunction(func,x_values[-1],y_values[-1]) + EvaluateFunction(func,x,yAux))/2)#Correcion
         x_values.append(x)
         y_values.append(y)
    return y
def error(func_str,func,xIni,y0,xFin,h):
    #Devuelve una lista de todos los valores x e y ademas del error absoluto y relativo asociado a cada valor
    x_values = []
    y_values = []
    errorAbs_values = []
    errorRel_values = []
    x = xIni
    y = y0
    errorAbs = 0
    errorRel = 0
    x_values.append(x)
    y_values.append(y)
    errorAbs_values.append(errorAbs)
    errorRel_values.append(errorRel)
    n = (xFin - x)/h
    pasos = int(n)
    for i in range(0,pasos):
            x = x + h
            lastX = x_values[-1]
            yAux = y_values[-1] + h * EvaluateFunction(func,x_values[-1],y_values[-1])
            y = y_values[-1] + h * ((EvaluateFunction(func,x_values[-1],y_values[-1]) + EvaluateFunction(func,x,yAux))/2)
            x_values.append(x)
            y_values.append(y)
            real_sol = solve_exact_edo(func_str,xIni,y0,x)
            errorAbs = abs(real_sol - y)
            errorRel = (errorAbs/abs(real_sol))*100
            errorAbs_values.append(errorAbs)
            errorRel_values.append(errorRel)
    return x_values,y_values,errorAbs_values,errorRel_values,x,y,errorAbs,errorRel
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
def ShowError():
    try:
        x0 = float(entry_x0.get())
        y0 = float(entry_y0.get())
        h = float(entry_h.get())
        f = float(entry_f.get())
        func = GetFunction(entry_func.get())
        x_values,y_values,errorAbs_values,errorRel_values,x,y,errorAbs,errorRel = error(entry_func.get(),func,x0,y0,f,h)
        messagebox.showinfo("Solucion",f"y en {f} es {y} , con un error absoluto de {errorAbs} y un error relativo de {errorRel} %")
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
def CreateTable():
    try:
      x0 = float(entry_x0.get())
      y0 = float(entry_y0.get())
      h = float(entry_h.get())
      f = float(entry_f.get())
      func = GetFunction(entry_func.get())
      x_values,y_values,errorAbs_values,errorRel_values,x,y,errorAbs,errorRel = error(entry_func.get(),func,x0,y0,f,h)
      fig, ax = plt.subplots(figsize=(10, 6))
      ax.axis('off')  # Ocultar ejes
      error_window = tkinter.Toplevel(app)
      error_window.title("Tabla de Errores")
      error_window.geometry("1920x1080")
        # Crear la tabla
      table_data = []
      for x, y, e_abs, e_rel in zip(x_values, y_values, errorAbs_values, errorRel_values):
            table_data.append([
                f"{x:.4f}", 
                f"{y:.6f}", 
                f"{e_abs:.6f}" if isinstance(e_abs, float) else "N/A", 
                f"{e_rel:.2f}%" if isinstance(e_rel, float) else "N/A"
            ])
        
        # Encabezados de la tabla
      headers = ["x", "y", "Error Absoluto", "Error Relativo (%)"]
        
        # Dibujar la tabla
      table = ax.table(
            cellText=table_data,
            colLabels=headers,
            loc="center",
            cellLoc="center"
        )
        
        # Ajustar estilo de la tabla
      table.auto_set_font_size(False)
      table.set_fontsize(10)
      table.scale(1.2, 1.2)  # Escalar tamaño de la tabla
        
        # Añadir la tabla a la ventana
      canvas = FigureCanvasTkAgg(fig, master=error_window)
      canvas.draw()
      canvas.get_tk_widget().pack(expand=True, fill="both")
        
    except Exception as e:
        messagebox.showerror("Error", f"Error al generar la tabla: {str(e)}")
def ResetValues():
    entry_func.delete(0, tkinter.END)  # Limpiar campo de la ecuación
    entry_x0.delete(0, tkinter.END)    # Limpiar campo de x0
    entry_y0.delete(0, tkinter.END)    # Limpiar campo de y0
    entry_f.delete(0, tkinter.END)     # Limpiar campo de x final
    entry_h.delete(0, tkinter.END)     # Limpiar campo de h
app = tkinter.Tk()
app.geometry("800x600")
app.title("Calculadora de EDO")
app.columnconfigure(1,weight=1)
for i in range(9):
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
btn_error = tkinter.Button(app,text="Errores",command=ShowError)
btn_error.grid(row=7,column=0,columnspan=2,pady=10,padx=5,sticky="nsew")
btn_Table = tkinter.Button(app,text="Tabla de Valores",command=CreateTable)
btn_Table.grid(row=8,column=0,columnspan=2,pady=10,padx=5,sticky="nsew")
btn_Reset = tkinter.Button(app,text="Reiniciar Valores",command=ResetValues)
btn_Reset.grid(row=9,column=0,columnspan=2,pady=10,padx=5,sticky="nsew")
app.mainloop()