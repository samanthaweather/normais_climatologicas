import fileinput
import numpy
import pandas as pd
import matplotlib.pyplot as plt
from geopy.geocoders import Nominatim
import folium
from folium import IFrame
import base64

geolocator = Nominatim(user_agent="name")

# funções
def transpor(matriz):
    etset=numpy.transpose(matriz)
    return etset

def plota_barra(dataframe,limite_y,cidade,UF,codigo):
    #plt.figure(figsize=(2,1))
    dataframe.plot.bar()
    plt.ylim(0, limite_y)
    plt.xlabel("meses")
    plt.ylabel("Precipitação média (mm)")
    plt.legend().remove()
    plt.title(f"Normal Climatológica 1991-2020 - Precipitação \n {cidade} - {UF} - {codigo}")
    plt.tight_layout()
    plt.savefig(f"{cidade}.png")
    plt.close()
    return

################################
df = pd.read_csv("normais91-20.csv")
#print (df)

meses=['janeiro','fevereiro','março','abril','maio','junho','julho','agosto','setembro','outubro','novembro','dezembro']
meses2=['1','2','3','4','5','6','7','8','9','10','11','12']

df ['janeiro']=df['jan1']+df['jan2']+df['jan3']
df ['fevereiro']=df['fev1']+df['fev2']+df['fev3']
df ['marco']=df['mar1']+df['mar2']+df['mar3']
df ['abril']=df['abr1']+df['abr2']+df['abr3']
df ['maio']=df['mai1']+df['mai2']+df['mai3']
df ['junho']=df['jun1']+df['jun2']+df['jun3']
df ['julho']=df['jul1']+df['jul2']+df['jul3']
df ['agosto']=df['ago1']+df['ago2']+df['ago3']
df ['setembro']=df['set1']+df['set2']+df['set3']
df ['outubro']=df['out1']+df['out2']+df['out3']
df ['novembro']=df['nov1']+df['nov2']+df['nov3']
df ['dezembro']=df['dez1']+df['dez2']+df['dez3']

linhas=len(df.index)
limitey=df[['janeiro','fevereiro','marco','abril','maio','junho','julho','agosto','setembro','outubro','novembro','dezembro']].max().max()

#Criando mapa
brasil_chuva = folium.Map(
    zoom_start=4,
    location=[-10.133932434766733, -48.103938729508073])
brasil_chuva



i=1
for i in range(2):
 teste=df.loc[i:i,'janeiro':'dezembro']
 cidade=df.loc[i:i,'Estacao']
 UF=df.loc[i:i,'UF']
 codigo=df.loc[i:i,'Codigo']

 print (f"{cidade[i]}-{UF[i]}-Brasil")
 latitude= geolocator.geocode(f"{cidade[i]}-{UF[i]}-Brasil").latitude
 longitude= geolocator.geocode(f"{cidade[i]}-{UF[i]}-Brasil").longitude

 df2=pd.DataFrame(data=transpor(teste))
 plota_barra(df2,limitey,cidade[i],UF[i],codigo[i])

 png = f"{cidade[i]}.png".format()   
 encoded = base64.b64encode(open(png, 'rb').read())

 html = '<img src="data:image/png;base64,{}">'.format
 iframe = IFrame(html(encoded.decode('UTF-8')), width=700, height=500)
 popup = folium.Popup(iframe, max_width=2650)

 folium.Marker(location=[latitude, longitude],popup=popup).add_to(brasil_chuva)
 brasil_chuva.save('brasil_chuva.html')




