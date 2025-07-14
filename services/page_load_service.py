from typing import Optional, Dict, Any
from services.property_service import property_service
from services.user_service import user_service
from schemas.property import PropertyQuery
from core.dependencies import get_current_user

class PageLoadService:
    async def get_home_data(self, user_info: dict = None) -> dict:
        """Get merged data for home page load"""
        try:
            # Get properties data
            property_query = PropertyQuery(MLS_TOP_LIMIT=10)
            properties_data = await property_service.search_properties(property_query)
            
            # Prepare response
            home_data = {
                "properties": properties_data.value,
                "user": user_info if user_info else None,
                "total_properties": len(properties_data.value)
            }
            
            return home_data
            
        except Exception as e:
            raise Exception(f"Failed to load home data: {str(e)}")

page_load_service = PageLoadService() 