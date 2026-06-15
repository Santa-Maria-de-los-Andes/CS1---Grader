"""
Autograder v1 — Notebook 3: Loops Anidados, Ifs Anidados, Funciones
🍄  THE LAST OF US — Firefly Research Terminal
"""

import sys
import datetime as _dt
from IPython.display import HTML, display

# ─── Supabase Config ──────────────────────────────────────────
SUPABASE_URL      = "https://uwykikwutjtkpffwmdiq.supabase.co"
SUPABASE_ANON_KEY = "sb_publishable_aBG6GD4wn9CgpSE-47fagQ_sNhnzznu"
LOGO_URL          = "https://raw.githubusercontent.com/Santa-Maria-de-los-Andes/CS1---Grader/main/icono%20SMA.png"

# ─── Deadline: set when course date is confirmed ──────────────
_DEADLINE_UTC   = _dt.datetime(2026, 12, 31, 23, 59, 0, tzinfo=_dt.timezone.utc)
DEADLINE_PASSED = _dt.datetime.now(_dt.timezone.utc) >= _DEADLINE_UTC

# ─── Scoring ─────────────────────────────────────────────────
#   Exercises:  ex1(6)+ex2(6)+ex3(8)+ex4(8)+ex5(8)+ex6(8)+ex7(8)+ex8(10)+ex9(6)+ex10(8)+ex11(10) = 86
#   Debugs:     debug1-5 (3 ea.) + debug2b (3) = 18
#   Teoría:     t1+t2+t3 (4 ea.) = 12
#   Integración: intex1(6)+intex2(8)+intex3(8)+intex4(10)+intex5(12) = 44
_CORE_MAX   = 160
_BONUS_KEYS = {"reto1", "reto2"}
_BONUS_MAX  = 12

# ─── TLOU Levels (by % of core score) ────────────────────────
_LEVELS = [
    (96, 6, "⚡ Proyecto Ellie"),
    (81, 5, "🌿 Agente Marlene"),
    (61, 4, "🔦 Explorador Firefly"),
    (41, 3, "👁️ Acechador"),
    (21, 2, "🍄 Corredor"),
    (0,  1, "☠️ Paciente 0"),
]

_XP_GRAD = {
    1: "linear-gradient(90deg,#1a1a1a,#2d2d2d)",
    2: "linear-gradient(90deg,#2d1200,#5c2800)",
    3: "linear-gradient(90deg,#3d1800,#8b4500)",
    4: "linear-gradient(90deg,#0a2010,#1a5030)",
    5: "linear-gradient(90deg,#0d3020,#2a7050)",
    6: "linear-gradient(90deg,#0d2d20,#4ca66b,#d4870a)",
}

_LV_CSS_COLOR = {
    1: "#444444",
    2: "#7a3000",
    3: "#cc5500",
    4: "#2d7a45",
    5: "#4ca66b",
    6: "#4ca66b",
}


def _level_info(pct):
    for thresh, num, name in _LEVELS:
        if pct >= thresh:
            return num, name
    return 1, "☠️ Paciente 0"


def _lv_color(n):
    return _LV_CSS_COLOR.get(n, "#444444")


# ─── Helpers ─────────────────────────────────────────────────

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


# ─── Main Class ──────────────────────────────────────────────

class Autograder:

    def __init__(self):
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except AttributeError:
            pass
        self._scores       = {}
        self._achievements = set()
        self._streak       = 0
        self._prev_level   = 0
        self._email        = None
        self._nombre_real  = None
        self._grado        = None
        self._dni          = None
        self._checkpoints  = set()
        self._show_registration_form()

    # ── Registration form ────────────────────────────────────

    def _show_registration_form(self):
        logo_tag = (f'<img src="{LOGO_URL}" style="height:48px;object-fit:contain;" '
                    f'onerror="this.style.display=\'none\'">'
                    if LOGO_URL else
                    '<span style="font-family:monospace;font-size:13px;'
                    'color:#4ca66b;letter-spacing:2px;">SMA</span>')

        try:
            from google.colab import output as _out

            def _on_register(nombre, grado, dni):
                nombre = (nombre or "").strip()
                grado  = (grado  or "").strip()
                dni    = (dni    or "").strip()
                if not nombre or not grado or not dni:
                    return
                self._nombre_real = nombre
                self._grado       = grado
                self._dni         = dni

                _best = None
                try:
                    import urllib.request as _ur2, json as _json2, urllib.parse as _up2
                    _qurl = (
                        f"{SUPABASE_URL}/rest/v1/submissions"
                        f"?select=earned,possible,pct,level_name,streak"
                        f"&dni=eq.{_up2.quote(str(dni), safe='')}"
                        f"&notebook=eq.nb3"
                        f"&order=pct.desc,submitted_at.desc&limit=1"
                    )
                    _req2 = _ur2.Request(_qurl, headers={
                        "apikey": SUPABASE_ANON_KEY,
                        "Authorization": f"Bearer {SUPABASE_ANON_KEY}",
                    })
                    with _ur2.urlopen(_req2, timeout=8) as _resp2:
                        _rows = _json2.loads(_resp2.read())
                    if _rows:
                        _best = _rows[0]
                except Exception:
                    pass

                if _best:
                    _score_html = f'''
  <div style="background:#020d02;border:1px solid #2d5a1b;border-radius:3px;
    padding:12px 20px;margin-top:6px;font-family:monospace;animation:ag-fadein .4s ease .1s both;">
    <div style="font-size:6px;color:#2d5a1b;letter-spacing:2px;margin-bottom:10px;">
      ✦ TU MEJOR MARCA — NOTEBOOK 3</div>
    <div style="display:flex;align-items:center;gap:20px;">
      <div style="font-size:28px;color:#4ca66b;
        text-shadow:0 0 16px rgba(76,166,107,.8),2px 2px 0 #0d2d10;">
        {_best['pct']}%</div>
      <div>
        <div style="font-size:8px;color:#d4870a;letter-spacing:1px;">{_best['level_name']}</div>
        <div style="font-size:6px;color:#8888bb;margin-top:6px;letter-spacing:1px;">
          {_best['earned']} / {_best['possible']} XP</div>
      </div>
    </div>
  </div>'''
                else:
                    _score_html = (
                        '<div style="background:#020d02;border:1px solid #1a2a1a;border-radius:3px;'
                        'padding:10px 20px;margin-top:6px;'
                        'font-family:monospace;font-size:6px;color:#2a3a2a;'
                        'letter-spacing:1px;animation:ag-fadein .4s ease .1s both;">'
                        '✦ Primera misión — aún no tienes marca registrada</div>'
                    )

                display(HTML(f'''
<link href="https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap" rel="stylesheet">
<style>
  @keyframes ag-fadein {{from{{opacity:0;transform:translateY(8px)}}to{{opacity:1;transform:translateY(0)}}}}
  @keyframes ag-dot    {{0%,80%,100%{{transform:scale(.6);opacity:.3}}40%{{transform:scale(1);opacity:1}}}}
  @keyframes ag-start  {{0%{{opacity:0;transform:scale(.7)}}60%{{transform:scale(1.12)}}100%{{opacity:1;transform:scale(1)}}}}
</style>
<div style="max-width:840px;margin:10px 0;box-sizing:border-box;">
  <div style="background:#010801;border:1px solid #4ca66b;border-radius:3px;padding:12px 18px;
    font-family:'Share Tech Mono',monospace;font-size:8px;
    color:#4ca66b;letter-spacing:1px;animation:ag-fadein .4s ease;">
    ✦ &nbsp;¡ACCESO CONCEDIDO, {nombre.upper()}! &nbsp;·&nbsp; FIREFLY NODE 7 &nbsp;·&nbsp; {grado}
  </div>
  {_score_html}
  <div id="ag-loading" style="background:#020d02;border:1px solid #1a2a1a;border-radius:3px;
    padding:22px 18px;margin-top:6px;text-align:center;animation:ag-fadein .5s ease .2s both;">
    <div style="display:flex;justify-content:center;gap:6px;margin-bottom:12px;">
      <div style="width:8px;height:8px;border-radius:50%;background:#2d5a1b;
        animation:ag-dot 1.2s ease-in-out 0s infinite;"></div>
      <div style="width:8px;height:8px;border-radius:50%;background:#2d5a1b;
        animation:ag-dot 1.2s ease-in-out .2s infinite;"></div>
      <div style="width:8px;height:8px;border-radius:50%;background:#2d5a1b;
        animation:ag-dot 1.2s ease-in-out .4s infinite;"></div>
    </div>
    <div style="font-family:'Share Tech Mono',monospace;font-size:7px;color:#2a3a2a;letter-spacing:2px;">
      INICIALIZANDO TERMINAL DE ANÁLISIS…
    </div>
  </div>
  <div id="ag-start" style="display:none;background:linear-gradient(160deg,#010801,#011206);
    border:2px solid #4ca66b;border-radius:4px;padding:36px 24px;margin-top:6px;text-align:center;
    box-shadow:0 0 40px rgba(76,166,107,.2),0 6px 24px rgba(0,0,0,.9);">
    <div style="font-size:44px;margin-bottom:14px;animation:ag-start .55s cubic-bezier(.34,1.56,.64,1);">🍄</div>
    <div style="font-family:'Share Tech Mono',monospace;font-size:clamp(18px,4vw,28px);color:#4ca66b;
      letter-spacing:6px;text-shadow:0 0 24px rgba(76,166,107,.8),2px 2px 0 #0d2d10;
      animation:ag-start .6s ease;margin-bottom:14px;">¡SOBREVIVE!</div>
    <div style="font-family:'Share Tech Mono',monospace;font-size:7px;color:#d4870a;
      letter-spacing:2px;margin-bottom:16px;">EJECUTA LA PRIMERA CELDA PARA COMENZAR LA MISIÓN</div>
    <div style="font-size:11px;color:#2d5a1b;opacity:.5;letter-spacing:8px;">✦ ✧ ✦ ✧ ✦ ✧ ✦ ✧ ✦ ✧</div>
  </div>
</div>
<script>
setTimeout(function(){{
  var l = document.getElementById('ag-loading');
  var s = document.getElementById('ag-start');
  if(l) l.style.display = 'none';
  if(s){{ s.style.display = 'block'; }}
}}, 1800);
</script>
'''))

            _out.register_callback('_ag_register', _on_register)

            display(HTML(f'''
<link href="https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap" rel="stylesheet">
<style>
  .ag-input,.ag-select {{
    width:100%;box-sizing:border-box;background:#010801;border:1px solid #1a2a1a;
    border-radius:3px;padding:0 12px;color:#b8ff9a;font-size:13px;height:42px;
    font-family:'Share Tech Mono',monospace;outline:none;transition:border .2s;
  }}
  .ag-input:focus,.ag-select:focus {{ border-color:#4ca66b; }}
  .ag-select option {{ background:#020d02; }}
  .ag-btn {{
    width:100%;padding:13px;background:linear-gradient(90deg,#0d3020,#1a5030);
    border:1px solid #4ca66b;border-radius:3px;color:#b8ff9a;
    font-family:'Share Tech Mono',monospace;font-size:9px;letter-spacing:2px;
    cursor:pointer;transition:opacity .2s;margin-top:6px;
  }}
  .ag-btn:hover {{ opacity:.85; }}
  .ag-err {{ color:#c0392b;font-size:11px;margin-top:6px;display:none; }}
  .ag-label {{ font-family:'Share Tech Mono',monospace;font-size:7px;letter-spacing:1px;
    margin-bottom:8px;display:flex;align-items:center;gap:5px; }}
  .ag-field {{ display:flex;flex-direction:column; }}
</style>
<div style="background:#020d02;border:2px solid #4ca66b;border-radius:4px;max-width:840px;
  margin:10px 0;overflow:hidden;box-shadow:0 0 40px rgba(76,166,107,.15),0 10px 30px rgba(0,0,0,.8);">

  <div style="background:linear-gradient(90deg,#010801,#011a06,#010801);border-bottom:2px solid #d4870a;
    padding:18px 24px;position:relative;display:flex;align-items:center;justify-content:center;min-height:80px;">
    <div style="position:absolute;left:20px;top:50%;transform:translateY(-50%);">{logo_tag}</div>
    <div style="text-align:center;">
      <div style="font-family:'Share Tech Mono',monospace;font-size:16px;color:#4ca66b;letter-spacing:3px;
        text-shadow:0 0 14px rgba(76,166,107,.7),2px 2px 0 #0d2d10;">✦ FIREFLY RESEARCH NODE 7 ✦</div>
      <div style="font-family:'Share Tech Mono',monospace;font-size:8px;color:#d4870a;
        letter-spacing:2px;margin-top:8px;">TERMINAL DE ANÁLISIS — NOTEBOOK III</div>
    </div>
    <div style="position:absolute;right:20px;top:50%;transform:translateY(-50%);">{logo_tag}</div>
  </div>

  <div style="padding:24px;">
    <div style="display:grid;grid-template-columns:2fr 1fr;gap:14px;margin-bottom:14px;align-items:end;">
      <div class="ag-field">
        <div class="ag-label" style="color:#4ca66b;">✦ NOMBRE COMPLETO</div>
        <input id="ag-nombre" class="ag-input" placeholder="Tu nombre y apellido" />
      </div>
      <div class="ag-field">
        <div class="ag-label" style="color:#4ca66b;">🏫 GRADO</div>
        <select id="ag-grado" class="ag-select">
          <option value="">— Selecciona —</option>
          <option value="3ro">3ro</option>
          <option value="4to">4to</option>
          <option value="5to">5to</option>
        </select>
      </div>
    </div>
    <div class="ag-field" style="margin-bottom:14px;">
      <div class="ag-label" style="color:#d4870a;">🪪 CÓDIGO DE ESTUDIANTE (DNI, Pasaporte, Carnet)</div>
      <input id="ag-dni" class="ag-input" placeholder="Ingresa tu código" />
    </div>
    <div id="ag-err" class="ag-err">⚠ Por favor completa todos los campos.</div>
    <button class="ag-btn" onclick="agRegister()">✦ &nbsp; ACCEDER AL TERMINAL &nbsp; ✦</button>
  </div>
</div>
<script>
async function agRegister() {{
  const nombre = document.getElementById('ag-nombre').value.trim();
  const grado  = document.getElementById('ag-grado').value.trim();
  const dni    = document.getElementById('ag-dni').value.trim();
  const err    = document.getElementById('ag-err');
  if (!nombre || !grado || !dni) {{ err.style.display = 'block'; return; }}
  err.style.display = 'none';
  await google.colab.kernel.invokeFunction('_ag_register', [nombre, grado, dni], {{}});
}}
</script>
'''))

        except ImportError:
            try:
                display(HTML('<div style="font-family:monospace;padding:10px;background:#020d02;'
                             'color:#4ca66b;border:1px solid #4ca66b;border-radius:3px;max-width:840px;">'
                             '✦ FIREFLY NODE 7 — Registro</div>'))
                self._nombre_real = input("Nombre completo: ").strip()
                grado_opts = {"1": "3ro", "2": "4to", "3": "5to"}
                print("Grado: 1) 3ro  2) 4to  3) 5to")
                self._grado = grado_opts.get(input("Elige (1/2/3): ").strip(), "3ro")
                self._dni   = input("Código de estudiante (DNI/Pasaporte/Carnet): ").strip()
            except Exception:
                pass

    # ── Internal helpers ─────────────────────────────────────

    @property
    def _logo_tag(self):
        if LOGO_URL:
            return (f'<img src="{LOGO_URL}" style="height:40px;object-fit:contain;" '
                    f'onerror="this.style.display:\'none\'">')
        return '<span style="font-family:monospace;font-size:11px;color:#4ca66b;">SMA</span>'

    @property
    def _logo_tag_sm(self):
        if LOGO_URL:
            return (f'<img src="{LOGO_URL}" style="height:24px;object-fit:contain;" '
                    f'onerror="this.style.display:\'none\'">')
        return '<span style="font-family:monospace;font-size:8px;color:#4ca66b;">SMA</span>'

    def _nombre(self):
        if self._nombre_real:
            return self._nombre_real
        n = _get("nombre")
        if isinstance(n, str) and n.strip() and n.strip() not in ("?", ""):
            return n.strip()
        return "explorador"

    def _totals(self):
        earned      = sum(e for e, _ in self._scores.values())
        possible    = sum(p for _, p in self._scores.values())
        core_earned = sum(e for k, (e, _) in self._scores.items() if k not in _BONUS_KEYS)
        pct         = min(round(core_earned / _CORE_MAX * 100), 100)
        return earned, possible, pct

    def _unlock(self, key):
        if key not in self._achievements:
            self._achievements.add(key)
            return True
        return False

    def _header(self, title, icon="🍄", pts=None):
        self._curr_title = title
        self._curr_icon  = icon
        self._curr_pts   = pts

    def _check_achievements(self, key):
        unlocked = []
        earned, possible, pct = self._totals()

        # Primer Contagio — first XP earned
        if any(e > 0 for e, _ in self._scores.values()) and self._unlock("primer_contagio"):
            unlocked.append(("🍄 Primer Contagio — Primera Exposición", "#8b5e00", "Común"))

        # Ojo Clínico — all debug perfect
        debug_keys = ["debug1", "debug2", "debug2b", "debug3", "debug4", "debug5"]
        if (all(k in self._scores and self._scores[k][0] == self._scores[k][1]
                for k in debug_keys)
                and self._unlock("ojo_clinico")):
            unlocked.append(("🩺 Ojo Clínico — Cero Errores de Lógica", "#8fa3a8", "Raro"))

        # Superviviente de Zona — all 5 checkpoints reached
        if len(self._checkpoints) >= 5 and self._unlock("superviviente_zona"):
            unlocked.append(("🚧 Superviviente de Zona — Todos los QZ", "#d4870a", "Épico"))

        # Esporas — streak >= 5
        if self._streak >= 5 and self._unlock("esporas"):
            unlocked.append(("💨 Esporas — Racha x5", "#8fa3a8", "Raro"))

        # Modelo SIR — all intex perfect
        sir_keys = ["intex1", "intex2", "intex3", "intex4", "intex5"]
        if (all(k in self._scores and self._scores[k][0] == self._scores[k][1]
                for k in sir_keys)
                and self._unlock("modelo_sir")):
            unlocked.append(("📈 Modelo SIR — Propagación Dominada", "#d4870a", "Épico"))

        # Inmunidad Adaptativa — 100% core
        if pct >= 100 and self._unlock("inmunidad_adaptativa"):
            unlocked.append(("🧬 Inmunidad Adaptativa — 100% del Notebook", "#c0392b", "Legendario"))

        # Esperanza de la Humanidad — both retos perfect
        if (all(k in self._scores and self._scores[k][0] == self._scores[k][1]
                for k in ["reto1", "reto2"])
                and self._unlock("esperanza_humanidad")):
            unlocked.append(("✦ Esperanza de la Humanidad", "#c0392b", "Legendario"))

        # Level-up
        lvl_num, lvl_name = _level_info(pct)
        if lvl_num > self._prev_level and self._prev_level > 0:
            unlocked.append((f"⬆️ ¡NIVEL! — {lvl_name}", "#39e5b6", "Nivel"))
        if lvl_num > self._prev_level:
            self._prev_level = lvl_num

        return unlocked

    def _award(self, key, checks, max_pts):
        passed = sum(1 for ok, _, _ in checks if ok)
        pts    = round(max_pts * passed / len(checks)) if checks else 0
        self._scores[key] = (pts, max_pts)

        if pts == max_pts:
            self._streak += 1
        else:
            self._streak = 0

        earned, possible, pct = self._totals()
        lvl_num, lvl_name     = _level_info(pct)
        core_earned  = sum(e for k, (e, _) in self._scores.items() if k not in _BONUS_KEYS)
        bonus_earned = sum(e for k, (e, _) in self._scores.items() if k in _BONUS_KEYS)
        _is_bonus    = key in _BONUS_KEYS

        import threading as _thr
        _thr.Thread(
            target=self._submit_to_supabase,
            args=(earned, possible, pct, lvl_num, lvl_name, True),
            daemon=True,
        ).start()

        rows_html = ""
        for ok, label, msg in checks:
            bdr = "#4ca66b" if ok else "#c0392b"
            bg  = "rgba(76,166,107,.04)" if ok else "rgba(192,57,43,.06)"
            sym = "✔" if ok else "✖"
            lbl_c = "#4ca66b" if ok else "#c0392b"
            msg_c = "#8888bb" if ok else "#cc7766"
            rows_html += (
                f'<div style="display:flex;align-items:flex-start;gap:10px;padding:7px 10px;'
                f'margin-bottom:3px;background:{bg};border-left:3px solid {bdr};border-radius:0 3px 3px 0;">'
                f'<span style="color:{bdr};font-size:13px;flex-shrink:0;line-height:1.5;">{sym}</span>'
                f'<div style="font-size:11px;line-height:1.5;">'
                f'<span style="color:{lbl_c};font-weight:bold;">{label}:</span> '
                f'<span style="color:{msg_c};">{msg}</span></div></div>'
            )

        star_r = pts / max_pts if max_pts > 0 else 0
        gold, dark = "#d4870a", "#2a1400"
        if star_r == 1.0:
            stars_html = f'<span style="color:{gold};font-size:15px;letter-spacing:3px;">★★★</span>'
        elif star_r >= 0.67:
            stars_html = (f'<span style="color:{gold};font-size:15px;letter-spacing:3px;">★★</span>'
                          f'<span style="color:{dark};font-size:15px;">★</span>')
        elif star_r > 0:
            stars_html = (f'<span style="color:{gold};font-size:15px;">★</span>'
                          f'<span style="color:{dark};font-size:15px;letter-spacing:3px;">★★</span>')
        else:
            stars_html = f'<span style="color:{dark};font-size:15px;letter-spacing:3px;">★★★</span>'

        combo_html = ""
        if self._streak >= 2:
            c_color = "#c0392b" if self._streak >= 5 else "#d4870a"
            combo_html = (
                f'<div style="display:inline-flex;align-items:center;gap:5px;padding:3px 10px;'
                f'background:rgba(212,135,10,.12);border:1px solid {c_color};border-radius:2px;'
                f'margin-left:8px;">'
                f'<span style="font-family:\'Share Tech Mono\',monospace;font-size:7px;'
                f'color:{c_color};">✦ RACHA x{self._streak}</span></div>'
            )

        if pts == max_pts:
            s_icon, s_text, s_color = "✦", f"¡PERFECTO! +{pts} XP", "#4ca66b"
            border_color, glow = "#4ca66b", "0 0 22px rgba(76,166,107,.15)"
        elif pts > 0:
            s_icon, s_text, s_color = "🔦", f"+{pts} XP  ·  {max_pts - pts} por ganar", "#d4870a"
            border_color, glow = "#d4870a", "0 0 22px rgba(212,135,10,.12)"
        else:
            s_icon, s_text, s_color = "🍄", "¡INTENTA DE NUEVO! — Corrige los ✖", "#c0392b"
            border_color, glow = "#c0392b", "0 0 22px rgba(192,57,43,.15)"

        xp_grad = _XP_GRAD.get(lvl_num, _XP_GRAD[1])

        dots = "".join(
            f'<span style="display:inline-block;width:7px;height:7px;border-radius:50%;'
            f'background:{"#4ca66b" if ok else "#c0392b"};margin:0 2px;'
            f'box-shadow:0 0 4px {"#4ca66b" if ok else "#c0392b"};"></span>'
            for ok, _, _ in checks
        )

        new_ach     = self._check_achievements(key)
        reg_ach     = [(n, c, r) for n, c, r in new_ach if r != "Nivel"]
        levelup_ach = [(n, c, r) for n, c, r in new_ach if r == "Nivel"]

        _RC = {
            "Común":     ("#8b5e00", "rgba(139,94,0,.12)",   "🍄"),
            "Raro":      ("#4a6fa5", "rgba(74,111,165,.12)", "🛡️"),
            "Épico":     ("#d4870a", "rgba(212,135,10,.10)", "✦"),
            "Legendario":("#c0392b", "rgba(192,57,43,.15)",  "🧬"),
        }
        ach_html = ""
        for ach_name, _, ach_rarity in reg_ach:
            bc, bg_a, ach_icon = _RC.get(ach_rarity, _RC["Común"])
            ach_html += (
                f'<div style="display:flex;align-items:center;gap:10px;margin-top:8px;'
                f'padding:10px 12px;background:{bg_a};border:1px solid {bc};border-radius:3px;">'
                f'<span style="font-size:18px;">{ach_icon}</span>'
                f'<div style="flex:1;">'
                f'<div style="margin-bottom:3px;">'
                f'<span style="background:{bc};color:#020d02;font-size:7px;font-weight:bold;'
                f'padding:1px 5px;border-radius:2px;font-family:\'Share Tech Mono\',monospace;">'
                f'{ach_rarity.upper()}</span>'
                f'<span style="font-family:\'Share Tech Mono\',monospace;font-size:7px;'
                f'color:{bc};margin-left:6px;">LOGRO DESBLOQUEADO</span>'
                f'</div>'
                f'<div style="color:#b8ff9a;font-size:12px;font-weight:bold;">{ach_name}</div>'
                f'</div></div>'
            )

        curr_icon  = getattr(self, '_curr_icon', '🍄')
        curr_title = getattr(self, '_curr_title', 'MISIÓN').upper()
        _logo_sm   = self._logo_tag_sm

        _core_pct_bar = min(round(core_earned / _CORE_MAX * 100), 100)
        if _is_bonus:
            _bpct = round(bonus_earned / _BONUS_MAX * 100) if bonus_earned else 0
            xp_bar_html = (
                f'<div style="display:flex;justify-content:space-between;margin-bottom:4px;">'
                f'<span style="font-family:\'Share Tech Mono\',monospace;font-size:7px;color:#39e5b6;">'
                f'Bonus XP: {bonus_earned}/{_BONUS_MAX}</span>'
                f'<span style="font-family:\'Share Tech Mono\',monospace;font-size:7px;color:#39e5b6;">'
                f'✧ RETO</span></div>'
                f'<div style="width:100%;height:10px;background:#0a1a0a;border:1px solid #1a2a1a;'
                f'border-radius:2px;overflow:hidden;">'
                f'<div style="width:{_bpct}%;height:100%;'
                f'background:linear-gradient(90deg,#0a2010,#39e5b6);border-radius:2px;'
                f'transform-origin:left;animation:pg-xpscale 1.1s cubic-bezier(.4,0,.2,1) forwards;'
                f'box-shadow:0 0 6px rgba(57,229,182,.3);"></div></div>'
            )
        else:
            xp_bar_html = (
                f'<div style="display:flex;justify-content:space-between;margin-bottom:4px;">'
                f'<span style="font-family:\'Share Tech Mono\',monospace;font-size:7px;color:#2a3a2a;">'
                f'XP: {core_earned}/{_CORE_MAX}</span>'
                f'<span style="font-family:\'Share Tech Mono\',monospace;font-size:7px;'
                f'color:{_lv_color(lvl_num)};">{lvl_name}</span></div>'
                f'<div style="width:100%;height:10px;background:#0a1a0a;border:1px solid #1a2a1a;'
                f'border-radius:2px;overflow:hidden;">'
                f'<div style="width:{_core_pct_bar}%;height:100%;background:{xp_grad};'
                f'border-radius:2px;transform-origin:left;'
                f'animation:pg-xpscale 1.1s cubic-bezier(.4,0,.2,1) forwards;'
                f'box-shadow:0 0 6px rgba(76,166,107,.25);"></div></div>'
            )

        deadline_html = ""
        if DEADLINE_PASSED:
            deadline_html = '''<div style="margin-top:10px;padding:12px 16px;background:#1a0000;
  border:2px solid #c0392b;border-radius:3px;text-align:center;">
  <div style="font-family:'Share Tech Mono',monospace;font-size:10px;color:#c0392b;
    letter-spacing:2px;">🚫 PLAZO VENCIDO</div>
  <div style="font-family:'Share Tech Mono',monospace;font-size:7px;color:#ff6666;
    margin-top:6px;">TU NOTA NO SERÁ ACTUALIZADA</div></div>'''
        elif self._dni:
            deadline_html = ('<div style="margin-top:8px;font-family:\'Share Tech Mono\',monospace;'
                             'font-size:6px;color:#39e5b6;letter-spacing:1px;opacity:.85;">'
                             '📊 Calificación actualizada en la base de datos</div>')

        card_html = f'''<link href="https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap" rel="stylesheet">
<style>
  @keyframes pg-xpscale{{from{{transform:scaleX(0)}}to{{transform:scaleX(1)}}}}
</style>
<div style="background:#020d02;border:2px solid {border_color};border-radius:4px;max-width:840px;
  margin-bottom:14px;overflow:hidden;box-shadow:{glow},0 6px 24px rgba(0,0,0,.7);
  font-family:'Segoe UI',Roboto,sans-serif;">
  <div style="background:{border_color}18;border-bottom:1px solid {border_color}40;
    padding:9px 16px;display:flex;justify-content:space-between;align-items:center;">
    <div style="display:flex;align-items:center;gap:8px;">
      {_logo_sm}
      <span style="font-family:'Share Tech Mono',monospace;font-size:9px;
        color:{border_color};letter-spacing:1px;">{curr_icon} {curr_title}</span>
    </div>
    <div style="display:flex;align-items:center;gap:10px;">
      {stars_html}
      <div style="font-family:'Share Tech Mono',monospace;font-size:7px;color:#d4870a;
        background:rgba(212,135,10,.1);border:1px solid rgba(212,135,10,.4);
        padding:3px 8px;border-radius:2px;">MAX {max_pts} XP</div>
    </div>
  </div>
  <div style="padding:10px 14px 6px;">{rows_html}</div>
  <div style="background:#010801;border-top:1px solid #0a1a0a;padding:11px 14px;">
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:9px;">
      <div style="display:flex;align-items:center;gap:8px;">
        <span style="font-size:16px;">{s_icon}</span>
        <span style="font-family:'Share Tech Mono',monospace;font-size:8px;
          color:{s_color};">{s_text}</span>
        {combo_html}
      </div>
      <div style="display:flex;align-items:center;gap:4px;color:#2a3a2a;font-size:10px;">
        {dots}<span style="margin-left:3px;">{passed}/{len(checks)}</span>
      </div>
    </div>
    {xp_bar_html}
    {ach_html}
    {deadline_html}
  </div>
</div>'''
        display(HTML(card_html))

        for _ in levelup_ach:
            display(HTML(self._render_levelup(lvl_num, lvl_name)))

        return pts

    # ── Level-up banner (TLOU style) ─────────────────────────

    def _render_levelup(self, lvl_num, lvl_name):
        import random as _r
        _r.seed(lvl_num * 97 + 31)
        uid = f"lu{_r.randint(10000, 99999)}"

        _cfg = {
            2: dict(bg="linear-gradient(160deg,#0d0a00,#1e1000)",
                    c="#7a3000", sc="#cc5500", rc="#7a3000",
                    sub="CORREDOR — EL HONGO TE TIENE, PERO AÚN PIENSAS", icon="🍄"),
            3: dict(bg="linear-gradient(160deg,#150800,#2e1400)",
                    c="#cc5500", sc="#ff7722", rc="#cc5500",
                    sub="ACECHADOR — VES EN LA OSCURIDAD", icon="👁️"),
            4: dict(bg="linear-gradient(160deg,#001208,#002818)",
                    c="#2d7a45", sc="#4ca66b", rc="#2d7a45",
                    sub="FIREFLY — CUANDO YA NO QUEDEN LUCIÉRNAGAS...", icon="🔦"),
            5: dict(bg="linear-gradient(160deg,#001a0a,#003020)",
                    c="#4ca66b", sc="#39e5b6", rc="#4ca66b",
                    sub="AGENTE MARLENE — LA HUMANIDAD TE NECESITA", icon="🌿"),
            6: dict(bg="linear-gradient(160deg,#001208,#002010,#1a0800)",
                    c="#4ca66b", sc="#d4870a", rc="#39e5b6",
                    sub="PROYECTO ELLIE — INMUNE. AL ERROR. AL CAOS. A LA ENTROPÍA.", icon="⚡"),
        }
        cfg = _cfg.get(lvl_num, _cfg[2])
        c, sc, rc = cfg["c"], cfg["sc"], cfg["rc"]

        _sd = [(-50,-88),(0,-100),(50,-88),(92,-35),(78,55),(0,92),(-78,55),(-92,-35)]
        _bd = [(-4,-115),(115,0),(4,115),(-115,0)]
        spark_css, spark_html = "", ""
        for i, (dx, dy) in enumerate(_sd):
            d = 0.12 + i * 0.035
            sz = 4 if i % 2 == 0 else 3
            spark_css  += (f"@keyframes {uid}-s{i}{{0%{{transform:translate(0,0);opacity:1}}"
                           f"100%{{transform:translate({dx}px,{dy}px);opacity:0}}}}")
            spark_html += (f'<div style="position:absolute;top:50%;left:50%;width:{sz}px;height:{sz}px;'
                           f'border-radius:50%;background:{sc};margin:-{sz//2}px;opacity:0;'
                           f'animation:{uid}-s{i} .85s ease-out {d:.2f}s forwards;'
                           f'pointer-events:none;z-index:6;"></div>')
        for i, (dx, dy) in enumerate(_bd):
            d = 0.08 + i * 0.08
            spark_css  += (f"@keyframes {uid}-b{i}{{0%{{transform:translate(0,0);opacity:.9}}"
                           f"100%{{transform:translate({dx}px,{dy}px);opacity:0}}}}")
            spark_html += (f'<div style="position:absolute;top:50%;left:50%;width:6px;height:6px;'
                           f'border-radius:50%;background:{c};margin:-3px;opacity:0;'
                           f'animation:{uid}-b{i} 1.1s ease-out {d:.2f}s forwards;'
                           f'pointer-events:none;z-index:6;"></div>')

        extra_ring = ""
        if lvl_num == 6:
            extra_ring = (f'<div style="position:absolute;top:50%;left:50%;width:100px;height:100px;'
                          f'margin:-50px;border-radius:50%;border:2px solid #39e5b6;opacity:0;'
                          f'animation:{uid}-ring 1.6s ease-out .5s forwards;'
                          f'pointer-events:none;z-index:5;"></div>')

        return f'''<link href="https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap" rel="stylesheet">
<style>
  @keyframes {uid}-flash{{0%{{opacity:.6}}35%{{opacity:.15}}100%{{opacity:0}}}}
  @keyframes {uid}-ring {{0%{{transform:scale(.08);opacity:.95}}100%{{transform:scale(4.5);opacity:0}}}}
  @keyframes {uid}-icon {{
    0%  {{transform:scale(0) rotate(-25deg);opacity:0}}
    55% {{transform:scale(1.22) rotate(6deg);opacity:1}}
    72% {{transform:scale(0.91) rotate(-3deg)}}
    86% {{transform:scale(1.06) rotate(2deg)}}
    100%{{transform:scale(1) rotate(0deg)}}}}
  @keyframes {uid}-slam {{
    0%  {{transform:scaleX(3) scaleY(0.05);opacity:0;letter-spacing:16px}}
    55% {{transform:scaleX(1.04) scaleY(1.04);opacity:1}}
    100%{{transform:scale(1);letter-spacing:4px}}}}
  @keyframes {uid}-rise {{
    0%  {{transform:translateY(32px);opacity:0;filter:blur(6px)}}
    100%{{transform:translateY(0);opacity:1;filter:blur(0)}}}}
  @keyframes {uid}-sub  {{from{{opacity:0;letter-spacing:6px}}to{{opacity:1;letter-spacing:2px}}}}
  @keyframes {uid}-cl   {{from{{transform:translateX(-115%);opacity:0}}to{{transform:translateX(0);opacity:1}}}}
  @keyframes {uid}-cr   {{from{{transform:translateX(115%);opacity:0}}to{{transform:translateX(0);opacity:1}}}}
  @keyframes {uid}-rl   {{from{{opacity:0;transform:translateY(-50%) translateX(-36px)}}
                          to{{opacity:.16;transform:translateY(-50%) translateX(0)}}}}
  @keyframes {uid}-rr   {{from{{opacity:0;transform:translateY(-50%) translateX(36px)}}
                          to{{opacity:.16;transform:translateY(-50%) translateX(0)}}}}
  @keyframes {uid}-pulse{{0%,100%{{text-shadow:0 0 10px {c}88,2px 2px 0 #000}}
                          50%{{text-shadow:0 0 32px {c},0 0 64px {c}55,2px 2px 0 #000}}}}
  {spark_css}
</style>
<div style="position:relative;overflow:hidden;background:{cfg['bg']};
  border:2px solid {c};border-radius:6px;max-width:840px;margin:14px 0;
  box-shadow:0 0 55px {c}44,0 0 110px {c}11,0 12px 50px rgba(0,0,0,.97);">

  <div style="position:absolute;inset:0;background:{c};border-radius:4px;
    animation:{uid}-flash .55s ease-out forwards;pointer-events:none;z-index:20;"></div>

  <div style="position:absolute;top:50%;left:50%;width:90px;height:90px;margin:-45px;
    border-radius:50%;border:3px solid {rc};opacity:0;
    animation:{uid}-ring 1.05s ease-out .04s forwards;pointer-events:none;z-index:8;"></div>
  <div style="position:absolute;top:50%;left:50%;width:90px;height:90px;margin:-45px;
    border-radius:50%;border:2px solid {sc}cc;opacity:0;
    animation:{uid}-ring 1.35s ease-out .26s forwards;pointer-events:none;z-index:8;"></div>
  <div style="position:absolute;top:50%;left:50%;width:90px;height:90px;margin:-45px;
    border-radius:50%;border:1px solid {c}55;opacity:0;
    animation:{uid}-ring 1.65s ease-out .48s forwards;pointer-events:none;z-index:8;"></div>
  {extra_ring}

  {spark_html}

  <div style="position:absolute;left:14px;top:50%;
    font-size:14px;color:{c};letter-spacing:5px;opacity:.4;
    animation:{uid}-rl .9s ease-out .6s both;pointer-events:none;z-index:7;">
    ✦ ✧ ✦ ✧ ✦</div>
  <div style="position:absolute;right:14px;top:50%;
    font-size:14px;color:{c};letter-spacing:5px;opacity:.4;
    animation:{uid}-rr .9s ease-out .6s both;pointer-events:none;z-index:7;">
    ✧ ✦ ✧ ✦ ✧</div>

  <div style="position:relative;z-index:15;padding:42px 60px 32px;text-align:center;">
    <div style="font-size:54px;margin-bottom:16px;display:block;
      animation:{uid}-icon .68s cubic-bezier(.34,1.56,.64,1) .15s both;">
      {cfg['icon']}</div>
    <div style="font-family:'Share Tech Mono',monospace;font-size:9px;color:{c};
      letter-spacing:4px;margin-bottom:20px;
      animation:{uid}-slam .52s cubic-bezier(.22,.61,.36,1) .38s both;">
      ¡ASCENDISTE!</div>
    <div style="font-family:'Share Tech Mono',monospace;
      font-size:clamp(13px,2.8vw,20px);color:{c};letter-spacing:4px;margin-bottom:18px;
      text-shadow:0 0 20px {c}88,2px 2px 0 #000;
      animation:{uid}-rise .55s ease-out .72s both,
                {uid}-pulse 2.8s ease-in-out 1.3s infinite;">
      {lvl_name}</div>
    <div style="font-family:'Share Tech Mono',monospace;font-size:7px;
      color:#2a3a2a;letter-spacing:2px;
      animation:{uid}-sub .5s ease-out 1.0s both;">{cfg['sub']}</div>
    <div style="display:flex;align-items:center;margin-top:26px;overflow:hidden;">
      <div style="font-size:12px;color:{c};opacity:.3;letter-spacing:4px;flex-shrink:0;
        animation:{uid}-cl .6s ease-out .92s both;">⬡ ⬡ ⬡ ⬡ ⬡</div>
      <div style="flex:1;height:1px;background:linear-gradient(90deg,{c}60,{c}10);margin:0 8px;"></div>
      <div style="font-family:'Share Tech Mono',monospace;font-size:8px;color:{c};opacity:.65;
        animation:{uid}-rise .4s ease-out 1.1s both;">LV {lvl_num}</div>
      <div style="flex:1;height:1px;background:linear-gradient(90deg,{c}10,{c}60);margin:0 8px;"></div>
      <div style="font-size:12px;color:{c};opacity:.3;letter-spacing:4px;flex-shrink:0;
        animation:{uid}-cr .6s ease-out .92s both;">⬡ ⬡ ⬡ ⬡ ⬡</div>
    </div>
  </div>
</div>'''

    # ── Supabase submit ───────────────────────────────────────

    def _submit_to_supabase(self, earned, possible, pct, lvl_num, lvl_name, silent=False):
        if DEADLINE_PASSED:
            return
        if not self._dni:
            return
        try:
            import json as _json, urllib.request as _ur
            payload = _json.dumps({
                "email":           self._dni,
                "dni":             self._dni,
                "nombre":          self._nombre_real or "explorador",
                "grado":           self._grado or "",
                "notebook":        "nb3",
                "earned":          earned,
                "possible":        possible,
                "pct":             pct,
                "level_num":       lvl_num,
                "level_name":      lvl_name,
                "achievements":    list(self._achievements),
                "streak":          self._streak,
                "score_breakdown": {k: {"e": e, "p": p}
                                    for k, (e, p) in self._scores.items()},
            }).encode("utf-8")
            req = _ur.Request(
                f"{SUPABASE_URL}/rest/v1/submissions",
                data=payload,
                headers={
                    "apikey":        SUPABASE_ANON_KEY,
                    "Authorization": f"Bearer {SUPABASE_ANON_KEY}",
                    "Content-Type":  "application/json",
                    "Prefer":        "return=minimal",
                },
                method="POST",
            )
            with _ur.urlopen(req, timeout=12):
                pass
        except Exception:
            pass

    # ── Helper: render checkpoint summary ────────────────────

    def _render_checkpoint(self, title, sección, color):
        rows = ""
        total_e = total_p = 0
        for key, (label, max_p) in sección.items():
            e, p = self._scores.get(key, (0, max_p))
            total_e += e; total_p += p
            ok = e == p
            bar_pct = round(e / p * 100) if p else 0
            rows += (
                f'<div style="display:flex;align-items:center;gap:10px;margin-bottom:6px;">'
                f'<span style="font-size:12px;">{"✅" if ok else "⬜"}</span>'
                f'<div style="flex:1;">'
                f'<div style="font-size:11px;color:#b8ff9a;margin-bottom:3px;">{label}</div>'
                f'<div style="height:5px;background:#0a1a0a;border-radius:2px;overflow:hidden;">'
                f'<div style="width:{bar_pct}%;height:100%;'
                f'background:{color};opacity:.8;border-radius:2px;"></div></div>'
                f'</div>'
                f'<span style="font-family:\'Share Tech Mono\',monospace;font-size:7px;'
                f'color:{color if ok else "#2a3a2a"};">{e}/{p}</span>'
                f'</div>'
            )
        pct_sec = round(total_e / total_p * 100) if total_p else 0
        display(HTML(
            f'<link href="https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap" rel="stylesheet">'
            f'<div style="background:#020d02;border:2px solid {color};border-radius:4px;'
            f'max-width:840px;margin:10px 0;padding:18px 20px;'
            f'box-shadow:0 0 20px {color}22,0 4px 16px rgba(0,0,0,.6);">'
            f'<div style="font-family:\'Share Tech Mono\',monospace;font-size:9px;'
            f'color:{color};letter-spacing:2px;margin-bottom:16px;">✅ {title}</div>'
            f'{rows}'
            f'<div style="margin-top:14px;padding-top:10px;border-top:1px solid {color}30;'
            f'display:flex;justify-content:space-between;align-items:center;">'
            f'<span style="font-family:\'Share Tech Mono\',monospace;font-size:7px;color:#2a3a2a;">'
            f'ZONA: {total_e}/{total_p} XP</span>'
            f'<span style="font-family:\'Share Tech Mono\',monospace;font-size:9px;color:{color};">'
            f'{pct_sec}%</span>'
            f'</div></div>'
        ))

    # ═══════════════════════════════════════════════════════════
    # SECCIÓN 3.1 — Loops Anidados: Grids
    # ═══════════════════════════════════════════════════════════

    def check_ex1(self):
        """Ex1 — Expansión Radial del Cordyceps (6 pts)"""
        self._header("EJERCICIO 1 — Expansión Radial del Cordyceps", icon="🍄", pts=6)
        checks = []
        fila = _get("fila")
        col  = _get("col")

        # After a correct 6×6 loop, fila=5 and col=5
        if fila is None:
            checks.append((False, "loop exterior (fila)",
                           "Variable 'fila' no encontrada — ¿ejecutaste la celda? Usa: for fila in range(6)"))
        elif fila == 5:
            checks.append((True, "loop exterior — 6 filas", "✓ fila llegó a 5 (range(6))"))
        else:
            checks.append((False, "loop exterior — 6 filas",
                           f"fila={fila} — el loop exterior debe ser range(6) (0 a 5)"))

        if col is None:
            checks.append((False, "loop interior (col)",
                           "Variable 'col' no encontrada — usa: for col in range(6)"))
        elif col == 5:
            checks.append((True, "loop interior — 6 columnas", "✓ col llegó a 5 (range(6))"))
        else:
            checks.append((False, "loop interior — 6 columnas",
                           f"col={col} — el loop interior debe ser range(6) (0 a 5)"))

        # Spot-check: last cell (5,5) is distance 4 from center → NOT infected
        # We can verify the Manhattan distance variable if the student defined it
        dist = _get("distancia") or _get("dist") or _get("d")
        if dist is not None and not isinstance(dist, bool) and isinstance(dist, (int, float)):
            exp_last = abs(5 - 3) + abs(5 - 3)   # = 4
            if _approx(dist, exp_last):
                checks.append((True, "distancia Manhattan (última celda = 4)",
                               f"✓ abs(5-3)+abs(5-3) = {exp_last}"))
            else:
                checks.append((False, "distancia Manhattan",
                               f"La última celda (5,5) debe tener distancia 4, obtuve {dist}. "
                               f"Verifica: abs(fila-3)+abs(col-3)"))

        return self._award("ex1", checks, 6)

    def check_ex2(self):
        """Ex2 — Dos Patógenos, Mismo Mapa (6 pts)"""
        self._header("EJERCICIO 2 — Dos Patógenos, Mismo Mapa", icon="🍄", pts=6)
        checks = []
        # Expected infected counts: Cordyceps (radius≤2) = 13, COVID (radius≤1) = 5
        EXP_CORD  = 13
        EXP_COVID = 5

        fila = _get("fila")
        col  = _get("col")

        if fila == 5 and col == 5:
            checks.append((True, "loops 6×6 ejecutados", "✓ fila=5, col=5"))
        else:
            checks.append((False, "loops 6×6",
                           f"fila={fila}, col={col} — ambos loops deben ser range(6). "
                           f"¿Ejecutaste las dos cuadrículas?"))

        # Search for Cordyceps count (13)
        cord_found = False
        for name in ["infectadas_cord", "n_cord", "total_cord", "infectadas_cordyceps",
                     "infectadas1", "count_cord", "zonas_cord", "cord_count"]:
            v = _get(name)
            if isinstance(v, int) and not isinstance(v, bool):
                if v == EXP_CORD:
                    checks.append((True, f"Cordyceps infectadas = 13 ({name})", "✓ 13 zonas"))
                else:
                    checks.append((False, f"Cordyceps infectadas ({name}={v})",
                                   f"Debe ser 13 (radio≤2 desde centro (3,3)), obtuve {v}"))
                cord_found = True
                break
        if not cord_found:
            checks.append((False, "Cordyceps infectadas (variable no encontrada)",
                           f"Guarda el conteo en una variable, ej: infectadas_cord = 0. "
                           f"Debe ser {EXP_CORD}"))

        # Search for COVID count (5)
        covid_found = False
        for name in ["infectadas_covid", "n_covid", "total_covid", "infectadas_covid19",
                     "infectadas2", "count_covid", "zonas_covid", "covid_count", "infectadas"]:
            v = _get(name)
            if isinstance(v, int) and not isinstance(v, bool):
                if v == EXP_COVID:
                    checks.append((True, f"COVID-19 infectadas = 5 ({name})", "✓ 5 zonas"))
                else:
                    checks.append((False, f"COVID-19 infectadas ({name}={v})",
                                   f"Debe ser 5 (radio≤1 desde centro (3,3)), obtuve {v}"))
                covid_found = True
                break
        if not covid_found:
            checks.append((False, "COVID-19 infectadas (variable no encontrada)",
                           f"Guarda el conteo en una variable, ej: infectadas_covid = 0. "
                           f"Debe ser {EXP_COVID}"))

        return self._award("ex2", checks, 6)

    def check_debug1(self):
        """Debug1 — Error de Indentación (3 pts)"""
        self._header("🔧 DEBUG 1 — Error de Indentación", icon="🔧", pts=3)
        checks = []
        fila = _get("fila")
        col  = _get("col")
        zona = _get("zona")

        # After debug1 (range(3)×range(3)), fila=2, col=2, zona=8
        if fila is None:
            checks.append((False, "loop externo (fila)", "Variable 'fila' no encontrada — ¿ejecutaste la celda?"))
        elif fila == 2:
            checks.append((True, "loop externo range(3)", "✓ fila=2"))
        else:
            checks.append((False, "loop externo range(3)",
                           f"fila={fila} — el loop debe ser range(3). ¿Modificaste el código?"))

        if col is None:
            checks.append((False, "loop interno (col)", "Variable 'col' no encontrada"))
        elif col == 2:
            checks.append((True, "loop interno range(3)", "✓ col=2"))
        else:
            checks.append((False, "loop interno range(3)",
                           f"col={col} — el loop debe ser range(3)"))

        if zona is None:
            checks.append((False, "zona", "Variable 'zona' no encontrada — ¿ejecutaste la celda?"))
        elif zona == 8:
            checks.append((True, "zona == 8 (celda 2×3+2, última iteración)",
                           "✓ El loop procesó las 9 celdas — indentación correcta"))
        else:
            checks.append((False, "zona",
                           f"Debe ser 8 (última celda: 2*3+2=8), obtuve {zona}"))

        return self._award("debug1", checks, 3)

    def check_t1(self):
        """T1 — Ejecuciones del loop interior 6×5 (4 pts)"""
        self._header("❓ TEORÍA T1 — Ejecuciones del loop interior", icon="🧠", pts=4)
        checks = []
        r = _get("respuesta_t1")

        if r is None:
            checks.append((False, "respuesta_t1",
                           "No definida — escribe: respuesta_t1 = 'b'"))
        elif not isinstance(r, str):
            checks.append((False, "respuesta_t1", "Debe ser str, ej: respuesta_t1 = 'b'"))
        elif r.strip().lower() == "b":
            checks.append((True, "respuesta_t1 == 'b'",
                           "¡Correcto! 6 filas × 5 columnas = 30 ejecuciones"))
        else:
            checks.append((False, "respuesta_t1",
                           f"Incorrecto ('{r}'). Pista: el print interior ejecuta "
                           f"filas × columnas veces — 6 × 5 = ?"))

        return self._award("t1", checks, 4)

    def check_mini_a(self):
        """Checkpoint 3.1 — Loops Anidados: Grids"""
        self._checkpoints.add("mini_a")
        sección = {
            "ex1":    ("Expansión Radial del Cordyceps", 6),
            "ex2":    ("Dos Patógenos, Mismo Mapa",       6),
            "debug1": ("Debug 1 – Indentación",            3),
            "t1":     ("T1 – Teoría 3.1",                  4),
        }
        self._render_checkpoint("CHECKPOINT 3.1 — LOOPS ANIDADOS: GRIDS", sección, "#4ca66b")

    # ═══════════════════════════════════════════════════════════
    # SECCIÓN 3.2 — Loops Anidados: Tiempo
    # ═══════════════════════════════════════════════════════════

    def check_ex3(self):
        """Ex3 — Propagación en 5 Zonas (8 pts)"""
        self._header("EJERCICIO 3 — Propagación en 5 Zonas", icon="🍄", pts=8)
        checks = []
        # infectados=[5,12,3,20,8], poblaciones=[500,1200,300,2000,800], r0=1.8, dias=7
        # Expected after 7 days (in-place updates, capped at population):
        EXP_INFECTADOS  = [291, 685, 162, 1204, 469]
        EXP_TOTAL_DIA7  = 2811   # sum of EXP_INFECTADOS

        dia         = _get("dia")
        infectados  = _get("infectados")
        total       = _get("total_ciudad") or _get("total")

        if dia is None:
            checks.append((False, "loop exterior (dia)",
                           "Variable 'dia' no encontrada — usa: for dia in range(1, dias+1)"))
        elif dia == 7:
            checks.append((True, "loop exterior — 7 días", "✓ dia=7"))
        else:
            checks.append((False, "loop exterior — 7 días",
                           f"dia={dia} — el loop de días debe ir de 1 a {7}. ¿Usaste dias=7?"))

        if infectados is None:
            checks.append((False, "infectados (lista final)",
                           "Variable 'infectados' no encontrada — actualiza la lista del starter"))
        elif not isinstance(infectados, list) or len(infectados) != 5:
            checks.append((False, "infectados (lista final)",
                           f"Debe ser lista de 5 zonas, obtuve {type(infectados).__name__}"))
        elif infectados == EXP_INFECTADOS:
            checks.append((True, "infectados día 7",
                           f"✓ {infectados} — todas las zonas correctas"))
        else:
            wrong = [(i, EXP_INFECTADOS[i], infectados[i])
                     for i in range(5) if infectados[i] != EXP_INFECTADOS[i]]
            pos, e, o = wrong[0]
            checks.append((False, "infectados día 7",
                           f"Zona {pos}: esperaba {e}, obtuve {o}. "
                           f"Verifica: infectados[i] = min(int(infectados[i]*r0), poblaciones[i])"))

        if total is None:
            checks.append((False, "total_ciudad (día 7)",
                           f"Variable 'total_ciudad' no encontrada — suma los infectados de todas las zonas "
                           f"en cada día. Debe ser {EXP_TOTAL_DIA7}"))
        elif total == EXP_TOTAL_DIA7:
            checks.append((True, f"total_ciudad == {EXP_TOTAL_DIA7}", "✓ suma correcta del día 7"))
        else:
            checks.append((False, "total_ciudad",
                           f"Debe ser {EXP_TOTAL_DIA7}, obtuve {total}. "
                           f"Asegúrate de acumular DENTRO del loop de días, no dentro del de zonas"))

        return self._award("ex3", checks, 8)

    def check_ex4(self):
        """Ex4 — Tres Patógenos, Diez Días (8 pts)"""
        self._header("EJERCICIO 4 — Tres Patógenos, Diez Días", icon="🍄", pts=8)
        checks = []
        # Pathogens: COVID r0=2.5, Ébola r0=1.8, Sarampión r0=15.0
        # infectados_0=50, poblacion=50_000, 10 days
        # Expected day-10: COVID=50000 (cap), Ébola=17767, Sarampión=50000 (cap)
        EXP_EBOLA        = 17_767
        EXP_SARAM        = 50_000

        dia        = _get("dia")
        infectados = _get("infectados")

        if dia is None:
            checks.append((False, "loop interior (dia)",
                           "Variable 'dia' no encontrada — usa: for dia in range(1, 11)"))
        elif dia == 10:
            checks.append((True, "loop interior — 10 días", "✓ dia=10"))
        else:
            checks.append((False, "loop interior — 10 días",
                           f"dia={dia} — el loop de días debe llegar a 10"))

        # After 3 pathogens loop, infectados = Sarampión result = 50000 (at cap)
        if infectados is None:
            checks.append((False, "infectados (último patógeno)",
                           f"Variable 'infectados' no encontrada — "
                           f"Sarampión (R0=15) debe llegar a {EXP_SARAM} en día 3"))
        elif isinstance(infectados, (int, float)) and not isinstance(infectados, bool):
            if infectados == EXP_SARAM:
                checks.append((True, f"Sarampión saturó población ({EXP_SARAM})",
                               f"✓ R0=15 llega al techo en día 3 — impresionante"))
            elif infectados == EXP_EBOLA:
                checks.append((False, "orden de patógenos",
                               f"infectados={infectados} corresponde a Ébola — el último patógeno "
                               f"(Sarampión, R0=15) debe ser el último en el loop exterior"))
            else:
                checks.append((False, "infectados día 10",
                               f"Obtuve {infectados}. Ébola→{EXP_EBOLA}, COVID/Sarampión→{EXP_SARAM}"))
        else:
            checks.append((False, "infectados",
                           f"Debe ser int con el total del último patógeno, obtuve {type(infectados).__name__}"))

        return self._award("ex4", checks, 8)

    def check_debug2(self):
        """Debug2 — Acumulador en el Nivel Equivocado (3 pts)"""
        self._header("🔧 DEBUG 2 — Acumulador en el Nivel Equivocado", icon="🔧", pts=3)
        checks = []
        # Fixed: total_ciudad=0 at the DIA level → total after 3 days = 503
        # Buggy: total_ciudad=0 inside zone loop → total = last zone only = 168
        EXP_TOTAL_FIXED = 503
        EXP_TOTAL_BUGGY = 168

        total_ciudad = _get("total_ciudad")
        dia          = _get("dia")

        if total_ciudad is None:
            checks.append((False, "total_ciudad",
                           "Variable 'total_ciudad' no encontrada — ¿ejecutaste la celda de Debug 2?"))
        elif total_ciudad == EXP_TOTAL_FIXED:
            checks.append((True, f"total_ciudad == {EXP_TOTAL_FIXED} (acumulador en nivel correcto)",
                           "✓ total_ciudad = 0 está ANTES del loop de zonas, no dentro"))
        elif total_ciudad == EXP_TOTAL_BUGGY:
            checks.append((False, "total_ciudad",
                           f"total_ciudad={EXP_TOTAL_BUGGY} — el bug sigue presente. "
                           f"Mueve 'total_ciudad = 0' al nivel del loop de días (debe ser {EXP_TOTAL_FIXED})"))
        else:
            checks.append((False, "total_ciudad",
                           f"Debe ser {EXP_TOTAL_FIXED} (corregido) o {EXP_TOTAL_BUGGY} (bug), "
                           f"obtuve {total_ciudad}. ¿Modificaste los datos del ejercicio?"))

        if dia is None:
            checks.append((False, "dia", "Variable 'dia' no encontrada — ¿ejecutaste la celda?"))
        elif dia == 3:
            checks.append((True, "loop días — range(1, 4)", "✓ dia=3"))
        else:
            checks.append((False, "dia",
                           f"Debe ser 3 (dias=3), obtuve {dia}. ¿Modificaste el código?"))

        return self._award("debug2", checks, 3)

    def check_debug2b(self):
        """Debug2B — El Error que Mató a 50 Millones (3 pts)"""
        self._header("🔧 DEBUG 2B — El Error que Mató a 50 Millones", icon="🔧", pts=3)
        checks = []
        # After fix: Ola 2 starts from where Ola 1 ended (not reset to infectados_0)
        # Both buggy and fixed end with infectados=100000 (cap) after Ola 2
        # Structural check: both olas ran to completion

        ola        = _get("ola")
        dia        = _get("dia")
        infectados = _get("infectados")

        if ola is None:
            checks.append((False, "loop olas",
                           "Variable 'ola' no encontrada — ¿ejecutaste la celda de Debug 2B?"))
        elif ola == 2:
            checks.append((True, "ambas olas ejecutadas (ola=2)", "✓ el loop corrió 2 olas"))
        else:
            checks.append((False, "ambas olas",
                           f"ola={ola} — el loop debe completar ambas olas (range(1,3))"))

        if dia is None:
            checks.append((False, "loop días (dia)",
                           "Variable 'dia' no encontrada — usa: for dia in range(1, dias_por_ola+1)"))
        elif dia == 10:
            checks.append((True, "loop días — 10 por ola (dia=10)", "✓"))
        else:
            checks.append((False, "loop días",
                           f"dia={dia} — cada ola tiene 10 días"))

        return self._award("debug2b", checks, 3)

    def check_ex5(self):
        """Ex5 — Las Dos Olas de 1918 (8 pts)"""
        self._header("EJERCICIO 5 — Las Dos Olas de 1918", icon="🍄", pts=8)
        checks = []
        # poblacion=100_000, r0=2.0, dias=10
        # Ola 1: start=100 → day 10 = 100000 (hits cap day 10)
        # Ola 2: start=5000 → day 10 = 100000 (hits cap day 5)
        # diferencia = abs(100000 - 100000) = 0
        EXP_OLA1_DIA10  = 100_000
        EXP_OLA2_DIA10  = 100_000
        EXP_DIFERENCIA  = 0

        dia        = _get("dia")
        infectados = _get("infectados")

        if dia is None:
            checks.append((False, "loop días (dia)",
                           "Variable 'dia' no encontrada — usa: for dia in range(1, dias+1)"))
        elif dia == 10:
            checks.append((True, "loop días — 10 días (dia=10)", "✓"))
        else:
            checks.append((False, "loop días",
                           f"dia={dia} — el loop de días debe llegar a 10"))

        if infectados is None:
            checks.append((False, "infectados (última ola, día 10)",
                           "No encontré 'infectados' — ¿ejecutaste la celda?"))
        elif isinstance(infectados, (int, float)) and not isinstance(infectados, bool):
            if infectados == EXP_OLA2_DIA10:
                checks.append((True, f"Ola 2 día 10 = {EXP_OLA2_DIA10} (saturó población)",
                               "✓ R0=2.0, inicio=5000 → saturación en día 5"))
            else:
                checks.append((False, "infectados (Ola 2 día 10)",
                               f"Debe ser {EXP_OLA2_DIA10} (ambas olas saturan con R0=2.0), "
                               f"obtuve {infectados}"))
        else:
            checks.append((False, "infectados", f"Debe ser int, obtuve {type(infectados).__name__}"))

        # Check difference between olas (expected = 0, both saturate)
        diff = None
        for name in ["diferencia", "diff", "diferencia_olas", "dif"]:
            v = _get(name)
            if isinstance(v, (int, float)) and not isinstance(v, bool):
                diff = (name, v)
                break
        if diff is None:
            checks.append((False, "diferencia ola1 vs ola2",
                           f"Variable 'diferencia' no encontrada — "
                           f"calcula: diferencia = infectados_ola1 - infectados_ola2. "
                           f"Resultado: {EXP_DIFERENCIA} (ambas olas llegan al mismo techo)"))
        elif diff[1] == EXP_DIFERENCIA:
            checks.append((True, f"diferencia == 0 ({diff[0]})",
                           "✓ Ambas olas saturan la ciudad — la velocidad cambia, el destino no"))
        else:
            checks.append((False, f"diferencia ({diff[0]}={diff[1]})",
                           f"Debe ser {EXP_DIFERENCIA} — ambas olas alcanzan la población máxima. "
                           f"¿Calculaste las diferencias al día 10?"))

        return self._award("ex5", checks, 8)

    def check_mini_b(self):
        """Checkpoint 3.2 — Loops Anidados: Tiempo"""
        self._checkpoints.add("mini_b")
        sección = {
            "ex3":     ("Propagación en 5 Zonas",             8),
            "ex4":     ("Tres Patógenos, Diez Días",           8),
            "debug2":  ("Debug 2 – Acumulador",                3),
            "debug2b": ("Debug 2B – Gripe 1918",               3),
            "ex5":     ("Las Dos Olas de 1918",                8),
        }
        self._render_checkpoint("CHECKPOINT 3.2 — LOOPS ANIDADOS: TIEMPO", sección, "#d4870a")

    # ═══════════════════════════════════════════════════════════
    # SECCIÓN 3.3 — Ifs Anidados: Triage
    # ═══════════════════════════════════════════════════════════

    def check_ex6(self):
        """Ex6 — Clasificador de Triage (8 pts)"""
        self._header("EJERCICIO 6 — Clasificador de Triage", icon="🔴", pts=8)

        resultado   = _get("resultado")
        infectado   = _get("infectado")
        horas       = _get("horas_expuesto")

        # Expected classifications for all 6 patients in order
        _expected = [
            "LIMPIO",
            "INMUNE — CASO DE ESTUDIO",
            "CUARENTENA TEMPRANA",
            "CUARENTENA TEMPRANA",
            "CUARENTENA TARDÍA",
            "CASO PERDIDO",
        ]

        # Search for a list of 6 classification results
        _list_names = [
            "clasificaciones", "resultados", "clases", "triage_resultados",
            "lista_resultados", "outputs", "todas", "mis_resultados",
            "lista_clasificaciones", "clasificacion_pacientes",
        ]
        _rlist = None
        for _n in _list_names:
            _v = _get(_n)
            if isinstance(_v, list) and len(_v) == 6:
                _rlist = _v
                break

        # Check 1: last patient (Paciente 6: infectado=True, horas=48, sin recursos) → CASO PERDIDO
        c1 = isinstance(resultado, str) and resultado.strip().upper() == "CASO PERDIDO"

        # Check 2: loop variable state confirms all 6 patients were processed
        c2 = (infectado is True or infectado == True) and horas == 48

        # Check 3: classification list exists and contains CUARENTENA TARDÍA (patient 5)
        c3 = (_rlist is not None and
              any(isinstance(r, str) and "CUARENTENA TARDÍA" in r.upper() for r in _rlist))

        # Check 4: classification list contains INMUNE — CASO DE ESTUDIO (patient 2)
        c4 = (_rlist is not None and
              any(isinstance(r, str) and "INMUNE" in r.upper() for r in _rlist))

        return self._award("ex6", [
            (c1, "Paciente 6 — CASO PERDIDO",
             f"resultado='{resultado}'" if resultado else "resultado no encontrado"),
            (c2, "Loop completo (6 pacientes)",
             f"infectado={infectado}, horas_expuesto={horas} (esperado True, 48)"),
            (c3, "Lista — CUARENTENA TARDÍA",
             "lista de 6 clasificaciones incluye CUARENTENA TARDÍA" if c3
             else "no se encontró lista con CUARENTENA TARDÍA"),
            (c4, "Lista — INMUNE",
             "lista incluye INMUNE — CASO DE ESTUDIO" if c4
             else "no se encontró lista con INMUNE — CASO DE ESTUDIO"),
        ], 8)

    def check_debug3(self):
        """Debug3 — Error de Árbol (3 pts)"""
        self._header("🔧 DEBUG 3 — Error de Árbol", icon="🔧", pts=3)

        resultado        = _get("resultado")
        infectado        = _get("infectado")
        horas_expuesto   = _get("horas_expuesto")
        recursos_medicos = _get("recursos_medicos")

        # After fix: horas=10 <24, recursos=True → "Cuarentena temprana — recursos OK"
        EXP = "Cuarentena temprana — recursos OK"

        c1 = isinstance(resultado, str) and resultado.strip() == EXP
        # Confirm inputs were not changed (fix is structural, not input-gaming)
        c2 = (infectado is True or infectado == True)
        c3 = horas_expuesto == 10 and (recursos_medicos is True or recursos_medicos == True)

        return self._award("debug3", [
            (c1, "Resultado correcto",
             f"resultado='{resultado}' esperado='{EXP}'"),
            (c2, "Entrada preservada — infectado=True",
             f"infectado={infectado} (no cambies la entrada, solo la estructura)"),
            (c3, "Entradas preservadas — horas=10, recursos=True",
             f"horas_expuesto={horas_expuesto}, recursos_medicos={recursos_medicos}"),
        ], 3)

    def check_ex7(self):
        """Ex7 — Clasificador de Zonas (8 pts)"""
        self._header("EJERCICIO 7 — Clasificador de Zonas", icon="🍄", pts=8)

        resultado            = _get("resultado")
        cfr                  = _get("cfr")
        infectados           = _get("infectados")
        poblacion            = _get("poblacion")
        dias_sin_suministros = _get("dias_sin_suministros")

        # Prueba 2 (Ébola): infectados=800, poblacion=5000, dias=4, cfr=0.65
        #   tasa = 800/5000 = 0.16 (16%)  — not >60%
        #   cfr = 0.65 > 0.5 → ZONA PERDIDA ✓
        EXP_EBOLA = "ZONA PERDIDA"

        # Check 1: Ébola test result (last cell test)
        c1 = isinstance(resultado, str) and resultado.strip().upper() == EXP_EBOLA.upper()

        # Check 2: Ébola CFR (mortalidad[3] = 0.65) was last value used
        c2 = _approx(cfr, 0.65) if cfr is not None else False

        # Check 3: inputs match the exercise spec (not modified by student)
        c3 = (infectados == 800 and poblacion == 5000 and dias_sin_suministros == 4)

        # Check 4: COVID prueba result (tasa=16%, dias_sin_sum=4>3 → ZONA ROJA)
        _covid_names = [
            "resultado_covid", "resultado1", "zona_covid", "zona1",
            "resultado_1", "r1", "z1", "resultado_c", "zona_c",
            "resultado_prueba1", "zona_prueba1",
        ]
        _r_covid = next((_get(n) for n in _covid_names
                         if isinstance(_get(n), str) and _get(n).strip().upper() == "ZONA ROJA"),
                        None)
        c4 = _r_covid is not None

        return self._award("ex7", [
            (c1, "Ébola → ZONA PERDIDA",
             f"resultado='{resultado}' (cfr=0.65>0.5 activa ZONA PERDIDA)"),
            (c2, "CFR Ébola (0.65)",
             f"cfr={cfr} esperado≈0.65"),
            (c3, "Datos de zona correctos",
             f"infectados={infectados}, poblacion={poblacion}, dias={dias_sin_suministros}"),
            (c4, "COVID → ZONA ROJA (variable separada)",
             "encontrado resultado_covid/zona1/etc='ZONA ROJA'" if c4
             else "guarda el resultado de COVID en una variable separada (resultado_covid, zona1…)"),
        ], 8)

    def check_t2(self):
        """T2 — Teoría Sección 3.3 (4 pts)"""
        self._header("❓ TEORÍA T2", icon="🧠", pts=4)

        r = _get("respuesta_t2")
        c1 = isinstance(r, str) and r.strip().lower() == "b"

        return self._award("t2", [
            (c1, "Respuesta T2",
             f"respuesta_t2='{r}' esperado='b' — el if anidado solo se evalúa si el exterior es True"),
        ], 4)

    def check_mini_c(self):
        """Checkpoint 3.3 — Ifs Anidados: Triage"""
        self._checkpoints.add("mini_c")
        sección = {
            "ex6":    ("Clasificador de Triage",    8),
            "debug3": ("Debug 3 – Error de Árbol",  3),
            "ex7":    ("Clasificador de Zonas",      8),
            "t2":     ("T2 – Teoría 3.3",            4),
        }
        self._render_checkpoint("CHECKPOINT 3.3 — IFS ANIDADOS: TRIAGE", sección, "#c0392b")

    # ═══════════════════════════════════════════════════════════
    # SECCIÓN 3.4 — Puente: Loops + Ifs
    # ═══════════════════════════════════════════════════════════

    def check_ex8(self):
        """Ex8 — Protocolo de Cuarentena con Intervención (10 pts)"""
        self._header("EJERCICIO 8 — Protocolo de Cuarentena con Intervención", icon="🏙️", pts=10)

        dia          = _get("dia")
        infectados_z = _get("infectados_z")
        zonas_caidas = _get("zonas_caidas")
        dia_q        = _get("dia_cuarentena")

        # Both valid final states (dia_cuarentena=5 or dia_cuarentena=14)
        _INF_DQ5  = [3905, 1950, 7812, 1167, 7812]   # dq=5: zone 3 survives
        _INF_DQ14 = [3905, 1950, 7812, 2000, 7812]   # dq=14: all fall

        # Search common total variable names for last-day total
        _tot_names = ["total", "total_infectados", "total_ciudad",
                      "totales", "total_dia", "t_infectados"]
        _tot = None
        for _n in _tot_names:
            _v = _get(_n)
            if isinstance(_v, list) and len(_v) == 21:
                _tot = _v[-1]
                break
            if isinstance(_v, (int, float)) and _v in (22646, 23479):
                _tot = int(_v)
                break

        # Check 1: simulation ran all 21 days
        c1 = dia == 21

        # Check 2: zones 0, 1, 2 always fall — correct regardless of dia_cuarentena
        c2 = (isinstance(infectados_z, list) and len(infectados_z) == 5
              and infectados_z[0] == 3905
              and infectados_z[2] == 7812)

        # Check 3: zone 3 result (key difference between the two valid runs)
        c3 = (isinstance(infectados_z, list) and len(infectados_z) == 5
              and infectados_z[3] in (1167, 2000))

        # Check 4: zonas_caidas tracking list is correct shape
        c4 = (isinstance(zonas_caidas, list) and len(zonas_caidas) == 5
              and zonas_caidas[0] is True and zonas_caidas[2] is True)

        # Check 5: total infectados for the last day matches either valid run
        c5 = _tot in (22646, 23479)

        def _inf_str():
            if isinstance(infectados_z, list):
                return str(infectados_z)
            return "infectados_z no encontrado"

        return self._award("ex8", [
            (c1, "21 días simulados",
             f"dia={dia} (esperado 21)"),
            (c2, "Zonas 0 y 2 correctas",
             f"infectados_z[0]={infectados_z[0] if isinstance(infectados_z,list) and len(infectados_z)>0 else '?'}, "
             f"infectados_z[2]={infectados_z[2] if isinstance(infectados_z,list) and len(infectados_z)>2 else '?'}"),
            (c3, "Zona 3 — clave de la cuarentena",
             f"infectados_z[3]={infectados_z[3] if isinstance(infectados_z,list) and len(infectados_z)>3 else '?'} "
             f"(1167→dq=5 salva la zona | 2000→dq=14 cae)"),
            (c4, "zonas_caidas correcto",
             f"zonas_caidas={zonas_caidas if isinstance(zonas_caidas,list) else 'no encontrado'}"),
            (c5, "Total ciudad último día",
             f"total={_tot} (esperado 22646 ó 23479)" if _tot is not None
             else "no se encontró variable total (totales, total_infectados…)"),
        ], 10)

    def check_debug4(self):
        """Debug4 — Dos Errores (3 pts)"""
        self._header("🔧 DEBUG 4 — Dos Errores", icon="🔧", pts=3)

        total_infectados = _get("total_infectados")
        dia              = _get("dia")
        zonas_inf        = _get("zonas_inf")

        # Fixed expected state after 5 days with r0=2.0
        EXP_TOTAL = 13000
        EXP_ZONAS = [2000, 3000, 1500, 4000, 2500]

        # Check 1: Bug 1 fixed — accumulator at outer loop level → correct total
        c1 = total_infectados == EXP_TOTAL

        # Check 2: loop ran 5 days
        c2 = dia == 5

        # Check 3: zone updates correct (same in both buggy/fixed; validates cell ran)
        c3 = zonas_inf == EXP_ZONAS

        return self._award("debug4", [
            (c1, "Total infectados correcto",
             f"total_infectados={total_infectados} "
             f"(esperado {EXP_TOTAL} — mueve 'total_infectados=0' fuera del loop interior)"),
            (c2, "Loop completó 5 días",
             f"dia={dia} (esperado 5)"),
            (c3, "Zonas actualizadas",
             f"zonas_inf={zonas_inf} (esperado {EXP_ZONAS})"),
        ], 3)

    def check_mini_d(self):
        """Checkpoint 3.4 — Puente: Loops + Ifs"""
        self._checkpoints.add("mini_d")
        sección = {
            "ex8":    ("Protocolo de Cuarentena", 10),
            "debug4": ("Debug 4 – Dos Errores",    3),
        }
        self._render_checkpoint("CHECKPOINT 3.4 — PUENTE: LOOPS + IFS", sección, "#39e5b6")

    # ═══════════════════════════════════════════════════════════
    # SECCIÓN 3.5 — Funciones
    # ═══════════════════════════════════════════════════════════

    def check_ex9(self):
        """Ex9 — clasificar_zona como función (6 pts)"""
        self._header("EJERCICIO 9 — clasificar_zona como función", icon="🍄", pts=6)
        # TODO: fill in Section 3.5
        return self._award("ex9", [
            (False, "pendiente", "Verificador en construcción — ¡vuelve pronto!"),
        ], 6)

    def check_debug5(self):
        """Debug5 — return faltante (3 pts)"""
        self._header("🔧 DEBUG 5 — return faltante", icon="🔧", pts=3)
        # TODO: fill in Section 3.5
        return self._award("debug5", [
            (False, "pendiente", "Verificador en construcción"),
        ], 3)

    def check_ex10(self):
        """Ex10 — simular_dia y tabla comparativa (8 pts)"""
        self._header("EJERCICIO 10 — simular_dia y tabla comparativa", icon="🍄", pts=8)
        # TODO: fill in Section 3.5
        return self._award("ex10", [
            (False, "pendiente", "Verificador en construcción — ¡vuelve pronto!"),
        ], 8)

    def check_ex11(self):
        """Ex11 — Motor de Intervención (10 pts)"""
        self._header("EJERCICIO 11 — Motor de Intervención", icon="🍄", pts=10)
        # TODO: fill in Section 3.5
        return self._award("ex11", [
            (False, "pendiente", "Verificador en construcción — ¡vuelve pronto!"),
        ], 10)

    def check_t3(self):
        """T3 — Teoría Sección 3.5 (4 pts)"""
        self._header("❓ TEORÍA T3", icon="🧠", pts=4)
        # TODO: fill in Section 3.5
        return self._award("t3", [
            (False, "pendiente", "Verificador en construcción"),
        ], 4)

    def check_mini_e(self):
        """Checkpoint 3.5 — Funciones"""
        self._checkpoints.add("mini_e")
        sección = {
            "ex9":    ("clasificar_zona como función",      6),
            "debug5": ("Debug 5 – return faltante",         3),
            "ex10":   ("simular_dia y tabla comparativa",   8),
            "ex11":   ("Motor de Intervención",            10),
            "t3":     ("T3 – Teoría 3.5",                   4),
        }
        self._render_checkpoint("CHECKPOINT 3.5 — FUNCIONES", sección, "#4ca66b")

    # ═══════════════════════════════════════════════════════════
    # PARTE 2 — Ejercicios de Integración
    # ═══════════════════════════════════════════════════════════

    def check_intex1(self):
        """IntEx1 — Perfil del Paciente Cero (6 pts)"""
        self._header("INTEGRACIÓN 1 — Perfil del Paciente Cero", icon="✦", pts=6)
        # TODO: fill in Part 2
        return self._award("intex1", [
            (False, "pendiente", "Verificador en construcción — ¡vuelve pronto!"),
        ], 6)

    def check_intex2(self):
        """IntEx2 — Mapa de Propagación Urbana (8 pts)"""
        self._header("INTEGRACIÓN 2 — Mapa de Propagación Urbana", icon="✦", pts=8)
        # TODO: fill in Part 2
        return self._award("intex2", [
            (False, "pendiente", "Verificador en construcción — ¡vuelve pronto!"),
        ], 8)

    def check_intex3(self):
        """IntEx3 — Comparador de Pandemias (8 pts)"""
        self._header("INTEGRACIÓN 3 — Comparador de Pandemias", icon="✦", pts=8)
        # TODO: fill in Part 2
        return self._award("intex3", [
            (False, "pendiente", "Verificador en construcción — ¡vuelve pronto!"),
        ], 8)

    def check_intex4(self):
        """IntEx4 — Protocolo de Cuarentena (10 pts)"""
        self._header("INTEGRACIÓN 4 — Protocolo de Cuarentena", icon="✦", pts=10)
        # TODO: fill in Part 2
        return self._award("intex4", [
            (False, "pendiente", "Verificador en construcción — ¡vuelve pronto!"),
        ], 10)

    def check_intex5(self):
        """IntEx5 — Motor de Simulación Epidemiológica / capstone (12 pts)"""
        self._header("INTEGRACIÓN 5 — Motor de Simulación Epidemiológica", icon="✦", pts=12)
        # TODO: fill in Part 2
        return self._award("intex5", [
            (False, "pendiente", "Verificador en construcción — ¡vuelve pronto!"),
        ], 12)

    # ═══════════════════════════════════════════════════════════
    # BONUS — Retos opcionales
    # ═══════════════════════════════════════════════════════════

    def check_reto1(self):
        """Reto1 — Días hasta colapso (6 pts, bonus)"""
        self._header("🌟 RETO 1 — Días hasta Colapso (BONUS)", icon="🌟", pts=6)
        # TODO: fill in Bonus
        return self._award("reto1", [
            (False, "pendiente", "Verificador en construcción — ¡vuelve pronto!"),
        ], 6)

    def check_reto2(self):
        """Reto2 — Motor SIR completo (6 pts, bonus)"""
        self._header("🌟 RETO 2 — Motor SIR Completo (BONUS)", icon="🌟", pts=6)
        # TODO: fill in Bonus
        return self._award("reto2", [
            (False, "pendiente", "Verificador en construcción — ¡vuelve pronto!"),
        ], 6)

    # ═══════════════════════════════════════════════════════════
    # RESUMEN FINAL
    # ═══════════════════════════════════════════════════════════

    def resumen(self):
        _, _, pct         = self._totals()
        n                 = self._nombre()
        lvl_num, lvl_name = _level_info(pct)
        core_earned       = sum(e for k, (e, _) in self._scores.items() if k not in _BONUS_KEYS)
        bonus_earned      = sum(e for k, (e, _) in self._scores.items() if k in _BONUS_KEYS)
        bonus_possible    = sum(p for k, (_, p) in self._scores.items() if k in _BONUS_KEYS)
        core_pct          = min(round(core_earned / _CORE_MAX * 100), 100)

        if core_pct >= 96:
            final_msg = (f"⚡ PROYECTO ELLIE. {n.upper()}, eres la última esperanza de la humanidad. "
                         f"El modelo SIR es tuyo.")
        elif core_pct >= 81:
            final_msg = (f"🌿 AGENTE MARLENE. {n}, la humanidad te necesita. "
                         f"Revisa los ✖ para completar la misión.")
        elif core_pct >= 61:
            final_msg = (f"🔦 EXPLORADOR FIREFLY. {n}, vas bien. "
                         f"Cuando ya no queden luciérnagas, tú seguirás encendiendo.")
        elif core_pct >= 41:
            final_msg = (f"👁️ ACECHADOR. {n}, ves en la oscuridad pero el hongo aún te frena. "
                         f"Practica los loops anidados.")
        elif core_pct >= 21:
            final_msg = (f"🍄 CORREDOR. {n}, el hongo te tiene pero aún piensas. "
                         f"Relee la teoría y vuelve a intentar.")
        else:
            final_msg = (f"☠️ {n}, paciente cero. Cada celda ejecutada es un día de cuarentena cumplido. "
                         f"¡Tú puedes!")

        ach_display = {
            "primer_contagio":     "🍄 Primer Contagio",
            "ojo_clinico":         "🩺 Ojo Clínico",
            "superviviente_zona":  "🚧 Superviviente de Zona",
            "esporas":             "💨 Esporas",
            "modelo_sir":          "📈 Modelo SIR",
            "inmunidad_adaptativa":"🧬 Inmunidad Adaptativa",
            "esperanza_humanidad": "✦ Esperanza de la Humanidad",
        }

        ach_html = ""
        if self._achievements:
            for ak, alabel in ach_display.items():
                if ak in self._achievements:
                    ach_html += (
                        f'<div style="display:inline-flex;align-items:center;gap:5px;'
                        f'padding:3px 8px;background:rgba(76,166,107,.08);'
                        f'border:1px solid #4ca66b40;border-radius:2px;margin:2px;">'
                        f'<span style="font-family:\'Share Tech Mono\',monospace;font-size:6px;'
                        f'color:#4ca66b;">{alabel}</span></div>'
                    )

        lv_color = _lv_color(lvl_num)
        xp_grad  = _XP_GRAD.get(lvl_num, _XP_GRAD[1])

        self._submit_to_supabase(core_earned, _CORE_MAX, core_pct, lvl_num, lvl_name)

        display(HTML(f'''
<link href="https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap" rel="stylesheet">
<style>
  @keyframes tlou-glow{{0%,100%{{text-shadow:0 0 14px rgba(76,166,107,.8),2px 2px 0 #0d2d10}}
    50%{{text-shadow:0 0 32px rgba(76,166,107,1),0 0 60px rgba(212,135,10,.4),2px 2px 0 #0d2d10}}}}
  @keyframes tlou-xp{{from{{transform:scaleX(0)}}to{{transform:scaleX(1)}}}}
</style>
<div style="background:#020d02;border:2px solid #4ca66b;border-radius:6px;max-width:840px;
  margin:12px 0;overflow:hidden;
  box-shadow:0 0 40px rgba(76,166,107,.12),0 0 80px rgba(212,135,10,.06),0 10px 40px rgba(0,0,0,.8);">

  <div style="background:linear-gradient(135deg,#010801,#011a06,#010801);
    border-bottom:2px solid #d4870a;padding:22px 28px;text-align:center;position:relative;">
    <div style="position:absolute;left:20px;top:50%;transform:translateY(-50%);">{self._logo_tag}</div>
    <div style="font-family:'Share Tech Mono',monospace;font-size:clamp(12px,2.5vw,18px);
      color:#4ca66b;animation:tlou-glow 2.5s ease-in-out infinite;letter-spacing:3px;
      margin-bottom:8px;">✦ FIREFLY RESEARCH NODE 7 ✦</div>
    <div style="font-family:'Share Tech Mono',monospace;font-size:8px;color:#d4870a;
      letter-spacing:2px;">NOTEBOOK III — RESUMEN FINAL DE MISIÓN</div>
    <div style="position:absolute;right:20px;top:50%;transform:translateY(-50%);">{self._logo_tag}</div>
  </div>

  <div style="padding:24px 28px;">
    <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;margin-bottom:20px;">
      <div style="background:#010801;border:1px solid #0a1a0a;border-radius:3px;
        padding:16px;text-align:center;">
        <div style="font-family:'Share Tech Mono',monospace;font-size:7px;color:#2a3a2a;
          letter-spacing:1px;margin-bottom:10px;">XP CORE</div>
        <div style="font-family:'Share Tech Mono',monospace;font-size:clamp(14px,3vw,22px);
          color:#4ca66b;">{core_earned}/{_CORE_MAX}</div>
      </div>
      <div style="background:#010801;border:1px solid #0a1a0a;border-radius:3px;
        padding:16px;text-align:center;">
        <div style="font-family:'Share Tech Mono',monospace;font-size:7px;color:#2a3a2a;
          letter-spacing:1px;margin-bottom:10px;">NIVEL</div>
        <div style="font-family:'Share Tech Mono',monospace;font-size:clamp(7px,1.4vw,11px);
          color:{lv_color};">{lvl_name}</div>
      </div>
      <div style="background:#010801;border:1px solid #0a1a0a;border-radius:3px;
        padding:16px;text-align:center;">
        <div style="font-family:'Share Tech Mono',monospace;font-size:7px;color:#2a3a2a;
          letter-spacing:1px;margin-bottom:10px;">SCORE</div>
        <div style="font-family:'Share Tech Mono',monospace;font-size:clamp(14px,3vw,22px);
          color:#b8ff9a;">{core_pct}%</div>
      </div>
    </div>

    <div style="margin-bottom:20px;">
      <div style="display:flex;justify-content:space-between;margin-bottom:6px;">
        <span style="font-family:'Share Tech Mono',monospace;font-size:7px;color:#2a3a2a;">
          PROGRESO CORE</span>
        <span style="font-family:'Share Tech Mono',monospace;font-size:7px;color:{lv_color};">
          {core_pct}%</span>
      </div>
      <div style="width:100%;height:14px;background:#0a1a0a;border:1px solid #1a2a1a;
        border-radius:3px;overflow:hidden;">
        <div style="width:{core_pct}%;height:100%;background:{xp_grad};
          border-radius:3px;transform-origin:left;
          animation:tlou-xp 1.4s cubic-bezier(.4,0,.2,1) forwards;
          box-shadow:0 0 8px rgba(76,166,107,.3);"></div>
      </div>
    </div>

    {f"""
    <div style="margin-bottom:20px;padding:12px 16px;background:#010801;
      border:1px solid #39e5b640;border-radius:3px;">
      <div style="font-family:'Share Tech Mono',monospace;font-size:7px;color:#39e5b6;
        margin-bottom:8px;">✧ BONUS XP</div>
      <div style="font-family:'Share Tech Mono',monospace;font-size:12px;color:#39e5b6;">
        {bonus_earned}/{bonus_possible} XP</div>
    </div>""" if bonus_possible > 0 else ""}

    <div style="background:#010801;border:1px solid #2d5a1b;border-radius:3px;
      padding:14px 18px;margin-bottom:20px;text-align:center;">
      <div style="font-size:13px;color:#b8ff9a;line-height:1.7;">{final_msg}</div>
    </div>

    {f"""
    <div style="margin-bottom:16px;">
      <div style="font-family:'Share Tech Mono',monospace;font-size:7px;color:#2a3a2a;
        letter-spacing:1px;margin-bottom:10px;">✦ LOGROS DESBLOQUEADOS</div>
      <div style="display:flex;flex-wrap:wrap;gap:4px;">{ach_html}</div>
    </div>""" if ach_html else ""}

    {"""
    <div style="padding:12px 16px;background:#1a0000;border:2px solid #c0392b;
      border-radius:3px;text-align:center;">
      <div style="font-family:'Share Tech Mono',monospace;font-size:10px;color:#c0392b;
        letter-spacing:2px;">🚫 PLAZO VENCIDO</div>
      <div style="font-family:'Share Tech Mono',monospace;font-size:7px;color:#ff6666;
        margin-top:6px;">La nota no será actualizada en la base de datos</div>
    </div>""" if DEADLINE_PASSED else f"""
    <div style="text-align:center;font-family:'Share Tech Mono',monospace;font-size:7px;
      color:#39e5b6;letter-spacing:1px;opacity:.9;">
      📊 Calificación final enviada · {n} · {lvl_name}
    </div>"""}
  </div>
</div>'''))


grader = Autograder()
