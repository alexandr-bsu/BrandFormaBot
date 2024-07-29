from typing import Any
from aiogram.types import CallbackQuery, Message

from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Button, Row, Back
from aiogram_dialog.widgets.text import Format, Const, Case
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog import Dialog, DialogManager
from src.bot.fsm.orderMarkFSM import OrderSG


async def on_dialog_start(start_data: Any, manager: DialogManager):
    manager.dialog_data['api_info'] = start_data
    manager.dialog_data['name'] = manager.event.from_user.first_name


async def order_mark_clicked(callback: CallbackQuery, button: Button, manager: DialogManager):
    if callback.data == 'bad_order':
        manager.dialog_data['reviewRequestText'] = 'Пожалуйста, напишите, что мы можем исправить'
        await manager.next()
    if callback.data == 'normal_order':
        manager.dialog_data['reviewRequestText'] = 'Пожалуйста, напишите, как мы можем стать лучше'
        await manager.next()

    if callback.data == 'good_order':
        await manager.switch_to(OrderSG.good_mark)



async def on_review_send(message: Message, widget: MessageInput, manager: DialogManager):
    await manager.done(result={'mark': manager.dialog_data['mark'], 'review': message.text})
    await message.answer('Спасибо за оставленный отзыв! Вы делаете нас лучше')


async def process_result(result: Any, dialog_manager: DialogManager):
    # Отправить на сервер ...
    return result


mark_window = Window(
    Format("{dialog_data[name]}, спасибо, что доверяете нам \n\n"
           "Пожалуйста, оцените работу нашей компании? \n\n"
           "😭 — Не понравилось\n😐 — Сложно сказать\n😊 — Понравилось\n"
           ),
    Row(
        Button(Const("😭"), id="bad_order", on_click=order_mark_clicked),
        Button(Const("😐"), id="normal_order", on_click=order_mark_clicked),
        Button(Const("😊"), id="good_order", on_click=order_mark_clicked)
    ),
    state=OrderSG.mark
)

review_window = Window(
    Format("{dialog_data[reviewRequestText]}"),
    MessageInput(func=on_review_send),
    Back(text=Const("Назад")),
    state=OrderSG.review
)


good_mark_window = Window(
    Const("Очень рады, что Вам понравилось, мы стараемся ради таких приятных моментов 😍\n\n"
          "Будем благодарны если также оставите небольшой отзыв по одной из следующих ссылок: \n\n"
          "+ https://instagram.com/brandforma03/\n"
          "+ https://2gis.ru/ulanude/firm/70000001006646937"),
    state=OrderSG.good_mark
)

mark_dialog = Dialog(
    mark_window,
    review_window,
    good_mark_window,
    on_start=on_dialog_start,
    on_close=process_result
)
