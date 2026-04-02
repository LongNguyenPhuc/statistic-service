from os import cpu_count, getenv
from dotenv import load_dotenv
from app.services.settings import get_settings


load_dotenv()
env = getenv("env")
settings = get_settings()

if __name__ == "__main__":
    from uvicorn import run

    print("Environment: " + env)
    if env.lower() != "production":
        run(
            "app:create_app",
            port=settings.PORT,
            reload=settings.DEBUG,
            factory=True,
        )
    else:
        from gunicorn.app.base import BaseApplication
        from app import create_app

        class StandaloneApplication(BaseApplication):
            def __init__(self, app, options=None):
                self.options = options or {}
                self.application = app
                super().__init__()

            def load_config(self):
                config = {
                    key: value
                    for key, value in self.options.items()
                    if key in self.cfg.settings and value is not None
                }
                for key, value in config.items():
                    self.cfg.set(key.lower(), value)

            def load(self):
                return self.application

        StandaloneApplication(
            create_app(),
            {
                "bind": f"{'0.0.0.0'}:{settings.PORT}",
                "workers": cpu_count() - 1,
                "worker_class": "uvicorn.workers.UvicornWorker",
            },
        ).run()
