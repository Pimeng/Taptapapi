import os
import json
import argparse
import logging
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from apis.update import router as app_update_router
from apis.notice import router as app_notice_router
from apis.info import router as app_info_router

CONFIG_FILE = 'config.json'
DEFAULT_HOST = '0.0.0.0'
DEFAULT_PORT = 8080

def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(app_update_router)
    app.include_router(app_notice_router)
    app.include_router(app_info_router)

    @app.exception_handler(404)
    async def not_found_handler(request: Request, exc):
        logging.warning(f"404 Not Found: {request.url}")
        return FileResponse(
            "static/1.mp3",
            media_type="audio/mpeg",
            filename="audio.mp3"
        )

    return app

def load_config() -> dict:
    config = {
        'host': DEFAULT_HOST,
        'port': DEFAULT_PORT
    }
    # 从配置文件加载
    try:
        with open(CONFIG_FILE) as f:
            config.update(json.load(f))
    except FileNotFoundError:
        pass
    except Exception as e:
        logging.error(f"加载配置文件出错: {e}")

    # 环境变量覆盖
    config['host'] = os.getenv('HOST', config['host'])
    config['port'] = int(os.getenv('PORT', config['port']))

    return config

app = create_app()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', help='监听地址')
    parser.add_argument('--port', type=int, help='监听端口')
    args = parser.parse_args()

    config = load_config()
    if args.host:
        config['host'] = args.host
    if args.port:
        config['port'] = args.port

    import uvicorn
    uvicorn.run(app=app, host=config['host'], port=config['port'], workers=1)