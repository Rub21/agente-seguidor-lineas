"""
Módulo de lógica del agente para el Agente Seguidor de Líneas
Contiene la implementación del agente inteligente con sus percepciones y acciones
"""

import random
from config import (
    AGENT_CONFIG, DIRECTIONS, ORIENTATION_SYMBOLS, 
    PERCEPTION_STATES, ACTIONS
)


class LineFollowerAgent:
    """
    Clase que representa el agente seguidor de líneas
    """
    
    def __init__(self, x, y, grid_width, grid_height):
        """
        Inicializa el agente en la posición especificada
        
        Args:
            x (int): Posición inicial x
            y (int): Posición inicial y
            grid_width (int): Ancho de la cuadrícula
            grid_height (int): Alto de la cuadrícula
        """
        self.x = x
        self.y = y
        self.orientation = AGENT_CONFIG['INITIAL_ORIENTATION']
        self.has_hit_wall = False
        self.grid_width = grid_width
        self.grid_height = grid_height
        
    def rotate(self, direction):
        """
        Rota el agente en la dirección especificada
        
        Args:
            direction (int): 0 para izquierda, 1 para derecha
        """
        if direction == 0:  # Rotar izquierda
            self.orientation = (self.orientation - 1) % 4
        else:  # Rotar derecha
            self.orientation = (self.orientation + 1) % 4
            
    def move_forward(self):
        """
        Mueve el agente hacia adelante según su orientación actual
        """
        dx, dy = 0, 0
        
        # Calcular dirección de movimiento según orientación
        if self.orientation == DIRECTIONS['UP']:  # Arriba
            dy = -1
        elif self.orientation == DIRECTIONS['RIGHT']:  # Derecha
            dx = 1
        elif self.orientation == DIRECTIONS['DOWN']:  # Abajo
            dy = 1
        elif self.orientation == DIRECTIONS['LEFT']:  # Izquierda
            dx = -1
            
        new_x, new_y = self.x + dx, self.y + dy
        
        # Verificar límites
        if 0 <= new_x < self.grid_width and 0 <= new_y < self.grid_height:
            self.x, self.y = new_x, new_y
            self.has_hit_wall = False
        else:
            self.has_hit_wall = True
            
    def perceive(self, environment):
        """
        Obtiene las percepciones del agente del entorno
        
        Args:
            environment: Instancia del entorno
            
        Returns:
            dict: Diccionario con las percepciones del agente
        """
        # Orientación actual
        orientation_symbol = ORIENTATION_SYMBOLS[self.orientation]
        
        # Estado de contacto con paredes
        contact = PERCEPTION_STATES['CONTACT'] if self.has_hit_wall else PERCEPTION_STATES['NO_CONTACT']
        
        # Cámara bajo el agente
        piso = PERCEPTION_STATES['DARK_FLOOR'] if environment.is_line_at(self.x, self.y) else PERCEPTION_STATES['LIGHT_FLOOR']
        
        # Cámaras adelante (izquierda, centro, derecha)
        perceptions = []
        for i in range(-1, 2):
            # Calcular la dirección relativa
            rel_dir = (self.orientation + i) % 4
            dx, dy = 0, 0
            
            if rel_dir == DIRECTIONS['UP']:  # Arriba
                dy = -1
            elif rel_dir == DIRECTIONS['RIGHT']:  # Derecha
                dx = 1
            elif rel_dir == DIRECTIONS['DOWN']:  # Abajo
                dy = 1
            elif rel_dir == DIRECTIONS['LEFT']:  # Izquierda
                dx = -1
                
            cam_x, cam_y = self.x + dx, self.y + dy
            
            # Verificar si está dentro de los límites
            if environment.is_valid_position(cam_x, cam_y):
                if environment.is_line_at(cam_x, cam_y):
                    perceptions.append(PERCEPTION_STATES['DARK_FLOOR'])
                else:
                    perceptions.append(PERCEPTION_STATES['LIGHT_FLOOR'])
            else:
                perceptions.append(PERCEPTION_STATES['BORDER'])
                
        return {
            'orientacion': orientation_symbol,
            'contacto': contact,
            'piso': piso,
            'izquierda': perceptions[0],
            'centro': perceptions[1],
            'derecha': perceptions[2]
        }
        
    def act(self, perceptions):
        """
        Ejecuta una acción basada en las percepciones actuales
        
        Args:
            perceptions (dict): Diccionario con las percepciones del agente
            
        Returns:
            str: Nombre de la acción tomada
        """
        # Tabla de percepción-acción
        if perceptions['piso'] == PERCEPTION_STATES['DARK_FLOOR'] or perceptions['centro'] == PERCEPTION_STATES['DARK_FLOOR']:
            # Avanzar si está sobre línea o hay línea al frente
            self.move_forward()
            return 'move_forward'
            
        elif perceptions['izquierda'] == PERCEPTION_STATES['DARK_FLOOR']:
            # Rotar izquierda si hay línea a la izquierda
            self.rotate(0)  # Rotar izquierda
            self.move_forward()
            return 'rotate_left'
            
        elif perceptions['derecha'] == PERCEPTION_STATES['DARK_FLOOR']:
            # Rotar derecha si hay línea a la derecha
            self.rotate(1)  # Rotar derecha
            self.move_forward()
            return 'rotate_right'
            
        elif perceptions['contacto'] == PERCEPTION_STATES['CONTACT']:
            # Girar 180 grados si hay contacto con pared
            self.rotate(1)
            self.rotate(1)
            self.move_forward()
            return 'rotate_180'
            
        else:
            # Buscar línea avanzando
            self.move_forward()
            return 'move_forward'
    
    def get_position(self):
        """
        Obtiene la posición actual del agente
        
        Returns:
            tuple: (x, y) posición actual
        """
        return (self.x, self.y)
    
    def get_orientation(self):
        """
        Obtiene la orientación actual del agente
        
        Returns:
            int: Orientación actual (0-3)
        """
        return self.orientation
    
    def reset_position(self, x, y):
        """
        Reinicia la posición del agente
        
        Args:
            x (int): Nueva posición x
            y (int): Nueva posición y
        """
        self.x = x
        self.y = y
        self.orientation = AGENT_CONFIG['INITIAL_ORIENTATION']
        self.has_hit_wall = False


def create_agent(x, y, grid_width, grid_height):
    """
    Función de conveniencia para crear un nuevo agente
    
    Args:
        x (int): Posición inicial x
        y (int): Posición inicial y
        grid_width (int): Ancho de la cuadrícula
        grid_height (int): Alto de la cuadrícula
        
    Returns:
        LineFollowerAgent: Instancia del agente creado
    """
    return LineFollowerAgent(x, y, grid_width, grid_height)
