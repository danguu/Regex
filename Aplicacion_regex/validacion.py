import re

class Validacion:
    """Clase independiente para validaciones mediante expresiones regulares"""
    
    @staticmethod
    def validar_placa(placa):
        """
        Valida placa colombiana (formato: ABC123 o ABC12D)
        """
        patron = r'^[A-Z]{3}\d{3}$|^[A-Z]{3}\d{2}[A-Z]$'
        return bool(re.match(patron, placa.upper()))
    
    @staticmethod
    def validar_marca(marca):
        """
        Valida marca: solo letras y espacios
        """
        patron = r'^[A-Za-záéíóúÁÉÍÓÚñÑ\s]+$'
        return bool(re.match(patron, marca))
    
    @staticmethod
    def validar_modelo(modelo):
        """
        Valida año: 1900-2026
        """
        try:
            año = int(modelo)
            return 1900 <= año <= 2026
        except ValueError:
            return False
    
    @staticmethod
    def validar_color(color):
        """
        Valida color: solo letras
        """
        patron = r'^[A-Za-záéíóúÁÉÍÓÚñÑ]+$'
        return bool(re.match(patron, color))
    
    @staticmethod
    def validar_chasis(chasis):
        """
        Valida número de chasis: alfanumérico de 17 caracteres
        """
        patron = r'^[A-Za-z0-9]{17}$'
        return bool(re.match(patron, chasis))
    
    @staticmethod
    def validar_motor(motor):
        """
        Valida número de motor: alfanumérico
        """
        patron = r'^[A-Za-z0-9]+$'
        return bool(re.match(patron, motor))
    
    @staticmethod
    def validar_cedula(cedula):
        """
        Valida cédula: solo números de 7-10 dígitos
        """
        patron = r'^\d{7,10}$'
        return bool(re.match(patron, cedula))
    
    @staticmethod
    def validar_nombre(nombre):
        """
        Valida nombre: solo letras y espacios
        """
        patron = r'^[A-Za-záéíóúÁÉÍÓÚñÑ\s]+$'
        return bool(re.match(patron, nombre))
    
    @staticmethod
    def validar_correo(correo):
        """
        Valida correo electrónico: formato usuario@dominio.com
        """
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(patron, correo))
    
    @staticmethod
    def validar_telefono(telefono):
        """
        Valida teléfono: 10 dígitos
        """
        patron = r'^\d{10}$'
        return bool(re.match(patron, telefono))