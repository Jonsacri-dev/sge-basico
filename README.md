# Sistema de Gestión de Estudiantes (SGE) básico

Aplicación de consola en Python que permite **agregar**, **mostrar** y **buscar por ID** estudiantes, y **salir** del sistema de forma controlada. Proyecto académico para practicar estructuras de control, variables especiales y listas.

**Autor:** Jonathan Salamanca Criado — Fundación Universitaria Compensar

## Requisitos

- Python **3.10 o superior** (usa `match-case`). Probado en Python 3.13.
- Sin librerías externas.

## Ejecución

```bash
python sge.py
```

Pruebas automáticas (15 casos, incluidas situaciones límite):

```bash
python evidencias.py
```

## Funcionalidades

| Opción | Descripción |
|---|---|
| 1. Agregar | Registra ID único, nombre, edad, programa y nota (0.0–5.0), validando cada dato. Controla la capacidad máxima (50). |
| 2. Mostrar | Lista en orden ascendente o descendente, con total, promedio general, aprobados y reprobados. |
| 3. Buscar | Busca por ID y clasifica el desempeño (superior, aprobado, en riesgo). |
| 4. Salir | Pide confirmación y finaliza la sesión. |

## Conceptos aplicados

| Concepto | Dónde |
|---|---|
| Repetición condicionada al comienzo (`while`) | Ciclo del menú en `main()`; búsqueda con bandera en `buscar_indice_por_id()` |
| Repetición condicionada al final (emulada con `while True`) | Funciones `leer_*` de entrada validada |
| Decisión múltiple (`match-case`, equivalente a `switch`) | Selección de la opción en `main()` |
| Decisión simple, doble y anidada (`if`) | Validaciones, sentido del recorrido y clasificación del desempeño |
| Iteración ascendente y descendente (`for` + `range`) | `mostrar_estudiantes()` |
| Contador | `contador_estudiantes`, `aprobados` |
| Acumulador (sumatoria) | `suma_notas` para el promedio |
| Bandera | `bandera_salir` (ciclo principal), `encontrado` (búsqueda) |
| Lista con tamaño máximo | `estudiantes` (lista de diccionarios), `MAX_ESTUDIANTES = 50` |
| Manejo de errores | `try-except` para `ValueError`, `KeyboardInterrupt` y `EOFError` |

## Estructura del repositorio

```
sge.py                     Programa principal
evidencias.py              Pruebas automáticas y transcripción de ejecución
SGE_Documento_Tecnico.pdf  Documentación técnica
doc/
  img/                     Diagramas de flujo y capturas de ejecución
  *.dot                    Fuentes de los diagramas (Graphviz)
  diagramas_modulares.py   Genera los diagramas por función
  capturas.py              Genera las capturas de ejecución
  generar_pdf.py           Genera el documento PDF
```

## Diagrama de flujo principal

![Diagrama principal](doc/img/d1_principal.png)
