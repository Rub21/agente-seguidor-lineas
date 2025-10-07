"""
Archivo de configuración para el Agente Seguidor de Líneas
Contiene todas las constantes y configuraciones del sistema
"""

# Dimensiones de la ventana
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 900

# Configuración de la cuadrícula
CELL_SIZE = 30
GRID_WIDTH = 25  # Fijo para mejor control
GRID_HEIGHT = 20  # Fijo para mejor control

# Colores del sistema
COLORS = {
    'WHITE': (255, 255, 255),
    'BLACK': (0, 0, 0),
    'GRAY': (128, 128, 128),
    'RED': (255, 0, 0),
    'GREEN': (0, 255, 0),
    'BLUE': (0, 0, 255),
    'YELLOW': (255, 255, 0),
    'CYAN': (0, 255, 255),
    'MAGENTA': (255, 0, 255)
}

# Configuración del agente
AGENT_CONFIG = {
    'INITIAL_ORIENTATION': 0,  # 0: arriba, 1: derecha, 2: abajo, 3: izquierda
    'MOVEMENT_SPEED': 5,  # FPS para el movimiento
    'SENSOR_RANGE': 1,  # Rango de sensores del agente
}

# Configuración del entorno
ENVIRONMENT_CONFIG = {
    'LINE_LENGTH_MIN': 20,
    'LINE_LENGTH_MAX': 50,
    'GRID_VALUE_LINE': 1,
    'GRID_VALUE_EMPTY': 0,
}

# Configuración de la interfaz
UI_CONFIG = {
    'FONT_SIZE': 20,
    'TEXT_MARGIN': 15,
    'TEXT_SPACING': 25,
    'WINDOW_TITLE': "Agente Seguidor de Líneas",
    'BUTTON_WIDTH': 120,
    'BUTTON_HEIGHT': 30,
    'BUTTON_MARGIN': 6,
    'TOP_PANEL_HEIGHT': 120,  # Más espacio para título y botones
    'GRID_PANEL_Y': 120,
    'GRID_PANEL_HEIGHT': WINDOW_HEIGHT - 120,
    'INFO_PANEL_WIDTH': 350,  # Panel más ancho
    'INFO_PANEL_X': WINDOW_WIDTH - 350,
    'GRID_AREA_WIDTH': GRID_WIDTH * CELL_SIZE,
    'GRID_AREA_HEIGHT': GRID_HEIGHT * CELL_SIZE,
    'GRID_START_X': 20,  # Margen izquierdo del grid
    'GRID_START_Y': 120   # Margen superior del grid
}

# Direcciones del agente
DIRECTIONS = {
    'UP': 0,
    'RIGHT': 1,
    'DOWN': 2,
    'LEFT': 3
}

# Símbolos de orientación
ORIENTATION_SYMBOLS = ['▲', '►', '▼', '◄']

# Estados de percepción
PERCEPTION_STATES = {
    'DARK_FLOOR': 'Piso Oscuro',
    'LIGHT_FLOOR': 'Piso no Oscuro',
    'BORDER': 'Borde',
    'CONTACT': 'Contacto',
    'NO_CONTACT': 'No Contacto'
}

# Acciones del agente
ACTIONS = {
    'MOVE_FORWARD': 'move_forward',
    'ROTATE_LEFT': 'rotate_left',
    'ROTATE_RIGHT': 'rotate_right',
    'ROTATE_180': 'rotate_180'
}

# Configuración de botones
BUTTONS = {
    'RANDOM_LINES': 'Generar Líneas Aleatorias',
    'RANDOM_AGENT': 'Posición Aleatoria del Agente',
    'RESET_AGENT': 'Reiniciar Agente',
    'CLEAR_GRID': 'Limpiar Cuadrícula',
    'PAUSE': 'Pausar/Continuar',
    'CLEAR_LOG': 'Limpiar Log',
    'EXPORT_LOG': 'Exportar Log',
    'PRINT_TABLE': 'Imprimir Tabla'
}
