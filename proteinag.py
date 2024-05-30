import pandas as pd
import plotly.graph_objects as go
import networkx as nx
import tkinter as tk
from tkinter import ttk

# Excel dosyasını oku
df = pd.read_excel("C:\\Users\\SoftwareQuenn\\Desktop\\deneme\\Bandyopadhyay2010.xls\\Bandyopadhyay2010.xls")

# Ağı oluştur
G = nx.from_pandas_edgelist(df, source='BAIT_OFFICIAL_SYMBOL', target='PREY_OFFICIAL_SYMBOL', edge_attr='EXPERIMENTAL_SYSTEM')

# Seçilebilecek protein listesi
protein_list = list(G.nodes())

# Tkinter uygulamasını oluştur
root = tk.Tk()
root.title("Protein Ağı Görüntüleyici")
root.geometry("240x240")  # Pencerenin boyutunu ayarla

# Dropdown menüsünü oluştur
protein_var = tk.StringVar(root)
protein_dropdown = ttk.Combobox(root, textvariable=protein_var, values=protein_list)
protein_dropdown.pack(pady=10)

# Callback fonksiyonu: Seçilen proteinin bağlantılı olduğu proteinlerle ağı göster
def show_network():
    selected_protein = protein_var.get()
    if selected_protein:
        # Seçilen proteinin 1 uzaklıktaki düğüm ile ağı göster
        subgraph = nx.ego_graph(G, selected_protein, radius=1)
        
        # Plotly için düğüm ve kenar listeleri
        node_positions = nx.spring_layout(subgraph)
        nodes = list(subgraph.nodes())
        edges = list(subgraph.edges())
        
        # Plotly grafiği oluştur
        fig = go.Figure()
        
        # Düğümleri ekle
        for node in nodes:
            # Node bilgilerini alın
            bait_info = df[df['BAIT_OFFICIAL_SYMBOL'] == node]
            prey_info = df[df['PREY_OFFICIAL_SYMBOL'] == node]

            if not bait_info.empty:
                bait_geneid = bait_info['BAIT_GENEID'].values[0]
                bait_symbol = node
                experimental_system = bait_info['EXPERIMENTAL_SYSTEM'].values[0]
            else:
                bait_geneid = "Yok"
                bait_symbol = node
                experimental_system = "Yok"

            if not prey_info.empty:
                prey_geneid = prey_info['PREY_GENE_ID'].values[0]
                prey_symbol = node
            else:
                prey_geneid = "Yok"
                prey_symbol = node

            # Tooltip metni oluştur
            text = (f"YEM_GEN_ID: {bait_geneid}<br>"
                    f"YEM_RESMI_SEMBOL: {bait_symbol}<br>"
                    f"AV_GEN_ID: {prey_geneid}<br>"
                    f"AV_RESMI_SEMBOL: {prey_symbol}<br>"
                    f"DENEYSEL_SISTEM: {experimental_system}")
            
            fig.add_trace(go.Scatter(x=[node_positions[node][0]], y=[node_positions[node][1]],
                                     mode='markers+text',
                                     marker=dict(size=10),
                                     text=[bait_symbol], hoverinfo='text', textposition="top center",
                                     hovertext=text, hoverlabel=dict(namelength=-1)))
        
        # Kenarları ekle
        for edge in edges:
            x0, y0 = node_positions[edge[0]]
            x1, y1 = node_positions[edge[1]]
            fig.add_trace(go.Scatter(x=[x0, x1, None], y=[y0, y1, None], mode='lines'))
        
        # Layout ayarları
        fig.update_layout(showlegend=False, hovermode='closest', title="{} Protein Ağı".format(selected_protein))
        
        # Grafiği göster
        fig.show()

# Buton oluştur
show_button = ttk.Button(root, text="Ağı Göster", command=show_network)
show_button.pack(pady=10)

# Tkinter döngüsünü başlat
root.mainloop()
