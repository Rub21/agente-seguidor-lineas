# Agente Seguidor de Líneas

Este proyecto implementa un agente inteligente que sigue líneas utilizando algoritmos de percepción-acción. El agente utiliza sensores para detectar líneas oscuras en el suelo y toma decisiones basadas en sus percepciones.

## Estructura del Proyecto

El proyecto está organizado en módulos separados para una mejor mantenibilidad:

### Archivos Principales

- **`main.py`** - Archivo principal que ejecuta la simulación
- **`config.py`** - Configuraciones y constantes del sistema
- **`agent.py`** - Lógica del agente inteligente
- **`environment.py`** - Gestión del entorno y generación de líneas
- **`interface.py`** - Interfaz gráfica y visualización
- **`requirements.txt`** - Dependencias del proyecto

### Características del Agente

- **Sensores**: El agente tiene sensores que detectan:
  - Piso oscuro (línea) vs piso claro
  - Contacto con paredes
  - Orientación actual
  - Visión hacia adelante (izquierda, centro, derecha)

- **Acciones**: El agente puede:
  - Moverse hacia adelante
  - Rotar a la izquierda o derecha
  - Girar 180 grados cuando encuentra obstáculos

### Algoritmo de Seguimiento

El agente utiliza una tabla de percepción-acción simple:

1. Si está sobre una línea o hay línea al frente → Avanzar
2. Si hay línea a la izquierda → Rotar izquierda y avanzar
3. Si hay línea a la derecha → Rotar derecha y avanzar
4. Si hay contacto con pared → Girar 180° y avanzar
5. En otros casos → Avanzar para buscar línea

## Instalación y Ejecución

1. Instalar dependencias:
```bash
pip install -r requirements.txt
```

2. Ejecutar la simulación:
```bash
python main.py
```

## Controles

### Teclado
- **ESC** o **Cerrar ventana**: Salir de la aplicación
- **ESPACIO**: Pausar/Continuar la simulación

### Botones de Control
- **Generar Líneas Aleatorias**: Crea nuevas líneas negras aleatorias en el entorno
- **Posición Aleatoria del Agente**: Mueve el agente a una posición aleatoria
- **Reiniciar Agente**: Reinicia el agente en su posición actual
- **Limpiar Cuadrícula**: Borra todas las líneas del entorno
- **Pausar/Continuar**: Pausa o reanuda la simulación

### Interfaz
- **Ventana más grande**: 1200x800 píxeles para mejor visualización
- **Panel superior**: Botones de control en la parte superior de la ventana
- **Panel de cuadrícula**: Área principal para visualizar el agente y las líneas
- **Panel de información**: Panel derecho con percepciones y estado del sistema
- **Layout organizado**: Separación clara entre controles, simulación e información

## Configuración

Puedes modificar los parámetros en `config.py`:

- Dimensiones de la ventana
- Tamaño de las celdas
- Colores del sistema
- Velocidad del agente
- Configuración del entorno

## Arquitectura Modular

Cada módulo tiene una responsabilidad específica:

- **Config**: Centraliza todas las configuraciones
- **Environment**: Maneja la generación y gestión del entorno
- **Agent**: Implementa la lógica del agente inteligente
- **Interface**: Proporciona la visualización gráfica
- **Main**: Orquesta la ejecución de todos los componentes

Esta arquitectura facilita el mantenimiento, testing y extensión del sistema.
