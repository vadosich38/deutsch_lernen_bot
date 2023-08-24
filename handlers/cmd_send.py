from set.dispatcher import my_disp
from aiogram import types
from configs.config import ADMIN
from configs.config import db_connection
from states.my_states import MyStatesGroup
from aiogram.dispatcher import FSMContext
from keyboards.confirm_ikb import confirm_ikb
from keyboards.choose_photo import choose_photo_ikb
from set.bot import my_bot
from operations.ads_sending_with_photo import sending_with_photo
from operations.ads_sending_withot_photo import sending_without_photo
from database.db_class import Database

NOT_ADMIN = "Рассылку может запустить только администратор. Вы не администратор!"
INSTRUCTION = "Теперь пришлите текст рассылки"
CONFIRM_INSTRUCTION = "Для продолжения подтвердите свой текст. Пришлите текст снова, если хотите его изменить" \
                      "\nВаше сообщение будет выглядеть вот так:"


@my_disp.message_handler(commands=["send"],
                         state="*")
async def cmd_send(message: types.Message):
    if ADMIN == message.from_user.id or Database.is_admin(user_id=message.from_user.id, conn=db_connection):
        await message.reply(text=INSTRUCTION)
        await MyStatesGroup.wait_text_to_send.set()
    else:
        await message.reply(text=NOT_ADMIN)


@my_disp.message_handler(lambda message: message.text,
                         lambda message: not message.text.startswith("/"),
                         state=MyStatesGroup.wait_text_to_send)
async def get_text(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["text"] = message.text
        await message.answer(text=CONFIRM_INSTRUCTION)
        await message.answer(data["text"],
                             reply_markup=confirm_ikb())


@my_disp.callback_query_handler(state=MyStatesGroup.wait_text_to_send,
                                text="CONFIRM")
async def get_confirm_callback(callback_data: types.CallbackQuery):
    await callback_data.answer(text="Текст сохранен!")
    await my_bot.send_message(chat_id=callback_data.from_user.id,
                              text="Хотите добавить фото?",
                              reply_markup=choose_photo_ikb())
    await MyStatesGroup.choose_photo_regim.set()


@my_disp.callback_query_handler(state=MyStatesGroup.choose_photo_regim)
async def get_regim_callback(callback_data: types.CallbackQuery,
                             state: FSMContext):
    if callback_data.data == "WITH PHOTO":
        await callback_data.answer(text="Рассылка поста с фото!")
        await my_bot.send_message(chat_id=callback_data.from_user.id,
                                  text="Теперь пришлите мне фото!")
        await MyStatesGroup.wait_photo_to_send.set()

    elif callback_data.data == "WITHOUT PHOTO":
        async with state.proxy() as data:
            await callback_data.answer(text="Рассылка началась!",
                                       show_alert=True)
            await sending_without_photo(author_id=callback_data.from_user.id,
                                        text=data["text"],
                                        regim="activ")
            await state.finish()


@my_disp.message_handler(lambda message: message.photo,
                         content_types="photo",
                         state=MyStatesGroup.wait_photo_to_send)
async def get_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["photo"] = message.photo[0].file_id

    await message.answer(text="Фото сохранено! Теперь нужно подтвердить корректность поста. Если вы хотите изменить "
                              "фото, пришлите новое фото"
                              "\nВаша рассылка будет выглядеть так:")
    await my_bot.send_photo(chat_id=message.from_user.id,
                            photo=data["photo"],
                            caption=data["text"],
                            reply_markup=confirm_ikb())


@my_disp.callback_query_handler(state=MyStatesGroup.wait_photo_to_send,
                                text="CONFIRM")
async def confirm_with_photo(callback_data: types.CallbackQuery, state: FSMContext):
    await callback_data.answer(text="Рассылка началась!",
                               show_alert=True)
    async with state.proxy() as data:
        await sending_with_photo(author_id=callback_data.from_user.id,
                                 photo_id=data["photo"],
                                 text=data["text"],
                                 regim="activ")
    await state.finish()


@my_disp.message_handler(lambda message: message.text,
                         state=MyStatesGroup.wait_text_to_send,
                         commands=["cancel"])
async def cmd_cancel_text(message: types.Message, state: FSMContext):
    await message.reply(text="Вы отменили рассылку!")
    await state.finish()


@my_disp.message_handler(lambda message: message.text,
                         state=MyStatesGroup.wait_photo_to_send,
                         commands=["cancel"])
async def cmd_cancel_photo(message: types.Message, state: FSMContext):
    await message.reply(text="Вы отменили рассылку!")
    await state.finish()


@my_disp.message_handler(lambda message: message.text,
                         state=MyStatesGroup.confirm_with_photo,
                         commands=["cancel"])
async def cmd_cancel_confirm_photo(message: types.Message, state: FSMContext):
    await message.reply(text="Вы отменили рассылку!")
    await state.finish()


@my_disp.message_handler(lambda message: message.text,
                         state=MyStatesGroup.choose_photo_regim,
                         commands=["cancel"])
async def cmd_cancel_choose(message: types.Message, state: FSMContext):
    await message.reply(text="Вы отменили рассылку!")
    await state.finish()
