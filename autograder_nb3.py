"""
Autograder — Notebook 3: Funciones
def, parámetros, return
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


def _approx(a, b, tol=1e-6):
    try:
        return abs(float(a) - float(b)) < tol
    except (TypeError, ValueError):
        return False


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


def _call(fn, *args):
    """Call a student function safely, return (ok, result, error_msg)."""
    try:
        result = fn(*args)
        return True, result, ""
    except Exception as e:
        return False, None, str(e)


# ─────────────────────────────────────────────────────────────
# Autograder
# ─────────────────────────────────────────────────────────────

class Autograder:

    def __init__(self):
        self._earned   = 0
        self._possible = 0
        print("✅ Autograder NB3 cargado. ¡Listo para revisar tus funciones!")

    def _award(self, checks, max_pts):
        passed = sum(1 for ok, _, _ in checks if ok)
        pts    = round(max_pts * passed / len(checks)) if checks else 0
        self._earned   += pts
        self._possible += max_pts
        for row in checks:
            _row(*row)
        _footer(passed, len(checks), pts, max_pts)
        return pts

    def _check_fn(self, checks, fn_name):
        """Validate that a function exists and is callable. Returns the function or None."""
        fn = _get(fn_name)
        if fn is None:
            checks.append((False, fn_name, f"No definida — escribe: def {fn_name}(...):"))
            return None
        if not callable(fn):
            checks.append((False, fn_name, "No es una función"))
            return None
        return fn

    # ── TEORÍA ───────────────────────────────────────────────

    def check_t1(self):
        """T1 — Palabra para definir función (5 pts)"""
        _header("TEORÍA 1 — Definir funciones (5 pts)")
        r = _get("respuesta_t1")
        checks = []
        if r is None:
            checks.append((False, "respuesta_t1", "No definida — escribe: respuesta_t1 = 'letra'"))
        elif not isinstance(r, str):
            checks.append((False, "respuesta_t1", "Debe ser string"))
        elif r.strip().lower() == "a":
            checks.append((True, "respuesta_t1", "¡Correcto! def es la palabra clave para definir funciones"))
        else:
            checks.append((False, "respuesta_t1", f"Incorrecto (recibí '{r}'). Pista: son 3 letras."))
        return self._award(checks, 5)

    def check_t2(self):
        """T2 — Instrucción para devolver valor (5 pts)"""
        _header("TEORÍA 2 — Instrucción return (5 pts)")
        r = _get("respuesta_t2")
        checks = []
        if r is None:
            checks.append((False, "respuesta_t2", "No definida — escribe: respuesta_t2 = 'letra'"))
        elif not isinstance(r, str):
            checks.append((False, "respuesta_t2", "Debe ser string"))
        elif r.strip().lower() == "c":
            checks.append((True, "respuesta_t2", "¡Correcto! return devuelve un valor desde la función"))
        else:
            checks.append((False, "respuesta_t2", f"Incorrecto (recibí '{r}'). Pista: se traduce como 'devolver'."))
        return self._award(checks, 5)

    def check_t3(self):
        """T3 — Cuándo retorna None (5 pts)"""
        _header("TEORÍA 3 — Valor None (5 pts)")
        r = _get("respuesta_t3")
        checks = []
        if r is None:
            checks.append((False, "respuesta_t3", "No definida — escribe: respuesta_t3 = 'letra'"))
        elif not isinstance(r, str):
            checks.append((False, "respuesta_t3", "Debe ser string"))
        elif r.strip().lower() == "c":
            checks.append((True, "respuesta_t3", "¡Correcto! una función sin return devuelve None automáticamente"))
        else:
            checks.append((False, "respuesta_t3", f"Incorrecto (recibí '{r}'). Pista: si no hay return, ¿qué pasa?"))
        return self._award(checks, 5)

    # ── EJERCICIOS ───────────────────────────────────────────

    def check_ex1(self):
        """Ex1 — saludar() sin parámetros (6 pts)"""
        _header("EJERCICIO 1 — Función saludar() (6 pts)")
        checks = []
        fn = self._check_fn(checks, "saludar")
        if fn:
            ok, result, err = _call(fn)
            if not ok:
                checks.append((False, "saludar()", f"Error al llamar: {err}"))
            elif result == "¡Hola, mundo!":
                checks.append((True, "saludar()", f"✓ → '{result}'"))
            else:
                checks.append((False, "saludar()", f"Debe retornar '¡Hola, mundo!', obtuve '{result}'"))
        return self._award(checks, 6)

    def check_ex2(self):
        """Ex2 — saludar_persona(nombre) (6 pts)"""
        _header("EJERCICIO 2 — Función saludar_persona(nombre) (6 pts)")
        checks = []
        fn = self._check_fn(checks, "saludar_persona")
        if fn:
            CASOS = [("Ana", "¡Hola, Ana!"), ("Carlos", "¡Hola, Carlos!"), ("Sofía", "¡Hola, Sofía!")]
            for nombre, esperado in CASOS:
                ok, result, err = _call(fn, nombre)
                if not ok:
                    checks.append((False, f"saludar_persona('{nombre}')", f"Error: {err}"))
                elif isinstance(result, str) and nombre in result:
                    checks.append((True, f"saludar_persona('{nombre}')", f"✓ → '{result}'"))
                else:
                    checks.append((False, f"saludar_persona('{nombre}')", f"Debe incluir '{nombre}', obtuve '{result}'"))
        return self._award(checks, 6)

    def check_ex3(self):
        """Ex3 — calcular_area(largo, ancho) (6 pts)"""
        _header("EJERCICIO 3 — Función calcular_area(largo, ancho) (6 pts)")
        checks = []
        fn = self._check_fn(checks, "calcular_area")
        if fn:
            CASOS = [(5, 3, 15), (10, 4, 40), (7, 7, 49)]
            for largo, ancho, exp in CASOS:
                ok, result, err = _call(fn, largo, ancho)
                if not ok:
                    checks.append((False, f"calcular_area({largo}, {ancho})", f"Error: {err}"))
                elif result is not None and _approx(result, exp, tol=0.01):
                    checks.append((True, f"calcular_area({largo}, {ancho})", f"✓ → {result}"))
                else:
                    checks.append((False, f"calcular_area({largo}, {ancho})", f"Debería ser {exp}, obtuve {result}"))
        return self._award(checks, 6)

    def check_ex4(self):
        """Ex4 — celsius_a_fahrenheit(celsius) (8 pts)"""
        _header("EJERCICIO 4 — Función celsius_a_fahrenheit(celsius) (8 pts)")
        checks = []
        fn = self._check_fn(checks, "celsius_a_fahrenheit")
        if fn:
            CASOS = [(0, 32.0), (100, 212.0), (25, 77.0), (-40, -40.0)]
            for celsius, exp in CASOS:
                ok, result, err = _call(fn, celsius)
                if not ok:
                    checks.append((False, f"celsius_a_fahrenheit({celsius})", f"Error: {err}"))
                elif result is not None and _approx(result, exp, tol=0.01):
                    checks.append((True, f"celsius_a_fahrenheit({celsius})", f"✓ → {result}°F"))
                else:
                    checks.append((False, f"celsius_a_fahrenheit({celsius})", f"Debería ser {exp}°F, obtuve {result}"))
        return self._award(checks, 8)

    def check_ex5(self):
        """Ex5 — calcular_promedio(n1, n2, n3) (8 pts)"""
        _header("EJERCICIO 5 — Función calcular_promedio(n1, n2, n3) (8 pts)")
        checks = []
        fn = self._check_fn(checks, "calcular_promedio")
        if fn:
            CASOS = [(10, 15, 20, 15.0), (0, 0, 0, 0.0), (18, 16, 14, 16.0), (7, 11, 15, 11.0)]
            for n1, n2, n3, exp in CASOS:
                ok, result, err = _call(fn, n1, n2, n3)
                if not ok:
                    checks.append((False, f"calcular_promedio({n1},{n2},{n3})", f"Error: {err}"))
                elif result is not None and _approx(result, exp, tol=0.01):
                    checks.append((True, f"calcular_promedio({n1},{n2},{n3})", f"✓ → {result}"))
                else:
                    checks.append((False, f"calcular_promedio({n1},{n2},{n3})", f"Debería ser {exp}, obtuve {result}"))
        return self._award(checks, 8)

    def check_ex6(self):
        """Ex6 — es_par(numero) (8 pts)"""
        _header("EJERCICIO 6 — Función es_par(numero) (8 pts)")
        checks = []
        fn = self._check_fn(checks, "es_par")
        if fn:
            CASOS = [(4, True), (7, False), (0, True), (13, False), (100, True)]
            for num, exp in CASOS:
                ok, result, err = _call(fn, num)
                if not ok:
                    checks.append((False, f"es_par({num})", f"Error: {err}"))
                elif result is exp or result == exp:
                    checks.append((True, f"es_par({num})", f"✓ → {result}"))
                else:
                    checks.append((False, f"es_par({num})", f"Debería ser {exp}, obtuve {result}"))
        return self._award(checks, 8)

    def check_ex7(self):
        """Ex7 — contar_vocales(texto) (9 pts)"""
        _header("EJERCICIO 7 — Función contar_vocales(texto) (9 pts)")
        checks = []
        fn = self._check_fn(checks, "contar_vocales")
        VOCALES = set("aeiouáéíóúAEIOUÁÉÍÓÚ")
        if fn:
            CASOS = [
                ("hola",    2),
                ("Python",  1),
                ("murciélago", 5),
                ("bcdfg",   0),
                ("AEIOU",   5),
            ]
            for texto, exp in CASOS:
                ok, result, err = _call(fn, texto)
                if not ok:
                    checks.append((False, f"contar_vocales('{texto}')", f"Error: {err}"))
                elif result == exp:
                    checks.append((True, f"contar_vocales('{texto}')", f"✓ → {result}"))
                else:
                    checks.append((False, f"contar_vocales('{texto}')", f"Debería ser {exp}, obtuve {result}"))
        return self._award(checks, 9)

    def check_ex8(self):
        """Ex8 — clasificar_nota(nota) (9 pts)"""
        _header("EJERCICIO 8 — Función clasificar_nota(nota) (9 pts)")
        checks = []
        fn = self._check_fn(checks, "clasificar_nota")
        if fn:
            CASOS = [
                (20, "sobresaliente"),
                (18, "sobresaliente"),
                (15, "bueno"),
                (14, "bueno"),
                (13, "aprobado"),
                (11, "aprobado"),
                (10, "desaprobado"),
                (0,  "desaprobado"),
            ]
            for nota, exp in CASOS:
                ok, result, err = _call(fn, nota)
                if not ok:
                    checks.append((False, f"clasificar_nota({nota})", f"Error: {err}"))
                elif isinstance(result, str) and result.strip().lower() == exp:
                    checks.append((True, f"clasificar_nota({nota})", f"✓ → '{result}'"))
                else:
                    checks.append((False, f"clasificar_nota({nota})", f"Para nota={nota} debería ser '{exp.title()}', obtuve '{result}'"))
        return self._award(checks, 9)

    def check_ex9(self):
        """Ex9 — calcular_factorial(n) (9 pts)"""
        _header("EJERCICIO 9 — Función calcular_factorial(n) (9 pts)")
        checks = []
        fn = self._check_fn(checks, "calcular_factorial")
        if fn:
            CASOS = [(0, 1), (1, 1), (5, 120), (6, 720), (10, 3628800)]
            for n, exp in CASOS:
                ok, result, err = _call(fn, n)
                if not ok:
                    checks.append((False, f"calcular_factorial({n})", f"Error: {err}"))
                elif result == exp:
                    checks.append((True, f"calcular_factorial({n})", f"✓ → {result}"))
                else:
                    checks.append((False, f"calcular_factorial({n})", f"{n}! debería ser {exp}, obtuve {result}"))
        return self._award(checks, 9)

    def check_ex10(self):
        """Ex10 — es_palindromo(palabra) (16 pts)"""
        _header("EJERCICIO 10 — Función es_palindromo(palabra) (16 pts)")
        checks = []
        fn = self._check_fn(checks, "es_palindromo")
        if fn:
            CASOS = [
                ("ana",      True),
                ("radar",    True),
                ("level",    True),
                ("reconocer", True),
                ("hola",     False),
                ("python",   False),
                ("codigo",   False),
                ("a",        True),
            ]
            for palabra, exp in CASOS:
                ok, result, err = _call(fn, palabra)
                if not ok:
                    checks.append((False, f"es_palindromo('{palabra}')", f"Error: {err}"))
                elif result is exp or result == exp:
                    checks.append((True, f"es_palindromo('{palabra}')", f"✓ → {result}"))
                else:
                    checks.append((False, f"es_palindromo('{palabra}')", f"Debería ser {exp}, obtuve {result}"))
        return self._award(checks, 16)

    # ── RESUMEN FINAL ─────────────────────────────────────────

    def resumen(self):
        print("\n" + "═" * 60)
        print("  RESUMEN FINAL — Notebook 3: Funciones")
        print("═" * 60)
        pct    = round(self._earned / self._possible * 100) if self._possible else 0
        filled = "█" * round(30 * pct / 100)
        empty  = "░" * (30 - len(filled))
        print(f"\n  Puntaje: {self._earned}/{self._possible} pts  ({pct}%)")
        print(f"  [{filled}{empty}]")
        if pct >= 90:
            print("\n  🌟 ¡EXCELENTE! ¡Dominas las funciones!")
        elif pct >= 70:
            print("\n  👍 ¡Buen trabajo! Repasa los ❌ para mejorar.")
        elif pct >= 50:
            print("\n  📚 Vas por buen camino. ¡Sigue practicando!")
        else:
            print("\n  💪 ¡No te rindas! Repasa la teoría e inténtalo de nuevo.")
        print(f"\n{'═' * 60}\n")
