"""
Autograder — Notebook 1: Fundamentos
Variables · Tipos · Aritmética · print() · f-strings
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
    print(f"\n{'═' * 62}")
    print(f"  {title}")
    print(f"{'═' * 62}")


def _row(ok, label, msg):
    icon = "✅" if ok else "❌"
    print(f"  {icon} {label}: {msg}")


def _footer(passed, total):
    bar = "█" * passed + "░" * (total - passed)
    print(f"\n  Checks: {passed}/{total}  [{bar}]")


# ─────────────────────────────────────────────────────────────
# Autograder
# ─────────────────────────────────────────────────────────────

class Autograder:

    def __init__(self):
        self._scores = {}   # key → (earned, possible) — overwritten on re-run
        print("✅ Autograder NB1 listo. ¡Puedes empezar!")

    def _nombre(self):
        n = _get("nombre")
        if isinstance(n, str) and n.strip() and n.strip() not in ("?", ""):
            return n.strip()
        return "estudiante"

    def _show_progress(self, pts, max_pts):
        earned   = sum(e for e, _ in self._scores.values())
        possible = sum(p for _, p in self._scores.values())
        pct      = round(earned / possible * 100) if possible else 0
        n        = self._nombre()
        filled   = round(20 * pct / 100)
        bar      = "█" * filled + "░" * (20 - filled)

        ej_icon = "⭐" if pts == max_pts else ("👍" if pts > 0 else "💪")
        if pct >= 90:
            cheer = "¡Excelente trabajo!"
        elif pct >= 75:
            cheer = "¡Muy bien!"
        elif pct >= 55:
            cheer = "¡Buen comienzo!"
        else:
            cheer = "¡Tú puedes!"

        print(f"  {ej_icon} Este ejercicio: {pts}/{max_pts} pts")
        print(f"  Total acumulado: {earned}/{possible} pts  ({pct}%)  [{bar}]")
        print(f"  {cheer} {n}.")
        print(f"{'═' * 62}\n")

    def _award(self, key, checks, max_pts):
        passed = sum(1 for ok, _, _ in checks if ok)
        pts    = round(max_pts * passed / len(checks)) if checks else 0
        self._scores[key] = (pts, max_pts)
        for row in checks:
            _row(*row)
        _footer(passed, len(checks))
        self._show_progress(pts, max_pts)
        return pts

    # ── MINI-A — Variables básicas ────────────────────────────

    def check_mini_a(self):
        """Mini-A — Mi Perfil: nombre, edad, ciudad (6 pts)"""
        _header("CHECKPOINT A — Mi Perfil (6 pts)")
        checks = []
        nombre = _get("nombre")
        edad   = _get("edad")
        ciudad = _get("ciudad")

        if nombre is None:
            checks.append((False, "nombre", "No definida"))
        elif not isinstance(nombre, str) or nombre.strip() in ("", "?"):
            checks.append((False, "nombre", f"Debe ser str con tu nombre real, recibí '{nombre}'"))
        else:
            checks.append((True, "nombre", f"str ✓  '{nombre}'"))

        if edad is None:
            checks.append((False, "edad", "No definida — usa entero sin comillas, ej: edad = 15"))
        elif isinstance(edad, bool) or not isinstance(edad, int):
            checks.append((False, "edad", f"Debe ser int (sin comillas), recibí {type(edad).__name__}"))
        elif not (5 <= edad <= 110):
            checks.append((False, "edad", f"Valor {edad} fuera de rango (5–110)"))
        else:
            checks.append((True, "edad", f"int ✓  {edad}"))

        if ciudad is None:
            checks.append((False, "ciudad", "No definida"))
        elif not isinstance(ciudad, str) or ciudad.strip() in ("", "?"):
            checks.append((False, "ciudad", "Debe ser str con tu ciudad real"))
        else:
            checks.append((True, "ciudad", f"str ✓  '{ciudad}'"))

        return self._award("mini_a", checks, 6)

    # ── T1 — Tipo int ─────────────────────────────────────────

    def check_t1(self):
        """T1 — ¿Tipo de edad = 15? (4 pts)"""
        _header("PREGUNTA T1 — Tipos de datos (4 pts)")
        r = _get("respuesta_t1")
        checks = []
        if r is None:
            checks.append((False, "respuesta_t1", "No definida — escribe: respuesta_t1 = 'letra'"))
        elif not isinstance(r, str):
            checks.append((False, "respuesta_t1", "Debe ser str, ej: respuesta_t1 = 'c'"))
        elif r.strip().lower() == "c":
            checks.append((True, "respuesta_t1", "¡Correcto! edad = 15 → int (número entero)"))
        else:
            checks.append((False, "respuesta_t1", f"Incorrecto ('{r}'). Pista: 15 no tiene punto decimal."))
        return self._award("t1", checks, 4)

    # ── MINI-B — Tipos correctos ──────────────────────────────

    def check_mini_b(self):
        """Mini-B — temperatura (float), piso (int), barrio (str) (6 pts)"""
        _header("CHECKPOINT B — Tipos correctos (6 pts)")
        checks = []
        temp = _get("temperatura")
        piso = _get("piso")
        bar  = _get("barrio")

        if temp is None:
            checks.append((False, "temperatura", "No definida — usa float con punto decimal, ej: 36.6"))
        elif not isinstance(temp, float):
            checks.append((False, "temperatura", f"Debe ser float (decimal), recibí {type(temp).__name__}. Ej: 36.6"))
        else:
            checks.append((True, "temperatura", f"float ✓  {temp}"))

        if piso is None:
            checks.append((False, "piso", "No definida — usa int (número entero), ej: 3"))
        elif isinstance(piso, bool) or not isinstance(piso, int):
            checks.append((False, "piso", f"Debe ser int (sin decimal), recibí {type(piso).__name__}"))
        else:
            checks.append((True, "piso", f"int ✓  {piso}"))

        if bar is None:
            checks.append((False, "barrio", "No definida — usa str entre comillas, ej: 'Santa Maria'"))
        elif not isinstance(bar, str) or bar.strip() in ("", "?"):
            checks.append((False, "barrio", "Debe ser str entre comillas"))
        else:
            checks.append((True, "barrio", f"str ✓  '{bar}'"))

        return self._award("mini_b", checks, 6)

    # ── T2 — Función print ────────────────────────────────────

    def check_t2(self):
        """T2 — ¿Qué función muestra texto? (4 pts)"""
        _header("PREGUNTA T2 — Función print (4 pts)")
        r = _get("respuesta_t2")
        checks = []
        if r is None:
            checks.append((False, "respuesta_t2", "No definida — escribe: respuesta_t2 = 'letra'"))
        elif not isinstance(r, str):
            checks.append((False, "respuesta_t2", "Debe ser str, ej: respuesta_t2 = 'd'"))
        elif r.strip().lower() == "d":
            checks.append((True, "respuesta_t2", "¡Correcto! print() muestra texto en pantalla"))
        else:
            checks.append((False, "respuesta_t2", f"Incorrecto ('{r}'). Pista: ¿qué función usamos en cada ejemplo?"))
        return self._award("t2", checks, 4)

    # ── T3 — Tipo float ───────────────────────────────────────

    def check_t3(self):
        """T3 — ¿Tipo de precio = 9.99? (4 pts)"""
        _header("PREGUNTA T3 — Tipo float (4 pts)")
        r = _get("respuesta_t3")
        checks = []
        if r is None:
            checks.append((False, "respuesta_t3", "No definida — escribe: respuesta_t3 = 'letra'"))
        elif not isinstance(r, str):
            checks.append((False, "respuesta_t3", "Debe ser str"))
        elif r.strip().lower() == "a":
            checks.append((True, "respuesta_t3", "¡Correcto! 9.99 tiene punto decimal → float"))
        else:
            checks.append((False, "respuesta_t3", f"Incorrecto ('{r}'). Pista: ¿tiene punto decimal?"))
        return self._award("t3", checks, 4)

    # ── MINI-D — f-string presentación ───────────────────────

    def check_mini_d(self):
        """Mini-D — presentacion con f-string (6 pts)"""
        _header("CHECKPOINT D — Presentación con f-string (6 pts)")
        checks = []
        nombre       = _get("nombre")
        ciudad       = _get("ciudad")
        presentacion = _get("presentacion")

        if not isinstance(nombre, str) or nombre.strip() in ("", "?"):
            checks.append((False, "nombre", "No definida o vacía — ¿completaste el Checkpoint A?"))
        else:
            checks.append((True, "nombre", f"str ✓  '{nombre}'"))

        if not isinstance(ciudad, str) or ciudad.strip() in ("", "?"):
            checks.append((False, "ciudad", "No definida o vacía — ¿completaste el Checkpoint A?"))
        else:
            checks.append((True, "ciudad", f"str ✓  '{ciudad}'"))

        if presentacion is None:
            checks.append((False, "presentacion", "No definida — crea la variable usando f\"...{nombre}...{ciudad}...\""))
        elif not isinstance(presentacion, str) or presentacion.strip() in ("", "?"):
            checks.append((False, "presentacion", "Debe ser un f-string con tu mensaje real"))
        else:
            n = nombre.strip().lower() if isinstance(nombre, str) else ""
            c = ciudad.strip().lower() if isinstance(ciudad, str) else ""
            p = presentacion.lower()
            falt = []
            if n and n not in p:
                falt.append("nombre")
            if c and c not in p:
                falt.append("ciudad")
            if not falt:
                checks.append((True, "presentacion incluye nombre y ciudad", f"✓  '{presentacion[:60]}'"))
            else:
                checks.append((False, "presentacion", f"Falta incluir: {', '.join(falt)}"))

        return self._award("mini_d", checks, 6)

    # ── MINI-C — La Lonchera ──────────────────────────────────

    def check_mini_c(self):
        """Mini-C — La Lonchera: suma de precios (6 pts)"""
        _header("CHECKPOINT C — La Lonchera (6 pts)")
        checks = []
        ps = _get("precio_sandwich")
        pj = _get("precio_jugo")
        pf = _get("precio_fruta")
        tl = _get("total_lonchera")

        for vname, val in [("precio_sandwich", ps), ("precio_jugo", pj), ("precio_fruta", pf)]:
            if val is None:
                checks.append((False, vname, "No definida"))
            elif not isinstance(val, (int, float)) or isinstance(val, bool):
                checks.append((False, vname, "Debe ser número"))
            elif val <= 0:
                checks.append((False, vname, "Debe ser positivo"))
            else:
                checks.append((True, vname, f"✓  {val}"))

        all_ok = all(
            isinstance(v, (int, float)) and not isinstance(v, bool) and v > 0
            for v in [ps, pj, pf] if v is not None
        )

        if tl is None:
            checks.append((False, "total_lonchera",
                           "No definida — suma: total_lonchera = precio_sandwich + precio_jugo + precio_fruta"))
        elif ps is not None and pj is not None and pf is not None and all_ok:
            exp = ps + pj + pf
            if _approx(tl, exp, tol=0.01):
                checks.append((True, "total_lonchera = suma correcta", f"✓  {tl:.2f}"))
            else:
                checks.append((False, "total_lonchera", f"Debería ser {exp:.2f}, obtuve {tl}"))
        else:
            checks.append((False, "total_lonchera", "Define primero los tres precios con valores positivos"))

        return self._award("mini_c", checks, 6)

    # ── EX 1 — Temperatura + f-string ────────────────────────

    def check_ex1(self):
        """Ex1 — Conversión Celsius → Fahrenheit (6 pts)"""
        _header("EJERCICIO 1 — Conversión de Temperatura (6 pts)")
        checks = []
        celsius    = _get("celsius")
        fahrenheit = _get("fahrenheit")

        if celsius is None:
            checks.append((False, "celsius", "No definida"))
        elif not isinstance(celsius, (int, float)) or isinstance(celsius, bool):
            checks.append((False, "celsius", "Debe ser número"))
        else:
            checks.append((True, "celsius", f"número ✓  {celsius}"))

        if fahrenheit is None:
            checks.append((False, "fahrenheit", "No definida — usa: fahrenheit = celsius * 9/5 + 32"))
        elif celsius is not None and isinstance(celsius, (int, float)):
            exp = celsius * 9 / 5 + 32
            if _approx(fahrenheit, exp, tol=0.01):
                checks.append((True, "fahrenheit = celsius × 9/5 + 32", f"✓  {fahrenheit:.2f}°F"))
            else:
                checks.append((False, "fahrenheit",
                               f"Para {celsius}°C debería ser {exp:.2f}°F, obtuve {fahrenheit}"))

        return self._award("ex1", checks, 6)

    def check_ex1_fstring(self):
        """Ex1-F — mensaje_temperatura con f-string (4 pts)"""
        _header("EJ 1 — F-string: mensaje_temperatura (4 pts)")
        checks = []
        celsius    = _get("celsius")
        fahrenheit = _get("fahrenheit")
        msg        = _get("mensaje_temperatura")

        if msg is None:
            checks.append((False, "mensaje_temperatura",
                           "No definida — crea: mensaje_temperatura = f\"...{celsius}...{fahrenheit}...\""))
        elif not isinstance(msg, str) or msg.strip() in ("", "?"):
            checks.append((False, "mensaje_temperatura", "Debe ser un f-string con tu mensaje"))
        else:
            c_str = str(celsius) if celsius is not None else ""
            f_str = str(fahrenheit) if fahrenheit is not None else ""
            f_int = str(int(fahrenheit)) if fahrenheit is not None else ""
            has_val = (c_str and c_str in msg) or (f_str and f_str in msg) or (f_int and f_int in msg)
            if has_val:
                checks.append((True, "mensaje_temperatura contiene los valores", f"✓  '{msg[:60]}'"))
            else:
                checks.append((False, "mensaje_temperatura",
                               "El mensaje debe incluir los valores de celsius y/o fahrenheit"))

        return self._award("ex1_f", checks, 4)

    # ── EX 2 — IGV + f-string ─────────────────────────────────

    def check_ex2(self):
        """Ex2 — Compra con IGV 18% (8 pts)"""
        _header("EJERCICIO 2 — Compra con IGV (8 pts)")
        checks = []
        base  = _get("precio_base")
        igv   = _get("igv")
        final = _get("precio_final")

        if base is None:
            checks.append((False, "precio_base", "No definida"))
        elif not isinstance(base, (int, float)) or isinstance(base, bool):
            checks.append((False, "precio_base", "Debe ser número"))
        elif base <= 0:
            checks.append((False, "precio_base", "Debe ser positivo"))
        else:
            checks.append((True, "precio_base", f"número ✓  {base}"))

        if igv is None:
            checks.append((False, "igv", "No definida — usa: igv = precio_base * 0.18"))
        elif base is not None and isinstance(base, (int, float)):
            exp = base * 0.18
            if _approx(igv, exp, tol=0.01):
                checks.append((True, "igv = precio_base × 0.18", f"✓  {igv:.2f}"))
            else:
                checks.append((False, "igv", f"Para base={base}, IGV debería ser {exp:.2f}, obtuve {igv}"))

        if final is None:
            checks.append((False, "precio_final", "No definida — usa: precio_final = precio_base + igv"))
        elif base is not None and isinstance(base, (int, float)):
            exp = base * 1.18
            if _approx(final, exp, tol=0.01):
                checks.append((True, "precio_final = precio_base + igv", f"✓  {final:.2f}"))
            else:
                checks.append((False, "precio_final", f"Debería ser {exp:.2f}, obtuve {final}"))

        return self._award("ex2", checks, 8)

    def check_ex2_fstring(self):
        """Ex2-F — mensaje_igv con f-string (4 pts)"""
        _header("EJ 2 — F-string: mensaje_igv (4 pts)")
        checks = []
        base  = _get("precio_base")
        final = _get("precio_final")
        msg   = _get("mensaje_igv")

        if msg is None:
            checks.append((False, "mensaje_igv",
                           "No definida — crea: mensaje_igv = f\"...{precio_base}...{precio_final}...\""))
        elif not isinstance(msg, str) or msg.strip() in ("", "?"):
            checks.append((False, "mensaje_igv", "Debe ser un f-string con tu mensaje"))
        else:
            b_str = str(int(base)) if isinstance(base, float) and base == int(base) else (str(base) if base is not None else "")
            f_str = str(final) if final is not None else ""
            has_val = (b_str and b_str in msg) or (f_str and f_str in msg)
            if has_val:
                checks.append((True, "mensaje_igv contiene los valores", f"✓  '{msg[:60]}'"))
            else:
                checks.append((False, "mensaje_igv",
                               "El mensaje debe incluir los valores de precio_base y/o precio_final"))

        return self._award("ex2_f", checks, 4)

    # ── EX 3 — Promedio ───────────────────────────────────────

    def check_ex3(self):
        """Ex3 — Promedio de tres notas (8 pts)"""
        _header("EJERCICIO 3 — Promedio Escolar (8 pts)")
        checks = []
        notas    = [_get(f"nota{i}") for i in range(1, 4)]
        promedio = _get("promedio")

        for i, nota in enumerate(notas, 1):
            if nota is None:
                checks.append((False, f"nota{i}", "No definida"))
            elif not isinstance(nota, (int, float)) or isinstance(nota, bool):
                checks.append((False, f"nota{i}", "Debe ser número"))
            elif not (0 <= nota <= 20):
                checks.append((False, f"nota{i}", f"Fuera del rango 0–20 (obtuve {nota})"))
            else:
                checks.append((True, f"nota{i}", f"✓  {nota}"))

        valid = [n for n in notas if isinstance(n, (int, float)) and not isinstance(n, bool)]
        if promedio is None:
            checks.append((False, "promedio", "No definida — usa: promedio = (nota1 + nota2 + nota3) / 3"))
        elif len(valid) == 3:
            exp = sum(valid) / 3
            if _approx(promedio, exp, tol=0.01):
                checks.append((True, "promedio correcto", f"✓  {promedio:.2f}"))
            else:
                checks.append((False, "promedio", f"Debería ser {exp:.4f}, obtuve {promedio}"))

        return self._award("ex3", checks, 8)

    # ── EX 4 — IMC ────────────────────────────────────────────

    def check_ex4(self):
        """Ex4 — Calculadora de IMC (9 pts)"""
        _header("EJERCICIO 4 — Calculadora de IMC (9 pts)")
        checks = []
        peso   = _get("peso")
        altura = _get("altura")
        imc    = _get("imc")

        if peso is None:
            checks.append((False, "peso", "No definida — float, ej: peso = 60.5"))
        elif not isinstance(peso, (int, float)) or isinstance(peso, bool):
            checks.append((False, "peso", "Debe ser número"))
        elif not (20 <= peso <= 300):
            checks.append((False, "peso", f"Valor {peso} fuera de rango (20–300 kg)"))
        else:
            checks.append((True, "peso", f"✓  {peso} kg"))

        if altura is None:
            checks.append((False, "altura", "No definida — en metros, ej: altura = 1.70"))
        elif not isinstance(altura, (int, float)) or isinstance(altura, bool):
            checks.append((False, "altura", "Debe ser número"))
        elif not (0.5 <= altura <= 3.0):
            checks.append((False, "altura", f"¿Usaste metros? (ej: 1.70 no 170). Obtuve: {altura}"))
        else:
            checks.append((True, "altura", f"✓  {altura} m"))

        if imc is None:
            checks.append((False, "imc", "No definida — usa: imc = peso / (altura ** 2)"))
        elif (peso is not None and altura is not None
              and isinstance(peso, (int, float)) and isinstance(altura, (int, float)) and altura > 0):
            exp = peso / (altura ** 2)
            if _approx(imc, exp, tol=0.01):
                checks.append((True, "imc = peso / altura²", f"✓  {imc:.2f}"))
            else:
                checks.append((False, "imc", f"Para peso={peso}, altura={altura}: debería ser {exp:.2f}, obtuve {imc}"))

        return self._award("ex4", checks, 9)

    # ── EX 5 — Email ──────────────────────────────────────────

    def check_ex5(self):
        """Ex5 — Generador de Email (9 pts)"""
        _header("EJERCICIO 5 — Generador de Email (9 pts)")
        checks = []
        nu    = _get("nombre_usuario")
        ap    = _get("apellido")
        dom   = _get("dominio")
        email = _get("email")

        for vname, val in [("nombre_usuario", nu), ("apellido", ap), ("dominio", dom)]:
            if val is None:
                checks.append((False, vname, "No definida"))
            elif not isinstance(val, str) or val.strip() in ("", "?"):
                checks.append((False, vname, "Debe ser str no vacío"))
            else:
                checks.append((True, vname, f"str ✓  '{val}'"))

        if email is None:
            checks.append((False, "email", "No definida — combina: nombre_usuario + '.' + apellido + '@' + dominio"))
        elif not isinstance(email, str):
            checks.append((False, "email", "Debe ser str"))
        elif "@" not in email:
            checks.append((False, "email", f"Falta '@' — obtuve: '{email}'"))
        elif nu and ap and dom:
            nl = nu.lower().replace(" ", "")
            al = ap.lower().replace(" ", "")
            dl = dom.lower()
            el = email.lower()
            if nl in el and al in el and dl in el:
                checks.append((True, "email con nombre+apellido+@+dominio", f"✓  '{email}'"))
            else:
                checks.append((False, "email", f"Debe incluir nombre, apellido y dominio — obtuve: '{email}'"))

        return self._award("ex5", checks, 9)

    # ── EX 6 — Conversor de Unidades ─────────────────────────

    def check_ex6(self):
        """Ex6 — Conversor de Unidades (9 pts)"""
        _header("EJERCICIO 6 — Conversor de Unidades (9 pts)")
        checks = []
        metros   = _get("metros")
        km       = _get("kilometros")
        cm       = _get("centimetros")
        pulgadas = _get("pulgadas")

        if metros is None:
            checks.append((False, "metros", "No definida"))
        elif not isinstance(metros, (int, float)) or isinstance(metros, bool):
            checks.append((False, "metros", "Debe ser número"))
        elif metros <= 0:
            checks.append((False, "metros", "Debe ser positivo"))
        else:
            checks.append((True, "metros", f"✓  {metros}"))

        if metros and isinstance(metros, (int, float)) and not isinstance(metros, bool):
            for vname, val, exp, tol in [
                ("kilometros",  km,       metros / 1000,    1e-9),
                ("centimetros", cm,       metros * 100,     1e-6),
                ("pulgadas",    pulgadas, metros * 39.3701, 0.01),
            ]:
                if val is None:
                    checks.append((False, vname, "No definida"))
                elif _approx(val, exp, tol):
                    checks.append((True, vname, f"✓  {val:.4f}"))
                else:
                    checks.append((False, vname, f"Para {metros} m debería ser {exp:.4f}, obtuve {val}"))
        else:
            for vname in ["kilometros", "centimetros", "pulgadas"]:
                checks.append((False, vname, "Define primero 'metros' con un valor positivo"))

        return self._award("ex6", checks, 9)

    # ── EX 7 — Fiesta de Cumpleaños (Capstone) ────────────────

    def check_ex7(self):
        """Ex7 — Fiesta de Cumpleaños: capstone (15 pts)"""
        _header("EJERCICIO 7 — Fiesta de Cumpleaños  (15 pts)")
        checks = []
        nombre_f  = _get("nombre_festejado")
        edad_n    = _get("edad_nueva")
        p_torta   = _get("precio_torta")
        p_deco    = _get("precio_decoracion")
        invitados = _get("num_invitados")
        costo_t   = _get("costo_total")
        costo_pp  = _get("costo_por_persona")

        if nombre_f is None:
            checks.append((False, "nombre_festejado", "No definida"))
        elif not isinstance(nombre_f, str) or nombre_f.strip() in ("", "?"):
            checks.append((False, "nombre_festejado", "Debe ser str con un nombre real"))
        else:
            checks.append((True, "nombre_festejado", f"str ✓  '{nombre_f}'"))

        if edad_n is None:
            checks.append((False, "edad_nueva", "No definida"))
        elif isinstance(edad_n, bool) or not isinstance(edad_n, int):
            checks.append((False, "edad_nueva", "Debe ser int (sin comillas)"))
        elif not (1 <= edad_n <= 110):
            checks.append((False, "edad_nueva", f"Valor {edad_n} fuera de rango"))
        else:
            checks.append((True, "edad_nueva", f"int ✓  {edad_n}"))

        for vname, val in [("precio_torta", p_torta), ("precio_decoracion", p_deco)]:
            if val is None:
                checks.append((False, vname, "No definida"))
            elif not isinstance(val, (int, float)) or isinstance(val, bool):
                checks.append((False, vname, "Debe ser número"))
            elif val <= 0:
                checks.append((False, vname, "Debe ser positivo"))
            else:
                checks.append((True, vname, f"float ✓  {val}"))

        if invitados is None:
            checks.append((False, "num_invitados", "No definida"))
        elif isinstance(invitados, bool) or not isinstance(invitados, int):
            checks.append((False, "num_invitados", "Debe ser int"))
        elif invitados <= 0:
            checks.append((False, "num_invitados", "Debe ser positivo"))
        else:
            checks.append((True, "num_invitados", f"int ✓  {invitados}"))

        if costo_t is None:
            checks.append((False, "costo_total",
                           "No definida — usa: costo_total = precio_torta + precio_decoracion"))
        elif p_torta is not None and p_deco is not None and isinstance(p_torta, (int, float)) and isinstance(p_deco, (int, float)):
            exp = p_torta + p_deco
            if _approx(costo_t, exp, tol=0.01):
                checks.append((True, "costo_total = precio_torta + precio_decoracion", f"✓  {costo_t}"))
            else:
                checks.append((False, "costo_total", f"Debería ser {exp:.2f}, obtuve {costo_t}"))

        if costo_pp is None:
            checks.append((False, "costo_por_persona",
                           "No definida — usa: costo_por_persona = costo_total / num_invitados"))
        elif costo_t is not None and invitados is not None and isinstance(invitados, int) and invitados > 0:
            exp = costo_t / invitados
            if _approx(costo_pp, exp, tol=0.01):
                checks.append((True, "costo_por_persona = costo_total / num_invitados", f"✓  {costo_pp:.2f}"))
            else:
                checks.append((False, "costo_por_persona", f"Debería ser {exp:.2f}, obtuve {costo_pp}"))

        return self._award("ex7", checks, 15)

    # ── COHETE — Ecuación de Tsiolkovsky ─────────────────────

    def check_cohete(self):
        """Cohete — Ecuación de Tsiolkovsky (10 pts)"""
        import math
        _header("DESAFÍO GUIADO — Combustible del Cohete (10 pts)")
        checks = []

        masa_carga = _get("masa_carga")
        masa_seca  = _get("masa_seca")
        Isp        = _get("Isp")
        g0         = _get("g0")
        delta_v    = _get("delta_v")
        masa_sc    = _get("masa_sin_combustible")
        mrat       = _get("masa_ratio")
        masa_comb  = _get("masa_combustible")
        fraccion   = _get("fraccion_combustible")

        inputs_ok = all(isinstance(v, (int, float)) and not isinstance(v, bool)
                        for v in [masa_carga, masa_seca, Isp, g0, delta_v]
                        if v is not None)

        if masa_carga is not None and masa_seca is not None and inputs_ok:
            exp_sc = masa_carga + masa_seca
            if masa_sc is None:
                checks.append((False, "masa_sin_combustible",
                               "No definida — usa: masa_sin_combustible = masa_carga + masa_seca"))
            elif _approx(masa_sc, exp_sc, tol=0.1):
                checks.append((True, "masa_sin_combustible", f"✓  {masa_sc:,.0f} kg"))
            else:
                checks.append((False, "masa_sin_combustible",
                               f"Debería ser {exp_sc:,.0f} kg, obtuve {masa_sc}"))
        else:
            checks.append((False, "masa_sin_combustible",
                           "Define primero: masa_carga, masa_seca, Isp, g0, delta_v"))

        if Isp is not None and g0 is not None and delta_v is not None and inputs_ok:
            exp_ratio = math.exp(delta_v / (Isp * g0))
            if mrat is None:
                checks.append((False, "masa_ratio",
                               "No definida — usa: masa_ratio = math.exp(delta_v / (Isp * g0))"))
            elif _approx(mrat, exp_ratio, tol=0.01):
                checks.append((True, "masa_ratio", f"✓  {mrat:.4f}"))
            else:
                checks.append((False, "masa_ratio",
                               f"Debería ser {exp_ratio:.4f}, obtuve {mrat}"))

        if masa_sc is not None and mrat is not None:
            exp_comb = masa_sc * (mrat - 1)
            if masa_comb is None:
                checks.append((False, "masa_combustible",
                               "No definida — usa: masa_combustible = masa_sin_combustible * (masa_ratio - 1)"))
            elif _approx(masa_comb, exp_comb, tol=1.0):
                checks.append((True, "masa_combustible", f"✓  {masa_comb:,.0f} kg"))
            else:
                checks.append((False, "masa_combustible",
                               f"Debería ser {exp_comb:,.0f} kg, obtuve {masa_comb:,.0f}"))

        if masa_comb is not None and masa_sc is not None:
            exp_frac = masa_comb / (masa_sc + masa_comb) * 100
            if fraccion is None:
                checks.append((False, "fraccion_combustible",
                               "No definida — usa: fraccion_combustible = masa_combustible / (masa_sin_combustible + masa_combustible) * 100"))
            elif _approx(fraccion, exp_frac, tol=0.1):
                checks.append((True, "fraccion_combustible", f"✓  {fraccion:.1f}%"))
            else:
                checks.append((False, "fraccion_combustible",
                               f"Debería ser {exp_frac:.1f}%, obtuve {fraccion}"))

        return self._award("cohete", checks, 10)

    # ── RETO 1 — Movimiento Parabólico ────────────────────────

    def check_reto1(self):
        """Reto 1 — Movimiento Parabólico (6 pts)"""
        import math
        _header("RETO 1 — Movimiento Parabólico (6 pts)")
        checks = []
        v0      = _get("v0")
        angulo  = _get("angulo")
        h_max   = _get("h_max")
        R       = _get("R")
        t_vuelo = _get("t_vuelo")
        g = 9.81

        if v0 is None or not isinstance(v0, (int, float)) or isinstance(v0, bool):
            checks.append((False, "v0", "No definida — usa v0 = 50"))
        else:
            checks.append((True, "v0", f"✓  {v0} m/s"))

        if angulo is None or not isinstance(angulo, (int, float)) or isinstance(angulo, bool):
            checks.append((False, "angulo", "No definida — usa angulo = 45"))
        else:
            checks.append((True, "angulo", f"✓  {angulo}°"))

        if (v0 is not None and angulo is not None
                and isinstance(v0, (int, float)) and isinstance(angulo, (int, float))):
            theta   = math.radians(angulo)
            exp_h   = (v0 ** 2 * math.sin(theta) ** 2) / (2 * g)
            exp_R   = (v0 ** 2 * math.sin(2 * theta)) / g
            exp_t   = (2 * v0 * math.sin(theta)) / g

            if h_max is None:
                checks.append((False, "h_max",
                               f"No definida — aplica la fórmula. Esperado: {exp_h:.2f} m"))
            elif _approx(h_max, exp_h, tol=0.01):
                checks.append((True, "h_max", f"✓  {h_max:.2f} m"))
            else:
                checks.append((False, "h_max",
                               f"Para v0={v0}, θ={angulo}°: debería ser {exp_h:.2f} m"))

            if R is None:
                checks.append((False, "R",
                               f"No definida. Esperado: {exp_R:.2f} m"))
            elif _approx(R, exp_R, tol=0.01):
                checks.append((True, "R (alcance)", f"✓  {R:.2f} m"))
            else:
                checks.append((False, "R", f"Debería ser {exp_R:.2f} m, obtuve {R}"))

            if t_vuelo is None:
                checks.append((False, "t_vuelo",
                               f"No definida. Esperado: {exp_t:.2f} s"))
            elif _approx(t_vuelo, exp_t, tol=0.01):
                checks.append((True, "t_vuelo", f"✓  {t_vuelo:.2f} s"))
            else:
                checks.append((False, "t_vuelo",
                               f"Debería ser {exp_t:.2f} s, obtuve {t_vuelo}"))

        return self._award("reto1", checks, 6)

    # ── RETO 2 — Dilatación del Tiempo ───────────────────────

    def check_reto2(self):
        """Reto 2 — Dilatación del Tiempo Relativista (6 pts)"""
        import math
        _header("RETO 2 — Dilatación del Tiempo (6 pts)")
        checks = []
        c        = _get("c")
        t_reposo = _get("t_reposo")

        if (c is None or t_reposo is None
                or not isinstance(c, (int, float)) or not isinstance(t_reposo, (int, float))):
            checks.append((False, "c y t_reposo",
                           "Define primero: c = 299792458  y  t_reposo = 1.0"))
            return self._award("reto2", checks, 6)

        for i, frac in enumerate([0.5, 0.9, 0.99], 1):
            gamma_exp = 1 / math.sqrt(1 - frac ** 2)
            t_exp     = t_reposo * gamma_exp
            t_var     = _get(f"t_movimiento_{i}")
            g_var     = _get(f"gamma_{i}")

            if g_var is None:
                checks.append((False, f"gamma_{i}",
                               f"No definida. Esperado: {gamma_exp:.4f}"))
            elif _approx(g_var, gamma_exp, tol=0.001):
                checks.append((True, f"gamma_{i} ({int(frac*100)}%c)", f"✓  {g_var:.4f}"))
            else:
                checks.append((False, f"gamma_{i}",
                               f"Debería ser {gamma_exp:.4f}, obtuve {g_var}"))

            if t_var is None:
                checks.append((False, f"t_movimiento_{i}",
                               f"No definida. Esperado: {t_exp:.4f} s"))
            elif _approx(t_var, t_exp, tol=0.001):
                checks.append((True, f"t_movimiento_{i}", f"✓  {t_var:.4f} s"))
            else:
                checks.append((False, f"t_movimiento_{i}",
                               f"Debería ser {t_exp:.4f} s, obtuve {t_var}"))

        return self._award("reto2", checks, 6)

    # ── RETO 3 — Gravitación Universal ───────────────────────

    def check_reto3(self):
        """Reto 3 — Ley de Gravitación Universal (6 pts)"""
        _header("RETO 3 — Ley de Gravitación Universal (6 pts)")
        checks = []
        G        = 6.674e-11
        m_tierra = 5.972e24

        # Caso 1: Tierra-Luna
        m_luna   = 7.342e22
        r_tl     = 384400000.0
        exp_F_tl = G * m_tierra * m_luna / r_tl ** 2
        exp_a_lu = exp_F_tl / m_luna
        F_tl     = _get("F_tierra_luna")
        a_lu     = _get("a_luna")

        if F_tl is None:
            checks.append((False, "F_tierra_luna",
                           f"No definida. Esperado: ≈ {exp_F_tl:.3e} N"))
        elif _approx(F_tl, exp_F_tl, tol=exp_F_tl * 0.01):
            checks.append((True, "F_tierra_luna", f"✓  {F_tl:.3e} N"))
        else:
            checks.append((False, "F_tierra_luna",
                           f"Debería ser {exp_F_tl:.3e} N, obtuve {F_tl:.3e}"))

        if a_lu is None:
            checks.append((False, "a_luna",
                           f"No definida. Esperado: ≈ {exp_a_lu:.5f} m/s²"))
        elif _approx(a_lu, exp_a_lu, tol=exp_a_lu * 0.01):
            checks.append((True, "a_luna", f"✓  {a_lu:.5f} m/s²"))
        else:
            checks.append((False, "a_luna",
                           f"Debería ser {exp_a_lu:.5f} m/s², obtuve {a_lu}"))

        # Caso 2: Persona en la Tierra
        m_persona = 70.0
        r_tierra  = 6371000.0
        exp_F_per = G * m_tierra * m_persona / r_tierra ** 2
        exp_a_per = exp_F_per / m_persona
        F_per     = _get("F_persona")
        a_per     = _get("a_persona")

        if F_per is None:
            checks.append((False, "F_persona",
                           f"No definida. Esperado: ≈ {exp_F_per:.1f} N"))
        elif _approx(F_per, exp_F_per, tol=exp_F_per * 0.01):
            checks.append((True, "F_persona", f"✓  {F_per:.1f} N"))
        else:
            checks.append((False, "F_persona",
                           f"Debería ser {exp_F_per:.1f} N, obtuve {F_per}"))

        if a_per is None:
            checks.append((False, "a_persona",
                           f"No definida. Esperado: ≈ {exp_a_per:.4f} m/s²"))
        elif _approx(a_per, exp_a_per, tol=0.01):
            checks.append((True, "a_persona ≈ g", f"✓  {a_per:.4f} m/s² (¡es g!)"))
        else:
            checks.append((False, "a_persona",
                           f"Debería ser ≈ {exp_a_per:.4f} m/s², obtuve {a_per}"))

        # Caso 3: Sol-Tierra
        m_sol    = 1.989e30
        r_se     = 1.496e11
        exp_F_se = G * m_sol * m_tierra / r_se ** 2
        exp_a_ti = exp_F_se / m_tierra
        F_se     = _get("F_sol_tierra")
        a_ti     = _get("a_tierra")

        if F_se is None:
            checks.append((False, "F_sol_tierra",
                           f"No definida. Esperado: ≈ {exp_F_se:.3e} N"))
        elif _approx(F_se, exp_F_se, tol=exp_F_se * 0.01):
            checks.append((True, "F_sol_tierra", f"✓  {F_se:.3e} N"))
        else:
            checks.append((False, "F_sol_tierra",
                           f"Debería ser {exp_F_se:.3e} N, obtuve {F_se:.3e}"))

        if a_ti is None:
            checks.append((False, "a_tierra",
                           f"No definida. Esperado: ≈ {exp_a_ti:.5f} m/s²"))
        elif _approx(a_ti, exp_a_ti, tol=exp_a_ti * 0.01):
            checks.append((True, "a_tierra", f"✓  {a_ti:.5f} m/s²"))
        else:
            checks.append((False, "a_tierra",
                           f"Debería ser {exp_a_ti:.5f} m/s², obtuve {a_ti}"))

        return self._award("reto3", checks, 6)

    # ── RESUMEN FINAL ─────────────────────────────────────────

    def resumen(self):
        earned   = sum(e for e, _ in self._scores.values())
        possible = sum(p for _, p in self._scores.values())
        pct      = round(earned / possible * 100) if possible else 0
        n        = self._nombre()
        filled   = round(30 * pct / 100)
        bar      = "█" * filled + "░" * (30 - filled)

        if pct >= 90:
            nota = "AD"
            nota_msg = "Nivel de Logro Destacado"
        elif pct >= 75:
            nota = "A"
            nota_msg = "Nivel de Logro Esperado"
        elif pct >= 55:
            nota = "B"
            nota_msg = "En Proceso"
        else:
            nota = "C"
            nota_msg = "En Inicio"

        print("\n" + "═" * 62)
        print(f"  REPORTE FINAL — {n.upper()}")
        print(f"  Notebook 1: Fundamentos de Python")
        print("═" * 62)
        print(f"\n  Puntaje: {earned}/{possible} pts  ({pct}%)")
        print(f"  [{bar}]")
        print(f"  Calificación: {nota}  —  {nota_msg}")

        if self._scores:
            labels = {
                "mini_a": "Checkpoint A  Mi Perfil        ",
                "t1":     "T1            Tipo int          ",
                "mini_b": "Checkpoint B  Tipos correctos   ",
                "t2":     "T2            Función print     ",
                "t3":     "T3            Tipo float        ",
                "mini_d": "Checkpoint D  F-string          ",
                "mini_c": "Checkpoint C  La Lonchera       ",
                "ex1":    "Ex 1          Temperatura       ",
                "ex1_f":  "Ex 1-F        F-string temp     ",
                "ex2":    "Ex 2          IGV               ",
                "ex2_f":  "Ex 2-F        F-string IGV      ",
                "ex3":    "Ex 3          Promedio Escolar  ",
                "ex4":    "Ex 4          IMC               ",
                "ex5":    "Ex 5          Email             ",
                "ex6":    "Ex 6          Conversor         ",
                "ex7":    "Ex 7          Fiesta            ",
                "cohete": "Cohete        Tsiolkovsky       ",
                "reto1":  "Reto 1        Proyectil         ",
                "reto2":  "Reto 2        Rel. Especial     ",
                "reto3":  "Reto 3        Gravitación       ",
            }
            print()
            for key, label in labels.items():
                if key in self._scores:
                    e, p = self._scores[key]
                    status = "⭐" if e == p else ("👍" if e > 0 else "  ")
                    print(f"  {status} {label} {e:2}/{p:2}")

        print()
        if pct >= 90:
            print(f"  ¡EXCELENTE, {n}! Dominas los fundamentos de Python.")
            print(f"  Estás listo/a para el Notebook 2.")
        elif pct >= 75:
            print(f"  ¡Bien hecho, {n}! Repasa los ❌ para llegar al AD.")
        elif pct >= 55:
            print(f"  Vas bien, {n}. Dedica tiempo a los ejercicios que fallaron.")
        else:
            print(f"  {n}, relee la teoría de cada sección y vuelve a intentarlo.")
            print(f"  ¡Cada intento cuenta!")
        print(f"\n{'═' * 62}\n")
