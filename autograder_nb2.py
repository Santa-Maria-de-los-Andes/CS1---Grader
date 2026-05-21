"""
Autograder — Notebook 2: Control de Flujo
if, if/else, if/elif/else, for
100 puntos: 15 teoría + 85 ejercicios
"""

# ─────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────

def _get(name):
    try:
        import __main__
        return getattr(__main__, name, None)
    except Exception:
        return None


def _header(title):
    print(f"\n{'═' * 60}")
    print(f"  {title}")
    print(f"{'═' * 60}")


def _row(ok, label, msg):
    print(f"  {'✅' if ok else '❌'} {label}: {msg}")


def _footer(passed, total, pts, max_pts):
    bar = "█" * passed + "░" * (total - passed)
    print(f"\n  Checks: {passed}/{total}  [{bar}]")
    print(f"  Puntos: {pts}/{max_pts}")
    if pts == max_pts:
        print("  ⭐ ¡Perfecto!")
    elif pts > 0:
        print("  👍 Revisa los ❌ para subir tu puntaje.")
    else:
        print("  💪 ¡Sigue intentando! Relee las instrucciones.")
    print(f"{'═' * 60}\n")


# ─────────────────────────────────────────────────────────────
# Autograder
# ─────────────────────────────────────────────────────────────

class Autograder:

    def __init__(self):
        self._earned   = 0
        self._possible = 0
        print("✅ Autograder NB2 cargado. ¡Listo para revisar tus respuestas!")

    def _award(self, checks, max_pts):
        passed = sum(1 for ok, _, _ in checks if ok)
        pts    = round(max_pts * passed / len(checks)) if checks else 0
        self._earned   += pts
        self._possible += max_pts
        for row in checks:
            _row(*row)
        _footer(passed, len(checks), pts, max_pts)
        return pts

    # ── TEORÍA ───────────────────────────────────────────────

    def check_t1(self):
        """T1 — Operador 'igual a' (5 pts)"""
        _header("TEORÍA 1 — Operadores de comparación (5 pts)")
        r = _get("respuesta_t1")
        checks = []
        if r is None:
            checks.append((False, "respuesta_t1", "No definida — escribe: respuesta_t1 = 'letra'"))
        elif not isinstance(r, str):
            checks.append((False, "respuesta_t1", "Debe ser string"))
        elif r.strip().lower() == "b":
            checks.append((True, "respuesta_t1", "¡Correcto! == compara dos valores (= solo asigna)"))
        else:
            checks.append((False, "respuesta_t1", f"Incorrecto (recibí '{r}'). Pista: usamos dos signos iguales."))
        return self._award(checks, 5)

    def check_t2(self):
        """T2 — Alternativa en if (5 pts)"""
        _header("TEORÍA 2 — Palabra 'else' (5 pts)")
        r = _get("respuesta_t2")
        checks = []
        if r is None:
            checks.append((False, "respuesta_t2", "No definida — escribe: respuesta_t2 = 'letra'"))
        elif not isinstance(r, str):
            checks.append((False, "respuesta_t2", "Debe ser string"))
        elif r.strip().lower() == "c":
            checks.append((True, "respuesta_t2", "¡Correcto! else es el bloque alternativo del if"))
        else:
            checks.append((False, "respuesta_t2", f"Incorrecto (recibí '{r}'). Pista: se traduce como 'si no'."))
        return self._award(checks, 5)

    def check_t3(self):
        """T3 — range(5) genera (5 pts)"""
        _header("TEORÍA 3 — Función range() (5 pts)")
        r = _get("respuesta_t3")
        checks = []
        if r is None:
            checks.append((False, "respuesta_t3", "No definida — escribe: respuesta_t3 = 'letra'"))
        elif not isinstance(r, str):
            checks.append((False, "respuesta_t3", "Debe ser string"))
        elif r.strip().lower() == "a":
            checks.append((True, "respuesta_t3", "¡Correcto! range(5) genera 0, 1, 2, 3, 4 (empieza en 0)"))
        else:
            checks.append((False, "respuesta_t3", f"Incorrecto (recibí '{r}'). Pista: Python empieza a contar desde 0."))
        return self._award(checks, 5)

    # ── EJERCICIOS ───────────────────────────────────────────

    def check_ex1(self):
        """Ex1 — Positivo, negativo o cero (6 pts)"""
        _header("EJERCICIO 1 — Positivo, negativo o cero (6 pts)")
        checks = []
        numero    = _get("numero")
        resultado = _get("resultado")

        if numero is None:
            checks.append((False, "numero", "No definida"))
        elif not isinstance(numero, (int, float)) or isinstance(numero, bool):
            checks.append((False, "numero", "Debe ser número"))
        else:
            checks.append((True, "numero", f"número ✓ → {numero}"))

        if resultado is None:
            checks.append((False, "resultado", "No definida — debe ser 'positivo', 'negativo' o 'cero'"))
        elif not isinstance(resultado, str):
            checks.append((False, "resultado", "Debe ser str"))
        elif numero is not None:
            if numero > 0:
                exp = "positivo"
            elif numero < 0:
                exp = "negativo"
            else:
                exp = "cero"
            if resultado.strip().lower() == exp:
                checks.append((True, f"resultado para numero={numero}", f"✓ → '{resultado}'"))
            else:
                checks.append((False, "resultado", f"Para numero={numero} debería ser '{exp}', obtuve '{resultado}'"))

        return self._award(checks, 6)

    def check_ex2(self):
        """Ex2 — Par o impar (6 pts)"""
        _header("EJERCICIO 2 — Par o impar (6 pts)")
        checks = []
        numero    = _get("numero")
        resultado = _get("resultado")

        if numero is None:
            checks.append((False, "numero", "No definida"))
        elif isinstance(numero, bool) or not isinstance(numero, int):
            checks.append((False, "numero", "Debe ser int (entero)"))
        else:
            checks.append((True, "numero", f"int ✓ → {numero}"))

        if resultado is None:
            checks.append((False, "resultado", "No definida — debe ser 'par' o 'impar'"))
        elif not isinstance(resultado, str):
            checks.append((False, "resultado", "Debe ser str"))
        elif numero is not None and isinstance(numero, int):
            exp = "par" if numero % 2 == 0 else "impar"
            if resultado.strip().lower() == exp:
                checks.append((True, f"resultado para numero={numero}", f"✓ → '{resultado}'"))
            else:
                checks.append((False, "resultado", f"Para numero={numero} debería ser '{exp}', obtuve '{resultado}'"))

        return self._award(checks, 6)

    def check_ex3(self):
        """Ex3 — Semáforo (6 pts)"""
        _header("EJERCICIO 3 — Semáforo (6 pts)")
        checks = []
        color  = _get("color")
        accion = _get("accion")

        SEMAFORO = {
            "rojo":     "detente",
            "amarillo": "precaución",
            "verde":    "avanza",
        }

        if color is None:
            checks.append((False, "color", "No definida — debe ser 'rojo', 'amarillo' o 'verde'"))
        elif not isinstance(color, str):
            checks.append((False, "color", "Debe ser str"))
        elif color.strip().lower() not in SEMAFORO:
            checks.append((False, "color", f"Valor '{color}' no reconocido. Usa: 'rojo', 'amarillo' o 'verde'"))
        else:
            checks.append((True, "color", f"str ✓ → '{color}'"))

        if accion is None:
            checks.append((False, "accion", "No definida"))
        elif not isinstance(accion, str):
            checks.append((False, "accion", "Debe ser str"))
        elif color is not None and color.strip().lower() in SEMAFORO:
            exp = SEMAFORO[color.strip().lower()]
            if accion.strip().lower() == exp:
                checks.append((True, f"accion para color='{color}'", f"✓ → '{accion}'"))
            else:
                checks.append((False, "accion", f"Para color='{color}' debería ser '{exp}', obtuve '{accion}'"))

        return self._award(checks, 6)

    def check_ex4(self):
        """Ex4 — Suma con for (8 pts)"""
        _header("EJERCICIO 4 — Suma con for (8 pts)")
        checks = []
        n    = _get("n")
        suma = _get("suma")

        if n is None:
            checks.append((False, "n", "No definida"))
        elif isinstance(n, bool) or not isinstance(n, int):
            checks.append((False, "n", "Debe ser int"))
        elif n <= 0:
            checks.append((False, "n", "Debe ser positivo"))
        else:
            checks.append((True, "n", f"int ✓ → {n}"))

        if suma is None:
            checks.append((False, "suma", "No definida — usa un for loop para sumar de 1 a n"))
        elif n is not None and isinstance(n, int) and n > 0:
            exp = n * (n + 1) // 2
            if suma == exp:
                checks.append((True, f"suma de 1 a {n}", f"✓ → {suma}"))
            else:
                checks.append((False, "suma", f"Para n={n} debería ser {exp}, obtuve {suma}"))

        return self._award(checks, 8)

    def check_ex5(self):
        """Ex5 — Calificación por letra (8 pts)"""
        _header("EJERCICIO 5 — Calificación por letra (8 pts)")
        checks = []
        nota_num  = _get("nota_num")
        categoria = _get("categoria")

        CATEGORIAS = [
            (18, 20, "sobresaliente"),
            (14, 17, "bueno"),
            (11, 13, "aprobado"),
            (0,  10, "desaprobado"),
        ]

        if nota_num is None:
            checks.append((False, "nota_num", "No definida — nota del 0 al 20"))
        elif not isinstance(nota_num, (int, float)) or isinstance(nota_num, bool):
            checks.append((False, "nota_num", "Debe ser número"))
        elif not (0 <= nota_num <= 20):
            checks.append((False, "nota_num", f"Fuera del rango 0–20 (obtuve {nota_num})"))
        else:
            checks.append((True, "nota_num", f"número ✓ → {nota_num}"))

        if categoria is None:
            checks.append((False, "categoria", "No definida — debe ser 'Sobresaliente', 'Bueno', 'Aprobado' o 'Desaprobado'"))
        elif not isinstance(categoria, str):
            checks.append((False, "categoria", "Debe ser str"))
        elif nota_num is not None and isinstance(nota_num, (int, float)):
            exp = ""
            for lo, hi, cat in CATEGORIAS:
                if lo <= nota_num <= hi:
                    exp = cat
                    break
            if categoria.strip().lower() == exp:
                checks.append((True, f"categoria para nota={nota_num}", f"✓ → '{categoria}'"))
            else:
                checks.append((False, "categoria", f"Para nota={nota_num} debería ser '{exp.title()}', obtuve '{categoria}'"))

        return self._award(checks, 8)

    def check_ex6(self):
        """Ex6 — Contar números pares (8 pts)"""
        _header("EJERCICIO 6 — Contar pares con for (8 pts)")
        checks = []
        limite         = _get("limite")
        contador_pares = _get("contador_pares")

        if limite is None:
            checks.append((False, "limite", "No definida — define hasta qué número contar"))
        elif isinstance(limite, bool) or not isinstance(limite, int):
            checks.append((False, "limite", "Debe ser int"))
        elif limite <= 0:
            checks.append((False, "limite", "Debe ser positivo"))
        else:
            checks.append((True, "limite", f"int ✓ → {limite}"))

        if contador_pares is None:
            checks.append((False, "contador_pares", "No definida — usa for + if para contar pares del 1 al limite"))
        elif isinstance(contador_pares, bool) or not isinstance(contador_pares, int):
            checks.append((False, "contador_pares", "Debe ser int"))
        elif limite is not None and isinstance(limite, int) and limite > 0:
            exp = limite // 2
            if contador_pares == exp:
                checks.append((True, f"contador_pares del 1 al {limite}", f"✓ → {contador_pares}"))
            else:
                checks.append((False, "contador_pares", f"Para limite={limite} debería ser {exp}, obtuve {contador_pares}"))

        return self._award(checks, 8)

    def check_ex7(self):
        """Ex7 — Factorial (9 pts)"""
        _header("EJERCICIO 7 — Factorial con for (9 pts)")
        checks = []
        n        = _get("n")
        factorial = _get("factorial")

        if n is None:
            checks.append((False, "n", "No definida"))
        elif isinstance(n, bool) or not isinstance(n, int):
            checks.append((False, "n", "Debe ser int"))
        elif not (0 <= n <= 12):
            checks.append((False, "n", f"Usa un valor entre 0 y 12 para evitar números muy grandes"))
        else:
            checks.append((True, "n", f"int ✓ → {n}"))

        if factorial is None:
            checks.append((False, "factorial", "No definida — multiplica con un for loop"))
        elif isinstance(factorial, bool) or not isinstance(factorial, int):
            checks.append((False, "factorial", "Debe ser int"))
        elif n is not None and isinstance(n, int) and 0 <= n <= 12:
            exp = 1
            for i in range(1, n + 1):
                exp *= i
            if factorial == exp:
                checks.append((True, f"{n}! (factorial)", f"✓ → {factorial}"))
            else:
                checks.append((False, "factorial", f"{n}! debería ser {exp}, obtuve {factorial}"))

        return self._award(checks, 9)

    def check_ex8(self):
        """Ex8 — FizzBuzz (9 pts)"""
        _header("EJERCICIO 8 — FizzBuzz con for (9 pts)")
        checks = []
        n                 = _get("n")
        resultado_fizzbuzz = _get("resultado_fizzbuzz")

        if n is None:
            checks.append((False, "n", "No definida — define n (ej: n = 15)"))
        elif isinstance(n, bool) or not isinstance(n, int):
            checks.append((False, "n", "Debe ser int"))
        elif not (1 <= n <= 50):
            checks.append((False, "n", "Usa un valor entre 1 y 50"))
        else:
            checks.append((True, "n", f"int ✓ → {n}"))

        if resultado_fizzbuzz is None:
            checks.append((False, "resultado_fizzbuzz", "No definida — crea una lista con los resultados del FizzBuzz"))
        elif not isinstance(resultado_fizzbuzz, list):
            checks.append((False, "resultado_fizzbuzz", "Debe ser una lista []"))
        elif n is not None and isinstance(n, int) and 1 <= n <= 50:
            exp = []
            for i in range(1, n + 1):
                if i % 3 == 0 and i % 5 == 0:
                    exp.append("FizzBuzz")
                elif i % 3 == 0:
                    exp.append("Fizz")
                elif i % 5 == 0:
                    exp.append("Buzz")
                else:
                    exp.append(str(i))
            if len(resultado_fizzbuzz) != len(exp):
                checks.append((False, "resultado_fizzbuzz", f"Debe tener {len(exp)} elementos, tiene {len(resultado_fizzbuzz)}"))
            else:
                errores = [(i + 1, exp[i], resultado_fizzbuzz[i])
                           for i in range(len(exp)) if str(resultado_fizzbuzz[i]) != exp[i]]
                if not errores:
                    checks.append((True, "resultado_fizzbuzz completo y correcto", f"✓ ({len(exp)} elementos)"))
                else:
                    pos, e, o = errores[0]
                    checks.append((False, "resultado_fizzbuzz", f"Error en posición {pos}: esperaba '{e}', obtuve '{o}'"))

        return self._award(checks, 9)

    def check_ex9(self):
        """Ex9 — Contar vocales (9 pts)"""
        _header("EJERCICIO 9 — Contar vocales con for (9 pts)")
        checks = []
        texto            = _get("texto")
        contador_vocales = _get("contador_vocales")

        VOCALES = set("aeiouáéíóúAEIOUÁÉÍÓÚ")

        if texto is None:
            checks.append((False, "texto", "No definida — define un texto (str)"))
        elif not isinstance(texto, str) or texto.strip() == "":
            checks.append((False, "texto", "Debe ser str no vacío"))
        else:
            checks.append((True, "texto", f"str ✓ → '{texto[:40]}'"))

        if contador_vocales is None:
            checks.append((False, "contador_vocales", "No definida — usa for + if para contar vocales"))
        elif isinstance(contador_vocales, bool) or not isinstance(contador_vocales, int):
            checks.append((False, "contador_vocales", "Debe ser int"))
        elif texto is not None and isinstance(texto, str):
            exp = sum(1 for c in texto if c in VOCALES)
            if contador_vocales == exp:
                checks.append((True, f"contador_vocales en '{texto[:30]}'", f"✓ → {contador_vocales}"))
            else:
                checks.append((False, "contador_vocales", f"Para texto='{texto[:30]}' debería ser {exp}, obtuve {contador_vocales}"))

        return self._award(checks, 9)

    def check_ex10(self):
        """Ex10 — Números especiales (16 pts)"""
        _header("EJERCICIO 10 — Números especiales (16 pts)")
        checks = []
        n                = _get("n")
        contador_triple  = _get("contador_triple")
        resultado_esp    = _get("resultado_especial")

        if n is None:
            checks.append((False, "n", "No definida — define n (ej: n = 20)"))
        elif isinstance(n, bool) or not isinstance(n, int):
            checks.append((False, "n", "Debe ser int"))
        elif not (5 <= n <= 100):
            checks.append((False, "n", "Usa un valor entre 5 y 100"))
        else:
            checks.append((True, "n", f"int ✓ → {n}"))

        if n is not None and isinstance(n, int) and 5 <= n <= 100:
            exp_triple = sum(1 for i in range(1, n + 1) if i % 3 == 0)
            exp_lista  = []
            for i in range(1, n + 1):
                if i % 3 == 0 and i % 5 == 0:
                    exp_lista.append("Triple y Quinto")
                elif i % 3 == 0:
                    exp_lista.append("Triple")
                elif i % 5 == 0:
                    exp_lista.append("Quinto")
                else:
                    exp_lista.append(str(i))

            if contador_triple is None:
                checks.append((False, "contador_triple", "No definida — cuenta cuántos múltiplos de 3 hay del 1 al n"))
            elif isinstance(contador_triple, bool) or not isinstance(contador_triple, int):
                checks.append((False, "contador_triple", "Debe ser int"))
            elif contador_triple == exp_triple:
                checks.append((True, f"contador_triple para n={n}", f"✓ → {contador_triple}"))
            else:
                checks.append((False, "contador_triple", f"Para n={n} debería ser {exp_triple}, obtuve {contador_triple}"))

            if resultado_especial := resultado_esp:
                if not isinstance(resultado_especial, list):
                    checks.append((False, "resultado_especial", "Debe ser una lista []"))
                elif len(resultado_especial) != len(exp_lista):
                    checks.append((False, "resultado_especial", f"Debe tener {len(exp_lista)} elementos, tiene {len(resultado_especial)}"))
                else:
                    errores = [(i + 1, exp_lista[i], resultado_especial[i])
                               for i in range(len(exp_lista)) if str(resultado_especial[i]) != exp_lista[i]]
                    if not errores:
                        checks.append((True, "resultado_especial completo y correcto", f"✓ ({len(exp_lista)} elementos)"))
                    else:
                        pos, e, o = errores[0]
                        checks.append((False, "resultado_especial", f"Error en posición {pos}: esperaba '{e}', obtuve '{o}'"))
            else:
                checks.append((False, "resultado_especial", "No definida — crea una lista con los resultados"))
        else:
            for vname in ["contador_triple", "resultado_especial"]:
                checks.append((False, vname, "Define primero 'n'"))

        return self._award(checks, 16)

    # ── RESUMEN FINAL ─────────────────────────────────────────

    def resumen(self):
        print("\n" + "═" * 60)
        print("  RESUMEN FINAL — Notebook 2: Control de Flujo")
        print("═" * 60)
        pct    = round(self._earned / self._possible * 100) if self._possible else 0
        filled = "█" * round(30 * pct / 100)
        empty  = "░" * (30 - len(filled))
        print(f"\n  Puntaje: {self._earned}/{self._possible} pts  ({pct}%)")
        print(f"  [{filled}{empty}]")
        if pct >= 90:
            print("\n  🌟 ¡EXCELENTE! ¡Dominas el control de flujo!")
        elif pct >= 70:
            print("\n  👍 ¡Buen trabajo! Repasa los ❌ para mejorar.")
        elif pct >= 50:
            print("\n  📚 Vas por buen camino. ¡Sigue practicando!")
        else:
            print("\n  💪 ¡No te rindas! Repasa la teoría e inténtalo de nuevo.")
        print(f"\n{'═' * 60}\n")
