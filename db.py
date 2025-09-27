import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Try to import MySQL connector with fallback
try:
    import mysql.connector
    from mysql.connector import Error
    MYSQL_AVAILABLE = True
    print("MySQL connector imported successfully")
except ImportError as e:
    print(f"MySQL connector import failed: {e}")
    MYSQL_AVAILABLE = False

# Database configuration
DB_CONFIG = {
    'host': os.getenv('MYSQL_HOST', 'localhost'),
    'database': 'fashion_stylist',
    'user': os.getenv('MYSQL_USER', 'root'),
    'password': os.getenv('MYSQL_PASSWORD', 'shreyash7710'),
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_unicode_ci'
}

def create_connection():
    """Create a database connection with error handling"""
    if not MYSQL_AVAILABLE:
        print("MySQL not available, skipping database connection")
        return None
    
    connection = None
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            print("Successfully connected to MySQL database")
            return connection
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        # Try connecting without specifying database (for initial setup)
        try:
            temp_config = DB_CONFIG.copy()
            temp_config.pop('database')
            connection = mysql.connector.connect(**temp_config)
            print("Connected to MySQL server (without database)")
            return connection
        except Error as e2:
            print(f"Failed to connect to MySQL server: {e2}")
    except Exception as e:
        print(f"Unexpected error connecting to database: {e}")
    
    return connection

def create_database():
    """Create the fashion_stylist database if it doesn't exist"""
    if not MYSQL_AVAILABLE:
        print("MySQL not available, skipping database creation")
        return False
    
    try:
        # Connect without specifying database
        temp_config = DB_CONFIG.copy()
        temp_config.pop('database')
        
        connection = mysql.connector.connect(**temp_config)
        cursor = connection.cursor()
        
        # Create database with proper charset
        create_db_query = """
        CREATE DATABASE IF NOT EXISTS fashion_stylist
        CHARACTER SET utf8mb4
        COLLATE utf8mb4_unicode_ci
        """
        cursor.execute(create_db_query)
        
        print("Database 'fashion_stylist' created or already exists")
        
        cursor.close()
        connection.close()
        return True
        
    except Error as e:
        print(f"Error creating database: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error creating database: {e}")
        return False

def create_tables():
    """Create the outfits table with proper error handling"""
    if not MYSQL_AVAILABLE:
        print("MySQL not available, skipping table creation")
        return False
    
    connection = create_connection()
    
    if connection is not None:
        try:
            cursor = connection.cursor()
            
            # Create table with better structure
            create_table_query = """
            CREATE TABLE IF NOT EXISTS outfits (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id VARCHAR(100) NOT NULL DEFAULT 'anonymous',
                detected_items JSON,
                ai_suggestions TEXT,
                shopping_links JSON,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                INDEX idx_user_id (user_id),
                INDEX idx_created_at (created_at)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """
            
            cursor.execute(create_table_query)
            connection.commit()
            print("Table 'outfits' created successfully")
            return True
            
        except Error as e:
            print(f"Error creating table: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error creating table: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
            if connection.is_connected():
                connection.close()
    
    return False

def save_outfit_analysis(user_id, detected_items, ai_suggestions, shopping_links):
    """Save outfit analysis to database with error handling"""
    if not MYSQL_AVAILABLE:
        print("MySQL not available, skipping database save")
        return None
    
    connection = create_connection()
    
    if connection is not None:
        try:
            cursor = connection.cursor()
            
            # Ensure user_id is not None or empty
            if not user_id or user_id.strip() == '':
                user_id = 'anonymous'
            
            insert_query = """
            INSERT INTO outfits (user_id, detected_items, ai_suggestions, shopping_links)
            VALUES (%s, %s, %s, %s)
            """
            
            # Prepare data - ensure JSON fields are strings
            record = (
                str(user_id)[:100],  # Limit user_id length
                str(detected_items) if detected_items else '[]',
                str(ai_suggestions) if ai_suggestions else '',
                str(shopping_links) if shopping_links else '[]'
            )
            
            cursor.execute(insert_query, record)
            connection.commit()
            
            outfit_id = cursor.lastrowid
            print(f"Outfit analysis saved successfully for user: {user_id}, ID: {outfit_id}")
            return outfit_id
            
        except Error as e:
            print(f"Error saving to database: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error saving to database: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
            if connection.is_connected():
                connection.close()
    
    return None

def get_user_outfits(user_id, limit=10):
    """Retrieve outfit history for a user"""
    if not MYSQL_AVAILABLE:
        print("MySQL not available, returning empty list")
        return []
    
    connection = create_connection()
    outfits = []
    
    if connection is not None:
        try:
            cursor = connection.cursor(dictionary=True)
            
            select_query = """
            SELECT * FROM outfits 
            WHERE user_id = %s 
            ORDER BY created_at DESC 
            LIMIT %s
            """
            
            cursor.execute(select_query, (user_id, limit))
            outfits = cursor.fetchall()
            
            print(f"Retrieved {len(outfits)} outfits for user: {user_id}")
            
        except Error as e:
            print(f"Error retrieving outfits: {e}")
        except Exception as e:
            print(f"Unexpected error retrieving outfits: {e}")
        finally:
            if cursor:
                cursor.close()
            if connection.is_connected():
                connection.close()
    
    return outfits

def get_outfit_by_id(outfit_id):
    """Retrieve a specific outfit by ID"""
    if not MYSQL_AVAILABLE:
        print("MySQL not available, returning None")
        return None
    
    connection = create_connection()
    outfit = None
    
    if connection is not None:
        try:
            cursor = connection.cursor(dictionary=True)
            
            select_query = "SELECT * FROM outfits WHERE id = %s"
            cursor.execute(select_query, (outfit_id,))
            outfit = cursor.fetchone()
            
            if outfit:
                print(f"Retrieved outfit ID: {outfit_id}")
            else:
                print(f"No outfit found with ID: {outfit_id}")
            
        except Error as e:
            print(f"Error retrieving outfit: {e}")
        except Exception as e:
            print(f"Unexpected error retrieving outfit: {e}")
        finally:
            if cursor:
                cursor.close()
            if connection.is_connected():
                connection.close()
    
    return outfit

def delete_outfit(outfit_id):
    """Delete an outfit record"""
    if not MYSQL_AVAILABLE:
        print("MySQL not available, cannot delete")
        return False
    
    connection = create_connection()
    
    if connection is not None:
        try:
            cursor = connection.cursor()
            
            delete_query = "DELETE FROM outfits WHERE id = %s"
            cursor.execute(delete_query, (outfit_id,))
            connection.commit()
            
            if cursor.rowcount > 0:
                print(f"Outfit {outfit_id} deleted successfully")
                return True
            else:
                print(f"No outfit found with ID {outfit_id}")
                return False
                
        except Error as e:
            print(f"Error deleting outfit: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error deleting outfit: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
            if connection.is_connected():
                connection.close()
    
    return False

def test_database_connection():
    """Test database connection and setup"""
    print("Testing database connection...")
    
    if not MYSQL_AVAILABLE:
        return False, "MySQL connector not available"
    
    try:
        connection = create_connection()
        if connection and connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            cursor.close()
            connection.close()
            
            if result:
                return True, "Database connection successful"
            else:
                return False, "Database query failed"
        else:
            return False, "Failed to connect to database"
            
    except Exception as e:
        return False, f"Database test error: {str(e)}"

def initialize_database():
    """Initialize the database and tables"""
    print("=== Initializing database ===")
    
    if not MYSQL_AVAILABLE:
        print("MySQL not available, skipping database initialization")
        return False
    
    try:
        # Step 1: Create database
        print("Creating database...")
        db_created = create_database()
        
        # Step 2: Create tables
        print("Creating tables...")
        tables_created = create_tables()
        
        # Step 3: Test connection
        print("Testing connection...")
        test_success, test_message = test_database_connection()
        
        if db_created and tables_created and test_success:
            print("✅ Database initialization complete!")
            return True
        else:
            print(f"⚠️ Database initialization partial. Test: {test_message}")
            return False
            
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        return False

if __name__ == "__main__":
    # Run this to set up the database
    print("=== Database Setup Script ===")
    initialize_database()
    
    # Test with sample data
    print("\n=== Testing with sample data ===")
    try:
        outfit_id = save_outfit_analysis(
            user_id="test_user",
            detected_items='[{"item": "test shirt", "color": "blue"}]',
            ai_suggestions="Test suggestions",
            shopping_links='[{"title": "Test product"}]'
        )
        
        if outfit_id:
            print(f"✅ Sample data saved with ID: {outfit_id}")
            
            # Test retrieval
            outfit = get_outfit_by_id(outfit_id)
            if outfit:
                print("✅ Sample data retrieved successfully")
            else:
                print("❌ Failed to retrieve sample data")
        else:
            print("❌ Failed to save sample data")
            
    except Exception as e:
        print(f"❌ Sample data test failed: {e}")
    
    print("\n=== Database setup complete ===")