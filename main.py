import os
import aiohttp
from aiogram import types
from aiogram.types import Update, MenuButtonWebApp, WebAppInfo
from aiohttp import web
from aiogram import Bot, Dispatcher
from core.settings import settings

bot = Bot(settings.API_TELEGRAM)
dp = Dispatcher(bot)
WH_URI = settings.WEBHOOK_URI
Bot.set_current(bot)
app = web.Application()
webhook_path = f'/{settings.API_TELEGRAM}'
routes = web.RouteTableDef()
local_dir = os.path.join(os.path.dirname(__file__), "templateFiles/static")
app.router.add_static('/static', local_dir)


async def set_webhook():
    webhook_uri = f'{WH_URI}{webhook_path}'
    await bot.set_webhook(url=webhook_uri)
    # await bot.set_webhook(url=webhook_uri, certificate=open('./YOURPUBLIC.pem', 'rb'))


async def on_startup(_):
    await set_webhook()
    await bot.set_chat_menu_button(
        menu_button=MenuButtonWebApp(text="тест", web_app=WebAppInfo(url=f"{WH_URI}/test"))
    )


def html_response(document):
    s = open(document, "r")
    return web.Response(text=s.read(), content_type='text/html')


@routes.get('/test')
async def test(request):
    return html_response('templateFiles/index.html')


@routes.post('/invoice')
async def test(request):
    """Invoice render logic"""
    payload = await request.json()
    prices = [types.LabeledPrice(label=payload.get('id'), amount=payload.get('price')*100)]
    invoice = await bot.create_invoice_link(
        title="Food",
        description="dump_payment",
        payload=str(payload),
        provider_token=settings.PAYMENT_TOKEN,
        currency='RUB',
        prices=prices,
        photo_url='https://images.squarespace-cdn.com/content/v1/5ec1febb58a4890157c8fbeb/19ebb9ed-4862-46e1'
                     '-9f7c-4e5876730227/Beetroot-Burger.jpg',
        need_name=True,
        need_phone_number=True
    )
    return web.json_response(status=200, data=invoice) if invoice else web.Response(status=400)


async def handle_wh(request):
    url = str(request.url)
    index = url.rfind('/')
    token = url[index + 1:]

    if token == settings.API_TELEGRAM:
        request_data = await request.json()
        update = Update(**request_data)
        await dp.process_update(update)
        return web.Response()
    else:
        return web.Response(status=403)


app.router.add_post(f'/{settings.API_TELEGRAM}', handle_wh)
app.add_routes(routes)

if __name__ == '__main__':
    app.on_startup.append(on_startup)
    web.run_app(app=app, host=settings.SERV_HOST, port=settings.SERV_PORT)
    # ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    # ssl_context.load_cert_chain('YOURPUBLIC.pem', 'YOURPRIVATE.key')
    # web.run_app(app=app, host=SERV_HOST, port=SERV_PORT, ssl_context=ssl_context)
