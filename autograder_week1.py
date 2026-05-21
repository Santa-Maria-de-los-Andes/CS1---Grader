"""
Autograder - Semana 1: Variables, Operaciones y Entrada del Usuario
===================================================================
Uso en Google Colab:
    from autograder_week1 import Autograder
    grader = Autograder()
    grader.check_s1_ex1()   # Sesión 1, Ejercicio 1
    grader.check_s2_ex1()   # Sesión 2, Ejercicio 1
"""

import math


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _get(name):
    """Read a variable from the student's notebook namespace."""
    try:
        import __main__
        return getattr(__main__, name, None)
    except Exception:
        return None


def _approx(a, b, tol=1e-6):
    try:
        return abs(float(a) - float(b)) < tol
    except (TypeError, ValueError):
        return False


def _header(title):
    print(f"\n{'═' * 58}")
    print(f"  {title}")
    print(f"{'═' * 58}")


def _footer(passed, total):
    filled = "█" * passed
    empty  = "░" * (total - passed)
    print(f"\n  Resultado: {passed}/{total}  [{filled}{empty}]")
    if passed == total:
        print("  🌟 ¡EXCELENTE! ¡Todo correcto!")
    elif passed >= total * 0.7:
        print("  👍 ¡Buen trabajo! Lee los mensajes de arriba para mejorar.")
    else:
        print("  💪 ¡Sigue intentando! Lee los ❌ para ver qué ajustar.")
    print(f"{'═' * 58}\n")


def _row(ok, label, msg):
    icon = "✅" if ok else "❌"
    print(f"  {icon} {label}: {msg}")


# ---------------------------------------------------------------------------
# Autograder class
# ---------------------------------------------------------------------------

class Autograder:
    """Autograder for Week 1 — both sessions."""

    def __init__(self):
        print("✅ Autograder cargado. ¡Listo para revisar tus ejercicios!")

    # =====================================================================
    # SESIÓN 1 — Variables y Operaciones Básicas
    # =====================================================================

    def check_s1_ex1(self):
        """S1-E1: Mi Información Personal"""
        _header("SESIÓN 1 · Ejercicio 1 — Mi Información Personal")
        r = []

        nombre = _get("tu_nombre")
        edad   = _get("tu_edad")
        ciudad = _get("tu_ciudad")

        # tu_nombre
        if nombre is None:
            r.append((False, "tu_nombre", "No encontrada — define: tu_nombre = \"TuNombre\""))
        elif not isinstance(nombre, str):
            r.append((False, "tu_nombre", f"Debe ser string (texto), recibí {type(nombre).__name__}"))
        elif nombre.strip() == "":
            r.append((False, "tu_nombre", "No puede estar vacía"))
        else:
            r.append((True, "tu_nombre", f"string ✓  →  '{nombre}'"))

        # tu_edad
        if edad is None:
            r.append((False, "tu_edad", "No encontrada — define: tu_edad = TuEdad  (sin comillas)"))
        elif isinstance(edad, bool):
            r.append((False, "tu_edad", "Debe ser int, no bool"))
        elif not isinstance(edad, int):
            r.append((False, "tu_edad", f"Debe ser int (entero sin comillas), recibí {type(edad).__name__}"))
        elif not (5 <= edad <= 110):
            r.append((False, "tu_edad", f"El valor {edad} no parece una edad válida (5-110)"))
        else:
            r.append((True, "tu_edad", f"int ✓  →  {edad}"))

        # tu_ciudad
        if ciudad is None:
            r.append((False, "tu_ciudad", "No encontrada — define: tu_ciudad = \"TuCiudad\""))
        elif not isinstance(ciudad, str):
            r.append((False, "tu_ciudad", f"Debe ser string, recibí {type(ciudad).__name__}"))
        elif ciudad.strip() == "":
            r.append((False, "tu_ciudad", "No puede estar vacía"))
        else:
            r.append((True, "tu_ciudad", f"string ✓  →  '{ciudad}'"))

        for row in r:
            _row(*row)
        _footer(sum(x[0] for x in r), len(r))

    # ------------------------------------------------------------------

    def check_s1_ex2(self):
        """S1-E2: Calculadora Simple"""
        _header("SESIÓN 1 · Ejercicio 2 — Calculadora Simple")
        r = []

        p1    = _get("precio1")
        p2    = _get("precio2")
        total = _get("total")

        for vname, val in [("precio1", p1), ("precio2", p2)]:
            if val is None:
                r.append((False, vname, f"No encontrada"))
            elif not isinstance(val, (int, float)) or isinstance(val, bool):
                r.append((False, vname, f"Debe ser número, recibí {type(val).__name__}"))
            else:
                r.append((True, vname, f"número ✓  →  {val}"))

        if total is None:
            r.append((False, "total", "No encontrada — usa: total = precio1 + precio2"))
        elif p1 is not None and p2 is not None and _approx(total, p1 + p2):
            r.append((True, "total = precio1 + precio2", f"✓  →  {p1} + {p2} = {total}"))
        else:
            exp = (p1 or 0) + (p2 or 0)
            r.append((False, "total", f"Debería ser {exp}, obtuve {total} — usa: total = precio1 + precio2"))

        for row in r:
            _row(*row)
        _footer(sum(x[0] for x in r), len(r))

    # ------------------------------------------------------------------

    def check_s1_ex3(self):
        """S1-E3: Área de un Rectángulo"""
        _header("SESIÓN 1 · Ejercicio 3 — Área de un Rectángulo")
        r = []

        largo = _get("largo")
        ancho = _get("ancho")
        area  = _get("area")

        for vname, val in [("largo", largo), ("ancho", ancho)]:
            if val is None:
                r.append((False, vname, "No encontrada"))
            elif not isinstance(val, (int, float)) or isinstance(val, bool):
                r.append((False, vname, "Debe ser número"))
            elif val <= 0:
                r.append((False, vname, f"Debe ser positivo, recibí {val}"))
            else:
                r.append((True, vname, f"número ✓  →  {val}"))

        if area is None:
            r.append((False, "area", "No encontrada — usa: area = largo * ancho"))
        elif largo is not None and ancho is not None and _approx(area, largo * ancho):
            r.append((True, "area = largo * ancho", f"✓  →  {largo} × {ancho} = {area}"))
        else:
            exp = (largo or 0) * (ancho or 0)
            r.append((False, "area", f"Debería ser {exp}, obtuve {area}"))

        perimetro = _get("perimetro")
        if perimetro is not None and largo is not None and ancho is not None:
            if _approx(perimetro, 2 * (largo + ancho)):
                r.append((True, "🌟 BONUS perimetro", f"✓  →  {perimetro}"))
            else:
                r.append((False, "🌟 BONUS perimetro", f"Debería ser {2*(largo+ancho)}, obtuve {perimetro}"))

        for row in r:
            _row(*row)
        _footer(sum(x[0] for x in r), len(r))

    # ------------------------------------------------------------------

    def check_s1_ex4(self):
        """S1-E4: Conversión de Temperatura"""
        _header("SESIÓN 1 · Ejercicio 4 — Conversión de Temperatura")
        r = []

        celsius    = _get("celsius")
        fahrenheit = _get("fahrenheit")

        if celsius is None:
            r.append((False, "celsius", "No encontrada"))
        elif not isinstance(celsius, (int, float)) or isinstance(celsius, bool):
            r.append((False, "celsius", "Debe ser número"))
        else:
            r.append((True, "celsius", f"número ✓  →  {celsius}"))

        if fahrenheit is None:
            r.append((False, "fahrenheit", "No encontrada — usa: fahrenheit = celsius * 9/5 + 32"))
        elif celsius is not None:
            exp = celsius * 9 / 5 + 32
            if _approx(fahrenheit, exp):
                r.append((True, "fahrenheit = celsius * 9/5 + 32", f"✓  →  {fahrenheit}°F"))
            else:
                r.append((False, "fahrenheit", f"Para {celsius}°C debería ser {exp:.2f}°F, obtuve {fahrenheit}"))

        for row in r:
            _row(*row)
        _footer(sum(x[0] for x in r), len(r))

    # ------------------------------------------------------------------

    def check_s1_ex5(self):
        """S1-E5: Cambio de Moneda"""
        _header("SESIÓN 1 · Ejercicio 5 — Cambio de Moneda")
        r = []

        soles       = _get("soles")
        tipo_cambio = _get("tipo_cambio")
        dolares     = _get("dolares")

        for vname, val in [("soles", soles), ("tipo_cambio", tipo_cambio)]:
            if val is None:
                r.append((False, vname, "No encontrada"))
            elif not isinstance(val, (int, float)) or isinstance(val, bool):
                r.append((False, vname, "Debe ser número"))
            else:
                r.append((True, vname, f"número ✓  →  {val}"))

        if dolares is None:
            r.append((False, "dolares", "No encontrada — usa: dolares = soles / tipo_cambio"))
        elif soles is not None and tipo_cambio is not None and tipo_cambio != 0:
            exp = soles / tipo_cambio
            if _approx(dolares, exp, tol=1e-4):
                r.append((True, "dolares = soles / tipo_cambio", f"✓  →  {dolares:.4f}"))
            else:
                r.append((False, "dolares", f"Debería ser {exp:.4f}, obtuve {dolares}"))

        for row in r:
            _row(*row)
        _footer(sum(x[0] for x in r), len(r))

    # ------------------------------------------------------------------

    def check_s1_ex6(self):
        """S1-E6: Promedio de Notas"""
        _header("SESIÓN 1 · Ejercicio 6 — Promedio de Notas")
        r = []

        notas = [_get(f"nota{i}") for i in range(1, 4)]
        promedio = _get("promedio")

        for i, nota in enumerate(notas, 1):
            if nota is None:
                r.append((False, f"nota{i}", "No encontrada"))
            elif not isinstance(nota, (int, float)) or isinstance(nota, bool):
                r.append((False, f"nota{i}", "Debe ser número"))
            elif not (0 <= nota <= 20):
                r.append((False, f"nota{i}", f"Nota {nota} fuera del rango 0-20"))
            else:
                r.append((True, f"nota{i}", f"número ✓  →  {nota}"))

        if promedio is None:
            r.append((False, "promedio", "No encontrada — usa: promedio = (nota1 + nota2 + nota3) / 3"))
        elif all(n is not None for n in notas):
            exp = sum(notas) / 3
            if _approx(promedio, exp):
                r.append((True, "promedio = (nota1+nota2+nota3)/3", f"✓  →  {promedio:.4f}"))
            else:
                r.append((False, "promedio", f"Debería ser {exp:.4f}, obtuve {promedio}"))

        for row in r:
            _row(*row)
        _footer(sum(x[0] for x in r), len(r))

    # ------------------------------------------------------------------

    def check_s1_ex7(self):
        """S1-E7: Compra con IGV"""
        _header("SESIÓN 1 · Ejercicio 7 — Compra con IGV")
        r = []

        base  = _get("precio_base")
        igv   = _get("igv")
        total = _get("precio_total")

        if base is None:
            r.append((False, "precio_base", "No encontrada"))
        elif not isinstance(base, (int, float)) or isinstance(base, bool):
            r.append((False, "precio_base", "Debe ser número"))
        else:
            r.append((True, "precio_base", f"número ✓  →  {base}"))

        if igv is None:
            r.append((False, "igv", "No encontrada — usa: igv = precio_base * 0.18"))
        elif base is not None:
            exp = base * 0.18
            if _approx(igv, exp):
                r.append((True, "igv = precio_base * 0.18", f"✓  →  {igv}"))
            else:
                r.append((False, "igv", f"Para base={base}, IGV debería ser {exp}, obtuve {igv}"))

        if total is None:
            r.append((False, "precio_total", "No encontrada — usa: precio_total = precio_base + igv"))
        elif base is not None and igv is not None:
            exp = base + igv
            if _approx(total, exp):
                r.append((True, "precio_total = precio_base + igv", f"✓  →  {total}"))
            else:
                r.append((False, "precio_total", f"Debería ser {exp}, obtuve {total}"))

        for row in r:
            _row(*row)
        _footer(sum(x[0] for x in r), len(r))

    # ------------------------------------------------------------------

    def check_s1_ex8(self):
        """S1-E8: Tu Edad en Días"""
        _header("SESIÓN 1 · Ejercicio 8 — Tu Edad en Días")
        r = []

        edad    = _get("tu_edad")
        dias    = _get("dias_vividos")
        horas   = _get("horas_vividas")
        minutos = _get("minutos_vividos")

        if edad is None:
            r.append((False, "tu_edad", "No encontrada"))
        elif isinstance(edad, bool) or not isinstance(edad, int):
            r.append((False, "tu_edad", "Debe ser int (entero)"))
        elif not (5 <= edad <= 110):
            r.append((False, "tu_edad", f"Valor {edad} no parece una edad válida"))
        else:
            r.append((True, "tu_edad", f"int ✓  →  {edad}"))

        if dias is None:
            r.append((False, "dias_vividos", "No encontrada — usa: dias_vividos = tu_edad * 365"))
        elif edad is not None and _approx(dias, edad * 365):
            r.append((True, "dias_vividos = tu_edad * 365", f"✓  →  {dias}"))
        else:
            r.append((False, "dias_vividos", f"Fórmula incorrecta — usa: dias_vividos = tu_edad * 365"))

        if horas is None:
            r.append((False, "horas_vividas", "No encontrada — usa: horas_vividas = dias_vividos * 24"))
        elif dias is not None and _approx(horas, dias * 24):
            r.append((True, "horas_vividas = dias_vividos * 24", f"✓  →  {horas}"))
        else:
            r.append((False, "horas_vividas", "Fórmula incorrecta — usa: horas_vividas = dias_vividos * 24"))

        if minutos is None:
            r.append((False, "minutos_vividos", "No encontrada — usa: minutos_vividos = horas_vividas * 60"))
        elif horas is not None and _approx(minutos, horas * 60):
            r.append((True, "minutos_vividos = horas_vividas * 60", f"✓  →  {minutos}"))
        else:
            r.append((False, "minutos_vividos", "Fórmula incorrecta"))

        segundos = _get("segundos_vividos")
        if segundos is not None and minutos is not None and _approx(segundos, minutos * 60):
            r.append((True, "🌟 BONUS segundos_vividos", f"✓  →  {segundos}"))

        for row in r:
            _row(*row)
        _footer(sum(x[0] for x in r), len(r))

    # ------------------------------------------------------------------

    def check_s1_ex9(self):
        """S1-E9: Velocidad Promedio"""
        _header("SESIÓN 1 · Ejercicio 9 — Velocidad Promedio")
        r = []

        distancia = _get("distancia")
        tiempo    = _get("tiempo")
        velocidad = _get("velocidad")

        for vname, val in [("distancia", distancia), ("tiempo", tiempo)]:
            if val is None:
                r.append((False, vname, "No encontrada"))
            elif not isinstance(val, (int, float)) or isinstance(val, bool):
                r.append((False, vname, "Debe ser número"))
            elif val <= 0:
                r.append((False, vname, f"Debe ser positivo, recibí {val}"))
            else:
                r.append((True, vname, f"número ✓  →  {val}"))

        if velocidad is None:
            r.append((False, "velocidad", "No encontrada — usa: velocidad = distancia / tiempo"))
        elif distancia is not None and tiempo is not None and tiempo != 0:
            exp = distancia / tiempo
            if _approx(velocidad, exp, tol=1e-4):
                r.append((True, "velocidad = distancia / tiempo", f"✓  →  {velocidad:.2f} km/h"))
            else:
                r.append((False, "velocidad", f"Debería ser {exp:.4f}, obtuve {velocidad}"))

        for row in r:
            _row(*row)
        _footer(sum(x[0] for x in r), len(r))

    # ------------------------------------------------------------------

    def check_s1_ex10(self):
        """S1-E10: Geometría del Círculo"""
        _header("SESIÓN 1 · Ejercicio 10 — Geometría del Círculo")
        r = []

        radio          = _get("radio")
        area_circulo   = _get("area_circulo")
        circunferencia = _get("circunferencia")

        if radio is None:
            r.append((False, "radio", "No encontrada"))
        elif not isinstance(radio, (int, float)) or isinstance(radio, bool):
            r.append((False, "radio", "Debe ser número"))
        elif radio <= 0:
            r.append((False, "radio", "Debe ser positivo"))
        else:
            r.append((True, "radio", f"número ✓  →  {radio}"))

        if area_circulo is None:
            r.append((False, "area_circulo", "No encontrada — usa: area_circulo = 3.14159 * radio ** 2"))
        elif radio is not None:
            exp = math.pi * radio ** 2
            if _approx(area_circulo, exp, tol=0.01):
                r.append((True, "area_circulo = pi * radio²", f"✓  →  {area_circulo:.4f}"))
            else:
                r.append((False, "area_circulo", f"Debería ser ≈{exp:.4f}, obtuve {area_circulo}"))

        if circunferencia is None:
            r.append((False, "circunferencia", "No encontrada — usa: circunferencia = 2 * 3.14159 * radio"))
        elif radio is not None:
            exp = 2 * math.pi * radio
            if _approx(circunferencia, exp, tol=0.01):
                r.append((True, "circunferencia = 2 * pi * radio", f"✓  →  {circunferencia:.4f}"))
            else:
                r.append((False, "circunferencia", f"Debería ser ≈{exp:.4f}, obtuve {circunferencia}"))

        for row in r:
            _row(*row)
        _footer(sum(x[0] for x in r), len(r))

    # ------------------------------------------------------------------

    def check_s1_ex11(self):
        """S1-E11: División Entera y Módulo"""
        _header("SESIÓN 1 · Ejercicio 11 — División Entera y Módulo")
        r = []

        dividendo = _get("dividendo")
        divisor   = _get("divisor")
        cociente  = _get("cociente")
        residuo   = _get("residuo")

        for vname, val in [("dividendo", dividendo), ("divisor", divisor)]:
            if val is None:
                r.append((False, vname, "No encontrada"))
            elif isinstance(val, bool) or not isinstance(val, int):
                r.append((False, vname, "Debe ser int (entero)"))
            else:
                r.append((True, vname, f"int ✓  →  {val}"))

        if cociente is None:
            r.append((False, "cociente", "No encontrada — usa: cociente = dividendo // divisor"))
        elif dividendo is not None and divisor is not None and divisor != 0:
            exp = dividendo // divisor
            if cociente == exp:
                r.append((True, "cociente = dividendo // divisor", f"✓  →  {cociente}"))
            else:
                r.append((False, "cociente", f"Debería ser {exp}, obtuve {cociente} — usa //"))

        if residuo is None:
            r.append((False, "residuo", "No encontrada — usa: residuo = dividendo % divisor"))
        elif dividendo is not None and divisor is not None and divisor != 0:
            exp = dividendo % divisor
            if residuo == exp:
                r.append((True, "residuo = dividendo % divisor", f"✓  →  {residuo}"))
            else:
                r.append((False, "residuo", f"Debería ser {exp}, obtuve {residuo} — usa %"))

        for row in r:
            _row(*row)
        _footer(sum(x[0] for x in r), len(r))

    # ------------------------------------------------------------------

    def check_s1_ex12(self):
        """S1-E12: Potencia y Raíz Cuadrada"""
        _header("SESIÓN 1 · Ejercicio 12 — Potencia y Raíz Cuadrada")
        r = []

        base    = _get("base")
        exp_val = _get("exponente")
        potencia = _get("potencia")
        raiz    = _get("raiz")

        for vname, val in [("base", base), ("exponente", exp_val)]:
            if val is None:
                r.append((False, vname, "No encontrada"))
            elif not isinstance(val, (int, float)) or isinstance(val, bool):
                r.append((False, vname, "Debe ser número"))
            else:
                r.append((True, vname, f"número ✓  →  {val}"))

        if potencia is None:
            r.append((False, "potencia", "No encontrada — usa: potencia = base ** exponente"))
        elif base is not None and exp_val is not None:
            exp = base ** exp_val
            if _approx(potencia, exp, tol=1e-3):
                r.append((True, "potencia = base ** exponente", f"✓  →  {potencia}"))
            else:
                r.append((False, "potencia", f"Debería ser {exp}, obtuve {potencia}"))

        if raiz is None:
            r.append((False, "raiz", "No encontrada — usa: raiz = base ** 0.5  o  base ** (1/2)"))
        elif base is not None and base >= 0:
            exp = base ** 0.5
            if _approx(raiz, exp, tol=1e-4):
                r.append((True, "raiz = base ** 0.5", f"✓  →  {raiz:.4f}"))
            else:
                r.append((False, "raiz", f"Debería ser {exp:.4f}, obtuve {raiz}"))

        for row in r:
            _row(*row)
        _footer(sum(x[0] for x in r), len(r))

    # =====================================================================
    # SESIÓN 2 — Texto Interactivo y Entrada del Usuario
    # =====================================================================

    def check_s2_ex1(self):
        """S2-E1: Saludo Personalizado"""
        _header("SESIÓN 2 · Ejercicio 1 — Saludo Personalizado")
        r = []

        nombre = _get("nombre")
        ciudad = _get("ciudad")

        for vname, val in [("nombre", nombre), ("ciudad", ciudad)]:
            if val is None:
                r.append((False, vname, "No encontrada — ejecuta tu celda primero (▶)"))
            elif not isinstance(val, str):
                r.append((False, vname, f"Debe ser string, recibí {type(val).__name__}"))
            elif val.strip() == "":
                r.append((False, vname, "No puede estar vacía"))
            else:
                r.append((True, vname, f"string ✓  →  '{val}'"))

        for row in r:
            _row(*row)
        _footer(sum(x[0] for x in r), len(r))

    # ------------------------------------------------------------------

    def check_s2_ex2(self):
        """S2-E2: Suma Interactiva"""
        _header("SESIÓN 2 · Ejercicio 2 — Suma Interactiva")
        r = []

        n1   = _get("numero1")
        n2   = _get("numero2")
        suma = _get("suma")

        for vname, val in [("numero1", n1), ("numero2", n2)]:
            if val is None:
                r.append((False, vname, "No encontrada — usa: numero1 = int(input(...))"))
            elif isinstance(val, bool) or not isinstance(val, int):
                r.append((False, vname, f"Debe ser int. ¿Usaste int(input(...))? Recibí {type(val).__name__}"))
            else:
                r.append((True, vname, f"int ✓  →  {val}"))

        if suma is None:
            r.append((False, "suma", "No encontrada — usa: suma = numero1 + numero2"))
        elif n1 is not None and n2 is not None and isinstance(n1, int) and isinstance(n2, int):
            exp = n1 + n2
            if suma == exp:
                r.append((True, "suma = numero1 + numero2", f"✓  →  {n1} + {n2} = {suma}"))
            else:
                r.append((False, "suma", f"Debería ser {exp}, obtuve {suma}"))

        for row in r:
            _row(*row)
        _footer(sum(x[0] for x in r), len(r))

    # ------------------------------------------------------------------

    def check_s2_ex3(self):
        """S2-E3: Generador de Apodos"""
        _header("SESIÓN 2 · Ejercicio 3 — Generador de Apodos")
        r = []

        nombre = _get("nombre")
        color  = _get("color")
        animal = _get("animal")
        apodo  = _get("apodo")

        for vname, val in [("nombre", nombre), ("color", color), ("animal", animal)]:
            if val is None:
                r.append((False, vname, "No encontrada"))
            elif not isinstance(val, str) or val.strip() == "":
                r.append((False, vname, "Debe ser string no vacío"))
            else:
                r.append((True, vname, f"string ✓  →  '{val}'"))

        if apodo is None:
            r.append((False, "apodo", "No encontrada — crea la variable apodo combinando nombre+color+animal"))
        elif not isinstance(apodo, str):
            r.append((False, "apodo", "Debe ser string"))
        else:
            faltantes = []
            for label, val in [("nombre", nombre), ("color", color), ("animal", animal)]:
                if val and val.lower() not in apodo.lower():
                    faltantes.append(label)
            if not faltantes:
                r.append((True, "apodo contiene nombre+color+animal", f"✓  →  '{apodo}'"))
            else:
                r.append((False, "apodo", f"Falta incluir: {', '.join(faltantes)}"))

        for row in r:
            _row(*row)
        _footer(sum(x[0] for x in r), len(r))

    # ------------------------------------------------------------------

    def check_s2_ex4(self):
        """S2-E4: Calculadora de Propina"""
        _header("SESIÓN 2 · Ejercicio 4 — Calculadora de Propina")
        r = []

        costo   = _get("costo")
        propina = _get("propina")
        total   = _get("total")

        if costo is None:
            r.append((False, "costo", "No encontrada — ejecuta tu celda primero"))
        elif not isinstance(costo, (int, float)) or isinstance(costo, bool):
            r.append((False, "costo", f"Debe ser float. ¿Usaste float(input(...))? Recibí {type(costo).__name__}"))
        else:
            r.append((True, "costo", f"float ✓  →  {costo}"))

        if propina is None:
            r.append((False, "propina", "No encontrada — usa: propina = costo * 0.10"))
        elif costo is not None:
            exp = costo * 0.10
            if _approx(propina, exp):
                r.append((True, "propina = costo * 0.10", f"✓  →  {propina}"))
            else:
                r.append((False, "propina", f"Para costo={costo}, propina debería ser {exp:.2f}, obtuve {propina}"))

        if total is None:
            r.append((False, "total", "No encontrada — usa: total = costo + propina"))
        elif costo is not None and propina is not None:
            exp = costo + propina
            if _approx(total, exp):
                r.append((True, "total = costo + propina", f"✓  →  {total}"))
            else:
                r.append((False, "total", f"Debería ser {exp:.2f}, obtuve {total}"))

        for row in r:
            _row(*row)
        _footer(sum(x[0] for x in r), len(r))

    # ------------------------------------------------------------------

    def check_s2_ex5(self):
        """S2-E5: Cuántos Meses Has Vivido"""
        _header("SESIÓN 2 · Ejercicio 5 — ¿Cuántos Meses Has Vivido?")
        r = []

        edad  = _get("edad")
        meses = _get("meses")

        if edad is None:
            r.append((False, "edad", "No encontrada — usa: edad = int(input(...))"))
        elif isinstance(edad, bool) or not isinstance(edad, int):
            r.append((False, "edad", f"Debe ser int. ¿Usaste int(input(...))? Recibí {type(edad).__name__}"))
        elif not (5 <= edad <= 110):
            r.append((False, "edad", f"Valor {edad} no parece una edad válida"))
        else:
            r.append((True, "edad", f"int ✓  →  {edad}"))

        if meses is None:
            r.append((False, "meses", "No encontrada — usa: meses = edad * 12"))
        elif edad is not None and isinstance(edad, int):
            exp = edad * 12
            if meses == exp:
                r.append((True, "meses = edad * 12", f"✓  →  {meses} meses"))
            else:
                r.append((False, "meses", f"Para {edad} años, meses debería ser {exp}, obtuve {meses}"))

        for row in r:
            _row(*row)
        _footer(sum(x[0] for x in r), len(r))

    # ------------------------------------------------------------------

    def check_s2_ex6(self):
        """S2-E6: Presentación Completa"""
        _header("SESIÓN 2 · Ejercicio 6 — Presentación Completa")
        r = []

        for vname in ["nombre", "edad", "comida", "hobby"]:
            val = _get(vname)
            if val is None:
                r.append((False, vname, "No encontrada"))
            elif str(val).strip() == "":
                r.append((False, vname, "No puede estar vacía"))
            else:
                r.append((True, vname, f"✓  →  '{val}'"))

        for bonus in ["materia", "pelicula"]:
            val = _get(bonus)
            if val is not None and str(val).strip():
                r.append((True, f"🌟 BONUS '{bonus}'", f"✓ ¡Agregaste preguntas extra!"))

        for row in r:
            _row(*row)
        _footer(sum(x[0] for x in r), len(r))

    # ------------------------------------------------------------------

    def check_s2_ex7(self):
        """S2-E7: Calculadora de Viaje"""
        _header("SESIÓN 2 · Ejercicio 7 — Calculadora de Viaje")
        r = []

        distancia        = _get("distancia")
        precio_gasolina  = _get("precio_gasolina")
        km_por_litro     = _get("km_por_litro")
        litros_necesarios = _get("litros_necesarios")
        costo_total      = _get("costo_total")

        for vname, val in [("distancia", distancia),
                           ("precio_gasolina", precio_gasolina),
                           ("km_por_litro", km_por_litro)]:
            if val is None:
                r.append((False, vname, "No encontrada — ejecuta tu celda primero"))
            elif not isinstance(val, (int, float)) or isinstance(val, bool):
                r.append((False, vname, f"Debe ser float. ¿Usaste float(input(...))?"))
            elif val <= 0:
                r.append((False, vname, f"Debe ser positivo, recibí {val}"))
            else:
                r.append((True, vname, f"float ✓  →  {val}"))

        if litros_necesarios is None:
            r.append((False, "litros_necesarios", "No encontrada — usa: litros_necesarios = distancia / km_por_litro"))
        elif distancia is not None and km_por_litro is not None and km_por_litro != 0:
            exp = distancia / km_por_litro
            if _approx(litros_necesarios, exp, tol=1e-3):
                r.append((True, "litros = distancia / km_por_litro", f"✓  →  {litros_necesarios:.2f} L"))
            else:
                r.append((False, "litros_necesarios", f"Debería ser {exp:.2f}, obtuve {litros_necesarios}"))

        if costo_total is None:
            r.append((False, "costo_total", "No encontrada — usa: costo_total = litros_necesarios * precio_gasolina"))
        elif litros_necesarios is not None and precio_gasolina is not None:
            exp = litros_necesarios * precio_gasolina
            if _approx(costo_total, exp, tol=0.01):
                r.append((True, "costo_total = litros * precio_gasolina", f"✓  →  {costo_total:.2f} soles"))
            else:
                r.append((False, "costo_total", f"Debería ser {exp:.2f}, obtuve {costo_total}"))

        for row in r:
            _row(*row)
        _footer(sum(x[0] for x in r), len(r))

    # ------------------------------------------------------------------

    def check_s2_ex8(self):
        """S2-E8: Mad Libs Peruano"""
        _header("SESIÓN 2 · Ejercicio 8 — Mad Libs Peruano")
        r = []

        for vname in ["nombre", "animal", "ciudad", "numero", "comida"]:
            val = _get(vname)
            if val is None:
                r.append((False, vname, "No encontrada"))
            elif str(val).strip() == "":
                r.append((False, vname, "No puede estar vacía"))
            else:
                r.append((True, vname, f"✓  →  '{val}'"))

        for bonus in ["adjetivo", "verbo"]:
            val = _get(bonus)
            if val is not None and str(val).strip():
                r.append((True, f"🌟 BONUS '{bonus}'", "✓ ¡Completaste la versión extendida!"))

        passed = sum(x[0] for x in r)
        for row in r:
            _row(*row)
        if passed >= 5:
            print("\n  🎉 ¡FELICITACIONES! ¡Comparte tu historia con la clase!")
        _footer(passed, len(r))

    # ------------------------------------------------------------------

    def check_s2_ex9(self):
        """S2-E9: Calculadora de IMC"""
        _header("SESIÓN 2 · Ejercicio 9 — Calculadora de IMC")
        r = []

        nombre = _get("nombre")
        peso   = _get("peso")
        altura = _get("altura")
        imc    = _get("imc")

        if nombre is None:
            r.append((False, "nombre", "No encontrada"))
        elif not isinstance(nombre, str) or nombre.strip() == "":
            r.append((False, "nombre", "Debe ser string no vacío"))
        else:
            r.append((True, "nombre", f"string ✓  →  '{nombre}'"))

        for vname, val, lo, hi in [("peso", peso, 20, 300), ("altura", altura, 0.5, 3.0)]:
            if val is None:
                r.append((False, vname, f"No encontrada — usa: {vname} = float(input(...))"))
            elif not isinstance(val, (int, float)) or isinstance(val, bool):
                r.append((False, vname, f"Debe ser float"))
            elif not (lo <= val <= hi):
                r.append((False, vname, f"Valor {val} fuera de rango ({lo}-{hi})"))
            else:
                r.append((True, vname, f"float ✓  →  {val}"))

        if imc is None:
            r.append((False, "imc", "No encontrada — usa: imc = peso / (altura ** 2)"))
        elif peso is not None and altura is not None and altura != 0:
            exp = peso / (altura ** 2)
            if _approx(imc, exp, tol=0.001):
                r.append((True, "imc = peso / (altura ** 2)", f"✓  →  {imc:.2f}"))
            else:
                r.append((False, "imc", f"Para peso={peso}, altura={altura}: IMC debería ser {exp:.2f}, obtuve {imc}"))

        for row in r:
            _row(*row)
        _footer(sum(x[0] for x in r), len(r))

    # ------------------------------------------------------------------

    def check_s2_ex10(self):
        """S2-E10: Generador de Email"""
        _header("SESIÓN 2 · Ejercicio 10 — Generador de Email")
        r = []

        nombre_u  = _get("nombre_usuario")
        apellido  = _get("apellido")
        dominio   = _get("dominio")
        email     = _get("email")

        for vname, val in [("nombre_usuario", nombre_u), ("apellido", apellido), ("dominio", dominio)]:
            if val is None:
                r.append((False, vname, "No encontrada"))
            elif not isinstance(val, str) or val.strip() == "":
                r.append((False, vname, "Debe ser string no vacío"))
            else:
                r.append((True, vname, f"string ✓  →  '{val}'"))

        if email is None:
            r.append((False, "email", "No encontrada — combina: nombre_usuario + '.' + apellido + '@' + dominio"))
        elif not isinstance(email, str):
            r.append((False, "email", "Debe ser string"))
        elif "@" not in email:
            r.append((False, "email", f"El email debe contener '@', obtuve: '{email}'"))
        elif nombre_u and apellido and dominio:
            nu = nombre_u.lower().replace(" ", "")
            ap = apellido.lower().replace(" ", "")
            dom = dominio.lower()
            email_l = email.lower()
            if nu in email_l and ap in email_l and dom in email_l:
                r.append((True, "email contiene nombre+apellido+@+dominio", f"✓  →  '{email}'"))
            else:
                r.append((False, "email", f"El email debe combinar nombre, apellido y dominio, obtuve: '{email}'"))

        for row in r:
            _row(*row)
        _footer(sum(x[0] for x in r), len(r))

    # ------------------------------------------------------------------

    def check_s2_ex11(self):
        """S2-E11: Conversor Múltiple"""
        _header("SESIÓN 2 · Ejercicio 11 — Conversor Múltiple")
        r = []

        metros    = _get("metros")
        km        = _get("kilometros")
        cm        = _get("centimetros")
        pulgadas  = _get("pulgadas")

        if metros is None:
            r.append((False, "metros", "No encontrada — usa: metros = float(input(...))"))
        elif not isinstance(metros, (int, float)) or isinstance(metros, bool):
            r.append((False, "metros", "Debe ser float"))
        elif metros <= 0:
            r.append((False, "metros", "Debe ser positivo"))
        else:
            r.append((True, "metros", f"float ✓  →  {metros}"))

        conversiones = [
            ("kilometros", km,       metros / 1000 if metros else None,    "km = metros / 1000"),
            ("centimetros", cm,      metros * 100 if metros else None,     "cm = metros * 100"),
            ("pulgadas",  pulgadas,  metros * 39.3701 if metros else None, "pulgadas = metros * 39.3701"),
        ]

        for vname, val, exp, formula in conversiones:
            if val is None:
                r.append((False, vname, f"No encontrada — usa: {formula}"))
            elif metros is not None and exp is not None and _approx(val, exp, tol=0.01):
                r.append((True, formula, f"✓  →  {val:.4f}"))
            else:
                r.append((False, vname, f"Para metros={metros}, debería ser {exp:.4f}, obtuve {val}"))

        for row in r:
            _row(*row)
        _footer(sum(x[0] for x in r), len(r))

    # ------------------------------------------------------------------

    def check_s2_ex12(self):
        """S2-E12: Mini Currículum"""
        _header("SESIÓN 2 · Ejercicio 12 — Mini Currículum")
        r = []

        required = {
            "nombre_completo": str,
            "edad":            (str, int),
            "profesion":       str,
            "habilidad1":      str,
            "habilidad2":      str,
            "meta":            str,
        }

        for vname, expected_type in required.items():
            val = _get(vname)
            if val is None:
                r.append((False, vname, "No encontrada"))
            elif not isinstance(val, expected_type):
                r.append((False, vname, f"Tipo incorrecto"))
            elif str(val).strip() == "":
                r.append((False, vname, "No puede estar vacía"))
            else:
                r.append((True, vname, f"✓  →  '{val}'"))

        for bonus in ["email_personal", "ciudad_origen"]:
            val = _get(bonus)
            if val is not None and str(val).strip():
                r.append((True, f"🌟 BONUS '{bonus}'", "✓"))

        for row in r:
            _row(*row)
        _footer(sum(x[0] for x in r), len(r))

    # =====================================================================
    # Run all at once
    # =====================================================================

    def check_all_s1(self):
        """Run all 12 Session-1 checks in one go."""
        print("\n" + "=" * 58)
        print("  VERIFICANDO SESIÓN 1 COMPLETA (12 ejercicios)")
        print("=" * 58)
        for fn in [self.check_s1_ex1, self.check_s1_ex2, self.check_s1_ex3,
                   self.check_s1_ex4, self.check_s1_ex5, self.check_s1_ex6,
                   self.check_s1_ex7, self.check_s1_ex8, self.check_s1_ex9,
                   self.check_s1_ex10, self.check_s1_ex11, self.check_s1_ex12]:
            fn()

    def check_all_s2(self):
        """Run all 12 Session-2 checks in one go."""
        print("\n" + "=" * 58)
        print("  VERIFICANDO SESIÓN 2 COMPLETA (12 ejercicios)")
        print("=" * 58)
        for fn in [self.check_s2_ex1, self.check_s2_ex2, self.check_s2_ex3,
                   self.check_s2_ex4, self.check_s2_ex5, self.check_s2_ex6,
                   self.check_s2_ex7, self.check_s2_ex8, self.check_s2_ex9,
                   self.check_s2_ex10, self.check_s2_ex11, self.check_s2_ex12]:
            fn()
