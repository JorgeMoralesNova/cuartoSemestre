from flask import Flask, render_template, request, redirect

app = Flask(__name__)

class Empleado:
    def __init__(self, nombre, salario):
        self.nombre = nombre
        self.salario = salario
        self.siguiente = None

class EmpleadoService:
    def __init__(self):
        self.primero = None

    def insertar_empleado(self, empleado):
        if not self.primero:
            self.primero = empleado
            empleado.siguiente = self.primero
        else:
            actual = self.primero
            while actual.siguiente != self.primero:
                actual = actual.siguiente
            actual.siguiente = empleado
            empleado.siguiente = self.primero

    def buscar_salario(self, nombre):
        actual = self.primero
        while actual:
            if actual.nombre == nombre:
                return actual.salario
            actual = actual.siguiente
            if actual == self.primero:
                break
        return None

    def obtener_empleados(self):
        empleados = []
        actual = self.primero
        while actual:
            empleados.append({'nombre': actual.nombre, 'salario': actual.salario})
            actual = actual.siguiente
            if actual == self.primero:
                break
        return empleados

    def actualizar_salario(self, nombre, nuevo_salario):
        actual = self.primero
        while actual:
            if actual.nombre == nombre:
                actual.salario = nuevo_salario
                break
            actual = actual.siguiente
            if actual == self.primero:
                break

    def eliminar_empleado(self, nombre):
        actual = self.primero
        anterior = None
        while actual:
            if actual.nombre == nombre:
                if anterior:
                    anterior.siguiente = actual.siguiente
                    if actual == self.primero:
                        self.primero = anterior.siguiente
                else:
                    if actual.siguiente == self.primero:
                        self.primero = None
                    else:
                        anterior = actual
                        while actual.siguiente != self.primero:
                            actual = actual.siguiente
                        actual.siguiente = anterior.siguiente
                        self.primero = anterior.siguiente
                break
            anterior = actual
            actual = actual.siguiente
            if actual == self.primero:
                break

# Crear una instancia del servicio
empleado_service = EmpleadoService()

# Rutas
@app.route('/')
def mostrar_empleados():
    empleados = empleado_service.obtener_empleados()
    return render_template('index.html', empleados=empleados)

@app.route('/insertar', methods=['POST'])
def insertar_empleado():
    nombre = request.form['nombre']
    salario = float(request.form['salario'])
    empleado = Empleado(nombre, salario)
    empleado_service.insertar_empleado(empleado)
    return redirect('/')

@app.route('/buscar')
def buscar_salario():
    nombre = request.args.get('nombre')
    salario = empleado_service.buscar_salario(nombre)
    return f"El salario de {nombre} es {salario}" if salario is not None else "Empleado no encontrado"

@app.route('/actualizar', methods=['POST'])
def actualizar_salario():
    nombre = request.form['nombre']
    nuevo_salario = float(request.form['nuevo_salario'])
    empleado_service.actualizar_salario(nombre, nuevo_salario)
    return redirect('/')

@app.route('/eliminar', methods=['POST'])
def eliminar_empleado():
    nombre = request.form['nombre']
    empleado_service.eliminar_empleado(nombre)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
