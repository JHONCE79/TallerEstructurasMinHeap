import tkinter as tk
from tkinter import messagebox

class Paciente:
    def __init__(self, numero_paciente, genero, nombre, edad, triaje):
        self.numero_paciente = numero_paciente
        self.genero = genero
        self.nombre = nombre
        self.edad = edad
        self.triaje = triaje

class HeapMin:
    def __init__(self):
        self.heap = []

    def insertar(self, paciente):
        self.heap.append(paciente)
        self._heapify_up(len(self.heap) - 1)

    def _heapify_up(self, index):
        parent_index = (index - 1) // 2
        if parent_index >= 0 and self.heap[index].triaje < self.heap[parent_index].triaje:
            self.heap[index], self.heap[parent_index] = self.heap[parent_index], self.heap[index]
            self._heapify_up(parent_index)

    def consultar_proximo(self):
        if self.heap:
            return self.heap[0]
        else:
            return None

    def atender_siguiente(self):
        if not self.heap:
            return None
        if len(self.heap) == 1:
            return self.heap.pop()
        root = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._heapify_down(0)
        return root

    def _heapify_down(self, index):
        smallest = index
        left_child_index = 2 * index + 1
        right_child_index = 2 * index + 2

        if left_child_index < len(self.heap) and self.heap[left_child_index].triaje < self.heap[smallest].triaje:
            smallest = left_child_index

        if right_child_index < len(self.heap) and self.heap[right_child_index].triaje < self.heap[smallest].triaje:
            smallest = right_child_index

        if smallest != index:
            self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
            self._heapify_down(smallest)

    def consultar_pacientes_espera(self):
        return "\n".join([f"Número: {p.numero_paciente} | Nombre: {p.nombre} | Triaje: {p.triaje}" for p in self.heap])

    def consultar_pacientes_por_triaje(self, triaje):
        return "\n".join([f"Nombre: {p.nombre} | Triaje: {p.triaje}" for p in self.heap if p.triaje == triaje])

    def eliminar_paciente_cola(self, nombre):
        for i, paciente in enumerate(self.heap):
            if paciente.nombre == nombre:
                last_paciente = self.heap.pop()
                if i < len(self.heap):
                    self.heap[i] = last_paciente
                    self._heapify_down(i)
                    self._heapify_up(i)
                break

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
        pacientes_espera_info = self.cola_pacientes.consultar_pacientes_espera()
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
