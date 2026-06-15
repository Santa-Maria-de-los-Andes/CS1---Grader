#!/usr/bin/env python3
"""Generate nb3_epidemias.ipynb"""
import json

def md(cell_id, source):
    return {"cell_type": "markdown", "id": cell_id, "metadata": {}, "source": source}

def code(cell_id, source):
    return {"cell_type": "code", "id": cell_id, "metadata": {}, "source": source,
            "outputs": [], "execution_count": None}

cells = []

# ════════════════════════════════════════════════════════════
# HEADER
# ════════════════════════════════════════════════════════════

cells.append(md("nb3-title", """\
# 🧬 Notebook 3 — Epidemias: De la Ficción a la Ciencia

**Temas:** Loops anidados · Ifs anidados · Funciones · Datos reales de pandemias

---

## ¿Cómo usar este notebook?

| Ícono | Tipo | Qué hacer |
|-------|------|-----------|
| 👀 | **OBSERVA** | Solo ejecuta y observa (no cambies nada) |
| ✏️ | **MODIFICA** | Edita y vuelve a ejecutar |
| 🔮 | **PREDICE** | Escribe tu predicción ANTES de ejecutar |
| 🧩 | **COMPLETA** | Reemplaza `___` con el valor correcto |
| 🔨 | **CONSTRUYE** | Escribe código desde cero |
| 🔧 | **DEBUG** | Ejecuta, lee el error, corrígelo |
| ✅ | **VERIFICA** | El autograder revisa tu respuesta |
| ❓ | **TEORÍA** | Pregunta de selección múltiple |

---

> *"En 2003 un Cordyceps mutado cruzó la barrera entre especies. En 2024 una fiebre hemorrágica paralizó África Occidental. En 1918 una gripe mató a 50 millones de personas. En cada caso, los sobrevivientes que entendieron la matemática de la transmisión fueron los que pudieron actuar. Este notebook enseña esa matemática."*"""))

cells.append(code("nb3-data", """\
# ═══════════════════════════════════════════
# DATOS DE PANDEMIAS — disponibles en todo el notebook
# Fuentes: WHO, CDC, epidemiología publicada
# ═══════════════════════════════════════════

nombres    = ["Cordyceps",  "Walker",  "COVID-19", "Ebola", "Gripe 1918", "Sarampión", "Peste Bubónica"]
r0_valores = [3.5,          1.2,       2.5,        1.8,     2.0,          15.0,        2.6            ]
mortalidad = [0.85,         1.0,       0.02,       0.65,    0.10,         0.002,       0.30           ]
duracion   = [2,            999,       14,         21,      7,            14,          37             ]
# duracion = días promedio de infección activa antes de recuperación o muerte
# Walker mortalidad = 1.0 — el 100% de los muertos reanima, independiente de la causa

print("Datos cargados:", nombres)"""))

cells.append(code("nb3-functions", """\
# ═══════════════════════════════════════════════════════════
# FUNCIONES PROPORCIONADAS — Lee y entiende antes de usar
# No necesitas saber derivarlas. Sí necesitas saber QUÉ hacen.
# ═══════════════════════════════════════════════════════════

def siguiente_paso_sir(S, I, R, N, beta, gamma):
    \"\"\"
    Calcula un día del modelo SIR (Susceptible-Infectado-Recuperado).
    S = susceptibles (sanos, pueden infectarse)
    I = infectados (actualmente enfermos)
    R = recuperados (inmunes)
    N = población total
    beta  = tasa de transmisión (qué tan fácil se contagia)
    gamma = tasa de recuperación (qué tan rápido se recupera)
    \"\"\"
    nuevos_infectados  = beta * S * I / N   # susceptibles que se infectan hoy
    nuevos_recuperados = gamma * I          # infectados que se recuperan hoy
    S_nuevo = S - nuevos_infectados
    I_nuevo = I + nuevos_infectados - nuevos_recuperados
    R_nuevo = R + nuevos_recuperados
    return S_nuevo, I_nuevo, R_nuevo


def r0_a_beta(r0, gamma):
    \"\"\"
    Convierte R0 (número básico de reproducción) a beta (tasa de transmisión).
    R0 = beta / gamma  →  beta = R0 * gamma
    \"\"\"
    return r0 * gamma


def tasa_infeccion(infectados, poblacion):
    \"\"\"
    Calcula qué porcentaje de la población está infectada.
    Devuelve un número entre 0.0 y 1.0
    \"\"\"
    return infectados / poblacion

print("✅ Funciones SIR cargadas.")"""))

cells.append(code("nb3-setup", """\
from autograder_nb3 import Autograder
grader = Autograder()"""))

cells.append(code("nb3-viz-setup", """\
# ═══════════════════════════════════════════
# MÓDULOS DE VISUALIZACIÓN — descarga una sola vez
# ═══════════════════════════════════════════
!wget -q https://raw.githubusercontent.com/Santa-Maria-de-los-Andes/CS1---Grader/main/mapa_brote.py
!wget -q https://raw.githubusercontent.com/Santa-Maria-de-los-Andes/CS1---Grader/main/viz_epidemias.py
!wget -q https://raw.githubusercontent.com/Santa-Maria-de-los-Andes/CS1---Grader/main/dashboard_oms.py

from mapa_brote    import MapaBrote    as mapa
from viz_epidemias import VizEpidemias as viz
from dashboard_oms import DashboardOMS as dash

print("✅ Visualización lista — mapa · viz · dash")"""))

# ════════════════════════════════════════════════════════════
# SECCIÓN 3.1 — NESTED LOOPS: LA CUADRÍCULA
# ════════════════════════════════════════════════════════════

cells.append(md("nb3-31-theory", """\
---
# Parte 1 — Loops Anidados, Ifs Anidados y Funciones

---
## 3.1 — Loops Anidados: La Cuadrícula

Un **loop anidado** es un loop dentro de otro loop. El loop exterior avanza una fila. Por cada fila, el loop interior recorre **todas** las columnas. El número total de ejecuciones = filas × columnas.

```python
for fila in range(3):        # loop exterior: 3 vueltas
    for col in range(4):     # loop interior: 4 vueltas POR CADA fila
        print(fila, col)     # ejecuta 3 × 4 = 12 veces
```

**Orden de iteración:**

```
(fila=0, col=0) → (fila=0, col=1) → (fila=0, col=2) → (fila=0, col=3)
(fila=1, col=0) → (fila=1, col=1) → ...
(fila=2, col=0) → ...
```

> **Clave:** el loop exterior avanza solo cuando el interior **termina completo**. Cada combinación (fila, col) se visita exactamente una vez."""))

cells.append(md("nb3-31-obs1-md", """\
### 👀 Observa — Tabla de multiplicar 5×5

Ejecuta y observa el patrón. Cada celda es `i × j`. El loop exterior controla la fila, el interior la columna."""))

cells.append(code("nb3-31-obs1", """\
for i in range(1, 6):
    for j in range(1, 6):
        print(f"{i*j:4}", end="")
    print()  # salto de línea al terminar cada fila"""))

cells.append(md("nb3-31-mod1-md", """\
### ✏️ Modifica — Extiende a 12×12

1. Cambia ambos `range(1, 6)` a `range(1, 13)` para una tabla 12×12
2. Cambia el ancho del campo de `4` a `5` para que los números de 3 dígitos quepan
3. Observa: la estructura del loop no cambia — solo los rangos"""))

cells.append(code("nb3-31-mod1", """\
# Tabla 12×12
for i in range(1, 13):
    for j in range(1, 13):
        print(f"{i*j:5}", end="")
    print()"""))

cells.append(md("nb3-31-pred1-md", """\
### 🔮 Predice — Número de ejecuciones

¿Cuántas veces ejecuta el `print` interior en un loop de **4 filas × 3 columnas**?

Escribe tu predicción como comentario **antes** de ejecutar."""))

cells.append(code("nb3-31-pred1", """\
# Mi predicción: el print interior ejecuta ___ veces

for fila in range(4):
    for col in range(3):
        print("*", end=" ")
    print()

# ¿Coincidió con tu predicción? filas × columnas = ___"""))

cells.append(md("nb3-31-comp1-md", """\
### 🧩 Completa — Tabla 3×3 desde 1

Reemplaza los `___` para producir una tabla donde filas y columnas van de 1 a 3.

**Resultado esperado:**
```
1 2 3
2 4 6
3 6 9
```"""))

cells.append(code("nb3-31-comp1", """\
for fila in range(___, ___):
    for col in range(___, ___):
        print(fila * col, end=" ")
    print()"""))

cells.append(md("nb3-31-obs2-md", """\
### 👀 Observa — El loop anidado COMO red de contactos

Las cuadrículas no son solo visuales — modelan contactos reales. Si asignamos **fila = persona infectada** y **columna = contacto potencial**, el loop anidado visita cada combinación posible de contagio.

Ejecuta y observa cuántos contactos posibles genera una población de 5 personas."""))

cells.append(code("nb3-31-obs2", """\
# Red de contactos: fila = persona infectada, columna = contacto potencial
# El loop anidado itera CADA par posible (i, j) donde i ≠ j
poblacion = 5
contactos = 0

print(f"Red de contactos — {poblacion} personas")
print("─" * 35)
for persona_infectada in range(poblacion):
    for contacto in range(poblacion):
        if persona_infectada != contacto:   # nadie contagia a sí mismo
            print(f"P{persona_infectada}→P{contacto}", end="  ")
            contactos += 1
    print()

print(f"\\nContactos posibles totales: {contactos}")
print(f"Fórmula exacta: N × (N-1) = {poblacion} × {poblacion-1} = {poblacion*(poblacion-1)}")"""))

cells.append(md("nb3-31-mod2-md", """\
### ✏️ Modifica — ¿Por qué Lima explota más rápido que Cusco?

Cambia `poblacion = 5` a `10`, luego `50`. Observa cómo crecen los contactos posibles.

```
Población  5  →  ___ contactos
Población 10  →  ___ contactos  (¿el doble? ¿más?)
Población 50  →  ___ contactos
```

Luego calcula **sin ejecutar el loop** (usa la fórmula `N × (N-1)`):

- Lima (10 millones): ¿cuántos contactos posibles?
- Cusco (400 mil): ¿cuántos contactos posibles?
- ¿Cuántas veces más contactos tiene Lima?

*Esto explica matemáticamente por qué el mismo patógeno necesita intervenciones más agresivas en ciudades grandes.*"""))

cells.append(code("nb3-31-mod2", """\
poblacion = 10   # ← prueba 10, 50, 100

contactos = 0
for persona_infectada in range(poblacion):
    for contacto in range(poblacion):
        if persona_infectada != contacto:
            contactos += 1

print(f"Población {poblacion:>4} → {contactos:>6} contactos posibles")

# Cálculo Lima vs Cusco (sin correr el loop — usa la fórmula)
lima   = 10_000_000
cusco  =    400_000
c_lima  = lima  * (lima  - 1)
c_cusco = cusco * (cusco - 1)
razon   = c_lima / c_cusco
print(f"\\nLima  ({lima/1e6:.0f}M): {c_lima:.2e} contactos posibles")
print(f"Cusco ({cusco/1e3:.0f}K): {c_cusco:.2e} contactos posibles")
print(f"Lima tiene {razon:.0f}× más contactos que Cusco — misma cuarentena, impacto distinto.")"""))

cells.append(md("nb3-31-pred2-md", """\
### 🔮 Predice — Patrón diagonal

Con la condición `if fila == col`, ¿qué patrón aparece en la cuadrícula 5×5?

Dibuja el mapa completo **antes** de ejecutar:
```
Fila 0: ___
Fila 1: ___
Fila 2: ___
Fila 3: ___
Fila 4: ___
```"""))

cells.append(code("nb3-31-pred2", """\
# Mi predicción: diagonal de [X] de arriba-izquierda a abajo-derecha

for fila in range(5):
    for col in range(5):
        if fila == col:
            print("[X]", end=" ")
        else:
            print("[ ]", end=" ")
    print()"""))

cells.append(md("nb3-31-comp2-md", """\
### 🧩 Completa — Borde exterior infectado

Completa las condiciones para que solo el borde exterior de la cuadrícula 5×5 aparezca infectado. El borde exterior son las filas/columnas 0 y 4.

**Resultado esperado:** un marco de `[X]` alrededor, todo `[ ]` adentro."""))

cells.append(code("nb3-31-comp2", """\
for fila in range(5):
    for col in range(5):
        if fila == ___ or fila == ___ or col == ___ or col == ___:
            print("[X]", end=" ")
        else:
            print("[ ]", end=" ")
    print()"""))

cells.append(md("nb3-31-ej1-md", """\
---
### 🔨 Ejercicio 1 — Expansión Radial del Cordyceps ⭐ (6 pts)

Imprime una cuadrícula 6×6 donde una zona está infectada si su **distancia Manhattan** al centro (fila=3, col=3) es ≤ 2.

**Distancia Manhattan:** `abs(fila - 3) + abs(col - 3)`
*(Representa cómo la infección se mueve por calles de ciudad, no en línea recta a través de paredes.)*

Zonas infectadas → `[X]`, zonas limpias → `[ ]`

Título: `"Día 3 — Expansión radial del Cordyceps desde Paciente Zero, Boston QZ"`

✅ Al terminar ejecuta `grader.check_ex1()`"""))

cells.append(code("nb3-31-ej1", """\
# Día 3 — Expansión radial del Cordyceps desde Paciente Zero, Boston QZ

### TU CODIGO AQUI ###
"""))

cells.append(code("nb3-31-ej1-check", "grader.check_ex1()"))

cells.append(md("nb3-31-ej1-exp", """\
> 💬 **Explicación:** ¿Qué representa la distancia Manhattan en términos reales?
> ¿Por qué no usamos distancia en línea recta para modelar una ciudad?
> *(Doble-click para responder aquí)*"""))

cells.append(md("nb3-31-ej2-md", """\
---
### 🔨 Ejercicio 2 — Dos Patógenos, Mismo Mapa ⭐ (6 pts)

Imprime **dos cuadrículas 6×6** con título sobre cada una:

- **Mapa 1 — Cordyceps:** radio ≤ 2, centro (3, 3)
- **Mapa 2 — COVID-19:** radio ≤ 1, centro (3, 3)

Después de cada mapa, imprime cuántas zonas están infectadas:
```
Cordyceps: X zonas.  COVID-19: Y zonas.
```

Primera comparación explícita entre ficción y realidad del notebook."""))

cells.append(code("nb3-31-ej2", """\
### TU CODIGO AQUI ###
"""))

cells.append(code("nb3-31-ej2-check", "grader.check_ex2()"))

cells.append(md("nb3-31-ej2-exp", """\
> 💬 **Explicación:** El sarampión tiene R0 = 15. Si modelaras su radio de expansión en este grid, ¿qué pasaría con la ciudad?
> *(Doble-click para responder aquí)*"""))

cells.append(md("nb3-31-debug1-md", """\
---
### 🔧 Debug 1 — Error de Indentación

El `print` está en el nivel de indentación equivocado — se ejecuta después del loop interior en vez de dentro de él. El resultado es una sola columna en vez de una cuadrícula.

1. Ejecuta y observa la salida incorrecta
2. Identifica en qué nivel de loop pertenece el `print`
3. Corrige la indentación

**Resultado esperado:** una cuadrícula 3×3 de asteriscos"""))

cells.append(code("nb3-31-debug1", """\
for fila in range(3):
    for col in range(3):
        zona = fila * 3 + col
    print(f"[{zona}]", end=" ")  # ← ¿adentro o afuera del loop interior?
print()"""))

cells.append(code("nb3-31-debug1-check", "grader.check_debug1()"))

cells.append(md("nb3-31-t1-md", """\
---
**❓ Pregunta T1 — Ejecuciones del loop interior**

En un nested loop de **6 filas × 5 columnas**, ¿cuántas veces ejecuta el `print` interior?

- **a)** 11
- **b)** 30
- **c)** 6
- **d)** 5"""))

cells.append(code("nb3-31-t1", 'respuesta_t1 = "?"   # 📝 escribe: a, b, c o d'))

cells.append(code("nb3-31-t1-check", "grader.check_t1()"))

cells.append(code("nb3-31-mini-a", "grader.check_mini_a()   # ✅ Checkpoint 3.1"))

# ════════════════════════════════════════════════════════════
# SECCIÓN 3.2 — NESTED LOOPS + TIEMPO: LA PROPAGACIÓN
# ════════════════════════════════════════════════════════════

cells.append(md("nb3-32-theory", """\
---
## 3.2 — Loops Anidados + Tiempo: La Propagación

Combinamos el loop exterior (el tiempo — días) con el loop interior (el espacio — zonas de la ciudad). El número total de iteraciones = días × zonas.

---

### R0 — El número más importante de la epidemiología

> **R0** (número básico de reproducción) es el número de personas que un infectado contagia en promedio en una población completamente susceptible.

| R0 > 1 | La epidemia **crece** |
|--------|----------------------|
| R0 = 1 | La epidemia es **endémica** |
| R0 < 1 | La epidemia **muere** |

Conseguir R0 < 1 fue el objetivo de cada cuarentena en la historia.

| Patógeno | R0 | Mortalidad |
|----------|----|-----------|
| Cordyceps | 3.5 | 85% |
| Walker | 1.2 | 100% |
| COVID-19 | 2.5 | 2% |
| Ébola | 1.8 | 65% |
| Gripe 1918 | 2.0 | 10% |
| **Sarampión** | **15.0** | 0.2% |
| Peste Bubónica | 2.6 | 30% |

El sarampión tiene el R0 más alto de todos los patógenos conocidos. Una habitación con un infectado puede contagiar a todas las personas no vacunadas presentes."""))

cells.append(md("nb3-32-r0-viz-md", """\
---
### 📊 Visualiza — R₀ en escala real

> *"— Marlene. Diario de campo, semana 3 post-Colapso. Los números de R₀ en la tabla no significan nada hasta que los ves en escala. El sarampión es 6× más contagioso que COVID. En una ciudad sin vacunar, eso es una sentencia de extinción."*

*Ejecuta para ver la transmisibilidad comparada de todos los patógenos.*"""))

cells.append(code("nb3-32-r0-viz", """\
# 📊 Transmisibilidad comparada — R₀ por patógeno
viz.grafico_r0(nombres, r0_valores)"""))

cells.append(md("nb3-32-obs1-md", """\
### 👀 Observa — 5 días, 4 zonas

Loop exterior: 5 días. Loop interior: 4 zonas. Cada día cada zona multiplica sus infectados por R0. Observa el crecimiento exponencial simultáneo en todas las zonas."""))

cells.append(code("nb3-32-obs1", """\
infectados_iniciales = [10, 15, 5, 20]   # infectados en cada zona al inicio
r0 = 2.5  # COVID-19

zonas = infectados_iniciales[:]  # copia para no modificar los originales

print(f"{'Día':<5}", end="")
for z in range(4):
    print(f"{'Zona '+str(z+1):<12}", end="")
print()
print("─" * 53)

for dia in range(1, 6):
    print(f"{dia:<5}", end="")
    for i in range(len(zonas)):
        zonas[i] = int(zonas[i] * r0)
        print(f"{zonas[i]:<12}", end="")
    print()"""))

cells.append(md("nb3-32-mod1-md", """\
### ✏️ Modifica — Cambia R0 a 0.7

Cambia `r0 = 2.5` a `r0 = 0.7`. Observa cómo la epidemia se extingue en vez de crecer.

*"Esto es exactamente lo que cada mascarilla, cuarentena y campaña de vacunación intentó lograr matemáticamente."*"""))

cells.append(code("nb3-32-mod1", """\
infectados_iniciales = [10, 15, 5, 20]
r0 = 0.7  # ← cambia este valor (prueba 0.7, 1.0, 1.5, 2.5)
# R0 < 1: la epidemia muere. R0 = 1: endémica. R0 > 1: crece.

zonas = infectados_iniciales[:]
for dia in range(1, 6):
    print(f"Día {dia}: ", end="")
    for i in range(len(zonas)):
        zonas[i] = int(zonas[i] * r0)
        print(f"Zona {i+1}={zonas[i]:<6}", end="")
    print()"""))

cells.append(md("nb3-32-pred1-md", """\
### 🔮 Predice — Día 3, Zona 2

Loop exterior: 3 días. Loop interior: 2 zonas. `infectados = [10, 20]`, `R0 = 2.0`.

¿Cuántos infectados hay en la **Zona 2** en el **Día 3**? Calcula a mano antes de ejecutar.

```
Día 1 — Zona 2: 20 × 2.0 = ___
Día 2 — Zona 2: ___ × 2.0 = ___
Día 3 — Zona 2: ___ × 2.0 = ___
```"""))

cells.append(code("nb3-32-pred1", """\
# Mi predicción: Zona 2 en Día 3 = ____

zonas = [10, 20]
r0 = 2.0
for dia in range(1, 4):
    for i in range(len(zonas)):
        zonas[i] = int(zonas[i] * r0)
    print(f"Día {dia}: Zona 1={zonas[0]}  Zona 2={zonas[1]}")"""))

cells.append(md("nb3-32-comp1-md", """\
### 🧩 Completa — El acumulador en el nivel correcto

Completa los blancos `___` para acumular el total de infectados **a través de todas las zonas en todos los días**.

**Pista:** el acumulador debe inicializarse FUERA del loop más externo y actualizarse DENTRO del más interno."""))

cells.append(code("nb3-32-comp1", """\
zonas = [10, 20, 30]
dias  = 5
total = ___   # ← valor inicial

for dia in range(dias):
    for i in range(len(zonas)):
        zonas[i] = int(zonas[i] * 1.5)
        total ___ zonas[i]   # ← operador acumulador

print(f"Total acumulado de infecciones: {total}")"""))

cells.append(md("nb3-32-ej3-md", """\
---
### 🔨 Ejercicio 3 — Propagación en 5 Zonas ⭐ (8 pts)

Simula 7 días de propagación en 5 zonas usando R0 = 1.8 (entre Ébola y COVID-19).

```python
infectados = [5, 12, 3, 20, 8]
poblaciones = [500, 1200, 300, 2000, 800]
```

- Cada día: multiplica infectados por R0 (usa `int()`), luego limita al máximo de la población
- Imprime una tabla: filas = días, columnas = zonas, última columna = total ciudad
- Anota cuáles zonas alcanzan su capacidad máxima primero

✅ Al terminar ejecuta `grader.check_ex3()`"""))

cells.append(code("nb3-32-ej3", """\
infectados  = [5, 12, 3, 20, 8]
poblaciones = [500, 1200, 300, 2000, 800]
r0  = 1.8
dias = 7

### TU CODIGO AQUI ###
"""))

cells.append(code("nb3-32-ej3-check", "grader.check_ex3()"))

cells.append(md("nb3-32-ej3-exp", """\
> 💬 **Explicación:** ¿Qué zona colapsa primero? ¿Es siempre la que empieza con más infectados? ¿Por qué?
> *(Doble-click para responder aquí)*"""))

cells.append(md("nb3-32-ej3-viz-md", """\
---
### 🌍 Visualiza — Tu simulación en Lima, Perú

Las **mismas tasas de infección** que acabas de calcular, proyectadas sobre el mapa real de Lima.
Los distritos más grandes de la ciudad. Los mismos distritos donde vivió el brote de COVID-19 más letal del mundo.

*Ejecuta la celda de abajo para ver tus resultados en el mapa.*"""))

cells.append(code("nb3-32-ej3-viz", """\
# 🗺 Tu simulación de propagación — Lima, Perú
# Si aún no completaste el Ejercicio 3, usamos valores de referencia para que el mapa funcione.
_zonas_nombres = ["San Juan de Lurigancho", "Ate", "Comas", "Villa El Salvador", "San Martín de Porres"]

try:
    _infectados_viz = list(infectados)
    _pobs_viz       = list(poblaciones)
    _dias_viz       = dias
    _r0_viz         = r0
    if _infectados_viz == [5, 12, 3, 20, 8]:   # ejercicio no completado aún
        raise ValueError("ejercicio pendiente")
except (NameError, ValueError):
    # Valores de referencia: día 7, R₀=1.8, mismas poblaciones del ejercicio
    _pobs_viz       = [500, 1200, 300, 2000, 800]
    _infectados_viz = [min(int(x * 1.8**7), p) for x, p in zip([5, 12, 3, 20, 8], _pobs_viz)]
    _dias_viz       = 7
    _r0_viz         = 1.8
    print("⚠️  Ejercicio 3 pendiente — mostrando simulación de referencia (Día 7, R₀=1.8)")

viz.semaforo_ciudad(_zonas_nombres, _infectados_viz, _pobs_viz, dia=_dias_viz, patogeno=f"COVID-19 (R₀={_r0_viz})")
mapa.brote_actual("lima", _infectados_viz, _pobs_viz, dia=_dias_viz, patogeno=f"COVID-19 simulado (R₀={_r0_viz})")"""))

cells.append(md("nb3-32-prop-viz-md", """\
---
### 📈 [ ANÁLISIS TEMPORAL — PROPAGACIÓN POR ZONA ]

El semáforo muestra el estado en **un día**. Este gráfico muestra **cómo llegó cada zona hasta ese punto** — la trayectoria completa de la simulación.

---

**[ LECTURA ]** Cada línea es una zona. La línea punteada blanca es el total ciudad. Las zonas con más casos iniciales saturan primero.

**[ CONCLUSIÓN ]** Con R₀ > 1, todas las zonas colapsan eventualmente — la diferencia es el tiempo. La zona que empieza con más infectados llega al límite días antes que las demás.

**[ MISIÓN ]** Cambia `r0 = 1.8` a `r0 = 0.7` en el ejercicio. ¿Qué le pasa a la curva total? ¿Por qué?"""))

cells.append(code("nb3-32-prop-viz", """\
# 📈 Propagación por zona — reconstruye el historial completo
_pob_ini = [5, 12, 3, 20, 8]
_pobs_ej3 = [500, 1200, 300, 2000, 800]
_z_names = ["Zona Norte", "Zona Este", "Zona Centro", "Zona Sur", "Zona Oeste"]
_sim = _pob_ini[:]
_hist = []
for _d in range(7):
    for _i in range(len(_sim)):
        _sim[_i] = min(int(_sim[_i] * 1.8), _pobs_ej3[_i])
    _hist.append(_sim[:])
viz.curva_propagacion(_hist, labels=_z_names, r0=1.8, patogeno="Propagación Urbana (R₀=1.8)")"""))

cells.append(md("nb3-32-ej4-md", """\
---
### 🔨 Ejercicio 4 — Tres Patógenos, Diez Días ⭐⭐ (8 pts)

Simula 10 días para tres patógenos reales de los datos del notebook:

- `r0_valores[2]` — COVID-19
- `r0_valores[3]` — Ébola
- `r0_valores[5]` — Sarampión

**Condiciones:** `infectados_iniciales = 50`, `poblacion = 50_000`

Loop exterior: patógenos. Loop interior: 10 días.

Imprime el **total infectados en día 10** para cada patógeno. El resultado del sarampión será impactante.

✅ Al terminar ejecuta `grader.check_ex4()`"""))

cells.append(code("nb3-32-ej4", """\
infectados_0 = 50
poblacion    = 50_000

### TU CODIGO AQUI ###
"""))

cells.append(code("nb3-32-ej4-check", "grader.check_ex4()"))

cells.append(md("nb3-32-ej4-exp", """\
> 💬 **Explicación:** El sarampión tiene R0 = 15 pero mortalidad = 0.2%. El Ébola tiene R0 = 1.8 pero mortalidad = 65%. ¿Cuál es más peligroso para una ciudad? ¿De qué depende?
> *(Doble-click para responder aquí)*"""))

cells.append(md("nb3-32-debug2-md", """\
---
### 🔧 Debug 2 — Acumulador en el Nivel Equivocado

El código corre sin error pero el total de cada día es incorrecto. El acumulador `total_ciudad` se reinicia en el lugar equivocado — una vuelta por zona en vez de una vez por día.

1. Ejecuta y observa los totales incorrectos
2. Identifica en qué nivel de loop está el `total_ciudad = 0`
3. Muévelo al nivel correcto y verifica

**Resultado esperado:** el total del Día 1 debería ser la suma de todas las zonas después de aplicar R0."""))

cells.append(code("nb3-32-debug2", """\
infectados_zonas = [10, 20, 30, 40, 50]
r0   = 1.5
dias = 3

for dia in range(1, dias + 1):
    for i in range(len(infectados_zonas)):
        total_ciudad = 0            # ← BUG: ¿nivel correcto?
        infectados_zonas[i] = int(infectados_zonas[i] * r0)
        total_ciudad += infectados_zonas[i]
    print(f"Día {dia}: Total ciudad = {total_ciudad}")"""))

cells.append(code("nb3-32-debug2-check", "grader.check_debug2()"))

cells.append(md("nb3-32-debug2b-md", """\
---
### 🔧 Debug 2B — El Error que Mató a 50 Millones

> *"Los epidemiólogos de 1918 creyeron que la primera ola de la Gripe Española había terminado en el verano. Sus modelos decían que sí. Pero sus modelos tenían un error fundamental."*

El código de abajo simula dos olas de un brote. Corre sin error Python — pero el resultado es **epidemiológicamente incorrecto**. La segunda ola ignora cuántas personas quedaron susceptibles después de la primera.

1. Ejecuta y observa: ¿por qué la Ola 2 empieza igual que la Ola 1?
2. Identifica la línea que borra la "memoria" del sistema entre olas
3. Corrígela para que la segunda ola comience con la población que **no se infectó** en la primera

**Pista:** ¿Cuántos susceptibles quedan después de la Ola 1? Eso es el punto de inicio de la Ola 2, no `infectados_0`.

**Resultado esperado:** la Ola 2 debe empezar con **menos** infectados iniciales que la Ola 1 porque parte de la población ya es inmune."""))

cells.append(code("nb3-32-debug2b", """\
poblacion    = 100_000
infectados_0 = 100
r0           = 2.0
dias_por_ola = 10

for ola in range(1, 3):
    infectados = infectados_0   # ← BUG: ¿debería ser siempre infectados_0?
    print(f"\\n=== OLA {ola} ===")
    for dia in range(1, dias_por_ola + 1):
        infectados = min(int(infectados * r0), poblacion)
        print(f"  Día {dia}: {infectados:>7} infectados")
    print(f"  Fin Ola {ola}: {infectados:>7} infectados acumulados")
    # Bug: la siguiente ola debería empezar desde 'infectados' (quienes quedan)
    # no desde infectados_0 (como si la Ola 1 nunca ocurrió)"""))

cells.append(code("nb3-32-debug2b-check", "grader.check_debug2b()"))

cells.append(md("nb3-32-ej5-context", """\
---

> *"La segunda ola de la Gripe Española de 1918 fue más mortífera que la primera — no porque el virus cambiara, sino porque más gente era susceptible después del verano. Las matemáticas no cambiaron. Solo el número inicial."*"""))

cells.append(md("nb3-32-ej5-md", """\
### 🔨 Ejercicio 5 — Las Dos Olas de 1918 ⭐⭐ (8 pts)

Simula las dos olas de la Gripe Española en una ciudad de **100,000 personas**, 10 días cada una, R0 = 2.0.

- **Ola 1:** `infectados_0 = 100`
- **Ola 2:** `infectados_0 = 5_000`

Imprime ambas simulaciones día a día y la diferencia en infectados totales al día 10.

✅ Al terminar ejecuta `grader.check_ex5()`"""))

cells.append(code("nb3-32-ej5", """\
poblacion = 100_000
r0        = 2.0
dias      = 10

### TU CODIGO AQUI ###
# Ola 1: infectados_0 = 100
# Ola 2: infectados_0 = 5_000
# Imprime ambas y la diferencia en día 10
"""))

cells.append(code("nb3-32-ej5-check", "grader.check_ex5()"))

cells.append(md("nb3-32-ej5-exp", """\
> 💬 **Explicación:** ¿Por qué importa tanto el número de infectados iniciales? ¿Qué implicación tiene esto para la detección temprana?
> *(Doble-click para responder aquí)*"""))

cells.append(md("nb3-32-ej5-viz-md", """\
---
### 📊 Visualiza — Las dos olas de la Gripe Española

Esto es exactamente la curva que los epidemiólogos analizaron en 1919 para entender por qué la segunda ola mató más que la primera.
La diferencia no fue el virus. Fue el número de infectados con los que empezó cada ola.

*Ejecuta para ver las dos curvas superpuestas.*"""))

cells.append(code("nb3-32-ej5-viz", """\
# 📊 Las dos olas — Gripe Española 1918
_pob = 100_000
_r0  = 2.0
_ola1, _ola2 = [100], [5_000]
for _ in range(9):
    _ola1.append(min(int(_ola1[-1] * _r0), _pob))
    _ola2.append(min(int(_ola2[-1] * _r0), _pob))

viz.comparar_patogenos(
    {"Gripe 1918 — Ola 1 (inicio: 100)":    _ola1,
     "Gripe 1918 — Ola 2 (inicio: 5,000)":  _ola2},
    titulo="Las Dos Olas — Gripe Española 1918"
)"""))

cells.append(md("nb3-32-ej5-interp", """\
---

**[ LECTURA ]** Misma Gripe Española 1918, mismo R₀ = 2.0. Dos puntos de partida: Ola 1 empieza con 100 infectados (sólida), Ola 2 con 5,000 (discontinua). La forma de la curva es idéntica — solo el tiempo cambia.

**[ CONCLUSIÓN ]** El R₀ determina la *forma*; el punto de inicio determina el *momento*. Con 5,000 infectados el Día 1, la epidemia ya lleva ventaja cuando los sistemas de detección la detectan.

**[ MISIÓN ]** Cambia `_ola2 = [5_000]` a `_ola2 = [500]`. ¿En cuántos días más aparece el pico? ¿Hay un umbral de inicio que haría a las dos olas prácticamente iguales?"""))

cells.append(code("nb3-32-mini-b", "grader.check_mini_b()   # ✅ Checkpoint 3.2"))

# ════════════════════════════════════════════════════════════
# SECCIÓN 3.3 — NESTED IFS: TRIAGE Y CLASIFICACIÓN
# ════════════════════════════════════════════════════════════

cells.append(md("nb3-33-theory", """\
---
## 3.3 — Ifs Anidados: Triage y Clasificación

Un **if anidado** es una decisión que depende de una decisión anterior. La estructura real del triage médico:

```
¿Está infectado?
├── SÍ → ¿Cuántas horas de exposición?
│         ├── < 24h → ¿Hay recursos médicos?
│         │           ├── SÍ → CUARENTENA TEMPRANA (posible supervivencia)
│         │           └── NO → CUARENTENA TEMPRANA sin recursos
│         └── ≥ 24h → CUARENTENA TARDÍA
└── NO  → ¿Tiene inmunidad?
          ├── SÍ → INMUNE — caso de estudio
          └── NO → LIMPIO — susceptible
```

> **Clave:** un if anidado solo se evalúa si el if exterior fue `True`. No son condiciones independientes — son una cadena de decisiones.

---

### CFR — Tasa de Mortalidad por Caso

**CFR (Case Fatality Rate):** porcentaje de infectados confirmados que mueren.

| Patógeno | CFR |
|----------|-----|
| COVID-19 | 2% |
| Gripe 1918 | 10% |
| Ébola | 65% |
| Cordyceps | 85% |
| Walker | 100% |

Con Ébola, una zona puede declararse perdida con mucho menos infectados que con COVID-19."""))

cells.append(md("nb3-33-cfr-viz-md", """\
---
### 📊 Visualiza — CFR en perspectiva real

> *"— Ellie: '¿Por qué Ébola necesita más recursos que COVID si infecta menos gente?' — Joel: 'Porque mata al 65% de los que toca. Un infectado de Ébola vale veinte de COVID en el triage. Eso es el CFR.'"*

El CFR determina cuán agresivo debe ser el protocolo. Compara los 7 patógenos antes de escribir el clasificador.

*Ejecuta para ver la tasa de mortalidad comparada.*"""))

cells.append(code("nb3-33-cfr-viz", """\
# 📊 Tasa de mortalidad por caso — CFR por patógeno
viz.grafico_cfr(nombres, mortalidad)"""))

cells.append(md("nb3-33-obs1-md", """\
### 👀 Observa — Árbol de triage completo

Ejecuta y observa cómo cada nivel del if se evalúa solo si el anterior fue verdadero. Cambia los valores y traza qué rama se activa."""))

cells.append(code("nb3-33-obs1", """\
infectado        = True
horas_expuesto   = 18
tiene_inmunidad  = False
recursos_medicos = True

if infectado:
    if horas_expuesto < 24:
        if recursos_medicos:
            resultado = "CUARENTENA TEMPRANA — recursos disponibles"
        else:
            resultado = "CUARENTENA TEMPRANA — sin recursos, riesgo alto"
    else:
        resultado = "CUARENTENA TARDÍA — exposición prolongada"
else:
    if tiene_inmunidad:
        resultado = "LIMPIO + INMUNE — candidato a donante de plasma"
    else:
        resultado = "LIMPIO — susceptible"

print(resultado)"""))

cells.append(md("nb3-33-mod1-md", """\
### ✏️ Modifica — Cruza todas las ramas

Prueba estas combinaciones en orden y observa qué rama se activa:

1. `infectado=False`, `tiene_inmunidad=True`
2. `infectado=True`, `horas_expuesto=48`
3. `infectado=True`, `horas_expuesto=10`, `recursos_medicos=False`

Nota: cuando `infectado=False`, el if interior de `horas_expuesto` **nunca se evalúa**."""))

cells.append(code("nb3-33-mod1", """\
infectado        = False     # ← cambia
horas_expuesto   = 10        # ← cambia
tiene_inmunidad  = True      # ← solo importa si infectado=False
recursos_medicos = False     # ← cambia

if infectado:
    if horas_expuesto < 24:
        if recursos_medicos:
            resultado = "CUARENTENA TEMPRANA — recursos disponibles"
        else:
            resultado = "CUARENTENA TEMPRANA — sin recursos, riesgo alto"
    else:
        resultado = "CUARENTENA TARDÍA — exposición prolongada"
else:
    if tiene_inmunidad:
        resultado = "LIMPIO + INMUNE — candidato a donante de plasma"
    else:
        resultado = "LIMPIO — susceptible"

print(resultado)"""))

cells.append(md("nb3-33-pred1-md", """\
### 🔮 Predice — Traza el árbol manualmente

Dados: `infectado=True`, `horas_expuesto=10`, `recursos_medicos=False`

Traza cada decisión manualmente y escribe el resultado antes de ejecutar.

```
¿infectado?        → ___
¿horas < 24?       → ___
¿recursos_medicos? → ___
Resultado:         → ___
```"""))

cells.append(code("nb3-33-pred1", """\
# Mi predicción: resultado = ____

infectado        = True
horas_expuesto   = 10
tiene_inmunidad  = False
recursos_medicos = False

if infectado:
    if horas_expuesto < 24:
        if recursos_medicos:
            resultado = "CUARENTENA TEMPRANA — recursos disponibles"
        else:
            resultado = "CUARENTENA TEMPRANA — sin recursos, riesgo alto"
    else:
        resultado = "CUARENTENA TARDÍA"
else:
    if tiene_inmunidad:
        resultado = "LIMPIO + INMUNE"
    else:
        resultado = "LIMPIO — susceptible"

print(resultado)"""))

cells.append(md("nb3-33-comp1-md", """\
### 🧩 Completa — Operador de comparación

Completa el operador `___` para que la cuarentena temprana se active cuando la exposición es **menor de 24 horas**.

**Opciones:** `<`  `<=`  `>`  `>=`  `==`"""))

cells.append(code("nb3-33-comp1", """\
infectado      = True
horas_expuesto = 18

if infectado:
    if horas_expuesto ___ 24:
        print("Cuarentena temprana — posible supervivencia")
    else:
        print("Cuarentena tardía")"""))

cells.append(md("nb3-33-ej6-md", """\
---

> *"Durante el brote de Ébola de 2014 en Guinea, el tiempo hasta el aislamiento fue el factor más determinante de supervivencia — exactamente este árbol de decisión."*

---

### 🔨 Ejercicio 6 — Clasificador de Triage ⭐⭐ (8 pts)

Dado un paciente con: `infectado` (bool), `horas_expuesto` (int), `tiene_inmunidad` (bool), `recursos_medicos` (bool)

Clasifícalo usando ifs anidados:

| Clasificación | Condición |
|---------------|-----------|
| `"LIMPIO"` | no infectado, sin inmunidad |
| `"INMUNE — CASO DE ESTUDIO"` | no infectado, con inmunidad |
| `"CUARENTENA TEMPRANA"` | infectado, horas < 24 |
| `"CUARENTENA TARDÍA"` | infectado, horas ≥ 24, con recursos |
| `"CASO PERDIDO"` | infectado, horas ≥ 24, sin recursos |

Prueba con los 6 pacientes de la lista. Cada clasificación debe activarse al menos una vez.

✅ Al terminar ejecuta `grader.check_ex6()`"""))

cells.append(code("nb3-33-ej6", """\
# (infectado, horas_expuesto, tiene_inmunidad, recursos_medicos)
pacientes = [
    (False, 0,  False, True),    # Paciente 1
    (False, 0,  True,  True),    # Paciente 2
    (True,  8,  False, True),    # Paciente 3
    (True,  8,  False, False),   # Paciente 4
    (True,  36, False, True),    # Paciente 5
    (True,  48, False, False),   # Paciente 6
]

### TU CODIGO AQUI ###
"""))

cells.append(code("nb3-33-ej6-check", "grader.check_ex6()"))

cells.append(md("nb3-33-ej6-exp", """\
> 💬 **Explicación:** ¿Por qué verificamos `infectado` ANTES de `recursos_medicos`? ¿Qué pasaría si invirtieras el orden?
> *(Doble-click para responder aquí)*"""))

cells.append(md("nb3-33-debug3-md", """\
---
### 🔧 Debug 3 — Error de Árbol

El if de severidad está bajo el `else` en vez de bajo `if infectado`. El código corre pero clasifica mal — un paciente infectado nunca llega al check de horas.

1. Ejecuta con `infectado=True`, `horas_expuesto=10`
2. Observa que el resultado es incorrecto
3. Mueve el if de horas al nivel correcto

**Resultado esperado:** `"Cuarentena temprana — recursos OK"`"""))

cells.append(code("nb3-33-debug3", """\
infectado        = True
horas_expuesto   = 10
recursos_medicos = True

if infectado:
    resultado = "Caso confirmado"
else:
    if horas_expuesto < 24:      # ← ¿debería estar aquí?
        if recursos_medicos:
            resultado = "Cuarentena temprana — recursos OK"
        else:
            resultado = "Cuarentena temprana — sin recursos"
    else:
        resultado = "Cuarentena tardía"

print(resultado)"""))

cells.append(code("nb3-33-debug3-check", "grader.check_debug3()"))

cells.append(md("nb3-33-ej7-md", """\
---
### 🔨 Ejercicio 7 — Clasificador de Zonas ⭐⭐ (8 pts)

Clasifica una zona usando umbrales epidemiológicos reales.

**Inputs:** `infectados`, `poblacion`, `dias_sin_suministros`, `cfr`

| Clasificación | Condición |
|---------------|-----------|
| `"ZONA PERDIDA"` | tasa > 60% **O** cfr > 0.5 ← **verifica primero** |
| `"ZONA ROJA"` | tasa > 20% **O** sin suministros > 3 días |
| `"ZONA AMARILLA"` | tasa 5%–20% |
| `"ZONA VERDE"` | tasa < 5% |

Prueba con parámetros de COVID-19 (`mortalidad[2]`) y Ébola (`mortalidad[3]`) — misma zona, diferente patógeno, diferente resultado.

✅ Al terminar ejecuta `grader.check_ex7()`"""))

cells.append(code("nb3-33-ej7", """\
# Prueba 1: COVID-19
infectados           = 800
poblacion            = 5000
dias_sin_suministros = 4
cfr                  = mortalidad[2]   # COVID-19

### TU CODIGO AQUI ###

# Prueba 2: Ébola (misma zona)
cfr = mortalidad[3]   # Ébola
### TU CODIGO AQUI (Ébola) ###
"""))

cells.append(code("nb3-33-ej7-check", "grader.check_ex7()"))

cells.append(md("nb3-33-ej7-exp", """\
> 💬 **Explicación:** Con Ébola (CFR=0.65) una zona puede declararse perdida con menos infectados que con COVID (CFR=0.02). ¿Tiene sentido desde el punto de vista médico?
> *(Doble-click para responder aquí)*"""))

cells.append(md("nb3-33-t2-md", """\
---
**❓ Pregunta T2 — Evaluación del if anidado**

¿Cuándo se evalúa un if **anidado**?

- **a)** Siempre
- **b)** Solo si el if exterior es `True`
- **c)** Solo si el if exterior es `False`
- **d)** Al mismo tiempo que el if exterior"""))

cells.append(code("nb3-33-t2", 'respuesta_t2 = "?"   # 📝 escribe: a, b, c o d'))

cells.append(code("nb3-33-t2-check", "grader.check_t2()"))

cells.append(code("nb3-33-mini-c", "grader.check_mini_c()   # ✅ Checkpoint 3.3"))

# ════════════════════════════════════════════════════════════
# SECCIÓN 3.4 — BRIDGE: NESTED LOOPS + NESTED IFS
# ════════════════════════════════════════════════════════════

cells.append(md("nb3-34-theory", """\
---
## 3.4 — Bridge: Loops Anidados + Ifs Anidados

> **Ya sabes nested loops. Ya sabes nested ifs. Esta sección los combina. No hay sintaxis nueva — solo las dos herramientas trabajando juntas.**

Un loop itera. Un if decide. Un loop con un if adentro **itera Y decide en cada paso**. Eso es una simulación: el tiempo avanza, y en cada momento el sistema toma decisiones basadas en su estado actual.

```python
for dia in range(dias):          # tiempo avanza
    for zona in range(zonas):    # espacio se recorre
        if condicion:            # decisión en cada celda
            ...
```

Así funcionaron los modelos que usaron los CDC durante COVID-19."""))

cells.append(md("nb3-34-obs1-md", """\
### 👀 Observa — Simulación completa: 7 días, 5 zonas, COVID-19

Loop exterior: 7 días. Loop interior: 5 zonas. Ifs anidados: si la zona cayó → muestra `[PERDIDA]`; si no cayó → aplica R0 o marca caída si tasa > 60%."""))

cells.append(code("nb3-34-obs1", """\
poblaciones  = [5000, 3000, 8000, 2000, 10000]
infectados_z = [100, 50, 200, 30, 500]
r0           = r0_valores[2]   # COVID-19
zonas_caidas = [False] * 5

for dia in range(1, 8):
    print(f"\\n=== DÍA {dia} ===")
    for z in range(5):
        if zonas_caidas[z]:
            print(f"  Zona {z+1}: [PERDIDA]")
        else:
            tasa = infectados_z[z] / poblaciones[z]
            if tasa > 0.6:
                zonas_caidas[z] = True
                print(f"  Zona {z+1}: ❌ ZONA PERDIDA (tasa {tasa:.1%})")
            else:
                infectados_z[z] = min(int(infectados_z[z] * r0), poblaciones[z])
                print(f"  Zona {z+1}: {infectados_z[z]:>6} infectados ({tasa:.1%})")"""))

cells.append(md("nb3-34-mod1-md", """\
### ✏️ Modifica — Cambia el patógeno

Cambia `r0 = r0_valores[2]` (COVID-19) a `r0 = r0_valores[5]` (Sarampión, R0=15).

Misma ciudad. Mismas condiciones iniciales. Diferente patógeno.

*"Este es el motivo por el que existen las campañas de vacunación contra el sarampión."*"""))

cells.append(code("nb3-34-mod1", """\
poblaciones  = [5000, 3000, 8000, 2000, 10000]
infectados_z = [100, 50, 200, 30, 500]
r0           = r0_valores[2]   # ← cambia el índice (prueba r0_valores[5])
zonas_caidas = [False] * 5

for dia in range(1, 8):
    print(f"\\n=== DÍA {dia} ===")
    for z in range(5):
        if zonas_caidas[z]:
            print(f"  Zona {z+1}: [PERDIDA]")
        else:
            tasa = infectados_z[z] / poblaciones[z]
            if tasa > 0.6:
                zonas_caidas[z] = True
                print(f"  Zona {z+1}: ❌ ZONA PERDIDA")
            else:
                infectados_z[z] = min(int(infectados_z[z] * r0), poblaciones[z])
                print(f"  Zona {z+1}: {infectados_z[z]:>6} infectados ({tasa:.1%})")"""))

cells.append(md("nb3-34-pred1-md", """\
### 🔮 Predice — ¿Qué día cae la Zona 3?

Con los valores iniciales de la observación (R0=2.5, infectados_z[2]=200, poblaciones[2]=8000):

```
Día 1: 200 × 2.5 = ___ infectados (tasa = ___%)
Día 2: ___ × 2.5 = ___ infectados (tasa = ___%)
...
```

¿En qué día la tasa supera el 60% y la zona cae? Escribe tu predicción."""))

cells.append(code("nb3-34-pred1", """\
# Mi predicción: Zona 3 cae en el Día ___

# Verificación manual: calcula paso a paso
inf = 200
pob = 8000
for dia in range(1, 8):
    inf = min(int(inf * 2.5), pob)
    tasa = inf / pob
    print(f"Día {dia}: {inf} infectados ({tasa:.1%}) {'← CAÍDA' if tasa > 0.6 else ''}") """))

cells.append(md("nb3-34-ej8-md", """\
---

> *"En marzo 2020 Italia implementó cuarentena nacional en el día 14 de su brote documentado. Nueva Zelanda lo hizo en el día 5. Los resultados reflejan exactamente esta diferencia matemática."*

---

### 🔨 Ejercicio 8 — Protocolo de Cuarentena con Intervención ⭐⭐⭐ (10 pts)

Simula 21 días en 5 zonas con cuarentena. A partir del `dia_cuarentena`, el R0 efectivo se reduce a `r0_base × 0.4` (mascarillas + distanciamiento + confinamiento).

```python
poblaciones   = [5000, 3000, 8000, 2000, 10000]
infectados_z  = [100, 50, 200, 30, 500]
r0_base       = r0_valores[2]   # COVID-19
```

- Si `dia >= dia_cuarentena`: usa `r0_base * 0.4`
- Si tasa de una zona > 0.6: zona cae, no se actualiza más
- Registra: zonas caídas por día, total infectados ciudad por día
- **Corre dos veces:** con `dia_cuarentena = 5` y luego con `dia_cuarentena = 14`

✅ Al terminar ejecuta `grader.check_ex8()`"""))

cells.append(code("nb3-34-ej8", """\
poblaciones    = [5000, 3000, 8000, 2000, 10000]
infectados_z   = [100, 50, 200, 30, 500]
r0_base        = r0_valores[2]   # COVID-19
dia_cuarentena = 5               # ← cambia a 14 para la segunda corrida

zonas_caidas = [False] * 5

### TU CODIGO AQUI ###
"""))

cells.append(code("nb3-34-ej8-check", "grader.check_ex8()"))

cells.append(md("nb3-34-ej8-exp", """\
> 💬 **Explicación:** ¿Hay un punto de no retorno — un día después del cual la cuarentena ya no cambia el resultado? ¿Cómo lo encontrarías?
> *(Doble-click para responder aquí)*"""))

cells.append(md("nb3-34-ej8-viz-md", """\
---
### 📊 Visualiza — ¿Cuántas vidas vale un día de retraso?

Esta gráfica muestra el área entre las dos curvas (sin cuarentena vs con cuarentena).
Esa área es la diferencia en casos. Multiplicada por la tasa de mortalidad = vidas salvadas.

Italia esperó hasta el Día 14. Nueva Zelanda actuó en el Día 5.
Los resultados están en los datos históricos — y en tu gráfica.

*Ejecuta para ver el impacto cuantificado.*"""))

cells.append(code("nb3-34-ej8-viz", """\
# 📊 Impacto de la cuarentena — cambia dia_cuarentena y el gráfico se actualiza
_pobs_q = [5000, 3000, 8000, 2000, 10000]
_inf0_q = [10, 5, 20, 3, 50]          # inicio contenido — permite ver divergencia
_r0b    = r0_valores[2]               # COVID-19

# Cambia el número para explorar: ¿qué pasa si actúas el Día 3? ¿El Día 20?
viz.impacto_cuarentena(_inf0_q, _pobs_q, _r0b, dia_cuarentena=5,
                       nombre_patogeno="COVID-19", cfr=mortalidad[2], dias=30)
viz.impacto_cuarentena(_inf0_q, _pobs_q, _r0b, dia_cuarentena=14,
                       nombre_patogeno="COVID-19", cfr=mortalidad[2], dias=30)"""))

cells.append(md("nb3-34-ej8-viz-interp", """\
---

**[ LECTURA ]** Mismo COVID-19, misma ciudad, misma cuarentena — pero el Día 5 vs. el Día 14. El área sombreada es la diferencia: casos que no ocurrieron porque se actuó antes.

**[ CONCLUSIÓN ]** La curva sin intervención es idéntica en ambos gráficos. Lo que cambia es cuándo se dobla. Ferguson et al. (Imperial College, 2020) usó exactamente este modelo para estimar que cada semana de retraso duplicaba las muertes proyectadas en UK.

**[ MISIÓN ]** Cambia `cfr=mortalidad[2]` (COVID, 2%) por `cfr=mortalidad[3]` (Ébola, 65%). ¿Cuántas vidas adicionales salva actuar el Día 5 vs. el Día 14 con Ébola? ¿Es la diferencia proporcional?"""))

cells.append(md("nb3-34-diseno-md", """\
---
### 🧠 Actividad de Diseño — Tú Decides la Intervención

Hasta ahora, la cuarentena siempre reduce R0 a `r0 × 0.4`. Pero en la realidad los gobiernos eligieron entre **tres tipos de intervención** con lógicas diferentes:

| Opción | Intervención | Efecto epidemiológico | Implementación |
|--------|---|---|---|
| **A** | Cuarentena estricta | Reduce contactos más agresivamente: R0 × 0.3 | Cambia el factor de reducción |
| **B** | Rastreo de contactos | Detecta y aísla más temprano: activa en Día 5 | Cambia el día de activación |
| **C** | Vacunación parcial | Reduce susceptibles en 30% desde el inicio | Reduce infectados iniciales × 0.7 |

Las tres funciones ya están implementadas abajo. Tu trabajo es:
1. Correr las tres simulaciones (ya está el código)
2. Comparar los resultados con `viz.comparar_patogenos`
3. Escribir una oración explicando cuál salvó más vidas Y POR QUÉ desde el punto de vista epidemiológico

> *"En 2020, epidemiólogos del Imperial College discutieron exactamente estas tres opciones para el UK. Eligieron una combinación. Tu simulación recrea esa lógica."*"""))

cells.append(code("nb3-34-diseno", """\
# ══════════════════════════════════════════════
# TRES INTERVENCIONES — misma ciudad, 30 días
# COVID-19, 5 zonas — inicio contenido para ver divergencia
# ══════════════════════════════════════════════
_pobs = [5000, 3000, 8000, 2000, 10000]
_inf0 = [10, 5, 20, 3, 50]    # inicio bajo: las 3 intervenciones divergen más
_r0b  = r0_valores[2]          # COVID-19
_dias = 30

def _simular(inf_inicio, factor, dia_activa):
    \"\"\"Simula una intervención. Devuelve lista de totales ciudad por día.\"\"\"
    inf      = inf_inicio[:]
    caidas   = [False] * 5
    totales  = []
    for dia in range(1, _dias + 1):
        r0_hoy = _r0b * factor if dia >= dia_activa else _r0b
        total  = 0
        for z in range(5):
            if not caidas[z]:
                tasa = inf[z] / _pobs[z]
                if tasa > 0.6:
                    caidas[z] = True
                else:
                    inf[z] = min(int(inf[z] * r0_hoy), _pobs[z])
            total += inf[z]
        totales.append(total)
    return totales

# OPCIÓN A: Cuarentena estricta (R0 × 0.3, activa Día 7)
curva_A = _simular(_inf0, factor=0.3, dia_activa=7)

# OPCIÓN B: Rastreo de contactos (R0 × 0.5, activa Día 5 — más temprano pero menos agresivo)
curva_B = _simular(_inf0, factor=0.5, dia_activa=5)

# OPCIÓN C: Vacunación parcial (40% menos susceptibles desde inicio, R0 sin cambio)
_inf_vacunados = [int(v * 0.6) for v in _inf0]   # 40% ya inmunes al inicio
curva_C = _simular(_inf_vacunados, factor=1.0, dia_activa=999)

# Sin intervención — línea base
curva_base = _simular(_inf0, factor=1.0, dia_activa=999)

# Resultados en día final
print(f"Sin intervención:        {curva_base[-1]:>7,} infectados al Día {_dias}")
print(f"A — Cuarentena D7:       {curva_A[-1]:>7,} infectados al Día {_dias}")
print(f"B — Rastreo D5:          {curva_B[-1]:>7,} infectados al Día {_dias}")
print(f"C — Vacunación 40%:      {curva_C[-1]:>7,} infectados al Día {_dias}")

# Vidas salvadas estimadas (CFR = 2% → dividir entre 100)
_cfr = mortalidad[2]
for nombre, curva in [("A", curva_A), ("B", curva_B), ("C", curva_C)]:
    casos_evitados = sum(max(b - c, 0) for b, c in zip(curva_base, curva))
    print(f"  Intervención {nombre}: ~{int(casos_evitados * _cfr / 100):,} vidas salvadas estimadas")

# Mi conclusión — ¿cuál es más efectiva y por qué?
# (Pista: piensa en la RAZÓN epidemiológica, no solo en el número)
# Mi respuesta: ___

# ── Visualización ──────────────────────────────────────────
viz.comparar_patogenos(
    {"Sin intervención":             curva_base,
     "A — Cuarentena estricta":     curva_A,
     "B — Rastreo temprano Día 5": curva_B,
     "C — Vacunación parcial":      curva_C},
    titulo="Diseño de Intervención — COVID-19, 30 días"
)"""))

cells.append(md("nb3-34-debug4-md", """\
---
### 🔧 Debug 4 — Dos Errores

Este código tiene **dos bugs**:

1. **Bug 1:** el acumulador `total_infectados` se reinicia en el nivel incorrecto del loop
2. **Bug 2:** la condición del if está invertida (`<` en vez de `>`)

Encuentra y corrige ambos. Este es el debug más difícil del notebook."""))

cells.append(code("nb3-34-debug4", """\
zonas_inf   = [100, 150, 80, 200, 120]
poblaciones = [2000, 3000, 1500, 4000, 2500]
r0          = 2.0
dias        = 5

for dia in range(1, dias + 1):
    for z in range(len(zonas_inf)):
        total_infectados = 0         # ← BUG 1: ¿nivel correcto?
        zonas_inf[z] = min(int(zonas_inf[z] * r0), poblaciones[z])
        total_infectados += zonas_inf[z]
        tasa = zonas_inf[z] / poblaciones[z]
        if tasa < 0.5:               # ← BUG 2: ¿condición correcta?
            print(f"  ⚠️  Zona {z+1} en riesgo: {tasa:.1%}")
    print(f"Día {dia}: Total = {total_infectados}")"""))

cells.append(code("nb3-34-debug4-check", "grader.check_debug4()"))

cells.append(code("nb3-34-mini-d", "grader.check_mini_d()   # ✅ Checkpoint 3.4"))

# ════════════════════════════════════════════════════════════
# SECCIÓN 3.5 — FUNCIONES: LAS HERRAMIENTAS
# ════════════════════════════════════════════════════════════

cells.append(md("nb3-35-theory", """\
---
## 3.5 — Funciones: Las Herramientas

Los epidemiólogos no reescriben las ecuaciones cada vez que cambian el patógeno. Las **encapsulan en funciones**. Una función tiene nombre, recibe parámetros, devuelve un resultado. Es una herramienta: la construyes una vez, la usas cuando necesites.

```python
def nombre_funcion(parametro1, parametro2):
    resultado = ...       # calcula algo
    return resultado      # devuelve el valor
```

**DRY — Don't Repeat Yourself:**
> Si escribes la misma lógica más de una vez, deberías tener una función.

**`return` termina la función inmediatamente** y entrega el resultado. Lo que venga después de `return` no se ejecuta.

```python
def es_pandemia(r0):
    if r0 > 1:
        return True    # ← función termina aquí si R0 > 1
    return False       # ← solo llega aquí si R0 <= 1
```"""))

cells.append(md("nb3-35-obs1-md", """\
### 👀 Observa — Con y sin función: mismo resultado, diferente mantenimiento

Sin función: la misma fórmula repetida 4 veces.
Con función: la fórmula en un solo lugar, llamada 4 veces.

Si hay un error en la fórmula — ¿en cuántos lugares lo tienes que corregir en cada versión?"""))

cells.append(code("nb3-35-obs1", """\
# SIN función — la misma lógica repetida 4 veces
print("=== SIN FUNCIÓN ===")
print(int(100 * r0_valores[0]))   # Cordyceps
print(int(100 * r0_valores[2]))   # COVID-19
print(int(100 * r0_valores[3]))   # Ébola
print(int(100 * r0_valores[4]))   # Gripe 1918

print()

# CON función — definida una vez, usada 4 veces
print("=== CON FUNCIÓN ===")
def aplicar_r0(infectados, r0):
    return int(infectados * r0)

print(aplicar_r0(100, r0_valores[0]))   # Cordyceps
print(aplicar_r0(100, r0_valores[2]))   # COVID-19
print(aplicar_r0(100, r0_valores[3]))   # Ébola
print(aplicar_r0(100, r0_valores[4]))   # Gripe 1918"""))

cells.append(md("nb3-35-mod1-md", """\
### ✏️ Modifica — El poder del mantenimiento centralizado

Cambia la fórmula dentro de `aplicar_r0` a algo incorrecto (ej: `int(infectados * r0 + 9999)`).

Observa cómo todos los llamados producen resultados incorrectos.
Corrige la fórmula — todos los llamados se arreglan con un solo cambio."""))

cells.append(code("nb3-35-mod1", """\
def aplicar_r0(infectados, r0):
    return int(infectados * r0)   # ← cambia esta fórmula, luego corrígela

print(aplicar_r0(100, r0_valores[0]))
print(aplicar_r0(100, r0_valores[2]))
print(aplicar_r0(100, r0_valores[3]))
print(aplicar_r0(100, r0_valores[4]))"""))

cells.append(md("nb3-35-pred1-md", """\
### 🔮 Predice — Llamadas anidadas

Un llamado a una función es un valor. Eso significa que puedes usar el resultado directamente.

¿Qué devuelve `duplicar(duplicar(5))`?
¿Y `duplicar(3) + duplicar(4)`?

Calcula a mano antes de ejecutar."""))

cells.append(code("nb3-35-pred1", """\
# Mi predicción:
# duplicar(duplicar(5)) = ____
# duplicar(3) + duplicar(4) = ____

def duplicar(n):
    return n * 2

print(duplicar(duplicar(5)))
print(duplicar(3) + duplicar(4))"""))

cells.append(md("nb3-35-comp1-md", """\
### 🧩 Completa — tasa_infeccion

Completa el cuerpo de la función y luego el llamado con datos reales.

**Resultado esperado:** `Tasa de infección: 16.0%`"""))

cells.append(code("nb3-35-comp1", """\
def tasa_infeccion(infectados, poblacion):
    return ___ / ___   # ← completa la fórmula

# Llamado con datos reales de una zona:
infectados_zona = 800
poblacion_zona  = 5000
tasa = tasa_infeccion(___, ___)   # ← completa el llamado
print(f"Tasa de infección: {tasa:.1%}")"""))

cells.append(md("nb3-35-gamma-md", """\
---
### 🔬 Conecta — De `duracion` a `gamma`: activando el campo que tenías desde el Día 1

Los datos del notebook tienen un campo `duracion` que hasta ahora no usamos:

```python
duracion = [2, 999, 14, 21, 7, 14, 37]  # días de infección activa
```

En el modelo SIR, `gamma` es la **tasa de recuperación por día**. La relación es directa:

> **gamma = 1 / duracion**

Si un paciente de Ébola tarda 21 días en resolverse, cada día el `1/21 ≈ 4.8%` de infectados se recupera (o muere). Si el Cordyceps solo dura 2 días, el `1/2 = 50%` se resuelve por día.

Un `gamma` más alto **no significa menos mortal** — significa que el brote se resuelve más rápido, para bien o para mal. El Cordyceps no da tiempo a responder.

---
### 🧩 Completa — Función `dias_a_gamma`"""))

cells.append(code("nb3-35-gamma-fn", """\
def dias_a_gamma(duracion_infecciosa):
    \"\"\"Convierte días de infección activa a tasa de recuperación diaria (gamma).\"\"\"
    return ___ / ___   # ← gamma = 1 / duracion

# Verifica con los 7 patógenos:
print(f"{'Patógeno':<16} {'Duración':>9} {'Gamma':>8}  {'Interpreta'}")
print("─" * 65)
for i in range(len(nombres)):
    if duracion[i] < 999:   # excluye Walker (∞)
        g = dias_a_gamma(duracion[i])
        velocidad = "muy rápido" if g > 0.3 else ("rápido" if g > 0.1 else "lento")
        print(f"{nombres[i]:<16} {duracion[i]:>6} días  {g:>6.3f}   se resuelve {velocidad}")

# 🔮 PREDICE antes de ejecutar:
# ¿Quién tiene gamma más ALTO — Ébola (21 días) o Gripe 1918 (7 días)?
# ¿Un gamma más alto es mejor o peor para la ciudad? Escribe tu razonamiento:
# Mi respuesta: ___"""))

cells.append(md("nb3-35-gamma-sir-md", """\
> 💡 **Conexión SIR:** Ahora que puedes calcular `gamma` desde `duracion`, el Reto 2 tiene más sentido:
> `beta = r0 * gamma = r0 / duracion`. Cordyceps (R0=3.5, duracion=2) transmite rápido Y se resuelve rápido.
> Ébola (R0=1.8, duracion=21) se propaga despacio pero permanece en el sistema 10× más tiempo.
> La curva SIR los captura de forma diferente — y eso es exactamente lo que verás en el Reto 2."""))

cells.append(md("nb3-35-ej9-md", """\
---
### 🔨 Ejercicio 9 — clasificar_zona como función ⭐ (6 pts)

Escribe `def clasificar_zona(infectados, poblacion, cfr):` que devuelve el estado de la zona usando los mismos umbrales del ejercicio 7 de la sección 3.3:

- `"ZONA PERDIDA"` si tasa > 60% O cfr > 0.5
- `"ZONA ROJA"` si tasa > 20%
- `"ZONA AMARILLA"` si tasa > 5%
- `"ZONA VERDE"` si tasa ≤ 5%

Luego llámala para **5 zonas** con parámetros de COVID-19 y otra vez con Ébola. Imprime ambos sets de resultados.

✅ Al terminar ejecuta `grader.check_ex9()`"""))

cells.append(code("nb3-35-ej9", """\
### TU CODIGO AQUI — define clasificar_zona ###


# Datos de prueba
zonas_inf = [200, 1500, 80, 3500, 1000]
pob_zonas = [5000, 5000, 5000, 5000, 5000]

print("=== COVID-19 ===")
for i in range(5):
    estado = clasificar_zona(zonas_inf[i], pob_zonas[i], mortalidad[2])
    print(f"Zona {i+1}: {estado}")

print("\\n=== ÉBOLA ===")
for i in range(5):
    estado = clasificar_zona(zonas_inf[i], pob_zonas[i], mortalidad[3])
    print(f"Zona {i+1}: {estado}")"""))

cells.append(code("nb3-35-ej9-check", "grader.check_ex9()"))

cells.append(md("nb3-35-ej9-exp", """\
> 💬 **Explicación:** ¿Cuántas líneas de código ahorraste usando la función en vez de escribir los ifs dos veces?
> *(Doble-click para responder aquí)*"""))

cells.append(md("nb3-35-debug5-md", """\
---
### 🔧 Debug 5 — return faltante

La función calcula correctamente pero no devuelve nada. Todos los llamados producen `None`.

1. Ejecuta y observa el `None`
2. Añade el `return` faltante en el lugar correcto

**Resultado esperado:** `Infectados mañana: 250`"""))

cells.append(code("nb3-35-debug5", """\
def simular_dia(infectados, r0, capacidad):
    nuevos = int(infectados * r0)
    if nuevos > capacidad:
        nuevos = capacidad
    # ← ¿qué falta aquí?

resultado = simular_dia(100, 2.5, 5000)
print(f"Infectados mañana: {resultado}")   # imprime None en vez del número"""))

cells.append(code("nb3-35-debug5-check", "grader.check_debug5()"))

cells.append(md("nb3-35-ej10-md", """\
---
### 🔨 Ejercicio 10 — simular_dia y tabla comparativa ⭐⭐ (8 pts)

Escribe `def simular_dia(infectados, r0, capacidad):` que aplica R0 y limita al máximo de capacidad.

Llámala en un loop de 10 días para **cada patógeno** de los datos. Imprime una tabla:

| Patógeno | Día 1 | Día 5 | Día 10 |
|----------|-------|-------|--------|

Condiciones: `infectados_0 = 100`, `capacidad = 10_000`

La fila del Sarampión será la más dramática.

✅ Al terminar ejecuta `grader.check_ex10()`"""))

cells.append(code("nb3-35-ej10", """\
### TU CODIGO AQUI — define simular_dia ###


# Tabla comparativa
infectados_0 = 100
capacidad    = 10_000

print(f"{'Patógeno':<16} {'Día 1':>8} {'Día 5':>8} {'Día 10':>8}")
print("─" * 44)

for i in range(len(nombres)):
    ### TU CODIGO AQUI — llama simular_dia en loop ###
    pass"""))

cells.append(code("nb3-35-ej10-check", "grader.check_ex10()"))

cells.append(md("nb3-35-ej10-exp", """\
> 💬 **Explicación:** ¿Por qué el Walker virus (R0=1.2) parece menos peligroso en esta tabla pero sería el más catastrófico en la realidad? (Pista: revisa su `mortalidad`.)
> *(Doble-click para responder aquí)*"""))

cells.append(md("nb3-35-ej11-md", """\
---
### 🔨 Ejercicio 11 — Motor de Intervención ⭐⭐⭐ (10 pts)

Escribe **dos funciones** que trabajen juntas:

**Función 1:** `def r0_efectivo(r0_base, intervencion_activa, factor_reduccion):`
- Si la intervención está activa: devuelve `r0_base * factor_reduccion`
- Si no: devuelve `r0_base`

**Función 2:** `def simular_brote(infectados_0, poblacion, r0_base, dias, dia_intervencion, factor_reduccion):`
- Loop `dias` días
- Cada día llama a `r0_efectivo` con `intervencion_activa = (dia >= dia_intervencion)`
- Aplica el R0 resultante (limita a `poblacion`)
- Devuelve lista de infectados diarios

Llámala para COVID-19 y Gripe 1918. Imprime el día en que cada uno alcanza su pico.

✅ Al terminar ejecuta `grader.check_ex11()`"""))

cells.append(code("nb3-35-ej11", """\
### TU CODIGO AQUI — define r0_efectivo ###


### TU CODIGO AQUI — define simular_brote ###


# Prueba: COVID-19
resultado_covid = simular_brote(
    infectados_0=100, poblacion=100_000,
    r0_base=r0_valores[2], dias=30,
    dia_intervencion=10, factor_reduccion=0.4
)

# Prueba: Gripe 1918
resultado_gripe = simular_brote(
    infectados_0=100, poblacion=100_000,
    r0_base=r0_valores[4], dias=30,
    dia_intervencion=10, factor_reduccion=0.4
)

print(f"COVID-19  — pico: día {resultado_covid.index(max(resultado_covid))+1}, {max(resultado_covid)} infectados")
print(f"Gripe 1918 — pico: día {resultado_gripe.index(max(resultado_gripe))+1}, {max(resultado_gripe)} infectados")"""))

cells.append(code("nb3-35-ej11-check", "grader.check_ex11()"))

cells.append(md("nb3-35-ej11-exp", """\
> 💬 **Explicación:** `simular_brote` llama a `r0_efectivo` dentro de un loop. ¿Qué ventaja tiene esto sobre escribir el `if` directamente dentro del loop?
> *(Doble-click para responder aquí)*"""))

cells.append(md("nb3-35-t3-md", """\
---
**❓ Pregunta T3 — Función sin return**

¿Qué devuelve una función que **no tiene `return`**?

- **a)** `0`
- **b)** Un error (`TypeError`)
- **c)** `None`
- **d)** El último valor calculado"""))

cells.append(code("nb3-35-t3", 'respuesta_t3 = "?"   # 📝 escribe: a, b, c o d'))

cells.append(code("nb3-35-t3-check", "grader.check_t3()"))

cells.append(code("nb3-35-mini-e", "grader.check_mini_e()   # ✅ Checkpoint 3.5"))

# ════════════════════════════════════════════════════════════
# PARTE 2 — EJERCICIOS DE INTEGRACIÓN
# ════════════════════════════════════════════════════════════

cells.append(md("nb3-p2-header", """\
---
# Parte 2 — Ejercicios de Integración

Combinas **loops anidados + ifs anidados + funciones** para resolver problemas reales.

Cada ejercicio tiene 5 pasos:
1. **Problema** — qué debes resolver
2. **Planificación** — piensas ANTES de programar
3. **Ayuda opcional** — pista si llevas más de 5 minutos atascado/a
4. **Tu código** — escribes la solución desde cero
5. **Autograder + Explicación** — verificas y reflexionas"""))

# INTEX 1
cells.append(md("nb3-intex1-md", """\
---

> *"Este árbol de decisión es una versión simplificada del protocolo de triage que usó Médicos Sin Fronteras durante el brote de Ébola de 2014 en Guinea."*

---

### Ex. 1 — Perfil del Paciente Cero ⭐ (6 pts)

Dado un paciente con:
- `horas_expuesto` (int)
- `tiene_fiebre` (bool)
- `tiene_sintomas_neurologicos` (bool)
- `perdio_consciencia` (bool)

Clasifícalo en una progresión de 5 niveles (cada nivel depende del anterior):

| Clasificación | Condición |
|---------------|-----------|
| `"LIMPIO"` | horas ≤ 0 |
| `"SOSPECHOSO"` | horas > 0 |
| `"INFECTADO TEMPRANO"` | sospechoso + fiebre |
| `"INFECTADO AVANZADO"` | infectado temprano + síntomas neurológicos |
| `"CASO TERMINAL"` | infectado avanzado + pérdida de consciencia |

Prueba con al menos 4 pacientes que cubran niveles distintos."""))

cells.append(md("nb3-intex1-plan", """\
## 📋 Planificación — COMPLETA ANTES DE PROGRAMAR
*(Doble-click para editar)*

**Estructura de ifs anidados:**
1. ¿`horas_expuesto > 0`? → si no: ___
2. Si sí → ¿`tiene_fiebre`? → si no: ___
3. Si sí → ¿`tiene_sintomas_neurologicos`? → si no: ___
4. Si sí → ¿`perdio_consciencia`? → ___

**¿Por qué verificamos `perdio_consciencia` DESPUÉS de `tiene_sintomas_neurologicos`?** ___"""))

cells.append(code("nb3-intex1-hint", """\
# 💡 AYUDA OPCIONAL — Descomenta para ver la estructura

# pacientes = [
#     (0,  False, False, False),   # Paciente A
#     (12, False, False, False),   # Paciente B
#     (12, True,  False, False),   # Paciente C
#     (36, True,  True,  True),    # Paciente D
# ]

# for (horas, fiebre, neuro, consciencia) in pacientes:
#     if horas <= 0:
#         clasificacion = "LIMPIO"
#     else:
#         if not fiebre:
#             clasificacion = "SOSPECHOSO"
#         else:
#             if not neuro:
#                 clasificacion = ???
#             else:
#                 if not consciencia:
#                     clasificacion = ???
#                 else:
#                     clasificacion = ???
#     print(f"Paciente: {clasificacion}")"""))

cells.append(code("nb3-intex1-code", """\
### TU CODIGO AQUI ###
"""))

cells.append(code("nb3-intex1-check", "grader.check_intex1()"))

cells.append(md("nb3-intex1-exp", """\
> 💬 **Explicación:** ¿Por qué `perdio_consciencia` se verifica DESPUÉS de `tiene_sintomas_neurologicos`? ¿Qué implicación clínica tiene ese orden?
> *(Doble-click para responder aquí)*"""))

# INTEX 2
cells.append(md("nb3-intex2-md", """\
---

> *"Los modelos de propagación urbana del Imperial College London usaron grids similares para predecir la expansión del COVID-19 en Londres en febrero 2020."*

---

### Ex. 2 — Mapa de Propagación Urbana ⭐⭐ (8 pts)

Imprime una cuadrícula 8×8 con reglas de clasificación usando ifs anidados:

| Símbolo | Condición | Significado |
|---------|-----------|-------------|
| `[QZ]` | esquinas (fila y col son 0 o 7) | Zona de Cuarentena — checkpoints FEDRA |
| `[P0]` | `fila + col <= 2` | Origen Paciente Zero |
| `[--]` | `abs(fila-4) + abs(col-4) <= 2` | Zona segura — centro limpio |
| `[IN]` | `fila % 3 == 0 and col % 3 == 0` | Nodo de infección |
| `[  ]` | todo lo demás | Calle normal |

**Importante:** las reglas tienen prioridad — verifica en el orden de la tabla. Si una zona cumple múltiples condiciones, aplica la primera.

Al final imprime el conteo de cada tipo de zona."""))

cells.append(md("nb3-intex2-plan", """\
## 📋 Planificación — COMPLETA ANTES DE PROGRAMAR
*(Doble-click para editar)*

**Variables para conteo (fuera del loop):**
- `cont_qz = ___`, `cont_p0 = ___`, `cont_segura = ___`, `cont_nodo = ___`, `cont_calle = ___`

**Dentro del loop (orden de prioridad):**
1. ¿Es esquina? (define la condición de esquina exacta)
2. ¿Es origen P0?
3. ¿Es zona segura?
4. ¿Es nodo de infección?
5. Si ninguna: calle normal

**Verificación:** ¿cuántas esquinas tiene una cuadrícula 8×8? ___"""))

cells.append(code("nb3-intex2-hint", """\
# 💡 AYUDA OPCIONAL — Descomenta para ver la estructura

# cont_qz = cont_p0 = cont_segura = cont_nodo = cont_calle = 0

# for fila in range(8):
#     for col in range(8):
#         es_esquina = (fila in [0, 7]) and (col in [0, 7])
#         if es_esquina:
#             simbolo = "[QZ]"
#             cont_qz += 1
#         elif fila + col <= 2:
#             simbolo = "[P0]"
#             cont_p0 += 1
#         elif ???:
#             simbolo = "[--]"
#             ...
#         elif ???:
#             simbolo = "[IN]"
#             ...
#         else:
#             simbolo = "[  ]"
#             cont_calle += 1
#         print(simbolo, end=" ")
#     print()

# print(f"QZ:{cont_qz}  P0:{cont_p0}  Segura:{cont_segura}  Nodos:{cont_nodo}  Calle:{cont_calle}")"""))

cells.append(code("nb3-intex2-code", """\
### TU CODIGO AQUI ###
"""))

cells.append(code("nb3-intex2-check", "grader.check_intex2()"))

cells.append(md("nb3-intex2-exp", """\
> 💬 **Explicación:** ¿Cuántos nodos de infección hay en el mapa? Si cada nodo contagia a sus 4 vecinos inmediatos, ¿cuántas zonas estarían infectadas en el Día 2?
> *(Doble-click para responder aquí)*"""))

# INTEX 3
cells.append(md("nb3-intex3-md", """\
---

> *"Esta tabla es análoga a los reportes de situación que publica la OMS durante brotes activos."*

---

### Ex. 3 — Comparador de Pandemias ⭐⭐ (8 pts)

Simula los 7 patógenos del notebook durante 14 días cada uno.

**Condiciones:** `infectados_0 = 50`, `poblacion = 50_000`

Para cada patógeno, registra:
- Día en que se alcanza el pico de infectados
- Infectados en el pico
- Si la ciudad "cayó" (>60% infectados)
- Muertes estimadas en el pico (`infectados_pico × mortalidad[i]`)

Imprime una tabla comparativa al final.

✅ Al terminar ejecuta `grader.check_intex3()`"""))

cells.append(md("nb3-intex3-plan", """\
## 📋 Planificación — COMPLETA ANTES DE PROGRAMAR
*(Doble-click para editar)*

**Loop exterior:** `for i in range(len(nombres)):` — itera los 7 patógenos

**Loop interior:** `for dia in range(14):` — simula 14 días

**Variables a rastrear por patógeno (resetear antes del loop interior):**
- `infectados = infectados_0`
- `pico_dia = ___`, `pico_inf = ___`

**Actualización por día:**
- `infectados = min(int(infectados * r0_valores[i]), poblacion)`
- Si `infectados > pico_inf`: actualiza pico

**Tabla final:** nombres, día_pico, infectados_pico, ciudad_caida (Sí/No), muertes_estimadas"""))

cells.append(code("nb3-intex3-hint", """\
# 💡 AYUDA OPCIONAL — Descomenta para ver la estructura

# infectados_0 = 50
# poblacion    = 50_000

# print(f"{'Patógeno':<16} {'Pico día':>9} {'Pico inf':>10} {'Cayó?':>7} {'Muertes':>9}")
# print("─" * 55)

# for i in range(len(nombres)):
#     infectados = infectados_0
#     pico_dia   = 0
#     pico_inf   = infectados_0

#     for dia in range(1, 15):
#         infectados = min(int(infectados * r0_valores[i]), poblacion)
#         if infectados > pico_inf:
#             pico_inf = infectados
#             pico_dia = dia

#     cayo    = "Sí" if pico_inf > poblacion * 0.6 else "No"
#     muertes = int(pico_inf * mortalidad[i])
#     print(f"{nombres[i]:<16} {pico_dia:>9} {pico_inf:>10} {cayo:>7} {muertes:>9}")"""))

cells.append(code("nb3-intex3-code", """\
### TU CODIGO AQUI ###
"""))

cells.append(code("nb3-intex3-check", "grader.check_intex3()"))

cells.append(md("nb3-intex3-exp", """\
> 💬 **Explicación:** ¿Qué patógeno es más peligroso — el que tiene mayor R0 o el que tiene mayor mortalidad? ¿De qué factores depende?
> *(Doble-click para responder aquí)*"""))

cells.append(md("nb3-intex3-viz-md", """\
---
### 🌍 Visualiza — Los 7 patógenos en una sola gráfica

La tabla que imprimiste muestra los números. La gráfica muestra por qué el sarampión asustó a cada epidemiólogo que la vio.

*Ejecuta para ver todas las curvas superpuestas — interactivas.*"""))

cells.append(code("nb3-intex3-viz", """\
# 📊 Los 7 patógenos — comparación interactiva
_inf0 = 50
_pob  = 50_000
_series = {}
for i in range(len(nombres)):
    inf = _inf0
    serie = []
    for _ in range(14):
        inf = min(int(inf * r0_valores[i]), _pob)
        serie.append(inf)
    _series[nombres[i]] = serie

viz.comparar_patogenos(_series, titulo="Los 7 Patógenos — 14 días desde 50 infectados iniciales")"""))

cells.append(md("nb3-intex3-viz-interp", """\
---

**[ LECTURA ]** Siete patógenos, mismo punto de partida: 50 infectados, 14 días. El Sarampión (R₀=15) domina en velocidad. Ébola (R₀=1.8) apenas se mueve en escala. La Peste Bubónica sigue entre ellos.

**[ CONCLUSIÓN ]** Transmisibilidad y mortalidad son dimensiones independientes. Sarampión mata menos del 0.1% pero infecta a casi todos. Ébola mata al 65% pero no se propaga tan rápido. Las dos variables juntas determinan el impacto real.

**[ MISIÓN ]** Modifica el código para simular solo los patógenos con R₀ > 2. ¿Cuántos quedan? ¿Cuál lidera en el Día 14? ¿Cambia el ranking si filtras por mortalidad en vez de R₀?"""))

# INTEX 4
cells.append(md("nb3-intex4-md", """\
---

> *"El modelo de Ferguson et al. (Imperial College, 2020) que convenció a Boris Johnson de implementar el lockdown en UK usó exactamente esta lógica: intervención tardía vs temprana en múltiples zonas simultáneas."*

---

### Ex. 4 — Protocolo de Cuarentena ⭐⭐⭐ (10 pts)

Simula 30 días en **6 zonas** con parámetros de COVID-19.

```python
zonas_inf   = [50, 20, 100, 10, 200, 30]
poblaciones = [5000, 3000, 10000, 2000, 8000, 4000]
```

**Lógica anidada (sin funciones):**
- Si `dia >= dia_cuarentena`: R0 efectivo = `r0_valores[2] × 0.4`
- Si zona tiene tasa > 40% Y sin suministros (`dia > 20`): R0 adicional × 0.2
- Si tasa > 60%: zona cae, no se actualiza más

**Registra por día:** infectados totales ciudad, zonas caídas, muertes estimadas (`mortalidad[2]`)

**Corre dos veces:**
1. `dia_cuarentena = 7`
2. `dia_cuarentena = 20`

✅ Al terminar ejecuta `grader.check_intex4()`"""))

cells.append(md("nb3-intex4-plan", """\
## 📋 Planificación — COMPLETA ANTES DE PROGRAMAR
*(Doble-click para editar)*

**Variables fuera del loop exterior:**
- `zonas_caidas = [False] * 6`
- `zonas_inf_1 = zonas_inf[:]` (copia para el primer run)

**Estructura del loop:**
```
for dia in range(1, 31):
    total_ciudad = 0
    for z in range(6):
        if zonas_caidas[z]:
            [skip]
        else:
            r0_hoy = ???  # depende de dia >= dia_cuarentena
            if dia > 20 and tasa > 0.4:
                r0_hoy = ???  # reducción adicional
            infectados[z] = min(int(infectados[z] * r0_hoy), poblaciones[z])
            if tasa > 0.6:
                zonas_caidas[z] = True
            total_ciudad += infectados[z]
    muertes = int(total_ciudad * mortalidad[2])
```"""))

cells.append(code("nb3-intex4-hint", """\
# 💡 AYUDA OPCIONAL — Descomenta para ver el esqueleto

# def correr_simulacion(zonas_iniciales, poblaciones, dia_cuarentena):
#     zonas_inf    = zonas_iniciales[:]
#     zonas_caidas = [False] * len(zonas_inf)
#     r0_base      = r0_valores[2]

#     for dia in range(1, 31):
#         total_ciudad = 0
#         caidas_hoy   = 0
#         for z in range(len(zonas_inf)):
#             if zonas_caidas[z]:
#                 caidas_hoy += 1
#                 continue
#             tasa = zonas_inf[z] / poblaciones[z]
#             if dia >= dia_cuarentena:
#                 r0_hoy = r0_base * 0.4
#             else:
#                 r0_hoy = r0_base
#             if dia > 20 and tasa > 0.4:
#                 r0_hoy *= 0.2
#             zonas_inf[z] = min(int(zonas_inf[z] * r0_hoy), poblaciones[z])
#             tasa = zonas_inf[z] / poblaciones[z]
#             if tasa > 0.6:
#                 zonas_caidas[z] = True
#             total_ciudad += zonas_inf[z]
#         muertes = int(total_ciudad * mortalidad[2])
#         if dia % 5 == 0:
#             print(f"Día {dia:>2}: Ciudad={total_ciudad:>6}  Caídas={caidas_hoy}  Muertes≈{muertes}")

# print("=== Cuarentena Día 7 ===")
# correr_simulacion([50, 20, 100, 10, 200, 30], [5000, 3000, 10000, 2000, 8000, 4000], 7)
# print("\\n=== Cuarentena Día 20 ===")
# correr_simulacion([50, 20, 100, 10, 200, 30], [5000, 3000, 10000, 2000, 8000, 4000], 20)"""))

cells.append(code("nb3-intex4-code", """\
zonas_inf_base = [50, 20, 100, 10, 200, 30]
poblaciones    = [5000, 3000, 10000, 2000, 8000, 4000]

### TU CODIGO AQUI ###
# Corre con dia_cuarentena = 7, luego con dia_cuarentena = 20
"""))

cells.append(code("nb3-intex4-check", "grader.check_intex4()"))

cells.append(md("nb3-intex4-exp", """\
> 💬 **Explicación:** ¿Cuál es el costo en vidas estimadas de retrasar la cuarentena de día 7 a día 20? ¿Hay un punto de no retorno?
> *(Doble-click para responder aquí)*"""))

cells.append(md("nb3-intex4-viz-md", """\
---
### 🌍 Visualiza — El mismo brote en dos ciudades del mundo

**Wuhan** tuvo cuarentena en el Día 7. **Cusco** tuvo capacidad hospitalaria casi nula durante todo el brote.
Los mapas animados de abajo muestran las mismas matemáticas que calculaste — en los lugares donde ocurrió.

*Presiona ▶ Reproducir para ver la expansión día a día.*"""))

cells.append(code("nb3-intex4-viz-wuhan", """\
# 🗺 Mapa animado — Wuhan (cuarentena temprana: Día 7)
_zi   = [50, 20, 100, 10, 200, 30]
_pobs = [5000, 3000, 10000, 2000, 8000, 4000]
_r0b  = r0_valores[2]

def _animar_sim(dia_q):
    inf = _zi[:]
    caidas = [False] * 6
    frames = []
    for dia in range(1, 31):
        r0_hoy = _r0b * 0.4 if dia >= dia_q else _r0b
        for z in range(6):
            if not caidas[z]:
                tasa = inf[z] / _pobs[z]
                if tasa > 0.6:
                    caidas[z] = True
                else:
                    inf[z] = min(int(inf[z] * r0_hoy), _pobs[z])
        frames.append(inf[:])
    return frames

mapa.animacion_brote("wuhan", _animar_sim(7), _pobs, patogeno="COVID-19 — Cuarentena Día 7")"""))

cells.append(md("nb3-intex4-viz-sep", """\
---
### 🗺 Mapa 2 — Cusco: respuesta tardía (Día 20)

El mismo modelo, la misma ciudad inicial — pero la cuarentena llegó 13 días después.
Observa cuántas zonas llegan a estado **PERDIDA** en comparación con Wuhan.

*Presiona ▶ Reproducir para comparar la expansión día a día.*"""))

cells.append(code("nb3-intex4-viz-cusco", """\
# 🗺 Mapa animado — Cusco (cuarentena tardía: Día 20)
mapa.animacion_brote("cusco", _animar_sim(20), _pobs, patogeno="COVID-19 — Cuarentena Día 20")"""))

cells.append(md("nb3-intex4-viz-interp", """\
---

**[ LECTURA ]** Mismo virus, misma simulación matemática — dos ciudades, dos decisiones de política. Los círculos rojos grandes en Cusco aparecen más rápido y en más zonas que en Wuhan.

**[ CONCLUSIÓN ]** Los números del modelo son idénticos. Lo que cambia es el momento de la intervención. 13 días de diferencia separan una ciudad contenida de una en estado PERDIDA.

**[ MISIÓN ]** Observa qué zonas de Cusco llegan a PERDIDA primero. ¿Son las más pobladas, las más cercanas al centro, o las que empezaron con más infectados? Discute cómo cambiaría el patrón si el Paciente Cero estuviera en una zona periférica."""))

# INTEX 5 — CAPSTONE
cells.append(md("nb3-intex5-md", """\
---
### Ex. 5 — Motor de Simulación Epidemiológica (capstone) ⭐⭐⭐ (12 pts)

Construye un motor de simulación reutilizable. Escribe **cuatro funciones**:

**`def aplicar_r0(infectados, r0, capacidad):`**
- Aplica R0 a los infectados de hoy, limita a capacidad
- Devuelve nuevos infectados (int)

**`def r0_efectivo(r0_base, dia, dia_intervencion, tasa_actual):`**
- Si `dia >= dia_intervencion` O `tasa_actual > 0.3`: devuelve `r0_base * 0.4`
- Si no: devuelve `r0_base`

**`def clasificar_zona(infectados, poblacion, cfr):`**
- Mismos umbrales del Ex. 9

**`def simular_ciudad(zonas_iniciales, poblaciones, r0_base, cfr, dia_intervencion, dias):`**
- Loop exterior: días. Loop interior: zonas.
- Llama a `r0_efectivo` y `aplicar_r0` en cada celda
- Si tasa > 0.6: zona cae
- Devuelve `(total_por_dia, zonas_caidas_por_dia)` — dos listas paralelas

**Luego llama `simular_ciudad` para:**
1. Cordyceps (`r0=3.5`, `cfr=0.85`, `dia_intervencion=7`)
2. COVID-19 (`r0=2.5`, `cfr=0.02`, `dia_intervencion=10`)
3. Ébola — usa `siguiente_paso_sir` para este run (ver nota abajo)

Imprime un reporte final comparativo: qué patógeno colapsó la ciudad más rápido, muertes estimadas por escenario.

> **Nota sobre el Walker:** su R0=1.2 parece bajo, pero `mortalidad=1.0`. En el modelo SIR, los "recuperados" deberían convertirse en nuevos infectados. El modelo no captura esto — esa brecha entre modelo y realidad es la lección.

✅ Al terminar ejecuta `grader.check_intex5()`"""))

cells.append(md("nb3-intex5-plan", """\
## 📋 Planificación — COMPLETA ANTES DE PROGRAMAR
*(Doble-click para editar)*

**Orden de construcción:**
1. Escribe `aplicar_r0` → pruébala sola con valores conocidos
2. Escribe `r0_efectivo` → pruébala con día antes y después de la intervención
3. Escribe `clasificar_zona` → pruébala con 3 casos límite
4. Escribe `simular_ciudad` → la que llama a las otras tres
5. Corre los 3 patógenos

**Pregunta clave:** ¿por qué `simular_ciudad` llama a las otras funciones en vez de tener toda la lógica adentro? ___"""))

cells.append(code("nb3-intex5-hint", """\
# 💡 AYUDA OPCIONAL — Estructura de simular_ciudad

# def simular_ciudad(zonas_iniciales, poblaciones, r0_base, cfr, dia_intervencion, dias):
#     zonas_inf    = zonas_iniciales[:]
#     zonas_caidas = [False] * len(zonas_inf)
#     total_por_dia       = []
#     caidas_por_dia      = []

#     for dia in range(1, dias + 1):
#         total = 0
#         caidas = 0
#         for z in range(len(zonas_inf)):
#             if zonas_caidas[z]:
#                 caidas += 1
#                 continue
#             tasa  = zonas_inf[z] / poblaciones[z]
#             r0_hoy = r0_efectivo(r0_base, dia, dia_intervencion, tasa)
#             zonas_inf[z] = aplicar_r0(zonas_inf[z], r0_hoy, poblaciones[z])
#             tasa = zonas_inf[z] / poblaciones[z]
#             if tasa > 0.6:
#                 zonas_caidas[z] = True
#             total += zonas_inf[z]
#         total_por_dia.append(total)
#         caidas_por_dia.append(caidas)

#     return total_por_dia, caidas_por_dia"""))

cells.append(code("nb3-intex5-code", """\
### TU CODIGO AQUI — define las 4 funciones ###


# Configuración compartida
zonas_iniciales = [100, 50, 200, 30, 500]
poblaciones     = [5000, 3000, 8000, 2000, 10000]
dias            = 30

# Corrida 1: Cordyceps
total_cordyceps, caidas_cordyceps = simular_ciudad(
    zonas_iniciales, poblaciones,
    r0_base=r0_valores[0], cfr=mortalidad[0],
    dia_intervencion=7, dias=dias
)

# Corrida 2: COVID-19
total_covid, caidas_covid = simular_ciudad(
    zonas_iniciales, poblaciones,
    r0_base=r0_valores[2], cfr=mortalidad[2],
    dia_intervencion=10, dias=dias
)

# Reporte comparativo
print("=== REPORTE COMPARATIVO ===")
print(f"Cordyceps — pico: {max(total_cordyceps):>6}  muertes≈{int(max(total_cordyceps)*mortalidad[0]):>5}")
print(f"COVID-19  — pico: {max(total_covid):>6}  muertes≈{int(max(total_covid)*mortalidad[2]):>5}")"""))

cells.append(code("nb3-intex5-check", "grader.check_intex5()"))

cells.append(md("nb3-intex5-exp", """\
> 💬 **Explicación:** ¿Por qué `simular_ciudad` llama a las otras funciones en vez de tener toda la lógica directamente? Si quisieras cambiar la fórmula de `r0_efectivo`, ¿cuántos lugares tendrías que editar?
> *(Doble-click para responder aquí)*"""))

cells.append(md("nb3-intex5-walker-md", """\
---
### 🔬 Análisis — Los Límites del Modelo: El Walker No Encaja

El Walker virus tiene `R0 = 1.2` y `mortalidad = 1.0`. Cuando ejecutas `simular_ciudad` con esos parámetros, parece menos peligroso que el Cordyceps. Pero algo está fundamentalmente roto.

**El problema:** el modelo SIR asume que Recuperados = Inmunes → salen del sistema. El Walker no sigue esa regla: los muertos **regresan como infectados**. El compartimiento R acumula personas que deberían volver a I.

Completa la función `paso_walker` que captura esta dinámica. No usa `gamma` — los "recuperados" son reanimados:

```python
# Modelo SIR estándar:   S → I → R (R es final)
# Modelo Walker:         S → I → Muerto → I (ciclo sin salida)
```

*"El SIR predice extinción del Walker en semanas. La realidad de la ficción muestra el mundo colapsado en días. Esa brecha entre modelo y realidad es exactamente lo que un epidemiólogo real debe detectar."*"""))

cells.append(code("nb3-intex5-walker", """\
def paso_walker(S, I, R_muertos, N, beta):
    \"\"\"
    Modelo SIR modificado para el Walker:
    - Los 'recuperados' son reanimados que vuelven al pool de infectados
    - No existe inmunidad — nadie sale del ciclo S → I → Reanimado → I
    S         = susceptibles (sanos)
    I         = infectados activos (incluyendo reanimados)
    R_muertos = acumulado de muertes (referencia histórica, ya reanimados)
    \"\"\"
    nuevos_infectados = beta * S * I / N        # contagios normales
    nuevos_reanimados = mortalidad[1] * I       # el 100% de infectados reanima
    # Los reanimados regresan a I — no a R
    S_nuevo        = S - ___                    # ← susceptibles que se infectan
    I_nuevo        = I + ___ + ___              # ← nuevos infectados + reanimados
    R_muertos_nuevo = R_muertos + nuevos_reanimados
    return S_nuevo, I_nuevo, R_muertos_nuevo

# Prueba: 100 infectados iniciales, ciudad de 10,000
N_w   = 10_000
I_w   = 100
S_w   = N_w - I_w
R_w   = 0
beta_w = r0_a_beta(r0_valores[1], gamma=1/2)   # Walker gamma ≈ Cordyceps

print("WALKER VIRUS — Modelo SIR modificado")
print(f"{'Día':<5} {'S':>8} {'I':>8} {'Muertos':>10}")
print("─" * 35)
for dia in range(1, 16):
    S_w, I_w, R_w = paso_walker(S_w, I_w, R_w, N_w, beta_w)
    print(f"{dia:<5} {int(S_w):>8} {int(I_w):>8} {int(R_w):>10}")
    if I_w >= N_w:
        print("  ⚠ POBLACIÓN COLAPSADA — todos infectados o reanimados")
        break

print("\\n¿Qué le pasa a S con el tiempo? ¿Por qué I no converge a 0?")
print("Escribe tu respuesta aquí:")
# Mi análisis: ___"""))

cells.append(md("nb3-intex5-walker-reflexion", """\
> 💬 **Reflexión:** Ejecuta `simular_ciudad` con los parámetros del Walker (`r0=1.2, cfr=1.0`).
> Luego ejecuta `paso_walker`. ¿Por qué dan resultados radicalmente distintos?
> La respuesta explica por qué los modelos matemáticos tienen **supuestos** que los hacen válidos
> para algunos patógenos y completamente erróneos para otros.
> *(Doble-click para responder aquí)*"""))

cells.append(md("nb3-intex5-viz-md", """\
---
### 🌍 Visualiza — Motor de simulación completo

Tu `simular_ciudad()` acaba de producir los mismos outputs que usan los modelos del Imperial College y la OMS.
La gráfica compara los dos escenarios que corriste. El dashboard es lo que ve un epidemiólogo en una sala de emergencias real.

*Ejecuta para ver los resultados de tu motor de simulación.*"""))

cells.append(code("nb3-intex5-viz", """\
# 📊 Resultados del motor de simulación
viz.comparar_patogenos(
    {"Cordyceps (R₀=3.5, CFR=85%)": total_cordyceps,
     "COVID-19  (R₀=2.5, CFR=2%)":  total_covid},
    titulo="Motor de Simulación — 30 días, 5 zonas"
)

# 🏥 Dashboard de situación — COVID-19
_pobs5 = [5000, 3000, 8000, 2000, 10000]
_zonas_dash = [{"nombre": f"Zona {i+1}", "infectados": int(total_covid[-1] * _pobs5[i] / sum(_pobs5)),
                "poblacion": _pobs5[i]} for i in range(5)]
dash.situacion(
    patogeno         = "COVID-19",
    dia              = dias,
    zonas_data       = _zonas_dash,
    r0               = r0_valores[2],
    cfr              = mortalidad[2],
    total_infectados = int(max(total_covid)),
    total_muertos    = int(max(total_covid) * mortalidad[2]),
    ciudad           = "Lima (simulación)",
    autor            = "Escribe tu nombre aquí"
)"""))

# ════════════════════════════════════════════════════════════
# BONUS
# ════════════════════════════════════════════════════════════

cells.append(md("nb3-memo-md", """\
---
### 📋 Memo de Política — Del Código a la Decisión Real

Tu motor de simulación acaba de producir los mismos outputs que usan los modelos del Imperial College y la OMS.

**Tu rol:** Eres el Director de Salud del Perú. Es el **Día 1** de un nuevo brote desconocido con R0 estimado entre 2.0 y 3.5. Los datos iniciales son escasos. Tu simulación es la mejor información disponible.

Escribe **3 recomendaciones de política** basadas en tus resultados. Cada una debe:
- Ser específica (no "actuar rápido" — ¿qué acción, en qué día?)
- Citar un resultado concreto de tu simulación como justificación
- Reconocer la incertidumbre del modelo (¿qué no sabe el modelo?)

*(No hay respuesta única correcta — la calidad del razonamiento es lo que cuenta.)*"""))

cells.append(code("nb3-memo", """\
# === MEMO DE POLÍTICA — DIRECTOR DE SALUD, PERÚ ===
# Basado en simulación: [escribe el patógeno y parámetros que usaste]
# Fecha: Día 1 del brote

recomendacion_1 = \"\"\"
ACCIÓN: ___
JUSTIFICACIÓN (resultado de mi simulación): ___
INCERTIDUMBRE DEL MODELO: ___
\"\"\"

recomendacion_2 = \"\"\"
ACCIÓN: ___
JUSTIFICACIÓN: ___
INCERTIDUMBRE: ___
\"\"\"

recomendacion_3 = \"\"\"
ACCIÓN: ___
JUSTIFICACIÓN: ___
INCERTIDUMBRE: ___
\"\"\"

print("=== MEMO DE POLÍTICA — MINISTERIO DE SALUD, PERÚ ===")
print(recomendacion_1)
print(recomendacion_2)
print(recomendacion_3)"""))

cells.append(md("nb3-bonus-header", """\
---
# 🌟 Bonus — Desafíos Opcionales

No son obligatorios. Para quien quiere ir más lejos."""))

cells.append(md("nb3-reto1-md", """\
---

> *"R0 = 1.0 es el umbral más importante en epidemiología. Todo lo que hace una vacuna, una mascarilla, o un confinamiento es intentar cruzar ese umbral hacia abajo. La diferencia entre R0 = 1.1 y R0 = 0.9 es la diferencia entre una pandemia y una extinción del patógeno."*

---

## Reto 1 — El Número que Cambió la Historia

Escribe `def dias_hasta_colapso(poblacion, infectados_0, r0):` que:
- Repite el loop hasta que `infectados > poblacion * 0.6` (ciudad colapsada)
- Devuelve el número de días hasta el colapso
- Si no colapsa en 365 días: devuelve `-1`

Llámala para los 7 patógenos usando sus R0 reales. Imprime los resultados ordenados de más rápido a más lento.

Luego llámala con `R0 = 0.99` para todos — observa que ninguno colapsa jamás."""))

cells.append(code("nb3-reto1-code", """\
### TU CODIGO AQUI — define dias_hasta_colapso ###


# Resultados con R0 reales:
print("=== Días hasta colapso (R0 reales) ===")
resultados = []
for i in range(len(nombres)):
    dias = dias_hasta_colapso(100_000, 100, r0_valores[i])
    resultados.append((dias if dias != -1 else 366, nombres[i], r0_valores[i], dias))

resultados.sort()
for _, nombre, r0, dias in resultados:
    label = f"{dias} días" if dias != -1 else "nunca colapsa"
    print(f"{nombre:<16} (R0={r0}) → {label}")

# Con R0 = 0.99:
print("\\n=== Con R0 = 0.99 (por debajo del umbral) ===")
for nombre in nombres:
    dias = dias_hasta_colapso(100_000, 100, 0.99)
    print(f"{nombre}: {dias}")"""))

cells.append(code("nb3-reto1-check", "grader.check_reto1()   # opcional"))

cells.append(md("nb3-reto2-md", """\
---

> *"El modelo SIR fue desarrollado por Kermack y McKendrick en 1927. Es el fundamento matemático de toda la epidemiología moderna. Durante COVID-19, cada gobierno del mundo corrió una versión de este modelo para decidir sus políticas. Tú acabas de correrlo también."*

---

## Reto 2 — Modelo SIR Completo

Usa las funciones proporcionadas `siguiente_paso_sir` y `r0_a_beta`.

**Simula 60 días** para Cordyceps (R0=3.5, γ=1/2) y COVID-19 (R0=2.5, γ=1/14) en una ciudad de 100,000 con 10 infectados iniciales.

Luego simula COVID-19 de nuevo con **R0 = 0.9** (efecto de vacuna masiva).

Para cada corrida, imprime el día en que I (infectados) alcanza su pico."""))

cells.append(code("nb3-reto2-code", """\
N = 100_000
I0 = 10

def correr_sir(r0, gamma, dias, nombre):
    beta = r0_a_beta(r0, gamma)
    S, I, R = N - I0, I0, 0
    pico_I, pico_dia = I0, 0
    for dia in range(1, dias + 1):
        S, I, R = siguiente_paso_sir(S, I, R, N, beta, gamma)
        if I > pico_I:
            pico_I  = I
            pico_dia = dia
    print(f"{nombre:<20} pico: día {pico_dia:>3}, I={int(pico_I):>7} infectados")

### TU CODIGO AQUI — llama correr_sir para los 3 escenarios ###
"""))

cells.append(code("nb3-reto2-check", "grader.check_reto2()   # opcional"))

cells.append(md("nb3-reto2-viz-md", """\
---
### 📈 Visualiza — La curva SIR de Kermack y McKendrick (1927)

Esta es la curva que publicaron en 1927 y que 93 años después Boris Johnson vio proyectada en Downing Street antes de ordenar el lockdown del Reino Unido.
Tú acaba de correr el mismo modelo. Tú acabas de ver los mismos números.

*Ejecuta para ver la curva SIR interactiva de tu simulación.*"""))

cells.append(code("nb3-reto2-viz", """\
# 📈 Curva SIR interactiva — COVID-19 en una ciudad de 100,000
_gamma = 1/14   # COVID-19: 14 días promedio de infección
_beta  = r0_a_beta(r0_valores[2], _gamma)
_S, _I, _R = float(N - I0), float(I0), 0.0
_Sh, _Ih, _Rh = [], [], []
for _ in range(200):
    _S, _I, _R = siguiente_paso_sir(_S, _I, _R, N, _beta, _gamma)
    _Sh.append(_S); _Ih.append(_I); _Rh.append(_R)

viz.curva_sir(_Sh, _Ih, _Rh, f"COVID-19 (R₀={r0_valores[2]}, γ=1/14)", N=N, r0=r0_valores[2])"""))

cells.append(md("nb3-reto2-viz-interp", """\
---

**[ LECTURA ]** Tres compartimentos en el tiempo: Susceptibles (gris, bajando), Infectados activos (ámbar, pico y caída), Recuperados/Inmunes (verde, subiendo). La línea punteada bioluminiscente es el umbral de inmunidad de rebaño al 60%.

**[ CONCLUSIÓN ]** El momento en que la línea verde cruza el 60% es exactamente cuando la epidemia empieza a colapsar. Eso es 1 − 1/R₀ = 1 − 1/2.5 = 0.60. La fórmula te dice cuánta población debe ser inmune (por infección o vacuna) para que cada infectado contagie a menos de 1 persona.

**[ MISIÓN ]** Cambia `r0 = r0_valores[2]` (COVID, 2.5) a `r0 = r0_valores[5]` (Sarampión, 15.0). ¿A cuánto sube el umbral de rebaño? Verifica: ¿coincide con 1 − 1/15? ¿Qué porcentaje de cobertura vacunal necesitaría Perú para estar protegido?"""))

cells.append(md("nb3-r0-slider-md", """\
---
### 🎛️ Explora — Slider interactivo de R₀

> *“Marcos Castañeda, biólogo de campo, Firefly. Campo, día 31. No entendía por qué el Cordyceps EL-1 mataba ciudades enteras mientras el EL-4 se extinguió solo. Entonces vi el R₀. Si está por debajo de 1, el virus muere solo. Por encima de 1, necesita ayuda para morir.”*

Arrastra el slider para cambiar el R₀ entre 0.5 y 5.0.
Observa cómo cambian:
- La **curva de infectados** (ámbar) — ¿más alta? ¿más temprana?
- El **umbral de inmunidad de rebaño** (línea punteada) — ¿cuánta vacunación se necesita?
- El **ritmo de caída** de susceptibles (gris)

*Punto de quiebre clave: ¿qué pasa cuando R₀ cruza exactamente 1.0?*"""))

cells.append(code("nb3-r0-slider", """\
# 🎛️ Slider interactivo R₀ → curva SIR
# Arrastra el control deslizante para cambiar R₀ y ver la epidemia evolucionar
viz.curva_r0_interactiva(N=10_000, dias=180)"""))

# ════════════════════════════════════════════════════════════
# LABORATORIO DE ANÁLISIS — ejercicios combinados
# ════════════════════════════════════════════════════════════

cells.append(md("nb3-lab-header", """\
---
## 🔬 Laboratorio de Análisis — Ejercicios Combinados

> *"El modelo SIR no es una predicción. Es una linterna. Tú decides hacia dónde apuntarla."*
> — *Diario de campo, Firefly Research Node 7*

Los siguientes ejercicios combinan **dos o más funciones** que ya escribiste. No hay respuesta única — el objetivo es explorar cómo interactúan los parámetros del modelo."""))

# LAB 1
cells.append(md("nb3-lab1-md", """\
### 🏁 Lab 1 — Carrera de Patógenos: ¿Cuál llega primero al 10%?

Usa `r0_a_beta` + `siguiente_paso_sir` + `tasa_infeccion` para correr dos epidemias en paralelo
y encontrar qué día cada una supera el 10% de la población infectada.

**Funciones que necesitas combinar:**
- `r0_a_beta(r0, gamma)` → convierte R₀ en beta
- `siguiente_paso_sir(S, I, R, N, beta, gamma)` → avanza un día
- `tasa_infeccion(infectados, poblacion)` → porcentaje de infectados

Completa la función `carrera_patogenos` y úsala para comparar **COVID-19 vs. Sarampión**."""))

cells.append(code("nb3-lab1-code", """\
def carrera_patogenos(r0_a, r0_b, nombre_a, nombre_b, N=10_000, gamma=1/14, umbral=10.0):
    \"\"\"
    Simula dos patógenos desde el mismo punto de partida.
    Devuelve el día en que cada uno supera el umbral% de la población.
    \"\"\"
    # 1. Calcula beta para cada patógeno usando r0_a_beta
    beta_a = r0_a_beta(r0_a, gamma)
    beta_b = r0_a_beta(r0_b, gamma)

    # 2. Estado inicial: 1 infectado, resto susceptibles
    Sa, Ia, Ra = float(N - 1), 1.0, 0.0
    Sb, Ib, Rb = float(N - 1), 1.0, 0.0
    dia_a, dia_b = None, None

    for dia in range(1, 120):
        # 3. Avanza un día cada simulación usando siguiente_paso_sir
        Sa, Ia, Ra = siguiente_paso_sir(Sa, Ia, Ra, N, beta_a, gamma)
        Sb, Ib, Rb = siguiente_paso_sir(Sb, Ib, Rb, N, beta_b, gamma)

        # 4. Verifica si cada uno cruzó el umbral usando tasa_infeccion
        if dia_a is None and tasa_infeccion(Ia, N) >= umbral:
            dia_a = dia
        if dia_b is None and tasa_infeccion(Ib, N) >= umbral:
            dia_b = dia

        if dia_a and dia_b:
            break

    print(f"Carrera al {umbral:.0f}% de infectados (N={N:,}):")
    print(f"  {nombre_a} (R₀={r0_a}): {'Día ' + str(dia_a) if dia_a else 'No llegó en 120 días'}")
    print(f"  {nombre_b} (R₀={r0_b}): {'Día ' + str(dia_b) if dia_b else 'No llegó en 120 días'}")
    if dia_a and dia_b:
        dif = abs(dia_a - dia_b)
        ganador = nombre_b if dia_b < dia_a else nombre_a
        print(f"  → {ganador} llega {dif} día(s) antes.")
    return dia_a, dia_b

# Compara COVID-19 vs Sarampión
carrera_patogenos(r0_valores[2], r0_valores[5], nombres[2], nombres[5])

# Opcional: compara Ébola vs Gripe 1918
# carrera_patogenos(r0_valores[3], r0_valores[1], nombres[3], nombres[1])"""))

# LAB 2
cells.append(md("nb3-lab2-md", """\
---
### 📉 Lab 2 — El Costo del Retraso: ¿Existe un punto de no retorno?

Cada día de retraso en la cuarentena tiene un costo. Pero ¿hay un día a partir del cual
la cuarentena ya no hace diferencia?

Usa `r0_a_beta` + `siguiente_paso_sir` en un loop sobre días de cuarentena (1 al 30)
para calcular el total de infectados al final del brote para cada día de inicio.

**Pregunta clave:** ¿La relación es lineal (cada día cuesta lo mismo) o exponencial (los primeros días son los más importantes)?"""))

cells.append(code("nb3-lab2-code", """\
def costo_del_retraso(r0=r0_valores[2], N=50_000, gamma=1/14, dias_sim=90, reduccion_r0=0.3):
    \"\"\"
    Para cada día de inicio de cuarentena (1-30), calcula el total de infectados.
    reduccion_r0: a qué fracción del R₀ original baja en cuarentena (0.3 = 70% de reducción)
    \"\"\"
    beta_normal = r0_a_beta(r0, gamma)
    beta_cuarentena = r0_a_beta(r0 * reduccion_r0, gamma)

    resultados = []
    for dia_q in range(1, 31):
        S, I, R = float(N - 1), 1.0, 0.0
        for dia in range(1, dias_sim + 1):
            beta_hoy = beta_cuarentena if dia >= dia_q else beta_normal
            S, I, R = siguiente_paso_sir(S, I, R, N, beta_hoy, gamma)
        total_infectados = N - int(S)
        resultados.append((dia_q, total_infectados))

    # Muestra tabla resumen
    print(f"Cuarentena con R₀ reducido al {reduccion_r0*100:.0f}% (N={N:,}, {dias_sim} días):")
    print(f"{'Día cuarentena':>15} | {'Total infectados':>16} | {'% población':>11}")
    print("-" * 48)
    for dia_q, total in resultados[::5]:   # muestra cada 5 días
        pct = total / N * 100
        bar = "█" * int(pct / 2)
        print(f"  Día {dia_q:>2}          |  {total:>14,}   | {pct:>9.1f}%  {bar}")

    # Costo marginal: ¿cuántos infectados extra por cada día de retraso?
    costos = [resultados[i+1][1] - resultados[i][1] for i in range(len(resultados)-1)]
    promedio = sum(costos) / len(costos)
    print(f"\nCosto promedio por día de retraso: +{promedio:,.0f} infectados")
    print(f"Mayor costo marginal: +{max(costos):,.0f} infectados (entre días {costos.index(max(costos))+1} y {costos.index(max(costos))+2})")
    return resultados

resultados_retraso = costo_del_retraso()"""))

# LAB 3
cells.append(md("nb3-lab3-md", """\
---
### 🧬 Lab 3 — El Umbral Real: ¿Cuánta gente necesita Perú vacunar?

Combina `r0_a_beta` + `siguiente_paso_sir` con la fórmula del umbral de inmunidad de rebaño
para calcular, para cada patógeno, cuántas personas deben estar inmunes en Lima (10 millones)
y cuántos muertos estimados sin vacunación.

Este es un ejercicio de política pública, no solo de código."""))

cells.append(code("nb3-lab3-code", """\
def analisis_umbral_vacunacion(nombres, r0_valores, mortalidad, N_ciudad=10_000_000):
    \"\"\"
    Para cada patógeno calcula:
    - Umbral de inmunidad de rebaño (1 - 1/R₀)
    - Personas a vacunar en la ciudad
    - Muertes estimadas si el 60% de la ciudad no vacunada se infecta (peor caso)
    \"\"\"
    print(f"Análisis de vacunación para ciudad de {N_ciudad:,} personas")
    print(f"{'Patógeno':>18} | {'R₀':>4} | {'Umbral':>7} | {'Vacunas necesarias':>18} | {'Muertes est. sin vac':>20}")
    print("-" * 80)

    for i in range(len(nombres)):
        r0 = r0_valores[i]
        cfr = mortalidad[i]    # ya está en % (e.g., 2.0 para 2%)

        # Calcula umbral de rebaño
        if r0 > 1:
            umbral = 1 - 1 / r0
        else:
            umbral = 0.0   # virus en extinción, no necesita umbral

        vacunas = int(umbral * N_ciudad)

        # Estimación de muertes: asume que sin vacunación, ~60% se infecta en epidemia típica
        infectados_estimados = int(0.60 * N_ciudad)
        muertes_estimadas = int(infectados_estimados * cfr / 100)

        barra = "█" * int(umbral * 10) + "░" * (10 - int(umbral * 10))
        print(f"  {nombres[i]:>16} | {r0:>4.1f} | {umbral*100:>5.0f}%  | {vacunas:>18,} | {muertes_estimadas:>20,}")

    print()
    print("Nota: muertes estimadas asumen 60% de infección sin intervención y CFR histórico.")
    print("No son proyecciones oficiales — son estimaciones del modelo.")

analisis_umbral_vacunacion(nombres, r0_valores, mortalidad)"""))

# ════════════════════════════════════════════════════════════
# FINAL
# ════════════════════════════════════════════════════════════

cells.append(md("nb3-final-header", """\
---
## 🏁 Puntaje Final"""))

cells.append(code("nb3-resumen", "grader.resumen()"))


# ════════════════════════════════════════════════════════════
# BUILD NOTEBOOK
# ════════════════════════════════════════════════════════════

nb = {
    "nbformat": 4,
    "nbformat_minor": 5,
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "codemirror_mode": {"name": "ipython", "version": 3},
            "file_extension": ".py",
            "mimetype": "text/x-python",
            "name": "python",
            "pygments_lexer": "ipython3",
            "version": "3.10.0"
        }
    },
    "cells": cells
}

out = "nb3_epidemias.ipynb"
with open(out, "w", encoding="utf-8") as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print(f"OK: {out} generado - {len(cells)} celdas")
