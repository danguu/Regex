import tkinter as tk
from tkinter import messagebox
from validacion import Validacion
from visualizador_registros import VisualizadorRegistros  

class RegistroVehiculoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Registro de Vehículo")
        self.root.geometry("500x750")  
        self.root.resizable(False, False)
        
        # Diccionario para almacenar los campos de entrada
        self.entries = {}
        
        # Inicializar visualizador de registros
        self.visualizador = VisualizadorRegistros(root)  # NUEVA LÍNEA
        
        # Crear los campos del formulario
        self.crear_formulario()
        
        # Botones
        self.crear_botones()
        
    def crear_formulario(self):
        """Crea todos los campos del formulario"""
        campos = [
            ("Placa del vehículo:", "placa"),
            ("Marca:", "marca"),
            ("Modelo (año):", "modelo"),
            ("Color:", "color"),
            ("Número de chasis:", "chasis"),
            ("Número de motor:", "motor"),
            ("Cédula del propietario:", "cedula"),
            ("Nombre del propietario:", "nombre"),
            ("Correo electrónico:", "correo"),
            ("Teléfono de contacto:", "telefono")
        ]
        
        for i, (label_text, campo) in enumerate(campos):
            # Label
            label = tk.Label(self.root, text=label_text, font=("Arial", 10))
            label.place(x=50, y=30 + i*60)
            
            # Entry
            entry = tk.Entry(self.root, font=("Arial", 10), width=30)
            entry.place(x=250, y=30 + i*60)
            
            # Label para mensaje de error
            error_label = tk.Label(self.root, text="", fg="red", font=("Arial", 8))
            error_label.place(x=250, y=55 + i*60)
            
            # Guardar referencia
            self.entries[campo] = {
                'entry': entry,
                'error_label': error_label
            }
    
    def crear_botones(self):
        """Crea los botones del formulario"""
        # Botón Guardar
        btn_guardar = tk.Button(
            self.root, 
            text="Guardar Registro", 
            command=self.validar_registro,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 11),
            width=15
        )
        btn_guardar.place(x=120, y=660)  
        
        # Botón Limpiar
        btn_limpiar = tk.Button(
            self.root, 
            text="Limpiar", 
            command=self.limpiar_campos,
            bg="#f44336",
            fg="white",
            font=("Arial", 11),
            width=15
        )
        btn_limpiar.place(x=250, y=660)  
        
        # Botón Ver Registros
        btn_ver_registros = tk.Button(
            self.root,
            text="Ver Registros Guardados",
            command=self.visualizador.mostrar_ventana,
            bg="#3498db",
            fg="white",
            font=("Arial", 11),
            width=32
        )
        btn_ver_registros.place(x=120, y=700)  
    
    def limpiar_campos(self):
        """Limpia todos los campos del formulario y mensajes de error"""
        for campo in self.entries.values():
            campo['entry'].delete(0, tk.END)
            campo['entry'].config(bg="white")
            campo['error_label'].config(text="")
    
    def validar_registro(self):
        """Valida todos los campos del formulario"""
        resultados_validacion = {}
        campos_validos = True
        datos_vehiculo = {}  # diccionario para guardar datos


        # Validar cada campo
        for campo, datos in self.entries.items():
            valor = datos['entry'].get().strip()
            
            # Limpiar mensajes de error anteriores
            datos['error_label'].config(text="")
            datos['entry'].config(bg="white")
            
            # Verificar campos vacíos
            if not valor:
                self.mostrar_error(campo, "Campo obligatorio")
                valido = False
            else:
                # Validar según el campo
                if campo == 'placa':
                    valido = Validacion.validar_placa(valor)
                    if not valido:
                        self.mostrar_error(campo, "Formato inválido. Ej: ABC123 o ABC12D")
                
                elif campo == 'marca':
                    valido = Validacion.validar_marca(valor)
                    if not valido:
                        self.mostrar_error(campo, "Solo letras y espacios")
                
                elif campo == 'modelo':
                    valido = Validacion.validar_modelo(valor)
                    if not valido:
                        self.mostrar_error(campo, "Año entre 1900 y 2026")
                
                elif campo == 'color':
                    valido = Validacion.validar_color(valor)
                    if not valido:
                        self.mostrar_error(campo, "Solo letras")
                
                elif campo == 'chasis':
                    valido = Validacion.validar_chasis(valor)
                    if not valido:
                        self.mostrar_error(campo, "17 caracteres alfanuméricos")
                
                elif campo == 'motor':
                    valido = Validacion.validar_motor(valor)
                    if not valido:
                        self.mostrar_error(campo, "Solo caracteres alfanuméricos")
                
                elif campo == 'cedula':
                    valido = Validacion.validar_cedula(valor)
                    if not valido:
                        self.mostrar_error(campo, "7-10 dígitos numéricos")
                
                elif campo == 'nombre':
                    valido = Validacion.validar_nombre(valor)
                    if not valido:
                        self.mostrar_error(campo, "Solo letras y espacios")
                
                elif campo == 'correo':
                    valido = Validacion.validar_correo(valor)
                    if not valido:
                        self.mostrar_error(campo, "Formato: usuario@dominio.com")
                
                elif campo == 'telefono':
                    valido = Validacion.validar_telefono(valor)
                    if not valido:
                        self.mostrar_error(campo, "10 dígitos numéricos")
            
            # Guardar datos del vehículo (solo si el campo tiene valor)
            if valor:
                datos_vehiculo[campo] = valor
            
            resultados_validacion[campo] = valido
            
            if not valido:
                campos_validos = False
        
        # Mostrar resultado final y guardar si es válido
        if campos_validos:
            # Guardar el registro antes de mostrar éxito
            if self.visualizador.guardar_registro(datos_vehiculo):
                self.mostrar_exito()
            else:
                messagebox.showerror("Error", "No se pudo guardar el registro")
    
    def mostrar_error(self, campo, mensaje):
        """Muestra error en el campo específico"""
        if campo in self.entries:
            self.entries[campo]['error_label'].config(text=mensaje)
            self.entries[campo]['entry'].config(bg="#FFE4E1")
    
    def mostrar_exito(self):
        """Muestra mensaje de registro exitoso"""
        messagebox.showinfo(
            "Registro Exitoso", 
            "¡El vehículo ha sido registrado correctamente!"
        )
        self.limpiar_campos()

def main():
    """Función principal"""
    root = tk.Tk()
    app = RegistroVehiculoApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()