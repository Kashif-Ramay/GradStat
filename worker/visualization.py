"""
Enhanced Visualizations with Plotly
Interactive, publication-ready plots with themes and export options
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
import json

# Color themes
THEMES = {
    'default': {
        'colors': ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b'],
        'template': 'plotly_white'
    },
    'colorblind': {
        'colors': ['#E69F00', '#56B4E9', '#009E73', '#F0E442', '#0072B2', '#D55E00'],
        'template': 'plotly_white'
    },
    'grayscale': {
        'colors': ['#000000', '#404040', '#808080', '#A0A0A0', '#C0C0C0', '#E0E0E0'],
        'template': 'simple_white'
    },
    'vibrant': {
        'colors': ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', '#F7DC6F'],
        'template': 'plotly_white'
    },
    'scientific': {
        'colors': ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#6A994E', '#BC4B51'],
        'template': 'simple_white'
    }
}


def get_theme_config(theme: str = 'default') -> Dict:
    """Get theme configuration"""
    return THEMES.get(theme, THEMES['default'])


def create_scatter_plot(
    x: List, 
    y: List, 
    title: str = 'Scatter Plot',
    x_label: str = 'X',
    y_label: str = 'Y',
    groups: Optional[List] = None,
    theme: str = 'default'
) -> Dict:
    """
    Create interactive scatter plot
    
    Args:
        x: X-axis data
        y: Y-axis data
        title: Plot title
        x_label: X-axis label
        y_label: Y-axis label
        groups: Optional group labels for coloring
        theme: Color theme
        
    Returns:
        Dictionary with Plotly JSON and metadata
    """
    theme_config = get_theme_config(theme)
    
    fig = go.Figure()
    
    if groups is None:
        # Single group
        fig.add_trace(go.Scatter(
            x=x,
            y=y,
            mode='markers',
            marker=dict(
                size=8,
                color=theme_config['colors'][0],
                opacity=0.7,
                line=dict(width=1, color='white')
            ),
            hovertemplate=f'{x_label}: %{{x}}<br>{y_label}: %{{y}}<extra></extra>'
        ))
    else:
        # Multiple groups
        unique_groups = list(set(groups))
        for i, group in enumerate(unique_groups):
            mask = [g == group for g in groups]
            fig.add_trace(go.Scatter(
                x=[x[j] for j in range(len(x)) if mask[j]],
                y=[y[j] for j in range(len(y)) if mask[j]],
                mode='markers',
                name=str(group),
                marker=dict(
                    size=8,
                    color=theme_config['colors'][i % len(theme_config['colors'])],
                    opacity=0.7,
                    line=dict(width=1, color='white')
                ),
                hovertemplate=f'{x_label}: %{{x}}<br>{y_label}: %{{y}}<extra></extra>'
            ))
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=16)),
        xaxis_title=x_label,
        yaxis_title=y_label,
        template=theme_config['template'],
        hovermode='closest',
        showlegend=groups is not None,
        font=dict(size=12),
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    return {
        'type': 'plotly',
        'data': json.loads(fig.to_json()),
        'title': title,
        'interactive': True
    }


def create_box_plot(
    data: pd.DataFrame,
    value_col: str,
    group_col: str,
    title: str = 'Box Plot',
    y_label: str = 'Value',
    theme: str = 'default'
) -> Dict:
    """
    Create interactive box plot
    
    Args:
        data: DataFrame with data
        value_col: Column name for values
        group_col: Column name for groups
        title: Plot title
        y_label: Y-axis label
        theme: Color theme
        
    Returns:
        Dictionary with Plotly JSON and metadata
    """
    theme_config = get_theme_config(theme)
    
    fig = go.Figure()
    
    groups = data[group_col].unique()
    for i, group in enumerate(groups):
        group_data = data[data[group_col] == group][value_col]
        fig.add_trace(go.Box(
            y=group_data,
            name=str(group),
            marker_color=theme_config['colors'][i % len(theme_config['colors'])],
            boxmean='sd',  # Show mean and SD
            hovertemplate='%{y}<extra></extra>'
        ))
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=16)),
        xaxis_title=group_col,
        yaxis_title=y_label,
        template=theme_config['template'],
        showlegend=False,
        font=dict(size=12),
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    return {
        'type': 'plotly',
        'data': json.loads(fig.to_json()),
        'title': title,
        'interactive': True
    }


def create_line_plot(
    x: List,
    y: List,
    title: str = 'Line Plot',
    x_label: str = 'X',
    y_label: str = 'Y',
    error: Optional[List] = None,
    groups: Optional[List] = None,
    group_names: Optional[List] = None,
    theme: str = 'default'
) -> Dict:
    """
    Create interactive line plot with optional error bars
    
    Args:
        x: X-axis data (can be list of lists for multiple lines)
        y: Y-axis data (can be list of lists for multiple lines)
        title: Plot title
        x_label: X-axis label
        y_label: Y-axis label
        error: Optional error values
        groups: Optional group indices
        group_names: Optional group names
        theme: Color theme
        
    Returns:
        Dictionary with Plotly JSON and metadata
    """
    theme_config = get_theme_config(theme)
    
    fig = go.Figure()
    
    # Handle single or multiple lines
    if groups is None:
        # Single line
        trace_config = dict(
            x=x,
            y=y,
            mode='lines+markers',
            line=dict(color=theme_config['colors'][0], width=2),
            marker=dict(size=6),
            hovertemplate=f'{x_label}: %{{x}}<br>{y_label}: %{{y}}<extra></extra>'
        )
        
        if error is not None:
            trace_config['error_y'] = dict(
                type='data',
                array=error,
                visible=True,
                color='rgba(0,0,0,0.3)'
            )
        
        fig.add_trace(go.Scatter(**trace_config))
    else:
        # Multiple lines
        unique_groups = list(set(groups))
        for i, group in enumerate(unique_groups):
            mask = [g == group for g in groups]
            group_x = [x[j] for j in range(len(x)) if mask[j]]
            group_y = [y[j] for j in range(len(y)) if mask[j]]
            
            name = group_names[i] if group_names and i < len(group_names) else str(group)
            
            fig.add_trace(go.Scatter(
                x=group_x,
                y=group_y,
                mode='lines+markers',
                name=name,
                line=dict(color=theme_config['colors'][i % len(theme_config['colors'])], width=2),
                marker=dict(size=6),
                hovertemplate=f'{x_label}: %{{x}}<br>{y_label}: %{{y}}<extra></extra>'
            ))
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=16)),
        xaxis_title=x_label,
        yaxis_title=y_label,
        template=theme_config['template'],
        hovermode='x unified',
        showlegend=groups is not None,
        font=dict(size=12),
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    return {
        'type': 'plotly',
        'data': json.loads(fig.to_json()),
        'title': title,
        'interactive': True
    }


def create_histogram(
    data: List,
    title: str = 'Histogram',
    x_label: str = 'Value',
    y_label: str = 'Frequency',
    bins: int = 30,
    theme: str = 'default'
) -> Dict:
    """
    Create interactive histogram
    
    Args:
        data: Data values
        title: Plot title
        x_label: X-axis label
        y_label: Y-axis label
        bins: Number of bins
        theme: Color theme
        
    Returns:
        Dictionary with Plotly JSON and metadata
    """
    theme_config = get_theme_config(theme)
    
    fig = go.Figure(data=[go.Histogram(
        x=data,
        nbinsx=bins,
        marker_color=theme_config['colors'][0],
        opacity=0.75,
        hovertemplate='Range: %{x}<br>Count: %{y}<extra></extra>'
    )])
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=16)),
        xaxis_title=x_label,
        yaxis_title=y_label,
        template=theme_config['template'],
        font=dict(size=12),
        plot_bgcolor='white',
        paper_bgcolor='white',
        bargap=0.1
    )
    
    return {
        'type': 'plotly',
        'data': json.loads(fig.to_json()),
        'title': title,
        'interactive': True
    }


def create_bar_plot(
    categories: List,
    values: List,
    title: str = 'Bar Plot',
    x_label: str = 'Category',
    y_label: str = 'Value',
    theme: str = 'default'
) -> Dict:
    """
    Create interactive bar plot
    
    Args:
        categories: Category labels
        values: Values for each category
        title: Plot title
        x_label: X-axis label
        y_label: Y-axis label
        theme: Color theme
        
    Returns:
        Dictionary with Plotly JSON and metadata
    """
    theme_config = get_theme_config(theme)
    
    fig = go.Figure(data=[go.Bar(
        x=categories,
        y=values,
        marker_color=theme_config['colors'][0],
        hovertemplate='%{x}<br>%{y}<extra></extra>'
    )])
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=16)),
        xaxis_title=x_label,
        yaxis_title=y_label,
        template=theme_config['template'],
        font=dict(size=12),
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    return {
        'type': 'plotly',
        'data': json.loads(fig.to_json()),
        'title': title,
        'interactive': True
    }


def create_heatmap(
    data: pd.DataFrame,
    title: str = 'Heatmap',
    x_label: str = 'X',
    y_label: str = 'Y',
    colorscale: str = 'RdBu_r',
    theme: str = 'default'
) -> Dict:
    """
    Create interactive heatmap
    
    Args:
        data: DataFrame or 2D array
        title: Plot title
        x_label: X-axis label
        y_label: Y-axis label
        colorscale: Plotly colorscale name
        theme: Color theme
        
    Returns:
        Dictionary with Plotly JSON and metadata
    """
    theme_config = get_theme_config(theme)
    
    if isinstance(data, pd.DataFrame):
        z = data.values
        x = list(data.columns)
        y = list(data.index)
    else:
        z = data
        x = list(range(data.shape[1]))
        y = list(range(data.shape[0]))
    
    fig = go.Figure(data=go.Heatmap(
        z=z,
        x=x,
        y=y,
        colorscale=colorscale,
        hovertemplate='%{y} - %{x}<br>Value: %{z:.3f}<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=16)),
        xaxis_title=x_label,
        yaxis_title=y_label,
        template=theme_config['template'],
        font=dict(size=12)
    )
    
    return {
        'type': 'plotly',
        'data': json.loads(fig.to_json()),
        'title': title,
        'interactive': True
    }


def create_qq_plot(
    data: List,
    title: str = 'Q-Q Plot',
    theme: str = 'default'
) -> Dict:
    """
    Create Q-Q plot for normality assessment
    
    Args:
        data: Data values
        title: Plot title
        theme: Color theme
        
    Returns:
        Dictionary with Plotly JSON and metadata
    """
    from scipy import stats
    
    theme_config = get_theme_config(theme)
    
    # Calculate theoretical quantiles
    sorted_data = np.sort(data)
    n = len(sorted_data)
    theoretical_quantiles = stats.norm.ppf(np.linspace(0.01, 0.99, n))
    
    fig = go.Figure()
    
    # Add scatter points
    fig.add_trace(go.Scatter(
        x=theoretical_quantiles,
        y=sorted_data,
        mode='markers',
        marker=dict(color=theme_config['colors'][0], size=6),
        name='Data',
        hovertemplate='Theoretical: %{x:.2f}<br>Sample: %{y:.2f}<extra></extra>'
    ))
    
    # Add reference line
    min_val = min(min(theoretical_quantiles), min(sorted_data))
    max_val = max(max(theoretical_quantiles), max(sorted_data))
    fig.add_trace(go.Scatter(
        x=[min_val, max_val],
        y=[min_val, max_val],
        mode='lines',
        line=dict(color='red', dash='dash', width=2),
        name='Normal',
        hoverinfo='skip'
    ))
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=16)),
        xaxis_title='Theoretical Quantiles',
        yaxis_title='Sample Quantiles',
        template=theme_config['template'],
        font=dict(size=12),
        plot_bgcolor='white',
        paper_bgcolor='white',
        showlegend=True
    )
    
    return {
        'type': 'plotly',
        'data': json.loads(fig.to_json()),
        'title': title,
        'interactive': True
    }
