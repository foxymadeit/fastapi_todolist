from loguru import logger
logger.add("logs/app.log", rotation="1 day",
            retention="7 days", level="INFO",
            filter=lambda record: record["level"].name not in ("ERROR", "WARNING"))

logger.add("logs/errors.log", rotation="1 week", retention="30 days", level="WARNING")


def log_task_created(task_title: str, user_id: int):
    logger.info(f"User: {user_id} created task: '{task_title}'")

