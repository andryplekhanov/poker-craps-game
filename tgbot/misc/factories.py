from aiogram.utils.callback_data import CallbackData

for_reroll = CallbackData("reroll", "dice_value")
for_reroll_done = CallbackData("reroll_done", "action")
for_fool_player_turn = CallbackData("fool_player_turn", "card", 'action')
for_fool_player_cover = CallbackData("fool_player_cover", "card")
for_fool_propose_more_cards_done = CallbackData("fool_propose_more_cards_done", 'action')
