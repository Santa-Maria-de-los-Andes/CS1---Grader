import sys
sys.stdout.reconfigure(encoding="utf-8")
import IPython.display as _d
_d.display = lambda *a, **k: None
_d.HTML    = lambda x: x

import importlib, autograder_nb3 as ag3
importlib.reload(ag3)

g = ag3.Autograder.__new__(ag3.Autograder)
g._scores = {}; g._achievements = set(); g._streak = 0; g._prev_level = 0
g._email = None; g._nombre_real = "T"; g._grado = "3ro"; g._dni = "0"; g._checkpoints = set()

import __main__

# ─── ex1: with count = 13 ─────────────────────────────────────
__main__.fila = 5; __main__.col = 5; __main__.distancia = 4; __main__.infectadas = 13
pts = g.check_ex1()
print(f"ex1 correct (count=13): {pts}/6")
assert pts == 6, f"Expected 6, got {pts}"

# ex1: no count variable (only loop state) → should be 4/6 (2 loop checks pass, count absent)
if hasattr(__main__, "infectadas"): del __main__.infectadas
if hasattr(__main__, "total"): del __main__.total
g._scores.pop("ex1", None)
pts = g.check_ex1()
print(f"ex1 no count var: {pts}/6")
assert pts == 4, f"Expected 4, got {pts}"

# ex1: wrong count → should lose that check
__main__.infectadas = 9
g._scores.pop("ex1", None)
pts = g.check_ex1()
print(f"ex1 wrong count: {pts}/6")
assert pts < 6

# ─── ex4 ──────────────────────────────────────────────────────
__main__.dia = 10; __main__.infectados = 50000
__main__.infectados_ebola = 17767; __main__.i = 5
g._scores.pop("ex4", None)
pts = g.check_ex4()
print(f"ex4 correct: {pts}/8")
assert pts == 8, f"Expected 8, got {pts}"

# Missing ebola var
if hasattr(__main__, "infectados_ebola"): del __main__.infectados_ebola
g._scores.pop("ex4", None)
pts = g.check_ex4()
print(f"ex4 no ebola var: {pts}/8")
assert pts < 8, f"Expected <8, got {pts}"

# ─── debug2b ──────────────────────────────────────────────────
__main__.ola = 2; __main__.dia = 10; __main__.infectados = 100000
__main__.infectados_ola1 = 100000
g._scores.pop("debug2b", None)
pts = g.check_debug2b()
print(f"debug2b with ola1 var: {pts}/3")
assert pts == 3, f"Expected 3, got {pts}"

# Without ola1 var: falls back to infectados==100000 check
if hasattr(__main__, "infectados_ola1"): del __main__.infectados_ola1
g._scores.pop("debug2b", None)
pts = g.check_debug2b()
print(f"debug2b fallback (infectados=100000): {pts}/3")
assert pts == 3  # still passes via fallback

# ─── ex5 ──────────────────────────────────────────────────────
__main__.ola = 2; __main__.dia = 10; __main__.infectados = 100000
__main__.infectados_ola1 = 100000; __main__.infectados_ola2 = 100000; __main__.diferencia = 0
g._scores.pop("ex5", None)
pts = g.check_ex5()
print(f"ex5 correct: {pts}/8")
assert pts == 8, f"Expected 8, got {pts}"

# Missing ola loop var
if hasattr(__main__, "ola"): del __main__.ola
g._scores.pop("ex5", None)
pts = g.check_ex5()
print(f"ex5 no ola var: {pts}/8")
assert pts < 8, f"Expected <8, got {pts}"

# ─── ex8 dq=5 (zone 3 saved) ──────────────────────────────────
__main__.dia = 21
__main__.infectados_z = [3905, 1950, 7812, 1167, 7812]
__main__.zonas_caidas = [True, True, True, False, True]
__main__.dia_cuarentena = 5
__main__.total = 22646
g._scores.pop("ex8", None)
pts = g.check_ex8()
print(f"ex8 dq=5 correct: {pts}/10")
assert pts == 10, f"Expected 10, got {pts}"

# ex8 dq=14 (zone 3 falls)
__main__.infectados_z = [3905, 1950, 7812, 2000, 7812]
__main__.zonas_caidas = [True, True, True, True, True]
__main__.dia_cuarentena = 14; __main__.total = 23479
g._scores.pop("ex8", None)
pts = g.check_ex8()
print(f"ex8 dq=14 correct: {pts}/10")
assert pts == 10, f"Expected 10, got {pts}"

# ex8 dq=5 but zone 3 wrongly marked fallen (broken quarantine if-block)
__main__.infectados_z = [3905, 1950, 7812, 1167, 7812]
__main__.zonas_caidas = [True, True, True, True, True]   # zone 3 wrongly True
__main__.dia_cuarentena = 5
g._scores.pop("ex8", None)
pts = g.check_ex8()
print(f"ex8 broken quarantine flag: {pts}/10")
assert pts < 10, f"Expected <10, got {pts}"

print("ALL REVISED CHECKS PASSED")
