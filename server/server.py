import asyncio

import aiohttp.web
import uvloop

from routes import ROUTES


if __name__ == '__main__':
    # Использованием UVLoop в качестве цикла событий по-умолчанию
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    # Конфигурация сервера
    loop = asyncio.get_event_loop()
    app = aiohttp.web.Application(loop=loop, debug=True)
    app.router.add_routes(ROUTES)

    # Запуск сервера
    aiohttp.web.run_app(app, host='0.0.0.0', port=8080)
