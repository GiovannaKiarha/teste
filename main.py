import pandas as pd # utilizo novamente pois vou ter que manipular outro arquivo que no caso é o test.csv
from _initial_ import calcular_rota # importo a função criada no initial
import time


df = pd.read_csv('Python/test.csv') # puxo o arquivo que coloquei na mesma pasta do python
print(df.head()) # leio as 5 primeiras linhas


# 2. Criar DataFrame para os resultados
resultados = pd.DataFrame(columns=['row_id', 'tempo_viagem'])

for i in range (len(df)):
     x = calcular_rota (df.iloc[i]['start_lat'],df.iloc[i]['start_lng'], df.iloc[i]['end_lat'], df.iloc[i]['end_lng'])
     print(x)
     if x >= 2:
          break