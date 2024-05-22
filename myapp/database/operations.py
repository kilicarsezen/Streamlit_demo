# In database/operations.py
from .db import Session
from .models import InventoryHistory, InventoryComment, Material, Inventory, Location
from sqlalchemy import and_, func
from datetime import datetime

# In database/operations.py

def get_inventory_distribution(material_code, start_date, end_date):
    with Session() as session:
        results = session.query(
            InventoryHistory.date,
            Location.name.label('location'),
            func.sum(InventoryHistory.quantity).label('total_quantity')
        ).join(Inventory, InventoryHistory.inventory_id == Inventory.id
        ).join(Material, Inventory.material_id == Material.id
        ).join(Location, Inventory.location_id == Location.id
        ).filter(
            Material.code_number == material_code,
            InventoryHistory.date >= start_date,
            InventoryHistory.date <= end_date
        ).group_by(
            InventoryHistory.date,
            Location.name
        ).order_by(
            InventoryHistory.date
        ).all()

        return results


def get_high_inventory_materials(threshold):
    with Session() as session:
        high_inventory_items = session.query(
            Material.code_number,
            Material.description,
            func.sum(Inventory.quantity).label('total_quantity')
        ).join(Inventory, Inventory.material_id == Material.id
        ).group_by(Material.code_number, Material.description
        ).having(func.sum(Inventory.quantity) > threshold
        ).all()

        return high_inventory_items

def fetch_inventory_data():
    with Session() as session:
        data = session.query(
            InventoryHistory.date,
            Material.code_number,
            InventoryHistory.quantity
        ).join(Inventory, InventoryHistory.inventory_id == Inventory.id
        ).join(Material, Inventory.material_id == Material.id
        ).limit(10).all()
    return data

def get_existing_comment(material_selected, date_selected_str):
    with Session() as session:
        # Get the material
        material = session.query(Material).filter(Material.code_number == material_selected).first()
        if not material:
            return None

        # Parse the date string to a datetime object
        date_selected_dt = datetime.strptime(date_selected_str, '%Y-%m-%d').date()

        # Get all inventory history records for this material and date (comparing only the date part)
        inventory_histories = session.query(InventoryHistory).join(
            Inventory, InventoryHistory.inventory_id == Inventory.id
        ).filter(
            and_(
                Inventory.material_id == material.id,
                func.date(InventoryHistory.date) == date_selected_dt
            )
        ).all()

        # Find the latest comment from the retrieved inventory histories
        latest_comment = None
        for inv_hist in inventory_histories:
            print('inv_hist', inv_hist.id, inv_hist.quantity)
            comment = session.query(InventoryComment).filter(
                InventoryComment.inventory_history_id == inv_hist.id
            ).order_by(InventoryComment.timestamp.desc()).first()
            
            if comment and (not latest_comment or comment.timestamp > latest_comment.timestamp):
                print('comment', comment.id, comment.comment)
                latest_comment = comment

        return latest_comment

def save_comment(material_selected, date_selected_str, comment_text, existing_comment_id):
    with Session() as session:
        user_id = 1  # Placeholder for user ID, replace with actual logic to get the user ID

        # Get the material
        material = session.query(Material).filter(Material.code_number == material_selected).first()
        if not material:
            return "Material not found."

        # Parse the date string to a datetime object and get the date part
        date_selected_dt = datetime.strptime(date_selected_str, '%Y-%m-%d').date()

        # Find the InventoryHistory record for this material and date
        inventory_history = session.query(InventoryHistory).join(
            Inventory, InventoryHistory.inventory_id == Inventory.id
        ).filter(
            and_(
                Inventory.material_id == material.id,
                func.date(InventoryHistory.date) == date_selected_dt
            )
        ).first()

        if not inventory_history:
            return "Inventory history record not found."

        # Update or create the comment
        if existing_comment_id:
            existing_comment = session.query(InventoryComment).filter(InventoryComment.id == existing_comment_id).first()
            if existing_comment:
                existing_comment.comment = comment_text
            else:
                return "Existing comment not found."
        else:
            new_comment = InventoryComment(
                comment=comment_text, 
                user_id=user_id, 
                inventory_history_id=inventory_history.id
            )
            session.add(new_comment)

        session.commit()
        return "Success"
