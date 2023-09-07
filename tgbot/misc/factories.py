from aiogram.utils.callback_data import CallbackData

for_reroll = CallbackData("reroll", "dice_value")
for_reroll_done = CallbackData("reroll_done", "action")
for_fool_player_turn = CallbackData("fool_player_turn", "card")
