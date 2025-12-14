import mysql.connector
from mysql.connector import Error

def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            port=3306,
            user='root',
            password='root',
            database='welvision_db'
        )
        if connection.is_connected():
            print("Successfully connected to the MySQL database")
            return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def create_tables(connection):
    try:
        cursor = connection.cursor()

        # Create ai_models table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ai_models (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL UNIQUE,
                path VARCHAR(500) NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                is_active TINYINT(1) DEFAULT 1
            )
        """)

        # Create datasets table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS datasets (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL UNIQUE,
                path VARCHAR(500) NOT NULL,
                description TEXT,
                image_count INT DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                is_active TINYINT(1) DEFAULT 1
            )
        """)

        connection.commit()
        print("All tables created successfully")

    except Error as e:
        print(f"Error creating tables: {e}")
    finally:
        cursor.close()

def main():
    connection = connect_to_database()
    if connection:
        create_tables(connection)
        connection.close()
        print("Database connection closed")

if __name__ == "__main__":
    main()