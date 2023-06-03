from aiogram import executor

from .dispatcher import dp

import bot.bot_script

executor.start_polling(dp, skip_updates=True)