"""
Módulo de interfaz para el Agente Seguidor de Líneas
Contiene la visualización y la interfaz de usuario
"""

import pygame
import sys
from config import (
    WINDOW_WIDTH, WINDOW_HEIGHT, CELL_SIZE, COLORS, 
    UI_CONFIG, DIRECTIONS, ENVIRONMENT_CONFIG, BUTTONS
)


class LineFollowerInterface:
    """
    Clase que maneja la interfaz gráfica del agente seguidor de líneas
    """
    
    def __init__(self):
        """
        Inicializa la interfaz gráfica
        """
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(UI_CONFIG['WINDOW_TITLE'])
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, UI_CONFIG['FONT_SIZE'])
        self.buttons = self._create_buttons()
        self.paused = False
        
    def _create_buttons(self):
        """
        Crea los botones de control en la parte superior
        
        Returns:
            dict: Diccionario con los botones creados
        """
        buttons = {}
        button_x = UI_CONFIG['TEXT_MARGIN']
        button_y = UI_CONFIG['TEXT_MARGIN'] + 40  # Espacio para el título
        
        # Área disponible para botones (sin el panel de información)
        available_width = UI_CONFIG['INFO_PANEL_X'] - UI_CONFIG['TEXT_MARGIN'] * 2
        
        # Calcular cuántos botones caben en una fila
        buttons_per_row = available_width // (UI_CONFIG['BUTTON_WIDTH'] + UI_CONFIG['BUTTON_MARGIN'])
        
        for i, (key, text) in enumerate(BUTTONS.items()):
            row = i // buttons_per_row
            col = i % buttons_per_row
            
            rect = pygame.Rect(
                button_x + col * (UI_CONFIG['BUTTON_WIDTH'] + UI_CONFIG['BUTTON_MARGIN']),
                button_y + row * (UI_CONFIG['BUTTON_HEIGHT'] + UI_CONFIG['BUTTON_MARGIN']),
                UI_CONFIG['BUTTON_WIDTH'], 
                UI_CONFIG['BUTTON_HEIGHT']
            )
            buttons[key] = {'rect': rect, 'text': text, 'pressed': False}
            
        return buttons
        
    def draw_buttons(self):
        """
        Dibuja todos los botones en pantalla
        """
        for button_data in self.buttons.values():
            rect = button_data['rect']
            text = button_data['text']
            
            # Color del botón según estado
            color = COLORS['GREEN'] if button_data['pressed'] else COLORS['GRAY']
            
            # Dibujar botón
            pygame.draw.rect(self.screen, color, rect)
            pygame.draw.rect(self.screen, COLORS['BLACK'], rect, 2)
            
            # Dibujar texto del botón
            text_surface = self.font.render(text, True, COLORS['BLACK'])
            text_rect = text_surface.get_rect(center=rect.center)
            self.screen.blit(text_surface, text_rect)
            
    def handle_button_click(self, pos):
        """
        Maneja el clic en los botones
        
        Args:
            pos (tuple): Posición del clic (x, y)
            
        Returns:
            str: Nombre del botón clickeado o None
        """
        for button_name, button_data in self.buttons.items():
            if button_data['rect'].collidepoint(pos):
                button_data['pressed'] = True
                return button_name
        return None
        
    def reset_button_states(self):
        """
        Reinicia el estado de todos los botones
        """
        for button_data in self.buttons.values():
            button_data['pressed'] = False
        
    def draw_grid(self, environment, agent):
        """
        Dibuja la cuadrícula del entorno y el agente en el panel inferior
        
        Args:
            environment: Instancia del entorno
            agent: Instancia del agente
        """
        grid = environment.get_grid()
        grid_width = len(grid[0])
        grid_height = len(grid)
        
        # Dibujar fondo del panel de la cuadrícula
        grid_panel_rect = pygame.Rect(0, UI_CONFIG['GRID_PANEL_Y'], 
                                     UI_CONFIG['INFO_PANEL_X'], 
                                     UI_CONFIG['GRID_PANEL_HEIGHT'])
        pygame.draw.rect(self.screen, COLORS['WHITE'], grid_panel_rect)
        
        # Dibujar celdas de la cuadrícula con offset para centrar
        for y in range(grid_height):
            for x in range(grid_width):
                rect = pygame.Rect(
                    UI_CONFIG['GRID_START_X'] + x * CELL_SIZE, 
                    UI_CONFIG['GRID_START_Y'] + y * CELL_SIZE, 
                    CELL_SIZE, 
                    CELL_SIZE
                )
                
                # Colorear según el contenido de la celda
                if grid[y][x] == ENVIRONMENT_CONFIG['GRID_VALUE_LINE']:
                    pygame.draw.rect(self.screen, COLORS['BLACK'], rect)
                else:
                    pygame.draw.rect(self.screen, COLORS['WHITE'], rect)
                    
                # Dibujar borde de la celda
                pygame.draw.rect(self.screen, COLORS['GRAY'], rect, 1)
        
        # Dibujar el agente
        self._draw_agent(agent)
        
        # Dibujar línea divisoria entre cuadrícula y panel de información
        divider_x = UI_CONFIG['INFO_PANEL_X']
        pygame.draw.line(self.screen, COLORS['BLACK'], 
                        (divider_x, UI_CONFIG['GRID_PANEL_Y']), 
                        (divider_x, WINDOW_HEIGHT), 3)
        
        # Dibujar línea divisoria entre botones y cuadrícula
        pygame.draw.line(self.screen, COLORS['BLACK'], 
                        (0, UI_CONFIG['GRID_PANEL_Y']), 
                        (UI_CONFIG['INFO_PANEL_X'], UI_CONFIG['GRID_PANEL_Y']), 3)
        
    def _draw_agent(self, agent):
        """
        Dibuja el agente en su posición actual
        
        Args:
            agent: Instancia del agente
        """
        # Dibujar cuerpo del agente
        agent_rect = pygame.Rect(
            UI_CONFIG['GRID_START_X'] + agent.x * CELL_SIZE, 
            UI_CONFIG['GRID_START_Y'] + agent.y * CELL_SIZE, 
            CELL_SIZE, 
            CELL_SIZE
        )
        pygame.draw.rect(self.screen, COLORS['RED'], agent_rect)
        
        # Dibujar triángulo para indicar orientación
        points = self._get_orientation_points(agent)
        pygame.draw.polygon(self.screen, COLORS['BLUE'], points)
        
    def _get_orientation_points(self, agent):
        """
        Calcula los puntos del triángulo de orientación del agente
        
        Args:
            agent: Instancia del agente
            
        Returns:
            list: Lista de puntos para dibujar el triángulo
        """
        center_x = UI_CONFIG['GRID_START_X'] + agent.x * CELL_SIZE + CELL_SIZE // 2
        center_y = UI_CONFIG['GRID_START_Y'] + agent.y * CELL_SIZE + CELL_SIZE // 2
        margin = 5
        
        if agent.orientation == DIRECTIONS['UP']:  # Arriba
            points = [
                (center_x, UI_CONFIG['GRID_START_Y'] + agent.y * CELL_SIZE + margin),
                (UI_CONFIG['GRID_START_X'] + agent.x * CELL_SIZE + margin, UI_CONFIG['GRID_START_Y'] + agent.y * CELL_SIZE + CELL_SIZE - margin),
                (UI_CONFIG['GRID_START_X'] + agent.x * CELL_SIZE + CELL_SIZE - margin, UI_CONFIG['GRID_START_Y'] + agent.y * CELL_SIZE + CELL_SIZE - margin)
            ]
        elif agent.orientation == DIRECTIONS['RIGHT']:  # Derecha
            points = [
                (UI_CONFIG['GRID_START_X'] + agent.x * CELL_SIZE + CELL_SIZE - margin, center_y),
                (UI_CONFIG['GRID_START_X'] + agent.x * CELL_SIZE + margin, UI_CONFIG['GRID_START_Y'] + agent.y * CELL_SIZE + margin),
                (UI_CONFIG['GRID_START_X'] + agent.x * CELL_SIZE + margin, UI_CONFIG['GRID_START_Y'] + agent.y * CELL_SIZE + CELL_SIZE - margin)
            ]
        elif agent.orientation == DIRECTIONS['DOWN']:  # Abajo
            points = [
                (center_x, UI_CONFIG['GRID_START_Y'] + agent.y * CELL_SIZE + CELL_SIZE - margin),
                (UI_CONFIG['GRID_START_X'] + agent.x * CELL_SIZE + CELL_SIZE - margin, UI_CONFIG['GRID_START_Y'] + agent.y * CELL_SIZE + margin),
                (UI_CONFIG['GRID_START_X'] + agent.x * CELL_SIZE + margin, UI_CONFIG['GRID_START_Y'] + agent.y * CELL_SIZE + margin)
            ]
        elif agent.orientation == DIRECTIONS['LEFT']:  # Izquierda
            points = [
                (UI_CONFIG['GRID_START_X'] + agent.x * CELL_SIZE + margin, center_y),
                (UI_CONFIG['GRID_START_X'] + agent.x * CELL_SIZE + CELL_SIZE - margin, UI_CONFIG['GRID_START_Y'] + agent.y * CELL_SIZE + CELL_SIZE - margin),
                (UI_CONFIG['GRID_START_X'] + agent.x * CELL_SIZE + CELL_SIZE - margin, UI_CONFIG['GRID_START_Y'] + agent.y * CELL_SIZE + margin)
            ]
        else:
            points = []
            
        return points
        
    def draw_perceptions(self, perceptions):
        """
        Dibuja las percepciones del agente en el panel derecho
        
        Args:
            perceptions (dict): Diccionario con las percepciones del agente
        """
        # Posición del panel de percepciones
        panel_x = UI_CONFIG['INFO_PANEL_X'] + UI_CONFIG['TEXT_MARGIN']
        panel_y = UI_CONFIG['GRID_PANEL_Y'] + UI_CONFIG['TEXT_MARGIN']
        
        # Dibujar fondo del panel de percepciones
        panel_rect = pygame.Rect(
            UI_CONFIG['INFO_PANEL_X'], 
            UI_CONFIG['GRID_PANEL_Y'], 
            UI_CONFIG['INFO_PANEL_WIDTH'], 
            UI_CONFIG['GRID_PANEL_HEIGHT']
        )
        pygame.draw.rect(self.screen, COLORS['GRAY'], panel_rect)
        pygame.draw.rect(self.screen, COLORS['BLACK'], panel_rect, 2)
        
        # Título del panel
        title_text = self.font.render("Percepciones del Agente:", True, COLORS['BLACK'])
        self.screen.blit(title_text, (panel_x, panel_y))
        
        y_offset = panel_y + UI_CONFIG['TEXT_SPACING']
        
        # Dibujar cada percepción
        for key in ['orientacion', 'contacto', 'piso', 'izquierda', 'centro', 'derecha']:
            text = self.font.render(
                f"{key.capitalize()}: {perceptions[key]}", 
                True, 
                COLORS['BLACK']
            )
            self.screen.blit(text, (panel_x, y_offset))
            y_offset += UI_CONFIG['TEXT_SPACING']
            
    def draw_info_panel(self, agent, environment):
        """
        Dibuja un panel de información adicional en el panel derecho
        
        Args:
            agent: Instancia del agente
            environment: Instancia del entorno
        """
        # Posición del panel de información (debajo de las percepciones)
        panel_x = UI_CONFIG['INFO_PANEL_X'] + UI_CONFIG['TEXT_MARGIN']
        panel_y = UI_CONFIG['GRID_PANEL_Y'] + UI_CONFIG['TEXT_SPACING'] * 8  # Después de las percepciones
        
        # Dibujar fondo del panel de información
        info_panel_rect = pygame.Rect(
            UI_CONFIG['INFO_PANEL_X'], 
            panel_y - UI_CONFIG['TEXT_MARGIN'], 
            UI_CONFIG['INFO_PANEL_WIDTH'], 
            200
        )
        pygame.draw.rect(self.screen, COLORS['WHITE'], info_panel_rect)
        pygame.draw.rect(self.screen, COLORS['BLACK'], info_panel_rect, 2)
        
        # Título del panel
        title_text = self.font.render("Información del Sistema:", True, COLORS['BLACK'])
        self.screen.blit(title_text, (panel_x, panel_y))
        
        # Información del agente
        info_texts = [
            f"Posición: ({agent.x}, {agent.y})",
            f"Orientación: {agent.orientation}",
            f"Estado: {'Contacto' if agent.has_hit_wall else 'Libre'}",
            f"Simulación: {'Pausada' if self.paused else 'Activa'}"
        ]
        
        y_offset = panel_y + UI_CONFIG['TEXT_SPACING']
        
        for text in info_texts:
            rendered_text = self.font.render(text, True, COLORS['BLACK'])
            self.screen.blit(rendered_text, (panel_x, y_offset))
            y_offset += UI_CONFIG['TEXT_SPACING']
            
    def draw_top_panel(self):
        """
        Dibuja el panel superior con fondo
        """
        # Dibujar fondo del panel superior
        top_panel_rect = pygame.Rect(0, 0, WINDOW_WIDTH, UI_CONFIG['TOP_PANEL_HEIGHT'])
        pygame.draw.rect(self.screen, COLORS['GRAY'], top_panel_rect)
        
        # Dibujar línea divisoria inferior
        pygame.draw.line(self.screen, COLORS['BLACK'], 
                        (0, UI_CONFIG['TOP_PANEL_HEIGHT']), 
                        (WINDOW_WIDTH, UI_CONFIG['TOP_PANEL_HEIGHT']), 3)
        
        # Dibujar título de la aplicación
        title_text = self.font.render("Agente Seguidor de Líneas", True, COLORS['BLACK'])
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, UI_CONFIG['TOP_PANEL_HEIGHT'] // 2))
        self.screen.blit(title_text, title_rect)
        
    def clear_screen(self):
        """
        Limpia la pantalla con color blanco
        """
        self.screen.fill(COLORS['WHITE'])
        
    def update_display(self):
        """
        Actualiza la pantalla
        """
        pygame.display.flip()
        
    def handle_events(self):
        """
        Maneja los eventos de la interfaz
        
        Returns:
            tuple: (continue_running, button_clicked)
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False, None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False, None
                elif event.key == pygame.K_SPACE:
                    self.paused = not self.paused
                    return True, 'PAUSE'
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Clic izquierdo
                    button_clicked = self.handle_button_click(event.pos)
                    if button_clicked:
                        return True, button_clicked
        return True, None
        
    def tick(self, fps):
        """
        Controla la velocidad de actualización
        
        Args:
            fps (int): Frames por segundo
        """
        self.clock.tick(fps)
        
    def draw_steps_table(self, logger, max_steps=10):
        """
        Dibuja una tabla con los últimos pasos del agente
        
        Args:
            logger: Instancia del logger del agente
            max_steps (int): Número máximo de pasos a mostrar
        """
        steps = logger.get_last_n_steps(max_steps)
        if not steps:
            return
        
        # Posición del panel de tabla
        table_x = UI_CONFIG['INFO_PANEL_X'] + UI_CONFIG['TEXT_MARGIN']
        table_y = UI_CONFIG['GRID_PANEL_Y'] + UI_CONFIG['TEXT_SPACING'] * 12  # Debajo de la información
        
        # Dibujar fondo del panel de tabla
        table_panel_rect = pygame.Rect(
            UI_CONFIG['INFO_PANEL_X'], 
            table_y - UI_CONFIG['TEXT_MARGIN'], 
            UI_CONFIG['INFO_PANEL_WIDTH'], 
            300
        )
        pygame.draw.rect(self.screen, COLORS['WHITE'], table_panel_rect)
        pygame.draw.rect(self.screen, COLORS['BLACK'], table_panel_rect, 2)
        
        # Título del panel
        title_text = self.font.render("Últimos Pasos:", True, COLORS['BLACK'])
        self.screen.blit(title_text, (table_x, table_y))
        
        # Encabezados de la tabla
        header_y = table_y + UI_CONFIG['TEXT_SPACING']
        headers = ['P', 'C', 'I', 'C', 'D', 'A', 'Pos']
        header_x = table_x
        
        for header in headers:
            header_text = self.font.render(header, True, COLORS['BLACK'])
            self.screen.blit(header_text, (header_x, header_y))
            header_x += 35
        
        # Dibujar cada paso
        step_y = header_y + UI_CONFIG['TEXT_SPACING']
        
        for step in steps[-max_steps:]:  # Mostrar solo los últimos pasos
            step_x = table_x
            
            # Paso
            step_text = self.font.render(str(step['paso']), True, COLORS['BLACK'])
            self.screen.blit(step_text, (step_x, step_y))
            step_x += 35
            
            # Cuerpo
            cuerpo_text = self.font.render(str(step['cuerpo']), True, COLORS['BLACK'])
            self.screen.blit(cuerpo_text, (step_x, step_y))
            step_x += 35
            
            # Izquierda
            izq_text = self.font.render(str(step['izquierda']), True, COLORS['BLACK'])
            self.screen.blit(izq_text, (step_x, step_y))
            step_x += 35
            
            # Centro
            cen_text = self.font.render(str(step['centro']), True, COLORS['BLACK'])
            self.screen.blit(cen_text, (step_x, step_y))
            step_x += 35
            
            # Derecha
            der_text = self.font.render(str(step['derecha']), True, COLORS['BLACK'])
            self.screen.blit(der_text, (step_x, step_y))
            step_x += 35
            
            # Acción
            acc_text = self.font.render(step['accion'], True, COLORS['BLACK'])
            self.screen.blit(acc_text, (step_x, step_y))
            step_x += 35
            
            # Posición
            pos_text = self.font.render(f"({step['posicion_x']},{step['posicion_y']})", True, COLORS['BLACK'])
            self.screen.blit(pos_text, (step_x, step_y))
            
            step_y += UI_CONFIG['TEXT_SPACING'] - 5  # Menos espacio entre filas
    
    def quit(self):
        """
        Cierra la interfaz gráfica
        """
        pygame.quit()
        sys.exit()


def create_interface():
    """
    Función de conveniencia para crear una nueva interfaz
    
    Returns:
        LineFollowerInterface: Instancia de la interfaz creada
    """
    return LineFollowerInterface()
