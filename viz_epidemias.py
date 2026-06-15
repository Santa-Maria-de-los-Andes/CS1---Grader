# viz_epidemias.py — Visualizaciones interactivas de epidemias con Plotly
# Santa María de los Andes — Intro CS, Notebook 3
# Requiere: plotly (preinstalado en Colab), IPython

from IPython.display import display, HTML

try:
    import plotly.graph_objects as go
    _PLOTLY = True
except ImportError:
    _PLOTLY = False
    print("⚠️  plotly no encontrado — ejecuta: !pip install plotly")


# ─────────────────────────────────────────────────────────────
# PALETA TLOU — Firefly Research Terminal
# ─────────────────────────────────────────────────────────────
_COLORES = {
    "Cordyceps":       "#D4870A",   # Cordyceps Amber
    "Walker":          "#D4870A",   # Walker — misma familia
    "COVID-19":        "#39E5B6",   # Bioluminiscente
    "Ebola":           "#C0392B",   # FEDRA Red
    "Ébola":           "#C0392B",
    "Gripe 1918":      "#E67E22",   # Naranja cálido
    "Gripe Española":  "#E67E22",
    "Sarampión":       "#8FA3A8",   # Quarantine Gray
    "Peste Bubónica":  "#6D4C41",   # Tierra oscura
    "default":         "#555555",
}

# SIR — colores canónicos del tema
_SIR_S = "#8FA3A8"   # Quarantine Gray   — susceptibles
_SIR_I = "#D4870A"   # Cordyceps Amber   — infectados
_SIR_R = "#4CA66B"   # Firefly Green     — recuperados

_TLOU = dict(
    paper_bgcolor="#0D0D0D",
    plot_bgcolor="#0D0D0D",
    font=dict(color="#B8FF9A", family="Courier New, monospace"),
    xaxis=dict(gridcolor="#1C1C1C", zerolinecolor="#1C1C1C", tickfont=dict(color="#8FA3A8")),
    yaxis=dict(gridcolor="#1C1C1C", zerolinecolor="#1C1C1C", tickfont=dict(color="#8FA3A8")),
    legend=dict(bgcolor="#0D0D0D", bordercolor="#39E5B6", borderwidth=1,
                font=dict(color="#B8FF9A")),
    margin=dict(l=70, r=50, t=90, b=70),
)

_LINE_STYLES = ["solid", "dash", "dot", "dashdot"]


def _color(nombre):
    for key in _COLORES:
        if key in nombre:
            return _COLORES[key]
    return _COLORES["default"]


def _watermark(fig):
    fig.add_annotation(
        text="✦ FIREFLIES ✦",
        x=0.99, y=0.01, xref="paper", yref="paper",
        showarrow=False, opacity=0.10,
        font=dict(size=9, color="#4CA66B", family="Courier New"),
    )


def _apply_theme(fig):
    fig.update_layout(**_TLOU)
    fig.update_xaxes(gridcolor="#1C1C1C", zerolinecolor="#1C1C1C",
                     tickfont=dict(color="#8FA3A8", family="Courier New"))
    fig.update_yaxes(gridcolor="#1C1C1C", zerolinecolor="#1C1C1C",
                     tickfont=dict(color="#8FA3A8", family="Courier New"))
    _watermark(fig)


class VizEpidemias:
    """
    Visualizaciones interactivas de epidemias — tema Firefly Research Terminal.
    Todos los métodos muestran la figura en Colab Y la devuelven para personalización.

    Uso rápido:
        viz = VizEpidemias
        viz.curva_sir(S_hist, I_hist, R_hist, "COVID-19", r0=2.5)
        viz.comparar_patogenos({"COVID-19": totales_covid, "Ébola": totales_ebola})
        viz.grafico_r0(nombres, r0_valores)
        viz.grafico_cfr(nombres, mortalidad)
    """

    # ─────────────────────────────────────────────────────────────
    # 1. CURVA SIR
    # ─────────────────────────────────────────────────────────────
    @staticmethod
    def curva_sir(S_hist, I_hist, R_hist, nombre_patogeno="Patógeno", N=None, r0=None):
        """
        Curva SIR interactiva — Kermack & McKendrick (1927).

        S_hist, I_hist, R_hist : listas con el valor de cada compartimento por día
        nombre_patogeno        : nombre para el título y leyenda
        N                      : población total (si se pasa, eje Y muestra porcentaje)
        r0                     : número básico de reproducción (muestra umbral de rebaño)
        """
        if not _PLOTLY:
            print("plotly no disponible"); return

        dias = list(range(1, len(I_hist) + 1))
        pico_I   = max(I_hist)
        pico_dia = I_hist.index(pico_I) + 1
        divisor  = N if N else 1
        pct_str  = "%" if N else "personas"

        S_plot = [v / divisor * (100 if N else 1) for v in S_hist]
        I_plot = [v / divisor * (100 if N else 1) for v in I_hist]
        R_plot = [v / divisor * (100 if N else 1) for v in R_hist]
        pico_y = pico_I / divisor * (100 if N else 1)

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=dias, y=S_plot, name="SUSCEPTIBLES (S)",
            line=dict(color=_SIR_S, width=2.5),
            hovertemplate="DÍA %{x}<br>SUSCEPTIBLES: %{y:.1f}" + pct_str + "<extra></extra>",
        ))
        fig.add_trace(go.Scatter(
            x=dias, y=I_plot, name="INFECTADOS ACTIVOS (I)",
            line=dict(color=_SIR_I, width=3),
            hovertemplate="DÍA %{x}<br>INFECTADOS: %{y:.1f}" + pct_str + "<extra></extra>",
        ))
        fig.add_trace(go.Scatter(
            x=dias, y=R_plot, name="RECUPERADOS / INMUNES (R)",
            line=dict(color=_SIR_R, width=2.5),
            hovertemplate="DÍA %{x}<br>RECUPERADOS: %{y:.1f}" + pct_str + "<extra></extra>",
        ))

        # Línea de pico infeccioso
        fig.add_vline(
            x=pico_dia, line_width=1.5, line_dash="dash", line_color="#39E5B6",
            annotation_text=f"  ▶ PICO INFECCIOSO: DÍA {pico_dia}",
            annotation_position="top right",
            annotation_font=dict(color="#39E5B6", size=11, family="Courier New"),
        )

        # Umbral de inmunidad de rebaño (1 - 1/R0)
        if r0 and r0 > 1 and N:
            herd = (1 - 1 / r0) * 100
            fig.add_hline(
                y=herd, line_dash="dot", line_color="#39E5B6", line_width=1.5,
                annotation_text=f"  ⚠ UMBRAL INMUNIDAD DE REBAÑO — {herd:.0f}%",
                annotation_position="bottom right",
                annotation_font=dict(color="#39E5B6", size=11, family="Courier New"),
            )

        fig.update_layout(
            title=dict(
                text=f"[ SIMULACIÓN SIR — {nombre_patogeno.upper()} ]",
                font=dict(size=16, color="#B8FF9A", family="Courier New"),
            ),
            xaxis_title="DÍA DE SIMULACIÓN",
            yaxis_title=f"POBLACIÓN ({pct_str.upper()})",
            hovermode="x unified",
        )
        _apply_theme(fig)
        fig.show()

    # ─────────────────────────────────────────────────────────────
    # 2. COMPARAR PATÓGENOS
    # ─────────────────────────────────────────────────────────────
    @staticmethod
    def comparar_patogenos(resultados_dict, titulo="COMPARACIÓN DE PATÓGENOS"):
        """
        Curvas de propagación superpuestas para múltiples patógenos.

        resultados_dict : { "COVID-19": [100, 250, 625, ...], "Ébola": [100, 180, ...], ... }
                          Cada lista = total infectados por día.
        """
        if not _PLOTLY:
            print("plotly no disponible"); return

        n_series = len(resultados_dict)
        fig = go.Figure()

        for idx, (nombre, totales) in enumerate(resultados_dict.items()):
            dias  = list(range(1, len(totales) + 1))
            pico  = max(totales)
            pico_d = totales.index(pico) + 1
            col   = _color(nombre)
            style = _LINE_STYLES[idx % len(_LINE_STYLES)]

            # Con dos series forzamos colores distintos si son iguales
            if n_series == 2 and idx == 1:
                same_as_first = _color(list(resultados_dict.keys())[0]) == col
                if same_as_first:
                    col = "#39E5B6"   # bioluminiscente como contraste

            fig.add_trace(go.Scatter(
                x=dias, y=totales, name=nombre,
                mode="lines+markers",
                marker=dict(size=4),
                line=dict(color=col, width=2.5, dash=style),
                hovertemplate=f"{nombre}<br>DÍA %{{x}}<br>INFECTADOS: %{{y:,}}<extra></extra>",
            ))

        # Nota especial si Walker está en el conjunto
        if any("Walker" in k for k in resultados_dict):
            fig.add_annotation(
                x=0.01, y=0.05, xref="paper", yref="paper",
                text="⚠ WALKER: R₀ bajo, MODELO SIR no captura reanimación",
                showarrow=False,
                font=dict(size=9, color="#D4870A", family="Courier New"),
                align="left",
            )

        fig.update_layout(
            title=dict(
                text=f"[ {titulo.upper()} ]",
                font=dict(size=16, color="#B8FF9A", family="Courier New"),
            ),
            xaxis_title="DÍA DE SIMULACIÓN",
            yaxis_title="TOTAL INFECTADOS",
            hovermode="x unified",
        )
        _apply_theme(fig)
        fig.show()

    # ─────────────────────────────────────────────────────────────
    # 3. IMPACTO DE CUARENTENA — "vidas salvadas"
    # ─────────────────────────────────────────────────────────────
    @staticmethod
    def impacto_cuarentena(infectados_ini, poblaciones, r0, dia_cuarentena,
                           nombre_patogeno="COVID-19", cfr=2.0,
                           dias=21, reduccion_r0=0.4):
        """
        Compara sin cuarentena vs. con cuarentena — calcula ambas curvas internamente.
        Cambia dia_cuarentena para ver el impacto en tiempo real.

        infectados_ini  : lista de infectados por zona al inicio
        poblaciones     : lista de poblaciones por zona
        r0              : número básico de reproducción (sin intervención)
        dia_cuarentena  : día en que se activa la cuarentena (1-indexed)
        cfr             : tasa de mortalidad en % (ej. 2.0 para COVID-19)
        dias            : duración de la simulación
        reduccion_r0    : factor de R₀ durante cuarentena (0.4 = reducción del 60%)
        """
        if not _PLOTLY:
            print("plotly no disponible"); return

        def _simular(dia_q):
            inf    = list(infectados_ini)
            caidas = [False] * len(inf)
            totales = []
            for dia in range(1, dias + 1):
                r0_hoy = r0 * reduccion_r0 if dia >= dia_q else r0
                total  = 0
                for z in range(len(inf)):
                    if not caidas[z]:
                        tasa = inf[z] / max(poblaciones[z], 1)
                        if tasa > 0.6:
                            caidas[z] = True
                        else:
                            inf[z] = min(int(inf[z] * r0_hoy), poblaciones[z])
                    total += inf[z]
                totales.append(total)
            return totales

        dias_x  = list(range(1, dias + 1))
        s_ext   = _simular(999)                # sin cuarentena
        c_ext   = _simular(dia_cuarentena)     # con cuarentena

        casos_evitados = sum(max(s - c, 0) for s, c in zip(s_ext, c_ext))
        vidas_salvadas = int(casos_evitados * cfr / 100)   # cfr is in %

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=dias_x + dias_x[::-1],
            y=s_ext + c_ext[::-1],
            fill="toself", fillcolor="rgba(192,57,43,0.12)",
            line=dict(color="rgba(0,0,0,0)"),
            name=f"CASOS EVITADOS  {casos_evitados:,}",
            hoverinfo="skip",
        ))
        fig.add_trace(go.Scatter(
            x=dias_x, y=s_ext, name="SIN CUARENTENA",
            line=dict(color="#C0392B", width=2.5),
            hovertemplate="DÍA %{x}<br>SIN CUARENTENA: %{y:,}<extra></extra>",
        ))
        fig.add_trace(go.Scatter(
            x=dias_x, y=c_ext, name=f"CUARENTENA DÍA {dia_cuarentena}",
            line=dict(color="#4CA66B", width=2.5),
            hovertemplate="DÍA %{x}<br>CON CUARENTENA: %{y:,}<extra></extra>",
        ))

        fig.add_vline(
            x=dia_cuarentena, line_width=1.5, line_dash="dash", line_color="#D4870A",
            annotation_text=f"  ⚠ DÍA {dia_cuarentena}",
            annotation_font=dict(color="#D4870A", size=11, family="Courier New"),
        )

        fig.add_annotation(
            x=0.97, y=0.96, xref="paper", yref="paper",
            text=(f"▶ VIDAS SALVADAS EST.<br>"
                  f"<span style='font-size:18px;color:#4CA66B'><b>{vidas_salvadas:,}</b></span><br>"
                  f"<span style='font-size:10px'>CFR {cfr:.1f}% · {casos_evitados:,} casos evitados</span>"),
            showarrow=False, align="right",
            font=dict(size=11, color="#B8FF9A", family="Courier New"),
            bgcolor="#0D0D0D", bordercolor="#4CA66B", borderwidth=1,
            borderpad=10,
        )

        fig.update_layout(
            title=dict(
                text=f"[ CUARENTENA DÍA {dia_cuarentena} — {nombre_patogeno.upper()} ]",
                font=dict(size=15, color="#B8FF9A", family="Courier New"),
            ),
            xaxis_title="DÍA DE SIMULACIÓN",
            yaxis_title="TOTAL INFECTADOS",
            hovermode="x unified",
        )
        _apply_theme(fig)
        fig.show()

    # ─────────────────────────────────────────────────────────────
    # 4. PROPAGACIÓN MULTI-ZONA (series de tiempo)
    # ─────────────────────────────────────────────────────────────
    @staticmethod
    def curva_propagacion(infectados_por_dia, labels=None, r0=None, patogeno=""):
        """
        Una línea por zona + línea total de ciudad.

        infectados_por_dia : lista de listas  [[z0_d1, z1_d1,...], [z0_d2,...], ...]
        labels             : nombres de zonas (opcional)
        r0                 : valor R0 para el subtítulo
        patogeno           : nombre del patógeno
        """
        if not _PLOTLY:
            print("plotly no disponible"); return

        n_dias  = len(infectados_por_dia)
        n_zonas = max(len(f) for f in infectados_por_dia)
        dias    = list(range(1, n_dias + 1))

        if not labels:
            labels = [f"ZONA {i+1}" for i in range(n_zonas)]

        zona_colors = ["#39E5B6", "#D4870A", "#4CA66B", "#8FA3A8",
                       "#C0392B", "#E67E22", "#6D4C41"]

        fig = go.Figure()

        for z in range(n_zonas):
            vals = [int(infectados_por_dia[d][z]) if z < len(infectados_por_dia[d]) else 0
                    for d in range(n_dias)]
            lbl  = labels[z].upper() if z < len(labels) else f"ZONA {z+1}"
            fig.add_trace(go.Scatter(
                x=dias, y=vals, name=lbl,
                line=dict(color=zona_colors[z % len(zona_colors)], width=2),
                hovertemplate=f"{lbl}<br>DÍA %{{x}}: %{{y:,}}<extra></extra>",
            ))

        # Total ciudad — línea prominente
        totales = [sum(infectados_por_dia[d]) for d in range(n_dias)]
        fig.add_trace(go.Scatter(
            x=dias, y=totales, name="▶ TOTAL CIUDAD",
            line=dict(color="#B8FF9A", width=3.5, dash="dot"),
            hovertemplate="TOTAL<br>DÍA %{x}: %{y:,}<extra></extra>",
        ))

        r0_str = f" | R₀ = {r0}" if r0 else ""
        fig.update_layout(
            title=dict(
                text=f"[ PROPAGACIÓN POR ZONA — {patogeno.upper()}{r0_str} ]",
                font=dict(size=16, color="#B8FF9A", family="Courier New"),
            ),
            xaxis_title="DÍA DE SIMULACIÓN",
            yaxis_title="INFECTADOS",
            hovermode="x unified",
        )
        _apply_theme(fig)
        fig.show()

    # ─────────────────────────────────────────────────────────────
    # 5. SEMÁFORO DE ZONAS — tablero de estado tipo terminal
    # ─────────────────────────────────────────────────────────────
    @staticmethod
    def semaforo_ciudad(zonas_nombres, infectados, poblaciones, dia=1, patogeno=""):
        """
        Tablero HTML de estado por zona — estilo terminal Firefly.

        zonas_nombres : lista de nombres de zonas
        infectados    : lista de infectados por zona
        poblaciones   : lista de poblaciones por zona
        dia           : día actual de la simulación
        patogeno      : nombre del patógeno
        """
        STATUS = [
            (0.10, "CONTENIDO",   "#4CA66B", "#001208", "La llama se apaga."),
            (0.30, "VIGILANCIA",  "#D4870A", "#1a0e00", "Monitorear. No correr. Aún."),
            (0.60, "CRÍTICA",     "#C0392B", "#1a0000", "Evacuación de Zona. Protocolo FEDRA activado."),
            (1.01, "PERDIDA",     "#C0392B", "#0d0000", "No hay protocolo para esto."),
        ]

        def clasif(tasa):
            for umbral, label, color, bg, msg in STATUS:
                if tasa < umbral:
                    return label, color, bg, msg
            return STATUS[-1][1], STATUS[-1][2], STATUS[-1][3], STATUS[-1][4]

        n = min(len(zonas_nombres), len(infectados), len(poblaciones))
        cards = ""
        total_inf = 0
        for i in range(n):
            inf  = int(infectados[i])
            pob  = int(poblaciones[i])
            tasa = inf / max(pob, 1)
            total_inf += inf
            label, color, bg, msg = clasif(tasa)
            pct   = tasa * 100
            bar_w = min(pct, 100)

            cards += f"""
            <div style="background:#0D0D0D;border:1px solid {color};border-radius:6px;
                        padding:16px;min-width:175px;flex:1;max-width:260px;
                        font-family:'Courier New',monospace">
              <div style="color:#8FA3A8;font-size:11px;letter-spacing:2px;margin-bottom:6px">
                {zonas_nombres[i].upper()}</div>
              <div style="color:{color};font-size:26px;font-weight:bold;margin-bottom:4px">
                {inf:,}</div>
              <div style="color:#555;font-size:11px;margin-bottom:8px">
                DE {pob:,} HAB. ({pct:.1f}%)</div>
              <div style="background:#111;border-radius:2px;height:4px;margin-bottom:10px">
                <div style="background:{color};width:{bar_w:.1f}%;height:4px;border-radius:2px"></div>
              </div>
              <div style="color:{color};font-size:11px;letter-spacing:1px;margin-bottom:4px;
                          font-weight:bold">[ {label} ]</div>
              <div style="color:#555;font-size:10px;font-style:italic">{msg}</div>
            </div>"""

        total_pob   = sum(int(poblaciones[i]) for i in range(n))
        tasa_global = total_inf / max(total_pob, 1) * 100

        html = f"""
        <div style="font-family:'Courier New',monospace;background:#0D0D0D;
                    padding:20px;border-radius:8px;border:1px solid #39E5B6">
          <div style="display:flex;justify-content:space-between;align-items:center;
                      margin-bottom:16px;flex-wrap:wrap;gap:10px">
            <div>
              <div style="color:#39E5B6;font-size:11px;letter-spacing:3px;margin-bottom:4px">
                ✦ FIREFLY RESEARCH NODE 7 — ESTADO DE ZONAS</div>
              <h3 style="color:#B8FF9A;margin:0 0 4px 0;font-size:15px">
                [ {patogeno.upper()} ]</h3>
              <p style="color:#555;font-size:11px;margin:0;letter-spacing:1px">
                DÍA {dia} DE SIMULACIÓN</p>
            </div>
            <div style="text-align:right">
              <div style="color:#B8FF9A;font-size:22px;font-weight:bold">{total_inf:,}</div>
              <div style="color:#555;font-size:11px">INFECTADOS TOTALES ({tasa_global:.1f}% CIUDAD)</div>
            </div>
          </div>
          <div style="display:flex;flex-wrap:wrap;gap:12px">
            {cards}
          </div>
          <div style="margin-top:14px;padding-top:12px;border-top:1px solid #1C1C1C;
                      display:flex;gap:14px;flex-wrap:wrap">
            <span style="font-size:10px;color:#39E5B6;letter-spacing:1px">UMBRALES:</span>
            <span style="font-size:10px;color:#4CA66B">● &lt;10% CONTENIDO</span>
            <span style="font-size:10px;color:#D4870A">● 10–30% VIGILANCIA</span>
            <span style="font-size:10px;color:#C0392B">● 30–60% CRÍTICA</span>
            <span style="font-size:10px;color:#C0392B">● &gt;60% PERDIDA</span>
          </div>
        </div>"""
        display(HTML(html))

    # ─────────────────────────────────────────────────────────────
    # 6. GRÁFICO R0 — transmisibilidad comparada (barras horizontales)
    # ─────────────────────────────────────────────────────────────
    @staticmethod
    def grafico_r0(nombres, r0_valores):
        """
        Barras horizontales de R₀ por patógeno — estándar WHO/CDC.

        nombres    : lista de nombres de patógenos
        r0_valores : lista de valores R₀ correspondientes

        Esta es la visualización correcta para comparar transmisibilidad:
        las curvas de tiempo son incorrectas para comparar categorías.
        """
        if not _PLOTLY:
            print("plotly no disponible"); return

        # Ordenar ascendente por R0
        pares = sorted(zip(r0_valores, nombres), key=lambda x: x[0])
        r0s   = [p[0] for p in pares]
        noms  = [p[1] for p in pares]

        # Color por umbral
        def tier_color(r):
            if r < 1:   return "#4CA66B"   # CONTENIDO — Firefly Green
            if r <= 2:  return "#D4870A"   # MODERADO  — Cordyceps Amber
            if r <= 5:  return "#C0392B"   # ALTO      — FEDRA Red
            return "#C0392B"               # EXTREMO   — FEDRA Red (anotación especial)

        bar_colors = [tier_color(r) for r in r0s]

        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=r0s,
            y=[n.upper() for n in noms],
            orientation="h",
            marker=dict(color=bar_colors, line=dict(width=0)),
            hovertemplate="%{y}<br>R₀ = %{x}<extra></extra>",
        ))

        # Línea umbral de extinción en R0 = 1
        fig.add_vline(
            x=1, line_dash="dot", line_color="#4CA66B", line_width=1.5,
            annotation_text="  ⚠ UMBRAL DE EXTINCIÓN (R₀ = 1)",
            annotation_position="top",
            annotation_font=dict(color="#4CA66B", size=10, family="Courier New"),
        )

        # Una sola anotación por barra — combina R₀ + nota especial
        max_r = max(r0s)
        for r, n in zip(r0s, noms):
            is_walker   = "Walker" in n or "walker" in n
            is_extreme  = r >= 10

            if is_walker:
                label = f"  R₀ = {r}  ⚠ REANIMACIÓN"
                col   = "#D4870A"
            elif is_extreme:
                label = f"  R₀ = {r}  — UNA AULA SIN VACUNAR"
                col   = "#C0392B"
            else:
                label = f"  R₀ = {r}"
                col   = "#B8FF9A"

            fig.add_annotation(
                x=r, y=n.upper(),
                text=label,
                showarrow=False,
                font=dict(size=10, color=col, family="Courier New"),
                xanchor="left",
                yanchor="middle",
            )

        fig.update_layout(
            title=dict(
                text="[ TRANSMISIBILIDAD COMPARADA — R₀ POR PATÓGENO ]",
                font=dict(size=15, color="#B8FF9A", family="Courier New"),
            ),
            xaxis_title="NÚMERO BÁSICO DE REPRODUCCIÓN (R₀)",
            yaxis_title="",
            showlegend=False,
            height=320 + len(noms) * 28,
        )
        _apply_theme(fig)
        fig.update_xaxes(range=[0, max_r * 1.35])
        fig.show()

    # ─────────────────────────────────────────────────────────────
    # 7. GRÁFICO CFR — tasa de mortalidad por caso
    # ─────────────────────────────────────────────────────────────
    @staticmethod
    def grafico_cfr(nombres, mortalidad):
        """
        Barras horizontales de CFR por patógeno.

        nombres    : lista de nombres de patógenos
        mortalidad : lista de CFR en escala 0–1 (ej. 0.65 = 65%)

        CFR = muertes confirmadas / casos confirmados.
        Esta cifra determina la agresividad del protocolo de triage.
        """
        if not _PLOTLY:
            print("plotly no disponible"); return

        # Ordenar descendente por CFR (más letal arriba)
        cfr_pct = [m * 100 for m in mortalidad]
        pares   = sorted(zip(cfr_pct, nombres), key=lambda x: x[0], reverse=True)
        cfrs    = [p[0] for p in pares]
        noms    = [p[1] for p in pares]

        def tier_color(c):
            if c < 1:   return "#8FA3A8"   # Quarantine Gray — bajo
            if c <= 10: return "#D4870A"   # Amber — moderado
            return "#C0392B"               # FEDRA Red — alto

        bar_colors = [tier_color(c) for c in cfrs]

        # Buscar CFR de COVID-19 para línea de referencia
        covid_cfr = None
        for c, n in zip(cfrs, noms):
            if "COVID" in n:
                covid_cfr = c
                break

        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=cfrs,
            y=[n.upper() for n in noms],
            orientation="h",
            marker=dict(color=bar_colors, line=dict(width=0)),
            hovertemplate="%{y}<br>CFR = %{x:.1f}%<extra></extra>",
        ))

        # Línea de referencia COVID-19
        if covid_cfr is not None:
            fig.add_vline(
                x=covid_cfr, line_dash="dot", line_color="#39E5B6", line_width=1.5,
                annotation_text=f"  REFERENCIA COVID-19 ({covid_cfr:.1f}%)",
                annotation_position="top",
                annotation_font=dict(color="#39E5B6", size=10, family="Courier New"),
            )

        # Una sola anotación por barra — combina CFR% + nota especial
        max_c = max(cfrs)
        for c, n in zip(cfrs, noms):
            is_walker = "Walker" in n

            if is_walker:
                label = f"  {c:.0f}%  — EL CORDYCEPS NO PERDONA"
                col   = "#D4870A"
            elif c >= 50:
                label = f"  {c:.0f}%"
                col   = "#C0392B"
            else:
                label = f"  {c:.1f}%"
                col   = "#B8FF9A"

            fig.add_annotation(
                x=c, y=n.upper(),
                text=label,
                showarrow=False,
                font=dict(size=10, color=col, family="Courier New"),
                xanchor="left",
                yanchor="middle",
            )

        fig.update_layout(
            title=dict(
                text="[ TASA DE MORTALIDAD POR CASO — CFR GLOBAL ]",
                font=dict(size=15, color="#B8FF9A", family="Courier New"),
            ),
            xaxis_title="CFR (%) — MUERTES CONFIRMADAS / CASOS CONFIRMADOS",
            yaxis_title="",
            showlegend=False,
            height=320 + len(noms) * 28,
        )
        _apply_theme(fig)
        fig.update_xaxes(range=[0, max_c * 1.35])
        fig.show()

    # ─────────────────────────────────────────────────────────────
    # 7. SLIDER INTERACTIVO R₀
    # ─────────────────────────────────────────────────────────────
    @staticmethod
    def curva_r0_interactiva(N=10_000, dias=180, gamma=1/14):
        """
        Slider R₀ interactivo: arrastra de 0.5 a 5.0 y observa cómo evoluciona
        la epidemia (S, I, R) y el umbral de inmunidad de rebaño.

        N     : tamaño de la población simulada
        dias  : duración de la simulación en días
        gamma : tasa de recuperación diaria (default 1/14 — período infeccioso de 14 días)
        """
        if not _PLOTLY:
            print("plotly no disponible"); return

        r0_vals = [round(v * 0.5, 1) for v in range(1, 11)]   # 0.5 → 5.0
        dias_x  = list(range(1, dias + 1))

        def _sim(r0):
            beta = r0 * gamma
            S, I, R = float(N - 1), 1.0, 0.0
            Sl, Il, Rl = [], [], []
            for _ in range(dias):
                dS = beta * S * I / N
                dR = gamma * I
                S  = max(0.0, S - dS)
                I  = max(0.0, I + dS - dR)
                R  = min(float(N), R + dR)
                Sl.append(S / N * 100)
                Il.append(I / N * 100)
                Rl.append(R / N * 100)
            return Sl, Il, Rl

        def _herd(r0):
            return max(0.0, (1 - 1 / r0) * 100) if r0 > 1 else 0.0

        def _title(r0):
            h = _herd(r0)
            suffix = f"UMBRAL REBAÑO: {h:.0f}%" if r0 > 1 else "R₀ ≤ 1 — EPIDEMIA EN EXTINCIÓN"
            return f"[ SIMULACIÓN SIR — R₀ = {r0:.1f} | {suffix} ]"

        init_idx   = r0_vals.index(2.5)
        S0, I0, R0 = _sim(r0_vals[init_idx])
        h0         = _herd(r0_vals[init_idx])

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=dias_x, y=S0, name="SUSCEPTIBLES",
            mode="lines", line=dict(color=_SIR_S, width=2.5)))
        fig.add_trace(go.Scatter(x=dias_x, y=I0, name="INFECTADOS ACTIVOS",
            mode="lines", line=dict(color=_SIR_I, width=2.5)))
        fig.add_trace(go.Scatter(x=dias_x, y=R0, name="RECUPERADOS",
            mode="lines", line=dict(color=_SIR_R, width=2.5)))
        fig.add_trace(go.Scatter(
            x=[1, dias], y=[h0, h0],
            name="UMBRAL INMUNIDAD DE REBAÑO",
            mode="lines",
            line=dict(color="#39E5B6", width=1.5, dash="dot"),
        ))

        def _yrange(Il, Rl, h):
            # Focus scale on the epidemic activity (I + R), not on S.
            # S clips at the top for low R₀ — that's intentional and readable.
            peak = max(max(Il), max(Rl), h, 3.0)   # minimum 3% so axis isn't microscopic
            return [0, min(peak * 1.20, 105)]        # cap at 105 so we never exceed 100%

        frames = []
        for r0 in r0_vals:
            Sl, Il, Rl = _sim(r0)
            h = _herd(r0)
            yr = _yrange(Il, Rl, h)
            frames.append(go.Frame(
                data=[
                    go.Scatter(y=Sl),
                    go.Scatter(y=Il),
                    go.Scatter(y=Rl),
                    go.Scatter(y=[h, h]),
                ],
                layout=go.Layout(
                    title=dict(
                        text=_title(r0),
                        font=dict(size=14, color="#B8FF9A", family="Courier New"),
                    ),
                    yaxis=dict(
                        range=yr,
                        gridcolor="#1C1C1C", zerolinecolor="#1C1C1C",
                        tickfont=dict(color="#8FA3A8", family="Courier New"),
                    ),
                ),
                name=str(r0),
            ))
        fig.frames = frames

        steps = [dict(
            method="animate",
            args=[[str(r0)], dict(mode="immediate",
                frame=dict(duration=0, redraw=True),
                transition=dict(duration=0))],
            label=f"{r0:.1f}",
        ) for r0 in r0_vals]

        init_yr = _yrange(I0, R0, h0)
        fig.update_layout(
            title=dict(text=_title(r0_vals[init_idx]),
                       font=dict(size=14, color="#B8FF9A", family="Courier New")),
            xaxis_title="DÍA DE SIMULACIÓN",
            yaxis_title="% POBLACIÓN",
            yaxis=dict(range=init_yr),
            height=520,
            sliders=[dict(
                active=init_idx,
                currentvalue=dict(prefix="R₀ = ",
                    font=dict(color="#B8FF9A", family="Courier New", size=14)),
                steps=steps,
                bgcolor="#111111",
                bordercolor="#39E5B6",
                font=dict(color="#8FA3A8", family="Courier New"),
                pad=dict(t=12, b=10),
                x=0, len=1,
            )],
            updatemenus=[],
        )
        _apply_theme(fig)
        fig.show()
