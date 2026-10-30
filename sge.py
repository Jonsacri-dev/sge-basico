"""
Sistema de Gestión de Estudiantes (SGE) básico
==============================================
Aplicación de consola que permite agregar estudiantes, y gestionar sus notas en un menú independiente.

Conceptos aplicados:
  - Decisión simple, doble y anidada
  - Decisión múltiple (match-case) en Menú Principal y Menú de Notas
  - Repetición condicionada al comienzo (while)
  - Repetición condicionada al final (emulada con while True + break)
  - Iteraciones ascendentes y descendentes (for con range)
  - Variables especiales: contador, acumulador (sumatoria) y bandera
  - Estructura de datos: lista con diccionarios y sublistas (notas)
  - Funciones reutilizables con una sola responsabilidad
"""

MAX_ESTUDIANTES = 50
EDAD_MINIMA = 14
EDAD_MAXIMA = 99
NOTA_MINIMA = 0.0
NOTA_MAXIMA = 5.0

OPCION_AGREGAR_ESTUDIANTE = 1
OPCION_MENU_NOTAS = 2
OPCION_MOSTRAR_TODOS = 3
OPCION_BUSCAR_ESTUDIANTE = 4
OPCION_SALIR = 5

OPCION_AGREGAR_NOTA = 1
OPCION_VOLVER = 2

def leer_entero(mensaje, minimo, maximo):
    while True:
        texto = input(mensaje).strip()
        try:
            valor = int(texto)
        except ValueError:
            print(f"  [!] '{texto}' no es un número entero válido.")
            continue
        if minimo <= valor <= maximo:
            return valor
        print(f"  [!] El valor debe estar entre {minimo} y {maximo}.")

def leer_decimal(mensaje, minimo, maximo):
    while True:
        texto = input(mensaje).strip().replace(",", ".")
        try:
            valor = float(texto)
        except ValueError:
            print(f"  [!] '{texto}' no es un número válido.")
            continue
        if minimo <= valor <= maximo:
            return round(valor, 2)
        print(f"  [!] La nota debe estar entre {minimo} y {maximo}.")

def leer_texto(mensaje):
    while True:
        texto = input(mensaje).strip()
        if texto != "":
            return texto
        print("  [!] Este campo no puede quedar vacío.")

def leer_si_no(mensaje):
    while True:
        respuesta = input(mensaje).strip().upper()
        if respuesta in ("S", "SI", "SÍ"):
            return True
        elif respuesta in ("N", "NO"):
            return False
        print("  [!] Responda S o N.")

def buscar_indice_por_id(estudiantes, id_buscado):
    encontrado = False
    posicion = -1
    i = 0
    while i < len(estudiantes) and not encontrado:
        if estudiantes[i]["id"] == id_buscado:
            encontrado = True
            posicion = i
        i += 1
    return posicion

def calcular_promedio(notas):
    if not notas:
        return 0.0
    return sum(notas) / len(notas)

def mostrar_estudiante(estudiante):
    promedio = calcular_promedio(estudiante["notas"])
    print(f"  {estudiante['id']:<10} {estudiante['nombre']:<28} "
          f"{estudiante['edad']:>4}   {estudiante['programa']:<22} {promedio:>5.2f}")

def imprimir_encabezado_tabla():
    print(f"  {'ID':<10} {'NOMBRE':<28} {'EDAD':>4}   {'PROGRAMA':<22} {'PROM.'}")
    print("  " + "-" * 75)

def agregar_estudiante(estudiantes, contador):
    print("\n--- AGREGAR ESTUDIANTE ---")
    if contador >= MAX_ESTUDIANTES:
        print(f"  [!] Capacidad máxima alcanzada ({MAX_ESTUDIANTES}).")
        return contador
    id_nuevo = leer_entero("ID del estudiante (1 - 999999): ", 1, 999999)
    if buscar_indice_por_id(estudiantes, id_nuevo) != -1:
        print(f"  [!] Ya existe un estudiante con ID {id_nuevo}. Cancelado.")
        return contador
    nombre = leer_texto("Nombre completo: ").title()
    edad = leer_entero(f"Edad ({EDAD_MINIMA}-{EDAD_MAXIMA}): ", EDAD_MINIMA, EDAD_MAXIMA)
    programa = leer_texto("Programa académico: ").title()
    
    estudiante = {"id": id_nuevo, "nombre": nombre, "edad": edad,
                  "programa": programa, "notas": []}
    estudiantes.append(estudiante)
    contador += 1
    print(f"  [OK] Estudiante '{nombre}' registrado. (Vaya al menú de notas para calificar).")
    return contador

def mostrar_estudiantes(estudiantes, contador):
    print("\n--- LISTA DE ESTUDIANTES ---")
    if contador == 0:
        print("  No hay estudiantes registrados todavía.")
        return
    orden = leer_entero("Orden: 1) Ascendente  2) Descendente: ", 1, 2)
    if orden == 1:
        indices = range(0, contador)
    else:
        indices = range(contador - 1, -1, -1)

    suma_promedios = 0.0
    aprobados = 0
    imprimir_encabezado_tabla()
    for i in indices:
        mostrar_estudiante(estudiantes[i])
        promedio_ind = calcular_promedio(estudiantes[i]["notas"])
        suma_promedios += promedio_ind
        if promedio_ind >= 3.0:
            aprobados += 1

    promedio_general = suma_promedios / contador
    print("  " + "-" * 75)
    print(f"  Total: {contador} | Promedio General: {promedio_general:.2f} | "
          f"Aprobados (>=3.0): {aprobados} | Reprobados: {contador - aprobados}")

def buscar_estudiante(estudiantes, contador):
    print("\n--- BUSCAR ESTUDIANTE POR ID ---")
    if contador == 0:
        print("  No hay estudiantes registrados.")
        return
    id_buscado = leer_entero("ID a buscar: ", 1, 999999)
    posicion = buscar_indice_por_id(estudiantes, id_buscado)
    if posicion != -1:
        estudiante = estudiantes[posicion]
        print("  [OK] Estudiante encontrado:")
        imprimir_encabezado_tabla()
        mostrar_estudiante(estudiante)
        
        promedio = calcular_promedio(estudiante["notas"])
        print(f"  Notas registradas: {estudiante['notas']}")
        
        if len(estudiante["notas"]) > 0:
            if promedio >= 3.0:
                if promedio >= 4.5:
                    print("  Desempeño: SUPERIOR")
                else:
                    print("  Desempeño: APROBADO")
            else:
                print("  Desempeño: EN RIESGO ACADÉMICO")
        else:
            print("  Desempeño: SIN CALIFICAR")
    else:
        print(f"  [X] No existe ningún estudiante con ID {id_buscado}.")

def menu_notas(estudiantes, contador):
    if contador == 0:
        print("\n  [!] Primero debe registrar estudiantes antes de asignar notas.")
        return
        
    bandera_volver = False
    while not bandera_volver:
        print("\n" + "-" * 45)
        print("   SUBMENÚ: GESTIÓN DE NOTAS")
        print("-" * 45)
        print(f"  {OPCION_AGREGAR_NOTA}. Buscar estudiante y agregar nota")
        print(f"  {OPCION_VOLVER}. Volver al menú principal")
        print("-" * 45)
        
        opcion = leer_entero("Seleccione una opción: ", OPCION_AGREGAR_NOTA, OPCION_VOLVER)
        
        match opcion:
            case 1:
                id_buscado = leer_entero("\n  Ingrese el ID del estudiante para calificar: ", 1, 999999)
                posicion = buscar_indice_por_id(estudiantes, id_buscado)
                
                if posicion != -1:
                    est = estudiantes[posicion]
                    print(f"  >> Estudiante encontrado: {est['nombre']}")
                    while True:
                        nota = leer_decimal(f"  Ingrese nueva nota ({NOTA_MINIMA}-{NOTA_MAXIMA}): ", NOTA_MINIMA, NOTA_MAXIMA)
                        est["notas"].append(nota)
                        print(f"  [OK] Nota {nota} añadida. Total de notas: {len(est['notas'])}")
                        
                        if not leer_si_no("  ¿Desea ingresar otra nota para este estudiante? (S/N): "):
                            break
                else:
                    print(f"  [X] ID {id_buscado} no encontrado.")
            case 2:
                bandera_volver = True
            case _:
                print("  [!] Opción no reconocida.")

def confirmar_salida():
    if leer_si_no("\n¿Seguro que desea salir del sistema? (S/N): "):
        return True
    print("  Regresando al menú principal...")
    return False

def mostrar_menu_principal(contador):
    print("\n" + "=" * 45)
    print("   SISTEMA DE GESTIÓN DE ESTUDIANTES (SGE)")
    print("=" * 45)
    print(f"  Registrados: {contador}/{MAX_ESTUDIANTES}")
    print(f"  {OPCION_AGREGAR_ESTUDIANTE}. Agregar estudiante (Datos básicos)")
    print(f"  {OPCION_MENU_NOTAS}. Menú de Notas (Asignar calificaciones)")
    print(f"  {OPCION_MOSTRAR_TODOS}. Mostrar todos los estudiantes")
    print(f"  {OPCION_BUSCAR_ESTUDIANTE}. Buscar estudiante por ID")
    print(f"  {OPCION_SALIR}. Salir")
    print("-" * 45)

def main():
    estudiantes = []        
    contador_estudiantes = 0  
    bandera_salir = False     

    while not bandera_salir:
        mostrar_menu_principal(contador_estudiantes)
        opcion = leer_entero("Seleccione una opción: ", OPCION_AGREGAR_ESTUDIANTE, OPCION_SALIR)

        match opcion:
            case 1:
                contador_estudiantes = agregar_estudiante(estudiantes, contador_estudiantes)
            case 2:
                menu_notas(estudiantes, contador_estudiantes)
            case 3:
                mostrar_estudiantes(estudiantes, contador_estudiantes)
            case 4:
                buscar_estudiante(estudiantes, contador_estudiantes)
            case 5:
                bandera_salir = confirmar_salida()
            case _:
                print("  [!] Opción no reconocida.")

    print(f"\nSesión finalizada. Estudiantes registrados: {contador_estudiantes}. ¡Hasta pronto!")

if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n\nEjecución interrumpida por el usuario. ¡Hasta pronto!")
