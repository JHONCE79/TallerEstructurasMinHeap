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
        self.padre = None


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
            self._insertar_nodo(self.raiz, nuevo_nodo)
            self._heapify_up(nuevo_nodo)

    def _insertar_nodo(self, nodo, nuevo_nodo):
        queue = [nodo]
        while queue:
            actual = queue.pop(0)
            if actual.izquierda is None:
                actual.izquierda = nuevo_nodo
                nuevo_nodo.padre = actual
                return
            elif actual.derecha is None:
                actual.derecha = nuevo_nodo
                nuevo_nodo.padre = actual
                return
            else:
                queue.append(actual.izquierda)
                queue.append(actual.derecha)

    def _heapify_up(self, nodo):
        while nodo.padre and nodo.paciente.triaje < nodo.padre.paciente.triaje:
            nodo.paciente, nodo.padre.paciente = nodo.padre.paciente, nodo.paciente
            nodo = nodo.padre

    def consultar_proximo(self):
        return self.raiz.paciente if self.raiz else None

    def atender_siguiente(self):
        if not self.raiz:
            return None
        if self.size == 1:
            paciente = self.raiz.paciente
            self.raiz = None
            self.size -= 1
            return paciente

        root_paciente = self.raiz.paciente
        last_node = self._get_last_node()
        self.raiz.paciente = last_node.paciente
        if last_node.padre:
            if last_node.padre.derecha == last_node:
                last_node.padre.derecha = None
            else:
                last_node.padre.izquierda = None
        self._heapify_down(self.raiz)
        self.size -= 1
        return root_paciente

    def _heapify_down(self, nodo):
        while nodo:
            smallest = nodo
            if nodo.izquierda and nodo.izquierda.paciente.triaje < smallest.paciente.triaje:
                smallest = nodo.izquierda
            if nodo.derecha and nodo.derecha.paciente.triaje < smallest.paciente.triaje:
                smallest = nodo.derecha
            if smallest == nodo:
                break
            nodo.paciente, smallest.paciente = smallest.paciente, nodo.paciente
            nodo = smallest

    def _get_last_node(self):
        queue = [self.raiz]
        last_node = None
        while queue:
            last_node = queue.pop(0)
            if last_node.izquierda:
                queue.append(last_node.izquierda)
            if last_node.derecha:
                queue.append(last_node.derecha)
        return last_node

    def consultar_pacientes_espera(self):
        pacientes_info = self._recorrer_arbol(self.raiz)
        return pacientes_info

    def _recorrer_arbol(self, nodo):
        if not nodo:
            return ""
        pacientes_info = ""
        queue = [nodo]
        while queue:
            actual = queue.pop(0)
            paciente = actual.paciente
            pacientes_info += f"Número: {paciente.numero_paciente} | Nombre: {paciente.nombre} | Triaje: {paciente.triaje}\n"
            if actual.izquierda:
                queue.append(actual.izquierda)
            if actual.derecha:
                queue.append(actual.derecha)
        return pacientes_info

    def consultar_pacientes_por_triaje(self, triaje):
        pacientes_info = self._buscar_y_mostrar_por_triaje(self.raiz, triaje)
        return pacientes_info

    def _buscar_y_mostrar_por_triaje(self, nodo, triaje):
        if not nodo:
            return ""
        pacientes_info = ""
        queue = [nodo]
        while queue:
            actual = queue.pop(0)
            if actual.paciente.triaje == triaje:
                pacientes_info += f"Nombre: {actual.paciente.nombre} | Triaje: {actual.paciente.triaje}\n"
            if actual.izquierda:
                queue.append(actual.izquierda)
            if actual.derecha:
                queue.append(actual.derecha)
        return pacientes_info

    def eliminar_paciente_cola(self, nombre):
        self.raiz = self._eliminar_nodo_por_nombre(self.raiz, nombre)

    def _eliminar_nodo_por_nombre(self, nodo, nombre):
        if not nodo:
            return None
        if nodo.paciente.nombre == nombre:
            self.size -= 1
            last_node = self._get_last_node()
            if nodo == last_node:
                return None
            nodo.paciente = last_node.paciente
            if last_node.padre:
                if last_node.padre.derecha == last_node:
                    last_node.padre.derecha = None
                else:
                    last_node.padre.izquierda = None
            self._heapify_down(nodo)
            return nodo
        nodo.izquierda = self._eliminar_nodo_por_nombre(nodo.izquierda, nombre)
        nodo.derecha = self._eliminar_nodo_por_nombre(nodo.derecha, nombre)
        return nodo


class ColaPacientesConsola:
    def __init__(self):
        self.cola_pacientes = HeapMin()
        self.menu()

    def menu(self):
        while True:
            print("\nCola de Pacientes")
            print("1. Registrar Paciente")
            print("2. Consultar Próximo Paciente")
            print("3. Atender Siguiente Paciente")
            print("4. Consultar Pacientes en Espera")
            print("5. Consultar Pacientes por Triaje")
            print("6. Eliminar Paciente")
            print("7. Salir")
            opcion = input("Seleccione una opción: ")

            if opcion == '1':
                self.registrar_paciente()
            elif opcion == '2':
                self.consultar_proximo_paciente()
            elif opcion == '3':
                self.atender_siguiente_paciente()
            elif opcion == '4':
                self.consultar_pacientes_espera()
            elif opcion == '5':
                self.consultar_pacientes_por_triaje()
            elif opcion == '6':
                self.eliminar_paciente()
            elif opcion == '7':
                break
            else:
                print("Opción no válida. Por favor, intente de nuevo.")

    def registrar_paciente(self):
        try:
            numero_paciente = int(input("Número de Paciente: "))
            genero = input("Género: ")
            nombre = input("Nombre: ")
            edad = int(input("Edad: "))
            triaje = int(input("Triaje: "))
            paciente = Paciente(numero_paciente, genero, nombre, edad, triaje)
            self.cola_pacientes.insertar(paciente)
            print("Paciente registrado exitosamente.")
        except ValueError:
            print("Error: Por favor, ingrese datos válidos.")

    def consultar_proximo_paciente(self):
        proximo_paciente = self.cola_pacientes.consultar_proximo()
        if proximo_paciente:
            print(f"Próximo paciente a ser atendido: {proximo_paciente.nombre}")
        else:
            print("No hay pacientes en espera.")

    def atender_siguiente_paciente(self):
        paciente_atendido = self.cola_pacientes.atender_siguiente()
        if paciente_atendido:
            print(f"Paciente atendido: {paciente_atendido.nombre}")
        else:
            print("No hay pacientes en espera.")

    def consultar_pacientes_espera(self):
        pacientes_espera_info = self.cola_pacientes.consultar_pacientes_espera()
        if pacientes_espera_info:
            print("Pacientes en espera:")
            print(pacientes_espera_info)
        else:
            print("No hay pacientes en espera.")

    def consultar_pacientes_por_triaje(self):
        try:
            triaje = int(input("Triaje: "))
            pacientes_info = self.cola_pacientes.consultar_pacientes_por_triaje(triaje)
            if pacientes_info:
                print("Pacientes con triaje", triaje, ":")
                print(pacientes_info)
            else:
                print(f"No hay pacientes en espera con triaje {triaje}.")
        except ValueError:
            print("Error: Por favor, ingrese un triaje válido.")

    def eliminar_paciente(self):
        nombre = input("Nombre del Paciente a eliminar: ")
        if nombre:
            self.cola_pacientes.eliminar_paciente_cola(nombre)
            print(f"Paciente {nombre} eliminado exitosamente.")
        else:
            print("Error: Por favor, ingrese el nombre del paciente a eliminar.")


if __name__ == "__main__":
    ColaPacientesConsola()
