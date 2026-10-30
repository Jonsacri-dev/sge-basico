"""
Sistema de Gestión de Estudiantes (SGE) básico
==============================================
Aplicación de consola que permite agregar, mostrar y buscar estudiantes.

Conceptos aplicados:
  - Decisión simple, doble y anidada (if / if-else / if dentro de if)
  - Decisión múltiple (match-case, el "switch" de Python 3.10+)
  - Repetición condicionada al comienzo (while)
  - Repetición condicionada al final (while True + break: Python no tiene do-while)
  - Iteraciones ascendentes y descendentes (for con range)
  - Variables especiales: contador, acumulador (sumatoria) y bandera
  - Estructura de datos: lista con tamaño máximo controlado
  - Funciones reutilizables con una sola responsabilidad
"""

# ---------------------------------------------------------------------------
# CONSTANTES DE CONFIGURACIÓN
# ---------------------------------------------------------------------------
# Se fija un máximo para comportarnos como un arreglo de tamaño fijo y
# demostrar el control de desbordamiento que pide la guía.
MAX_ESTUDIANTES = 50
EDAD_MINIMA = 14
EDAD_MAXIMA = 99
NOTA_MINIMA = 0.0
NOTA_MAXIMA = 5.0   # Escala de calificación colombiana

# Opciones del menú (nombres significativos en lugar de "números mágicos")
OPCION_AGREGAR = 1
OPCION_MOSTRAR = 2
OPCION_BUSCAR = 3
OPCION_SALIR = 4


# ---------------------------------------------------------------------------
# FUNCIONES DE ENTRADA VALIDADA
# ---------------------------------------------------------------------------
def leer_entero(mensaje, minimo, maximo):
    """Pide un número entero dentro de [minimo, maximo].

    Usa una repetición condicionada al FINAL: el cuerpo se ejecuta al menos
    una vez (hay que preguntar antes de poder validar) y solo se sale cuando
    el dato es válido. En Python se emula el do-while con while True + break.
    """
    while True:
        texto = input(mensaje).strip()
        try:
            valor = int(texto)
        except ValueError:
            # Evita que el programa se caiga si escriben letras o vacío
            print(f"  [!] '{texto}' no es un número entero válido. Intente de nuevo.")
            continue
        if minimo <= valor <= maximo:
            return valor  # Condición de salida evaluada al final
        print(f"  [!] El valor debe estar entre {minimo} y {maximo}.")


def leer_decimal(mensaje, minimo, maximo):
    """Pide un número decimal dentro de [minimo, maximo] (acepta coma o punto)."""
    while True:
        texto = input(mensaje).strip().replace(",", ".")
        try:
            valor = float(texto)
        except ValueError:
            print(f"  [!] '{texto}' no es un número válido. Use, por ejemplo, 4.5")
            continue
        if minimo <= valor <= maximo:
            return round(valor, 2)
        print(f"  [!] La nota debe estar entre {minimo} y {maximo}.")


def leer_texto(mensaje):
    """Pide un texto no vacío; repite hasta que el usuario escriba algo."""
    while True:
        texto = input(mensaje).strip()
        if texto != "":
            return texto
        print("  [!] Este campo no puede quedar vacío.")


def leer_si_no(mensaje):
    """Devuelve True para 'S' y False para 'N'. Cualquier otra cosa se repite."""
    while True:
        respuesta = input(mensaje).strip().upper()
        if respuesta in ("S", "SI", "SÍ"):
            return True
        elif respuesta in ("N", "NO"):
            return False
        print("  [!] Responda S o N.")


# ---------------------------------------------------------------------------
# FUNCIONES DE LÓGICA DEL NEGOCIO
# ---------------------------------------------------------------------------
def buscar_indice_por_id(estudiantes, id_buscado):
    """Búsqueda lineal: devuelve la posición del estudiante o -1 si no existe.

    Usa una BANDERA (encontrado) dentro de la condición del while: el ciclo
    se detiene en cuanto hay coincidencia, sin recorrer el resto de la lista.
    """
    encontrado = False   # BANDERA de búsqueda
    posicion = -1
    i = 0
    # Repetición condicionada al comienzo con condición compuesta
    while i < len(estudiantes) and not encontrado:
        if estudiantes[i]["id"] == id_buscado:  # Decisión simple
            encontrado = True
            posicion = i
        i += 1                                  # Avance ascendente
    return posicion


def mostrar_estudiante(estudiante):
    """Imprime un estudiante en una línea con formato de tabla (reutilizable)."""
    print(f"  {estudiante['id']:<10} {estudiante['nombre']:<28} "
          f"{estudiante['edad']:>4}   {estudiante['programa']:<22} {estudiante['nota']:>5.2f}")


def imprimir_encabezado_tabla():
    print(f"  {'ID':<10} {'NOMBRE':<28} {'EDAD':>4}   {'PROGRAMA':<22} {'NOTA':>5}")
    print("  " + "-" * 75)


def agregar_estudiante(estudiantes, contador):
    """Registra un estudiante nuevo y devuelve el contador actualizado."""
    print("\n--- AGREGAR ESTUDIANTE ---")

    # Decisión simple: control de capacidad del "arreglo"
    if contador >= MAX_ESTUDIANTES:
        print(f"  [!] Capacidad máxima alcanzada ({MAX_ESTUDIANTES}). No se puede agregar.")
        return contador

    id_nuevo = leer_entero("ID del estudiante (1 - 999999): ", 1, 999999)

    # Decisión doble: el ID debe ser único
    if buscar_indice_por_id(estudiantes, id_nuevo) != -1:
        print(f"  [!] Ya existe un estudiante con ID {id_nuevo}. Registro cancelado.")
        return contador

    nombre = leer_texto("Nombre completo: ").title()
    edad = leer_entero(f"Edad ({EDAD_MINIMA}-{EDAD_MAXIMA}): ", EDAD_MINIMA, EDAD_MAXIMA)
    programa = leer_texto("Programa académico: ").title()
    nota = leer_decimal(f"Nota promedio ({NOTA_MINIMA}-{NOTA_MAXIMA}): ", NOTA_MINIMA, NOTA_MAXIMA)

    # Cada estudiante es un diccionario; todos se guardan en la lista
    estudiante = {"id": id_nuevo, "nombre": nombre, "edad": edad,
                  "programa": programa, "nota": nota}
    estudiantes.append(estudiante)
    contador += 1   # Variable de CONTEO

    print(f"  [OK] Estudiante '{nombre}' registrado. Total: {contador}/{MAX_ESTUDIANTES}")
    return contador


def mostrar_estudiantes(estudiantes, contador):
    """Lista todos los estudiantes en orden ascendente o descendente
    y calcula estadísticas con un ACUMULADOR (sumatoria)."""
    print("\n--- LISTA DE ESTUDIANTES ---")

    if contador == 0:
        print("  No hay estudiantes registrados todavía.")
        return

    orden = leer_entero("Orden de registro: 1) Ascendente  2) Descendente: ", 1, 2)

    # Decisión doble que selecciona el sentido de la iteración
    if orden == 1:
        indices = range(0, contador)            # 0, 1, 2, ... n-1
    else:
        indices = range(contador - 1, -1, -1)   # n-1, ..., 1, 0

    suma_notas = 0.0       # ACUMULADOR (sumatoria)
    aprobados = 0          # CONTADOR condicionado
    imprimir_encabezado_tabla()
    for i in indices:
        mostrar_estudiante(estudiantes[i])
        suma_notas += estudiantes[i]["nota"]
        if estudiantes[i]["nota"] >= 3.0:      # 3.0 es la nota aprobatoria
            aprobados += 1

    promedio = suma_notas / contador
    print("  " + "-" * 75)
    print(f"  Total estudiantes: {contador}   Promedio general: {promedio:.2f}   "
          f"Aprobados (>=3.0): {aprobados}   Reprobados: {contador - aprobados}")


def buscar_estudiante(estudiantes, contador):
    """Pide un ID y muestra el estudiante si existe."""
    print("\n--- BUSCAR ESTUDIANTE POR ID ---")

    if contador == 0:
        print("  No hay estudiantes registrados para buscar.")
        return

    id_buscado = leer_entero("ID a buscar: ", 1, 999999)
    posicion = buscar_indice_por_id(estudiantes, id_buscado)

    # Decisión simple: ¿se encontró o no?
    if posicion != -1:
        print("  [OK] Estudiante encontrado:")
        imprimir_encabezado_tabla()
        mostrar_estudiante(estudiantes[posicion])
        # Decisión anidada: clasificación del rendimiento
        nota = estudiantes[posicion]["nota"]
        if nota >= 3.0:
            if nota >= 4.5:
                print("  Desempeño: SUPERIOR")
            else:
                print("  Desempeño: APROBADO")
        else:
            print("  Desempeño: EN RIESGO ACADÉMICO")
    else:
        print(f"  [X] No existe ningún estudiante con ID {id_buscado}.")


def confirmar_salida():
    """Pide confirmación antes de salir para evitar cierres por error.
    Devuelve True si el usuario confirma (valor que tomará la bandera)."""
    if leer_si_no("¿Seguro que desea salir? (S/N): "):
        return True
    print("  Regresando al menú...")
    return False


# ---------------------------------------------------------------------------
# MENÚ Y PROGRAMA PRINCIPAL
# ---------------------------------------------------------------------------
def mostrar_menu(contador):
    print("\n" + "=" * 45)
    print("   SISTEMA DE GESTIÓN DE ESTUDIANTES (SGE)")
    print("=" * 45)
    print(f"  Registrados: {contador}/{MAX_ESTUDIANTES}")
    print(f"  {OPCION_AGREGAR}. Agregar estudiante")
    print(f"  {OPCION_MOSTRAR}. Mostrar estudiantes")
    print(f"  {OPCION_BUSCAR}. Buscar estudiante por ID")
    print(f"  {OPCION_SALIR}. Salir")
    print("-" * 45)


def main():
    estudiantes = []        # Lista (arreglo dinámico) que almacena los registros
    contador_estudiantes = 0  # CONTADOR del total registrado
    bandera_salir = False     # BANDERA que controla el ciclo principal

    # Repetición condicionada al COMIENZO: se evalúa antes de cada vuelta
    while not bandera_salir:
        mostrar_menu(contador_estudiantes)
        opcion = leer_entero("Seleccione una opción: ", OPCION_AGREGAR, OPCION_SALIR)

        # Decisión MÚLTIPLE (equivalente a switch)
        match opcion:
            case 1:
                contador_estudiantes = agregar_estudiante(estudiantes, contador_estudiantes)
            case 2:
                mostrar_estudiantes(estudiantes, contador_estudiantes)
            case 3:
                buscar_estudiante(estudiantes, contador_estudiantes)
            case 4:
                # Cambiar la bandera a True es lo que termina el while
                bandera_salir = confirmar_salida()
            case _:
                # No debería ocurrir porque leer_entero ya valida el rango;
                # se deja como defensa (equivale al 'default' de un switch).
                print("  [!] Opción no reconocida.")

    print(f"\nSesión finalizada. Estudiantes registrados: {contador_estudiantes}. ¡Hasta pronto!")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        # Ctrl+C o fin de entrada: se cierra sin mostrar un error técnico
        print("\n\nEjecución interrumpida por el usuario. ¡Hasta pronto!")
