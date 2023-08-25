import pandas as pd
import psycopg2

dbname = "sus"
user = "antoniofco"
password = "ck5XhvZgOw3q"
host = "ep-sweet-grass-79413934.us-east-2.aws.neon.tech"
port = "5432"

# Your connection details here

csv_file = "cnes_estabelecimentos.csv"
batch_size = 1000
columns_to_read = ["CO_CNES", "NO_FANTASIA", "NU_LATITUDE", "NU_LONGITUDE"]
progress_file = "progress.txt"  # File to store progress information

connection = None

try:
    connection = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
    cursor = connection.cursor()

    # Load progress if available
    try:
        with open(progress_file, 'r') as progress:
            last_processed = int(progress.read())
    except FileNotFoundError:
        last_processed = 0

    with open(csv_file, 'r', encoding="latin-1") as file:
        next(file)
        inserted_count = last_processed

        batch_data = []

        for idx, line in enumerate(file):
            if idx < last_processed:
                continue

            data = line.strip().split(";")
            co_cnes = data[0]
            no_fantasia = data[6]
            nu_latitude = data[21]
            nu_longitude = data[22]

            if pd.notna(nu_latitude) and pd.notna(nu_longitude) and nu_latitude != "" and nu_longitude != "":
                select_query = f"SELECT co_cnes FROM locais_atendimento WHERE co_cnes = {co_cnes}"
                cursor.execute(select_query)
                existing_record = cursor.fetchone()

                if not existing_record:
                    batch_data.append((co_cnes, no_fantasia, nu_latitude, nu_longitude))
                    inserted_count += 1

                    if len(batch_data) >= batch_size:
                        insert_query = "INSERT INTO locais_atendimento(co_cnes, no_fantasia, nu_latitude, nu_longitude) VALUES (%s, %s, %s, %s)"
                        cursor.executemany(insert_query, batch_data)
                        connection.commit()
                        print(f"Inserted {inserted_count} records")

                        # Save progress
                        with open(progress_file, 'w') as progress:
                            progress.write(str(idx + 1))  # +1 to account for 0-based index

                        # Clear batch data for the next batch
                        batch_data = []

        # Insert any remaining records in the last batch
        if batch_data:
            insert_query = "INSERT INTO locais_atendimento(co_cnes, no_fantasia, nu_latitude, nu_longitude) VALUES (%s, %s, %s, %s)"
            cursor.executemany(insert_query, batch_data)
            connection.commit()
            print(f"Inserted {inserted_count} records")

    print("Data insertion completed")

except (Exception, psycopg2.Error) as error:
    print("Error connecting or inserting data:", error)
finally:
    if connection:
        cursor.close()
        connection.close()
        print("Connection closed.")
