# mapa_brote.py — Mapas de brotes epidémicos en ciudades reales
# Santa María de los Andes — Intro CS, Notebook 3
# Requiere: folium (preinstalado en Colab), IPython

import json
import math
import uuid as _uuid
from IPython.display import display, HTML


# ─────────────────────────────────────────────────────────────
# CSS ESTÁTICO — tema oscuro tipo sala de emergencias
# ─────────────────────────────────────────────────────────────
_CSS = """
<style>
  .mb-wrapper { font-family:'Segoe UI',Arial,sans-serif; background:#0d1117;
                border-radius:12px; overflow:hidden; border:1px solid #2c3e50; }
  .mb-header  { background:linear-gradient(135deg,#0d1117 0%,#1a1a2e 100%);
                padding:14px 20px; display:flex; align-items:center;
                justify-content:space-between; flex-wrap:wrap; gap:10px; }
  .mb-header h2 { color:#ECF0F1; font-size:16px; margin:0 0 3px 0; }
  .mb-header p  { color:#95A5A6; font-size:11px; margin:0; }
  .mb-badge { padding:6px 14px; border-radius:20px; font-size:12px;
              font-weight:bold; letter-spacing:1px; color:#fff; }
  .mb-badge.pulse { animation:mbpulse 1.4s infinite; }
  @keyframes mbpulse { 0%{opacity:1;transform:scale(1)} 50%{opacity:.7;transform:scale(1.06)} 100%{opacity:1;transform:scale(1)} }
  .mb-tag { background:#1e2a3a; color:#7F8C8D; font-size:11px;
            padding:4px 10px; border-radius:4px; border:1px solid #2c3e50; }
  .mb-controls { background:#1a1a2e; padding:12px 20px; border-bottom:2px solid #2c3e50;
                 display:flex; align-items:center; gap:14px; flex-wrap:wrap; }
  .mb-play { background:#3498DB; color:#fff; border:none; border-radius:6px;
             padding:8px 18px; cursor:pointer; font-size:13px; font-weight:bold;
             min-width:110px; transition:background .2s; }
  .mb-play:hover { background:#2980b9; }
  .mb-slider { flex:1; min-width:180px; accent-color:#3498DB; cursor:pointer; }
  .mb-daylabel { color:#fff; font-size:14px; font-weight:bold; background:#2c3e50;
                 padding:6px 14px; border-radius:6px; min-width:60px; text-align:center; }
  .mb-total   { color:#BDC3C7; font-size:12px; background:#2c3e50;
                padding:6px 14px; border-radius:6px; }
  .mb-nota { background:#16213e; padding:8px 20px; font-size:11px;
             color:#7F8C8D; border-top:1px solid #2c3e50; font-style:italic; }
  .leaflet-popup-content-wrapper { background:#1a1a2e !important; color:#ECF0F1 !important;
    border:1px solid #2c3e50 !important; border-radius:8px !important; }
  .leaflet-popup-tip { background:#1a1a2e !important; }
  .mb-popup { padding:12px 15px; min-width:210px; }
  .mb-popup-title { font-size:14px; font-weight:bold; color:#ECF0F1; margin-bottom:8px;
                    border-bottom:1px solid #2c3e50; padding-bottom:6px; }
  .mb-popup-row { display:flex; justify-content:space-between; font-size:12px; margin-bottom:4px; }
  .mb-popup-label { color:#95A5A6; }
  .mb-popup-val   { color:#ECF0F1; font-weight:bold; }
  .mb-popup-status { display:inline-block; padding:3px 10px; border-radius:4px;
                     font-size:11px; font-weight:bold; margin-top:6px; color:#fff; }
</style>
"""

def _build_map_js(uid, frames_json, totales_json, pz_idx, n_dias, dia_actual,
                  animado, centro, zoom):
    """Genera un bloque <script> IIFE completamente autocontenido y sin colisiones."""
    animado_js = "true" if animado else "false"
    return f"""<script>
(function() {{
  var UID      = '{uid}';
  var FRAMES   = {frames_json};
  var TOTALES  = {totales_json};
  var PZ_IDX   = {pz_idx};
  var N_DIAS   = {n_dias};
  var DIA_ACT  = {dia_actual};
  var ANIMADO  = {animado_js};
  var cLayer, lLayer;
  var playing=false, timer=null, curDay=0;

  function fmtN(n) {{
    return Math.round(n).toString().replace(/\\B(?=(\\d{{3}})+(?!\\d))/g,',');
  }}

  function buildPopup(z, dia, isPZ) {{
    var sc={{'CONTROLADA':'#27AE60','ALERTA':'#F39C12','CRÍTICA':'#E67E22','PERDIDA':'#E74C3C'}};
    var c=sc[z.status]||'#999';
    var icuMsg=z.icu_beds>0
      ?(z.icu_ratio>10?'⛔ COLAPSADO ('+z.icu_ratio.toFixed(1)+'×)':z.icu_ratio.toFixed(1)+'× cap.')
      :'❌ Sin UCI registrada';
    return '<div class="mb-popup">'
      +'<div class="mb-popup-title">'+(isPZ?'☣️ ':'')+z.nombre+'</div>'
      +'<div class="mb-popup-row"><span class="mb-popup-label">Día</span><span class="mb-popup-val">'+dia+'</span></div>'
      +'<div class="mb-popup-row"><span class="mb-popup-label">Infectados</span><span class="mb-popup-val">'+fmtN(z.infectados)+'</span></div>'
      +'<div class="mb-popup-row"><span class="mb-popup-label">Tasa</span><span class="mb-popup-val">'+z.tasa+'%</span></div>'
      +'<div class="mb-popup-row"><span class="mb-popup-label">Población</span><span class="mb-popup-val">'+fmtN(z.poblacion)+'</span></div>'
      +'<div class="mb-popup-row"><span class="mb-popup-label">UCI</span>'
      +'<span class="mb-popup-val" style="color:'+(z.icu_ratio>10?'#E74C3C':'#27AE60')+'">'+icuMsg+'</span></div>'
      +'<span class="mb-popup-status" style="background:'+c+'">'+z.status+'</span>'
      +'</div>';
  }}

  function shortLabel(nombre) {{
    var w=nombre.split(' ');
    if(w.length<=2) return nombre;
    var s=w[0]+' '+w[1];
    return s.length>14?s.substring(0,13)+'…':s;
  }}

  function drawFrame(dayIdx) {{
    if(!cLayer||!lLayer) return;
    cLayer.clearLayers(); lLayer.clearLayers();
    var frame=FRAMES[dayIdx], total=TOTALES[dayIdx], maxTasa=0;
    frame.forEach(function(z,i) {{
      if(z.tasa>maxTasa) maxTasa=z.tasa;
      var isPZ=(dayIdx===0&&i===PZ_IDX&&PZ_IDX>=0);
      var diaLbl=ANIMADO?(dayIdx+1):DIA_ACT;
      L.circle(z.coords,{{radius:z.radio,color:z.color,fillColor:z.color,
        fillOpacity:0.38,weight:isPZ?3:1.5,
        dashArray:z.status==='PERDIDA'?'6,4':null
      }}).bindPopup(buildPopup(z,diaLbl,isPZ)).addTo(cLayer);
      var sn=shortLabel(z.nombre);
      var lbl=L.divIcon({{
        html:'<div style="background:rgba(13,17,23,.92);color:#ECF0F1;'
            +'padding:4px 8px;border-radius:4px;font-size:11px;font-weight:bold;'
            +'white-space:nowrap;border:1px solid '+z.color+';line-height:1.4">'
            +sn+'<br><span style="color:'+z.color+';font-size:12px">'+z.tasa+'%</span></div>',
        className:'',iconAnchor:[0,0]
      }});
      L.marker(z.coords,{{icon:lbl}}).addTo(lLayer);
      if(isPZ) {{
        var pzI=L.divIcon({{html:'<div style="font-size:24px;filter:drop-shadow(0 0 6px #C0392B)">☣️</div>',className:'',iconAnchor:[12,12]}});
        L.marker(z.coords,{{icon:pzI}}).bindPopup('<div class="mb-popup"><div class="mb-popup-title">⚠️ PACIENTE ZERO</div><p style="color:#E74C3C;font-size:12px">Origen documentado del brote</p></div>').addTo(lLayer);
      }}
    }});
    var AC={{VERDE:'#27AE60',AMARILLO:'#F1C40F',NARANJA:'#E67E22',ROJO:'#E74C3C'}};
    var al=maxTasa>=60?'ROJO':maxTasa>=30?'NARANJA':maxTasa>=10?'AMARILLO':'VERDE';
    var badge=document.getElementById('mb-alert-'+UID);
    if(badge){{badge.textContent='ALERTA '+al;badge.style.background=AC[al];badge.className='mb-badge'+(al==='ROJO'||al==='NARANJA'?' pulse':'');}}
    var dl=document.getElementById('mb-day-'+UID);if(dl) dl.textContent='Día '+(dayIdx+1);
    var tl=document.getElementById('mb-total-'+UID);if(tl) tl.textContent='🦠 '+fmtN(total)+' infectados';
    var hdr=document.getElementById('mb-hdr-'+UID);if(hdr) hdr.style.borderBottomColor=AC[al];
  }}

  function setDay(d) {{
    curDay=d; drawFrame(d);
    var sl=document.getElementById('mb-slider-'+UID);if(sl) sl.value=d;
  }}
  function togglePlay() {{
    var btn=document.getElementById('mb-play-'+UID);if(!btn) return;
    if(playing) {{
      clearInterval(timer);playing=false;
      btn.textContent='▶ Reproducir';btn.style.background='#3498DB';
    }} else {{
      playing=true;btn.textContent='⏸ Pausar';btn.style.background='#E74C3C';
      timer=setInterval(function(){{
        curDay=(curDay+1)%N_DIAS;setDay(curDay);
        if(curDay===N_DIAS-1){{clearInterval(timer);playing=false;btn.textContent='▶ Reproducir';btn.style.background='#3498DB';}}
      }},850);
    }}
  }}

  setTimeout(function() {{
    var map=L.map('mb-map-'+UID,{{zoomControl:true,scrollWheelZoom:true}})
             .setView({centro},{zoom});
    L.tileLayer('https://{{s}}.basemaps.cartocdn.com/dark_all/{{z}}/{{x}}/{{y}}.png',{{
      attribution:'© OpenStreetMap © CARTO',subdomains:'abcd',maxZoom:19
    }}).addTo(map);
    cLayer=L.layerGroup().addTo(map);
    lLayer=L.layerGroup().addTo(map);
    map.invalidateSize();
    drawFrame(ANIMADO?0:Math.max(0,DIA_ACT-1));
    var sl=document.getElementById('mb-slider-'+UID);
    if(sl) sl.addEventListener('input',function(){{setDay(parseInt(this.value));}});
    var pb=document.getElementById('mb-play-'+UID);
    if(pb) pb.addEventListener('click',togglePlay);
  }},200);
}})();
</script>"""


class MapaBrote:
    """
    Mapas interactivos de brotes epidémicos sobre ciudades reales.
    Uso en Google Colab — NB3 Epidemias.
    """

    CIUDADES = {
        "lima": {
            "nombre":    "Lima, Perú",
            "subtitulo": "COVID-19 — Mayor tasa de mortalidad per cápita del mundo (2021)",
            "centro":    [-12.0464, -77.0428],
            "zoom":      11,
            "nota":      "Perú registró ~6,400 muertes por 100,000 habitantes durante el pico de 2021 — la cifra más alta del mundo.",
            "zonas": [
                {"nombre": "San Juan de Lurigancho", "coords": [-11.9808, -77.0006], "poblacion": 1_100_000, "icu_beds": 45},
                {"nombre": "Ate",                    "coords": [-12.0261, -76.9090], "poblacion":   678_000, "icu_beds": 20},
                {"nombre": "Comas",                  "coords": [-11.9381, -77.0558], "poblacion":   520_000, "icu_beds": 12},
                {"nombre": "Villa El Salvador",      "coords": [-12.2127, -76.9419], "poblacion":   463_000, "icu_beds":  8},
                {"nombre": "San Martín de Porres",   "coords": [-11.9711, -77.0703], "poblacion":   700_000, "icu_beds": 18},
                {"nombre": "Callao",                 "coords": [-12.0566, -77.1180], "poblacion":   430_000, "icu_beds": 35},
            ],
        },
        "cusco": {
            "nombre":    "Cusco, Perú",
            "subtitulo": "COVID-19 — Colapso del sistema de salud, 2020",
            "centro":    [-13.5183, -71.9781],
            "zoom":      12,
            "nota":      "Cusco tenía ~50 camas UCI para una región de 1.3 millones de personas. Urubamba: 0 camas UCI.",
            "zonas": [
                {"nombre": "Cusco",         "coords": [-13.5183, -71.9781], "poblacion": 120_000, "icu_beds": 50},
                {"nombre": "San Sebastián", "coords": [-13.5386, -71.9420], "poblacion":  85_000, "icu_beds":  5},
                {"nombre": "San Jerónimo",  "coords": [-13.5530, -71.8939], "poblacion":  45_000, "icu_beds":  2},
                {"nombre": "Wanchaq",       "coords": [-13.5336, -71.9743], "poblacion":  65_000, "icu_beds":  8},
                {"nombre": "Santiago",      "coords": [-13.5359, -72.0075], "poblacion":  85_000, "icu_beds":  3},
                {"nombre": "Urubamba",      "coords": [-13.3167, -72.1167], "poblacion":  25_000, "icu_beds":  0},
            ],
        },
        "boston": {
            "nombre":          "Boston, MA",
            "subtitulo":       "Zona de Cuarentena Federal — The Last of Us (Ficción, 2023)",
            "centro":          [42.3601, -71.0589],
            "zoom":            12,
            "nota":            "Zona de Cuarentena Federal establecida el Día 14 post-pandemia Cordyceps. Población civil reducida al 30%.",
            "patient_zero_zona": 0,
            "zonas": [
                {"nombre": "Downtown / QZ Central", "coords": [42.3561, -71.0589], "poblacion":  45_000, "icu_beds": 200},
                {"nombre": "South End",             "coords": [42.3388, -71.0790], "poblacion":  35_000, "icu_beds":  50},
                {"nombre": "Dorchester",            "coords": [42.3010, -71.0653], "poblacion":  95_000, "icu_beds":  30},
                {"nombre": "Roxbury",               "coords": [42.3126, -71.0968], "poblacion":  58_000, "icu_beds":  20},
                {"nombre": "East Boston",           "coords": [42.3736, -71.0317], "poblacion":  44_000, "icu_beds":  15},
                {"nombre": "Cambridge",             "coords": [42.3736, -71.1097], "poblacion": 120_000, "icu_beds":  80},
            ],
        },
        "wuhan": {
            "nombre":          "Wuhan, China",
            "subtitulo":       "COVID-19 — Brote original, diciembre 2019",
            "centro":          [30.5700, 114.3055],
            "zoom":            11,
            "nota":            "Mercado de Mariscos de Huanan — Primer cluster documentado. Diciembre 2019.",
            "patient_zero_zona": 0,
            "zonas": [
                {"nombre": "Jianghan (Mercado Huanan)", "coords": [30.5928, 114.2819], "poblacion":   680_000, "icu_beds":  800},
                {"nombre": "Wuchang",                   "coords": [30.5434, 114.3029], "poblacion": 1_200_000, "icu_beds": 1500},
                {"nombre": "Hanyang",                   "coords": [30.5551, 114.2739], "poblacion":   600_000, "icu_beds":  600},
                {"nombre": "Qingshan",                  "coords": [30.6268, 114.4104], "poblacion":   500_000, "icu_beds":  400},
                {"nombre": "Hongshan",                  "coords": [30.5596, 114.3599], "poblacion":   800_000, "icu_beds":  900},
                {"nombre": "Jiangan",                   "coords": [30.6258, 114.2884], "poblacion":   900_000, "icu_beds": 1000},
            ],
        },
        "guinea": {
            "nombre":          "Guinea, África Occidental",
            "subtitulo":       "Ébola 2014 — Brote más grande jamás registrado",
            "centro":          [9.20, -11.50],
            "zoom":            7,
            "nota":            "Guéckédou: Paciente Zero documentado dic 2013. Médicos Sin Fronteras respondió en marzo 2014.",
            "patient_zero_zona": 0,
            "zonas": [
                {"nombre": "Guéckédou (Paciente Zero)", "coords": [ 8.5580, -10.1280], "poblacion":   280_000, "icu_beds":  4},
                {"nombre": "Macenta",                   "coords": [ 8.5496,  -9.4736], "poblacion":   180_000, "icu_beds":  2},
                {"nombre": "Kissidougou",               "coords": [ 9.1857, -10.1054], "poblacion":   160_000, "icu_beds":  3},
                {"nombre": "Conakry (Capital)",         "coords": [ 9.5370, -13.6773], "poblacion": 1_900_000, "icu_beds": 50},
                {"nombre": "Nzérékoré",                 "coords": [ 7.7500,  -8.8167], "poblacion":   200_000, "icu_beds":  5},
                {"nombre": "Kindia",                    "coords": [10.0573, -12.8592], "poblacion":   120_000, "icu_beds":  3},
            ],
        },
        "bogota": {
            "nombre":    "Bogotá, Colombia",
            "subtitulo": "COVID-19 — Ola urbana 2020",
            "centro":    [4.7110, -74.0721],
            "zoom":      11,
            "nota":      "Ciudad de 7 millones de habitantes — modelo de expansión urbana densa.",
            "zonas": [
                {"nombre": "Chapinero",     "coords": [4.6486, -74.0537], "poblacion":   130_000, "icu_beds": 400},
                {"nombre": "Kennedy",       "coords": [4.6277, -74.1547], "poblacion": 1_200_000, "icu_beds": 200},
                {"nombre": "Suba",          "coords": [4.7462, -74.0782], "poblacion": 1_300_000, "icu_beds": 150},
                {"nombre": "Bosa",          "coords": [4.6195, -74.1818], "poblacion":   800_000, "icu_beds":  80},
                {"nombre": "Usaquén",       "coords": [4.7027, -74.0323], "poblacion":   500_000, "icu_beds": 600},
                {"nombre": "La Candelaria", "coords": [4.5975, -74.0761], "poblacion":    23_000, "icu_beds":  50},
            ],
        },
    }

    # ─────────────────────────────────────────────────────────────
    # HELPERS INTERNOS
    # ─────────────────────────────────────────────────────────────

    @staticmethod
    def _clasificar(tasa):
        if tasa < 0.10: return "CONTROLADA", "#27AE60"
        if tasa < 0.30: return "ALERTA",     "#F39C12"
        if tasa < 0.60: return "CRÍTICA",    "#E67E22"
        return              "PERDIDA",    "#E74C3C"

    @staticmethod
    def _radio(infectados, poblacion):
        tasa = infectados / max(poblacion, 1)
        return int(400 + 8000 * math.sqrt(min(tasa, 1.0)))

    @classmethod
    def _build_frames(cls, zonas, infectados_por_dia, poblaciones_override):
        frames, totales = [], []
        for raw_frame in infectados_por_dia:
            frame_data = []
            total = 0
            for i, zona in enumerate(zonas):
                inf = int(raw_frame[i]) if i < len(raw_frame) else 0
                pob = poblaciones_override[i] if (poblaciones_override and i < len(poblaciones_override)) else zona["poblacion"]
                tasa = inf / max(pob, 1)
                status, color = cls._clasificar(tasa)
                icu = zona.get("icu_beds", 0)
                frame_data.append({
                    "nombre":    zona["nombre"],
                    "coords":    zona["coords"],
                    "infectados": inf,
                    "poblacion":  pob,
                    "tasa":       round(tasa * 100, 1),
                    "status":     status,
                    "color":      color,
                    "radio":      cls._radio(inf, pob),
                    "icu_beds":   icu,
                    "icu_ratio":  round(inf / max(icu, 1), 1) if icu > 0 else 999,
                })
                total += inf
            frames.append(frame_data)
            totales.append(total)
        return frames, totales

    @classmethod
    def _render(cls, ciudad_key, infectados_por_dia, poblaciones, patogeno, altura, animado, dia_actual=1):
        ciudad  = cls.CIUDADES[ciudad_key]
        zonas   = ciudad["zonas"]
        pz_idx  = ciudad.get("patient_zero_zona", -1)
        frames, totales = cls._build_frames(zonas, infectados_por_dia, poblaciones)
        n_dias  = len(frames)

        uid = f"{ciudad_key}_{_uuid.uuid4().hex[:8]}"

        # Nivel de alerta final
        last = frames[-1]
        max_tasa = max(z["tasa"] for z in last) if last else 0
        al = "ROJO" if max_tasa >= 60 else "NARANJA" if max_tasa >= 30 else "AMARILLO" if max_tasa >= 10 else "VERDE"
        al_color = {"VERDE": "#27AE60", "AMARILLO": "#F1C40F", "NARANJA": "#E67E22", "ROJO": "#E74C3C"}[al]
        pulse = "pulse" if al in ("ROJO", "NARANJA") else ""

        controls = ""
        if animado and n_dias > 1:
            controls = f"""
<div class="mb-controls">
  <button id="mb-play-{uid}" class="mb-play">▶ Reproducir</button>
  <input  id="mb-slider-{uid}" class="mb-slider" type="range" min="0" max="{n_dias-1}" value="0">
  <div id="mb-day-{uid}"   class="mb-daylabel">Día 1</div>
  <div id="mb-total-{uid}" class="mb-total">🦠 calculando...</div>
</div>"""

        iife_js = _build_map_js(
            uid        = uid,
            frames_json  = json.dumps(frames),
            totales_json = json.dumps(totales),
            pz_idx     = pz_idx,
            n_dias     = n_dias,
            dia_actual = dia_actual,
            animado    = animado,
            centro     = ciudad["centro"],
            zoom       = ciudad["zoom"],
        )

        return f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
{_CSS}
</head><body>
<div class="mb-wrapper">
  <div class="mb-header" id="mb-hdr-{uid}" style="border-bottom:3px solid {al_color}">
    <div>
      <h2>🗺 {ciudad['nombre']} &nbsp;—&nbsp; {patogeno}</h2>
      <p>{ciudad['subtitulo']}</p>
    </div>
    <div style="display:flex;gap:10px;align-items:center;flex-wrap:wrap;">
      <span class="mb-tag">{len(zonas)} zonas</span>
      {'<span class="mb-tag">Día ' + str(dia_actual) + '</span>' if not animado else ''}
      <span id="mb-alert-{uid}" class="mb-badge {pulse}" style="background:{al_color}">ALERTA {al}</span>
    </div>
  </div>
  {controls}
  <div id="mb-map-{uid}" style="height:{altura}px;width:100%"></div>
  <div class="mb-nota">📌 {ciudad['nota']}</div>
</div>
{iife_js}
</body></html>"""

    # ─────────────────────────────────────────────────────────────
    # API PÚBLICA
    # ─────────────────────────────────────────────────────────────

    @classmethod
    def brote_actual(cls, ciudad, infectados, poblaciones=None, dia=1, patogeno="Desconocido", altura=560):
        """
        Mapa estático — estado del brote en un día dado.

        ciudad:      'lima' | 'cusco' | 'boston' | 'wuhan' | 'guinea' | 'bogota'
        infectados:  lista de infectados por zona  [zona0, zona1, ...]
        poblaciones: lista de poblaciones (opcional; usa datos reales si se omite)
        dia:         número de día (solo afecta el popup)
        patogeno:    nombre del patógeno para el encabezado
        """
        if ciudad not in cls.CIUDADES:
            print(f"❌ Ciudad '{ciudad}' no encontrada.\n   Opciones: {list(cls.CIUDADES.keys())}")
            return
        n = len(cls.CIUDADES[ciudad]["zonas"])
        padded = list(infectados[:n]) + [0] * (n - len(infectados))
        html = cls._render(ciudad, [padded], poblaciones, patogeno, altura, animado=False, dia_actual=dia)
        display(HTML(f'<div style="height:{altura+80}px">{html}</div>'))

    @classmethod
    def animacion_brote(cls, ciudad, infectados_por_dia, poblaciones=None, patogeno="Desconocido", altura=540):
        """
        Mapa animado con slider día a día.

        ciudad:             'lima' | 'cusco' | 'boston' | 'wuhan' | 'guinea' | 'bogota'
        infectados_por_dia: lista de listas  [[zona0_dia1, zona1_dia1,...], [día2...], ...]
        poblaciones:        lista de poblaciones por zona (opcional)
        patogeno:           nombre del patógeno
        """
        if ciudad not in cls.CIUDADES:
            print(f"❌ Ciudad '{ciudad}' no encontrada.\n   Opciones: {list(cls.CIUDADES.keys())}")
            return
        n = len(cls.CIUDADES[ciudad]["zonas"])
        frames = [list(f[:n]) + [0] * (n - len(f)) for f in infectados_por_dia]
        html = cls._render(ciudad, frames, poblaciones, patogeno, altura, animado=True)
        display(HTML(f'<div style="height:{altura+140}px">{html}</div>'))

    @classmethod
    def ciudades_disponibles(cls):
        """Muestra una tabla con las ciudades pre-cargadas."""
        rows = "".join(
            f'<tr style="background:{"#111827" if i%2==0 else "#0d1117"};color:#ECF0F1">'
            f'<td style="padding:9px;color:#3498DB;font-family:monospace">"{k}"</td>'
            f'<td style="padding:9px;font-weight:bold">{v["nombre"]}</td>'
            f'<td style="padding:9px;color:#95A5A6;font-style:italic">{v["subtitulo"]}</td>'
            f'<td style="padding:9px;text-align:center;color:#F39C12">{len(v["zonas"])}</td>'
            f'</tr>'
            for i, (k, v) in enumerate(cls.CIUDADES.items())
        )
        display(HTML(f"""
        <div style="font-family:'Segoe UI',Arial,sans-serif;background:#0d1117;
                    padding:20px;border-radius:10px;border:1px solid #2c3e50">
          <h3 style="color:#ECF0F1;margin-bottom:14px">🌎 Ciudades disponibles en MapaBrote</h3>
          <table style="width:100%;border-collapse:collapse;font-size:13px">
            <tr style="background:#1a1a2e;color:#BDC3C7">
              <th style="padding:9px;text-align:left">Clave</th>
              <th style="padding:9px;text-align:left">Ciudad</th>
              <th style="padding:9px;text-align:left">Escenario</th>
              <th style="padding:9px;text-align:center">Zonas</th>
            </tr>{rows}
          </table>
          <p style="color:#7F8C8D;font-size:11px;margin-top:12px">
            Ejemplo: mapa.brote_actual("lima", infectados, dia=7, patogeno="COVID-19")
          </p>
        </div>"""))
