import random

def choose_game(games, user_id):
    """
    Выбирает игру на основе вероятности.

    :param games: список игр, каждая игра - словарь с ключами 'game_text' и 'probability'
    :param user_id: ID пользователя (может использоваться для настройки вероятностей)
    :return: выбранная игра
    """
    total_probability = sum(game['probability'] for game in games)
    rand_val = random.uniform(0, total_probability)
    cumulative = 0
    for game in games:
        cumulative += game['probability']
        if rand_val <= cumulative:
            return game
    return games[-1]  # на случай, если что-то пошло не так
