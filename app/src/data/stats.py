from fastapi import HTTPException
from data import async_db
from models.stats import ClickRequest


class StatsRepository:
    """
    Database clients for the app stats
    """
    async def register_click(self, socials: ClickRequest):
        """
        Register a click on the site
        """
        if socials.platform.lower() not in ["w", "g"]:
            raise HTTPException(status_code=400, detail="Invalid platform identifier")
        
        platform_map = {"W": "Whatsapp", "G": "Instagram"}
        platform_key = platform_map[socials.platform]

        # Ensure stats document exists
        stats = await async_db.stats.find_one({"name": "stats"})
        if not stats:
            stats = {
                "name": "stats",
                "number_of_click": {
                    "Whatsapp": 0,
                    "Instagram": 0
                }
            }
            await async_db.stats.insert_one(stats)
        
        # Update the click count
        await async_db.stats.update_one(
            {"name": "stats"},
            {"$inc": {f"number_of_click.{platform_key}": 1}}
        )

    async def get_number_of_clicks(self):
        """
        Get the number of clicks on the site
        """
        stats = await async_db.stats.find_one({"name": "stats"})
        
        if not stats:
            return {
                "whatsapp": 0,
                "Instagram": 0
            }
        
        # Extract and return the number_of_click dictionary
        return stats.get("number_of_click", {"whatsapp": 0, "Instagram": 0})