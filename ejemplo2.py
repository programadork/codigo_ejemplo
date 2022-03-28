
from tkinter import ttk 
from tkinter import *

import sqlite3

class Productos:
    base = 'productos.db'

    def __init__(self, root):
        self.wind = root
        self.wind.title("Productos")
        self.wind.geometry("850x600")

        frame1 = LabelFrame(self.wind, text="Informacion Del Producto", font=("Calibri", 14))
        frame2 = LabelFrame(self.wind, text="Datos Del Producto", font=("Calibri", 14))

        frame1.pack(fill="both", expand="yes", padx=20, pady=10)
        frame2.pack(fill="both", expand="yes", padx=20, pady=10)

        self.trv = ttk.Treeview(frame1, columns=(1,2,3,4), show="headings", height="5")
        self.trv.pack()

        self.trv.heading(1, text="ID Del Producto")
        self.trv.heading(2, text="Nombre Del Producto")
        self.trv.heading(3, text="Precio Del Producto")
        self.trv.heading(4, text="Cantidad Del Producto")
        self.consulta()

        lbl1 = Label(frame2, text="ID Del Producto", width=20)
        lbl1.grid(row=0, column=0, padx=5, pady=3)
        self.ent1 = Entry(frame2)
        self.ent1.grid(row=0, column=1, padx=5, pady=3)

        lbl2 = Label(frame2, text="Nombre Del Producto", width=20)
        lbl2.grid(row=1, column=0, padx=5, pady=3)
        self.ent2 = Entry(frame2)
        self.ent2.grid(row=1, column=1, padx=5, pady=3)

        lbl3 = Label(frame2, text="Precio Del Producto", width=20)
        lbl3.grid(row=2, column=0, padx=5, pady=3)
        self.ent3 = Entry(frame2)
        self.ent3.grid(row=2, column=1, padx=5, pady=3)

        lbl4 = Label(frame2, text="Cantidad Del Producto", width=20)
        lbl4.grid(row=3, column=0, padx=5, pady=3)
        self.ent4 = Entry(frame2)
        self.ent4.grid(row=3, column=1, padx=5, pady=3)

        btn1 = Button(frame2, text="Agregar", command=self.Agregar, width=12, height=2)
        btn1.grid(row=5, column=0)

        btn2 = Button(frame2, text="Eliminar", command=self.Eliminar, width=12, height=2)
        btn2.grid(row=5, column=1)

        btn3 = Button(frame2, text="Actualizar", command=self.Actualizar, width=12, height=2)
        btn3.grid(row=5, column=2)




    def run_query(self, query, parameters = ()):
        with sqlite3.connect(self.base) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters) 
            conn.commit()
            return result


    def consulta(self):
        book = self.trv.get_children()
        for element in book:
            self.trv.delete(element)  
        query = 'SELECT id, nombre, precio, cantidad FROM articulos'    
        rows = self.run_query(query)
        for row in rows:
            self.trv.insert('', 0, text=row[1], values=row) 

    def validar(self):   
        return len(self.ent1.get()) != 0 and len(self.ent2.get()) != 0 and len(self.ent3.get()) != 0 and len(self.ent4.get()) != 0


    def Agregar(self):
        if self.validar():
            query = 'INSERT INTO articulos VALUES(?,?,?,?)'
            parameters = (self.ent1.get(), self.ent2.get(), self.ent3.get(), self.ent4.get())      
            self.run_query(query, parameters)
            self.ent1.delete(0, END)
            self.ent2.delete(0, END)
            self.ent3.delete(0, END)
            self.ent4.delete(0, END)    
        else:
            print("no salvado") 
        self.consulta()      


    def Eliminar(self):
        try:
          self.trv.item(self.trv.selection())['text'] 
        except IndexError as e:
            return
        nombre = self.trv.item(self.trv.selection())['text'] 
        query = 'DELETE FROM articulos WHERE nombre = ?'
        self.run_query(query, (nombre,)) 
        self.consulta()  

    def Actualizar(self):  
        try:
          self.trv.item(self.trv.selection())['text']
        except IndexError as e:
            return
        precio = self.trv.item(self.trv.selection())['values'][2]
        cantidad = self.trv.item(self.trv.selection())['values'][3] 
        self.edit_wind = Toplevel()
        self.edit_wind.title("Actualizar")
        self.edit_wind.geometry("400x300")

        frame = LabelFrame(self.edit_wind, text="Actualizar Producto",  font=("Calibri", 12))
        frame.pack(fill="both", expand="yes", padx=20, pady=10)  

        Label(frame, text="Antiguo Precio:", width=15, font=("Calibri", 10)).grid(row=2, column=1, padx=10, pady=20)
        Entry(frame, textvariable = StringVar(frame, value = precio), state = 'readonly').grid(row=2, column=2)

        Label(frame, text="Nuevo Precio", width=15, font=("Calibri", 10)).grid(row=3, column=1)
        nue_vo = Entry(frame)
        nue_vo.grid(row=3, column=2)

        Label(frame, text="Antigua Cantidad:", width=15, font=("Calibri", 10)).grid(row=4, column=1, padx=10, pady=20)
        Entry(frame, textvariable = StringVar(frame, value = cantidad), state = 'readonly').grid(row=4, column=2)


        Label(frame, text="Nueva Cantidad", width=15, font=("Calibri", 10)).grid(row=5, column=1)
        nueva = Entry(frame)
        nueva.grid(row=5, column=2)

        Button(frame, text="Actualizar", command = lambda: self.edit_record(nue_vo.get(), precio, nueva.get(), cantidad), width=12, height=2).grid(row=7, column=2, pady=20)



    def edit_record(self, nue_vo, precio, nueva, cantidad): 
        query = 'UPDATE articulos SET precio = ?, cantidad = ? WHERE precio = ? AND cantidad = ?'
        parameters = (nue_vo, nueva, precio, cantidad) 
        self.run_query(query, parameters)
        self.edit_wind.destroy()
        self.consulta()     

           
    
      
if __name__ == '__main__':
    root = Tk()
    product = Productos(root)  
    root.mainloop()  