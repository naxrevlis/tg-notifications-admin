from dotenv import dotenv_values

config = dotenv_values(".env")

for key, value in config.items():
    print(f"{key}={value}")

print(config["DATABASE_URL"])

TORTOISE_ORM = {
    "connections": {"default": config["DATABASE_URL"]},
    "apps": {
        "models": {
            "models": ["tg_notifications_admin.database.models", "aerich.models"],
            "default_connection": "default"
        }
    }
}