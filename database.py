import sqlite3


conn = sqlite3.connect('real_estate.db')
cursor = conn.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS listings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    price REAL NOT NULL,
    city TEXT NOT NULL,
    address TEXT,
    image1 TEXT,
    image2 TEXT,
    image3 TEXT,
    image4 TEXT,
    image5 TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()
conn.close()


def create_object(title, description, price, city, address, image1, image2, image3, image4, image5):
    try:
        conn = sqlite3.connect('real_estate.db')
        cursor = conn.cursor()

        cursor.execute("""
    INSERT INTO listings (title, description, price, city, address, image1, image2, image3, image4, image5)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (title, description, price, city, address, image1, image2, image3, image4, image5))
        conn.commit()

    except Exception as e:
        print(f"Error inserting object: {e}")
    finally:
        conn.close()


# Async wrapper for sync function
# async def create_object(title, description, price, city, address, image1, image2, image3, image4, image5):
#    loop = asyncio.get_event_loop()
#    # Run the sync function in an executor (separate thread)
#    await loop.run_in_executor(None, create_object_sync, title, description, price, city, address, image1, image2, image3, image4, image5)
