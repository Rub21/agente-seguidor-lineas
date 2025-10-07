"""
Módulo de lógica del entorno para el Agente Seguidor de Líneas
Contiene la generación de líneas y la gestión del entorno
"""

import random
from config import ENVIRONMENT_CONFIG, DIRECTIONS


class Environment:
    """
    Clase que representa el entorno donde se mueve el agente
    """
    
    def __init__(self, width, height):
        """
        Inicializa el entorno con las dimensiones especificadas
        
        Args:
            width (int): Ancho de la cuadrícula
            height (int): Alto de la cuadrícula
        """
        self.width = width
        self.height = height
        self.grid = self._create_empty_grid()
        
    def _create_empty_grid(self):
        """
        Crea una cuadrícula vacía
        
        Returns:
            list: Cuadrícula vacía inicializada con ceros
        """
        return [[ENVIRONMENT_CONFIG['GRID_VALUE_EMPTY'] for _ in range(self.width)] 
                for _ in range(self.height)]
    
    def generate_line(self):
        """
        Genera múltiples grupos de líneas separados en la cuadrícula
        
        Returns:
            list: Cuadrícula con los grupos de líneas generados
        """
        # Reiniciar la cuadrícula
        self.grid = self._create_empty_grid()
        
        # Generar exactamente 6 grupos de líneas (uno por área)
        num_groups = 6
        
        for group in range(num_groups):
            self._generate_line_group(group)
            
        return self.grid
    
    def _generate_line_group(self, group_id):
        """
        Genera un grupo específico de líneas
        
        Args:
            group_id (int): Identificador del grupo
        """
        # Definir áreas para cada grupo para evitar solapamiento
        area_width = self.width // 3
        area_height = self.height // 2
        
        # Calcular posición base del grupo
        if group_id < 3:
            # Grupos en la parte superior
            base_x = group_id * area_width
            base_y = 0
        else:
            # Grupos en la parte inferior
            base_x = (group_id - 3) * area_width
            base_y = area_height
        
        # Asegurar que no se salga de los límites
        base_x = min(base_x, self.width - 5)
        base_y = min(base_y, self.height - 5)
        
        # Posición inicial aleatoria dentro del área del grupo
        x = base_x + random.randint(0, min(area_width - 1, 4))
        y = base_y + random.randint(0, min(area_height - 1, 4))
        
        # Asegurar que esté dentro de los límites
        x = min(x, self.width - 1)
        y = min(y, self.height - 1)
        
        # Marcar la posición inicial
        self.grid[y][x] = ENVIRONMENT_CONFIG['GRID_VALUE_LINE']
        
        # Direcciones posibles
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        
        # Generar líneas en este grupo con longitud variable
        length = random.randint(8, 15)  # Líneas más cortas por grupo
        
        for _ in range(length):
            # Elegir una dirección aleatoria
            dx, dy = random.choice(directions)
            new_x, new_y = x + dx, y + dy
            
            # Verificar límites y que no se salga del área del grupo
            if (0 <= new_x < self.width and 
                0 <= new_y < self.height and
                base_x <= new_x < base_x + area_width and
                base_y <= new_y < base_y + area_height):
                x, y = new_x, new_y
                self.grid[y][x] = ENVIRONMENT_CONFIG['GRID_VALUE_LINE']
            else:
                # Si no puede continuar en esa dirección, elegir otra
                valid_dirs = []
                for dir_x, dir_y in directions:
                    test_x, test_y = x + dir_x, y + dir_y
                    if (0 <= test_x < self.width and 
                        0 <= test_y < self.height and
                        base_x <= test_x < base_x + area_width and
                        base_y <= test_y < base_y + area_height):
                        valid_dirs.append((dir_x, dir_y))
                
                if valid_dirs:
                    dx, dy = random.choice(valid_dirs)
                    x, y = x + dx, y + dy
                    self.grid[y][x] = ENVIRONMENT_CONFIG['GRID_VALUE_LINE']
                else:
                    # Si no hay direcciones válidas, terminar este grupo
                    break
    
    def get_cell_value(self, x, y):
        """
        Obtiene el valor de una celda específica
        
        Args:
            x (int): Coordenada x
            y (int): Coordenada y
            
        Returns:
            int: Valor de la celda o None si está fuera de límites
        """
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x]
        return None
    
    def is_valid_position(self, x, y):
        """
        Verifica si una posición es válida dentro del entorno
        
        Args:
            x (int): Coordenada x
            y (int): Coordenada y
            
        Returns:
            bool: True si la posición es válida, False en caso contrario
        """
        return 0 <= x < self.width and 0 <= y < self.height
    
    def is_line_at(self, x, y):
        """
        Verifica si hay una línea en la posición especificada
        
        Args:
            x (int): Coordenada x
            y (int): Coordenada y
            
        Returns:
            bool: True si hay línea, False en caso contrario
        """
        if not self.is_valid_position(x, y):
            return False
        return self.grid[y][x] == ENVIRONMENT_CONFIG['GRID_VALUE_LINE']
    
    def get_grid(self):
        """
        Obtiene la cuadrícula completa
        
        Returns:
            list: Cuadrícula del entorno
        """
        return self.grid
    
    def reset(self):
        """
        Reinicia el entorno a su estado inicial
        """
        self.grid = self._create_empty_grid()


def create_environment(width, height):
    """
    Función de conveniencia para crear un nuevo entorno
    
    Args:
        width (int): Ancho del entorno
        height (int): Alto del entorno
        
    Returns:
        Environment: Instancia del entorno creado
    """
    return Environment(width, height)
