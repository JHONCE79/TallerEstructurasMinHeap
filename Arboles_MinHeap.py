import tkinter as tk
from tkinter import messagebox


class Paciente:
    def __init__(self, numero_paciente, genero, nombre, edad, triaje):
        self.numero_paciente = numero_paciente
        self.genero = genero
        self.nombre = nombre
        self.edad = edad
        self.triaje = triaje


class Nodo:
    def __init__(self, paciente):
        self.paciente = paciente
        self.izquierda = None
        self.derecha = None


class HeapMin:
    def __init__(self):
        self.raiz = None
        self.size = 0

    def insertar(self, paciente):
        nuevo_nodo = Nodo(paciente)
        self.size += 1
        if self.raiz is None:
            self.raiz = nuevo_nodo
        else:
            self.insertar_nodo(self.raiz, nuevo_nodo)

    def insertar_nodo(self, nodo_actual, nuevo_nodo):
        if nuevo_nodo.paciente.triaje < nodo_actual.paciente.triaje:
            if nodo_actual.izquierda is None:
                nodo_actual.izquierda = nuevo_nodo
            else:
                self.insertar_nodo(nodo_actual.izquierda, nuevo_nodo)
        else:
            if nodo_actual.derecha is None:
                nodo_actual.derecha = nuevo_nodo
            else:
                self.insertar_nodo(nodo_actual.derecha, nuevo_nodo)

    def consultar_proximo(self):
        if self.raiz:
            return self.raiz.paciente
        else:
            return None

    def atender_siguiente(self):
        if self.raiz:
            paciente_atendido = self.raiz.paciente
            self.raiz = self.eliminar_nodo(self.raiz)
            self.size -= 1
            return paciente_atendido
        else:
            return None

    def eliminar_nodo(self, nodo_actual):
        if nodo_actual.izquierda is None and nodo_actual.derecha is None:
            return None
        elif nodo_actual.izquierda is None:
            return nodo_actual.derecha
        elif nodo_actual.derecha is None:
            return nodo_actual.izquierda
        else:
            nodo_menor = self.obtener_nodo_menor(nodo_actual.derecha)
            nodo_actual.paciente = nodo_menor.paciente
            nodo_actual.derecha = self.eliminar_nodo(nodo_actual.derecha)
            return nodo_actual

    def obtener_nodo_menor(self, nodo):
        if nodo.izquierda:
            return self.obtener_nodo_menor(nodo.izquierda)
        else:
            return nodo

    def consultar_pacientes_espera(self):
        self.recorrer_arbol(self.raiz)

    def recorrer_arbol(self, nodo):
        pacientes_info = ""
        if nodo:
            pacientes_info += self.recorrer_arbol(nodo.izquierda)
            paciente = nodo.paciente
            pacientes_info += f"Número: {paciente.numero_paciente} | Nombre: {paciente.nombre} | Triaje: {paciente.triaje}\n"
            pacientes_info += self.recorrer_arbol(nodo.derecha)
        return pacientes_info

    def consultar_pacientes_por_triaje(self, triaje):
        return self.buscar_y_mostrar_por_triaje(self.raiz, triaje)

    def buscar_y_mostrar_por_triaje(self, nodo, triaje):
        pacientes_info = ""
        if nodo:
            pacientes_info += self.buscar_y_mostrar_por_triaje(nodo.izquierda, triaje)
            if nodo.paciente.triaje == triaje:
                paciente = nodo.paciente
                pacientes_info += f"Nombre: {paciente.nombre} | Triaje: {paciente.triaje}\n"
            pacientes_info += self.buscar_y_mostrar_por_triaje(nodo.derecha, triaje)
        return pacientes_info

    def eliminar_paciente_cola(self, nombre):
        self.raiz = self.eliminar_nodo_por_nombre(self.raiz, nombre)

    def eliminar_nodo_por_nombre(self, nodo, nombre):
        if nodo is None:
            return None
        elif nodo.paciente.nombre == nombre:
            self.size -= 1
            return self.eliminar_nodo(nodo)
        else:
            nodo.izquierda = self.eliminar_nodo_por_nombre(nodo.izquierda, nombre)
            nodo.derecha = self.eliminar_nodo_por_nombre(nodo.derecha, nombre)
            return nodo


class ColaPacientesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cola de Pacientes")

        self.cola_pacientes = HeapMin()

        self.create_widgets()

    def create_widgets(self):

        tk.Label(self.root, text="Datos del Paciente").grid(row=0, column=0, columnspan=2)
        tk.Label(self.root, text="Número de Paciente:").grid(row=1, column=0)
        self.num_paciente_entry = tk.Entry(self.root)
        self.num_paciente_entry.grid(row=1, column=1)
        tk.Label(self.root, text="Género:").grid(row=2, column=0)
        self.genero_entry = tk.Entry(self.root)
        self.genero_entry.grid(row=2, column=1)
        tk.Label(self.root, text="Nombre:").grid(row=3, column=0)
        self.nombre_entry = tk.Entry(self.root)
        self.nombre_entry.grid(row=3, column=1)
        tk.Label(self.root, text="Edad:").grid(row=4, column=0)
        self.edad_entry = tk.Entry(self.root)
        self.edad_entry.grid(row=4, column=1)
        tk.Label(self.root, text="Triaje:").grid(row=5, column=0)
        self.triaje_entry = tk.Entry(self.root)
        self.triaje_entry.grid(row=5, column=1)
        tk.Label(self.root, text="Eliminar Paciente").grid(row=12, column=0, columnspan=2)
        tk.Label(self.root, text="Nombre del Paciente:").grid(row=13, column=0)
        self.eliminar_nombre_entry = tk.Entry(self.root)
        self.eliminar_nombre_entry.grid(row=13, column=1)

        tk.Button(self.root, text="Registrar Paciente", command=self.registrar_paciente).grid(row=6, column=0,
                                                                                              columnspan=2)

        tk.Button(self.root, text="Consultar Próximo Paciente", command=self.consultar_proximo_paciente).grid(row=7,
                                                                                                              column=0,
                                                                                                              columnspan=2)

        tk.Button(self.root, text="Atender Siguiente Paciente", command=self.atender_siguiente_paciente).grid(row=8,
                                                                                                              column=0,
                                                                                                              columnspan=2)

        tk.Button(self.root, text="Consultar Pacientes en Espera", command=self.consultar_pacientes_espera).grid(row=9,
                                                                                                                 column=0,
                                                                                                                 columnspan=2)

        tk.Button(self.root, text="Consultar Pacientes por Triaje", command=self.consultar_pacientes_por_triaje).grid(
            row=10, column=0, columnspan=2)

        tk.Button(self.root, text="Eliminar Paciente", command=self.eliminar_paciente).grid(row=14, column=0,
                                                                                            columnspan=2)

    def registrar_paciente(self):
        try:
            numero_paciente = int(self.num_paciente_entry.get())
            genero = self.genero_entry.get()
            nombre = self.nombre_entry.get()
            edad = int(self.edad_entry.get())
            triaje = int(self.triaje_entry.get())
            paciente = Paciente(numero_paciente, genero, nombre, edad, triaje)
            self.cola_pacientes.insertar(paciente)
            messagebox.showinfo("Éxito", "Paciente registrado exitosamente.")
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese datos válidos.")

    def consultar_proximo_paciente(self):
        proximo_paciente = self.cola_pacientes.consultar_proximo()
        if proximo_paciente:
            messagebox.showinfo("Próximo Paciente", f"Próximo paciente a ser atendido: {proximo_paciente.nombre}")
        else:
            messagebox.showinfo("Próximo Paciente", "No hay pacientes en espera.")

    def atender_siguiente_paciente(self):
        paciente_atendido = self.cola_pacientes.atender_siguiente()
        if paciente_atendido:
            messagebox.showinfo("Paciente Atendido", f"Paciente atendido: {paciente_atendido.nombre}")
        else:
            messagebox.showinfo("Paciente Atendido", "No hay pacientes en espera.")

    def consultar_pacientes_espera(self):
        pacientes_espera_info = self.cola_pacientes.recorrer_arbol(self.cola_pacientes.raiz)
        if pacientes_espera_info:
            messagebox.showinfo("Pacientes en Espera", pacientes_espera_info)
        else:
            messagebox.showinfo("Pacientes en Espera", "No hay pacientes en espera.")

    def consultar_pacientes_por_triaje(self):
        try:
            triaje = int(self.triaje_entry.get())
            pacientes_info = self.cola_pacientes.consultar_pacientes_por_triaje(triaje)
            if pacientes_info:
                messagebox.showinfo("Pacientes por Triaje", pacientes_info)
            else:
                messagebox.showinfo("Pacientes por Triaje", f"No hay pacientes en espera con triaje {triaje}.")
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese un triaje válido.")

    def eliminar_paciente(self):
        nombre = self.eliminar_nombre_entry.get()
        if nombre:
            self.cola_pacientes.eliminar_paciente_cola(nombre)
            messagebox.showinfo("Paciente Eliminado", f"Paciente {nombre} eliminado exitosamente.")
        else:
            messagebox.showerror("Error", "Por favor, ingrese el nombre del paciente a eliminar.")


root = tk.Tk()
app = ColaPacientesApp(root)
root.mainloop()
#