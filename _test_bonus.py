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

# ─── RETO 1 ────────────────────────────────────────────────────
nombres    = ['Cordyceps','Walker','COVID-19','Ebola','Gripe 1918','Sarampion','Peste Bubonica']
r0_valores = [3.5, 1.2, 2.5, 1.8, 2.0, 15.0, 2.6]

def dias_hasta_colapso(poblacion, infectados_0, r0):
    infectados = infectados_0
    for dia in range(1, 366):
        infectados = int(infectados * r0)
        if infectados > poblacion * 0.6:
            return dia
    return -1

__main__.dias_hasta_colapso = dias_hasta_colapso

resultados = []
for i in range(len(nombres)):
    dias = dias_hasta_colapso(100_000, 100, r0_valores[i])
    resultados.append((dias if dias != -1 else 366, nombres[i], r0_valores[i], dias))
resultados.sort()

print(f"resultados[0] = {resultados[0]}")
print(f"resultados[-1] = {resultados[-1]}")
__main__.resultados = resultados

pts = g.check_reto1()
print(f"reto1 correct: {pts}/6")
assert pts == 6, f"Expected 6, got {pts}"

# Wrong: no collapse with R0<1 but return 0 instead of -1
def dtc_bad(p, i0, r0):
    infectados = i0
    for dia in range(1, 366):
        infectados = int(infectados * r0)
        if infectados > p * 0.6:
            return dia
    return 0  # Bug: returns 0 instead of -1

__main__.dias_hasta_colapso = dtc_bad
g._scores.pop("reto1", None)
pts2 = g.check_reto1()
print(f"reto1 bad R0<1 return: {pts2}/6")
assert pts2 < 6

# ─── RETO 2 ────────────────────────────────────────────────────
def siguiente_paso_sir(S, I, R, N, beta, gamma):
    ni = beta * S * I / N
    nr = gamma * I
    return S - ni, I + ni - nr, R + nr

def r0_a_beta(r0, gamma):
    return r0 * gamma

__main__.siguiente_paso_sir = siguiente_paso_sir
__main__.r0_a_beta = r0_a_beta

pts = g.check_reto2()
print(f"reto2 correct: {pts}/6")
assert pts == 6, f"Expected 6, got {pts}"

# Wrong: r0_a_beta returns r0 only
def bad_beta(r0, gamma): return r0
__main__.r0_a_beta = bad_beta
g._scores.pop("reto2", None)
pts2 = g.check_reto2()
print(f"reto2 bad beta: {pts2}/6")
assert pts2 < 6

print("ALL BONUS CHECKS PASSED")
