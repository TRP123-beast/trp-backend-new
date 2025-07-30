from fastapi import APIRouter, HTTPException, Depends
from typing import List
from uuid import UUID
from app.auth.deps import get_current_user
from app.property.models import PropertyDetail
from app.property.clients import mls_client

router = APIRouter(tags=["cart"])

# In-memory cart storage (replace with database in production)
user_carts = {}

@router.post("/add/{property_id}")
async def add_to_cart(property_id: str, current_user: str = Depends(get_current_user)):
    """Add a property to user's cart"""
    try:
        # Get property details
        select_fields = "BathroomsTotalInteger,BedroomsTotal,BuildingAreaTotal,City,CityRegion,CrossStreet,ListingKey,ListPrice,ParkingSpaces,UnparsedAddress"
        property_detail = await mls_client.get_property_by_id(property_id, select_fields)
        
        # Initialize cart if it doesn't exist
        if current_user not in user_carts:
            user_carts[current_user] = []
        
        # Check if property already in cart
        if property_id not in [item.ListingKey for item in user_carts[current_user]]:
            user_carts[current_user].append(property_detail)
            return {"message": f"Property {property_id} added to cart", "cart_count": len(user_carts[current_user])}
        else:
            return {"message": "Property already in cart", "cart_count": len(user_carts[current_user])}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[PropertyDetail])
async def get_cart(current_user: str = Depends(get_current_user)):
    """Get user's cart"""
    return user_carts.get(current_user, [])

@router.delete("/remove/{property_id}")
async def remove_from_cart(property_id: str, current_user: str = Depends(get_current_user)):
    """Remove a property from user's cart"""
    if current_user in user_carts:
        user_carts[current_user] = [item for item in user_carts[current_user] if item.ListingKey != property_id]
        return {"message": f"Property {property_id} removed from cart", "cart_count": len(user_carts[current_user])}
    return {"message": "Cart is empty"}

@router.delete("/clear")
async def clear_cart(current_user: str = Depends(get_current_user)):
    """Clear user's cart"""
    if current_user in user_carts:
        user_carts[current_user] = []
        return {"message": "Cart cleared"}
    return {"message": "Cart is already empty"} 