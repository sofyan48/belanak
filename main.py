from dotenv import load_dotenv
import os, logging, sys, uvicorn, argparse
from uvicorn import Config, Server
from loguru import logger
from pkg import utils

LOG_LEVEL = logging.getLevelName(os.environ.get("LOGGER_LEVEL", "INFO"))

try:
    load_dotenv(
        dotenv_path=os.path.join(os.getcwd(), '.env'), 
        verbose=True)
except Exception as e:
    print("Error Env: ", e)
    

class InterceptHandler(logging.Handler):
    def emit(self, record):
        # get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # find caller from where originated the logged message
        frame, depth = sys._getframe(6), 6
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1
        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def setup_logging():
    logging.root.handlers = [InterceptHandler()]
    logging.root.setLevel(LOG_LEVEL)

    for name in logging.root.manager.loggerDict.keys():
        logging.getLogger(name).handlers = []
        logging.getLogger(name).propagate = True
    # configure loguru
    logger.configure(handlers=[{"sink": sys.stdout, "serialize": True}])


if __name__ == '__main__':
    from app import app, APP_ROOT

    parser = argparse.ArgumentParser()
    parser.add_argument("command", help="Perintah yang ingin Anda jalankan")
    args = parser.parse_args()
   
    if args.command == "serve":
        if utils.environment_transform() != "loc":
            server = Server(
                Config(
                    app=app,
                    host=os.environ.get("APP_HOST", "0.0.0.0"),
                    port=int(os.environ.get("APP_PORT", "8080")),
                    log_level=LOG_LEVEL,
                    workers=16,
                    timeout_keep_alive=60,
                    root_path=APP_ROOT
                ),
            )
            setup_logging()
            server.run()
        else:
            uvicorn.run(
                app="app:app",
                host=os.environ.get("APP_HOST", "0.0.0.0"),
                port=int(os.environ.get("APP_PORT", "8080")),
                reload=True,
                log_level=logging.getLevelName(os.environ.get("LOGGER_LEVEL", "DEBUG")),
            )
            
        exit(0);