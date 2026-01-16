
import psycopg2
from psycopg2 import sql

def create_user():
    try:
        # Connect to default postgres DB
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="1234",
            host="localhost"
        )
        conn.autocommit = True
        cur = conn.cursor()
        
        # Check if user exists
        cur.execute("SELECT 1 FROM pg_roles WHERE rolname='odoo19user'")
        if cur.fetchone():
            print("El usuario odoo19user ya existe.")
        else:
            # Create user
            cur.execute("CREATE USER odoo19user WITH PASSWORD 'odoo19pwd' CREATEDB")
            print("Usuario odoo19user creado exitosamente.")
            
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error creando usuario: {e}")

if __name__ == "__main__":
    create_user()
