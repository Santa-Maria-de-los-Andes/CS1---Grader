# NB3 Epidemias — The Last of Us Theme Reference

## Concept
The notebook is a **Firefly Research Terminal**. Students are **Firefly field analysts** feeding outbreak data into the SIR model to find a cure. Every pathogen simulated is compared to the Walker Virus — the one that broke the world.

---

## Color Palette

| Role | Name | Hex |
|---|---|---|
| Infected / Danger | Cordyceps Amber | `#D4870A` |
| Susceptible / Population | Quarantine Gray | `#8FA3A8` |
| Recovered / Hope | Firefly Green | `#4CA66B` |
| Background | Dead City Black | `#0D0D0D` |
| Terminal Text | Phosphor | `#B8FF9A` |
| Alert / Error | FEDRA Red | `#C0392B` |
| Accent | Bioluminescent | `#39E5B6` |

---

## Voice & Typography

- Plot titles: ALL CAPS, sparse, mission-report style — `"PROPAGACIÓN: SEMANAS 0–40"`
- Axis labels: field-report clipped — `"HUÉSPEDES SUSCEPTIBLES"`, `"INFECTADOS ACTIVOS"`
- Annotations: Firefly data stamps — `▶ PICO INFECCIOSO: DÍA 14`, `⚠ R0 > 2.5 — CUARENTENA`
- Flavor text: written as Marlene's field journal or Ellie's margin notes

---

## Levels (6 tiers by % of core score)

```python
_LEVELS = [
    (96, 6, "Ultima esperanza de la humanidad"),
    (81, 5, ""),
    (61, 4, "🔦 Explorador Firefly"),
    (41, 3, ""),
    (21, 2, "Quarentena"),
    (0,  1, "Paciente 0"),
]
```

### XP Bar Gradients

```python
_XP_GRAD = {
    1: "linear-gradient(90deg,#1a1a1a,#2d2d2d)",          # Dead City Gray
    2: "linear-gradient(90deg,#2d1200,#5c2800)",           # Cordyceps Early
    3: "linear-gradient(90deg,#3d1800,#8b4500)",           # Cordyceps Deep
    4: "linear-gradient(90deg,#0a2010,#1a5030)",           # Firefly Dark
    5: "linear-gradient(90deg,#0d3020,#2a7050)",           # Firefly Green
    6: "linear-gradient(90deg,#0d2d20,#4ca66b,#d4870a)",  # Ellie — immune meets cordyceps
}
```

### CSS Accent Colors

```python
_LV_CSS_COLOR = {
    1: "#444444",   # Dead Gray
    2: "#7a3000",   # Dark Amber
    3: "#cc5500",   # Cordyceps Orange
    4: "#2d7a45",   # Firefly Dark Green
    5: "#4ca66b",   # Firefly Green
    6: "#4ca66b",   # Ellie (gradient handled in HTML)
}
```

### Level-up Banner Config

```python
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
```

Level 6 uses the tri-color gradient and an extra shockwave ring (same as NB2 level 6).

---

## Achievements

Same rarity system as NB2: Común → Raro → Épico → Legendario.

| Key | Trigger | Name | Rarity |
|---|---|---|---|
| `primer_contagio` | First XP earned | `🍄 Primer Contagio — Primera Exposición` | Común |
| `ojo_clinico` | All debug exercises perfect | `🩺 Ojo Clínico — Cero Errores de Lógica` | Raro |
| `superviviente_zona` | All 3 checkpoints reached | `🚧 Superviviente de Zona — Todos los QZ` | Épico |
| `esporas` | Streak ≥ 5 | `💨 Esporas — Racha x5` | Raro |
| `modelo_sir` | All SIR/loop exercises perfect | `📈 Modelo SIR — Propagación Dominada` | Épico |
| `inmunidad_adaptativa` | 100% core score | `🧬 Inmunidad Adaptativa — 100% del Notebook` | Legendario |
| `esperanza_humanidad` | Both retos perfect | `✦ Esperanza de la Humanidad` | Legendario |

---

## Registration / Startup Screen

- Header: `[ FIREFLY RESEARCH NODE 7 — TERMINAL DE ANÁLISIS ]`
- Launch banner text: `¡SOBREVIVE!` (replaces NB2's `¡RAGNARÖK!`)
- Sub-text: `EJECUTA LA PRIMERA CELDA PARA COMENZAR LA MISIÓN`
- Rune-equivalent: Firefly symbol row — `✦ ✧ ✦ ✧ ✦ ✧ ✦ ✧ ✦ ✧`
- Chain ornament replacement: spore dots `· · · · ·` or `⬡ ⬡ ⬡ ⬡ ⬡`

---

## viz_epidemias.py — Aesthetic Spec

### SIR Curve
- Background: `#0D0D0D`
- S line: `#8FA3A8` (Quarantine Gray), I line: `#D4870A` (Cordyceps Amber), R line: `#4CA66B` (Firefly Green)
- No fills; `linewidth=2.5`; faint glow via shadow layer
- Title: `[ FIREFLY RESEARCH NODE 7 — SIMULACIÓN SIR ]`
- Watermark: `✦ FIREFLIES ✦` bottom-right, 10% opacity

### Zone Semaphore (R0 alert)
| R0 | Status | Color | Message |
|---|---|---|---|
| < 1 | `CONTENIDO` | Firefly Green | "La llama se apaga." |
| 1–2 | `VIGILANCIA` | Cordyceps Amber | "Monitorear. No correr. Aún." |
| > 2 | `CUARENTENA` | FEDRA Red | "Evacuación de Zona. Protocolo FEDRA activado." |
| > 4 | `EXTINCIÓN` | Blinking FEDRA Red | "No hay protocolo para esto." |

### Pathogen Comparison Chart
- Horizontal bar chart ranked by R0
- Walker Virus always rendered in Cordyceps Amber, separated by dashed line
- Label: `⚠ WALKER — MODELO NO APLICA (REANIMACIÓN)`

---

## Flavor Text Templates

**Section opener (Marlene's journal):**
> *"Boston, semana 3 post-Colapso. Dibujé la ciudad en cuadrícula. Cada bloque: susceptible o perdido. Los loops son la única manera de ver cuántos quedan."*

**Debug section (Ellie's margin note):**
> *"Joel diría que el código 'simplemente no funciona'. Yo digo que hay un error en la lógica del if. Arréglalo."*

**Reto intro:**
> *"El laboratorio en Salt Lake tiene los datos. Tú tienes el modelo. Construye el motor. El resto de la humanidad espera."*

**Walker Virus gap note:**
> *"R0 = 1.2. Mortalidad = 1.0. El modelo SIR no captura la reanimación. Eso es intencional. Ningún modelo captura lo que no tiene cura."*

---

## NB2 Structural Reference (mirror when building NB3)

- `autograder_nb2.py` — full working reference for HTML cards, level-up banners, achievement system, Supabase submit, registration form
- Core scoring: `_CORE_MAX` + `_BONUS_KEYS` pattern
- `_award()` → check rows → stars → combo → XP bar → achievements
- `_render_levelup()` → sparks + shockwave rings + bounce icon + slam text
- Font: `Press Start 2P` (Google Fonts)
- Supabase table: `submissions`, field `notebook` will be `"nb3"`
