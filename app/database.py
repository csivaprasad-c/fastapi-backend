# import json
import sqlite3
from typing import Any
from contextlib import contextmanager

from app.schemas import ShipmentCreate, ShipmentPatch, ShipmentStatus, ShipmentUpdate

class Database:
    # def __init__(self):
    #     self.create_table("shipments")

    def connect_to_db(self):
        self.connection = sqlite3.connect("shipments.db", check_same_thread=False)
        self.cursor = self.connection.cursor()

    def create_table(self, name: str):
        self.cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {name} (
                id INTEGER PRIMARY KEY,
                weight REAL,
                content TEXT,
                status TEXT,
                destination INTEGER
            )
        """)
    
    def create(self, shipment: ShipmentCreate):
        self.cursor.execute("""
            INSERT INTO shipments (weight, content, status, destination)
            VALUES (?, ?, ?, ?)
        """, (
            shipment.weight,
            shipment.content,
            ShipmentStatus.placed.value,
            shipment.destination
        ))
        self.connection.commit()
        return {"id": self.cursor.lastrowid}
    
    def get(self, shipment_id: int) -> dict[str, Any] | None:
        self.cursor.execute("""
            SELECT * FROM shipments WHERE id = ?
        """, (shipment_id,))
        row = self.cursor.fetchone()

        if not row:
            return None
        
        return {
            "id": row[0],
            "weight": row[1],
            "content": row[2],
            "status": row[3],
            "destination": row[4]
        }
    
    def update(self, shipment_id: int, shipment: ShipmentUpdate):
        self.cursor.execute("""
            UPDATE shipments
            SET weight = ?, content = ?, status = ?, destination = ?
            WHERE id = ?
        """, (
            shipment.weight,
            shipment.content,
            shipment.status.value,
            shipment.destination,
            shipment_id
        ))
        self.connection.commit()
        return self.get(shipment_id)
    
    def patch(self, shipment_id: int, shipment: ShipmentPatch):
        existing_shipment = self.get(shipment_id)

        if existing_shipment is None:
            return None
        
        updated_shipment = {
            "weight": shipment.weight or existing_shipment["weight"],
            "content": shipment.content or existing_shipment["content"],
            "status": shipment.status.value if shipment.status else existing_shipment["status"],
            "destination": shipment.destination or existing_shipment["destination"]
        }

        print(updated_shipment)

        self.cursor.execute("""
            UPDATE shipments
            SET weight = ?, content = ?, status = ?, destination = ?
            WHERE id = ?
        """, (
            updated_shipment["weight"],
            updated_shipment["content"],
            updated_shipment["status"],
            updated_shipment["destination"],
            shipment_id
        ))
        self.connection.commit()
        return self.get(shipment_id)
    
    def delete(self, shipment_id: int):
        self.cursor.execute("""
            DELETE FROM shipments WHERE id = ?
        """, (shipment_id,))
        self.connection.commit()

    def close(self):
        self.connection.close()
    
    def __enter__(self):
        self.connect_to_db()
        self.create_table("shipments")
        return self
    
    def __exit__(self, *arg):
        self.close()
        
@contextmanager
def managed_db():
    db = Database()
    db.connect_to_db()
    db.create_table("shipments")

    yield db

    db.close()

with managed_db() as db:
    print(db.get(2))

# shipments = {}

# with open("shipments.json", "r") as f:
#     data = json.load(f)
#     for shipment in data:
#         shipments[shipment["id"]] = {
#             "weight": shipment["weight"],
#             "content": shipment["content"],
#             "status": shipment["status"],
#             "destination": shipment["destination"]
#         }

# def save():
#     with open("shipments.json", "w") as f:
#         json.dump(
#             list(shipments.values()),
#             f,
#         )