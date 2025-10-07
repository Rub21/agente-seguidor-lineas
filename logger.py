"""
Módulo de logging para el Agente Seguidor de Líneas
Registra cada paso del agente con sus percepciones y acciones
"""

import csv
import os
from datetime import datetime
from config import PERCEPTION_STATES, ACTIONS


class AgentLogger:
    """
    Clase para registrar y mostrar el comportamiento del agente
    """
    
    def __init__(self):
        """
        Inicializa el logger del agente
        """
        self.steps = []
        self.current_step = 0
        self.log_file = None
        
    def log_step(self, agent, perceptions, action_taken):
        """
        Registra un paso del agente
        
        Args:
            agent: Instancia del agente
            perceptions (dict): Percepciones del agente
            action_taken (str): Acción tomada por el agente
        """
        self.current_step += 1
        
        # Convertir percepciones a valores binarios
        cuerpo = 1 if perceptions['piso'] == PERCEPTION_STATES['DARK_FLOOR'] else 0
        izquierda = 1 if perceptions['izquierda'] == PERCEPTION_STATES['DARK_FLOOR'] else 0
        centro = 1 if perceptions['centro'] == PERCEPTION_STATES['DARK_FLOOR'] else 0
        derecha = 1 if perceptions['derecha'] == PERCEPTION_STATES['DARK_FLOOR'] else 0
        
        # Determinar acción basada en la acción tomada
        if action_taken == 'move_forward':
            accion = 'A'  # Avanzar
        elif action_taken == 'rotate_left':
            accion = 'R-'  # Rotar izquierda
        elif action_taken == 'rotate_right':
            accion = 'R+'  # Rotar derecha
        else:
            accion = 'A'  # Por defecto avanzar
        
        step_data = {
            'paso': self.current_step,
            'cuerpo': cuerpo,
            'izquierda': izquierda,
            'centro': centro,
            'derecha': derecha,
            'accion': accion,
            'posicion_x': agent.x,
            'posicion_y': agent.y,
            'orientacion': agent.orientation,
            'contacto': 1 if agent.has_hit_wall else 0,
            'timestamp': datetime.now().strftime('%H:%M:%S.%f')[:-3]
        }
        
        self.steps.append(step_data)
        
        # Si hay archivo de log, escribir inmediatamente
        if self.log_file:
            self._write_to_file(step_data)
    
    def _write_to_file(self, step_data):
        """
        Escribe un paso al archivo de log
        
        Args:
            step_data (dict): Datos del paso a escribir
        """
        if not self.log_file:
            return
            
        # Crear archivo si no existe
        file_exists = os.path.exists(self.log_file)
        
        with open(self.log_file, 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['paso', 'cuerpo', 'izquierda', 'centro', 'derecha', 'accion', 
                         'posicion_x', 'posicion_y', 'orientacion', 'contacto', 'timestamp']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            # Escribir header si es un archivo nuevo
            if not file_exists:
                writer.writeheader()
            
            writer.writerow(step_data)
    
    def start_logging(self, filename=None):
        """
        Inicia el logging a archivo
        
        Args:
            filename (str): Nombre del archivo de log (opcional)
        """
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'agente_log_{timestamp}.csv'
        
        self.log_file = filename
        print(f"📝 Iniciando log en archivo: {filename}")
    
    def stop_logging(self):
        """
        Detiene el logging a archivo
        """
        if self.log_file:
            print(f"📝 Log guardado en: {self.log_file}")
            self.log_file = None
    
    def get_table_data(self):
        """
        Obtiene los datos de la tabla para mostrar
        
        Returns:
            list: Lista de diccionarios con los datos de cada paso
        """
        return self.steps.copy()
    
    def get_last_n_steps(self, n=10):
        """
        Obtiene los últimos n pasos
        
        Args:
            n (int): Número de pasos a obtener
            
        Returns:
            list: Lista de los últimos n pasos
        """
        return self.steps[-n:] if len(self.steps) >= n else self.steps
    
    def clear_log(self):
        """
        Limpia el log actual
        """
        self.steps = []
        self.current_step = 0
        print("🗑️ Log limpiado")
    
    def print_table(self, max_steps=None):
        """
        Imprime la tabla de pasos en consola
        
        Args:
            max_steps (int): Número máximo de pasos a mostrar (None para todos)
        """
        if not self.steps:
            print("📋 No hay pasos registrados")
            return
        
        steps_to_show = self.steps if max_steps is None else self.steps[-max_steps:]
        
        print("\n" + "="*80)
        print("📋 TABLA DE PASOS DEL AGENTE")
        print("="*80)
        print(f"{'Paso':<4} {'Cuerpo':<6} {'Izq':<4} {'Centro':<6} {'Der':<4} {'Acción':<6} {'Pos':<8} {'Orient':<6} {'Contacto':<8}")
        print("-"*80)
        
        for step in steps_to_show:
            pos_str = f"({step['posicion_x']},{step['posicion_y']})"
            orient_str = f"{step['orientacion']}"
            contacto_str = "Sí" if step['contacto'] else "No"
            
            print(f"{step['paso']:<4} {step['cuerpo']:<6} {step['izquierda']:<4} {step['centro']:<6} {step['derecha']:<4} {step['accion']:<6} {pos_str:<8} {orient_str:<6} {contacto_str:<8}")
        
        print("="*80)
        print(f"Total de pasos: {len(self.steps)}")
        print("="*80 + "\n")
    
    def export_to_csv(self, filename=None):
        """
        Exporta el log completo a un archivo CSV
        
        Args:
            filename (str): Nombre del archivo (opcional)
        """
        if not self.steps:
            print("📋 No hay datos para exportar")
            return
        
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'agente_export_{timestamp}.csv'
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['paso', 'cuerpo', 'izquierda', 'centro', 'derecha', 'accion', 
                         'posicion_x', 'posicion_y', 'orientacion', 'contacto', 'timestamp']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for step in self.steps:
                writer.writerow(step)
        
        print(f"📊 Datos exportados a: {filename}")


def create_logger():
    """
    Función de conveniencia para crear un nuevo logger
    
    Returns:
        AgentLogger: Instancia del logger creado
    """
    return AgentLogger()
