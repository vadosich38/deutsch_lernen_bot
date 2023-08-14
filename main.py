from aiogram import executor
from set.dispatcher import my_disp

from handlers.start import cmd_start
from handlers.regims import noun_chang_state, verb_chang_state
from handlers.regims import noun_answer
from handlers.regims import verb_answer
from handlers.callback_preteritum import callback_preteritum
from handlers.callback_presens import callback_presens


async def on_startup(_):
    print("Бот успешно запущен")


if __name__ == "__main__":
    executor.start_polling(dispatcher=my_disp,
                           on_startup=on_startup,
                           skip_updates=True)
