"""
Archivo principal del Agente Seguidor de Líneas
Integra todos los módulos para ejecutar la simulación
"""

import random
from config import GRID_WIDTH, GRID_HEIGHT, AGENT_CONFIG
from environment import create_environment
from agent import create_agent
from interface import create_interface
from logger import create_logger


def main():
    """
    Función principal que ejecuta la simulación del agente seguidor de líneas
    """
    # Crear el entorno
    environment = create_environment(GRID_WIDTH, GRID_HEIGHT)
    
    # Generar una línea aleatoria
    environment.generate_line()
    
    # Crear el agente en una posición aleatoria
    agent_x = random.randint(0, GRID_WIDTH - 1)
    agent_y = random.randint(0, GRID_HEIGHT - 1)
    agent = create_agent(agent_x, agent_y, GRID_WIDTH, GRID_HEIGHT)
    
    # Crear la interfaz
    interface = create_interface()
    
    # Crear el logger
    logger = create_logger()
    logger.start_logging()
    
    print("🤖 Agente Seguidor de Líneas iniciado")
    print("📝 Logging activado - cada paso será registrado")
    print("🎮 Controles:")
    print("   - Click en botones para controlar la simulación")
    print("   - Espacio: Pausar/Continuar")
    print("   - Escape: Salir")
    print("   - Los pasos se muestran en tiempo real en el panel derecho")
    
    # Bucle principal de la simulación
    running = True
    while running:
        # Manejar eventos
        running, button_clicked = interface.handle_events()
        
        # Procesar acciones de botones
        if button_clicked:
            if button_clicked == 'RANDOM_LINES':
                environment.generate_line()
            elif button_clicked == 'RANDOM_AGENT':
                agent_x = random.randint(0, GRID_WIDTH - 1)
                agent_y = random.randint(0, GRID_HEIGHT - 1)
                agent.reset_position(agent_x, agent_y)
            elif button_clicked == 'RESET_AGENT':
                agent.reset_position(agent.x, agent.y)
            elif button_clicked == 'CLEAR_GRID':
                environment.reset()
            elif button_clicked == 'PAUSE':
                interface.paused = not interface.paused
            elif button_clicked == 'CLEAR_LOG':
                logger.clear_log()
            elif button_clicked == 'EXPORT_LOG':
                logger.export_to_csv()
            elif button_clicked == 'PRINT_TABLE':
                logger.print_table()
            
            # Reiniciar estados de botones después de procesar
            interface.reset_button_states()
        
        # Solo actualizar agente si no está pausado
        if not interface.paused:
            # Percepción del agente
            perceptions = agent.perceive(environment)
            
            # Acción del agente
            action_taken = agent.act(perceptions)
            
            # Registrar el paso en el logger
            logger.log_step(agent, perceptions, action_taken)
        else:
            # Si está pausado, solo obtener percepciones para mostrar
            perceptions = agent.perceive(environment)
        
        # Dibujar todo
        interface.clear_screen()
        interface.draw_top_panel()
        interface.draw_buttons()
        interface.draw_grid(environment, agent)
        interface.draw_perceptions(perceptions)
        interface.draw_info_panel(agent, environment)
        interface.draw_steps_table(logger, max_steps=8)
        
        # Actualizar pantalla
        interface.update_display()
        
        # Controlar velocidad
        interface.tick(AGENT_CONFIG['MOVEMENT_SPEED'])
    
    # Cerrar la aplicación
    logger.stop_logging()
    interface.quit()


if __name__ == "__main__":
    main()