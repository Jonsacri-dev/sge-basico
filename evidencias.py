"""Pruebas automatizadas del SGE.

Ejecuta el programa con entradas simuladas (mostrando en pantalla lo que
'escribe' el usuario, como en una terminal real), verifica los resultados
esperados y guarda la transcripción completa en transcripcion.txt.

Uso:  python evidencias.py
"""
import builtins
import contextlib
import io

import sge

INICIO_ENTRADA, FIN_ENTRADA = "\x01", "\x02"   # marcas para resaltar lo tecleado


def ejecutar(entradas, max_estudiantes=None, marcar=False):
    """Corre sge.main() alimentándolo con la lista 'entradas'."""
    cola = list(entradas)
    salida = io.StringIO()

    def input_simulado(msg=""):
        valor = cola.pop(0)
        eco = f"{INICIO_ENTRADA}{valor}{FIN_ENTRADA}" if marcar else valor
        print(msg + eco)
        return valor

    original_input, original_max = builtins.input, sge.MAX_ESTUDIANTES
    builtins.input = input_simulado
    if max_estudiantes is not None:
        sge.MAX_ESTUDIANTES = max_estudiantes
    try:
        with contextlib.redirect_stdout(salida):
            sge.main()
    finally:
        builtins.input, sge.MAX_ESTUDIANTES = original_input, original_max
    return salida.getvalue()


# Flujo completo: cubre todas las opciones, errores de entrada y situaciones límite
FLUJO_COMPLETO = [
    "2",                                                                     # mostrar sin datos
    "1", "1001", "ana maría pérez", "19", "ingeniería de software", "4.6",   # agregar normal
    "1", "abc", "1002", "", "Carlos Gómez", "150", "22",
    "Ingeniería Industrial", "2,8",                                          # agregar con errores
    "1", "1003", "Laura Rincón", "20", "Psicología", "3.9",
    "1", "1001",                                                             # ID duplicado
    "2", "1",                                                                # mostrar ascendente
    "2", "2",                                                                # mostrar descendente
    "3", "1002",                                                             # búsqueda exitosa
    "3", "9999",                                                             # búsqueda fallida
    "7", "4", "N",                                                           # opción inválida / salida cancelada
    "4", "S",                                                                # salida confirmada
]

# Capacidad máxima reducida a 2 para probar el control de desbordamiento
FLUJO_CAPACIDAD = [
    "1", "1", "Ana", "18", "Derecho", "4",
    "1", "2", "Luis", "19", "Medicina", "3.5",
    "1",                                    # el tercero debe rechazarse
    "4", "S",
]


def verificar():
    texto = ejecutar(FLUJO_COMPLETO)
    casos = [
        ("Lista vacía", "No hay estudiantes registrados todavía." in texto),
        ("Registro exitoso", "Total: 3/50" in texto),
        ("Texto en campo numérico", "'abc' no es un número entero válido" in texto),
        ("Campo vacío", "Este campo no puede quedar vacío." in texto),
        ("Edad fuera de rango", "El valor debe estar entre 14 y 99." in texto),
        ("Nota con coma decimal", "2.80" in texto),
        ("ID duplicado", "Ya existe un estudiante con ID 1001" in texto),
        ("Sumatoria / promedio", "Promedio general: 3.77" in texto),
        ("Contador condicionado", "Aprobados (>=3.0): 2" in texto),
        ("Búsqueda exitosa", "Estudiante encontrado" in texto),
        ("Búsqueda fallida", "No existe ningún estudiante con ID 9999" in texto),
        ("Opción fuera de rango", "El valor debe estar entre 1 y 4." in texto),
        ("Salida cancelada", "Regresando al menú..." in texto),
        ("Salida confirmada", "Sesión finalizada" in texto),
    ]
    texto_cap = ejecutar(FLUJO_CAPACIDAD, max_estudiantes=2)
    casos.append(("Capacidad máxima", "Capacidad máxima alcanzada (2)" in texto_cap))

    aprobados = 0
    for nombre, ok in casos:
        print(f"[{'PASA' if ok else 'FALLA'}] {nombre}")
        aprobados += ok
    print(f"\n{aprobados}/{len(casos)} casos de prueba aprobados")

    with open("transcripcion.txt", "w", encoding="utf-8") as f:
        f.write(texto)
        f.write("\n\n===== PRUEBA DE CAPACIDAD (MAX_ESTUDIANTES = 2) =====\n")
        f.write(texto_cap)


if __name__ == "__main__":
    verificar()
