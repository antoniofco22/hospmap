import pandas as pd
import psycopg2

dbname = "sus"
user = "antoniofco"
password = "ck5XhvZgOw3q"
host = "ep-sweet-grass-79413934.us-east-2.aws.neon.tech"
port = "5432"

csv_file = "cnes_estabelecimentos.csv"
columns_to_read = ["CO_CNES", "NO_FANTASIA", "NU_LATITUDE", "NU_LONGITUDE"]

try:
	connection = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
	cursor = connection.cursor()

	with open(csv_file, 'r', encoding="utf-8") as file:
		next(file)  # Pula a linha de cabeçalho
		for line in file:
			data = line.strip().split(";")
			co_cnes = data[0]
			no_fantasia = data[6]
			nu_latitude = data[21]
			nu_longitude = data[22]
			#print(nu_latitude, ' ', nu_longitude)
			#print(nu_latitude=="")
			#print(pd.notna(nu_latitude))
			if pd.notna(nu_latitude) and pd.notna(nu_longitude)  and nu_latitude!="" and nu_longitude!="":
				select_query = f"SELECT co_cnes FROM locais_atendimento WHERE co_cnes = {co_cnes}"
				cursor.execute(select_query)
				existing_record = cursor.fetchone()

				if not existing_record:
					insert_query = f"INSERT INTO locais_atendimento(co_cnes, no_fantasia, nu_latitude, nu_longitude) VALUES ({co_cnes}, '{no_fantasia}', {nu_latitude}, {nu_longitude})"
					cursor.execute(insert_query)
					connection.commit()  # Inserção imediata

	print("Dados inseridos com sucesso")

except (Exception, psycopg2.Error) as error:
	print("Erro ao conectar ou inserir dados:", error)
finally:
	if connection:
		cursor.close()
		connection.close()
		print("Conexão fechada.")
