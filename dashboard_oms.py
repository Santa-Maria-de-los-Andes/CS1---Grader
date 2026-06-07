# dashboard_oms.py — Dashboard estilo OMS / Sala de Operaciones de Emergencia
# Santa María de los Andes — Intro CS, Notebook 3
# Requiere solo IPython (preinstalado en Colab)

from IPython.display import display, HTML
import datetime


# Niveles de alerta OMS
_NIVELES = {
    1: ("NIVEL 1 — MONITOREO",    "#27AE60", "#1a4a2e"),
    2: ("NIVEL 2 — ALERTA",       "#F1C40F", "#4a3c00"),
    3: ("NIVEL 3 — EMERGENCIA",   "#E67E22", "#4a2a00"),
    4: ("NIVEL 4 — PANDEMIA",     "#E74C3C", "#4a1010"),
}

def _calcular_nivel(r0, cfr, tasa_max):
    if r0 > 5  or cfr > 0.3 or tasa_max > 60: return 4
    if r0 > 2  or cfr > 0.1 or tasa_max > 30: return 3
    if r0 > 1  or tasa_max > 10:               return 2
    return 1

def _fmt(n):
    return f"{int(n):,}"


class DashboardOMS:
    """
    Dashboard HTML tipo Sala de Operaciones de Emergencia de la OMS.
    Se renderiza directamente en Google Colab.

    Uso:
        dash = DashboardOMS
        dash.situacion("COVID-19", dia=10, zonas_data=[...], r0=2.5, cfr=0.02,
                       total_infectados=8500, total_muertos=170)
    """

    # ─────────────────────────────────────────────────────────────
    # 1. DASHBOARD PRINCIPAL
    # ─────────────────────────────────────────────────────────────
    @staticmethod
    def situacion(patogeno, dia, zonas_data, r0, cfr,
                  total_infectados, total_muertos, ciudad="", autor=""):
        """
        Dashboard completo de situación de brote.

        patogeno          : nombre del patógeno (str)
        dia               : día actual de la simulación (int)
        zonas_data        : lista de dicts o lista de listas con datos por zona
                            Formato dict:  [{"nombre":"Zona 1","infectados":800,"poblacion":5000}, ...]
                            Formato lista: [[nombre, infectados, poblacion], ...]
        r0                : número de reproducción básico (float)
        cfr               : tasa de mortalidad (0.0–1.0)
        total_infectados  : total acumulado de infectados (int)
        total_muertos     : total acumulado de muertos (int)
        ciudad            : nombre de la ciudad (str, opcional)
        autor             : nombre del estudiante para el pie del reporte (str, opcional)
        """
        # Normalizar zonas_data
        zonas = []
        for z in zonas_data:
            if isinstance(z, dict):
                zonas.append(z)
            elif isinstance(z, (list, tuple)) and len(z) >= 3:
                zonas.append({"nombre": z[0], "infectados": z[1], "poblacion": z[2]})

        # Clasificar zonas
        STATUS_MAP = [
            (0.10, "CONTROLADA", "#27AE60", "#1a3a2a"),
            (0.30, "ALERTA",     "#F1C40F", "#3a3000"),
            (0.60, "CRÍTICA",    "#E67E22", "#3a2000"),
            (1.01, "PERDIDA",    "#E74C3C", "#3a1010"),
        ]
        def clasif(tasa):
            for u, l, c, b in STATUS_MAP:
                if tasa < u: return l, c, b
            return "PERDIDA", "#E74C3C", "#3a1010"

        tasa_max = 0
        zonas_rows = ""
        for z in zonas:
            inf = int(z.get("infectados", 0))
            pob = int(z.get("poblacion", 1))
            tasa = inf / max(pob, 1)
            if tasa > tasa_max: tasa_max = tasa
            label, color, bg = clasif(tasa)
            bar = min(tasa * 100, 100)
            zonas_rows += f"""
              <tr>
                <td style="padding:9px 12px;color:#ECF0F1;font-weight:500">{z.get("nombre","—")}</td>
                <td style="padding:9px 12px;color:{color};font-weight:bold;text-align:right">{_fmt(inf)}</td>
                <td style="padding:9px 12px;text-align:right;color:#95A5A6">{_fmt(pob)}</td>
                <td style="padding:9px 12px">
                  <div style="background:#1a1a2e;border-radius:3px;height:8px;width:120px">
                    <div style="background:{color};width:{bar:.1f}%;height:8px;border-radius:3px"></div>
                  </div>
                </td>
                <td style="padding:9px 12px">
                  <span style="background:{bg};color:{color};border:1px solid {color};
                               padding:3px 9px;border-radius:4px;font-size:11px;font-weight:bold">
                    {label}
                  </span>
                </td>
              </tr>"""

        nivel = _calcular_nivel(r0, cfr, tasa_max * 100)
        nlabel, ncolor, nbg = _niveles = _NIVELES[nivel]
        pulse = "animation:pulse 1.3s infinite;" if nivel >= 3 else ""
        tasa_mort = cfr * 100
        r_efectivo = round(r0, 2)
        fecha = datetime.date.today().strftime("%d %b %Y")
        ciudad_str = f" · {ciudad}" if ciudad else ""
        autor_str  = autor if autor else "Sistema de Vigilancia Epidemiológica SMA"

        html = f"""
<div style="font-family:'Segoe UI',Arial,sans-serif;background:#0a0e1a;
            border-radius:14px;overflow:hidden;border:2px solid {ncolor};
            box-shadow:0 0 30px {ncolor}44">

  <!-- ─── BARRA SUPERIOR ─── -->
  <div style="background:linear-gradient(135deg,#0d1117,#1a1a2e);
              padding:16px 24px;border-bottom:3px solid {ncolor};
              display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px">
    <div>
      <div style="display:flex;align-items:center;gap:12px">
        <span style="font-size:28px">🏥</span>
        <div>
          <h2 style="color:#ECF0F1;margin:0;font-size:20px;letter-spacing:.5px">
            EMERGENCIA EPIDEMIOLÓGICA — {patogeno.upper()}
          </h2>
          <p style="color:#7F8C8D;margin:3px 0 0 0;font-size:12px">
            Centro de Operaciones de Emergencia{ciudad_str} · Día {dia} · {fecha}
          </p>
        </div>
      </div>
    </div>
    <div style="display:flex;align-items:center;gap:12px">
      <div style="background:#1a1a2e;border:1px solid #2c3e50;border-radius:8px;
                  padding:8px 16px;text-align:center">
        <div style="color:#7F8C8D;font-size:10px;letter-spacing:1px">DÍA DE BROTE</div>
        <div style="color:#ECF0F1;font-size:24px;font-weight:bold">{dia}</div>
      </div>
      <div style="background:{nbg};border:2px solid {ncolor};border-radius:10px;
                  padding:10px 20px;text-align:center;{pulse}">
        <div style="color:{ncolor};font-size:13px;font-weight:bold;letter-spacing:.5px">{nlabel}</div>
      </div>
    </div>
  </div>

  <!-- ─── KPIs ─── -->
  <div style="display:flex;gap:1px;background:#0a0e1a">
    {_kpi("🦠", "Infectados Totales",  _fmt(total_infectados), "#3498DB", "#0d2137")}
    {_kpi("💀", "Muertes Estimadas",   _fmt(total_muertos),    "#E74C3C", "#2d0a0a")}
    {_kpi("📈", "R₀ (Reproducción)",  str(r_efectivo),         "#F39C12", "#2d1f00")}
    {_kpi("⚠️", "Tasa de Mortalidad", f"{tasa_mort:.1f}%",      "#8E44AD", "#1e0d2d")}
  </div>

  <!-- ─── TABLA DE ZONAS ─── -->
  <div style="padding:20px 24px">
    <h4 style="color:#BDC3C7;margin:0 0 12px 0;font-size:13px;letter-spacing:1px;
               text-transform:uppercase">Estado por Zona</h4>
    <div style="border-radius:8px;overflow:hidden;border:1px solid #2c3e50">
      <table style="width:100%;border-collapse:collapse;font-size:13px">
        <thead>
          <tr style="background:#1a1a2e;color:#7F8C8D;font-size:11px;letter-spacing:.8px">
            <th style="padding:9px 12px;text-align:left">ZONA</th>
            <th style="padding:9px 12px;text-align:right">INFECTADOS</th>
            <th style="padding:9px 12px;text-align:right">POBLACIÓN</th>
            <th style="padding:9px 12px">TASA</th>
            <th style="padding:9px 12px">ESTADO</th>
          </tr>
        </thead>
        <tbody style="background:#0d1117">
          {zonas_rows}
        </tbody>
      </table>
    </div>
  </div>

  <!-- ─── EVALUACIÓN DE RIESGO ─── -->
  <div style="padding:0 24px 20px">
    <h4 style="color:#BDC3C7;margin:0 0 12px 0;font-size:13px;letter-spacing:1px;
               text-transform:uppercase">Evaluación de Riesgo</h4>
    <div style="display:flex;gap:12px;flex-wrap:wrap">
      {_riesgo_card("Transmisibilidad", r0, 1.0, 3.0, 6.0, "R₀")}
      {_riesgo_card("Mortalidad", cfr*100, 1.0, 10.0, 30.0, "CFR %")}
      {_riesgo_card("Saturación Urbana", tasa_max*100, 10.0, 30.0, 60.0, "% infectados")}
    </div>
  </div>

  <!-- ─── PIE ─── -->
  <div style="background:#060912;padding:10px 24px;border-top:1px solid #1a1a2e;
              display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:6px">
    <span style="color:#4a5568;font-size:11px">
      📋 Generado por: <strong style="color:#7F8C8D">{autor_str}</strong>
    </span>
    <span style="color:#4a5568;font-size:11px">
      Sistema de Vigilancia Epidemiológica · Santa María de los Andes · Intro CS
    </span>
  </div>

</div>
<style>
  @keyframes pulse {{ 0%{{opacity:1}} 50%{{opacity:.65}} 100%{{opacity:1}} }}
</style>"""
        display(HTML(html))

    # ─────────────────────────────────────────────────────────────
    # 2. REPORTE DE SITUACIÓN (SitRep) — formato OMS
    # ─────────────────────────────────────────────────────────────
    @staticmethod
    def reporte_sitrep(patogeno, dia, total_infectados, total_muertos, r0, cfr,
                       zonas_data, medidas_tomadas=None, nombre_estudiante="",
                       ciudad=""):
        """
        Genera un Reporte de Situación formato OMS — idéntico a los que
        publica la OMS diariamente durante brotes activos.

        patogeno          : nombre del patógeno
        dia               : día actual
        total_infectados  : acumulado de infectados
        total_muertos     : acumulado de muertos
        r0                : R₀ del patógeno simulado
        cfr               : tasa de mortalidad (0.0–1.0)
        zonas_data        : lista de dicts [{"nombre":..,"infectados":..,"poblacion":..}]
        medidas_tomadas   : lista de strings con medidas implementadas (opcional)
        nombre_estudiante : autor del reporte
        ciudad            : nombre de la ciudad
        """
        fecha     = datetime.date.today().strftime("%d de %B de %Y")
        sitrep_n  = dia
        ciudad_str = ciudad if ciudad else "Ciudad Simulada"
        autor_str  = nombre_estudiante if nombre_estudiante else "Equipo de Vigilancia"
        tasa_ataque = total_infectados / max(sum(int(z.get("poblacion", 0)) for z in zonas_data if isinstance(z, dict)), 1) * 100

        if not medidas_tomadas:
            medidas_tomadas = ["— (sin intervenciones registradas)"]

        medidas_li = "".join(f"<li style='margin-bottom:6px'>{m}</li>" for m in medidas_tomadas)

        # Tabla de zonas para el SitRep
        zonas_filas = ""
        for z in zonas_data:
            if not isinstance(z, dict): continue
            inf = int(z.get("infectados", 0))
            pob = int(z.get("poblacion", 1))
            tasa = inf / max(pob, 1) * 100
            mort = int(inf * cfr)
            zonas_filas += f"""
              <tr style="border-bottom:1px solid #e2e8f0">
                <td style="padding:8px 12px">{z.get("nombre","—")}</td>
                <td style="padding:8px 12px;text-align:right;font-weight:bold">{_fmt(inf)}</td>
                <td style="padding:8px 12px;text-align:right">{_fmt(mort)}</td>
                <td style="padding:8px 12px;text-align:right">{tasa:.1f}%</td>
              </tr>"""

        nivel = _calcular_nivel(r0, cfr, tasa_ataque)
        nlabel, ncolor, _ = _NIVELES[nivel]

        html = f"""
<div style="font-family:Georgia,'Times New Roman',serif;background:#FAFAFA;
            border:2px solid #1a56a4;border-radius:4px;max-width:860px;
            margin:0 auto;overflow:hidden;color:#1a202c">

  <!-- ENCABEZADO -->
  <div style="background:#1a56a4;padding:20px 30px">
    <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:10px">
      <div>
        <div style="color:#93c5fd;font-size:11px;letter-spacing:2px;font-family:'Segoe UI',sans-serif">
          ORGANIZACIÓN MUNDIAL DE LA SALUD — SIMULACIÓN ACADÉMICA
        </div>
        <h1 style="color:#fff;margin:6px 0;font-size:20px">
          Reporte de Situación No. {sitrep_n}
        </h1>
        <h2 style="color:#bfdbfe;margin:0;font-size:15px;font-weight:normal">
          Brote de {patogeno} — {ciudad_str}
        </h2>
      </div>
      <div style="text-align:right">
        <div style="color:#93c5fd;font-size:11px">Fecha de publicación</div>
        <div style="color:#fff;font-size:14px;font-weight:bold">{fecha}</div>
        <div style="margin-top:8px;background:{ncolor};color:#fff;font-family:'Segoe UI',sans-serif;
                    font-size:11px;font-weight:bold;padding:4px 12px;border-radius:3px;
                    letter-spacing:.5px;text-align:center">{nlabel}</div>
      </div>
    </div>
  </div>

  <div style="padding:24px 30px">

    <!-- SITUACIÓN DE UN VISTAZO -->
    <div style="background:#EFF6FF;border-left:4px solid #1a56a4;padding:14px 18px;
                border-radius:0 6px 6px 0;margin-bottom:24px">
      <h3 style="margin:0 0 10px 0;color:#1a56a4;font-size:14px;font-family:'Segoe UI',sans-serif">
        SITUACIÓN DE UN VISTAZO
      </h3>
      <div style="display:flex;gap:30px;flex-wrap:wrap;font-family:'Segoe UI',sans-serif">
        <div><span style="color:#64748b;font-size:12px">Casos confirmados</span><br>
             <strong style="font-size:20px;color:#1a56a4">{_fmt(total_infectados)}</strong></div>
        <div><span style="color:#64748b;font-size:12px">Muertes estimadas</span><br>
             <strong style="font-size:20px;color:#DC2626">{_fmt(total_muertos)}</strong></div>
        <div><span style="color:#64748b;font-size:12px">Tasa de ataque</span><br>
             <strong style="font-size:20px;color:#D97706">{tasa_ataque:.2f}%</strong></div>
        <div><span style="color:#64748b;font-size:12px">R₀ estimado</span><br>
             <strong style="font-size:20px;color:#7C3AED">{r0}</strong></div>
        <div><span style="color:#64748b;font-size:12px">CFR</span><br>
             <strong style="font-size:20px;color:#B45309">{cfr*100:.1f}%</strong></div>
      </div>
    </div>

    <!-- DISTRIBUCIÓN GEOGRÁFICA -->
    <h3 style="color:#1a56a4;border-bottom:1px solid #CBD5E1;padding-bottom:6px;
               font-size:14px;font-family:'Segoe UI',sans-serif;text-transform:uppercase;
               letter-spacing:.8px">Distribución Geográfica</h3>
    <table style="width:100%;border-collapse:collapse;font-size:13px;
                  font-family:'Segoe UI',sans-serif;margin-bottom:24px">
      <thead>
        <tr style="background:#1a56a4;color:#fff">
          <th style="padding:8px 12px;text-align:left">Zona / Distrito</th>
          <th style="padding:8px 12px;text-align:right">Infectados</th>
          <th style="padding:8px 12px;text-align:right">Muertes est.</th>
          <th style="padding:8px 12px;text-align:right">Tasa de ataque</th>
        </tr>
      </thead>
      <tbody>
        {zonas_filas}
        <tr style="background:#EFF6FF;font-weight:bold">
          <td style="padding:8px 12px">TOTAL</td>
          <td style="padding:8px 12px;text-align:right">{_fmt(total_infectados)}</td>
          <td style="padding:8px 12px;text-align:right">{_fmt(total_muertos)}</td>
          <td style="padding:8px 12px;text-align:right">{tasa_ataque:.2f}%</td>
        </tr>
      </tbody>
    </table>

    <!-- MEDIDAS DE SALUD PÚBLICA -->
    <h3 style="color:#1a56a4;border-bottom:1px solid #CBD5E1;padding-bottom:6px;
               font-size:14px;font-family:'Segoe UI',sans-serif;text-transform:uppercase;
               letter-spacing:.8px">Medidas de Salud Pública Aplicadas</h3>
    <ul style="font-size:13px;line-height:1.7;margin:0 0 24px 0;padding-left:20px;
               font-family:'Segoe UI',sans-serif;color:#374151">
      {medidas_li}
    </ul>

    <!-- EVALUACIÓN DE RIESGO NARRATIVA -->
    <h3 style="color:#1a56a4;border-bottom:1px solid #CBD5E1;padding-bottom:6px;
               font-size:14px;font-family:'Segoe UI',sans-serif;text-transform:uppercase;
               letter-spacing:.8px">Evaluación de Riesgo</h3>
    <p style="font-size:13px;line-height:1.8;color:#374151;font-family:'Segoe UI',sans-serif;
              margin-bottom:24px">
      Con un R₀ de <strong>{r0}</strong>, cada persona infectada contagia en promedio
      {r0} personas nuevas {"— la epidemia crece exponencialmente" if r0 > 1 else "— la epidemia está en declive"}.
      La tasa de mortalidad de caso (CFR) de <strong>{cfr*100:.1f}%</strong>
      {"es elevada y requiere respuesta inmediata" if cfr > 0.05 else "es relativamente baja pero el volumen total de casos genera presión sobre el sistema de salud"}.
      La tasa de ataque de {tasa_ataque:.2f}% indica
      {"saturación crítica en múltiples zonas" if tasa_ataque > 30 else "propagación activa que requiere intervención sostenida" if tasa_ataque > 10 else "brote en etapa temprana con oportunidad de contención"}.
    </p>

  </div>

  <!-- PIE -->
  <div style="background:#F1F5F9;padding:12px 30px;border-top:1px solid #CBD5E1;
              font-family:'Segoe UI',sans-serif;font-size:11px;color:#64748b;
              display:flex;justify-content:space-between;flex-wrap:wrap;gap:6px">
    <span>Preparado por: <strong>{autor_str}</strong></span>
    <span>Este reporte es una simulación académica · Santa María de los Andes · Intro CS NB3</span>
  </div>

</div>"""
        display(HTML(html))


# ─────────────────────────────────────────────────────────────
# HELPERS PRIVADOS DE RENDERIZADO
# ─────────────────────────────────────────────────────────────

def _kpi(icono, label, valor, color, bg):
    return f"""
    <div style="flex:1;background:{bg};padding:18px 20px;min-width:140px;
                border-right:1px solid #0a0e1a">
      <div style="font-size:22px;margin-bottom:4px">{icono}</div>
      <div style="color:{color};font-size:26px;font-weight:bold;line-height:1">{valor}</div>
      <div style="color:#7F8C8D;font-size:11px;margin-top:5px;letter-spacing:.5px">{label.upper()}</div>
    </div>"""

def _riesgo_card(titulo, valor, bajo, medio, alto, unidad):
    if valor >= alto:   color, nivel = "#E74C3C", "ALTO"
    elif valor >= medio: color, nivel = "#E67E22", "MEDIO"
    elif valor >= bajo:  color, nivel = "#F1C40F", "BAJO"
    else:               color, nivel = "#27AE60", "MÍNIMO"
    pct = min(valor / max(alto, 0.01) * 100, 100)
    return f"""
    <div style="background:#111827;border:1px solid #2c3e50;border-radius:8px;
                padding:14px 16px;flex:1;min-width:160px">
      <div style="color:#BDC3C7;font-size:11px;margin-bottom:8px;letter-spacing:.5px">
        {titulo.upper()}
      </div>
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px">
        <span style="color:#ECF0F1;font-size:18px;font-weight:bold">{valor:.1f} <span style="font-size:11px;color:#7F8C8D">{unidad}</span></span>
        <span style="background:{color}22;color:{color};border:1px solid {color};
                     padding:2px 8px;border-radius:4px;font-size:11px;font-weight:bold">{nivel}</span>
      </div>
      <div style="background:#1a1a2e;border-radius:4px;height:5px">
        <div style="background:{color};width:{pct:.0f}%;height:5px;border-radius:4px"></div>
      </div>
    </div>"""
