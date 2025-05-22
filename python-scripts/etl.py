import pandas as pd
import psycopg2

print("🚀 Starting ETL")

# 1. Extract
url = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-01.parquet"
df = pd.read_parquet(url)

# 2. Transform
df = df[["tpep_pickup_datetime", "tpep_dropoff_datetime", "passenger_count", "trip_distance"]]
df = df.sample(10000, random_state=42)

# Drop rows with null or non-numeric values
df = df.dropna(subset=["tpep_pickup_datetime", "tpep_dropoff_datetime", "passenger_count", "trip_distance"])

# Convert to correct types to ensure compatibility
df["passenger_count"] = df["passenger_count"].astype(int)
df["trip_distance"] = df["trip_distance"].astype(float)


# 3. Load
try:
    conn = psycopg2.connect(
        host="postgres",
        user="root",
        password="root",
        dbname="yellow_taxi"
    )
    cur = conn.cursor()

    cur.execute("""
    DROP TABLE IF EXISTS trips;
    CREATE TABLE trips (
        id SERIAL PRIMARY KEY,
        pickup TIMESTAMP,
        dropoff TIMESTAMP,
        passengers SMALLINT,
        distance DOUBLE PRECISION
    );
    """)

    for _, row in df.iterrows():
        cur.execute(
            "INSERT INTO trips (pickup, dropoff, passengers, distance) VALUES (%s, %s, %s, %s)",
            (row["tpep_pickup_datetime"], row["tpep_dropoff_datetime"], row["passenger_count"], row["trip_distance"])
        )

    conn.commit()
    print("✅ ETL complete!")

except Exception as e:
    print(f"❌ ETL error: {e}")

finally:
    cur.close()
    conn.close()
