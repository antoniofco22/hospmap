import tkinter as tk
import folium
import io
import geocoder
import math
import psycopg2
from decimal import Decimal
from tkhtmlview  import HTMLLabel

dbname = "sus"
user = "antoniofco"
password = "ck5XhvZgOw3q"
host = "ep-sweet-grass-79413934.us-east-2.aws.neon.tech"
port = "5432"

connection = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
cursor = connection.cursor()

def plotar_mapa():
	cont = 0;
	html_content= "";
	localizacoes_proximas = locationsdistancia();
	for loc in localizacoes_proximas:
		latitude1, longitude1 = loc[4],loc[5]
		latitude2, longitude2 = loc[1],loc[2]
		#print(latitude1," ",longitude1)
		#print(latitude2," ",longitude2)

		mapa = folium.Map(location=[latitude1, longitude1], zoom_start=15)

		folium.Marker([latitude1, longitude1], tooltip='Minha Localização').add_to(mapa)
		folium.Marker([latitude2, longitude2], tooltip='Alvo da Localização').add_to(mapa)

		linha = folium.PolyLine([(latitude1, longitude1), (latitude2, longitude2)], color='blue')
		linha.add_to(mapa)

		temp_map_file = "temp_map_"+str(cont)+".html"
		#print(temp_map_file)
		mapa.save(temp_map_file)
		nome = loc[0]
		html_content += "<a href='temp_map_"+str(cont)+".html'>Vá para o "+str(nome)+"</a><br>"
		cont+=1
	my_label = HTMLLabel(janela, html=html_content)
	my_label.pack(pady=20, padx=20)
	
	cursor.close()
	connection.close()

def locationsdistancia():
	g = geocoder.ip('me')
	if g.latlng:
		latitude, longitude = g.latlng
		if latitude and longitude:
			print(f"Latitude: {latitude}, Longitude: {longitude}")
	else:
		print("Não foi possível obter a localização.")

	minha_localizacao = (latitude, longitude)

	query = "SELECT CO_CNES, NU_LATITUDE, NU_LONGITUDE, NO_FANTASIA FROM locais_atendimento"
	cursor.execute(query)
	all_locations = cursor.fetchall()

	distancias = []
	for loc in all_locations:
		#print(loc[0], " ",loc[1], " ",loc[2])
		localizacao_bd = (float(loc[1]), float(loc[2]))  # Convertendo Decimal para float
		distancia = calcular_distancia_euclidiana(minha_localizacao, localizacao_bd)
		distancias.append((loc[3], loc[1], loc[2], distancia, latitude, longitude))

	distancias.sort(key=lambda x: x[1])

	localizacoes_proximas = distancias[:10]
	return localizacoes_proximas


def calcular_distancia_euclidiana(coord1, coord2):
	lat1, lon1 = coord1
	lat2, lon2 = coord2
	return math.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2)

janela = tk.Tk()
janela.title("Mapa com Coordenadas")


botao = tk.Button(janela, text="Me mostre os Mapas", command=plotar_mapa)
botao.pack()



janela.mainloop()
