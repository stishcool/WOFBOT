from aiogram.utils.deep_linking import get_start_link

async def generate_referral_link(user_id):
    referral_link = await get_start_link(payload=user_id)
    return referral_link
