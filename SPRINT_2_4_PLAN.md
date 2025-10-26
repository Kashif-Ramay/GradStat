# 🎯 Sprint 2.4: Enhanced Visualizations

## Goal
Transform static matplotlib plots into interactive, publication-ready visualizations with customization options.

## Features to Implement

### 1. Interactive Plots with Plotly ⏳
**Priority:** HIGH

**Description:**
- Replace static matplotlib plots with interactive Plotly plots
- Hover tooltips with data values
- Zoom, pan, and export capabilities
- Responsive design

**Implementation:**
- Install `plotly` and `kaleido` (for static export)
- Create wrapper functions for common plot types
- Convert to JSON for frontend rendering
- Use Plotly.js in React frontend

**Plot Types to Convert:**
- Scatter plots
- Line plots
- Box plots
- Bar charts
- Histograms
- Heatmaps
- Survival curves

---

### 2. Publication-Ready Figures ⏳
**Priority:** HIGH

**Description:**
- High-resolution output (300 DPI minimum)
- Professional styling
- Proper axis labels and titles
- Legend positioning
- Grid options
- Font customization

**Features:**
- DPI settings (72, 150, 300, 600)
- Figure size presets (journal, presentation, poster)
- Font family selection (Arial, Times, Helvetica)
- Font size scaling
- Color palette options

---

### 3. Customizable Themes ⏳
**Priority:** MEDIUM

**Description:**
- Pre-built color schemes
- Light/dark mode
- Colorblind-friendly palettes
- Grayscale option for print

**Themes:**
- Default (blue/orange)
- Scientific (grayscale with accent)
- Colorblind-safe (Okabe-Ito palette)
- Vibrant (high contrast)
- Pastel (soft colors)
- Monochrome (publication-ready)

---

### 4. Multiple Export Formats ⏳
**Priority:** MEDIUM

**Description:**
- PNG (raster, web-friendly)
- SVG (vector, scalable)
- PDF (publication-ready)
- Interactive HTML (Plotly)

**Implementation:**
- Backend generates multiple formats
- Frontend provides download buttons
- Batch export option (all plots at once)

---

### 5. Plot Customization UI ⏳
**Priority:** LOW

**Description:**
- Frontend controls for plot appearance
- Real-time preview
- Save preferences

**Controls:**
- Title and axis labels
- Font sizes
- Color scheme
- Grid on/off
- Legend position
- Figure dimensions

---

### 6. Enhanced Plot Types ⏳
**Priority:** MEDIUM

**Description:**
- Add more sophisticated visualizations
- Statistical annotations
- Confidence bands
- Error bars

**New Plots:**
- Violin plots (distribution + box plot)
- Ridge plots (multiple distributions)
- Raincloud plots (distribution + scatter + box)
- Forest plots (meta-analysis)
- Q-Q plots (normality check)
- Residual plots (regression diagnostics)

---

## Architecture

### Backend Structure
```
worker/
  visualization.py          # New file - Plotly wrapper functions
  analysis_functions.py     # Update to use new viz functions
  requirements.txt          # Add plotly, kaleido
```

### Frontend Structure
```
frontend/src/components/
  PlotlyChart.tsx           # New component - Plotly.js wrapper
  PlotCustomizer.tsx        # New component - Plot controls
  ExportOptions.tsx         # New component - Export buttons
  
frontend/src/utils/
  plotly-config.ts          # Plotly configuration
```

---

## Implementation Plan

### Phase 1: Plotly Integration (3-4 hours)
1. Install Plotly and dependencies
2. Create `visualization.py` with wrapper functions
3. Convert 5 common plot types to Plotly
4. Test backend generation

### Phase 2: Frontend Integration (2-3 hours)
1. Create `PlotlyChart.tsx` component
2. Update `Results.tsx` to use Plotly charts
3. Add interactive features (zoom, pan, hover)
4. Test rendering

### Phase 3: Export & Themes (1-2 hours)
1. Implement multiple export formats
2. Create theme system
3. Add export buttons to UI
4. Test downloads

---

## Plotly Plot Examples

### Scatter Plot:
```python
import plotly.graph_objects as go

fig = go.Figure(data=go.Scatter(
    x=x_data,
    y=y_data,
    mode='markers',
    marker=dict(size=8, color='blue', opacity=0.6),
    hovertemplate='X: %{x}<br>Y: %{y}<extra></extra>'
))

fig.update_layout(
    title='Scatter Plot',
    xaxis_title='X Variable',
    yaxis_title='Y Variable',
    hovermode='closest',
    template='plotly_white'
)

# Convert to JSON for frontend
plot_json = fig.to_json()
```

### Box Plot:
```python
fig = go.Figure()
for group in groups:
    fig.add_trace(go.Box(
        y=data[group],
        name=group,
        boxmean='sd'
    ))

fig.update_layout(
    title='Box Plot by Group',
    yaxis_title='Value',
    template='plotly_white'
)
```

---

## Theme Configuration

### Color Palettes:
```python
THEMES = {
    'default': ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'],
    'colorblind': ['#E69F00', '#56B4E9', '#009E73', '#F0E442'],
    'grayscale': ['#000000', '#404040', '#808080', '#C0C0C0'],
    'vibrant': ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A'],
    'pastel': ['#A8E6CF', '#FFD3B6', '#FFAAA5', '#FF8B94']
}
```

---

## Export Options

### Format Specifications:
- **PNG:** 300 DPI, RGB, transparent background option
- **SVG:** Vector, editable in Illustrator/Inkscape
- **PDF:** Embedded fonts, CMYK option for print
- **HTML:** Interactive Plotly plot, standalone file

---

## UI Design

### Plot Controls Panel:
```
┌─────────────────────────────────────────┐
│ 🎨 Plot Customization                   │
├─────────────────────────────────────────┤
│ Theme: [Default ▼]                      │
│ DPI: [300 ▼]                            │
│ Size: [Journal (6x4) ▼]                │
│                                         │
│ Title: [Scatter Plot          ]        │
│ X-axis: [Variable X           ]        │
│ Y-axis: [Variable Y           ]        │
│                                         │
│ ☑ Show grid                            │
│ ☑ Show legend                          │
│ Legend position: [Top Right ▼]         │
│                                         │
│ [Apply] [Reset]                        │
└─────────────────────────────────────────┘
```

### Export Panel:
```
┌─────────────────────────────────────────┐
│ 💾 Export Options                       │
├─────────────────────────────────────────┤
│ Format:                                 │
│ [📊 PNG] [📐 SVG] [📄 PDF] [🌐 HTML]   │
│                                         │
│ Quality: [High (300 DPI) ▼]            │
│                                         │
│ [Download This Plot]                    │
│ [Download All Plots]                    │
└─────────────────────────────────────────┘
```

---

## Success Metrics

### Functionality:
- ✅ All plot types converted to Plotly
- ✅ Interactive features working (zoom, pan, hover)
- ✅ Multiple export formats available
- ✅ Themes applied correctly

### User Experience:
- ✅ Plots load quickly (<1 second)
- ✅ Interactions smooth and responsive
- ✅ Export downloads work reliably
- ✅ Customization intuitive

### Quality:
- ✅ Publication-ready output (300+ DPI)
- ✅ Professional appearance
- ✅ Consistent styling
- ✅ Accessible color schemes

---

## Estimated Timeline

**Total: 6-8 hours**

- Phase 1 (Plotly Integration): 3-4 hours
- Phase 2 (Frontend): 2-3 hours
- Phase 3 (Export & Themes): 1-2 hours

---

## Dependencies

### Python Packages:
```
plotly>=5.18.0
kaleido>=0.2.1
```

### Frontend Packages:
```
react-plotly.js
plotly.js
```

---

## Next Steps

1. Install Plotly dependencies
2. Create visualization.py module
3. Convert scatter, box, line plots
4. Create PlotlyChart component
5. Test interactive features
6. Add export options

**Ready to start implementation!** 🚀
