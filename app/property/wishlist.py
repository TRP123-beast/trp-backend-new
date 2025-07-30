from fastapi import APIRouter, HTTPException, Depends
from typing import List
from uuid import UUID
from app.auth.deps import get_current_user
from app.property.models import PropertyDetail
from app.property.clients import mls_client

router = APIRouter(tags=["wishlist"])

# In-memory wishlist storage (replace with database in production)
user_wishlists = {}

@router.post("/add/{property_id}")
async def add_to_wishlist(property_id: str, current_user: str = Depends(get_current_user)):
    """Add a property to user's wishlist"""
    try:
        # Get property details
        select_fields = "BathroomsTotalInteger,BedroomsTotal,BuildingAreaTotal,City,CityRegion,CrossStreet,ListingKey,ListPrice,ParkingSpaces,UnparsedAddress"
        property_detail = await mls_client.get_property_by_id(property_id, select_fields)
        
        # Initialize wishlist if it doesn't exist
        if current_user not in user_wishlists:
            user_wishlists[current_user] = []
        
        # Check if property already in wishlist
        if property_id not in [item.ListingKey for item in user_wishlists[current_user]]:
            user_wishlists[current_user].append(property_detail)
            return {"message": f"Property {property_id} added to wishlist", "wishlist_count": len(user_wishlists[current_user])}
        else:
            return {"message": "Property already in wishlist", "wishlist_count": len(user_wishlists[current_user])}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[PropertyDetail])
async def get_wishlist(current_user: str = Depends(get_current_user)):
    """Get user's wishlist"""
    return user_wishlists.get(current_user, [])

@router.delete("/remove/{property_id}")
async def remove_from_wishlist(property_id: str, current_user: str = Depends(get_current_user)):
    """Remove a property from user's wishlist"""
    if current_user in user_wishlists:
        user_wishlists[current_user] = [item for item in user_wishlists[current_user] if item.ListingKey != property_id]
        return {"message": f"Property {property_id} removed from wishlist", "wishlist_count": len(user_wishlists[current_user])}
    return {"message": "Wishlist is empty"}

@router.delete("/clear")
async def clear_wishlist(current_user: str = Depends(get_current_user)):
    """Clear user's wishlist"""
    if current_user in user_wishlists:
        user_wishlists[current_user] = []
        return {"message": "Wishlist cleared"}
    return {"message": "Wishlist is already empty"}

@router.post("/move-to-cart/{property_id}")
async def move_to_cart(property_id: str, current_user: str = Depends(get_current_user)):
    """Move a property from wishlist to cart"""
    # This would integrate with the cart functionality
    # For now, just remove from wishlist
    if current_user in user_wishlists:
        user_wishlists[current_user] = [item for item in user_wishlists[current_user] if item.ListingKey != property_id]
        return {"message": f"Property {property_id} moved to cart", "wishlist_count": len(user_wishlists[current_user])}
    return {"message": "Wishlist is empty"} 