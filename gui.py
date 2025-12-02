"""
SIR Model Simülasyonu - Streamlit GUI
"""

import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import time
import io

from src.data_loading import create_sample_network, load_edge_list, get_largest_component
from src.centrality import calculate_all_centralities, get_top_k_nodes_by_measure
from src.sir_simulation import SIRModel, run_multiple_simulations, aggregate_simulation_results
from src.experiments import ExperimentRunner

st.set_page_config(
    page_title="SIR Model Simülasyonu",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    /* Ana Başlık Animasyonu */
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 0.5rem;
        animation: fadeInDown 0.8s ease-out;
    }
    
    .sub-header {
        font-size: 1.2rem;
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
        animation: fadeInUp 0.8s ease-out 0.2s both;
    }
    
    /* Fade In Animasyonları */
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes pulse {
        0%, 100% {
            transform: scale(1);
        }
        50% {
            transform: scale(1.05);
        }
    }
    
    @keyframes bounce {
        0%, 20%, 50%, 80%, 100% {
            transform: translateY(0);
        }
        40% {
            transform: translateY(-10px);
        }
        60% {
            transform: translateY(-5px);
        }
    }
    
    @keyframes shimmer {
        0% {
            background-position: -1000px 0;
        }
        100% {
            background-position: 1000px 0;
        }
    }
    
    /* Metric Card Animasyonları */
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        transition: all 0.3s ease;
        animation: fadeInUp 0.5s ease-out;
    }
    
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 4px 12px rgba(31, 119, 180, 0.2);
        border-left-width: 6px;
    }
    
    /* Progress Bar Animasyonu */
    .stProgress > div > div > div > div {
        background-color: #1f77b4;
        background-image: linear-gradient(
            90deg,
            rgba(255,255,255,0) 0%,
            rgba(255,255,255,0.3) 50%,
            rgba(255,255,255,0) 100%
        );
        background-size: 200% 100%;
        animation: shimmer 2s infinite;
        transition: width 0.3s ease;
    }
    
    /* Button Animasyonları */
    .stButton > button {
        transition: all 0.3s ease;
        animation: fadeIn 0.5s ease-out;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(31, 119, 180, 0.3);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Primary Button Özel Animasyon */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #1f77b4 0%, #2a9df4 100%);
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button[kind="primary"]::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        transition: left 0.5s;
    }
    
    .stButton > button[kind="primary"]:hover::before {
        left: 100%;
    }
    
    /* Success/Error Mesajları Animasyonu */
    .stSuccess {
        animation: slideInRight 0.5s ease-out, pulse 0.5s ease-out 0.5s;
    }
    
    .stError {
        animation: slideInRight 0.5s ease-out, shake 0.5s ease-out 0.5s;
    }
    
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-5px); }
        75% { transform: translateX(5px); }
    }
    
    /* Spinner Animasyonu */
    .stSpinner {
        animation: fadeIn 0.3s ease-out;
    }
    
    /* Tab Animasyonları */
    .stTabs [data-baseweb="tab-list"] {
        animation: fadeInDown 0.5s ease-out;
    }
    
    .stTabs [data-baseweb="tab"] {
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        transform: translateY(-2px);
    }
    
    /* Selectbox ve Slider Animasyonları */
    .stSelectbox, .stSlider {
        animation: fadeInUp 0.5s ease-out;
    }
    
    /* Info Box Animasyonu */
    .stInfo {
        animation: fadeInUp 0.5s ease-out;
        transition: all 0.3s ease;
    }
    
    .stInfo:hover {
        transform: scale(1.02);
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    /* Chart Container Animasyonu */
    [data-testid="stPlotlyChart"] {
        animation: fadeIn 0.8s ease-out;
        transition: transform 0.3s ease;
    }
    
    [data-testid="stPlotlyChart"]:hover {
        transform: scale(1.01);
    }
    
    /* Loading Overlay */
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Smooth Scroll */
    html {
        scroll-behavior: smooth;
    }
    
    /* Metric Value Animasyonu */
    [data-testid="stMetricValue"] {
        animation: fadeInUp 0.5s ease-out;
        transition: all 0.3s ease;
    }
    
    [data-testid="stMetricValue"]:hover {
        transform: scale(1.05);
        color: #1f77b4;
    }
    
    /* Sidebar Animasyonu */
    [data-testid="stSidebar"] {
        animation: slideInRight 0.5s ease-out;
    }
    
    /* Column Animasyonları */
    [data-testid="column"] {
        animation: fadeInUp 0.6s ease-out;
    }
    
    [data-testid="column"]:nth-child(1) {
        animation-delay: 0.1s;
    }
    
    [data-testid="column"]:nth-child(2) {
        animation-delay: 0.2s;
    }
    
    [data-testid="column"]:nth-child(3) {
        animation-delay: 0.3s;
    }
    
    /* Divider Animasyonu */
    hr {
        animation: fadeIn 0.5s ease-out;
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #1f77b4, transparent);
    }
    
    /* Text Input Animasyonu */
    .stTextInput > div > div > input {
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        transform: scale(1.02);
        box-shadow: 0 0 10px rgba(31, 119, 180, 0.3);
    }
</style>
""", unsafe_allow_html=True)

if 'graph' not in st.session_state:
    st.session_state.graph = None
if 'centralities' not in st.session_state:
    st.session_state.centralities = None
if 'experiment_results' not in st.session_state:
    st.session_state.experiment_results = None
if 'simulation_running' not in st.session_state:
    st.session_state.simulation_running = False
if 'layout_3d' not in st.session_state:
    st.session_state.layout_3d = None
if 'infection_history' not in st.session_state:
    st.session_state.infection_history = None
if 'last_initial_infected' not in st.session_state:
    st.session_state.last_initial_infected = None


def spring_layout_3d(G, seed=42, k=0.5, iterations=50):
    """3D spring layout hesapla"""
    # 2D layout hesapla
    pos_2d = nx.spring_layout(G, seed=seed, k=k, iterations=iterations, dim=2)
    
    # 3. boyutu ekle (merkeziyet skoruna göre veya rastgele)
    pos_3d = {}
    for node in G.nodes():
        x, y = pos_2d[node]
        # Z koordinatını degree'ye göre ayarla (daha yüksek degree = daha yüksek Z)
        z = G.degree(node) / max(dict(G.degree()).values()) if G.number_of_nodes() > 0 else 0
        pos_3d[node] = (x, y, z)
    
    return pos_3d


def plot_network_interactive(G, states=None, centrality=None, title="Network Graph", view_3d=False, pos_3d=None, show_edges=True):
    """Ağ görselleştirmesi"""
    
    if view_3d:
        return plot_network_3d(G, states, centrality, title, pos_3d, show_edges)
    
    # Layout hesapla
    pos = nx.spring_layout(G, seed=42, k=0.5, iterations=50)
    
    # Kenarlar
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)
    
    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')
    
    # Düğümler
    node_x = []
    node_y = []
    node_text = []
    node_color = []
    
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        
        # Node ismi varsa al
        node_name = G.nodes[node].get('name', f'Node {node}')
        
        # Durum bilgisi
        if states:
            state = states[node]
            node_text.append(f'{node_name}<br>State: {state}<br>Degree: {G.degree(node)}')
            
            # Renk
            if state == 'S':
                node_color.append('#3498db')  # Mavi
            elif state == 'I':
                node_color.append('#e74c3c')  # Kırmızı
            else:  # R
                node_color.append('#2ecc71')  # Yeşil
        elif centrality:
            score = centrality.get(node, 0)
            node_text.append(f'{node_name}<br>Centrality: {score:.4f}<br>Degree: {G.degree(node)}')
            node_color.append(score)
        else:
            node_text.append(f'{node_name}<br>Degree: {G.degree(node)}')
            node_color.append(G.degree(node))
    
    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        text=node_text,
        marker=dict(
            showscale=True if not states else False,
            colorscale='Viridis' if not states else None,
            color=node_color,
            size=10,
            colorbar=dict(
                thickness=15,
                title=dict(
                    text='Score' if centrality else 'Degree',
                    side='right'
                ),
                xanchor='left'
            ) if not states else None,
            line_width=2))
    
    # Figür oluştur
    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        title=dict(text=title, font=dict(size=16)),
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=0, l=0, r=0, t=40),
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        height=500
                    ))
    
    return fig


def plot_network_3d(G, states=None, centrality=None, title="3D Network Graph", pos_3d=None, show_edges=True):
    """3D ağ görselleştirmesi"""
    
    if pos_3d is None:
        pos_3d = spring_layout_3d(G, seed=42, k=0.5, iterations=50)
    
    traces = []
    
    if show_edges:
        edge_x, edge_y, edge_z = [], [], []
        for edge in G.edges():
            if edge[0] in pos_3d and edge[1] in pos_3d:
                x0, y0, z0 = pos_3d[edge[0]]
                x1, y1, z1 = pos_3d[edge[1]]
                edge_x.extend([x0, x1, None])
                edge_y.extend([y0, y1, None])
                edge_z.extend([z0, z1, None])
        
        edge_trace = go.Scatter3d(
            x=edge_x, y=edge_y, z=edge_z,
            mode='lines',
            line=dict(width=8, color='rgba(100,100,100,1)'),
            hoverinfo='none',
            showlegend=False,
            opacity=0.8
        )
        traces.append(edge_trace)
    
    # Düğümler için 3D koordinatlar
    node_x, node_y, node_z = [], [], []
    node_text = []
    node_color = []
    node_size = []
    
    for node in G.nodes():
        if node not in pos_3d:
            continue
        x, y, z = pos_3d[node]
        node_x.append(x)
        node_y.append(y)
        node_z.append(z)
        
        # Node ismi varsa al
        node_name = G.nodes[node].get('name', f'Node {node}')
        degree = G.degree(node)
        
        # Durum bilgisi
        if states:
            state = states[node]
            node_text.append(f'{node_name}<br>State: {state}<br>Degree: {degree}')
            
            # Renk
            if state == 'S':
                node_color.append('#3498db')  # Mavi
            elif state == 'I':
                node_color.append('#e74c3c')  # Kırmızı
            else:  # R
                node_color.append('#2ecc71')  # Yeşil
            
            # Boyut (duruma göre)
            node_size.append(15 if state == 'I' else 10)
        elif centrality:
            score = centrality.get(node, 0)
            node_text.append(f'{node_name}<br>Centrality: {score:.4f}<br>Degree: {degree}')
            node_color.append(score)
            # Boyut merkeziyet skoruna göre
            max_score = max(centrality.values()) if centrality.values() else 1
            node_size.append(5 + 15 * (score / max_score) if max_score > 0 else 10)
        else:
            node_text.append(f'{node_name}<br>Degree: {degree}')
            node_color.append(degree)
            # Boyut degree'ye göre
            max_degree = max(dict(G.degree()).values()) if G.number_of_nodes() > 0 else 1
            node_size.append(5 + 15 * (degree / max_degree) if max_degree > 0 else 10)
    
    # Colorbar için colorscale
    if states:
        colorscale = None
        show_colorbar = False
    else:
        colorscale = 'Viridis'
        show_colorbar = True
    
    node_trace = go.Scatter3d(
        x=node_x, y=node_y, z=node_z,
        mode='markers',
        marker=dict(
            size=node_size,
            color=node_color,
            colorscale=colorscale,
            showscale=show_colorbar,
            colorbar=dict(
                thickness=20,
                title=dict(
                    text='Score' if centrality else 'Degree',
                    side='right'
                ),
                x=1.1
            ) if show_colorbar else None,
            line=dict(width=1, color='rgba(50,50,50,0.5)'),
            opacity=0.9
        ),
        text=node_text,
        hoverinfo='text',
        name='Nodes'
    )
    
    traces.append(node_trace)
    
    fig = go.Figure(data=traces)
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=18)),
        scene=dict(
            xaxis=dict(title='X', showgrid=True, gridcolor='rgba(200,200,200,0.3)'),
            yaxis=dict(title='Y', showgrid=True, gridcolor='rgba(200,200,200,0.3)'),
            zaxis=dict(title='Z (Degree)', showgrid=True, gridcolor='rgba(200,200,200,0.3)'),
            bgcolor='rgba(255,255,255,0.9)',
            camera=dict(
                eye=dict(x=1.5, y=1.5, z=1.2),
                center=dict(x=0, y=0, z=0)
            )
        ),
        height=600,
        margin=dict(l=0, r=0, t=50, b=0),
        hovermode='closest'
    )
    
    return fig


def plot_time_series_interactive(time_series_dict, title="SIR Time Series"):
    """Zaman serisi grafiği"""
    
    fig = go.Figure()
    
    colors = {'random': 'gray', 'degree': 'red', 'betweenness': 'blue',
              'closeness': 'green', 'eigenvector': 'purple'}
    
    for scenario, time_series in time_series_dict.items():
        S_values = [counts[0] for counts in time_series]
        I_values = [counts[1] for counts in time_series]
        R_values = [counts[2] for counts in time_series]
        time_steps = list(range(len(S_values)))
        
        color = colors.get(scenario, 'black')
        scenario_name = scenario.replace('_', ' ').title()
        
        # S
        fig.add_trace(go.Scatter(
            x=time_steps, y=S_values,
            mode='lines',
            name=f'{scenario_name} - S',
            line=dict(color=color, dash='solid'),
            legendgroup=scenario
        ))
        
        # I
        fig.add_trace(go.Scatter(
            x=time_steps, y=I_values,
            mode='lines',
            name=f'{scenario_name} - I',
            line=dict(color=color, dash='dash'),
            legendgroup=scenario
        ))
        
        # R
        fig.add_trace(go.Scatter(
            x=time_steps, y=R_values,
            mode='lines',
            name=f'{scenario_name} - R',
            line=dict(color=color, dash='dot'),
            legendgroup=scenario
        ))
    
    fig.update_layout(
        title=title,
        xaxis_title="Time Step",
        yaxis_title="Count",
        hovermode='x unified',
        height=500
    )
    
    return fig


def plot_comparison_interactive(plotting_data):
    """Karşılaştırma grafiği"""
    
    scenarios = [s.replace('_', ' ').title() for s in plotting_data['scenarios']]
    
    fig = make_subplots(
        rows=1, cols=3,
        subplot_titles=('Final Outbreak Size', 'Peak Infected', 'Peak Time')
    )
    
    colors = ['gray', 'red', 'blue', 'green', 'purple'][:len(scenarios)]
    
    # Outbreak Size
    fig.add_trace(
        go.Bar(
            x=scenarios,
            y=plotting_data['outbreak_sizes'],
            error_y=dict(type='data', array=plotting_data['outbreak_stds']),
            marker_color=colors,
            showlegend=False,
            text=[f"{val:.0f}" for val in plotting_data['outbreak_sizes']],
            textposition='outside'
        ),
        row=1, col=1
    )
    
    # Peak Infected
    fig.add_trace(
        go.Bar(
            x=scenarios,
            y=plotting_data['peak_infecteds'],
            error_y=dict(type='data', array=plotting_data['peak_infected_stds']),
            marker_color=colors,
            showlegend=False,
            text=[f"{val:.0f}" for val in plotting_data['peak_infecteds']],
            textposition='outside'
        ),
        row=1, col=2
    )
    
    # Peak Time
    fig.add_trace(
        go.Bar(
            x=scenarios,
            y=plotting_data['peak_times'],
            error_y=dict(type='data', array=plotting_data['peak_time_stds']),
            marker_color=colors,
            showlegend=False,
            text=[f"{val:.1f}" for val in plotting_data['peak_times']],
            textposition='outside'
        ),
        row=1, col=3
    )
    
    fig.update_layout(height=400, showlegend=False)
    fig.update_xaxes(tickangle=45)
    
    return fig


def plot_infection_path(G, infection_history, initial_infected, title="Enfeksiyon Yolu Takibi", view_3d=False, pos_3d=None, show_edges=True):
    """Enfeksiyon yolu görselleştirmesi"""
    
    if view_3d and pos_3d is None:
        pos_3d = spring_layout_3d(G, seed=42, k=0.5, iterations=50)
    
    if view_3d:
        return plot_infection_path_3d(G, infection_history, initial_infected, title, pos_3d, show_edges)
    
    pos = nx.spring_layout(G, seed=42, k=0.5, iterations=50)
    
    # Normal kenarlar (gri, ince)
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
    
    normal_edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='rgba(200,200,200,0.3)'),
        hoverinfo='none',
        mode='lines',
        name='Ağ Bağlantıları'
    )
    
    # Enfeksiyon yolu kenarları (kırmızı, kalın)
    infection_edge_x = []
    infection_edge_y = []
    infection_edge_info = []
    
    for node, (source, time_step) in infection_history.items():
        if source is not None:  # Başlangıç enfekte değilse
            if source in pos and node in pos:
                x0, y0 = pos[source]
                x1, y1 = pos[node]
                infection_edge_x.extend([x0, x1, None])
                infection_edge_y.extend([y0, y1, None])
                infection_edge_info.extend([f"t={time_step}", f"t={time_step}", None])
    
    infection_edge_trace = go.Scatter(
        x=infection_edge_x, y=infection_edge_y,
        line=dict(width=3, color='rgba(231,76,60,0.8)'),
        hoverinfo='text',
        text=infection_edge_info,
        mode='lines',
        name='Enfeksiyon Yolu'
    )
    
    # Node'lar
    node_x = []
    node_y = []
    node_text = []
    node_color = []
    node_size = []
    
    max_time = max((time_step for _, (_, time_step) in infection_history.items()), default=0)
    
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        
        node_name = G.nodes[node].get('name', f'Node {node}')
        
        if node in initial_infected:
            node_text.append(f'{node_name}<br>Başlangıç Enfekte (t=0)')
            node_color.append('#e74c3c')  # Koyu kırmızı
            node_size.append(20)
        elif node in infection_history:
            source, time_step = infection_history[node]
            if source is not None:
                node_text.append(f'{node_name}<br>Enfekte: t={time_step}<br>Kaynak: Node {source}')
            else:
                node_text.append(f'{node_name}<br>Başlangıç Enfekte')
            node_color.append('#f39c12')  # Sarı
            node_size.append(15)
        else:
            node_text.append(f'{node_name}<br>Enfekte Olmadı')
            node_color.append('#3498db')  # Mavi
            node_size.append(10)
    
    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        text=node_text,
        marker=dict(
            color=node_color,
            size=node_size,
            line=dict(width=2, color='rgba(50,50,50,0.8)')
        ),
        name='Düğümler'
    )
    
    fig = go.Figure(data=[normal_edge_trace, infection_edge_trace, node_trace],
                    layout=go.Layout(
                        title=dict(text=title, font=dict(size=16)),
                        showlegend=True,
                        hovermode='closest',
                        margin=dict(b=0, l=0, r=0, t=40),
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        height=600
                    ))
    
    # Patient Zero annotations
    for node in initial_infected:
        if node in pos:
            x, y = pos[node]
            fig.add_annotation(
                x=x,
                y=y + 0.05,
                text="Patient Zero",
                showarrow=True,
                arrowhead=2,
                arrowsize=1,
                arrowwidth=2,
                arrowcolor="#e74c3c",
                ax=0,
                ay=-30,
                font=dict(size=12, color="#e74c3c", family="Arial Black")
            )
    
    return fig


def plot_infection_path_3d(G, infection_history, initial_infected, title="3D Enfeksiyon Yolu Takibi", pos_3d=None, show_edges=True):
    """3D enfeksiyon yolu görselleştirmesi"""
    
    if pos_3d is None:
        pos_3d = spring_layout_3d(G, seed=42, k=0.5, iterations=50)
    
    traces = []
    
    # Normal kenarlar
    if show_edges:
        edge_x, edge_y, edge_z = [], [], []
        for edge in G.edges():
            if edge[0] in pos_3d and edge[1] in pos_3d:
                x0, y0, z0 = pos_3d[edge[0]]
                x1, y1, z1 = pos_3d[edge[1]]
                edge_x.extend([x0, x1, None])
                edge_y.extend([y0, y1, None])
                edge_z.extend([z0, z1, None])
        
        normal_edge_trace = go.Scatter3d(
            x=edge_x, y=edge_y, z=edge_z,
            mode='lines',
            line=dict(width=2, color='rgba(200,200,200,0.2)'),
            hoverinfo='none',
            showlegend=True,
            name='Ağ Bağlantıları'
        )
        traces.append(normal_edge_trace)
    
    # Enfeksiyon yolu kenarları
    infection_edge_x, infection_edge_y, infection_edge_z = [], [], []
    for node, (source, time_step) in infection_history.items():
        if source is not None and source in pos_3d and node in pos_3d:
            x0, y0, z0 = pos_3d[source]
            x1, y1, z1 = pos_3d[node]
            infection_edge_x.extend([x0, x1, None])
            infection_edge_y.extend([y0, y1, None])
            infection_edge_z.extend([z0, z1, None])
    
    if infection_edge_x:
        infection_edge_trace = go.Scatter3d(
            x=infection_edge_x, y=infection_edge_y, z=infection_edge_z,
            mode='lines',
            line=dict(width=8, color='rgba(231,76,60,0.9)'),
            hoverinfo='none',
            showlegend=True,
            name='Enfeksiyon Yolu'
        )
        traces.append(infection_edge_trace)
    
    # Node'lar
    node_x, node_y, node_z = [], [], []
    node_text = []
    node_color = []
    node_size = []
    
    max_time = max((time_step for _, (_, time_step) in infection_history.items()), default=0)
    
    for node in G.nodes():
        if node not in pos_3d:
            continue
        x, y, z = pos_3d[node]
        node_x.append(x)
        node_y.append(y)
        node_z.append(z)
        
        node_name = G.nodes[node].get('name', f'Node {node}')
        
        if node in initial_infected:
            node_text.append(f'{node_name}<br>Başlangıç Enfekte (t=0)')
            node_color.append('#e74c3c')
            node_size.append(20)
        elif node in infection_history:
            source, time_step = infection_history[node]
            if source is not None:
                node_text.append(f'{node_name}<br>Enfekte: t={time_step}<br>Kaynak: Node {source}')
            else:
                node_text.append(f'{node_name}<br>Başlangıç Enfekte')
            node_color.append('#f39c12')  # Sarı
            node_size.append(15)
        else:
            node_text.append(f'{node_name}<br>Enfekte Olmadı')
            node_color.append('#3498db')
            node_size.append(10)
    
    node_trace = go.Scatter3d(
        x=node_x, y=node_y, z=node_z,
        mode='markers',
        marker=dict(
            size=node_size,
            color=node_color,
            line=dict(width=2, color='rgba(50,50,50,0.8)'),
            opacity=0.9
        ),
        text=node_text,
        hoverinfo='text',
        name='Düğümler'
    )
    traces.append(node_trace)
    
    fig = go.Figure(data=traces)
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=18)),
        scene=dict(
            xaxis=dict(title='X', showgrid=True, gridcolor='rgba(200,200,200,0.3)'),
            yaxis=dict(title='Y', showgrid=True, gridcolor='rgba(200,200,200,0.3)'),
            zaxis=dict(title='Z (Degree)', showgrid=True, gridcolor='rgba(200,200,200,0.3)'),
            bgcolor='rgba(255,255,255,0.9)',
            camera=dict(
                eye=dict(x=1.5, y=1.5, z=1.2),
                center=dict(x=0, y=0, z=0)
            ),
            annotations=[
                dict(
                    x=pos_3d[node][0],
                    y=pos_3d[node][1],
                    z=pos_3d[node][2] + 0.15,
                    text="Patient Zero",
                    showarrow=True,
                    arrowhead=2,
                    arrowsize=1.5,
                    arrowwidth=2,
                    arrowcolor="#e74c3c",
                    ax=0,
                    ay=-50,
                    font=dict(size=12, color="#e74c3c")
                )
                for node in initial_infected if node in pos_3d
            ]
        ),
        height=700,
        margin=dict(l=0, r=0, t=50, b=0),
        hovermode='closest'
    )
    
    return fig


def main():
    # Başlık
    st.markdown('<p class="main-header">SIR Model Simülasyonu</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Merkeziyet Ölçüleri ve Hastalık Yayılımı Analizi</p>', unsafe_allow_html=True)
    
    st.sidebar.header("Veri Seti")
    
    data_source = st.sidebar.radio(
        "Veri Kaynağı Seçin:",
        ["Örnek Ağ Oluştur", "Hazır Modeller"]
    )
    
    G = None
    
    if data_source == "Örnek Ağ Oluştur":
        st.sidebar.subheader("Ağ Parametreleri")
        
        network_type = st.sidebar.selectbox(
            "Ağ Tipi:",
            ["Watts-Strogatz (Small World)", "Barabási-Albert (Scale Free)", "Erdős-Rényi (Random)"]
        )
        
        n_nodes = st.sidebar.slider("Düğüm Sayısı (n)", 50, 500, 200, 10)
        
        if network_type == "Watts-Strogatz (Small World)":
            k = st.sidebar.slider("Komşu Sayısı (k)", 2, 20, 6, 1)
            p = st.sidebar.slider("Rewiring Olasılığı (p)", 0.0, 1.0, 0.1, 0.05)
            
            if st.sidebar.button("Ağ Oluştur", type="primary"):
                with st.spinner("Ağ oluşturuluyor..."):
                    G = nx.watts_strogatz_graph(n_nodes, k, p, seed=42)
                    st.session_state.graph = G
                    st.session_state.centralities = None
                    st.success(f"Ağ oluşturuldu: {G.number_of_nodes()} düğüm, {G.number_of_edges()} kenar")
        
        elif network_type == "Barabási-Albert (Scale Free)":
            m = st.sidebar.slider("Yeni düğüm bağlantı sayısı (m)", 1, 10, 3, 1)
            
            if st.sidebar.button("Ağ Oluştur", type="primary"):
                with st.spinner("Ağ oluşturuluyor..."):
                    G = nx.barabasi_albert_graph(n_nodes, m, seed=42)
                    st.session_state.graph = G
                    st.session_state.centralities = None
                    st.success(f"Ağ oluşturuldu: {G.number_of_nodes()} düğüm, {G.number_of_edges()} kenar")
        
        else:  # Erdős-Rényi
            p_edge = st.sidebar.slider("Kenar Olasılığı (p)", 0.01, 0.2, 0.05, 0.01)
            
            if st.sidebar.button("Ağ Oluştur", type="primary"):
                with st.spinner("Ağ oluşturuluyor..."):
                    G = nx.erdos_renyi_graph(n_nodes, p_edge, seed=42)
                    if not nx.is_connected(G):
                        largest_cc = max(nx.connected_components(G), key=len)
                        G = G.subgraph(largest_cc).copy()
                    st.session_state.graph = G
                    st.session_state.centralities = None
                    st.success(f"Ağ oluşturuldu: {G.number_of_nodes()} düğüm, {G.number_of_edges()} kenar")
    
    else:
        st.sidebar.subheader("Hazır Modeller")
        
        predefined = st.sidebar.selectbox(
            "Model Seçin:",
            ["Karate Club (34 düğüm)", "Les Misérables (77 düğüm)", "Örnek Ağ (100 düğüm)"]
        )
        
        if st.sidebar.button("Modeli Yükle", type="primary"):
            with st.spinner("Ağ yükleniyor..."):
                try:
                    if predefined == "Karate Club (34 düğüm)":
                        G = nx.karate_club_graph()
                    elif predefined == "Les Misérables (77 düğüm)":
                        G = nx.les_miserables_graph()
                    else:
                        G = create_sample_network(n=100, k=6, p=0.1)
                    
                    st.session_state.graph = G
                    st.session_state.centralities = None
                    st.success(f"Ağ yüklendi: {G.number_of_nodes()} düğüm, {G.number_of_edges()} kenar")
                
                except Exception as e:
                    st.error(f"Yükleme hatası: {str(e)}")
                    import traceback
                    st.code(traceback.format_exc())
    
    # Graf yüklendiyse
    G = st.session_state.graph
    
    if G is not None:
        
        st.sidebar.header("Simülasyon Parametreleri")
        
        beta = st.sidebar.slider("Bulaşma Olasılığı (β)", 0.0, 1.0, 0.3, 0.05)
        gamma = st.sidebar.slider("İyileşme Olasılığı (γ)", 0.0, 1.0, 0.1, 0.05)
        
        R0 = beta / gamma if gamma > 0 else float('inf')
        st.sidebar.metric("R₀ (Temel Üreme Sayısı)", f"{R0:.2f}")
        
        k_initial = st.sidebar.slider("Başlangıç Enfekte Sayısı", 1, min(20, G.number_of_nodes()//10), 5, 1)
        n_runs = st.sidebar.slider("Tekrar Sayısı", 5, 100, 30, 5)
        
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["Ağ Analizi", "Simülasyon", "Sonuçlar", "Animasyon", "Enfeksiyon Yolu"])
        
        with tab1:
            st.header("Ağ Görselleştirme ve Merkeziyet Analizi")
            
            col1, col2 = st.columns([2, 1])
            
            with col2:
                st.subheader("Ağ İstatistikleri")
                st.metric("Düğüm Sayısı", G.number_of_nodes())
                st.metric("Kenar Sayısı", G.number_of_edges())
                st.metric("Ortalama Derece", f"{sum(dict(G.degree()).values()) / G.number_of_nodes():.2f}")
                st.metric("Kümeleme Katsayısı", f"{nx.average_clustering(G):.4f}")
                
                if nx.is_connected(G):
                    st.metric("Çap (Diameter)", nx.diameter(G))
                else:
                    st.metric("Bağlantılı mı?", "Hayır")
                
                st.divider()
                
                st.subheader("Görselleştirme")
                view_mode = st.radio(
                    "Görünüm Modu:",
                    ["2D", "3D"],
                    horizontal=True
                )
                
                show_edges_3d = True
                if view_mode == "3D":
                    show_edges_3d = st.checkbox("Kenarları Göster", value=True)
                
                st.divider()
                
                if st.button("Merkeziyet Hesapla", type="primary", use_container_width=True):
                    with st.spinner("Merkeziyet ölçüleri hesaplanıyor..."):
                        centralities = calculate_all_centralities(G, use_approximation=False)
                        st.session_state.centralities = centralities
                        st.success("Hesaplandı")
                
                if st.session_state.centralities:
                    st.subheader("Merkeziyet Görselleştir")
                    cent_measure = st.selectbox(
                        "Merkeziyet Ölçüsü:",
                        ["degree", "betweenness", "closeness", "eigenvector"],
                        help="Farklı merkeziyet ölçülerini görselleştirin"
                    )
            
            with col1:
                # Ağ görselleştirme
                view_3d = (view_mode == "3D")
                
                if st.session_state.centralities and 'cent_measure' in locals():
                    centrality = st.session_state.centralities[cent_measure]
                    title = f"Network - {cent_measure.title()} Centrality ({view_mode})"
                    fig = plot_network_interactive(G, centrality=centrality, 
                                                   title=title, view_3d=view_3d, show_edges=show_edges_3d)
                else:
                    title = f"Network Graph ({view_mode})"
                    fig = plot_network_interactive(G, title=title, view_3d=view_3d, show_edges=show_edges_3d)
                
                
                st.plotly_chart(fig, width='stretch', use_container_width=True, key="network_analysis_chart")
                
                # En önemli düğümler
                if st.session_state.centralities:
                    st.subheader("En Yüksek Merkeziyete Sahip Düğümler")
                    
                    cols = st.columns(4)
                    for i, measure in enumerate(['degree', 'betweenness', 'closeness', 'eigenvector']):
                        with cols[i]:
                            st.markdown(f"**{measure.title()}**")
                            top_nodes = get_top_k_nodes_by_measure(st.session_state.centralities, measure, 5)
                            for j, node in enumerate(top_nodes, 1):
                                st.text(f"{j}. Node {node}")
        
        with tab2:
            st.header("Simülasyon Çalıştır")
            
            if st.button("Tüm Senaryoları Çalıştır", type="primary", use_container_width=True):
                
                progress_container = st.container()
                with progress_container:
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    status_icon = st.empty()
                
                try:
                    status_text.markdown("Merkeziyet ölçüleri hesaplanıyor...")
                    
                    runner = ExperimentRunner(G, beta, gamma, k_initial, n_runs)
                    progress_bar.progress(0.1)
                    
                    scenarios = ['random', 'degree', 'betweenness', 'closeness', 'eigenvector']
                    scenario_names = {
                        'random': 'Rastgele',
                        'degree': 'Derece',
                        'betweenness': 'Arasındalık',
                        'closeness': 'Yakınlık',
                        'eigenvector': 'Özdeğer'
                    }
                    
                    for i, scenario in enumerate(scenarios):
                        status_text.markdown(f"{scenario_names[scenario]} senaryosu çalıştırılıyor... ({i+1}/{len(scenarios)})")
                        
                        if scenario == 'random':
                            runner.run_random_scenario()
                        else:
                            runner.run_centrality_scenario(scenario)
                        
                        progress_bar.progress((i + 1) / len(scenarios))
                    
                    status_text.markdown("Tüm senaryolar tamamlandı")
                    progress_bar.progress(1.0)
                    
                    st.session_state.experiment_results = runner
                    st.success("Simülasyon tamamlandı. Sonuçlar sekmesine geçin.")
                    
                except Exception as e:
                    status_text.markdown("Hata oluştu")
                    st.error(f"Hata: {str(e)}")
                    import traceback
                    with st.expander("Detaylı Hata Bilgisi"):
                        st.code(traceback.format_exc())
        
        with tab3:
            st.header("Simülasyon Sonuçları")
            
            if st.session_state.experiment_results:
                runner = st.session_state.experiment_results
                plotting_data = runner.get_results_for_plotting()
                
                st.subheader("Özet Metrikler")
                
                cols = st.columns(len(plotting_data['scenarios']))
                for i, scenario in enumerate(plotting_data['scenarios']):
                    with cols[i]:
                        st.markdown(f"**{scenario.title()}**")
                        st.metric("Salgın Büyüklüğü", 
                                 f"{plotting_data['outbreak_sizes'][i]:.1f}",
                                 delta=f"±{plotting_data['outbreak_stds'][i]:.1f}")
                        st.metric("Peak Enfekte", 
                                 f"{plotting_data['peak_infecteds'][i]:.1f}",
                                 delta=f"±{plotting_data['peak_infected_stds'][i]:.1f}")
                        st.metric("Peak Zamanı", 
                                 f"{plotting_data['peak_times'][i]:.1f}",
                                 delta=f"±{plotting_data['peak_time_stds'][i]:.1f}")
                
                st.divider()
                
                st.subheader("Zaman Serisi Analizi")
                fig_ts = plot_time_series_interactive(plotting_data['time_series'], 
                                                      "SIR Model - Zaman Serisi Karşılaştırması")
                st.plotly_chart(fig_ts, width='stretch', key="time_series_chart")
                
                st.divider()
                
                st.subheader("Senaryo Karşılaştırması")
                fig_comp = plot_comparison_interactive(plotting_data)
                st.plotly_chart(fig_comp, width='stretch', key="comparison_chart")
                
                st.divider()
                
                st.subheader("En Etkili Stratejiler")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    max_idx = np.argmax(plotting_data['outbreak_sizes'])
                    st.success(f"**En Büyük Salgın:**\n\n{plotting_data['scenarios'][max_idx].title()}")
                    st.metric("Ortalama Enfekte", f"{plotting_data['outbreak_sizes'][max_idx]:.1f}")
                
                with col2:
                    max_idx = np.argmax(plotting_data['peak_infecteds'])
                    st.warning(f"**En Yüksek Peak:**\n\n{plotting_data['scenarios'][max_idx].title()}")
                    st.metric("Simultane Enfekte", f"{plotting_data['peak_infecteds'][max_idx]:.1f}")
                
                with col3:
                    min_idx = np.argmin(plotting_data['peak_times'])
                    st.info(f"**En Hızlı Yayılım:**\n\n{plotting_data['scenarios'][min_idx].title()}")
                    st.metric("Peak Zamanı", f"{plotting_data['peak_times'][min_idx]:.1f}")
                
            else:
                st.warning("Henüz simülasyon çalıştırılmadı. Simülasyon sekmesine gidin.")
        
        with tab4:
            st.header("Simülasyon Animasyonu")
            
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.subheader("Animasyon Parametreleri")
                
                anim_strategy = st.selectbox(
                    "Strateji Seçin:",
                    ["Random", "Degree", "Betweenness", "Closeness", "Eigenvector"]
                )
                
                anim_beta = st.slider("Beta (Bulaşma)", 0.0, 1.0, beta, 0.05, key="anim_beta")
                anim_gamma = st.slider("Gamma (İyileşme)", 0.0, 1.0, gamma, 0.05, key="anim_gamma")
                anim_k = st.slider("Başlangıç Enfekte", 1, min(10, G.number_of_nodes()//10), 3, key="anim_k")
                
                large_network = G.number_of_nodes() > 200
                
                if large_network:
                    st.info("200+ düğümlü ağlarda performans gerekçesiyle 3D animasyon desteklenmemektedir.")
                    anim_view_3d = st.checkbox("3D Görünüm", value=False, disabled=True)
                else:
                    anim_view_3d = st.checkbox("3D Görünüm", value=False)
                
                anim_show_edges = True
                if anim_view_3d and not large_network:
                    anim_show_edges = st.checkbox("Kenarları Göster", value=True, key="anim_show_edges")
                
                anim_speed = st.slider("Animasyon Hızı", 0.0, 1.0, 0.30, 0.05)
                
                max_steps = st.slider("Maksimum Adım", 10, 100, 50, 5)
                
                st.divider()
                
                metrics_placeholder = st.empty()
                
                if st.button("Animasyon Başlat", type="primary", use_container_width=True):
                    
                    with st.spinner("Hazırlanıyor..."):
                        if anim_strategy == "Random":
                            import random
                            random.seed(42)
                            initial_infected = random.sample(list(G.nodes()), anim_k)
                        else:
                            if not st.session_state.centralities:
                                with st.spinner("Merkeziyet hesaplanıyor..."):
                                    st.session_state.centralities = calculate_all_centralities(G)
                            
                            measure = anim_strategy.lower()
                            initial_infected = get_top_k_nodes_by_measure(
                                st.session_state.centralities, measure, anim_k
                            )
                        
                        model = SIRModel(G, anim_beta, anim_gamma, seed=42)
                        model.set_initial_infected(initial_infected)
                        
                        if anim_view_3d and not large_network:
                            if st.session_state.layout_3d is None:
                                iterations = 30 if G.number_of_nodes() > 100 else 50
                                st.session_state.layout_3d = spring_layout_3d(G, seed=42, k=0.5, iterations=iterations)
                    
                    with col2:
                        st.subheader("Ağ Durumu")
                        chart_placeholder = st.empty()
                        status_placeholder = st.empty()
                        
                        pos_3d = st.session_state.layout_3d if anim_view_3d else None
                        
                        S, I, R = model.get_state_counts()
                        title = f"t=0 | S:{S} I:{I} R:{R}"
                        fig = plot_network_interactive(G, model.states, title=title, view_3d=anim_view_3d, pos_3d=pos_3d, show_edges=anim_show_edges)
                        chart_placeholder.plotly_chart(fig, width='stretch', use_container_width=True)
                        
                        with metrics_placeholder:
                            col_s, col_i, col_r = st.columns(3)
                            with col_s:
                                st.metric("Susceptible", S)
                            with col_i:
                                st.metric("Infected", I)
                            with col_r:
                                st.metric("Recovered", R)
                        
                        for step in range(max_steps):
                            continues = model.step()
                            
                            S, I, R = model.get_state_counts()
                            
                            with metrics_placeholder:
                                col_s, col_i, col_r = st.columns(3)
                                with col_s:
                                    st.metric("Susceptible", S)
                                with col_i:
                                    st.metric("Infected", I, delta=I if step > 0 else None)
                                with col_r:
                                    st.metric("Recovered", R, delta=R if step > 0 else None)
                            
                            title = f"t={step+1} | S:{S} I:{I} R:{R}"
                            fig = plot_network_interactive(G, model.states, title=title, view_3d=anim_view_3d, pos_3d=pos_3d, show_edges=anim_show_edges)
                            chart_placeholder.plotly_chart(fig, width='stretch', use_container_width=True)
                            
                            if anim_speed > 0:
                                time.sleep(anim_speed)
                            
                            if I == 0:
                                status_placeholder.success(f"Simülasyon tamamlandı (Adım {step+1})")
                                break
                            elif step == 0:
                                status_placeholder.info(f"Simülasyon devam ediyor (Adım {step+1}/{max_steps})")
                            else:
                                status_placeholder.info(f"Simülasyon devam ediyor (Adım {step+1}/{max_steps}) | Enfekte: {I}")
                        
                        if I > 0:
                            status_placeholder.warning(f"Maksimum adım sayısına ulaşıldı ({max_steps} adım)")
                        
                        st.session_state.infection_history = model.infection_history.copy()
                        st.session_state.last_initial_infected = initial_infected.copy()
                        status_placeholder.info("Enfeksiyon yolu kaydedildi. 'Enfeksiyon Yolu' sekmesine geçin.")
            
            with col2:
                if 'model' not in locals():
                    st.subheader("Ağ Durumu")
                    
                    if st.session_state.centralities:
                        st.subheader("Önizleme")
                        preview_fig = plot_network_interactive(G, title="Ağ Önizlemesi", view_3d=False)
                        st.plotly_chart(preview_fig, width='stretch', use_container_width=True, key="preview_chart")
        
        with tab5:
            st.header("Enfeksiyon Yolu Takibi")
            
            if st.session_state.infection_history is None or st.session_state.last_initial_infected is None:
                st.info("Henüz enfeksiyon yolu kaydedilmedi. Animasyon sekmesinde bir simülasyon çalıştırın.")
            else:
                infection_history = st.session_state.infection_history
                initial_infected = st.session_state.last_initial_infected
                
                col1, col2 = st.columns([2, 1])
                
                with col2:
                    st.subheader("Görünüm Ayarları")
                    
                    view_mode_path = st.radio(
                        "Görünüm Modu:",
                        ["2D", "3D"],
                        horizontal=True,
                        key="path_view_mode"
                    )
                    
                    show_edges_path = True
                    if view_mode_path == "3D":
                        show_edges_path = st.checkbox("Kenarları Göster", value=True, key="path_show_edges")
                    
                    st.divider()
                    
                    st.subheader("İstatistikler")
                    total_infected = len(infection_history)
                    st.metric("Toplam Enfekte", total_infected)
                    st.metric("Başlangıç Enfekte", len(initial_infected))
                    
                    if infection_history:
                        max_time = max((time_step for _, (_, time_step) in infection_history.items()), default=0)
                        st.metric("En Geç Enfeksiyon Adımı", max_time)
                    
                    st.divider()
                    
                    st.subheader("Başlangıç Enfekte Node'lar")
                    for i, node in enumerate(initial_infected, 1):
                        st.text(f"{i}. Node {node}")
                
                with col1:
                    view_3d_path = (view_mode_path == "3D")
                    pos_3d_path = None
                    
                    if view_3d_path:
                        if st.session_state.layout_3d is None:
                            iterations = 30 if G.number_of_nodes() > 100 else 50
                            st.session_state.layout_3d = spring_layout_3d(G, seed=42, k=0.5, iterations=iterations)
                        pos_3d_path = st.session_state.layout_3d
                    
                    title = "Enfeksiyon Yolu Takibi - İlk Enfekte Node'lardan Tüm Ağa Yayılım"
                    fig_path = plot_infection_path(
                        G, 
                        infection_history, 
                        initial_infected, 
                        title=title,
                        view_3d=view_3d_path,
                        pos_3d=pos_3d_path,
                        show_edges=show_edges_path
                    )
                    st.plotly_chart(fig_path, width='stretch', use_container_width=True, key="infection_path_chart")
                    
                    st.markdown("""
                    **Renk Açıklaması:**
                    - 🔴 **Koyu Kırmızı**: Başlangıç enfekte node'lar (Patient Zero, t=0)
                    - 🟡 **Sarı**: Sonradan enfekte olan node'lar
                    - 🔵 **Mavi**: Enfekte olmayan node'lar
                    - **Kalın Kırmızı Çizgiler**: Enfeksiyon yolu (hangi node'dan hangi node'a geçti)
                    """)
    
    else:
        st.info("Lütfen sol menüden bir veri seti seçin veya oluşturun")


if __name__ == "__main__":
    main()

