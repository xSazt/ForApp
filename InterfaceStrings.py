class Interface:
    APP_TITLE="[magenta]ForApp[/magenta]"

    ACCESS_MENU="""Ingrese el número correspondiente a la acción deseada.\n
[magenta]1[/magenta]. Iniciar sesión
[magenta]2[/magenta]. Registrarse
[magenta]3[/magenta]. Salir
"""
        
    LOGIN="""Ingrese las credenciales especificadas durante el registro.
[yellow]ADVERTENCIA: Por motivos de seguridad, los caracteres de tu contraseña NO se mostraran[/yellow]

"""

    REGISTER="""Los siguientes datos se le pedirán:

[magenta]>[/magenta]Correo*
[magenta]>[/magenta]Telefono/Celular
[magenta]>[/magenta]Nombre
[magenta]>[/magenta]Dirección
[magenta]>[/magenta]Universidad
[magenta]>[/magenta]Contraseña de acceso(Al menos ocho caracteres)*

[yellow]Los datos obligatorios están marcados con *\nPara los opcionales dejar en blanco si opta por no diligenciar.\nPor motivos de seguridad, los caracteres de su contraseña NO se mostraran[/yellow]
"""

    MAIN_MENU="""Bienvenid@ {Name}

Opciones:
[magenta]1[/magenta]. Administrador de gastos
[magenta]2[/magenta]. Horario
[magenta]3[/magenta]. Calculadora de calificaciones
[magenta]4[/magenta]. Configuración
[magenta]5[/magenta]. Salir

"""
    def SCHEDULE_MENU(other):
        activities=[]
        for act in other:
            activities.append(f"[magenta]{act['fecha']} | {act['hora']}[/magenta] - {act['desc']}")
        joinedActivities="\n".join(activities)
        return f"""Otras actividades:
{joinedActivities}

Opciones:
[magenta]1[/magenta]. Añadir tarea
[magenta]2[/magenta]. Quitar tarea
[magenta]3[/magenta]. Menú principal"""
    
    ADD_TASK_MENU="""Los siguientes datos se le pedirán:

[magenta]>[/magenta]Tipo de tarea: [yellow](1 si es semanal; 2 si no es semanal )[/yellow]
[magenta]>[/magenta]Dia: [yellow]Si eligió semanal digite el dia de la semana, de lo contrario ingrese la fecha con el siguiente formato: DD/MM/AAAA[/yellow]
[magenta]>[/magenta]Hora: [yellow]La hora debe seguir el siguiente formato: HH:MM[AM ó PM][/yellow]
[magenta]>[/magenta]Descripción

[cyan]Escribe "cancelar" para volver[/cyan]

"""

    def DELETE_TASK_MENU(tasks):
        weeklyTasks=[]
        otherTasks=[]
        for day in tasks["programacion_semanal"]:
            if tasks["programacion_semanal"][day]:
                for hour,desc in tasks["programacion_semanal"][day].items():
                    weeklyTasks.append(f"[magenta]{day}[/magenta] | [magenta]{hour}[/magenta] - {desc}")
        if tasks["otras_programaciones"]:
            for task in tasks["otras_programaciones"]:
                otherTasks.append(f"[magenta]{task['fecha']}[/magenta] | [magenta]{task['hora']}[/magenta] - {task['desc']}")
        
        joinedWeeklyTasks="\n".join(weeklyTasks)
        joinedOtherTasks="\n".join(otherTasks)

        return f"""Tareas semanales:
{joinedWeeklyTasks}

Otras tareas:
{joinedOtherTasks}

Para eliminar una tarea indique:
[magenta]>[/magenta]Tipo de tarea: [yellow](1 si es semanal; 2 si no es semanal )[/yellow]
[magenta]>[/magenta]Dia: [yellow]Si eligió semanal digite el dia de la semana, de lo contrario ingrese la fecha con el siguiente formato: DD/MM/AAAA[/yellow]
[magenta]>[/magenta]Hora: [yellow]La hora debe seguir el siguiente formato: HH:MM[AM ó PM][/yellow]

[cyan]Escribe "cancelar" para volver[/cyan]
"""

