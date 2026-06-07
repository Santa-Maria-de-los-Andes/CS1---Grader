# viz_epidemias.py — Visualizaciones interactivas de epidemias con Plotly
# Santa María de los Andes — Intro CS, Notebook 3
# Requiere: plotly (preinstalado en Colab), IPython

from IPython.display import display, HTML

try:
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    import plotly.io as pio
    _PLOTLY = True
except ImportError:
    _PLOTLY = False
    print("⚠️  plotly no encontrado — ejecuta: !pip install plotly")


# ─────────────────────────────────────────────────────────────
# COLORES POR PATÓGENO
# ─────────────────────────────────────────────────────────────
_COLORES = {
    "Cordyceps":       "#E74C3C",
    "Walker":          "#922B21",
    "COVID-19":        "#3498DB",
    "Ebola":           "#8E44AD",
    "Ébola":           "#8E44AD",
    "Gripe 1918":      "#E67E22",
    "Gripe Española":  "#E67E22",
    "Sarampión":       "#F1C40F",
    "Peste Bubónica":  "#795548",
    "default":         "#95A5A6",
}

_DARK = dict(
    paper_bgcolor="#0d1117",
    plot_bgcolor="#111827",
    font=dict(color="#ECF0F1", family="Segoe UI, Arial"),
    xaxis=dict(gridcolor="#2c3e50", zerolinecolor="#2c3e50"),
    yaxis=dict(gridcolor="#2c3e50", zerolinecolor="#2c3e50"),
    legend=dict(bgcolor="#1a1a2e", bordercolor="#2c3e50", borderwidth=1),
    margin=dict(l=60, r=30, t=70, b=60),
)

def _color(nombre):
    for key in _COLORES:
        if key in nombre:
            return _COLORES[key]
    return _COLORES["default"]


class VizEpidemias:
    """
    Visualizaciones interactivas de epidemias.
    Todos los métodos muestran la figura en Colab Y la devuelven para personalización.

    Uso rápido:
        viz = VizEpidemias
        viz.curva_sir(S_hist, I_hist, R_hist, "COVID-19")
        viz.comparar_patogenos({"COVID-19": totales_covid, "Ébola": totales_ebola})
    """

    # ─────────────────────────────────────────────────────────────
    # 1. CURVA SIR
    # ─────────────────────────────────────────────────────────────
    @staticmethod
    def curva_sir(S_hist, I_hist, R_hist, nombre_patogeno="Patógeno", N=None):
        """
        Curva SIR interactiva — la misma publicada por Ferguson et al. (Imperial College, 2020).

        S_hist, I_hist, R_hist : listas con el valor de cada compartimento por día
        nombre_patogeno        : nombre para el título y leyenda
        N                      : población total (si se pasa, eje Y muestra porcentaje)
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
        fig.add_trace(go.Scatter(x=dias, y=S_plot, name="Susceptibles (S)",
            line=dict(color="#3498DB", width=2.5),
            hovertemplate="Día %{x}<br>Susceptibles: %{y:.1f}" + pct_str + "<extra></extra>"))
        fig.add_trace(go.Scatter(x=dias, y=I_plot, name="Infectados activos (I)",
            line=dict(color="#E74C3C", width=3),
            fill="tozeroy", fillcolor="rgba(231,76,60,0.12)",
            hovertemplate="Día %{x}<br>Infectados: %{y:.1f}" + pct_str + "<extra></extra>"))
        fig.add_trace(go.Scatter(x=dias, y=R_plot, name="Recuperados / Inmunes (R)",
            line=dict(color="#27AE60", width=2.5),
            hovertemplate="Día %{x}<br>Recuperados: %{y:.1f}" + pct_str + "<extra></extra>"))

        # Línea de pico
        fig.add_vline(x=pico_dia, line_width=1.5, line_dash="dash", line_color="#F39C12",
                      annotation_text=f"  Pico: Día {pico_dia}",
                      annotation_position="top right",
                      annotation_font=dict(color="#F39C12", size=12))

        fig.update_layout(
            title=dict(text=f"📈 Modelo SIR — {nombre_patogeno}", font=dict(size=17, color="#ECF0F1")),
            xaxis_title="Días desde el primer caso",
            yaxis_title=f"Población ({pct_str})",
            hovermode="x unified",
            **_DARK,
        )
        fig.show()
        return fig

    # ─────────────────────────────────────────────────────────────
    # 2. COMPARAR PATÓGENOS
    # ─────────────────────────────────────────────────────────────
    @staticmethod
    def comparar_patogenos(resultados_dict, titulo="Comparación de patógenos"):
        """
        Curvas de propagación superpuestas para múltiples patógenos.

        resultados_dict : { "COVID-19": [100, 250, 625, ...], "Ébola": [100, 180, ...], ... }
                          Cada lista = total infectados por día.
        """
        if not _PLOTLY:
            print("plotly no disponible"); return

        fig = go.Figure()
        for nombre, totales in resultados_dict.items():
            dias = list(range(1, len(totales) + 1))
            pico = max(totales)
            pico_d = totales.index(pico) + 1
            fig.add_trace(go.Scatter(
                x=dias, y=totales, name=nombre,
                line=dict(color=_color(nombre), width=2.5),
                hovertemplate=f"{nombre}<br>Día %{{x}}<br>Infectados: %{{y:,}}<extra></extra>",
            ))
            fig.add_annotation(
                x=pico_d, y=pico,
                text=f"  {nombre}<br>  Pico: {pico:,}",
                showarrow=False, font=dict(size=10, color=_color(nombre)),
                xanchor="left",
            )

        fig.update_layout(
            title=dict(text=f"🦠 {titulo}", font=dict(size=17, color="#ECF0F1")),
            xaxis_title="Días",
            yaxis_title="Total infectados",
            hovermode="x unified",
            **_DARK,
        )
        fig.show()
        return fig

    # ─────────────────────────────────────────────────────────────
    # 3. IMPACTO DE CUARENTENA — "vidas salvadas"
    # ─────────────────────────────────────────────────────────────
    @staticmethod
    def impacto_cuarentena(sin_intervencion, con_intervencion, dia_cuarentena,
                           nombre_patogeno="COVID-19", cfr=0.02):
        """
        Dos curvas superpuestas + área "vidas salvadas" sombreada.

        sin_intervencion : lista de infectados/día sin cuarentena
        con_intervencion : lista de infectados/día con cuarentena
        dia_cuarentena   : día en que se implementó la cuarentena
        cfr              : tasa de mortalidad (para calcular vidas salvadas)
        """
        if not _PLOTLY:
            print("plotly no disponible"); return

        n    = max(len(sin_intervencion), len(con_intervencion))
        dias = list(range(1, n + 1))

        # Extender la más corta al mismo largo
        def pad(lst): return lst + [lst[-1]] * (n - len(lst))
        s_ext = pad(list(sin_intervencion))
        c_ext = pad(list(con_intervencion))

        casos_evitados = sum(max(s - c, 0) for s, c in zip(s_ext, c_ext))
        vidas_salvadas = int(casos_evitados * cfr)

        fig = go.Figure()

        # Área sombreada entre curvas (casos evitados)
        fig.add_trace(go.Scatter(
            x=dias + dias[::-1],
            y=s_ext + c_ext[::-1],
            fill="toself",
            fillcolor="rgba(231,76,60,0.18)",
            line=dict(color="rgba(0,0,0,0)"),
            name=f"Casos evitados (~{casos_evitados:,})",
            hoverinfo="skip",
        ))

        fig.add_trace(go.Scatter(
            x=dias, y=s_ext, name="Sin cuarentena",
            line=dict(color="#E74C3C", width=3),
            hovertemplate="Día %{x}<br>Sin cuarentena: %{y:,}<extra></extra>"))
        fig.add_trace(go.Scatter(
            x=dias, y=c_ext, name=f"Cuarentena día {dia_cuarentena}",
            line=dict(color="#27AE60", width=3),
            hovertemplate="Día %{x}<br>Con cuarentena: %{y:,}<extra></extra>"))

        # Línea vertical del día de cuarentena
        fig.add_vline(x=dia_cuarentena, line_width=2, line_dash="dash", line_color="#F39C12",
                      annotation_text=f"  🔒 Cuarentena Día {dia_cuarentena}",
                      annotation_font=dict(color="#F39C12", size=12))

        # Anotación de vidas salvadas
        fig.add_annotation(
            x=n * 0.55, y=max(s_ext) * 0.85,
            text=f"<b>❤️ Vidas salvadas estimadas</b><br><span style='font-size:22px'>{vidas_salvadas:,}</span><br>(CFR = {cfr*100:.1f}%)",
            showarrow=False, align="center",
            font=dict(size=13, color="#ECF0F1"),
            bgcolor="#1a1a2e", bordercolor="#27AE60", borderwidth=2,
            borderpad=10,
        )

        fig.update_layout(
            title=dict(text=f"🔒 Impacto de la Cuarentena — {nombre_patogeno}", font=dict(size=17, color="#ECF0F1")),
            xaxis_title="Días",
            yaxis_title="Total infectados",
            hovermode="x unified",
            **_DARK,
        )
        fig.show()
        return fig

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
            labels = [f"Zona {i+1}" for i in range(n_zonas)]

        zona_colors = ["#3498DB","#E74C3C","#27AE60","#F39C12","#8E44AD","#16A085","#D35400"]

        fig = go.Figure()

        # Una línea por zona
        for z in range(n_zonas):
            vals = [int(infectados_por_dia[d][z]) if z < len(infectados_por_dia[d]) else 0
                    for d in range(n_dias)]
            fig.add_trace(go.Scatter(
                x=dias, y=vals,
                name=labels[z] if z < len(labels) else f"Zona {z+1}",
                line=dict(color=zona_colors[z % len(zona_colors)], width=2),
                hovertemplate=f"{labels[z] if z < len(labels) else 'Zona'}<br>Día %{{x}}: %{{y:,}}<extra></extra>",
            ))

        # Total ciudad (línea gruesa)
        totales = [sum(infectados_por_dia[d]) for d in range(n_dias)]
        fig.add_trace(go.Scatter(
            x=dias, y=totales, name="TOTAL ciudad",
            line=dict(color="#ECF0F1", width=3.5, dash="dot"),
            hovertemplate="TOTAL<br>Día %{x}: %{y:,}<extra></extra>",
        ))

        r0_str = f" | R₀ = {r0}" if r0 else ""
        fig.update_layout(
            title=dict(text=f"📊 Propagación por zonas — {patogeno}{r0_str}", font=dict(size=17, color="#ECF0F1")),
            xaxis_title="Días",
            yaxis_title="Infectados",
            hovermode="x unified",
            **_DARK,
        )
        fig.show()
        return fig

    # ─────────────────────────────────────────────────────────────
    # 5. SEMÁFORO DE ZONAS — tablero de estado tipo hospital
    # ─────────────────────────────────────────────────────────────
    @staticmethod
    def semaforo_ciudad(zonas_nombres, infectados, poblaciones, dia=1, patogeno=""):
        """
        Tablero HTML de estado por zona — estilo sala de emergencias.

        zonas_nombres : lista de nombres de zonas
        infectados    : lista de infectados por zona
        poblaciones   : lista de poblaciones por zona
        dia           : día actual de la simulación
        patogeno      : nombre del patógeno
        """
        STATUS = [
            (0.10, "CONTROLADA", "#27AE60", "#1a4a2e"),
            (0.30, "ALERTA",     "#F39C12", "#4a3500"),
            (0.60, "CRÍTICA",    "#E67E22", "#4a2800"),
            (1.01, "PERDIDA",    "#E74C3C", "#4a1010"),
        ]

        def clasif(tasa):
            for umbral, label, color, bg in STATUS:
                if tasa < umbral:
                    return label, color, bg
            return "PERDIDA", "#E74C3C", "#4a1010"

        n = min(len(zonas_nombres), len(infectados), len(poblaciones))
        cards = ""
        total_inf = 0
        for i in range(n):
            inf = int(infectados[i])
            pob = int(poblaciones[i])
            tasa = inf / max(pob, 1)
            total_inf += inf
            label, color, bg = clasif(tasa)
            pct = tasa * 100
            bar_w = min(pct, 100)

            cards += f"""
            <div style="background:#111827;border:1px solid {color};border-radius:10px;
                        padding:16px;min-width:170px;flex:1;max-width:260px">
              <div style="color:#BDC3C7;font-size:12px;margin-bottom:6px">{zonas_nombres[i]}</div>
              <div style="color:{color};font-size:26px;font-weight:bold;margin-bottom:4px">{inf:,}</div>
              <div style="color:#7F8C8D;font-size:11px;margin-bottom:8px">de {pob:,} hab. ({pct:.1f}%)</div>
              <div style="background:#1a1a2e;border-radius:4px;height:6px;margin-bottom:10px">
                <div style="background:{color};width:{bar_w:.1f}%;height:6px;border-radius:4px;
                            transition:width .4s ease"></div>
              </div>
              <span style="background:{bg};color:{color};border:1px solid {color};
                           padding:3px 10px;border-radius:4px;font-size:11px;font-weight:bold">
                {label}
              </span>
            </div>"""

        total_pob = sum(int(poblaciones[i]) for i in range(n))
        tasa_global = total_inf / max(total_pob, 1) * 100

        html = f"""
        <div style="font-family:'Segoe UI',Arial,sans-serif;background:#0d1117;
                    padding:20px;border-radius:12px;border:1px solid #2c3e50">
          <div style="display:flex;justify-content:space-between;align-items:center;
                      margin-bottom:16px;flex-wrap:wrap;gap:10px">
            <div>
              <h3 style="color:#ECF0F1;margin:0 0 4px 0">🚦 Estado por Zonas — {patogeno}</h3>
              <p style="color:#7F8C8D;font-size:12px;margin:0">Día {dia} de simulación</p>
            </div>
            <div style="text-align:right">
              <div style="color:#ECF0F1;font-size:22px;font-weight:bold">{total_inf:,}</div>
              <div style="color:#7F8C8D;font-size:11px">infectados totales ({tasa_global:.1f}% ciudad)</div>
            </div>
          </div>
          <div style="display:flex;flex-wrap:wrap;gap:12px">
            {cards}
          </div>
          <div style="margin-top:14px;display:flex;gap:10px;flex-wrap:wrap">
            <span style="font-size:11px;color:#95A5A6">Umbrales: </span>
            <span style="font-size:11px;color:#27AE60">● &lt;10% Controlada</span>
            <span style="font-size:11px;color:#F39C12">● 10–30% Alerta</span>
            <span style="font-size:11px;color:#E67E22">● 30–60% Crítica</span>
            <span style="font-size:11px;color:#E74C3C">● &gt;60% Perdida</span>
          </div>
        </div>"""
        display(HTML(html))
