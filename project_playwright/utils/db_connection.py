import mysql.connector
import yaml
from pathlib import Path

# Load database configuration
config_path = Path(__file__).parent.parent / "config" / "database.yaml"

with open(config_path, "r", encoding="utf-8") as f:
    db_config = yaml.safe_load(f)

db_settings = db_config["database"]

try:
    # Connect to MySQL
    connection = mysql.connector.connect(
        host=db_settings["host"],
        port=db_settings["port"],
        user=db_settings["username"],
        password=db_settings["password"],
        database=db_settings["database_name"]
    )

    cursor = connection.cursor()

    # Get all tables
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()

    print(f"\n{'='*80}")
    print(f"Database: {db_settings['database_name']}")
    print(f"{'='*80}\n")
    print(f"Total Tables: {len(tables)}\n")

    if tables:
        for i, table in enumerate(tables, 1):
            table_name = table[0]
            print(f"\n{i}. TABLE: {table_name}")
            print(f"{'-'*80}")

            # Get table structure
            cursor.execute(f"DESCRIBE {table_name}")
            columns = cursor.fetchall()
            column_names = [col[0] for col in columns]

            # Display column names
            header = " | ".join(column_names)
            print(header)
            print("-" * 80)

            # Get table data
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()

            if rows:
                for row in rows:
                    row_data = " | ".join(str(val) for val in row)
                    print(row_data)
                print(f"\nTotal rows in {table_name}: {len(rows)}")
            else:
                print("(No data in this table)")

            print(f"{'-'*80}")
    else:
        print("No tables found in the database.")

    print(f"\n{'='*80}\n")

    cursor.close()
    connection.close()

except mysql.connector.Error as err:
    print(f"Error: {err}")
except Exception as e:
    print(f"An error occurred: {e}")
