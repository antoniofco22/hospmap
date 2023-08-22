import psycopg2

dbname = "sus"
user = "antoniofco"
password = "ck5XhvZgOw3q"
host = "ep-sweet-grass-79413934.us-east-2.aws.neon.tech"
port = "5432"

print('Ver Registros ou Contagem(y/n):')
x = input()
if x=='y':
	try:
		connection = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
		cursor = connection.cursor()

		select_query = "SELECT co_cnes, no_fantasia, nu_latitude, nu_longitude FROM locais_atendimento"
		cursor.execute(select_query)
		records = cursor.fetchall()

		print("Registros na tabela:")
		for record in records:
			co_cnes, no_fantasia, nu_latitude, nu_longitude = record
			print(f"CO_CNES: {co_cnes}, Fantasia: {no_fantasia}, Latitude: {nu_latitude}, Longitude: {nu_longitude}")

	except (Exception, psycopg2.Error) as error:
		print("Erro ao conectar ou consultar dados:", error)
	finally:
		if connection:
			cursor.close()
			connection.close()
			print("Conexão fechada.")

else:
	try:
		connection = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
		cursor = connection.cursor()

		count_query = "SELECT COUNT(*) FROM locais_atendimento"
		cursor.execute(count_query)
		count = cursor.fetchone()[0]

		print(f"Total de registros na tabela locais_atendimento: {count}/496226")

	except (Exception, psycopg2.Error) as error:
		print("Erro ao conectar ou executar consulta:", error)
	finally:
		if connection:
			cursor.close()
			connection.close()
			print("Conexão fechada.")
