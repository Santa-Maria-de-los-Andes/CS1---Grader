"""
Autograder v3 — Notebook 1: Fundamentos de Python
🎮 MODO AVENTURA — ¡Desbloquea logros, sube de nivel y domina Python!

Novedades v3:
 - Detecta el email de Google Colab automaticamente
 - Envia el puntaje final a Supabase para el leaderboard en vivo
 - Compatible con GitHub Pages (leaderboard.html)
"""

import sys
from IPython.display import HTML, display

# ─── ANSI Colors (rendered in Jupyter output cells) ──────────
_R  = "\033[91m"   # red
_G  = "\033[92m"   # green
_Y  = "\033[93m"   # yellow
_B  = "\033[94m"   # blue
_M  = "\033[95m"   # magenta
_C  = "\033[96m"   # cyan
_BD = "\033[1m"    # bold
_DM = "\033[2m"    # dim
_RS = "\033[0m"    # reset

# ─── Supabase Leaderboard Config ─────────────────────────────
# Reemplaza con las credenciales de tu proyecto Supabase
SUPABASE_URL      = "https://uwykikwutjtkpffwmdiq.supabase.co"
SUPABASE_ANON_KEY = "sb_publishable_aBG6GD4wn9CgpSE-47fagQ_sNhnzznu"

# ─── Total possible XP for Notebook 1 (sum of all max_pts) ──
_NOTEBOOK_MAX = 156

# ─── Level thresholds (by %) ─────────────────────────────────
_LEVELS = [
    (96, 6, "💎 Dios del Código Eterno"),
    (81, 5, "⚡ Archimago del Caos"),
    (61, 4, "🐉 Domador de Programas"),
    (41, 3, "🔮 Hechicero Codicioso"),
    (21, 2, "⚗️ Alquimista de Variables"),
    (0,  1, "👾 Engendro del Código"),
]

def _level_info(pct):
    for thresh, num, name in _LEVELS:
        if pct >= thresh:
            return num, name
    return 1, "👾 Engendro del Código"

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


def _block_bar(filled, total, width=20):
    n = round(width * filled / total) if total else 0
    return "█" * n + "░" * (width - n)


def _xp_bar(pct, width=26):
    n = round(width * pct / 100)
    return f"{_G}{'▰' * n}{_DM}{'▱' * (width - n)}{_RS}"


# ─── Autograder ──────────────────────────────────────────────

class Autograder:

    def __init__(self):
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except AttributeError:
            pass
        self._scores       = {}   # key -> (earned, possible)
        self._achievements = set()
        self._streak       = 0
        self._prev_level   = 0
        self._email        = None
        self._print_welcome()

    # ── Welcome screen ──────────────────────────────────────

    def _print_welcome(self):
        html = '''
<link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">
<style>
  @keyframes pg-glow  {0%,100%{text-shadow:0 0 12px rgba(255,215,0,.8),2px 2px 0 #7a5500}50%{text-shadow:0 0 28px rgba(255,215,0,1),0 0 55px rgba(255,140,0,.5),2px 2px 0 #7a5500}}
  @keyframes pg-blink {50%{opacity:0}}
  @keyframes pg-float {0%,100%{transform:translateY(0)}50%{transform:translateY(-5px)}}
  @keyframes pg-combo {0%,100%{transform:scale(1)}25%{transform:scale(1.12) rotate(-2deg)}75%{transform:scale(1.12) rotate(2deg)}}
  @keyframes pg-achieve{from{opacity:0;transform:translateX(28px)}to{opacity:1;transform:translateX(0)}}
  @keyframes pg-xpscale{from{transform:scaleX(0)}to{transform:scaleX(1)}}
  @keyframes pg-shimmer{0%{background-position:-200% 0}100%{background-position:200% 0}}
  @keyframes pg-levelup{0%{opacity:0;transform:scale(.85)}60%{transform:scale(1.04)}100%{opacity:1;transform:scale(1)}}
</style>
<div style="background:#0d0d1a;border:2px solid #ffd700;border-radius:4px;max-width:840px;margin:10px 0;overflow:hidden;box-shadow:0 0 0 1px #0d0d1a,0 0 0 4px #ffd700,0 0 50px rgba(255,215,0,.12),0 10px 36px rgba(0,0,0,.8);position:relative;">
  <div style="position:absolute;top:0;left:0;right:0;bottom:0;background:repeating-linear-gradient(0deg,rgba(0,0,0,0) 0px,rgba(0,0,0,0) 3px,rgba(0,0,0,.04) 3px,rgba(0,0,0,.04) 4px);pointer-events:none;z-index:5;"></div>
  <div style="background:linear-gradient(90deg,#120f00,#231a00,#120f00);border-bottom:2px solid #ffd700;padding:20px 24px;text-align:center;">
    <div style="font-family:'Press Start 2P',monospace;font-size:20px;color:#ffd700;animation:pg-glow 2.5s ease-in-out infinite;letter-spacing:3px;margin-bottom:10px;">⚔ PYTHON QUEST ⚔</div>
    <div style="font-family:'Press Start 2P',monospace;font-size:9px;color:#9d4edd;letter-spacing:2px;">NOTEBOOK I — FUNDAMENTOS DE PYTHON</div>
  </div>
  <div style="padding:20px 24px;">
    <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;margin-bottom:16px;">
      <div style="background:rgba(0,245,212,.04);border:1px solid rgba(0,245,212,.25);border-radius:3px;padding:14px;">
        <div style="font-family:'Press Start 2P',monospace;font-size:7px;color:#00f5d4;margin-bottom:10px;letter-spacing:1px;">⚡ MISIONES</div>
        <div style="color:#8888bb;font-size:12px;line-height:1.9;">Variables &amp; Tipos<br>Función print()<br>f-strings<br>Operadores</div>
      </div>
      <div style="background:rgba(157,78,221,.04);border:1px solid rgba(157,78,221,.25);border-radius:3px;padding:14px;">
        <div style="font-family:'Press Start 2P',monospace;font-size:7px;color:#9d4edd;margin-bottom:10px;letter-spacing:1px;">🏆 SISTEMA XP</div>
        <div style="color:#8888bb;font-size:12px;line-height:1.9;">6 Niveles<br>Logros &amp; Trofeos<br>Combos x Rachas<br>Boss Battles</div>
      </div>
      <div style="background:rgba(255,51,102,.04);border:1px solid rgba(255,51,102,.25);border-radius:3px;padding:14px;">
        <div style="font-family:'Press Start 2P',monospace;font-size:7px;color:#ff3366;margin-bottom:10px;letter-spacing:1px;">🌌 NIVELES</div>
        <div style="color:#8888bb;font-size:11px;line-height:1.9;">👾 Engendro<br>⚗️ Alquimista<br>🔮 Hechicero<br>🐉 Domador<br>⚡ Archimago<br>💎 Dios</div>
      </div>
    </div>
    <div style="background:rgba(57,255,20,.04);border:1px solid rgba(57,255,20,.3);border-radius:3px;padding:12px 16px;text-align:center;animation:pg-float 3s ease-in-out infinite;">
      <span style="font-family:'Press Start 2P',monospace;font-size:8px;color:#39ff14;animation:pg-blink 1.5s step-end infinite;letter-spacing:1px;">▶  EJECUTA TU PRIMERA CELDA PARA COMENZAR</span>
    </div>
  </div>
</div>
        '''
        display(HTML(html))

    # ── Internal helpers ────────────────────────────────────

    def _nombre(self):
        n = _get("nombre")
        if isinstance(n, str) and n.strip() and n.strip() not in ("?", ""):
            return n.strip()
        return "estudiante"

    def _totals(self):
        earned   = sum(e for e, _ in self._scores.values())
        possible = sum(p for _, p in self._scores.values())
        # pct is always over the full notebook max so levels reflect true progress
        pct      = round(earned / _NOTEBOOK_MAX * 100)
        return earned, possible, pct

    def _unlock(self, key):
        if key not in self._achievements:
            self._achievements.add(key)
            return True
        return False

    # ── Display ─────────────────────────────────────────────

    def _header(self, title, icon="🎯", pts=None):
        self._curr_title = title
        self._curr_icon = icon
        self._curr_pts = pts

    def _row(self, ok, label, msg):
        pass # Not used in HTML rendering

    def _check_achievements(self, key):
        unlocked = []
        earned, possible, pct = self._totals()

        perfect_names = {
            "mini_a":  ("🏅 Perfil Perfecto", "#cba6f7", "Épico"),
            "mini_b":  ("🔬 Type Detective", "#89b4fa", "Raro"),
            "mini_c":  ("🛒 Lonchera Pro", "#89b4fa", "Raro"),
            "mini_d":  ("💬 f-string Wizard", "#89b4fa", "Raro"),
            "ex1":     ("🌡️ Conversor de Elite", "#cba6f7", "Épico"),
            "ex2":     ("💸 IGV Master", "#cba6f7", "Épico"),
            "ex3":     ("📊 Matemático Escolar", "#cba6f7", "Épico"),
            "ex4":     ("⚖️ IMC Master", "#cba6f7", "Épico"),
            "ex5":     ("📧 Email Engineer", "#cba6f7", "Épico"),
            "ex6":     ("📏 Conversor Universal", "#cba6f7", "Épico"),
            "ex7":     ("🎉 Party Planner 5★", "#f9e2af", "Legendario"),
            "cohete":  ("🚀 Rocket Scientist", "#f9e2af", "Legendario"),
        }
        if key in perfect_names and key in self._scores:
            e, p = self._scores[key]
            if e == p and self._unlock(f"perf_{key}"):
                unlocked.append(perfect_names[key])

        if any(e > 0 for e, _ in self._scores.values()) and self._unlock("first_point"):
            unlocked.append(("🎯 ¡Primer XP! — ¡Arrancaste!", "#a6e3a1", "Común"))

        t_keys = ["t1", "t2", "t3"]
        if all(k in self._scores and self._scores[k][0] == self._scores[k][1] for k in t_keys) and self._unlock("quiz_master"):
            unlocked.append(("🧠 Quiz Master", "#cba6f7", "Épico"))

        ex_keys = ["ex1", "ex2", "ex3", "ex4", "ex5", "ex6", "ex7"]
        if all(k in self._scores and self._scores[k][0] > 0 for k in ex_keys) and self._unlock("ejercicios_master"):
            unlocked.append(("⭐ Ejercicios Master", "#f9e2af", "Legendario"))

        if self._streak >= 3 and self._unlock("streak3"):
            unlocked.append(("🔥 Racha x3", "#fab387", "Raro"))
        if self._streak >= 5 and self._unlock("streak5"):
            unlocked.append(("💥 Racha x5", "#f38ba8", "Épico"))

        reto_keys = ["reto1", "reto2", "reto3"]
        if any(k in self._scores and self._scores[k][0] == self._scores[k][1] for k in reto_keys) and self._unlock("reto_master"):
            unlocked.append(("🌌 Físico Avanzado", "#f9e2af", "Legendario"))

        lvl_num, lvl_name = _level_info(pct)
        if lvl_num > self._prev_level and self._prev_level > 0:
            unlocked.append((f"⬆️ ¡NIVEL UP! — {lvl_name}", "#94e2d5", "Nivel"))
        
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

        import threading as _thr
        _thr.Thread(
            target=self._submit_to_supabase,
            args=(earned, possible, pct, lvl_num, lvl_name, True),
            daemon=True,
        ).start()

        # ── Check rows ───────────────────────────────────────
        rows_html = ""
        for ok, label, msg in checks:
            if ok:
                rows_html += (
                    f'<div style="display:flex;align-items:flex-start;gap:10px;padding:7px 10px;'
                    f'margin-bottom:3px;background:rgba(57,255,20,.05);'
                    f'border-left:3px solid #39ff14;border-radius:0 3px 3px 0;">'
                    f'<span style="color:#39ff14;font-size:13px;flex-shrink:0;line-height:1.5;">✔</span>'
                    f'<div style="font-size:11px;line-height:1.5;">'
                    f'<span style="color:#39ff14;font-weight:bold;">{label}:</span> '
                    f'<span style="color:#8888bb;">{msg}</span></div></div>'
                )
            else:
                rows_html += (
                    f'<div style="display:flex;align-items:flex-start;gap:10px;padding:7px 10px;'
                    f'margin-bottom:3px;background:rgba(255,51,102,.05);'
                    f'border-left:3px solid #ff3366;border-radius:0 3px 3px 0;">'
                    f'<span style="color:#ff3366;font-size:13px;flex-shrink:0;line-height:1.5;">✖</span>'
                    f'<div style="font-size:11px;line-height:1.5;">'
                    f'<span style="color:#ff3366;font-weight:bold;">{label}:</span> '
                    f'<span style="color:#ff7799;">{msg}</span></div></div>'
                )

        # ── Stars ────────────────────────────────────────────
        star_r = pts / max_pts if max_pts > 0 else 0
        if star_r == 1.0:
            stars_html = '<span style="color:#ffd700;font-size:15px;letter-spacing:3px;">★★★</span>'
        elif star_r >= 0.67:
            stars_html = '<span style="color:#ffd700;font-size:15px;letter-spacing:3px;">★★</span><span style="color:#2a2a4a;font-size:15px;">★</span>'
        elif star_r > 0:
            stars_html = '<span style="color:#ffd700;font-size:15px;">★</span><span style="color:#2a2a4a;font-size:15px;letter-spacing:3px;">★★</span>'
        else:
            stars_html = '<span style="color:#2a2a4a;font-size:15px;letter-spacing:3px;">★★★</span>'

        # ── Combo ─────────────────────────────────────────────
        combo_html = ""
        if self._streak >= 2:
            c_color = "#ff3366" if self._streak >= 5 else "#ff6b35"
            combo_html = (
                f'<div style="display:inline-flex;align-items:center;gap:5px;padding:3px 10px;'
                f'background:rgba(255,107,53,.12);border:1px solid {c_color};border-radius:2px;'
                f'margin-left:8px;animation:pg-combo .5s ease;">'
                f'<span style="font-family:\'Press Start 2P\',monospace;font-size:7px;color:{c_color};">🔥 COMBO x{self._streak}</span>'
                f'</div>'
            )

        # ── Status ────────────────────────────────────────────
        if pts == max_pts:
            s_icon, s_text, s_color = "⚡", f"¡PERFECTO! +{pts} XP", "#39ff14"
            border_color, glow = "#39ff14", "0 0 22px rgba(57,255,20,.18)"
        elif pts > 0:
            s_icon, s_text, s_color = "✦", f"+{pts} XP  ·  {max_pts - pts} por ganar", "#ffd700"
            border_color, glow = "#ffd700", "0 0 22px rgba(255,215,0,.12)"
        else:
            s_icon, s_text, s_color = "☠", "¡INTENTA DE NUEVO! — Corrige los ✖", "#ff3366"
            border_color, glow = "#ff3366", "0 0 22px rgba(255,51,102,.12)"

        # ── XP bar gradient per level ─────────────────────────
        _XP_GRAD = {
            1: "linear-gradient(90deg,#333355,#6666aa)",
            2: "linear-gradient(90deg,#1b3a0e,#39ff14)",
            3: "linear-gradient(90deg,#0e1b3a,#00f5d4)",
            4: "linear-gradient(90deg,#2d0e3a,#9d4edd)",
            5: "linear-gradient(90deg,#3a2800,#ffd700)",
            6: "linear-gradient(90deg,#ff3366,#ffd700,#39ff14,#00f5d4,#9d4edd)",
        }
        xp_grad = _XP_GRAD.get(lvl_num, _XP_GRAD[1])

        # ── Objective dots ────────────────────────────────────
        dots = "".join(
            f'<span style="display:inline-block;width:7px;height:7px;border-radius:50%;'
            f'background:{"#39ff14" if ok else "#ff3366"};margin:0 2px;'
            f'box-shadow:0 0 4px {"#39ff14" if ok else "#ff3366"};"></span>'
            for ok, _, _ in checks
        )

        # ── Achievements (regular only — level-ups rendered separately) ──
        new_ach    = self._check_achievements(key)
        reg_ach    = [(n, c, r) for n, c, r in new_ach if r != "Nivel"]
        levelup_ach = [(n, c, r) for n, c, r in new_ach if r == "Nivel"]

        ach_html = ""
        _RC = {
            "Común":     ("#cd7f32", "rgba(205,127,50,.12)",  "🥉"),
            "Raro":      ("#c0c0c0", "rgba(192,192,192,.12)", "🥈"),
            "Épico":     ("#ffd700", "rgba(255,215,0,.10)",   "🥇"),
            "Legendario":("#9d4edd", "rgba(157,78,221,.12)",  "💎"),
        }
        for ach_name, _, ach_rarity in reg_ach:
            bc, bg, ach_icon = _RC.get(ach_rarity, _RC["Común"])
            ach_html += (
                f'<div style="display:flex;align-items:center;gap:10px;margin-top:8px;'
                f'padding:10px 12px;background:{bg};border:1px solid {bc};border-radius:3px;'
                f'animation:pg-achieve .4s ease-out;">'
                f'<span style="font-size:18px;">{ach_icon}</span>'
                f'<div style="flex:1;">'
                f'<div style="margin-bottom:3px;">'
                f'<span style="background:{bc};color:#0d0d1a;font-size:7px;font-weight:bold;'
                f'padding:1px 5px;border-radius:2px;'
                f'font-family:\'Press Start 2P\',monospace;">{ach_rarity.upper()}</span>'
                f'<span style="font-family:\'Press Start 2P\',monospace;font-size:7px;'
                f'color:{bc};margin-left:6px;">LOGRO</span>'
                f'</div>'
                f'<div style="color:#e8e8ff;font-size:12px;font-weight:bold;">{ach_name}</div>'
                f'</div>'
                f'</div>'
            )

        curr_icon  = getattr(self, '_curr_icon', '⚔')
        curr_title = getattr(self, '_curr_title', 'MISIÓN').upper()

        card_html = f'''<link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">
<style>
  @keyframes pg-combo  {{0%,100%{{transform:scale(1)}}25%{{transform:scale(1.12) rotate(-2deg)}}75%{{transform:scale(1.12) rotate(2deg)}}}}
  @keyframes pg-achieve{{from{{opacity:0;transform:translateX(25px)}}to{{opacity:1;transform:translateX(0)}}}}
  @keyframes pg-xpscale{{from{{transform:scaleX(0)}}to{{transform:scaleX(1)}}}}
  @keyframes pg-shimmer{{0%{{background-position:-200% 0}}100%{{background-position:200% 0}}}}
</style>
<div style="background:#0d0d1a;border:2px solid {border_color};border-radius:4px;max-width:840px;margin-bottom:14px;overflow:hidden;box-shadow:{glow},0 6px 24px rgba(0,0,0,.6);font-family:'Segoe UI',Roboto,sans-serif;">
  <div style="background:{border_color}0d;border-bottom:1px solid {border_color}40;padding:9px 16px;display:flex;justify-content:space-between;align-items:center;">
    <div style="font-family:'Press Start 2P',monospace;font-size:9px;color:{border_color};letter-spacing:1px;">{curr_icon} {curr_title}</div>
    <div style="display:flex;align-items:center;gap:10px;">
      {stars_html}
      <div style="font-family:'Press Start 2P',monospace;font-size:7px;color:#ff3366;background:rgba(255,51,102,.08);border:1px solid rgba(255,51,102,.35);padding:3px 8px;border-radius:2px;">MAX {max_pts} XP</div>
    </div>
  </div>
  <div style="padding:10px 14px 6px;">{rows_html}</div>
  <div style="background:#09091a;border-top:1px solid #1a1a3a;padding:11px 14px;">
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:9px;">
      <div style="display:flex;align-items:center;gap:8px;">
        <span style="font-size:16px;">{s_icon}</span>
        <span style="font-family:'Press Start 2P',monospace;font-size:8px;color:{s_color};">{s_text}</span>
        {combo_html}
      </div>
      <div style="display:flex;align-items:center;gap:4px;color:#444466;font-size:10px;">{dots}<span style="margin-left:3px;">{passed}/{len(checks)}</span></div>
    </div>
    <div style="display:flex;justify-content:space-between;margin-bottom:4px;">
      <span style="font-family:'Press Start 2P',monospace;font-size:7px;color:#444466;">XP {earned}/{_NOTEBOOK_MAX}</span>
      <span style="font-family:'Press Start 2P',monospace;font-size:7px;color:#9d4edd;">{lvl_name}</span>
    </div>
    <div style="width:100%;height:10px;background:#141428;border:1px solid #2a2a4a;border-radius:2px;overflow:hidden;">
      <div style="width:{pct}%;height:100%;background:{xp_grad};border-radius:2px;transform-origin:left;animation:pg-xpscale 1.1s cubic-bezier(.4,0,.2,1) forwards;box-shadow:0 0 6px rgba(255,215,0,.2);"></div>
    </div>
    {ach_html}
  </div>
</div>'''
        display(HTML(card_html))

        # ── Level-up banner (shown after the card, full prominence) ──
        for _ in levelup_ach:
            display(HTML(self._render_levelup(lvl_num, lvl_name)))

        return pts
    # ── MINI-A — Variables basicas ───────────────────────────

    def check_mini_a(self):
        """Mini-A — Mi Perfil: nombre, edad, ciudad (6 pts)"""
        self._header("MISIÓN A — Mi Perfil", icon="👤", pts=6)
        checks = []
        nombre = _get("nombre")
        edad   = _get("edad")
        ciudad = _get("ciudad")

        if nombre is None:
            checks.append((False, "nombre", "No definida"))
        elif not isinstance(nombre, str):
            checks.append((False, "nombre", f"Debe ser str con tu nombre real, recibi {type(nombre).__name__}"))
        elif nombre.strip() in ("", "?"):
            checks.append((False, "nombre", f"Debe ser str con tu nombre real, recibi '{nombre}'"))
        else:
            checks.append((True, "nombre", f"str ✓  '{nombre}'"))

        if edad is None:
            checks.append((False, "edad", "No definida — usa entero sin comillas, ej: edad = 15"))
        elif isinstance(edad, bool) or not isinstance(edad, int):
            checks.append((False, "edad", f"Debe ser int (sin comillas), recibi {type(edad).__name__}"))
        elif not (5 <= edad <= 110):
            checks.append((False, "edad", f"Valor {edad} fuera de rango (5–110)"))
        else:
            checks.append((True, "edad", f"int ✓  {edad}"))

        if ciudad is None:
            checks.append((False, "ciudad", "No definida"))
        elif not isinstance(ciudad, str):
            checks.append((False, "ciudad", f"Debe ser str con tu ciudad real, recibi {type(ciudad).__name__}"))
        elif ciudad.strip() in ("", "?"):
            checks.append((False, "ciudad", "Debe ser str con tu ciudad real"))
        else:
            checks.append((True, "ciudad", f"str ✓  '{ciudad}'"))

        return self._award("mini_a", checks, 6)

    # ── T1 — Tipo int ────────────────────────────────────────

    def check_t1(self):
        """T1 — ¿Tipo de edad = 15? (4 pts)"""
        self._header("QUIZ T1 — Tipos de datos", icon="🧠", pts=4)
        r = _get("respuesta_t1")
        checks = []
        if r is None:
            checks.append((False, "respuesta_t1", "No definida — escribe: respuesta_t1 = 'letra'"))
        elif not isinstance(r, str):
            checks.append((False, "respuesta_t1", "Debe ser str, ej: respuesta_t1 = 'c'"))
        elif r.strip().lower() == "c":
            checks.append((True, "respuesta_t1", "¡Correcto! edad = 15 → int (numero entero)"))
        else:
            checks.append((False, "respuesta_t1", f"Incorrecto ('{r}'). Pista: 15 no tiene punto decimal."))
        return self._award("t1", checks, 4)

    # ── MINI-B — Tipos correctos ─────────────────────────────

    def check_mini_b(self):
        """Mini-B — temperatura (float), piso (int), barrio (str) (6 pts)"""
        self._header("MISIÓN B — Tipos Correctos", icon="🔬", pts=6)
        checks = []
        temp = _get("temperatura")
        piso = _get("piso")
        bar  = _get("barrio")

        if temp is None:
            checks.append((False, "temperatura", "No definida — usa float con punto decimal, ej: 36.6"))
        elif not isinstance(temp, float):
            checks.append((False, "temperatura",
                           f"Debe ser float (decimal), recibi {type(temp).__name__}. Ej: 36.6"))
        else:
            checks.append((True, "temperatura", f"float ✓  {temp}"))

        if piso is None:
            checks.append((False, "piso", "No definida — usa int (numero entero), ej: 3"))
        elif isinstance(piso, bool) or not isinstance(piso, int):
            checks.append((False, "piso", f"Debe ser int (sin decimal), recibi {type(piso).__name__}"))
        else:
            checks.append((True, "piso", f"int ✓  {piso}"))

        if bar is None:
            checks.append((False, "barrio", "No definida — usa str entre comillas, ej: 'Santa Maria'"))
        elif not isinstance(bar, str):
            checks.append((False, "barrio", f"Debe ser str entre comillas, recibi {type(bar).__name__}"))
        elif bar.strip() in ("", "?"):
            checks.append((False, "barrio", "Debe ser str entre comillas"))
        else:
            checks.append((True, "barrio", f"str ✓  '{bar}'"))

        return self._award("mini_b", checks, 6)

    # ── T2 — Funcion print ───────────────────────────────────

    def check_t2(self):
        """T2 — ¿Que funcion muestra texto? (4 pts)"""
        self._header("QUIZ T2 — Función print()", icon="🧠", pts=4)
        r = _get("respuesta_t2")
        checks = []
        if r is None:
            checks.append((False, "respuesta_t2", "No definida — escribe: respuesta_t2 = 'letra'"))
        elif not isinstance(r, str):
            checks.append((False, "respuesta_t2", "Debe ser str, ej: respuesta_t2 = 'd'"))
        elif r.strip().lower() == "d":
            checks.append((True, "respuesta_t2", "¡Correcto! print() muestra texto en pantalla"))
        else:
            checks.append((False, "respuesta_t2", f"Incorrecto ('{r}'). Pista: ¿que funcion usamos en cada ejemplo?"))
        return self._award("t2", checks, 4)

    # ── T3 — Tipo float ──────────────────────────────────────

    def check_t3(self):
        """T3 — ¿Tipo de precio = 9.99? (4 pts)"""
        self._header("QUIZ T3 — Tipo float", icon="🧠", pts=4)
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

    # ── MINI-D — f-string presentacion ──────────────────────

    def check_mini_d(self):
        """Mini-D — presentacion con f-string (6 pts)"""
        self._header("MISIÓN D — Presentación con f-string", icon="💬", pts=6)
        checks = []
        nombre       = _get("nombre")
        ciudad       = _get("ciudad")
        presentacion = _get("presentacion")

        if not isinstance(nombre, str) or nombre.strip() in ("", "?"):
            checks.append((False, "nombre", "No definida o vacia — ¿completaste la Mision A?"))
        else:
            checks.append((True, "nombre", f"str ✓  '{nombre}'"))

        if not isinstance(ciudad, str) or ciudad.strip() in ("", "?"):
            checks.append((False, "ciudad", "No definida o vacia — ¿completaste la Mision A?"))
        else:
            checks.append((True, "ciudad", f"str ✓  '{ciudad}'"))

        if presentacion is None:
            checks.append((False, "presentacion",
                           "No definida — crea la variable usando f\"...{nombre}...{ciudad}...\""))
        elif not isinstance(presentacion, str):
            checks.append((False, "presentacion", f"Debe ser str, recibi {type(presentacion).__name__}"))
        elif presentacion.strip() in ("", "?"):
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

    # ── MINI-C — La Lonchera ─────────────────────────────────

    def check_mini_c(self):
        """Mini-C — La Lonchera: suma de precios (6 pts)"""
        self._header("MISIÓN C — La Lonchera 🍱", icon="🛒", pts=6)
        checks = []
        ps = _get("precio_sandwich")
        pj = _get("precio_jugo")
        pf = _get("precio_fruta")
        tl = _get("total_lonchera")

        for vname, val in [("precio_sandwich", ps), ("precio_jugo", pj), ("precio_fruta", pf)]:
            if val is None:
                checks.append((False, vname, "No definida"))
            elif not isinstance(val, (int, float)) or isinstance(val, bool):
                checks.append((False, vname, f"Debe ser numero, recibi {type(val).__name__}"))
            elif val <= 0:
                checks.append((False, vname,
                               f"Debe ser positivo — cambia 0.0 por el precio real, ej: {vname} = 3.50"))
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
                checks.append((False, "total_lonchera", f"Deberia ser {exp:.2f}, obtuve {tl}"))
        else:
            checks.append((False, "total_lonchera", "Define primero los tres precios con valores positivos"))

        return self._award("mini_c", checks, 6)

    # ── EX 1 — Temperatura + f-string ───────────────────────

    def check_ex1(self):
        """Ex1 — Conversion Celsius -> Fahrenheit (6 pts)"""
        self._header("EJERCICIO 1 — Conversión de Temperatura 🌡️", icon="🎯", pts=6)
        checks = []
        celsius    = _get("celsius")
        fahrenheit = _get("fahrenheit")

        if celsius is None:
            checks.append((False, "celsius", "No definida — crea la variable: celsius = 25"))
        elif isinstance(celsius, bool) or not isinstance(celsius, (int, float)):
            checks.append((False, "celsius", f"Debe ser numero, recibi {type(celsius).__name__}"))
        else:
            checks.append((True, "celsius", f"numero ✓  {celsius}"))

        if fahrenheit is None:
            checks.append((False, "fahrenheit",
                           "No definida — escribe: fahrenheit = celsius * 9/5 + 32"))
        elif isinstance(fahrenheit, bool) or not isinstance(fahrenheit, (int, float)):
            checks.append((False, "fahrenheit",
                           f"Debe ser numero (resultado del calculo), recibi {type(fahrenheit).__name__}"))
        elif fahrenheit == 0.0 and celsius is not None and not _approx(celsius * 9/5 + 32, 0.0, tol=0.01):
            checks.append((False, "fahrenheit",
                           "¿Reemplazaste el 0.0 con la formula? Escribe: fahrenheit = celsius * 9/5 + 32"))
        elif celsius is not None and isinstance(celsius, (int, float)) and not isinstance(celsius, bool):
            exp = celsius * 9 / 5 + 32
            if _approx(fahrenheit, exp, tol=0.01):
                checks.append((True, "fahrenheit = celsius x 9/5 + 32", f"✓  {fahrenheit:.2f}°F"))
            else:
                checks.append((False, "fahrenheit",
                               f"Para {celsius}°C deberia ser {exp:.2f}°F, obtuve {fahrenheit}. "
                               f"Escribe: fahrenheit = celsius * 9/5 + 32"))
        else:
            checks.append((False, "fahrenheit", "Define primero celsius con un valor numerico"))

        return self._award("ex1", checks, 6)

    def check_ex1_fstring(self):
        """Ex1-F — mensaje_temperatura con f-string (4 pts)"""
        self._header("EJ 1-F — F-string: mensaje_temperatura", icon="💬", pts=4)
        checks = []
        celsius    = _get("celsius")
        fahrenheit = _get("fahrenheit")
        msg        = _get("mensaje_temperatura")

        if msg is None:
            checks.append((False, "mensaje_temperatura",
                           "No definida — crea: mensaje_temperatura = f\"...{celsius}...{fahrenheit}...\""))
        elif not isinstance(msg, str):
            checks.append((False, "mensaje_temperatura", f"Debe ser str, recibi {type(msg).__name__}"))
        elif msg.strip() in ("", "?"):
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

    # ── EX 2 — IGV + f-string ────────────────────────────────

    def check_ex2(self):
        """Ex2 — Compra con IGV 18% (8 pts)"""
        self._header("EJERCICIO 2 — Compra con IGV 💸", icon="🎯", pts=8)
        checks = []
        base  = _get("precio_base")
        igv   = _get("igv")
        final = _get("precio_final")

        if base is None:
            checks.append((False, "precio_base", "No definida — crea la variable: precio_base = 200.0"))
        elif isinstance(base, bool) or not isinstance(base, (int, float)):
            checks.append((False, "precio_base", f"Debe ser numero, recibi {type(base).__name__}"))
        elif base <= 0:
            checks.append((False, "precio_base", "Debe ser positivo"))
        else:
            checks.append((True, "precio_base", f"numero ✓  {base}"))

        if igv is None:
            checks.append((False, "igv", "No definida — escribe: igv = precio_base * 0.18"))
        elif isinstance(igv, bool) or not isinstance(igv, (int, float)):
            checks.append((False, "igv", f"Debe ser numero, recibi {type(igv).__name__}"))
        elif igv == 0.0 and base is not None and base > 0:
            checks.append((False, "igv",
                           "¿Reemplazaste el 0.0 con la formula? Escribe: igv = precio_base * 0.18"))
        elif base is not None and isinstance(base, (int, float)) and not isinstance(base, bool):
            exp = base * 0.18
            if _approx(igv, exp, tol=0.01):
                checks.append((True, "igv = precio_base x 0.18", f"✓  {igv:.2f}"))
            else:
                checks.append((False, "igv",
                               f"Para base={base}, IGV deberia ser {exp:.2f}, obtuve {igv}. "
                               f"Escribe: igv = precio_base * 0.18"))
        else:
            checks.append((False, "igv", "Define primero precio_base con un valor positivo"))

        if final is None:
            checks.append((False, "precio_final",
                           "No definida — escribe: precio_final = precio_base + igv"))
        elif isinstance(final, bool) or not isinstance(final, (int, float)):
            checks.append((False, "precio_final", f"Debe ser numero, recibi {type(final).__name__}"))
        elif final == 0.0 and base is not None and base > 0:
            checks.append((False, "precio_final",
                           "¿Reemplazaste el 0.0 con la formula? Escribe: precio_final = precio_base + igv"))
        elif base is not None and isinstance(base, (int, float)) and not isinstance(base, bool):
            exp = base * 1.18
            if _approx(final, exp, tol=0.01):
                checks.append((True, "precio_final = precio_base + igv", f"✓  {final:.2f}"))
            else:
                checks.append((False, "precio_final",
                               f"Deberia ser {exp:.2f}, obtuve {final}. "
                               f"Escribe: precio_final = precio_base + igv"))
        else:
            checks.append((False, "precio_final", "Define primero precio_base con un valor positivo"))

        return self._award("ex2", checks, 8)

    def check_ex2_fstring(self):
        """Ex2-F — mensaje_igv con f-string (4 pts)"""
        self._header("EJ 2-F — F-string: mensaje_igv", icon="💬", pts=4)
        checks = []
        base  = _get("precio_base")
        final = _get("precio_final")
        msg   = _get("mensaje_igv")

        if msg is None:
            checks.append((False, "mensaje_igv",
                           "No definida — crea: mensaje_igv = f\"...{precio_base}...{precio_final}...\""))
        elif not isinstance(msg, str):
            checks.append((False, "mensaje_igv", f"Debe ser str, recibi {type(msg).__name__}"))
        elif msg.strip() in ("", "?"):
            checks.append((False, "mensaje_igv", "Debe ser un f-string con tu mensaje"))
        else:
            b_str = (str(int(base)) if isinstance(base, float) and base == int(base)
                     else (str(base) if base is not None else ""))
            f_str = str(final) if final is not None else ""
            has_val = (b_str and b_str in msg) or (f_str and f_str in msg)
            if has_val:
                checks.append((True, "mensaje_igv contiene los valores", f"✓  '{msg[:60]}'"))
            else:
                checks.append((False, "mensaje_igv",
                               "El mensaje debe incluir los valores de precio_base y/o precio_final"))

        return self._award("ex2_f", checks, 4)

    # ── EX 3 — Promedio ──────────────────────────────────────

    def check_ex3(self):
        """Ex3 — Promedio de tres notas (8 pts)"""
        self._header("EJERCICIO 3 — Promedio Escolar 📊", icon="🎯", pts=8)
        checks = []
        notas    = [_get(f"nota{i}") for i in range(1, 4)]
        promedio = _get("promedio")

        for i, nota in enumerate(notas, 1):
            if nota is None:
                checks.append((False, f"nota{i}",
                               f"No definida — escribe: nota{i} = 15  (un numero entre 0 y 20)"))
            elif isinstance(nota, bool) or not isinstance(nota, (int, float)):
                checks.append((False, f"nota{i}", f"Debe ser numero, recibi {type(nota).__name__}"))
            elif not (0 <= nota <= 20):
                checks.append((False, f"nota{i}", f"Fuera del rango 0-20 (obtuve {nota})"))
            else:
                checks.append((True, f"nota{i}", f"✓  {nota}"))

        valid = [n for n in notas if isinstance(n, (int, float)) and not isinstance(n, bool)]
        if promedio is None:
            checks.append((False, "promedio",
                           "No definida — escribe: promedio = (nota1 + nota2 + nota3) / 3"))
        elif isinstance(promedio, bool) or not isinstance(promedio, (int, float)):
            checks.append((False, "promedio", f"Debe ser numero, recibi {type(promedio).__name__}"))
        elif promedio == 0.0 and len(valid) == 3 and sum(valid) != 0:
            checks.append((False, "promedio",
                           "¿Escribiste la formula? Escribe: promedio = (nota1 + nota2 + nota3) / 3"))
        elif len(valid) == 3:
            exp = sum(valid) / 3
            if _approx(promedio, exp, tol=0.01):
                checks.append((True, "promedio correcto", f"✓  {promedio:.2f}"))
            else:
                checks.append((False, "promedio",
                               f"Deberia ser {exp:.4f}, obtuve {promedio}. "
                               f"Recuerda los parentesis: (nota1 + nota2 + nota3) / 3"))
        else:
            checks.append((False, "promedio", "Define primero las tres notas"))

        return self._award("ex3", checks, 8)

    # ── EX 4 — IMC ───────────────────────────────────────────

    def check_ex4(self):
        """Ex4 — Calculadora de IMC (9 pts)"""
        self._header("EJERCICIO 4 — Calculadora de IMC ⚖️", icon="🎯", pts=9)
        checks = []
        peso   = _get("peso")
        altura = _get("altura")
        imc    = _get("imc")

        if peso is None:
            checks.append((False, "peso", "No definida — escribe: peso = 60.5  (en kg)"))
        elif isinstance(peso, bool) or not isinstance(peso, (int, float)):
            checks.append((False, "peso", f"Debe ser numero, recibi {type(peso).__name__}"))
        elif peso == 0.0:
            checks.append((False, "peso",
                           "¿Reemplazaste el 0.0 con tu peso real? Ej: peso = 60.5"))
        elif not (20 <= peso <= 300):
            checks.append((False, "peso", f"Valor {peso} fuera de rango (20-300 kg)"))
        else:
            checks.append((True, "peso", f"✓  {peso} kg"))

        if altura is None:
            checks.append((False, "altura", "No definida — escribe en metros, ej: altura = 1.70"))
        elif isinstance(altura, bool) or not isinstance(altura, (int, float)):
            checks.append((False, "altura", f"Debe ser numero, recibi {type(altura).__name__}"))
        elif altura == 0.0:
            checks.append((False, "altura",
                           "¿Reemplazaste el 0.0 con tu altura real? Ej: altura = 1.70 (en metros)"))
        elif not (0.5 <= altura <= 3.0):
            checks.append((False, "altura", f"¿Usaste metros? (ej: 1.70 no 170). Obtuve: {altura}"))
        else:
            checks.append((True, "altura", f"✓  {altura} m"))

        if imc is None:
            checks.append((False, "imc", "No definida — escribe: imc = peso / (altura ** 2)"))
        elif isinstance(imc, bool) or not isinstance(imc, (int, float)):
            checks.append((False, "imc", f"Debe ser numero, recibi {type(imc).__name__}"))
        elif imc == 0.0 and peso is not None and altura is not None and peso > 0 and altura > 0:
            checks.append((False, "imc",
                           "¿Reemplazaste el 0.0 con la formula? Escribe: imc = peso / (altura ** 2)"))
        elif (peso is not None and altura is not None
              and isinstance(peso, (int, float)) and not isinstance(peso, bool)
              and isinstance(altura, (int, float)) and not isinstance(altura, bool)
              and altura > 0):
            exp = peso / (altura ** 2)
            if _approx(imc, exp, tol=0.01):
                checks.append((True, "imc = peso / altura^2", f"✓  {imc:.2f}"))
            else:
                checks.append((False, "imc",
                               f"Para peso={peso}, altura={altura}: deberia ser {exp:.2f}, obtuve {imc}. "
                               f"Escribe: imc = peso / (altura ** 2)"))
        else:
            checks.append((False, "imc", "Define primero peso y altura con valores validos"))

        return self._award("ex4", checks, 9)

    # ── EX 5 — Email ─────────────────────────────────────────

    def check_ex5(self):
        """Ex5 — Generador de Email (9 pts)"""
        self._header("EJERCICIO 5 — Generador de Email 📧", icon="🎯", pts=9)
        checks = []
        nu    = _get("nombre_usuario")
        ap    = _get("apellido")
        dom   = _get("dominio")
        email = _get("email")

        for vname, val in [("nombre_usuario", nu), ("apellido", ap), ("dominio", dom)]:
            if val is None:
                checks.append((False, vname, f"No definida — escribe: {vname} = 'tu_valor'"))
            elif not isinstance(val, str):
                checks.append((False, vname, f"Debe ser str, recibi {type(val).__name__}"))
            elif val.strip() in ("", "?"):
                checks.append((False, vname, "Debe ser str no vacio"))
            else:
                checks.append((True, vname, f"str ✓  '{val}'"))

        if email is None:
            checks.append((False, "email",
                           "No definida — combina: "
                           "email = nombre_usuario + '.' + apellido + '@' + dominio"))
        elif not isinstance(email, str):
            checks.append((False, "email", f"Debe ser str, recibi {type(email).__name__}"))
        elif "@" not in email:
            checks.append((False, "email",
                           f"Falta '@' — obtuve: '{email}'. "
                           f"Ej: nombre_usuario + '.' + apellido + '@' + dominio"))
        elif nu and ap and dom:
            nl = nu.lower().replace(" ", "")
            al = ap.lower().replace(" ", "")
            dl = dom.lower()
            el = email.lower()
            if nl in el and al in el and dl in el:
                checks.append((True, "email con nombre+apellido+@+dominio", f"✓  '{email}'"))
            else:
                checks.append((False, "email",
                               f"Debe incluir nombre, apellido y dominio — obtuve: '{email}'"))
        else:
            checks.append((False, "email", "Define primero nombre_usuario, apellido y dominio"))

        return self._award("ex5", checks, 9)

    # ── EX 6 — Conversor de Unidades ─────────────────────────

    def check_ex6(self):
        """Ex6 — Conversor de Unidades (9 pts)"""
        self._header("EJERCICIO 6 — Conversor de Unidades 📏", icon="🎯", pts=9)
        checks = []
        metros   = _get("metros")
        km       = _get("kilometros")
        cm       = _get("centimetros")
        pulgadas = _get("pulgadas")

        if metros is None:
            checks.append((False, "metros", "No definida — escribe: metros = 5.0"))
        elif isinstance(metros, bool) or not isinstance(metros, (int, float)):
            checks.append((False, "metros", f"Debe ser numero, recibi {type(metros).__name__}"))
        elif metros <= 0:
            checks.append((False, "metros", "Debe ser positivo"))
        else:
            checks.append((True, "metros", f"✓  {metros}"))

        metros_ok = (metros is not None and isinstance(metros, (int, float))
                     and not isinstance(metros, bool) and metros > 0)

        if metros_ok:
            for vname, val, exp, tol, formula in [
                ("kilometros",  km,       metros / 1000,    1e-9,  "metros / 1000"),
                ("centimetros", cm,       metros * 100,     1e-6,  "metros * 100"),
                ("pulgadas",    pulgadas, metros * 39.3701, 0.01,  "metros * 39.3701"),
            ]:
                if val is None:
                    checks.append((False, vname, f"No definida — escribe: {vname} = {formula}"))
                elif isinstance(val, bool) or not isinstance(val, (int, float)):
                    checks.append((False, vname, f"Debe ser numero, recibi {type(val).__name__}"))
                elif val == 0.0:
                    checks.append((False, vname,
                                   f"¿Reemplazaste el 0.0 con la formula? Escribe: {vname} = {formula}"))
                elif _approx(val, exp, tol):
                    checks.append((True, vname, f"✓  {val:.4f}"))
                else:
                    checks.append((False, vname,
                                   f"Para {metros} m deberia ser {exp:.4f}, obtuve {val}. "
                                   f"Escribe: {vname} = {formula}"))
        else:
            for vname in ["kilometros", "centimetros", "pulgadas"]:
                checks.append((False, vname, "Define primero 'metros' con un valor positivo"))

        return self._award("ex6", checks, 9)

    # ── EX 7 — Fiesta de Cumpleanos (Boss Battle) ────────────

    def check_ex7(self):
        """Ex7 — Fiesta de Cumpleanos: capstone (15 pts)"""
        self._header("⚔️  JEFE FINAL — Fiesta de Cumpleaños 🎉", icon="⚔️", pts=15)
        print(f"  {_DM}¡El ejercicio mas dificil! 7 variables, todas conectadas.{_RS}")
        checks = []
        nombre_f  = _get("nombre_festejado")
        edad_n    = _get("edad_nueva")
        p_torta   = _get("precio_torta")
        p_deco    = _get("precio_decoracion")
        invitados = _get("num_invitados")
        costo_t   = _get("costo_total")
        costo_pp  = _get("costo_por_persona")

        if nombre_f is None:
            checks.append((False, "nombre_festejado",
                           "No definida — escribe: nombre_festejado = 'Ana'"))
        elif not isinstance(nombre_f, str):
            checks.append((False, "nombre_festejado", f"Debe ser str, recibi {type(nombre_f).__name__}"))
        elif nombre_f.strip() in ("", "?"):
            checks.append((False, "nombre_festejado", "Debe ser str con un nombre real"))
        else:
            checks.append((True, "nombre_festejado", f"str ✓  '{nombre_f}'"))

        if edad_n is None:
            checks.append((False, "edad_nueva",
                           "No definida — escribe: edad_nueva = 15  (sin comillas)"))
        elif isinstance(edad_n, bool) or not isinstance(edad_n, int):
            checks.append((False, "edad_nueva", f"Debe ser int (sin comillas), recibi {type(edad_n).__name__}"))
        elif not (1 <= edad_n <= 110):
            checks.append((False, "edad_nueva", f"Valor {edad_n} fuera de rango"))
        else:
            checks.append((True, "edad_nueva", f"int ✓  {edad_n}"))

        for vname, val in [("precio_torta", p_torta), ("precio_decoracion", p_deco)]:
            if val is None:
                checks.append((False, vname, f"No definida — escribe: {vname} = 80.0  (en soles)"))
            elif isinstance(val, bool) or not isinstance(val, (int, float)):
                checks.append((False, vname, f"Debe ser numero, recibi {type(val).__name__}"))
            elif val <= 0:
                checks.append((False, vname, "Debe ser positivo (en soles)"))
            else:
                checks.append((True, vname, f"float ✓  {val}"))

        if invitados is None:
            checks.append((False, "num_invitados",
                           "No definida — escribe: num_invitados = 10  (sin comillas)"))
        elif isinstance(invitados, bool) or not isinstance(invitados, int):
            checks.append((False, "num_invitados", f"Debe ser int, recibi {type(invitados).__name__}"))
        elif invitados <= 0:
            checks.append((False, "num_invitados", "Debe ser positivo (al menos 1 invitado)"))
        else:
            checks.append((True, "num_invitados", f"int ✓  {invitados}"))

        if costo_t is None:
            checks.append((False, "costo_total",
                           "No definida — usa: costo_total = precio_torta + precio_decoracion"))
        elif isinstance(costo_t, bool) or not isinstance(costo_t, (int, float)):
            checks.append((False, "costo_total", f"Debe ser numero, recibi {type(costo_t).__name__}"))
        elif (p_torta is not None and p_deco is not None
              and isinstance(p_torta, (int, float)) and not isinstance(p_torta, bool)
              and isinstance(p_deco, (int, float)) and not isinstance(p_deco, bool)):
            exp = p_torta + p_deco
            if _approx(costo_t, exp, tol=0.01):
                checks.append((True, "costo_total = precio_torta + precio_decoracion", f"✓  {costo_t}"))
            else:
                checks.append((False, "costo_total",
                               f"Deberia ser {exp:.2f}, obtuve {costo_t}. "
                               f"Escribe: costo_total = precio_torta + precio_decoracion"))
        else:
            checks.append((False, "costo_total", "Define primero precio_torta y precio_decoracion"))

        if costo_pp is None:
            checks.append((False, "costo_por_persona",
                           "No definida — usa: costo_por_persona = costo_total / num_invitados"))
        elif isinstance(costo_pp, bool) or not isinstance(costo_pp, (int, float)):
            checks.append((False, "costo_por_persona", f"Debe ser numero, recibi {type(costo_pp).__name__}"))
        elif (costo_t is not None and invitados is not None
              and isinstance(invitados, int) and not isinstance(invitados, bool)
              and invitados > 0):
            exp = costo_t / invitados
            if _approx(costo_pp, exp, tol=0.01):
                checks.append((True, "costo_por_persona = costo_total / num_invitados", f"✓  {costo_pp:.2f}"))
            else:
                checks.append((False, "costo_por_persona",
                               f"Deberia ser {exp:.2f}, obtuve {costo_pp}. "
                               f"Escribe: costo_por_persona = costo_total / num_invitados"))
        else:
            checks.append((False, "costo_por_persona", "Define primero costo_total y num_invitados"))

        return self._award("ex7", checks, 15)

    # ── TIER 3 — Temperatura ────────────────────────────────

    def check_tier3_temperatura(self):
        """Tier 3 — Celda Completa: fahrenheit_c3 (4 pts)"""
        self._header("TIER 3 — Temperatura: rellena los blancos", icon="🧩", pts=4)
        checks = []
        fahrenheit_c3 = _get("fahrenheit_c3")
        celsius_c3    = _get("celsius_c3")

        if celsius_c3 is not None and isinstance(celsius_c3, (int, float)) and not isinstance(celsius_c3, bool):
            exp = celsius_c3 * 9 / 5 + 32
        else:
            exp = 59.0

        if fahrenheit_c3 is None:
            checks.append((False, "fahrenheit_c3",
                           "No definida — reemplaza ??? con: celsius_c3 * 9/5 + 32"))
        elif isinstance(fahrenheit_c3, bool) or not isinstance(fahrenheit_c3, (int, float)):
            checks.append((False, "fahrenheit_c3",
                           f"Debe ser numero, recibi {type(fahrenheit_c3).__name__}"))
        elif _approx(fahrenheit_c3, exp, tol=0.1):
            checks.append((True, "fahrenheit_c3",
                           f"✓  {fahrenheit_c3:.2f}°F (correcto para {celsius_c3 if celsius_c3 else 15}°C)"))
        else:
            checks.append((False, "fahrenheit_c3",
                           f"Para {celsius_c3 if celsius_c3 else 15}°C deberia ser {exp:.2f}°F, "
                           f"obtuve {fahrenheit_c3}. Formula: celsius_c3 * 9/5 + 32"))

        return self._award("tier3_temp", checks, 4)

    # ── DEBUG 1 ──────────────────────────────────────────────

    def check_debug1(self):
        """Debug 1 — nombre_debug (str corregido) (3 pts)"""
        self._header("🔧 DEBUG 1 — nombre_debug", icon="🔧", pts=3)
        checks = []
        nombre_debug = _get("nombre_debug")

        if nombre_debug is None:
            checks.append((False, "nombre_debug",
                           "No definida — ejecuta la celda de debug y corrigela"))
        elif not isinstance(nombre_debug, str):
            checks.append((False, "nombre_debug",
                           f"Debe ser str, recibi {type(nombre_debug).__name__}. "
                           f"¿Cerraste las comillas? Ej: nombre_debug = \"Ana\""))
        elif nombre_debug.strip() in ("", "?"):
            checks.append((False, "nombre_debug", "Debe ser str con un nombre real"))
        else:
            checks.append((True, "nombre_debug", f"str ✓  '{nombre_debug}' — ¡error corregido!"))

        return self._award("debug1", checks, 3)

    # ── DEBUG 2 ──────────────────────────────────────────────

    def check_debug2(self):
        """Debug 2 — temperatura_debug (float) (3 pts)"""
        self._header("🔧 DEBUG 2 — temperatura_debug", icon="🔧", pts=3)
        checks = []
        temperatura_debug = _get("temperatura_debug")

        if temperatura_debug is None:
            checks.append((False, "temperatura_debug",
                           "No definida — ejecuta la celda de debug y corrigela"))
        elif isinstance(temperatura_debug, bool) or not isinstance(temperatura_debug, float):
            checks.append((False, "temperatura_debug",
                           f"Debe ser float (numero con punto decimal), "
                           f"recibi {type(temperatura_debug).__name__}. "
                           f"Pista: convierte el str a float con float(nota_texto)"))
        else:
            checks.append((True, "temperatura_debug", f"float ✓  {temperatura_debug} — ¡error corregido!"))

        return self._award("debug2", checks, 3)

    # ── DEBUG 3 ──────────────────────────────────────────────

    def check_debug3(self):
        """Debug 3 — celsius_debug == 0, fahrenheit_debug == 32 (4 pts)"""
        self._header("🔧 DEBUG 3 — celsius_debug y fahrenheit_debug", icon="🔧", pts=4)
        checks = []
        celsius_debug    = _get("celsius_debug")
        fahrenheit_debug = _get("fahrenheit_debug")

        if celsius_debug is None:
            checks.append((False, "celsius_debug",
                           "No definida — ejecuta la celda y corrigela"))
        elif isinstance(celsius_debug, bool) or not isinstance(celsius_debug, (int, float)):
            checks.append((False, "celsius_debug", f"Debe ser numero, recibi {type(celsius_debug).__name__}"))
        elif _approx(celsius_debug, 0, tol=0.01):
            checks.append((True, "celsius_debug == 0", f"✓  {celsius_debug}"))
        else:
            checks.append((False, "celsius_debug",
                           f"Deberia ser 0, obtuve {celsius_debug}."))

        if fahrenheit_debug is None:
            checks.append((False, "fahrenheit_debug",
                           "No definida — ejecuta la celda y corrigela"))
        elif isinstance(fahrenheit_debug, bool) or not isinstance(fahrenheit_debug, (int, float)):
            checks.append((False, "fahrenheit_debug",
                           f"Debe ser numero, recibi {type(fahrenheit_debug).__name__}"))
        elif _approx(fahrenheit_debug, 32, tol=0.01):
            checks.append((True, "fahrenheit_debug == 32", f"✓  {fahrenheit_debug}°F"))
        else:
            checks.append((False, "fahrenheit_debug",
                           f"Para 0°C deberia ser 32°F, obtuve {fahrenheit_debug}. "
                           f"Formula: celsius_debug * 9/5 + 32"))

        return self._award("debug3", checks, 4)

    # ── DEBUG OPERADORES ─────────────────────────────────────

    def check_debug_op(self):
        """Debug Operadores — promedio_debug ≈ 15.0 (3 pts)"""
        self._header("🔧 DEBUG 4 — promedio_debug (precedencia)", icon="🔧", pts=3)
        checks = []
        promedio_debug = _get("promedio_debug")

        if promedio_debug is None:
            checks.append((False, "promedio_debug",
                           "No definida — ejecuta la celda de debug y corrigela"))
        elif isinstance(promedio_debug, bool) or not isinstance(promedio_debug, (int, float)):
            checks.append((False, "promedio_debug",
                           f"Debe ser numero, recibi {type(promedio_debug).__name__}"))
        elif _approx(promedio_debug, 15.0, tol=0.01):
            checks.append((True, "promedio_debug ≈ 15.0", f"✓  {promedio_debug:.2f} — ¡error corregido!"))
        else:
            checks.append((False, "promedio_debug",
                           f"Deberia ser 15.00, obtuve {promedio_debug:.2f}. "
                           f"Pista: necesitas parentesis: (nota_d1 + nota_d2 + nota_d3) / 3"))

        return self._award("debug_op", checks, 3)

    # ── DEBUG F-STRING ───────────────────────────────────────

    def check_debug_fstr(self):
        """Debug F-string — mensaje_debug_f contiene 'laptop' y '2500' (3 pts)"""
        self._header("🔧 DEBUG 5 — mensaje_debug_f (f-string)", icon="🔧", pts=3)
        checks = []
        mensaje_debug_f = _get("mensaje_debug_f")

        if mensaje_debug_f is None:
            checks.append((False, "mensaje_debug_f",
                           "No definida — ejecuta la celda de debug y corrigela"))
        elif not isinstance(mensaje_debug_f, str):
            checks.append((False, "mensaje_debug_f",
                           f"Debe ser str, recibi {type(mensaje_debug_f).__name__}"))
        else:
            mf = mensaje_debug_f.lower()
            has_laptop = "laptop" in mf
            has_precio = "2500" in mensaje_debug_f

            if has_laptop and has_precio:
                checks.append((True, "mensaje_debug_f contiene 'laptop' y '2500'",
                               f"✓  '{mensaje_debug_f[:60]}' — ¡error corregido!"))
            else:
                falt = []
                if not has_laptop:
                    falt.append("'laptop'")
                if not has_precio:
                    falt.append("'2500'")
                checks.append((False, "mensaje_debug_f",
                               f"Falta incluir: {', '.join(falt)}. "
                               f"Pista: agrega la 'f' antes de las comillas"))

        return self._award("debug_fstr", checks, 3)

    # ── COHETE — Ecuacion de Tsiolkovsky (Boss) ──────────────

    def check_cohete(self):
        """Cohete — Ecuacion de Tsiolkovsky (10 pts)"""
        import math
        self._header("⚔️  JEFE GUIADO — Combustible del Cohete 🚀", icon="⚔️", pts=10)
        print(f"  {_DM}Ecuacion de Tsiolkovsky — ingenieria espacial real.{_RS}")
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
                               f"Deberia ser {exp_sc:,.0f} kg, obtuve {masa_sc}"))
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
                               f"Deberia ser {exp_ratio:.4f}, obtuve {mrat}"))

        if masa_sc is not None and mrat is not None:
            exp_comb = masa_sc * (mrat - 1)
            if masa_comb is None:
                checks.append((False, "masa_combustible",
                               "No definida — usa: masa_combustible = masa_sin_combustible * (masa_ratio - 1)"))
            elif _approx(masa_comb, exp_comb, tol=1.0):
                checks.append((True, "masa_combustible", f"✓  {masa_comb:,.0f} kg"))
            else:
                checks.append((False, "masa_combustible",
                               f"Deberia ser {exp_comb:,.0f} kg, obtuve {masa_comb:,.0f}"))

        if masa_comb is not None and masa_sc is not None:
            exp_frac = masa_comb / (masa_sc + masa_comb) * 100
            if fraccion is None:
                checks.append((False, "fraccion_combustible",
                               "No definida — usa: "
                               "fraccion_combustible = masa_combustible / "
                               "(masa_sin_combustible + masa_combustible) * 100"))
            elif _approx(fraccion, exp_frac, tol=0.1):
                checks.append((True, "fraccion_combustible", f"✓  {fraccion:.1f}%"))
            else:
                checks.append((False, "fraccion_combustible",
                               f"Deberia ser {exp_frac:.1f}%, obtuve {fraccion}"))

        return self._award("cohete", checks, 10)

    # ── RETO 1 — Movimiento Parabolico ───────────────────────

    def check_reto1(self):
        """Reto 1 — Movimiento Parabolico (6 pts)"""
        import math
        self._header("🌌 RETO CIENTÍFICO 1 — Proyectil", icon="🌌", pts=6)
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
                checks.append((False, "h_max", f"No definida — aplica la formula. Esperado: {exp_h:.2f} m"))
            elif _approx(h_max, exp_h, tol=0.01):
                checks.append((True, "h_max", f"✓  {h_max:.2f} m"))
            else:
                checks.append((False, "h_max",
                               f"Para v0={v0}, angulo={angulo}°: deberia ser {exp_h:.2f} m"))

            if R is None:
                checks.append((False, "R", f"No definida. Esperado: {exp_R:.2f} m"))
            elif _approx(R, exp_R, tol=0.01):
                checks.append((True, "R (alcance)", f"✓  {R:.2f} m"))
            else:
                checks.append((False, "R", f"Deberia ser {exp_R:.2f} m, obtuve {R}"))

            if t_vuelo is None:
                checks.append((False, "t_vuelo", f"No definida. Esperado: {exp_t:.2f} s"))
            elif _approx(t_vuelo, exp_t, tol=0.01):
                checks.append((True, "t_vuelo", f"✓  {t_vuelo:.2f} s"))
            else:
                checks.append((False, "t_vuelo",
                               f"Deberia ser {exp_t:.2f} s, obtuve {t_vuelo}"))

        return self._award("reto1", checks, 6)

    # ── RETO 2 — Dilatacion del Tiempo ───────────────────────

    def check_reto2(self):
        """Reto 2 — Dilatacion del Tiempo Relativista (6 pts)"""
        import math
        self._header("🌌 RETO CIENTÍFICO 2 — Relatividad Especial", icon="🌌", pts=6)
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
                checks.append((False, f"gamma_{i}", f"No definida. Esperado: {gamma_exp:.4f}"))
            elif _approx(g_var, gamma_exp, tol=0.001):
                checks.append((True, f"gamma_{i} ({int(frac*100)}%c)", f"✓  {g_var:.4f}"))
            else:
                checks.append((False, f"gamma_{i}",
                               f"Deberia ser {gamma_exp:.4f}, obtuve {g_var}"))

            if t_var is None:
                checks.append((False, f"t_movimiento_{i}", f"No definida. Esperado: {t_exp:.4f} s"))
            elif _approx(t_var, t_exp, tol=0.001):
                checks.append((True, f"t_movimiento_{i}", f"✓  {t_var:.4f} s"))
            else:
                checks.append((False, f"t_movimiento_{i}",
                               f"Deberia ser {t_exp:.4f} s, obtuve {t_var}"))

        return self._award("reto2", checks, 6)

    # ── RETO 3 — Gravitacion Universal ───────────────────────

    def check_reto3(self):
        """Reto 3 — Ley de Gravitacion Universal (6 pts)"""
        self._header("🌌 RETO CIENTÍFICO 3 — Gravitación Universal", icon="🌌", pts=6)
        checks = []
        G        = 6.674e-11
        m_tierra = 5.972e24

        m_luna   = 7.342e22
        r_tl     = 384400000.0
        exp_F_tl = G * m_tierra * m_luna / r_tl ** 2
        exp_a_lu = exp_F_tl / m_luna
        F_tl     = _get("F_tierra_luna")
        a_lu     = _get("a_luna")

        if F_tl is None:
            checks.append((False, "F_tierra_luna", f"No definida. Esperado: ≈ {exp_F_tl:.3e} N"))
        elif _approx(F_tl, exp_F_tl, tol=exp_F_tl * 0.01):
            checks.append((True, "F_tierra_luna", f"✓  {F_tl:.3e} N"))
        else:
            checks.append((False, "F_tierra_luna",
                           f"Deberia ser {exp_F_tl:.3e} N, obtuve {F_tl:.3e}"))

        if a_lu is None:
            checks.append((False, "a_luna", f"No definida. Esperado: ≈ {exp_a_lu:.5f} m/s²"))
        elif _approx(a_lu, exp_a_lu, tol=exp_a_lu * 0.01):
            checks.append((True, "a_luna", f"✓  {a_lu:.5f} m/s²"))
        else:
            checks.append((False, "a_luna",
                           f"Deberia ser {exp_a_lu:.5f} m/s², obtuve {a_lu}"))

        m_persona = 70.0
        r_tierra  = 6371000.0
        exp_F_per = G * m_tierra * m_persona / r_tierra ** 2
        exp_a_per = exp_F_per / m_persona
        F_per     = _get("F_persona")
        a_per     = _get("a_persona")

        if F_per is None:
            checks.append((False, "F_persona", f"No definida. Esperado: ≈ {exp_F_per:.1f} N"))
        elif _approx(F_per, exp_F_per, tol=exp_F_per * 0.01):
            checks.append((True, "F_persona", f"✓  {F_per:.1f} N"))
        else:
            checks.append((False, "F_persona",
                           f"Deberia ser {exp_F_per:.1f} N, obtuve {F_per}"))

        if a_per is None:
            checks.append((False, "a_persona", f"No definida. Esperado: ≈ {exp_a_per:.4f} m/s²"))
        elif _approx(a_per, exp_a_per, tol=0.01):
            checks.append((True, "a_persona ≈ g", f"✓  {a_per:.4f} m/s² (¡es g!)"))
        else:
            checks.append((False, "a_persona",
                           f"Deberia ser ≈ {exp_a_per:.4f} m/s², obtuve {a_per}"))

        m_sol    = 1.989e30
        r_se     = 1.496e11
        exp_F_se = G * m_sol * m_tierra / r_se ** 2
        exp_a_ti = exp_F_se / m_tierra
        F_se     = _get("F_sol_tierra")
        a_ti     = _get("a_tierra")

        if F_se is None:
            checks.append((False, "F_sol_tierra", f"No definida. Esperado: ≈ {exp_F_se:.3e} N"))
        elif _approx(F_se, exp_F_se, tol=exp_F_se * 0.01):
            checks.append((True, "F_sol_tierra", f"✓  {F_se:.3e} N"))
        else:
            checks.append((False, "F_sol_tierra",
                           f"Deberia ser {exp_F_se:.3e} N, obtuve {F_se:.3e}"))

        if a_ti is None:
            checks.append((False, "a_tierra", f"No definida. Esperado: ≈ {exp_a_ti:.5f} m/s²"))
        elif _approx(a_ti, exp_a_ti, tol=exp_a_ti * 0.01):
            checks.append((True, "a_tierra", f"✓  {a_ti:.5f} m/s²"))
        else:
            checks.append((False, "a_tierra",
                           f"Deberia ser {exp_a_ti:.5f} m/s², obtuve {a_ti}"))

        return self._award("reto3", checks, 6)

    # ── Level-up banner ─────────────────────────────────────

    def _render_levelup(self, lvl_num, lvl_name):
        _LVL_COLOR = {1:"#6666aa",2:"#39ff14",3:"#00f5d4",4:"#9d4edd",5:"#ffd700",6:"#ff3366"}
        _LVL_GRAD  = {
            1: "linear-gradient(135deg,#333355,#6666aa)",
            2: "linear-gradient(135deg,#0a2205,#39ff14)",
            3: "linear-gradient(135deg,#050d1a,#00f5d4)",
            4: "linear-gradient(135deg,#12052a,#9d4edd)",
            5: "linear-gradient(135deg,#1a0f00,#ffd700)",
            6: "linear-gradient(135deg,#1a0010,#ff3366,#ffd700,#39ff14)",
        }
        color = _LVL_COLOR.get(lvl_num, "#ffd700")
        grad  = _LVL_GRAD.get(lvl_num, _LVL_GRAD[1])
        emoji = lvl_name.split()[0]  # grab the leading emoji from level name

        return f'''<link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">
<style>
  @keyframes lu-appear  {{0%{{opacity:0;transform:scale(.65) translateY(20px)}}70%{{transform:scale(1.04) translateY(-4px)}}100%{{opacity:1;transform:scale(1) translateY(0)}}}}
  @keyframes lu-glow    {{0%,100%{{text-shadow:0 0 20px {color}cc,0 0 40px {color}66}}50%{{text-shadow:0 0 50px {color},0 0 90px {color}88,0 0 120px {color}44}}}}
  @keyframes lu-pulse   {{0%,100%{{box-shadow:0 0 0 0 {color}55,0 0 60px {color}22}}60%{{box-shadow:0 0 0 18px transparent,0 0 80px {color}44}}}}
  @keyframes lu-shimmer {{0%{{background-position:-300% 0}}100%{{background-position:300% 0}}}}
  @keyframes lu-stars   {{0%,100%{{opacity:.9;letter-spacing:6px}}50%{{opacity:.25;letter-spacing:10px}}}}
  @keyframes lu-emoji   {{0%{{transform:scale(0) rotate(-20deg)}}70%{{transform:scale(1.2) rotate(5deg)}}100%{{transform:scale(1) rotate(0)}}}}
</style>
<div style="
  background:linear-gradient(160deg,#06000f,#0d0020,#06000f);
  border:3px solid {color};
  border-radius:6px;
  max-width:840px;
  margin:6px 0 16px;
  padding:28px 20px 24px;
  text-align:center;
  animation:lu-appear .75s cubic-bezier(.34,1.56,.64,1) both, lu-pulse 2.2s ease-in-out 1s infinite;
  font-family:'Segoe UI',Roboto,sans-serif;
">
  <div style="font-family:'Press Start 2P',monospace;font-size:8px;color:{color}55;letter-spacing:6px;margin-bottom:14px;animation:lu-stars 1.8s ease-in-out infinite;">
    ✦ &nbsp; ✦ &nbsp; ✦ &nbsp; ✦ &nbsp; ✦ &nbsp; ✦ &nbsp; ✦
  </div>

  <div style="font-family:'Press Start 2P',monospace;font-size:clamp(15px,4vw,24px);color:{color};letter-spacing:5px;margin-bottom:18px;animation:lu-glow 1.6s ease-in-out infinite;">
    ⬆ ¡NIVEL UP!
  </div>

  <div style="font-size:clamp(44px,10vw,64px);line-height:1;margin-bottom:18px;animation:lu-emoji .6s cubic-bezier(.34,1.56,.64,1) .2s both;">
    {emoji}
  </div>

  <div style="
    font-family:'Press Start 2P',monospace;
    font-size:clamp(9px,2.2vw,14px);
    background:{grad};
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
    background-size:300%;
    animation:lu-shimmer 2.5s linear infinite;
    letter-spacing:2px;
    margin-bottom:12px;
    line-height:1.8;
  ">{lvl_name}</div>

  <div style="font-family:'Press Start 2P',monospace;font-size:7px;color:#555577;letter-spacing:3px;margin-bottom:14px;">
    NIVEL {lvl_num} DESBLOQUEADO
  </div>

  <div style="font-family:'Press Start 2P',monospace;font-size:8px;color:{color}55;letter-spacing:6px;animation:lu-stars 1.8s ease-in-out infinite .9s;">
    ✦ &nbsp; ✦ &nbsp; ✦ &nbsp; ✦ &nbsp; ✦ &nbsp; ✦ &nbsp; ✦
  </div>
</div>'''

    # ── Colab email + Supabase submit ───────────────────────

    def _fetch_colab_email(self):
        """Detect the signed-in Google account email in Colab. Returns str or None."""
        # Method 1: gcloud (already configured if Colab has any Google auth)
        try:
            import subprocess
            r = subprocess.run(
                ["gcloud", "config", "get-value", "account"],
                capture_output=True, text=True, timeout=8,
            )
            email = r.stdout.strip().lower()
            if email and "@" in email and "unset" not in email:
                return email
        except Exception:
            pass

        # Method 2: google.auth default credentials + userinfo endpoint
        try:
            import json as _json, urllib.request as _ur
            import google.auth, google.auth.transport.requests
            creds, _ = google.auth.default()
            if not creds.valid:
                creds.refresh(google.auth.transport.requests.Request())
            req = _ur.Request(
                "https://www.googleapis.com/oauth2/v1/userinfo",
                headers={"Authorization": f"Bearer {creds.token}"},
            )
            with _ur.urlopen(req, timeout=8) as resp:
                info = _json.loads(resp.read())
                email = info.get("email", "").lower()
                if "@" in email:
                    return email
        except Exception:
            pass

        # Method 3: trigger Colab auth popup then retry gcloud
        try:
            from google.colab import auth
            auth.authenticate_user()
            import subprocess
            r = subprocess.run(
                ["gcloud", "config", "get-value", "account"],
                capture_output=True, text=True, timeout=8,
            )
            email = r.stdout.strip().lower()
            if email and "@" in email and "unset" not in email:
                return email
        except Exception:
            pass

        return None

    def _submit_to_supabase(self, earned, possible, pct, lvl_num, lvl_name, silent=False):
        """POST the final score to Supabase. Silently skips if not configured."""
        if "YOUR_PROJECT_ID" in SUPABASE_URL or not SUPABASE_URL.startswith("https://"):
            return

        try:
            import json as _json, urllib.request as _ur

            if self._email is None:
                self._email = self._fetch_colab_email()

            email = self._email or "anonimo@sma.edu.pe"

            payload = _json.dumps({
                "email":           email,
                "notebook":        "nb1",
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
                    f'✅ SCORE ENVIADO AL LEADERBOARD &nbsp;·&nbsp; {email}</div>'
                ))

        except Exception as _ex:
            if not silent:
                display(HTML(
                    f'<div style="font-family:\'Press Start 2P\',monospace;font-size:7px;'
                    f'color:#ff3366;background:#1a0202;border:1px solid #ff3366;'
                    f'border-radius:3px;padding:10px 16px;max-width:840px;margin-top:6px;">'
                    f'⚠️ Leaderboard no disponible: {_ex}</div>'
                ))

    # ── RESUMEN FINAL ────────────────────────────────────────

    def resumen(self):
        earned, possible, pct = self._totals()
        n                     = self._nombre()
        lvl_num, lvl_name     = _level_info(pct)

        if pct >= 90:
            nota, nota_msg, nota_color = "AD", "Logro Destacado", "#39ff14"
        elif pct >= 75:
            nota, nota_msg, nota_color = "A",  "Logro Esperado",  "#ffd700"
        elif pct >= 55:
            nota, nota_msg, nota_color = "B",  "En Proceso",      "#ff6b35"
        else:
            nota, nota_msg, nota_color = "C",  "En Inicio",       "#ff3366"

        if pct >= 96:
            final_msg = f"💎 LEYENDA ABSOLUTA. {n.upper()}, eres el Dios del Código Eterno."
        elif pct >= 90:
            final_msg = f"⚡ ¡INCREÍBLE, {n}! Archimago confirmado. El Notebook 2 te aguarda."
        elif pct >= 75:
            final_msg = f"¡Bien hecho, {n}! Repasa los ✖ para alcanzar el AD."
        elif pct >= 55:
            final_msg = f"Buen comienzo, {n}. Dedica tiempo a los ejercicios que fallaron."
        else:
            final_msg = f"{n}, relee la teoría de cada sección. ¡Cada intento suma XP!"

        ach_display = {
            "perf_mini_a":       "🏅 Perfil Perfecto",
            "perf_mini_b":       "🔬 Type Detective",
            "perf_mini_c":       "🛒 Lonchera Pro",
            "perf_mini_d":       "💬 f-string Wizard",
            "perf_ex1":          "🌡️ Conversor de Elite",
            "perf_ex2":          "💸 IGV Master",
            "perf_ex3":          "📊 Matemático Escolar",
            "perf_ex4":          "⚖️ IMC Master",
            "perf_ex5":          "📧 Email Engineer",
            "perf_ex6":          "📏 Conversor Universal",
            "perf_ex7":          "🎉 Party Planner 5★",
            "perf_cohete":       "🚀 Rocket Scientist",
            "first_point":       "🎯 Primer XP",
            "quiz_master":       "🧠 Quiz Master",
            "ejercicios_master": "⭐ Ejercicios Master",
            "streak3":           "🔥 Racha x3",
            "streak5":           "💥 Racha x5",
            "reto_master":       "🌌 Físico Avanzado",
        }
        earned_ach = [label for k, label in ach_display.items() if k in self._achievements]

        # ── XP gradient per level ─────────────────────────────
        _XP_GRAD = {
            1: "linear-gradient(90deg,#333355,#6666aa)",
            2: "linear-gradient(90deg,#1b3a0e,#39ff14)",
            3: "linear-gradient(90deg,#0e1b3a,#00f5d4)",
            4: "linear-gradient(90deg,#2d0e3a,#9d4edd)",
            5: "linear-gradient(90deg,#3a2800,#ffd700)",
            6: "linear-gradient(90deg,#ff3366,#ffd700,#39ff14,#00f5d4,#9d4edd)",
        }
        xp_grad = _XP_GRAD.get(lvl_num, _XP_GRAD[1])

        _LVL_COLOR = {1:"#6666aa",2:"#39ff14",3:"#00f5d4",4:"#9d4edd",5:"#ffd700",6:"#ff3366"}
        lvl_color = _LVL_COLOR.get(lvl_num, "#6666aa")

        # ── Breakdown grid ────────────────────────────────────
        labels = {
            "mini_a":     "Misión A: Mi Perfil",
            "t1":         "Quiz T1: Tipo int",
            "mini_b":     "Misión B: Tipos correctos",
            "t2":         "Quiz T2: Función print",
            "t3":         "Quiz T3: Tipo float",
            "mini_d":     "Misión D: F-string",
            "mini_c":     "Misión C: La Lonchera",
            "tier3_temp": "Tier 3: Temperatura",
            "debug1":     "Debug 1: nombre_debug",
            "debug2":     "Debug 2: temperatura_debug",
            "debug3":     "Debug 3: celsius/fahrenheit",
            "debug_op":   "Debug 4: promedio_debug",
            "debug_fstr": "Debug 5: mensaje_debug_f",
            "ex1":        "Ejercicio 1: Temperatura",
            "ex1_f":      "Ejercicio 1-F: f-string temp",
            "ex2":        "Ejercicio 2: IGV",
            "ex2_f":      "Ejercicio 2-F: f-string IGV",
            "ex3":        "Ejercicio 3: Promedio",
            "ex4":        "Ejercicio 4: IMC",
            "ex5":        "Ejercicio 5: Email",
            "ex6":        "Ejercicio 6: Conversor",
            "ex7":        "⚔️ Jefe 1: Fiesta",
            "cohete":     "⚔️ Jefe 2: Cohete",
            "reto1":      "🌌 Reto 1: Proyectil",
            "reto2":      "🌌 Reto 2: Relatividad",
            "reto3":      "🌌 Reto 3: Gravitación",
        }
        breakdown_items = ""
        for key, label in labels.items():
            if key in self._scores:
                e, p = self._scores[key]
                if e == p:
                    bc, tc, bd_icon = "rgba(57,255,20,.07)",   "#39ff14", "★"
                elif e > 0:
                    bc, tc, bd_icon = "rgba(255,215,0,.07)",   "#ffd700", "◆"
                else:
                    bc, tc, bd_icon = "rgba(255,51,102,.07)",  "#ff3366", "✖"
                breakdown_items += (
                    f'<div style="background:{bc};border:1px solid {tc}40;border-radius:3px;'
                    f'padding:7px 11px;display:flex;justify-content:space-between;align-items:center;">'
                    f'<span style="color:#a8a8cc;font-size:11px;">{bd_icon} {label}</span>'
                    f'<span style="color:{tc};font-weight:bold;'
                    f'font-family:\'Press Start 2P\',monospace;font-size:8px;">{e}/{p}</span>'
                    f'</div>'
                )

        ach_section = ""
        if earned_ach:
            badges = "".join(
                f'<span style="background:rgba(157,78,221,.1);border:1px solid #9d4edd;'
                f'color:#cba6f7;padding:5px 11px;border-radius:20px;font-size:11px;'
                f'font-weight:bold;">{a}</span>'
                for a in earned_ach
            )
            ach_section = (
                f'<div style="padding:16px 20px;border-bottom:1px solid #1a1a3a;">'
                f'<div style="font-family:\'Press Start 2P\',monospace;font-size:8px;'
                f'color:#cba6f7;margin-bottom:12px;letter-spacing:1px;">🏅 LOGROS DESBLOQUEADOS</div>'
                f'<div style="display:flex;flex-wrap:wrap;gap:8px;">{badges}</div>'
                f'</div>'
            )

        html = f'''<link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">
<style>
  @keyframes pg-glow2  {{0%,100%{{text-shadow:0 0 15px rgba(255,215,0,.7),2px 2px 0 #7a5500}}50%{{text-shadow:0 0 32px rgba(255,215,0,1),0 0 60px rgba(255,140,0,.5),2px 2px 0 #7a5500}}}}
  @keyframes pg-xpscale{{from{{transform:scaleX(0)}}to{{transform:scaleX(1)}}}}
  @keyframes pg-float  {{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-5px)}}}}
  @keyframes pg-shimmer{{0%{{background-position:-200% 0}}100%{{background-position:200% 0}}}}
  @keyframes pg-pulse  {{0%,100%{{box-shadow:0 0 0 0 rgba(255,215,0,.4)}}70%{{box-shadow:0 0 0 8px rgba(255,215,0,0)}}}}
</style>
<div style="background:#0d0d1a;border:2px solid #ffd700;border-radius:4px;max-width:920px;margin:20px 0;overflow:hidden;box-shadow:0 0 0 1px #0d0d1a,0 0 0 4px #ffd700,0 0 70px rgba(255,215,0,.12),0 14px 44px rgba(0,0,0,.8);font-family:'Segoe UI',Roboto,sans-serif;">

  <div style="background:linear-gradient(90deg,#120f00,#231a00,#120f00);border-bottom:2px solid #ffd700;padding:22px;text-align:center;">
    <div style="font-family:'Press Start 2P',monospace;font-size:20px;color:#ffd700;animation:pg-glow2 2.5s ease-in-out infinite;letter-spacing:3px;margin-bottom:10px;">🏆 REPORTE FINAL</div>
    <div style="font-family:'Press Start 2P',monospace;font-size:8px;color:#9d4edd;letter-spacing:2px;">PYTHON QUEST — NOTEBOOK I</div>
  </div>

  <div style="display:grid;grid-template-columns:1fr 1fr 1fr;border-bottom:1px solid #1a1a3a;">
    <div style="padding:20px;border-right:1px solid #1a1a3a;text-align:center;">
      <div style="font-family:'Press Start 2P',monospace;font-size:7px;color:#444466;margin-bottom:10px;letter-spacing:1px;">AGENTE</div>
      <div style="font-family:'Press Start 2P',monospace;font-size:11px;color:#e8e8ff;letter-spacing:2px;word-break:break-all;">{n.upper()}</div>
    </div>
    <div style="padding:20px;border-right:1px solid #1a1a3a;text-align:center;">
      <div style="font-family:'Press Start 2P',monospace;font-size:7px;color:#444466;margin-bottom:10px;letter-spacing:1px;">NIVEL</div>
      <div style="font-family:'Press Start 2P',monospace;font-size:9px;color:{lvl_color};line-height:1.6;">{lvl_name}</div>
    </div>
    <div style="padding:20px;text-align:center;">
      <div style="font-family:'Press Start 2P',monospace;font-size:7px;color:#444466;margin-bottom:10px;letter-spacing:1px;">CALIFICACIÓN</div>
      <div style="font-family:'Press Start 2P',monospace;font-size:26px;color:{nota_color};text-shadow:0 0 14px {nota_color};">{nota}</div>
      <div style="font-size:11px;color:{nota_color}99;margin-top:5px;">{nota_msg}</div>
    </div>
  </div>

  <div style="padding:18px 20px;border-bottom:1px solid #1a1a3a;">
    <div style="display:flex;justify-content:space-between;margin-bottom:6px;">
      <span style="font-family:'Press Start 2P',monospace;font-size:7px;color:#444466;">XP TOTAL: {earned}/{_NOTEBOOK_MAX}</span>
      <span style="font-family:'Press Start 2P',monospace;font-size:7px;color:#ffd700;">{pct}%</span>
    </div>
    <div style="width:100%;height:14px;background:#141428;border:1px solid #2a2a4a;border-radius:3px;overflow:hidden;">
      <div style="width:{pct}%;height:100%;background:{xp_grad};border-radius:3px;transform-origin:left;animation:pg-xpscale 1.5s cubic-bezier(.4,0,.2,1) forwards;box-shadow:0 0 10px rgba(255,215,0,.25);"></div>
    </div>
    <div style="text-align:center;margin-top:14px;font-family:'Press Start 2P',monospace;font-size:8px;color:#ffd700;animation:pg-float 3s ease-in-out infinite;">{final_msg}</div>
  </div>

  {ach_section}

  <div style="padding:16px 20px;border-bottom:1px solid #1a1a3a;">
    <div style="font-family:'Press Start 2P',monospace;font-size:8px;color:#89b4fa;margin-bottom:12px;letter-spacing:1px;">📊 DETALLE DE MISIONES</div>
    <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:6px;">
      {breakdown_items}
    </div>
  </div>

  <div style="padding:22px;text-align:center;background:linear-gradient(180deg,#0d0d1a,#090912);">
    <!-- Para usar tu logo real: reemplaza el bloque de abajo con <img src="URL_DE_TU_LOGO" style="height:42px;"> -->
    <div style="display:inline-flex;align-items:center;gap:12px;background:#0a0a14;border:2px solid #ffd700;border-radius:4px;padding:10px 26px;box-shadow:0 0 22px rgba(255,215,0,.22);animation:pg-pulse 2.5s ease-in-out infinite;">
      <span style="font-family:'Press Start 2P',monospace;font-size:18px;background:linear-gradient(135deg,#ffd700,#ff6b35,#ffd700);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-size:200%;animation:pg-shimmer 3s linear infinite;letter-spacing:4px;">SMA</span>
    </div>
    <div style="font-family:'Press Start 2P',monospace;font-size:7px;color:#2a2a4a;margin-top:10px;letter-spacing:1px;">PYTHON QUEST v3 — AUTOGRADER</div>
  </div>

</div>'''
        display(HTML(html))
        self._submit_to_supabase(earned, possible, pct, lvl_num, lvl_name)
