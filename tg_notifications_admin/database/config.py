from dotenv import dotenv_values

config = dotenv_values(".env")

TORTOISE_ORM = {
    "connections": {"default": config["DATABASE_URL"]},
    "apps": {
        "models": {
            "models": ["tg_notifications_admin.database.models", "aerich.models"],
            "default_connection": "default",
        }
    },
}
