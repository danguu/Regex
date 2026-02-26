import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

class VisualizadorRegistros:
    """Clase independiente para visualizar los registros guardados"""
    
    def __init__(self, parent):
        self.parent = parent
        self.archivo_registros = "registros_vehiculos.json"
        
    def mostrar_ventana(self):
        """Crea y muestra una ventana con todos los registros"""
        # Crear nueva ventana
        ventana = tk.Toplevel(self.parent)
        ventana.title("Registros de Vehículos Guardados")
        ventana.geometry("1000x650")
        ventana.resizable(True, True)
        
        # Título
        titulo = tk.Label(
            ventana, 
            text="LISTADO DE VEHÍCULOS REGISTRADOS", 
            font=("Arial", 14, "bold"),
            fg="#2c3e50"
        )
        titulo.pack(pady=10)
        
        # Frame para la tabla y scrollbar
        frame_tabla = tk.Frame(ventana)
        frame_tabla.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Crear Treeview (tabla)
        columnas = (
            "Placa", "Marca", "Modelo", "Color", "Chasis", 
            "Motor", "Cédula", "Propietario", "Correo", "Teléfono"
        )
        
        tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=15)
        
        # Configurar columnas
        anchos = [80, 100, 60, 70, 120, 100, 90, 120, 150, 90]
        for col, ancho in zip(columnas, anchos):
            tabla.heading(col, text=col)
            tabla.column(col, width=ancho, minwidth=ancho)
        
        # Scrollbars
        scroll_y = ttk.Scrollbar(frame_tabla, orient=tk.VERTICAL, command=tabla.yview)
        scroll_x = ttk.Scrollbar(frame_tabla, orient=tk.HORIZONTAL, command=tabla.xview)
        tabla.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        
        # Posicionar tabla y scrollbars
        tabla.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")
        
        frame_tabla.grid_rowconfigure(0, weight=1)
        frame_tabla.grid_columnconfigure(0, weight=1)
        
        # Cargar y mostrar registros
        self.cargar_registros_en_tabla(tabla)
        
        # Frame para botones
        frame_botones = tk.Frame(ventana)
        frame_botones.pack(pady=10)
        
        # Botón Actualizar
        btn_actualizar = tk.Button(
            frame_botones,
            text="Actualizar Lista",
            command=lambda: self.actualizar_tabla(tabla, ventana),
            bg="#3498db",
            fg="white",
            font=("Arial", 10),
            width=15
        )
        btn_actualizar.pack(side=tk.LEFT, padx=5)
        
        # Botón Eliminar Registro Seleccionado
        btn_eliminar = tk.Button(
            frame_botones,
            text="Eliminar Registro",
            command=lambda: self.eliminar_registro_seleccionado(tabla, ventana),
            bg="#e74c3c",
            fg="white",
            font=("Arial", 10),
            width=15
        )
        btn_eliminar.pack(side=tk.LEFT, padx=5)
        
        # Botón Cerrar
        btn_cerrar = tk.Button(
            frame_botones,
            text="Cerrar",
            command=ventana.destroy,
            bg="#95a5a6",
            fg="white",
            font=("Arial", 10),
            width=15
        )
        btn_cerrar.pack(side=tk.LEFT, padx=5)
        
        # Etiqueta con conteo de registros
        self.actualizar_conteo(ventana, tabla)
        
        # Instrucción de selección
        label_instruccion = tk.Label(
            ventana,
            text="💡 Para eliminar: selecciona un registro haciendo clic en él y presiona 'Eliminar Registro'",
            font=("Arial", 9, "italic"),
            fg="#7f8c8d"
        )
        label_instruccion.pack(pady=2)
    
    def cargar_registros_en_tabla(self, tabla):
        """
        Carga los registros desde el archivo JSON a la tabla
        """
        try:
            # Limpiar tabla
            for item in tabla.get_children():
                tabla.delete(item)
            
            # Cargar registros
            registros = self.cargar_registros()
            
            if not registros:
                # Mostrar mensaje si no hay registros
                tabla.insert("", tk.END, values=("No hay registros", "", "", "", "", "", "", "", "", ""))
                return
            
            # Insertar registros en la tabla
            for registro in registros:
                # Asegurar que todos los campos existen y convertir a string
                valores = (
                    str(registro.get('placa', '')).strip(),
                    str(registro.get('marca', '')).strip(),
                    str(registro.get('modelo', '')).strip(),
                    str(registro.get('color', '')).strip(),
                    str(registro.get('chasis', '')).strip(),
                    str(registro.get('motor', '')).strip(),
                    str(registro.get('cedula', '')).strip(),
                    str(registro.get('nombre', '')).strip(),
                    str(registro.get('correo', '')).strip(),
                    str(registro.get('telefono', '')).strip()
                )
                tabla.insert("", tk.END, values=valores)
            
            print(f"✅ {len(registros)} registros cargados correctamente")
            
        except Exception as e:
            print(f"❌ Error al cargar registros: {e}")
            messagebox.showerror("Error", f"Error al cargar registros: {str(e)}")
    
    def cargar_registros(self):
        """
        Carga los registros desde el archivo JSON
        """
        if os.path.exists(self.archivo_registros):
            try:
                with open(self.archivo_registros, 'r', encoding='utf-8') as file:
                    contenido = file.read().strip()
                    if contenido:
                        return json.loads(contenido)
                    else:
                        return []
            except json.JSONDecodeError as e:
                print(f"❌ Error al decodificar JSON: {e}")
                return []
            except Exception as e:
                print(f"❌ Error al leer archivo: {e}")
                return []
        else:
            print(f"📁 Archivo {self.archivo_registros} no existe. Creando nuevo...")
            return []
    
    def guardar_registro(self, datos_vehiculo):
        """
        Guarda un nuevo registro en el archivo JSON
        """
        try:
            registros = self.cargar_registros()
            registros.append(datos_vehiculo)
            
            with open(self.archivo_registros, 'w', encoding='utf-8') as file:
                json.dump(registros, file, ensure_ascii=False, indent=4)
            
            print(f"✅ Registro guardado: {datos_vehiculo.get('placa', '')}")
            return True
            
        except Exception as e:
            print(f"❌ Error al guardar registro: {e}")
            return False
    
    def eliminar_registro_seleccionado(self, tabla, ventana):
        """
        Elimina el registro seleccionado de la tabla y del archivo
        """
        # Obtener el elemento seleccionado
        seleccion = tabla.selection()
        
        if not seleccion:
            messagebox.showwarning(
                "Sin selección", 
                "Por favor, selecciona un registro para eliminar."
            )
            return
        
        # Obtener valores del registro seleccionado
        item = tabla.item(seleccion[0])
        valores = item['values']
        
        # Verificar si es el mensaje de "No hay registros"
        if valores[0] == "No hay registros":
            messagebox.showinfo("Información", "No hay registros para eliminar.")
            return
        
        # Crear un diccionario con los datos del registro seleccionado
        registro_seleccionado = {
            'placa': str(valores[0]).strip(),
            'marca': str(valores[1]).strip(),
            'modelo': str(valores[2]).strip(),
            'color': str(valores[3]).strip(),
            'chasis': str(valores[4]).strip(),
            'motor': str(valores[5]).strip(),
            'cedula': str(valores[6]).strip(),
            'nombre': str(valores[7]).strip(),
            'correo': str(valores[8]).strip(),
            'telefono': str(valores[9]).strip()
        }
        
        # Mostrar información del registro a eliminar
        mensaje_confirmacion = f"¿Estás seguro de eliminar el siguiente registro?\n\n"
        mensaje_confirmacion += f"📋 Placa: {valores[0]}\n"
        mensaje_confirmacion += f"👤 Propietario: {valores[7]}\n"
        mensaje_confirmacion += f"🚗 Marca: {valores[1]} - Modelo: {valores[2]}\n"
        mensaje_confirmacion += f"🎨 Color: {valores[3]}"
        
        # Confirmar eliminación
        respuesta = messagebox.askyesno(
            "Confirmar eliminación",
            mensaje_confirmacion,
            icon='warning'
        )
        
        if respuesta:
            # Cargar todos los registros
            registros = self.cargar_registros()
            
            if not registros:
                messagebox.showerror("Error", "No hay registros para eliminar.")
                return
            
            # Buscar y eliminar el registro correspondiente
            registros_actualizados = []
            eliminado = False
            registro_encontrado = None
            
            for registro in registros:
                # Comparar todos los campos importantes
                placa_coincide = str(registro.get('placa', '')).strip() == registro_seleccionado['placa']
                cedula_coincide = str(registro.get('cedula', '')).strip() == registro_seleccionado['cedula']
                chasis_coincide = str(registro.get('chasis', '')).strip() == registro_seleccionado['chasis']
                
                # Si coinciden placa Y (cédula O chasis), consideramos que es el mismo registro
                if placa_coincide and (cedula_coincide or chasis_coincide):
                    eliminado = True
                    registro_encontrado = registro
                    print(f"🗑️ Registro eliminado: {registro}")
                    continue
                
                registros_actualizados.append(registro)
            
            if eliminado:
                # Guardar registros actualizados
                try:
                    with open(self.archivo_registros, 'w', encoding='utf-8') as file:
                        json.dump(registros_actualizados, file, ensure_ascii=False, indent=4)
                    
                    # Actualizar tabla
                    self.actualizar_tabla(tabla, ventana)
                    
                    messagebox.showinfo(
                        "✅ Registro eliminado",
                        "El registro ha sido eliminado correctamente."
                    )
                    
                except Exception as e:
                    messagebox.showerror(
                        "❌ Error",
                        f"No se pudo eliminar el registro: {str(e)}"
                    )
            else:
                # Mostrar información de depuración
                print("🔍 Registro buscado:", registro_seleccionado)
                print("📋 Registros en archivo:", registros)
                
                messagebox.showerror(
                    "❌ Error",
                    "No se pudo encontrar el registro para eliminar.\n"
                    "Por favor, actualiza la lista e intenta nuevamente."
                )
    
    def actualizar_tabla(self, tabla, ventana):
        """
        Actualiza la tabla con los registros más recientes
        """
        self.cargar_registros_en_tabla(tabla)
        self.actualizar_conteo(ventana, tabla)
    
    def actualizar_conteo(self, ventana, tabla):
        """
        Actualiza el contador de registros
        """
        total_registros = len(tabla.get_children())
        
        # Verificar si hay registros reales (no el mensaje de "No hay registros")
        if total_registros == 1:
            item = tabla.get_children()[0]
            valores = tabla.item(item)['values']
            if valores[0] == "No hay registros":
                total_registros = 0
        
        # Eliminar label anterior si existe
        for widget in ventana.winfo_children():
            if isinstance(widget, tk.Label) and "registros encontrados" in widget.cget("text"):
                widget.destroy()
        
        # Crear nuevo label con conteo
        label_conteo = tk.Label(
            ventana,
            text=f"Total de registros: {total_registros} vehículo(s) encontrado(s)",
            font=("Arial", 10, "italic"),
            fg="#7f8c8d"
        )
        label_conteo.pack(pady=5)