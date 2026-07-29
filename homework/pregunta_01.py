# pylint: disable=line-too-long
"""
Escriba el codigo que ejecute la accion solicitada.
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd


def pregunta_01():
    """
    El archivo `files//shipping-data.csv` contiene información sobre los envios
    de productos de una empresa. Cree un dashboard estático en HTML que
    permita visualizar los siguientes campos:
    * `Warehouse_block`
    * `Mode_of_Shipment`
    * `Customer_rating`
    * `Weight_in_gms`
    El dashboard generado debe ser similar a este:
    https://github.com/jdvelasq/LAB_matplotlib_dashboard/blob/main/shipping-dashboard-example.png
    Para ello, siga las instrucciones dadas en el siguiente video:
    https://youtu.be/AgbWALiAGVo
    Tenga en cuenta los siguientes cambios respecto al video:
    * El archivo de datos se encuentra en la carpeta `data`.
    * Todos los archivos debe ser creados en la carpeta `docs`.
    * Su código debe crear la carpeta `docs` si no existe.
    """
    data_path = Path("files") / "shipping-data.csv"
    docs_path = Path("docs")
    docs_path.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(data_path)

    plt.style.use("seaborn-v0_8-whitegrid")
    colors_wh = ["#4C72B0", "#55A868", "#C44E52", "#8172B2", "#CCB974"]
    colors_mode = ["#4C72B0", "#55A868", "#C44E52"]

    # 1. Warehouse_block – bar chart
    fig, ax = plt.subplots(figsize=(6, 4))
    counts = df["Warehouse_block"].value_counts().sort_index()
    bars = ax.bar(
        counts.index, counts.values, color=colors_wh, edgecolor="black", linewidth=0.5
    )
    ax.set_title("Shipping per Warehouse Block", fontsize=14, fontweight="bold")
    ax.set_xlabel("Warehouse Block")
    ax.set_ylabel("Number of Shipments")
    for bar, v in zip(bars, counts.values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + max(counts.values) * 0.01,
            str(int(v)),
            ha="center",
            va="bottom",
            fontsize=9,
        )
    ax.set_ylim(0, counts.max() * 1.15)
    fig.tight_layout()
    fig.savefig(docs_path / "shipping_per_warehouse.png", dpi=120, bbox_inches="tight")
    plt.close(fig)

    # 2. Mode_of_Shipment – pie chart
    fig, ax = plt.subplots(figsize=(6, 4))
    mode_counts = df["Mode_of_Shipment"].value_counts()
    _, _, autotexts = ax.pie(
        mode_counts.values,
        labels=mode_counts.index,
        autopct="%1.1f%%",
        startangle=90,
        colors=colors_mode,
        explode=(0.02,) * len(mode_counts),
        textprops={"fontsize": 11},
    )
    for t in autotexts:
        t.set_fontsize(10)
        t.set_fontweight("bold")
    ax.set_title("Mode of Shipment", fontsize=14, fontweight="bold")
    fig.tight_layout()
    fig.savefig(docs_path / "mode_of_shipment.png", dpi=120, bbox_inches="tight")
    plt.close(fig)

    # 3. Customer_rating – bar chart
    fig, ax = plt.subplots(figsize=(6, 4))
    rating_counts = df["Customer_rating"].value_counts().sort_index()
    bars = ax.bar(
        rating_counts.index.astype(str),
        rating_counts.values,
        color="#4C72B0",
        edgecolor="black",
        linewidth=0.5,
    )
    ax.set_title("Customer Rating Distribution", fontsize=14, fontweight="bold")
    ax.set_xlabel("Customer Rating")
    ax.set_ylabel("Count")
    for bar, v in zip(bars, rating_counts.values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + max(rating_counts.values) * 0.01,
            str(int(v)),
            ha="center",
            va="bottom",
            fontsize=9,
        )
    ax.set_ylim(0, rating_counts.max() * 1.15)
    fig.tight_layout()
    fig.savefig(docs_path / "customer_rating.png", dpi=120, bbox_inches="tight")
    plt.close(fig)

    # 4. Weight_in_gms – histogram
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.hist(
        df["Weight_in_gms"],
        bins=40,
        color="#55A868",
        edgecolor="black",
        linewidth=0.4,
        alpha=0.85,
    )
    ax.set_title("Weight Distribution (grams)", fontsize=14, fontweight="bold")
    ax.set_xlabel("Weight (gms)")
    ax.set_ylabel("Frequency")
    fig.tight_layout()
    fig.savefig(docs_path / "weight_distribution.png", dpi=120, bbox_inches="tight")
    plt.close(fig)

    # HTML dashboard
    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Shipping Dashboard</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
            background: #f0f2f5;
            color: #333;
            padding: 20px;
        }
        header {
            text-align: center;
            margin-bottom: 30px;
            padding: 20px;
            background: linear-gradient(135deg, #1a237e, #283593);
            color: white;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }
        header h1 { font-size: 2rem; margin-bottom: 6px; }
        header p { opacity: 0.9; font-size: 1rem; }
        .dashboard {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 24px;
            max-width: 1200px;
            margin: 0 auto;
        }
        .card {
            background: white;
            border-radius: 12px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.08);
            padding: 16px;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .card:hover {
            transform: translateY(-3px);
            box-shadow: 0 6px 18px rgba(0,0,0,0.12);
        }
        .card img {
            width: 100%;
            height: auto;
            display: block;
            border-radius: 6px;
        }
        footer {
            text-align: center;
            margin-top: 40px;
            color: #777;
            font-size: 0.85rem;
        }
        @media (max-width: 768px) {
            .dashboard { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
    <header>
        <h1>Shipping Dashboard</h1>
        <p>Static overview of warehouse blocks, shipment modes, customer ratings and package weights</p>
    </header>

    <div class="dashboard">
        <div class="card">
            <img src="shipping_per_warehouse.png" alt="Shipping per Warehouse Block">
        </div>
        <div class="card">
            <img src="mode_of_shipment.png" alt="Mode of Shipment">
        </div>
        <div class="card">
            <img src="customer_rating.png" alt="Customer Rating Distribution">
        </div>
        <div class="card">
            <img src="weight_distribution.png" alt="Weight Distribution">
        </div>
    </div>

    <footer>
        Generated from files/shipping-data.csv &mdash; Matplotlib static dashboard
    </footer>
</body>
</html>
"""
    (docs_path / "index.html").write_text(html, encoding="utf-8")
