#!/usr/bin/env python
"""
Script de utilidad para ejecutar tareas administrativas de Django
desde la línea de comandos (por ejemplo: runserver, migrate, createsuperuser).
"""
import os
import sys


def main():
    """Configura el entorno Django y despacha el comando CLI."""
    # Define la variable de entorno con el módulo de settings de Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proyecto.settings')
    try:
        # Importa la función que ejecuta comandos de Django
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # Si falla la importación, muestra un error indicando posibles causas
        raise ImportError(
            "No se pudo importar Django. ¿Estás seguro de que está instalado "
            "y disponible en tu variable PYTHONPATH? ¿Olvidaste activar "
            "tu entorno virtual?"
        ) from exc
    # Ejecuta el comando recibido por línea de comandos
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    # Punto de entrada: llama a main() cuando se ejecute este script directamente
    main()
