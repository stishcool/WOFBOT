async def check_subscriptions(user_id, channels, bot):
    for channel in channels:
        chat_member = await bot.get_chat_member(chat_id=channel[2], user_id=user_id)
        if chat_member.status == 'left':
            return False
    return True
