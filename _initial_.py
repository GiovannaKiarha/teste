import pandas as pd # para manipulação dos dados
import osmnx as ox # biblioteca nova para cálculos 
from geopy.distance import great_circle  # Para cálculo de distância mais preciso envolvendo a terra

# Carregar os dados do arquivo csv
df = pd.read_csv('Python/train.csv')
print(df.head()) # ler as 5 primeiras linhas do banco para saber as colunas que tenho

def calcular_rota(start_lat: float, start_lng: float, end_lat: float, end_lng: float): # defini como float pois não são números precisos

    # Calcular distância em linha reta e o great circle leva em consideração a curvatura da terra
    distancia_euclidiana = ox.distance.great_circle(start_lat, start_lng, end_lat, end_lng)
    
    # Calcular distância usando fórmula de Haversine (mais precisa para a Terra). Tive que ir para o Google e documentação
    ponto_origem = (start_lat, start_lng)
    ponto_destino = (end_lat, end_lng)
    distancia_haversine = great_circle(ponto_origem, ponto_destino).km
    
    # Obter rota 
    try:
        # Carregar rede viária para a área 
        graph = ox.graph_from_bbox(
            max(start_lat, end_lat) + 0.1,
            min(start_lat, end_lat) - 0.1,
            max(start_lng, end_lng) + 0.1,
            min(start_lng, end_lng) - 0.1,
            network_type='drive' # tipo de via. Se é carro, avião e afins
        )
        
        # Encontrar nós mais próximos pq o ox trabalha com interseções e ruas, daí pega as br mais próximas
        origem_node = ox.distance.nearest_nodes(graph, start_lng, start_lat)
        destino_node = ox.distance.nearest_nodes(graph, end_lng, end_lat)
        
        # Calcular rota mais curta
        rota = ox.shortest_path(graph, origem_node, destino_node, weight='length') # lenght é para as distâncias das ruas
        
        # Calcular distância da rota. Vai somar tudo e transformar em km. Se não encontrar, retorna none
        if rota:
            distancia_rota = sum(ox.utils_graph.get_route_edge_attributes(graph, rota, 'length'))/1000  # em km
        else:
            distancia_rota = None
    except Exception as e:
        print(f"Erro ao calcular rota: {e}")
        rota = None
        distancia_rota = None
    
    return {
        "distancia_euclidiana_km": distancia_euclidiana,
        "distancia_haversine_km": distancia_haversine,
        "distancia_rota_km": distancia_rota,
        "rota": rota
    }
