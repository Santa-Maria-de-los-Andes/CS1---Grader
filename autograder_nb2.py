"""
Autograder v1 — Notebook 2: Listas, Condicionales y Bucles for
⚔️  GOD OF WAR — Conviértete en el Dios de la Guerra del Código
"""

import sys
import datetime as _dt
from IPython.display import HTML, display

# ─── Supabase Config ──────────────────────────────────────────
SUPABASE_URL      = "https://uwykikwutjtkpffwmdiq.supabase.co"
SUPABASE_ANON_KEY = "sb_publishable_aBG6GD4wn9CgpSE-47fagQ_sNhnzznu"
LOGO_URL          = "https://raw.githubusercontent.com/Santa-Maria-de-los-Andes/CS1---Grader/main/icono%20SMA.png"

# ─── Deadline: June 14 2026 11:59 PM Peru (UTC-5) = June 15 04:59 UTC ───
_DEADLINE_UTC   = _dt.datetime(2026, 6, 15, 4, 59, 0, tzinfo=_dt.timezone.utc)
DEADLINE_PASSED = _dt.datetime.now(_dt.timezone.utc) >= _DEADLINE_UTC

# ─── Scoring ─────────────────────────────────────────────────
_CORE_MAX     = 124
_BONUS_KEYS   = {"reto1", "reto2"}
_BONUS_MAX    = 12

# ─── God of War Levels (by % of core score) ──────────────────
_LEVELS = [
    (96, 6, "👻 Fantasma de Esparta"),
    (81, 5, "⚔️ Dios de la Guerra"),
    (61, 4, "🔱 Semidiós"),
    (41, 3, "🛡️ Comandante de Legiones"),
    (21, 2, "⚔️ Espartano"),
    (0,  1, "💀 Simple Mortal"),
]

_XP_GRAD = {
    1: "linear-gradient(90deg,#333344,#666688)",
    2: "linear-gradient(90deg,#3a0000,#8b1a1a)",
    3: "linear-gradient(90deg,#5a0000,#cc2200)",
    4: "linear-gradient(90deg,#0a2040,#4aa8d8)",
    5: "linear-gradient(90deg,#3a2800,#ffd700)",
    6: "linear-gradient(90deg,#cc2200,#ffd700,#4aa8d8)",
}

_LV_CSS_COLOR = {
    1: "#666688",
    2: "#8b1a1a",
    3: "#cc2200",
    4: "#4aa8d8",
    5: "#ffd700",
    6: "#ffd700",  # fallback; gradient handled in HTML
}


def _level_info(pct):
    for thresh, num, name in _LEVELS:
        if pct >= thresh:
            return num, name
    return 1, "💀 Simple Mortal"


def _lv_color(n):
    return _LV_CSS_COLOR.get(n, "#666688")


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
        self._checkpoints  = set()   # tracks mini_a / mini_b / mini_c calls
        self._show_registration_form()

    # ── Registration form ────────────────────────────────────

    def _show_registration_form(self):
        logo_tag = (f'<img src="{LOGO_URL}" style="height:48px;object-fit:contain;" '
                    f'onerror="this.style.display=\'none\'">'
                    if LOGO_URL else
                    '<span style="font-family:\'Press Start 2P\',monospace;font-size:13px;'
                    'color:#ffd700;letter-spacing:2px;">SMA</span>')

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
                        f"&notebook=eq.nb2"
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
  <div style="background:#0d0005;border:1px solid #8b1a1a;border-radius:3px;
    padding:12px 20px;margin-top:6px;
    font-family:'Press Start 2P',monospace;animation:ag-fadein .4s ease .1s both;">
    <div style="font-size:6px;color:#8b1a1a;letter-spacing:2px;margin-bottom:10px;">
      ⚔️ TU MEJOR MARCA — NOTEBOOK 2</div>
    <div style="display:flex;align-items:center;gap:20px;">
      <div style="font-size:28px;color:#ffd700;
        text-shadow:0 0 16px rgba(255,215,0,.8),2px 2px 0 #7a3300;">
        {_best['pct']}%</div>
      <div>
        <div style="font-size:8px;color:#cc2200;letter-spacing:1px;">{_best['level_name']}</div>
        <div style="font-size:6px;color:#8888bb;margin-top:6px;letter-spacing:1px;">
          {_best['earned']} / {_best['possible']} XP</div>
      </div>
    </div>
  </div>'''
                else:
                    _score_html = (
                        '<div style="background:#0d0005;border:1px solid #2a1a1a;border-radius:3px;'
                        'padding:10px 20px;margin-top:6px;'
                        'font-family:\'Press Start 2P\',monospace;font-size:6px;color:#555544;'
                        'letter-spacing:1px;animation:ag-fadein .4s ease .1s both;">'
                        '⚔️ Primera batalla — ¡aún no tienes marca registrada!</div>'
                    )

                display(HTML(f'''
<link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">
<style>
  @keyframes ag-fadein {{from{{opacity:0;transform:translateY(8px)}}to{{opacity:1;transform:translateY(0)}}}}
  @keyframes ag-spin   {{to{{transform:rotate(360deg)}}}}
  @keyframes ag-start  {{0%{{opacity:0;transform:scale(.7)}}60%{{transform:scale(1.12)}}100%{{opacity:1;transform:scale(1)}}}}
</style>
<div style="width:100%;box-sizing:border-box;">
  <div style="background:#0a0000;border:1px solid #cc2200;border-radius:3px;padding:12px 18px;
    font-family:'Press Start 2P',monospace;font-size:8px;
    color:#cc2200;letter-spacing:1px;animation:ag-fadein .4s ease;">
    ⚔️ &nbsp;¡ENTRA AL CAMPO DE BATALLA, {nombre.upper()}! &nbsp;·&nbsp; {grado}
  </div>
  {_score_html}
  <div id="ag-loading" style="background:#0d0005;border:1px solid #2a1a1a;border-radius:3px;
    padding:18px;margin-top:6px;text-align:center;animation:ag-fadein .5s ease .2s both;">
    <div style="display:inline-block;width:28px;height:28px;border:3px solid #3a1a1a;
      border-top-color:#8b1a1a;border-radius:50%;animation:ag-spin .8s linear infinite;margin-bottom:10px;"></div>
    <div style="font-family:'Press Start 2P',monospace;font-size:7px;color:#8b1a1a;letter-spacing:2px;">
      PREPARANDO EL CAMPO DE BATALLA…
    </div>
  </div>
  <div id="ag-start" style="display:none;background:#0d0005;border:2px solid #cc2200;border-radius:4px;
    padding:24px;margin-top:6px;text-align:center;">
    <div style="font-family:'Press Start 2P',monospace;font-size:28px;color:#cc2200;letter-spacing:6px;
      text-shadow:0 0 20px rgba(204,34,0,.9),2px 2px 0 #7a1100;animation:ag-start .6s ease;">
      ¡RAGNARÖK!
    </div>
    <div style="font-family:'Press Start 2P',monospace;font-size:7px;color:#ffd700;
      letter-spacing:2px;margin-top:10px;">EJECUTA LA PRIMERA CELDA PARA COMENZAR</div>
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
<link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">
<style>
  .ag-input,.ag-select {{
    width:100%;box-sizing:border-box;background:#0a0005;border:1px solid #2a1a1a;
    border-radius:3px;padding:0 12px;color:#d4c5a9;font-size:13px;height:42px;
    font-family:'Segoe UI',Roboto,sans-serif;outline:none;transition:border .2s;
  }}
  .ag-input:focus,.ag-select:focus {{ border-color:#8b1a1a; }}
  .ag-select option {{ background:#0d0005; }}
  .ag-btn {{
    width:100%;padding:13px;background:linear-gradient(90deg,#6a0000,#8b1a1a);
    border:none;border-radius:3px;color:#ffd700;font-family:'Press Start 2P',monospace;
    font-size:9px;letter-spacing:2px;cursor:pointer;transition:opacity .2s;margin-top:6px;
  }}
  .ag-btn:hover {{ opacity:.85; }}
  .ag-err {{ color:#ff3333;font-size:11px;margin-top:6px;display:none; }}
  .ag-label {{ font-family:'Press Start 2P',monospace;font-size:7px;letter-spacing:1px;
    margin-bottom:8px;display:flex;align-items:center;gap:5px; }}
  .ag-field {{ display:flex;flex-direction:column; }}
</style>
<div style="background:#0d0005;border:2px solid #8b1a1a;border-radius:4px;max-width:840px;
  margin:10px 0;overflow:hidden;box-shadow:0 0 40px rgba(139,26,26,.2),0 10px 30px rgba(0,0,0,.8);">

  <div style="background:linear-gradient(90deg,#1a0000,#2a0800,#1a0000);border-bottom:2px solid #ffd700;
    padding:18px 24px;position:relative;display:flex;align-items:center;justify-content:center;min-height:80px;">
    <div style="position:absolute;left:20px;top:50%;transform:translateY(-50%);">{logo_tag}</div>
    <div style="text-align:center;">
      <div style="font-family:'Press Start 2P',monospace;font-size:18px;color:#ffd700;letter-spacing:3px;
        text-shadow:0 0 14px rgba(255,215,0,.7),2px 2px 0 #7a3300;">⚔ PYTHON QUEST ⚔</div>
      <div style="font-family:'Press Start 2P',monospace;font-size:8px;color:#cc2200;
        letter-spacing:2px;margin-top:8px;">NOTEBOOK II — GOD OF WAR MODE</div>
    </div>
    <div style="position:absolute;right:20px;top:50%;transform:translateY(-50%);">{logo_tag}</div>
  </div>

  <div style="padding:24px;">
    <div style="display:grid;grid-template-columns:2fr 1fr;gap:14px;margin-bottom:14px;align-items:end;">
      <div class="ag-field">
        <div class="ag-label" style="color:#cc2200;">⚔️ NOMBRE COMPLETO</div>
        <input id="ag-nombre" class="ag-input" placeholder="Tu nombre y apellido" />
      </div>
      <div class="ag-field">
        <div class="ag-label" style="color:#cc2200;">🏫 GRADO</div>
        <select id="ag-grado" class="ag-select">
          <option value="">— Selecciona —</option>
          <option value="3ro">3ro</option>
          <option value="4to">4to</option>
          <option value="5to">5to</option>
        </select>
      </div>
    </div>
    <div class="ag-field" style="margin-bottom:14px;">
      <div class="ag-label" style="color:#ffd700;">🪪 CÓDIGO DE ESTUDIANTE (DNI, Pasaporte, Carnet)</div>
      <input id="ag-dni" class="ag-input" placeholder="Ingresa tu código" />
    </div>
    <div id="ag-err" class="ag-err">⚠ Por favor completa todos los campos.</div>
    <button class="ag-btn" onclick="agRegister()">⚔️ &nbsp; ENTRAR A BATALLA &nbsp; ⚔️</button>
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
                display(HTML('<div style="font-family:monospace;padding:10px;background:#0d0005;'
                             'color:#cc2200;border:1px solid #8b1a1a;border-radius:3px;max-width:840px;">'
                             '⚔️ PYTHON QUEST NB2 — Registro</div>'))
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
        return '<span style="font-family:\'Press Start 2P\',monospace;font-size:11px;color:#ffd700;">SMA</span>'

    @property
    def _logo_tag_sm(self):
        if LOGO_URL:
            return (f'<img src="{LOGO_URL}" style="height:24px;object-fit:contain;" '
                    f'onerror="this.style.display:\'none\'">')
        return '<span style="font-family:\'Press Start 2P\',monospace;font-size:8px;color:#ffd700;">SMA</span>'

    def _nombre(self):
        if self._nombre_real:
            return self._nombre_real
        n = _get("nombre")
        if isinstance(n, str) and n.strip() and n.strip() not in ("?", ""):
            return n.strip()
        return "guerrero"

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

    def _header(self, title, icon="⚔️", pts=None):
        self._curr_title = title
        self._curr_icon  = icon
        self._curr_pts   = pts

    def _check_achievements(self, key):
        unlocked = []
        earned, possible, pct = self._totals()

        # Primer Golpe — first XP earned
        if any(e > 0 for e, _ in self._scores.values()) and self._unlock("primer_golpe"):
            unlocked.append(("⚔️ Primer Golpe — ¡Primera sangre!", "#cd7f32", "Común"))

        # Leviathan — ex6 + ex7 + ex8 all perfect
        loop_keys = ["ex6", "ex7", "ex8"]
        if (all(k in self._scores and self._scores[k][0] == self._scores[k][1]
                for k in loop_keys)
                and self._unlock("leviathan")):
            unlocked.append(("🪓 Leviathan — Maestro de los Bucles", "#ffd700", "Épico"))

        # Escudo del Norte — all debug perfect
        debug_keys = ["debug1", "debug2", "debug3", "debug4"]
        if (all(k in self._scores and self._scores[k][0] == self._scores[k][1]
                for k in debug_keys)
                and self._unlock("escudo_norte")):
            unlocked.append(("🛡️ Escudo del Norte — 0 Errores de Lógica", "#c0c0c0", "Raro"))

        # Hacha del Bifrost — all 3 checkpoints reached
        if len(self._checkpoints) >= 3 and self._unlock("hacha_bifrost"):
            unlocked.append(("❄️ Hacha del Bifrost — Todos los Checkpoints", "#ffd700", "Épico"))

        # Martillo de Thor — streak >= 5
        if self._streak >= 5 and self._unlock("martillo_thor"):
            unlocked.append(("⚡ Martillo de Thor — Racha x5", "#c0c0c0", "Raro"))

        # Príncipe de Asgard — 100% core
        if pct >= 100 and self._unlock("principe_asgard"):
            unlocked.append(("👑 Príncipe de Asgard — 100% del Notebook", "#9d1f1f", "Legendario"))

        # Ojo de Odín — both bonus perfect
        if (all(k in self._scores and self._scores[k][0] == self._scores[k][1]
                for k in ["reto1", "reto2"])
                and self._unlock("ojo_odin")):
            unlocked.append(("👁️ Ojo de Odín — Todos los Bonus", "#9d1f1f", "Legendario"))

        # Level-up
        lvl_num, lvl_name = _level_info(pct)
        if lvl_num > self._prev_level and self._prev_level > 0:
            unlocked.append((f"⬆️ ¡NIVEL! — {lvl_name}", "#4aa8d8", "Nivel"))
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

        # Check rows
        rows_html = ""
        for ok, label, msg in checks:
            if ok:
                rows_html += (
                    f'<div style="display:flex;align-items:flex-start;gap:10px;padding:7px 10px;'
                    f'margin-bottom:3px;background:rgba(57,255,20,.04);'
                    f'border-left:3px solid #39ff14;border-radius:0 3px 3px 0;">'
                    f'<span style="color:#39ff14;font-size:13px;flex-shrink:0;line-height:1.5;">✔</span>'
                    f'<div style="font-size:11px;line-height:1.5;">'
                    f'<span style="color:#39ff14;font-weight:bold;">{label}:</span> '
                    f'<span style="color:#8888bb;">{msg}</span></div></div>'
                )
            else:
                rows_html += (
                    f'<div style="display:flex;align-items:flex-start;gap:10px;padding:7px 10px;'
                    f'margin-bottom:3px;background:rgba(204,34,0,.06);'
                    f'border-left:3px solid #cc2200;border-radius:0 3px 3px 0;">'
                    f'<span style="color:#cc2200;font-size:13px;flex-shrink:0;line-height:1.5;">✖</span>'
                    f'<div style="font-size:11px;line-height:1.5;">'
                    f'<span style="color:#cc2200;font-weight:bold;">{label}:</span> '
                    f'<span style="color:#cc7766;">{msg}</span></div></div>'
                )

        # Stars
        star_r = pts / max_pts if max_pts > 0 else 0
        gold, dark = "#ffd700", "#2a1a00"
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

        # Combo
        combo_html = ""
        if self._streak >= 2:
            c_color = "#cc2200" if self._streak >= 5 else "#ff6b35"
            combo_html = (
                f'<div style="display:inline-flex;align-items:center;gap:5px;padding:3px 10px;'
                f'background:rgba(204,34,0,.12);border:1px solid {c_color};border-radius:2px;'
                f'margin-left:8px;">'
                f'<span style="font-family:\'Press Start 2P\',monospace;font-size:7px;'
                f'color:{c_color};">⚔ COMBO x{self._streak}</span></div>'
            )

        # Status
        if pts == max_pts:
            s_icon, s_text, s_color = "⚡", f"¡PERFECTO! +{pts} XP", "#39ff14"
            border_color, glow = "#39ff14", "0 0 22px rgba(57,255,20,.15)"
        elif pts > 0:
            s_icon, s_text, s_color = "🗡️", f"+{pts} XP  ·  {max_pts - pts} por ganar", "#ffd700"
            border_color, glow = "#ffd700", "0 0 22px rgba(255,215,0,.12)"
        else:
            s_icon, s_text, s_color = "💀", "¡INTENTA DE NUEVO! — Corrige los ✖", "#cc2200"
            border_color, glow = "#cc2200", "0 0 22px rgba(204,34,0,.15)"

        xp_grad = _XP_GRAD.get(lvl_num, _XP_GRAD[1])

        dots = "".join(
            f'<span style="display:inline-block;width:7px;height:7px;border-radius:50%;'
            f'background:{"#39ff14" if ok else "#cc2200"};margin:0 2px;'
            f'box-shadow:0 0 4px {"#39ff14" if ok else "#cc2200"};"></span>'
            for ok, _, _ in checks
        )

        new_ach     = self._check_achievements(key)
        reg_ach     = [(n, c, r) for n, c, r in new_ach if r != "Nivel"]
        levelup_ach = [(n, c, r) for n, c, r in new_ach if r == "Nivel"]

        # Achievement rarity display
        _RC = {
            "Común":     ("#cd7f32", "rgba(205,127,50,.12)",  "🥉"),
            "Raro":      ("#4a6fa5", "rgba(74,111,165,.12)",  "🛡️"),
            "Épico":     ("#ffd700", "rgba(255,215,0,.10)",   "⚔️"),
            "Legendario":("#9d1f1f", "rgba(157,31,31,.15)",   "👑"),
        }
        ach_html = ""
        for ach_name, _, ach_rarity in reg_ach:
            bc, bg, ach_icon = _RC.get(ach_rarity, _RC["Común"])
            ach_html += (
                f'<div style="display:flex;align-items:center;gap:10px;margin-top:8px;'
                f'padding:10px 12px;background:{bg};border:1px solid {bc};border-radius:3px;">'
                f'<span style="font-size:18px;">{ach_icon}</span>'
                f'<div style="flex:1;">'
                f'<div style="margin-bottom:3px;">'
                f'<span style="background:{bc};color:#0d0005;font-size:7px;font-weight:bold;'
                f'padding:1px 5px;border-radius:2px;font-family:\'Press Start 2P\',monospace;">'
                f'{ach_rarity.upper()}</span>'
                f'<span style="font-family:\'Press Start 2P\',monospace;font-size:7px;'
                f'color:{bc};margin-left:6px;">LOGRO DESBLOQUEADO</span>'
                f'</div>'
                f'<div style="color:#d4c5a9;font-size:12px;font-weight:bold;">{ach_name}</div>'
                f'</div></div>'
            )

        curr_icon  = getattr(self, '_curr_icon', '⚔️')
        curr_title = getattr(self, '_curr_title', 'MISIÓN').upper()
        _logo_sm   = self._logo_tag_sm

        _core_pct_bar = min(round(core_earned / _CORE_MAX * 100), 100)
        if _is_bonus:
            _bpct = round(bonus_earned / _BONUS_MAX * 100) if bonus_earned else 0
            xp_bar_html = (
                f'<div style="display:flex;justify-content:space-between;margin-bottom:4px;">'
                f'<span style="font-family:\'Press Start 2P\',monospace;font-size:7px;color:#4aa8d8;">'
                f'Bonus XP: {bonus_earned}/{_BONUS_MAX}</span>'
                f'<span style="font-family:\'Press Start 2P\',monospace;font-size:7px;color:#4aa8d8;">'
                f'🌌 RETO</span></div>'
                f'<div style="width:100%;height:10px;background:#141428;border:1px solid #1a2a3a;'
                f'border-radius:2px;overflow:hidden;">'
                f'<div style="width:{_bpct}%;height:100%;'
                f'background:linear-gradient(90deg,#0e2a3a,#4aa8d8);border-radius:2px;'
                f'transform-origin:left;animation:pg-xpscale 1.1s cubic-bezier(.4,0,.2,1) forwards;'
                f'box-shadow:0 0 6px rgba(74,168,216,.3);"></div></div>'
            )
        else:
            xp_bar_html = (
                f'<div style="display:flex;justify-content:space-between;margin-bottom:4px;">'
                f'<span style="font-family:\'Press Start 2P\',monospace;font-size:7px;color:#444433;">'
                f'XP: {core_earned}/{_CORE_MAX}</span>'
                f'<span style="font-family:\'Press Start 2P\',monospace;font-size:7px;'
                f'color:{_lv_color(lvl_num)};">{lvl_name}</span></div>'
                f'<div style="width:100%;height:10px;background:#141428;border:1px solid #2a1a1a;'
                f'border-radius:2px;overflow:hidden;">'
                f'<div style="width:{_core_pct_bar}%;height:100%;background:{xp_grad};'
                f'border-radius:2px;transform-origin:left;'
                f'animation:pg-xpscale 1.1s cubic-bezier(.4,0,.2,1) forwards;'
                f'box-shadow:0 0 6px rgba(204,34,0,.25);"></div></div>'
            )

        deadline_html = ""
        if DEADLINE_PASSED:
            deadline_html = '''<div style="margin-top:10px;padding:12px 16px;background:#1a0000;
  border:2px solid #ff0000;border-radius:3px;text-align:center;">
  <div style="font-family:'Press Start 2P',monospace;font-size:10px;color:#ff0000;
    letter-spacing:2px;text-shadow:0 0 10px rgba(255,0,0,.6);">🚫 PLAZO VENCIDO</div>
  <div style="font-family:'Press Start 2P',monospace;font-size:7px;color:#ff6666;
    margin-top:6px;letter-spacing:1px;">TU NOTA NO SERÁ ACTUALIZADA</div>
  <div style="font-size:11px;color:#cc4444;margin-top:6px;">
    Puedes revisar tus respuestas, pero la entrega ya cerró.</div></div>'''
        elif self._dni:
            deadline_html = ('<div style="margin-top:8px;font-family:\'Press Start 2P\',monospace;'
                             'font-size:6px;color:#4aa8d8;letter-spacing:1px;opacity:.85;">'
                             '📊 Calificación actualizada en la base de datos</div>')

        card_html = f'''<link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">
<style>
  @keyframes pg-xpscale{{from{{transform:scaleX(0)}}to{{transform:scaleX(1)}}}}
</style>
<div style="background:#0d0005;border:2px solid {border_color};border-radius:4px;max-width:840px;
  margin-bottom:14px;overflow:hidden;box-shadow:{glow},0 6px 24px rgba(0,0,0,.7);
  font-family:'Segoe UI',Roboto,sans-serif;">
  <div style="background:{border_color}18;border-bottom:1px solid {border_color}40;
    padding:9px 16px;display:flex;justify-content:space-between;align-items:center;">
    <div style="display:flex;align-items:center;gap:8px;">
      {_logo_sm}
      <span style="font-family:'Press Start 2P',monospace;font-size:9px;
        color:{border_color};letter-spacing:1px;">{curr_icon} {curr_title}</span>
    </div>
    <div style="display:flex;align-items:center;gap:10px;">
      {stars_html}
      <div style="font-family:'Press Start 2P',monospace;font-size:7px;color:#cc2200;
        background:rgba(204,34,0,.1);border:1px solid rgba(204,34,0,.4);
        padding:3px 8px;border-radius:2px;">MAX {max_pts} XP</div>
    </div>
  </div>
  <div style="padding:10px 14px 6px;">{rows_html}</div>
  <div style="background:#090005;border-top:1px solid #1a0a0a;padding:11px 14px;">
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:9px;">
      <div style="display:flex;align-items:center;gap:8px;">
        <span style="font-size:16px;">{s_icon}</span>
        <span style="font-family:'Press Start 2P',monospace;font-size:8px;
          color:{s_color};">{s_text}</span>
        {combo_html}
      </div>
      <div style="display:flex;align-items:center;gap:4px;color:#444433;font-size:10px;">
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

    # ── Level-up banner (God of War style) ───────────────────

    def _render_levelup(self, lvl_num, lvl_name):
        color = _lv_color(lvl_num)
        if lvl_num == 6:
            bg = "linear-gradient(135deg,#1a0000,#0a0a2a,#1a0000)"
            glow = f"0 0 40px rgba(204,34,0,.4),0 0 80px rgba(74,168,216,.2)"
            sub = "FUEGO Y HIELO FUSIONADOS"
        elif lvl_num == 5:
            bg = "linear-gradient(135deg,#1a0800,#2a1400)"
            glow = f"0 0 40px rgba(255,215,0,.35)"
            sub = "EL OLIMPO TIEMBLA"
        elif lvl_num == 4:
            bg = "linear-gradient(135deg,#001020,#002040)"
            glow = f"0 0 40px rgba(74,168,216,.35)"
            sub = "EL BIFROST TE LLAMA"
        elif lvl_num == 3:
            bg = "linear-gradient(135deg,#1a0000,#2a0000)"
            glow = f"0 0 40px rgba(204,34,0,.35)"
            sub = "LAS LEGIONES TE OBEDECEN"
        else:
            bg = "linear-gradient(135deg,#0a0000,#1a0000)"
            glow = f"0 0 28px rgba(139,26,26,.3)"
            sub = "TU CAMINO COMIENZA"

        return f'''<link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">
<style>
  @keyframes gow-lu{{0%{{opacity:0;transform:scale(.8) translateY(12px)}}
    60%{{transform:scale(1.04)}}100%{{opacity:1;transform:scale(1) translateY(0)}}}}
  @keyframes gow-glow{{0%,100%{{opacity:.7}}50%{{opacity:1}}}}
</style>
<div style="background:{bg};border:2px solid {color};border-radius:6px;max-width:840px;
  margin:10px 0;padding:28px;text-align:center;
  box-shadow:{glow},0 8px 32px rgba(0,0,0,.8);
  animation:gow-lu .7s cubic-bezier(.22,1,.36,1) forwards;">
  <div style="font-size:36px;margin-bottom:10px;animation:gow-glow 2s ease infinite;">⚔️</div>
  <div style="font-family:'Press Start 2P',monospace;font-size:8px;color:{color};
    letter-spacing:3px;margin-bottom:12px;">¡ASCENDISTE!</div>
  <div style="font-family:'Press Start 2P',monospace;font-size:clamp(12px,2.5vw,20px);
    color:{color};letter-spacing:4px;
    text-shadow:0 0 20px {color}80,2px 2px 0 #000;margin-bottom:8px;">{lvl_name}</div>
  <div style="font-family:'Press Start 2P',monospace;font-size:7px;color:#666655;
    letter-spacing:2px;">{sub}</div>
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
                "nombre":          self._nombre_real or "guerrero",
                "grado":           self._grado or "",
                "notebook":        "nb2",
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
            if not silent:
                display(HTML(
                    f'<div style="font-family:\'Press Start 2P\',monospace;font-size:8px;'
                    f'color:#39ff14;background:#020d02;border:1px solid #39ff14;'
                    f'border-radius:3px;padding:10px 16px;max-width:840px;margin-top:6px;">'
                    f'✅ SCORE ENVIADO — {self._nombre_real} · DNI {self._dni}'
                    f'<br><span style="color:#4aa8d8;font-size:7px;">'
                    f'📊 Calificación actualizada en la base de datos</span></div>'
                ))
        except Exception as _ex:
            if not silent:
                display(HTML(
                    f'<div style="font-family:\'Press Start 2P\',monospace;font-size:7px;'
                    f'color:#cc2200;background:#1a0002;border:1px solid #cc2200;'
                    f'border-radius:3px;padding:10px 16px;max-width:840px;margin-top:6px;">'
                    f'⚠️ Leaderboard no disponible: {_ex}</div>'
                ))

    # ═══════════════════════════════════════════════════════════
    # PARTE 1 — Sección 2.1: Listas e Indexación
    # ═══════════════════════════════════════════════════════════

    def check_ex1(self):
        """Ex1 — Mis Materias: lista de 5 materias (6 pts)"""
        self._header("EJERCICIO 1 — Mis Materias 📚", icon="🗡️", pts=6)
        checks = []
        mis_materias = _get("mis_materias")

        if mis_materias is None:
            checks.append((False, "mis_materias", "No definida — crea la lista: mis_materias = ['Mate', ...]"))
        elif not isinstance(mis_materias, list):
            checks.append((False, "mis_materias", f"Debe ser list, recibí {type(mis_materias).__name__}"))
        else:
            checks.append((True, "mis_materias es list", f"list ✓  {len(mis_materias)} elemento(s)"))
            if len(mis_materias) != 5:
                checks.append((False, "5 materias", f"Debe tener 5 elementos, tiene {len(mis_materias)}"))
            else:
                checks.append((True, "5 materias", "✓  cinco materias"))
            empties = [i for i, m in enumerate(mis_materias)
                       if not isinstance(m, str) or not m.strip()]
            if empties:
                checks.append((False, "materias no vacías",
                               f"Los índices {empties} tienen valores vacíos o no son strings"))
            elif isinstance(mis_materias, list) and len(mis_materias) == 5:
                checks.append((True, "materias no vacías", "✓  todas son strings no vacíos"))

        return self._award("ex1", checks, 6)

    def check_ex2(self):
        """Ex2 — Precio en Rebaja: precios[2] = 19.9 (6 pts)"""
        self._header("EJERCICIO 2 — Precio en Rebaja 💰", icon="🗡️", pts=6)
        checks = []
        precios = _get("precios")

        if precios is None:
            checks.append((False, "precios", "No definida — ¿ejecutaste la celda?"))
        elif not isinstance(precios, list):
            checks.append((False, "precios", f"Debe ser list, recibí {type(precios).__name__}"))
        else:
            checks.append((True, "precios es list", f"list ✓  {len(precios)} elemento(s)"))
            if len(precios) != 5:
                checks.append((False, "5 precios", f"Debe tener 5 elementos, tiene {len(precios)}"))
            else:
                checks.append((True, "5 precios", "✓"))
            if len(precios) >= 3:
                p2 = precios[2]
                if _approx(p2, 19.9, tol=0.01):
                    checks.append((True, "precios[2] == 19.9 (rebaja aplicada)", f"✓  {p2}"))
                elif _approx(p2, 25.0, tol=0.01):
                    checks.append((False, "precios[2]",
                                   "Aún vale 25.0 — escribe: precios[2] = 19.9"))
                else:
                    checks.append((False, "precios[2]",
                                   f"Debe ser 19.9, obtuve {p2}. Escribe: precios[2] = 19.9"))

        return self._award("ex2", checks, 6)

    def check_debug1(self):
        """Debug1 — IndexError: planetas[5] → planetas[-1] (3 pts)"""
        self._header("🔧 DEBUG 1 — IndexError corregido", icon="🔧", pts=3)
        checks = []
        resultado_debug1 = _get("resultado_debug1")

        if resultado_debug1 is None:
            checks.append((False, "resultado_debug1",
                           "No definida — cambia la línea a: resultado_debug1 = planetas[???]"
                           " (usa un índice válido 0–4 o negativo)"))
        elif not isinstance(resultado_debug1, str):
            checks.append((False, "resultado_debug1",
                           f"Debe ser str (nombre de planeta), recibí {type(resultado_debug1).__name__}"))
        elif resultado_debug1.strip() == "Júpiter":
            checks.append((True, "resultado_debug1 == 'Júpiter'",
                           "✓  planetas[-1] o planetas[4] — IndexError corregido"))
        else:
            checks.append((False, "resultado_debug1",
                           f"Debe ser 'Júpiter', obtuve '{resultado_debug1}'. "
                           f"Usa planetas[4] o planetas[-1]"))

        return self._award("debug1", checks, 3)

    def check_t1(self):
        """T1 — Índice del primer elemento (4 pts)"""
        self._header("❓ TEORÍA T1 — Índice del primer elemento", icon="🧠", pts=4)
        r = _get("respuesta_t1")
        checks = []
        if r is None:
            checks.append((False, "respuesta_t1", "No definida — escribe: respuesta_t1 = 'letra'"))
        elif not isinstance(r, str):
            checks.append((False, "respuesta_t1", "Debe ser str, ej: respuesta_t1 = 'b'"))
        elif r.strip().lower() == "b":
            checks.append((True, "respuesta_t1", "¡Correcto! El primer elemento siempre tiene índice 0"))
        else:
            checks.append((False, "respuesta_t1",
                           f"Incorrecto ('{r}'). Pista: Python empieza a contar desde cero."))
        return self._award("t1", checks, 4)

    def check_mini_a(self):
        """Checkpoint 2.1 — Listas (resumen de sección)"""
        self._checkpoints.add("mini_a")
        # Check achievement now that checkpoint is reached
        if len(self._checkpoints) >= 3:
            if self._unlock("hacha_bifrost"):
                display(HTML(
                    '<div style="font-family:\'Press Start 2P\',monospace;font-size:8px;'
                    'color:#4aa8d8;background:#001020;border:1px solid #4aa8d8;'
                    'border-radius:3px;padding:12px 16px;max-width:840px;margin:6px 0;">'
                    '❄️ LOGRO: Hacha del Bifrost — Todos los Checkpoints alcanzados</div>'
                ))

        sección = {
            "ex1": ("Mis Materias", 6),
            "ex2": ("Precio en Rebaja", 6),
            "debug1": ("Debug 1 – IndexError", 3),
            "t1": ("T1 – Índice", 4),
        }
        self._render_checkpoint("CHECKPOINT 2.1 — LISTAS", sección, "#4aa8d8")

    # ═══════════════════════════════════════════════════════════
    # PARTE 1 — Sección 2.2: Condicionales
    # ═══════════════════════════════════════════════════════════

    def check_ex3(self):
        """Ex3 — Clasificador de Velocidad (8 pts)"""
        self._header("EJERCICIO 3 — Clasificador de Velocidad 🚗", icon="🗡️", pts=8)
        checks = []
        velocidad = _get("velocidad")
        categoria = _get("categoria")

        if velocidad is None:
            checks.append((False, "velocidad", "No definida — ¿ejecutaste la celda?"))
        elif isinstance(velocidad, bool) or not isinstance(velocidad, (int, float)):
            checks.append((False, "velocidad", f"Debe ser número, recibí {type(velocidad).__name__}"))
        else:
            checks.append((True, "velocidad", f"número ✓  {velocidad} km/h"))

        if categoria is None:
            checks.append((False, "categoria",
                           "No definida — agrega al final de tu if/elif: categoria = '...'"))
        elif not isinstance(categoria, str):
            checks.append((False, "categoria", f"Debe ser str, recibí {type(categoria).__name__}"))
        else:
            if isinstance(velocidad, (int, float)) and not isinstance(velocidad, bool):
                if velocidad < 30:
                    expected = "zona escolar"
                elif velocidad < 80:
                    expected = "normal"
                elif velocidad < 120:
                    expected = "exceso leve"
                else:
                    expected = "exceso grave"
                if categoria.strip().lower() == expected:
                    checks.append((True, f"categoria para velocidad={velocidad}",
                                   f"✓  '{categoria}'"))
                else:
                    checks.append((False, "categoria",
                                   f"Para velocidad={velocidad} debería ser '{expected.title()}', "
                                   f"obtuve '{categoria}'"))
            else:
                checks.append((False, "categoria", "Define primero velocidad con un valor numérico"))

        return self._award("ex3", checks, 8)

    def check_debug2(self):
        """Debug2 — SyntaxError: dos puntos faltantes (3 pts)"""
        self._header("🔧 DEBUG 2 — SyntaxError corregido", icon="🔧", pts=3)
        checks = []
        lluvia = _get("lluvia")

        if lluvia is None:
            checks.append((False, "lluvia",
                           "No definida — agrega ':' al final del if y vuelve a ejecutar"))
        elif lluvia is True:
            checks.append((True, "lluvia = True y celda ejecutada",
                           "✓  SyntaxError corregido — el if tiene sus dos puntos"))
        else:
            checks.append((False, "lluvia",
                           f"Valor inesperado: {lluvia!r}. ¿Modificaste lluvia = True?"))

        return self._award("debug2", checks, 3)

    def check_ex4(self):
        """Ex4 — Clasificador de IMC (8 pts)"""
        self._header("EJERCICIO 4 — Clasificador de IMC ⚖️", icon="🗡️", pts=8)
        checks = []
        peso     = _get("peso")
        altura   = _get("altura")
        imc      = _get("imc")
        categoria = _get("categoria")

        for vname, val, lo, hi, unit in [
            ("peso",   peso,   20, 300, "kg"),
            ("altura", altura, 0.5, 3.0, "m"),
        ]:
            if val is None:
                checks.append((False, vname, f"No definida"))
            elif isinstance(val, bool) or not isinstance(val, (int, float)):
                checks.append((False, vname, f"Debe ser número"))
            elif not (lo <= val <= hi):
                checks.append((False, vname, f"Fuera de rango ({lo}–{hi} {unit}), obtuve {val}"))
            else:
                checks.append((True, vname, f"✓  {val} {unit}"))

        if (isinstance(peso, (int, float)) and not isinstance(peso, bool) and
                isinstance(altura, (int, float)) and not isinstance(altura, bool) and altura > 0):
            exp_imc = peso / (altura ** 2)
            if imc is None:
                checks.append((False, "imc", "No definida — ya está en la celda: imc = peso / (altura ** 2)"))
            elif _approx(imc, exp_imc, tol=0.01):
                checks.append((True, "imc = peso / altura²", f"✓  {imc:.2f}"))
            else:
                checks.append((False, "imc",
                               f"Para peso={peso}, altura={altura} → debe ser {exp_imc:.2f}, "
                               f"obtuve {imc}"))
        else:
            if imc is None:
                checks.append((False, "imc", "Define primero peso y altura"))

        if categoria is None:
            checks.append((False, "categoria",
                           "No definida — agrega categoria = '...' en cada rama de tu if/elif"))
        elif not isinstance(categoria, str):
            checks.append((False, "categoria", f"Debe ser str, recibí {type(categoria).__name__}"))
        elif isinstance(imc, (int, float)) and not isinstance(imc, bool):
            if imc >= 30:
                expected = "obesidad"
            elif imc >= 25:
                expected = "sobrepeso"
            elif imc >= 18.5:
                expected = "normal"
            else:
                expected = "bajo peso"
            if categoria.strip().lower() == expected:
                checks.append((True, f"categoria para imc={imc:.2f}", f"✓  '{categoria}'"))
            else:
                checks.append((False, "categoria",
                               f"Para imc={imc:.2f} debería ser '{expected.title()}', "
                               f"obtuve '{categoria}'"))
        else:
            checks.append((False, "categoria", "Define primero peso, altura e imc"))

        return self._award("ex4", checks, 8)

    def check_debug3(self):
        """Debug3 — Error lógico: orden de elif (3 pts)"""
        self._header("🔧 DEBUG 3 — Error lógico en elif corregido", icon="🔧", pts=3)
        checks = []
        magnitud = _get("magnitud")
        categoria = _get("categoria")

        if magnitud is None:
            checks.append((False, "magnitud",
                           "No definida — ¿ejecutaste la celda de debug 3?"))
        elif not _approx(magnitud, 6.8, tol=0.01):
            checks.append((False, "magnitud",
                           f"Debe ser 6.8 (el valor de la celda), obtuve {magnitud}"))
        else:
            checks.append((True, "magnitud == 6.8", "✓"))
            if categoria is None:
                checks.append((False, "categoria",
                               "No definida — reordena los elif y vuelve a ejecutar"))
            elif categoria.strip().lower() == "fuerte":
                checks.append((True, "categoria == 'Fuerte'",
                               "✓  elif reordenado correctamente"))
            else:
                checks.append((False, "categoria",
                               f"Para magnitud=6.8 debe ser 'Fuerte', obtuve '{categoria}'. "
                               f"Pista: reordena de mayor a menor umbral"))

        return self._award("debug3", checks, 3)

    def check_ex5(self):
        """Ex5 — Clasificador de Planetas por Distancia (8 pts)"""
        self._header("EJERCICIO 5 — Clasificador de Planetas 🪐", icon="🗡️", pts=8)
        checks = []
        distancia_au = _get("distancia_au")
        zona         = _get("zona")

        if distancia_au is None:
            checks.append((False, "distancia_au", "No definida — ¿ejecutaste la celda?"))
        elif isinstance(distancia_au, bool) or not isinstance(distancia_au, (int, float)):
            checks.append((False, "distancia_au",
                           f"Debe ser número (UA), recibí {type(distancia_au).__name__}"))
        else:
            checks.append((True, "distancia_au", f"número ✓  {distancia_au} UA"))

        if zona is None:
            checks.append((False, "zona",
                           "No definida — agrega zona = '...' en cada rama de tu if/elif"))
        elif not isinstance(zona, str):
            checks.append((False, "zona", f"Debe ser str, recibí {type(zona).__name__}"))
        elif isinstance(distancia_au, (int, float)) and not isinstance(distancia_au, bool):
            if distancia_au < 1.5:
                expected = "interior"
            elif distancia_au < 4.0:
                expected = "cinturón de asteroides"
            elif distancia_au < 30.0:
                expected = "exterior"
            else:
                expected = "trans-neptuniano"
            if zona.strip().lower() == expected:
                checks.append((True, f"zona para distancia_au={distancia_au}",
                               f"✓  '{zona}'"))
            else:
                checks.append((False, "zona",
                               f"Para {distancia_au} UA debería ser '{expected.title()}', "
                               f"obtuve '{zona}'"))
        else:
            checks.append((False, "zona", "Define primero distancia_au"))

        return self._award("ex5", checks, 8)

    def check_t2(self):
        """T2 — Ramas de if/elif/else (4 pts)"""
        self._header("❓ TEORÍA T2 — Ramas de if/elif/else", icon="🧠", pts=4)
        r = _get("respuesta_t2")
        checks = []
        if r is None:
            checks.append((False, "respuesta_t2", "No definida — escribe: respuesta_t2 = 'letra'"))
        elif not isinstance(r, str):
            checks.append((False, "respuesta_t2", "Debe ser str"))
        elif r.strip().lower() == "b":
            checks.append((True, "respuesta_t2",
                           "¡Correcto! Solo la primera rama verdadera se ejecuta"))
        else:
            checks.append((False, "respuesta_t2",
                           f"Incorrecto ('{r}'). Pista: Python sale de la cadena al encontrar la primera condición verdadera."))
        return self._award("t2", checks, 4)

    def check_mini_b(self):
        """Checkpoint 2.2 — Condicionales (resumen de sección)"""
        self._checkpoints.add("mini_b")
        sección = {
            "ex3":    ("Clasificador de Velocidad", 8),
            "debug2": ("Debug 2 – SyntaxError", 3),
            "ex4":    ("Clasificador de IMC", 8),
            "debug3": ("Debug 3 – Lógica elif", 3),
            "ex5":    ("Clasificador de Planetas", 8),
            "t2":     ("T2 – Ramas if/elif", 4),
        }
        self._render_checkpoint("CHECKPOINT 2.2 — CONDICIONALES", sección, "#cc2200")

    # ═══════════════════════════════════════════════════════════
    # PARTE 1 — Sección 2.3: Bucles for
    # ═══════════════════════════════════════════════════════════

    def check_ex6(self):
        """Ex6 — Mis Materias en Loop (6 pts)"""
        self._header("EJERCICIO 6 — Mis Materias en Loop 🔁", icon="🗡️", pts=6)
        checks = []
        mis_materias = _get("mis_materias")

        if mis_materias is None:
            checks.append((False, "mis_materias",
                           "No definida — ¿completaste el Ejercicio 1 primero?"))
        elif not isinstance(mis_materias, list) or len(mis_materias) != 5:
            checks.append((False, "mis_materias",
                           f"Debe ser list de 5 elementos (del Ej. 1), obtuve {mis_materias!r}"))
        else:
            checks.append((True, "mis_materias (del Ej. 1)", "list ✓  5 elementos"))

        # Check loop variable (try common names)
        loop_var = None
        for name in ["materia", "m", "item", "subject", "curso"]:
            v = _get(name)
            if v is not None:
                loop_var = (name, v)
                break

        if loop_var is None:
            checks.append((False, "variable del loop",
                           "No encontré la variable del loop (ej: 'materia'). "
                           "¿Ejecutaste tu celda for?"))
        elif (isinstance(mis_materias, list) and len(mis_materias) == 5 and
              loop_var[1] == mis_materias[-1]):
            checks.append((True, f"loop ejecutado (var '{loop_var[0]}' = última materia)",
                           f"✓  '{loop_var[1]}'"))
        else:
            checks.append((False, "variable del loop",
                           f"'{loop_var[0]}' = {loop_var[1]!r} no es la última materia "
                           f"de mis_materias. ¿Usaste mis_materias en el for?"))

        return self._award("ex6", checks, 6)

    def check_debug4(self):
        """Debug4 — IndentationError: 4 espacios faltantes (3 pts)"""
        self._header("🔧 DEBUG 4 — IndentationError corregido", icon="🔧", pts=3)
        checks = []
        planeta = _get("planeta")

        if planeta is None:
            checks.append((False, "planeta",
                           "No definida — agrega 4 espacios al print y vuelve a ejecutar"))
        elif not isinstance(planeta, str):
            checks.append((False, "planeta",
                           f"Debe ser str (último planeta), recibí {type(planeta).__name__}"))
        elif planeta.strip() == "Júpiter":
            checks.append((True, "planeta == 'Júpiter' (loop corrió sin errores)",
                           "✓  IndentationError corregido"))
        else:
            checks.append((False, "planeta",
                           f"Debe ser 'Júpiter' (última iteración), obtuve '{planeta}'"))

        return self._award("debug4", checks, 3)

    def check_ex7(self):
        """Ex7 — Crecimiento Bacteriano: for loop duplicando (8 pts)"""
        self._header("EJERCICIO 7 — Crecimiento Bacteriano 🦠", icon="🗡️", pts=8)
        checks = []
        poblacion = _get("poblacion")

        if poblacion is None:
            checks.append((False, "poblacion",
                           "No definida — ¿ejecutaste tu for loop?"))
        elif isinstance(poblacion, bool) or not isinstance(poblacion, (int, float)):
            checks.append((False, "poblacion", f"Debe ser número, recibí {type(poblacion).__name__}"))
        elif poblacion == 1024:
            checks.append((True, "poblacion == 1024 (2^10)",
                           "✓  duplicó correctamente 10 veces desde 1"))
        elif poblacion == 1:
            checks.append((False, "poblacion",
                           "Aún vale 1 — ¿pusiste poblacion = poblacion * 2 DENTRO del loop?"))
        else:
            checks.append((False, "poblacion",
                           f"Para 10 generaciones desde 1, debe ser 1024 (2¹⁰), "
                           f"obtuve {poblacion}. Verifica la operación de duplicación."))

        return self._award("ex7", checks, 8)

    def check_ex8(self):
        """Ex8 — Análisis de Temperatura Cusco (10 pts)"""
        self._header("EJERCICIO 8 — Temperatura Cusco 🌡️", icon="🗡️", pts=10)
        checks = []
        # temps = [14.2, 8.5, 16.1, 11.3, 19.0, 7.8, 13.5]
        # > 12: 14.2, 16.1, 19.0, 13.5 → 4
        # < 10: 8.5, 7.8 → 2
        EXP_TEMPLADOS = 4
        EXP_FRIOS     = 2

        temperaturas = _get("temperaturas_cusco")
        dias_templados = _get("dias_templados")
        dias_frios     = _get("dias_frios")

        if temperaturas is None:
            checks.append((False, "temperaturas_cusco", "No definida — ¿ejecutaste la celda?"))
        elif not isinstance(temperaturas, list):
            checks.append((False, "temperaturas_cusco", "Debe ser list"))
        else:
            checks.append((True, "temperaturas_cusco", f"list ✓  {len(temperaturas)} elementos"))

        if dias_templados is None:
            checks.append((False, "dias_templados",
                           "No definida — crea el contador antes del loop: dias_templados = 0"))
        elif isinstance(dias_templados, bool) or not isinstance(dias_templados, int):
            checks.append((False, "dias_templados", "Debe ser int (contador)"))
        elif dias_templados == EXP_TEMPLADOS:
            checks.append((True, "dias_templados == 4", "✓  (temperaturas > 12°C)"))
        else:
            checks.append((False, "dias_templados",
                           f"Debe ser {EXP_TEMPLADOS} (14.2, 16.1, 19.0, 13.5 > 12), "
                           f"obtuve {dias_templados}"))

        if dias_frios is None:
            checks.append((False, "dias_frios",
                           "No definida — crea el contador antes del loop: dias_frios = 0"))
        elif isinstance(dias_frios, bool) or not isinstance(dias_frios, int):
            checks.append((False, "dias_frios", "Debe ser int (contador)"))
        elif dias_frios == EXP_FRIOS:
            checks.append((True, "dias_frios == 2", "✓  (temperaturas < 10°C)"))
        else:
            checks.append((False, "dias_frios",
                           f"Debe ser {EXP_FRIOS} (8.5, 7.8 < 10), obtuve {dias_frios}"))

        return self._award("ex8", checks, 10)

    def check_mini_c(self):
        """Checkpoint 2.3 — Bucles for (resumen de sección)"""
        self._checkpoints.add("mini_c")
        sección = {
            "ex6":    ("Mis Materias en Loop", 6),
            "debug4": ("Debug 4 – IndentationError", 3),
            "ex7":    ("Crecimiento Bacteriano", 8),
            "ex8":    ("Temperatura Cusco", 10),
        }
        self._render_checkpoint("CHECKPOINT 2.3 — BUCLES FOR", sección, "#ffd700")

    # ── Helper: render checkpoint summary ────────────────────

    def _render_checkpoint(self, title, sección, color):
        rows = ""
        total_e = total_p = 0
        for key, (label, max_p) in sección.items():
            e, p = self._scores.get(key, (0, max_p))
            total_e += e; total_p += p
            ok = e == p
            bar_w = round(60 * e / p) if p else 0
            rows += (
                f'<div style="display:flex;align-items:center;gap:10px;margin-bottom:6px;">'
                f'<span style="font-size:12px;">{"✅" if ok else "⬜"}</span>'
                f'<div style="flex:1;">'
                f'<div style="font-size:11px;color:#d4c5a9;margin-bottom:3px;">{label}</div>'
                f'<div style="height:5px;background:#1a0a0a;border-radius:2px;overflow:hidden;">'
                f'<div style="width:{bar_w * 100 // 60}%;height:100%;'
                f'background:{color};opacity:.8;border-radius:2px;"></div></div>'
                f'</div>'
                f'<span style="font-family:\'Press Start 2P\',monospace;font-size:7px;'
                f'color:{color if ok else "#555544"};">{e}/{p}</span>'
                f'</div>'
            )
        pct_sec = round(total_e / total_p * 100) if total_p else 0
        display(HTML(
            f'<link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">'
            f'<div style="background:#0d0005;border:2px solid {color};border-radius:4px;'
            f'max-width:840px;margin:10px 0;padding:18px 20px;'
            f'box-shadow:0 0 20px {color}22,0 4px 16px rgba(0,0,0,.6);">'
            f'<div style="font-family:\'Press Start 2P\',monospace;font-size:9px;'
            f'color:{color};letter-spacing:2px;margin-bottom:16px;">✅ {title}</div>'
            f'{rows}'
            f'<div style="margin-top:14px;padding-top:10px;border-top:1px solid {color}30;'
            f'display:flex;justify-content:space-between;align-items:center;">'
            f'<span style="font-family:\'Press Start 2P\',monospace;font-size:7px;color:#666655;">'
            f'SECCIÓN: {total_e}/{total_p} XP</span>'
            f'<span style="font-family:\'Press Start 2P\',monospace;font-size:9px;color:{color};">'
            f'{pct_sec}%</span>'
            f'</div></div>'
        ))

    # ═══════════════════════════════════════════════════════════
    # PARTE 2 — Ejercicios de Integración
    # ═══════════════════════════════════════════════════════════

    def check_intex1(self):
        """IntEx1 — Clasificador de Exoplanetas (6 pts)"""
        self._header("INTEGRACIÓN 1 — Exoplanetas ⭐", icon="⚔️", pts=6)
        checks = []
        radio         = _get("radio")
        temperatura   = _get("temperatura")
        clasificacion = _get("clasificacion")

        if radio is None:
            checks.append((False, "radio", "No definida (en radios terrestres, ej: radio = 1.2)"))
        elif isinstance(radio, bool) or not isinstance(radio, (int, float)):
            checks.append((False, "radio", f"Debe ser número, recibí {type(radio).__name__}"))
        else:
            checks.append((True, "radio", f"✓  {radio} R⊕"))

        if temperatura is None:
            checks.append((False, "temperatura", "No definida (en Kelvin, ej: temperatura = 265)"))
        elif isinstance(temperatura, bool) or not isinstance(temperatura, (int, float)):
            checks.append((False, "temperatura", f"Debe ser número, recibí {type(temperatura).__name__}"))
        else:
            checks.append((True, "temperatura", f"✓  {temperatura} K"))

        if clasificacion is None:
            checks.append((False, "clasificacion",
                           "No definida — guarda el resultado: clasificacion = '...'"))
        elif not isinstance(clasificacion, str):
            checks.append((False, "clasificacion", f"Debe ser str, recibí {type(clasificacion).__name__}"))
        else:
            if isinstance(radio, (int, float)) and not isinstance(radio, bool):
                if radio > 2:
                    expected = "gigante gaseoso"
                elif isinstance(temperatura, (int, float)) and not isinstance(temperatura, bool):
                    if temperatura > 600:
                        expected = "demasiado caliente"
                    elif temperatura >= 200:
                        expected = "zona habitable"
                    else:
                        expected = "demasiado frio"
                else:
                    expected = None
                if expected and clasificacion.strip().lower() == expected:
                    checks.append((True, f"clasificacion correcta",
                                   f"✓  '{clasificacion}' para radio={radio}, T={temperatura}K"))
                elif expected:
                    checks.append((False, "clasificacion",
                                   f"Para radio={radio}, T={temperatura}K → esperaba "
                                   f"'{expected.title()}', obtuve '{clasificacion}'"))
            else:
                checks.append((False, "clasificacion", "Define primero radio y temperatura"))

        return self._award("intex1", checks, 6)

    def check_intex2(self):
        """IntEx2 — Caja Registradora (8 pts)"""
        self._header("INTEGRACIÓN 2 — Caja Registradora ⭐⭐", icon="⚔️", pts=8)
        checks = []
        # precios = [1.5, 4.2, 6.0, 3.8, 8.5] → sum = 24.0
        EXP_SUBTOTAL = 24.0
        EXP_IGV      = round(24.0 * 0.18, 10)   # 4.32
        EXP_TOTAL    = round(24.0 * 1.18, 10)   # 28.32

        subtotal = _get("subtotal")
        igv      = _get("igv")
        total    = _get("total")

        for vname, val, exp, desc in [
            ("subtotal", subtotal, EXP_SUBTOTAL, "suma de todos los precios"),
            ("igv",      igv,      EXP_IGV,      "subtotal × 0.18"),
            ("total",    total,    EXP_TOTAL,     "subtotal + igv"),
        ]:
            if val is None:
                checks.append((False, vname, f"No definida — {desc}"))
            elif isinstance(val, bool) or not isinstance(val, (int, float)):
                checks.append((False, vname, f"Debe ser número"))
            elif _approx(val, exp, tol=0.02):
                checks.append((True, f"{vname} ≈ {exp:.2f}", f"✓  {val:.2f}"))
            else:
                checks.append((False, vname,
                               f"Debe ser {exp:.2f} ({desc}), obtuve {val}"))

        return self._award("intex2", checks, 8)

    def check_intex3(self):
        """IntEx3 — Simulador de Población Bacteriana (8 pts)"""
        self._header("INTEGRACIÓN 3 — Población Bacteriana ⭐⭐", icon="⚔️", pts=8)
        checks = []
        poblacion = _get("poblacion")

        if poblacion is None:
            checks.append((False, "poblacion",
                           "No definida — ¿ejecutaste tu for loop con generaciones?"))
        elif isinstance(poblacion, bool) or not isinstance(poblacion, (int, float)):
            checks.append((False, "poblacion", f"Debe ser número, recibí {type(poblacion).__name__}"))
        elif poblacion == 1024:
            checks.append((True, "poblacion == 1024 (2¹⁰ desde 1)",
                           "✓  10 generaciones duplicadas correctamente"))
        elif poblacion == 1:
            checks.append((False, "poblacion",
                           "Aún vale 1 — ¿duplicas DENTRO del loop? poblacion = poblacion * 2"))
        else:
            checks.append((False, "poblacion",
                           f"Después de 10 generaciones desde 1 debe ser 1024, obtuve {poblacion}"))

        return self._award("intex3", checks, 8)

    def check_intex4(self):
        """IntEx4 — Análisis Temperatura Semanal Cusco (10 pts)"""
        self._header("INTEGRACIÓN 4 — Temperatura Semanal Cusco ⭐⭐⭐", icon="⚔️", pts=10)
        checks = []
        # temps = [14.2, 8.5, 16.1, 11.3, 19.0, 7.8, 13.5]
        # frío < 10: 8.5, 7.8 → 2
        # templado 10–16: 14.2, 11.3, 13.5 → 3
        # caluroso > 16: 16.1, 19.0 → 2
        # promedio = 90.4/7 ≈ 12.914
        EXP_FRIO      = 2
        EXP_TEMPLADO  = 3
        EXP_CALUROSO  = 2
        EXP_PROMEDIO  = 90.4 / 7  # ≈ 12.914

        cont_frio      = _get("cont_frio")
        cont_templado  = _get("cont_templado")
        cont_caluroso  = _get("cont_caluroso")
        promedio       = _get("promedio")

        for vname, val, exp, desc in [
            ("cont_frio",     cont_frio,     EXP_FRIO,     "días con temp < 10°C"),
            ("cont_templado", cont_templado, EXP_TEMPLADO, "días con 10 ≤ temp ≤ 16°C"),
            ("cont_caluroso", cont_caluroso, EXP_CALUROSO, "días con temp > 16°C"),
        ]:
            if val is None:
                checks.append((False, vname,
                               f"No definida — inicializa antes del loop: {vname} = 0"))
            elif isinstance(val, bool) or not isinstance(val, int):
                checks.append((False, vname, "Debe ser int (contador)"))
            elif val == exp:
                checks.append((True, f"{vname} == {exp}", f"✓  ({desc})"))
            else:
                checks.append((False, vname,
                               f"Debe ser {exp} ({desc}), obtuve {val}"))

        if promedio is None:
            checks.append((False, "promedio",
                           "No definida — calcula: promedio = total_temps / len(temps)"))
        elif isinstance(promedio, bool) or not isinstance(promedio, (int, float)):
            checks.append((False, "promedio", "Debe ser número"))
        elif _approx(promedio, EXP_PROMEDIO, tol=0.05):
            checks.append((True, f"promedio ≈ {EXP_PROMEDIO:.2f}", f"✓  {promedio:.2f}°C"))
        else:
            checks.append((False, "promedio",
                           f"Debe ser ≈ {EXP_PROMEDIO:.2f}°C, obtuve {promedio}"))

        return self._award("intex4", checks, 10)

    def check_intex5(self):
        """IntEx5 — Simulador de Misión Espacial (12 pts)"""
        self._header("INTEGRACIÓN 5 — Misión Espacial ⭐⭐⭐", icon="⚔️", pts=12)
        checks = []
        # costos=[350,200,280,90,150], combustible=1000
        # 1000-350=650, 650-200=450, 450-280=170, 170-90=80, 80<150 → ABORT
        # etapas_completadas=4, combustible_usado=920, mision_exitosa=False
        EXP_ETAPAS  = 4
        EXP_USADO   = 920
        EXP_EXITOSA = False

        mision_exitosa       = _get("mision_exitosa")
        etapas_completadas   = _get("etapas_completadas")
        combustible_usado    = _get("combustible_usado")

        if mision_exitosa is None:
            checks.append((False, "mision_exitosa",
                           "No definida — inicializa: mision_exitosa = True"))
        elif mision_exitosa is EXP_EXITOSA:
            checks.append((True, "mision_exitosa == False",
                           "✓  misión abortada en Llegada (combustible insuficiente)"))
        else:
            checks.append((False, "mision_exitosa",
                           f"Debe ser False (la misión se aborta al intentar 'Llegada'), "
                           f"obtuve {mision_exitosa}"))

        if etapas_completadas is None:
            checks.append((False, "etapas_completadas",
                           "No definida — inicializa: etapas_completadas = 0"))
        elif isinstance(etapas_completadas, bool) or not isinstance(etapas_completadas, int):
            checks.append((False, "etapas_completadas", "Debe ser int"))
        elif etapas_completadas == EXP_ETAPAS:
            checks.append((True, "etapas_completadas == 4",
                           "✓  Despegue, Separación, Inserción orbital, Corrección"))
        else:
            checks.append((False, "etapas_completadas",
                           f"Debe ser 4 (se completan 4 antes de quedarse sin combustible), "
                           f"obtuve {etapas_completadas}"))

        if combustible_usado is None:
            checks.append((False, "combustible_usado",
                           "No definida — inicializa: combustible_usado = 0"))
        elif isinstance(combustible_usado, bool) or not isinstance(combustible_usado, (int, float)):
            checks.append((False, "combustible_usado", "Debe ser número"))
        elif _approx(combustible_usado, EXP_USADO, tol=0.5):
            checks.append((True, f"combustible_usado == {EXP_USADO}",
                           f"✓  350+200+280+90 = {EXP_USADO}"))
        else:
            checks.append((False, "combustible_usado",
                           f"Debe ser {EXP_USADO}, obtuve {combustible_usado}"))

        return self._award("intex5", checks, 12)

    # ═══════════════════════════════════════════════════════════
    # BONUS — Retos opcionales
    # ═══════════════════════════════════════════════════════════

    def check_reto1(self):
        """Reto1 — ¿Es Primo? (6 pts, bonus)"""
        self._header("🌟 RETO 1 — ¿Es Primo? (BONUS)", icon="🌟", pts=6)
        checks = []
        numero   = _get("numero")
        es_primo = _get("es_primo")

        if numero is None:
            checks.append((False, "numero", "No definida"))
        elif isinstance(numero, bool) or not isinstance(numero, int):
            checks.append((False, "numero", "Debe ser int"))
        else:
            checks.append((True, "numero", f"int ✓  {numero}"))

        if es_primo is None:
            checks.append((False, "es_primo",
                           "No definida — inicializa: es_primo = True (antes del loop)"))
        elif not isinstance(es_primo, bool):
            checks.append((False, "es_primo", f"Debe ser bool (True/False), recibí {type(es_primo).__name__}"))
        elif isinstance(numero, int) and not isinstance(numero, bool):
            # candidatos = [2..12] as given in notebook
            # Ignore candidate equal to numero itself
            actual_primo = all(
                numero % c != 0
                for c in range(2, 13)
                if c != numero
            ) and numero > 1
            if numero <= 1:
                actual_primo = False
            if es_primo == actual_primo:
                checks.append((True,
                               f"es_primo == {actual_primo} para numero={numero}",
                               f"✓  {'primo' if actual_primo else 'no primo'}"))
            else:
                checks.append((False, "es_primo",
                               f"Para numero={numero} debería ser {actual_primo}, "
                               f"obtuve {es_primo}"))
        else:
            checks.append((False, "es_primo", "Define primero numero"))

        return self._award("reto1", checks, 6)

    def check_reto2(self):
        """Reto2 — Secuencia de Fibonacci (6 pts, bonus)"""
        self._header("🌟 RETO 2 — Fibonacci (BONUS)", icon="🌟", pts=6)
        checks = []
        fib = _get("fib")
        # Expected: start [1,1] + 13 pasos = 15 elements
        exp_fib = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610]

        if fib is None:
            checks.append((False, "fib",
                           "No definida — ¿ejecutaste el loop con fib.append()?"))
        elif not isinstance(fib, list):
            checks.append((False, "fib", f"Debe ser list, recibí {type(fib).__name__}"))
        elif len(fib) != len(exp_fib):
            checks.append((False, "fib",
                           f"Debe tener {len(exp_fib)} elementos, tiene {len(fib)}. "
                           f"¿Iteraste sobre los 13 pasos?"))
        else:
            wrong = [(i, exp_fib[i], fib[i])
                     for i in range(len(exp_fib)) if fib[i] != exp_fib[i]]
            if not wrong:
                checks.append((True, "fib completa y correcta",
                               f"✓  15 números, llega hasta {exp_fib[-1]}"))
            else:
                pos, e, o = wrong[0]
                checks.append((False, "fib",
                               f"Error en índice {pos}: esperaba {e}, obtuve {o}. "
                               f"Pista: fib[-1] + fib[-2]"))

        return self._award("reto2", checks, 6)

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
            final_msg = f"👻 FANTASMA DE ESPARTA. {n.upper()}, tu nombre será grabado en las runas del Olimpo."
        elif core_pct >= 81:
            final_msg = f"⚔️ DIOS DE LA GUERRA. {n}, el Olimpo tiembla ante tu poder. El NB3 te aguarda."
        elif core_pct >= 61:
            final_msg = f"🔱 SEMIDIÓS. {n}, el Bifrost te llama. Revisa los ✖ para ascender."
        elif core_pct >= 41:
            final_msg = f"🛡️ COMANDANTE. {n}, tus legiones necesitan más entrenamiento. ¡Practica!"
        elif core_pct >= 21:
            final_msg = f"⚔️ ESPARTANO. {n}, cada guerrero empieza aquí. Relee la teoría."
        else:
            final_msg = f"💀 {n}, el camino de Kratos es largo. Cada celda ejecutada es un golpe de hacha."

        # Achievement display names
        ach_display = {
            "primer_golpe":   "⚔️ Primer Golpe",
            "leviathan":      "🪓 Leviathan",
            "escudo_norte":   "🛡️ Escudo del Norte",
            "hacha_bifrost":  "❄️ Hacha del Bifrost",
            "martillo_thor":  "⚡ Martillo de Thor",
            "principe_asgard":"👑 Príncipe de Asgard",
            "ojo_odin":       "👁️ Ojo de Odín",
        }

        ach_html = ""
        if self._achievements:
            for ak, alabel in ach_display.items():
                if ak in self._achievements:
                    ach_html += (
                        f'<div style="display:inline-flex;align-items:center;gap:5px;'
                        f'padding:3px 8px;background:rgba(255,215,0,.08);'
                        f'border:1px solid #ffd70040;border-radius:2px;margin:2px;">'
                        f'<span style="font-family:\'Press Start 2P\',monospace;font-size:6px;'
                        f'color:#ffd700;">{alabel}</span></div>'
                    )

        lv_color = _lv_color(lvl_num)
        xp_grad  = _XP_GRAD.get(lvl_num, _XP_GRAD[1])

        # Submit final score
        self._submit_to_supabase(core_earned, _CORE_MAX, core_pct, lvl_num, lvl_name)

        display(HTML(f'''
<link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">
<style>
  @keyframes gow-glow{{0%,100%{{text-shadow:0 0 14px rgba(255,215,0,.8),2px 2px 0 #7a3300}}
    50%{{text-shadow:0 0 32px rgba(255,215,0,1),0 0 60px rgba(204,34,0,.5),2px 2px 0 #7a3300}}}}
  @keyframes gow-xp{{from{{transform:scaleX(0)}}to{{transform:scaleX(1)}}}}
  @keyframes gow-float{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-6px)}}}}
</style>
<div style="background:#0d0005;border:2px solid #ffd700;border-radius:6px;max-width:840px;
  margin:12px 0;overflow:hidden;
  box-shadow:0 0 40px rgba(255,215,0,.15),0 0 80px rgba(204,34,0,.08),0 10px 40px rgba(0,0,0,.8);">

  <!-- Header -->
  <div style="background:linear-gradient(135deg,#1a0000,#2a0800,#1a0000);
    border-bottom:2px solid #ffd700;padding:22px 28px;text-align:center;position:relative;">
    <div style="position:absolute;left:20px;top:50%;transform:translateY(-50%);">{self._logo_tag}</div>
    <div style="font-family:'Press Start 2P',monospace;font-size:clamp(14px,3vw,22px);
      color:#ffd700;animation:gow-glow 2.5s ease-in-out infinite;letter-spacing:3px;
      margin-bottom:8px;">⚔ PYTHON QUEST ⚔</div>
    <div style="font-family:'Press Start 2P',monospace;font-size:8px;color:#cc2200;
      letter-spacing:2px;">NOTEBOOK II — RESUMEN FINAL</div>
    <div style="position:absolute;right:20px;top:50%;transform:translateY(-50%);">{self._logo_tag}</div>
  </div>

  <!-- Score -->
  <div style="padding:24px 28px;">
    <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;margin-bottom:20px;">
      <div style="background:#0a0000;border:1px solid #2a0a0a;border-radius:3px;
        padding:16px;text-align:center;">
        <div style="font-family:'Press Start 2P',monospace;font-size:7px;color:#444433;
          letter-spacing:1px;margin-bottom:10px;">XP CORE</div>
        <div style="font-family:'Press Start 2P',monospace;font-size:clamp(14px,3vw,22px);
          color:#ffd700;">{core_earned}/{_CORE_MAX}</div>
      </div>
      <div style="background:#0a0000;border:1px solid #2a0a0a;border-radius:3px;
        padding:16px;text-align:center;">
        <div style="font-family:'Press Start 2P',monospace;font-size:7px;color:#444433;
          letter-spacing:1px;margin-bottom:10px;">NIVEL</div>
        <div style="font-family:'Press Start 2P',monospace;font-size:clamp(8px,1.5vw,12px);
          color:{lv_color};">{lvl_name}</div>
      </div>
      <div style="background:#0a0000;border:1px solid #2a0a0a;border-radius:3px;
        padding:16px;text-align:center;">
        <div style="font-family:'Press Start 2P',monospace;font-size:7px;color:#444433;
          letter-spacing:1px;margin-bottom:10px;">SCORE</div>
        <div style="font-family:'Press Start 2P',monospace;font-size:clamp(14px,3vw,22px);
          color:#39ff14;">{core_pct}%</div>
      </div>
    </div>

    <!-- XP Bar -->
    <div style="margin-bottom:20px;">
      <div style="display:flex;justify-content:space-between;margin-bottom:6px;">
        <span style="font-family:'Press Start 2P',monospace;font-size:7px;color:#444433;">
          PROGRESO CORE</span>
        <span style="font-family:'Press Start 2P',monospace;font-size:7px;color:{lv_color};">
          {core_pct}%</span>
      </div>
      <div style="width:100%;height:14px;background:#141428;border:1px solid #2a1a1a;
        border-radius:3px;overflow:hidden;">
        <div style="width:{core_pct}%;height:100%;background:{xp_grad};
          border-radius:3px;transform-origin:left;
          animation:gow-xp 1.4s cubic-bezier(.4,0,.2,1) forwards;
          box-shadow:0 0 8px rgba(204,34,0,.4);"></div>
      </div>
    </div>

    <!-- Bonus -->
    {f"""
    <div style="margin-bottom:20px;padding:12px 16px;background:#0a0010;
      border:1px solid #4aa8d840;border-radius:3px;">
      <div style="font-family:'Press Start 2P',monospace;font-size:7px;color:#4aa8d8;
        margin-bottom:8px;">🌌 BONUS XP</div>
      <div style="font-family:'Press Start 2P',monospace;font-size:12px;color:#4aa8d8;">
        {bonus_earned}/{bonus_possible} XP</div>
    </div>""" if bonus_possible > 0 else ""}

    <!-- Message -->
    <div style="background:#0a0000;border:1px solid #8b1a1a;border-radius:3px;
      padding:14px 18px;margin-bottom:20px;text-align:center;">
      <div style="font-size:13px;color:#d4c5a9;line-height:1.7;">{final_msg}</div>
    </div>

    <!-- Achievements -->
    {f"""
    <div style="margin-bottom:16px;">
      <div style="font-family:'Press Start 2P',monospace;font-size:7px;color:#444433;
        letter-spacing:1px;margin-bottom:10px;">⚔️ LOGROS DESBLOQUEADOS</div>
      <div style="display:flex;flex-wrap:wrap;gap:4px;">{ach_html}</div>
    </div>""" if ach_html else ""}

    <!-- Deadline -->
    {"""
    <div style="padding:12px 16px;background:#1a0000;border:2px solid #ff0000;
      border-radius:3px;text-align:center;">
      <div style="font-family:'Press Start 2P',monospace;font-size:10px;color:#ff0000;
        letter-spacing:2px;">🚫 PLAZO VENCIDO</div>
      <div style="font-family:'Press Start 2P',monospace;font-size:7px;color:#ff6666;
        margin-top:6px;">La nota no será actualizada en la base de datos</div>
    </div>""" if DEADLINE_PASSED else f"""
    <div style="text-align:center;font-family:'Press Start 2P',monospace;font-size:7px;
      color:#4aa8d8;letter-spacing:1px;opacity:.9;">
      📊 Calificación final enviada al leaderboard · {n} · {lvl_name}
    </div>"""}
  </div>
</div>'''))
