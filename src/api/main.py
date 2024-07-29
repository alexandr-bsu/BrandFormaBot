from typing import Union, Any, Annotated

from fastapi import FastAPI, Depends
import uvicorn

from aiogram_dialog import StartMode, ShowMode
from src.bot.main import bot
from src.bot.fsm.orderMarkFSM import OrderSG
from src.bot.main import bg_manager
from src.api.schemas.Telegram import Chat
from src.api.schemas.Order import Order
from src.api.utils import get_token

app = FastAPI(root_path='/api')


@app.post('/requestOrderMark')
async def send_order_mark_message_to_telegram(chat_data: Union[Chat, Order]):
    """Запросить у клиента оценку за работу по выполненному заказу"""
    manager = bg_manager.bg(bot, chat_data.id, chat_data.id, load=True)
    await manager.start(OrderSG.mark, mode=StartMode.RESET_STACK, show_mode=ShowMode.SEND, data={'order_number': 777})
    return {'status': 'ok'}


@app.get('/getOrders')
async def get_orders(token: Annotated[Any, Depends(get_token)]):
    return {'token': token}


uvicorn.run(app, port=8080)
