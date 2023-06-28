import csv
import psycopg2

# Database connection details
conn = psycopg2.connect(
    host="localhost",
    port=5433,
    dbname="metabase",
    user="metabase",
    password="metabase"
)
print("Connecting to Database")

# Path to the CSV file
csv_file_path = "metrics.csv"

# Extract table name from the CSV file name
table_name = csv_file_path.replace(".csv", "")

# Open the CSV file
with open(csv_file_path, "r") as file:
    reader = csv.reader(file)
    header = next(reader)  # Get the header row

    # Build the CREATE TABLE query.
    create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ("

    # Iterate over the header columns to create the table columns
    for column in header:
        if column in ['enrolled_students', 'course_id', 'weekly_active_users', 'daily_active_users']:
            create_table_query += f"{column} INTEGER, "
        elif column == 'date':
            create_table_query += f"{column} DATE, "
        else:
            create_table_query += f"{column} VARCHAR(255), "

    create_table_query = create_table_query.rstrip(", ")  # Remove the trailing comma and space
    create_table_query += ");"

    # Execute the CREATE TABLE query
    with conn.cursor() as cursor:
        cursor.execute(create_table_query)
        conn.commit()

    # Load the CSV data into the table
    with open(csv_file_path, "r") as file:
        reader = csv.DictReader(file)
        with conn.cursor() as cursor:
            for row in reader:
                # Build the INSERT query
                # NOTE: had to remove single quotes from CSV file because it messed with the script.

                insert_query = f"INSERT INTO {table_name} ({', '.join(header)}) VALUES ("

                # Iterate over the header columns to construct the INSERT query
                for column in header:
                    if column in ['enrolled_students', 'course_id', 'weekly_active_users', 'daily_active_users']:
                        if row[column] == '':
                            insert_query += f"{0}, "
                        else:
                            insert_query += f"{int(row[column])}, "
                    elif column == 'Date':
                        insert_query += f'TO_DATE("{row[column]}", "MM/DD/YY"), '
                    else:
                        insert_query += f"'{row[column]}', "

                insert_query = insert_query.rstrip(", ")  # Remove the trailing comma and space
                insert_query += ");"

                # Execute the INSERT query
                cursor.execute(insert_query)
                conn.commit()

# Close the database connection
conn.close()
print("Database connection closed.")
