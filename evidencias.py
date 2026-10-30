import builtins
import contextlib
import io
import sge

INICIO_ENTRADA, FIN_ENTRADA = "\x01", "\x02"

def ejecutar(entradas, max_estudiantes=None, marcar=False):
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

FLUJO_COMPLETO = [
    "3",                                                # mostrar sin datos
    "1", "1001", "ana maría pérez", "19", "software",   # agregar est 1
    "2", "1", "1001", "4.6", "S", "5.0", "N", "2",      # asignar dos notas y volver
    "1", "abc", "1002", "", "Carlos Gómez", "150", "22", "Industrial", # agregar est 2 con errores previos
    "2", "1", "1002", "2.8", "N", "2",                  # asignar una nota y volver
    "1", "1001",                                        # intentar duplicar ID
    "3", "1",                                           # mostrar ascendente
    "4", "1001",                                        # búsqueda exitosa
    "4", "9999",                                        # búsqueda fallida
    "5", "S",                                           # salir
]

def verificar():
    texto = ejecutar(FLUJO_COMPLETO)
    print("--- TRANSCRIPCIÓN DEL SISTEMA (Con multi-notas) ---")
    print(texto)
    with open("/mnt/data/transcripcion_multinotas.txt", "w", encoding="utf-8") as f:
        f.write(texto)

if __name__ == "__main__":
    verificar()
