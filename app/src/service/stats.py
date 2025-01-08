from models.stats import ClickRequest
from data.stats import StatsRepository

stats_repo = StatsRepository()

async def register_socials_click(socials: ClickRequest):
    """
    Register a click on the site
    """
    await stats_repo.register_click(socials)

async def get_clicks():
    """
    Get the number of clicks on the site
    """
    return await stats_repo.get_number_of_clicks()