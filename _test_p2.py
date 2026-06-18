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

# ─── intex1 ────────────────────────────────────────────────────
pacientes = [
    (0,  False, False, False),
    (12, False, False, False),
    (12, True,  False, False),
    (36, True,  True,  True),
]
for (horas, fiebre, neuro, consciencia) in pacientes:
    if horas <= 0:
        clasificacion = "LIMPIO"
    else:
        if not fiebre:
            clasificacion = "SOSPECHOSO"
        else:
            if not neuro:
                clasificacion = "INFECTADO TEMPRANO"
            else:
                if not consciencia:
                    clasificacion = "INFECTADO AVANZADO"
                else:
                    clasificacion = "CASO TERMINAL"

__main__.clasificacion = clasificacion
__main__.horas = horas
__main__.fiebre = fiebre
__main__.neuro = neuro
__main__.consciencia = consciencia

pts = g.check_intex1()
print(f"intex1 correct: {pts}/6")
assert pts == 6, f"Expected 6, got {pts}"

# Wrong: only SOSPECHOSO level reached
__main__.clasificacion = "SOSPECHOSO"
__main__.fiebre = False
__main__.neuro = False
__main__.consciencia = False
g._scores.pop("intex1", None)
pts2 = g.check_intex1()
print(f"intex1 only SOSPECHOSO: {pts2}/6")
assert pts2 < 6

# ─── intex2 ────────────────────────────────────────────────────
cont_qz = cont_p0 = cont_segura = cont_nodo = cont_calle = 0
fila_v = col_v = 0
for fila in range(8):
    for col in range(8):
        if (fila in [0,7]) and (col in [0,7]):
            cont_qz += 1; simbolo = "[QZ]"
        elif fila + col <= 2:
            cont_p0 += 1; simbolo = "[P0]"
        elif abs(fila-4) + abs(col-4) <= 2:
            cont_segura += 1; simbolo = "[--]"
        elif fila % 3 == 0 and col % 3 == 0:
            cont_nodo += 1; simbolo = "[IN]"
        else:
            cont_calle += 1; simbolo = "[  ]"
        fila_v = fila; col_v = col

__main__.cont_qz = cont_qz; __main__.cont_p0 = cont_p0
__main__.cont_segura = cont_segura; __main__.cont_nodo = cont_nodo
__main__.cont_calle = cont_calle; __main__.fila = fila_v; __main__.col = col_v

pts = g.check_intex2()
print(f"intex2 correct: {pts}/8")
assert pts == 8, f"Expected 8, got {pts}"

# Wrong counts
__main__.cont_qz = 8; __main__.cont_p0 = 3
g._scores.pop("intex2", None)
pts2 = g.check_intex2()
print(f"intex2 wrong: {pts2}/8")
assert pts2 < 8

# ─── intex3 ────────────────────────────────────────────────────
nombres    = ['Cordyceps','Walker','COVID-19','Ebola','Gripe 1918','Sarampion','Peste Bubonica']
r0_valores = [3.5, 1.2, 2.5, 1.8, 2.0, 15.0, 2.6]
mortalidad = [0.85, 1.0, 0.02, 0.65, 0.10, 0.002, 0.30]
infectados_0 = 50; poblacion = 50_000

for i in range(len(nombres)):
    infectados = infectados_0; pico_dia = 0; pico_inf = infectados_0
    for dia in range(1, 15):
        infectados = min(int(infectados * r0_valores[i]), poblacion)
        if infectados > pico_inf:
            pico_inf = infectados; pico_dia = dia
    muertes = int(pico_inf * mortalidad[i])

__main__.i = i; __main__.dia = dia; __main__.pico_inf = pico_inf
__main__.pico_dia = pico_dia; __main__.muertes = muertes

pts = g.check_intex3()
print(f"intex3 correct: {pts}/8")
assert pts == 8, f"Expected 8, got {pts}"

__main__.pico_inf = 40000; __main__.muertes = 12000
g._scores.pop("intex3", None)
pts2 = g.check_intex3()
print(f"intex3 wrong values: {pts2}/8")
assert pts2 < 8

# ─── intex4 ────────────────────────────────────────────────────
r0_base = r0_valores[2]  # 2.5 COVID
def correr_sim4(dq):
    zi = [50,20,100,10,200,30]; pobs=[5000,3000,10000,2000,8000,4000]
    caidas=[False]*6
    for dia in range(1,31):
        for z in range(6):
            if caidas[z]: continue
            tasa = zi[z]/pobs[z]
            r0_hoy = r0_base*0.4 if dia>=dq else r0_base
            if dia>20 and tasa>0.4: r0_hoy *= 0.2
            zi[z] = min(int(zi[z]*r0_hoy), pobs[z])
            tasa = zi[z]/pobs[z]
            if tasa>0.6: caidas[z]=True
    return dia, zi, caidas

dia_v, zi_v, caidas_v = correr_sim4(20)
__main__.dia = dia_v; __main__.zonas_inf = zi_v
__main__.zonas_caidas = caidas_v; __main__.dia_cuarentena = 20

pts = g.check_intex4()
print(f"intex4 correct (dq=20): {pts}/10")
assert pts == 10, f"Expected 10, got {pts}"

# Wrong: incomplete loop
__main__.dia = 15
g._scores.pop("intex4", None)
pts2 = g.check_intex4()
print(f"intex4 incomplete (dia=15): {pts2}/10")
assert pts2 < 10

# ─── intex5 ────────────────────────────────────────────────────
def aplicar_r0(infectados, r0, capacidad):
    return min(int(infectados*r0), capacidad)

def r0_efectivo(r0_base, dia, dia_intervencion, tasa_actual):
    if dia >= dia_intervencion or tasa_actual > 0.3:
        return r0_base * 0.4
    return r0_base

def simular_ciudad(zonas_iniciales, poblaciones, r0_base, cfr, dia_intervencion, dias):
    zi = zonas_iniciales[:]
    caidas = [False]*len(zi)
    total_por_dia = []; caidas_por_dia = []
    for dia in range(1, dias+1):
        total = 0; c = 0
        for z in range(len(zi)):
            if caidas[z]: c+=1; continue
            tasa = zi[z]/poblaciones[z]
            r0_hoy = r0_efectivo(r0_base, dia, dia_intervencion, tasa)
            zi[z] = aplicar_r0(zi[z], r0_hoy, poblaciones[z])
            tasa = zi[z]/poblaciones[z]
            if tasa > 0.6: caidas[z] = True
            total += zi[z]
        total_por_dia.append(total); caidas_por_dia.append(c)
    return total_por_dia, caidas_por_dia

r0v = [3.5,1.2,2.5,1.8,2.0,15.0,2.6]; mort=[0.85,1.0,0.02,0.65,0.10,0.002,0.30]
zi=[100,50,200,30,500]; pbs=[5000,3000,8000,2000,10000]
tc, cc = simular_ciudad(zi, pbs, r0v[0], mort[0], 7, 30)
tv, cv = simular_ciudad(zi, pbs, r0v[2], mort[2], 10, 30)

__main__.aplicar_r0    = aplicar_r0
__main__.r0_efectivo   = r0_efectivo
__main__.simular_ciudad = simular_ciudad
__main__.total_cordyceps = tc
__main__.total_covid    = tv

pts = g.check_intex5()
print(f"intex5 correct: {pts}/12")
assert pts == 12, f"Expected 12, got {pts}"

# bad aplicar_r0 (no cap)
def aplicar_r0_bad(i,r,c): return int(i*r)
__main__.aplicar_r0 = aplicar_r0_bad
g._scores.pop("intex5", None)
pts2 = g.check_intex5()
print(f"intex5 no-cap aplicar_r0: {pts2}/12")
assert pts2 < 12

print("ALL PARTE 2 CHECKS PASSED")
