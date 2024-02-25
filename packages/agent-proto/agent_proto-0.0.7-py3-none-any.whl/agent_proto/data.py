import json
import logging
import os
from datetime import datetime
from functools import cached_property, wraps
from hashlib import sha256
from typing import (
    Any,
    Callable,
    Coroutine,
    Generic,
    List,
    Optional,
    Type,
    TypeVar,
    Union,
)
from uuid import uuid4

import aiofiles  # pylint:disable=E0401
from pydantic import BaseModel
from typing_extensions import ParamSpec

T = TypeVar("T")
M = TypeVar("M", bound=BaseModel)
P = ParamSpec("P")


class JSONLinesLogRecord(BaseModel):
    """
    A typed dictionary representing a log record in JSON Lines format.

    Attributes:
                                                                    request_id (str): The unique request ID.
                                                                    timestamp (str): The timestamp of the log record.
                                                                    message (str): The log message.
                                                                    level (str): The log level.
                                                                    module (str): The module where the log was created.
                                                                    function (str): The function where the log was created.
                                                                    line (int): The line number where the log was created.
    """

    request_id: str
    timestamp: str
    message: Union[dict[str, Any], list[dict[str, Any]], str]
    level: str
    module: str
    function: str
    line: int


class JSONLinesHandler(logging.FileHandler):
    """
    A custom logging handler that writes log records in JSON Lines format.

    Inherits from logging.FileHandler.

    Args:
                                                                    filename (str): The name of the log file.
                                                                    mode (str, optional): The file mode to open the log file in. Defaults to "a".
                                                                    encoding (str, optional): The encoding to use for the log file. Defaults to "utf-8".
                                                                    delay (bool, optional): Whether to delay the file opening. Defaults to False.
    """

    def __init__(
        self,
        filename: str,
        mode: str = "a",
        encoding: str = "utf-8",
        delay: bool = False,
    ) -> None:
        super().__init__(filename, mode, encoding, delay)

    def emit(self, record: logging.LogRecord) -> None:
        log_entry = self.format(record)
        self.stream.write(log_entry)
        self.flush()

    def format(self, record: logging.LogRecord) -> str:
        return JSONLinesLogRecord(
            request_id=sha256(str(uuid4()).encode()).hexdigest(),
            timestamp=datetime.utcfromtimestamp(record.created)
            .astimezone()
            .isoformat(),
            message=record.getMessage(),
            level=record.levelname,
            module=record.module,
            function=record.funcName,
            line=record.lineno,
        ).model_dump_json()  # Decode bytes to string here


class JSONLinesFormatter(logging.Formatter):
    """
    A custom formatter for logging records in JSONLines format.
    """

    def format(self, record: logging.LogRecord) -> str:
        """
        Formats the log record into a JSONLines string.

        Args:
                                                                        record (logging.LogRecord): The log record to be formatted.

        Returns:
                                                                        str: The formatted log record in JSONLines format.
        """
        return JSONLinesLogRecord(
            request_id=sha256(str(uuid4()).encode()).hexdigest(),
            timestamp=datetime.utcfromtimestamp(record.created)
            .astimezone()
            .isoformat(),
            message=record.getMessage(),
            level=record.levelname,
            module=record.module,
            function=record.funcName,
            line=record.lineno,
        ).model_dump_json()


class JSONLinesLogger(logging.Logger):
    """
    A custom logger that logs messages to a JSONLines file.

    Args:
                                                                    name (str): The name of the logger.

    Attributes:
                                                                    handler (JSONLinesHandler): The handler responsible for writing log records to the JSONLines file.
                                                                    formatter (JSONLinesFormatter): The formatter used to format log records.

    """

    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.setLevel(logging.DEBUG)
        self.addHandler(self.handler)
        self.handler.setFormatter(self.formatter)
        self.propagate = False

    @cached_property
    def handler(self) -> JSONLinesHandler:
        return JSONLinesHandler(f".cache/{self.name}.jsonl", "a", "utf-8")

    @cached_property
    def formatter(self) -> JSONLinesFormatter:
        return JSONLinesFormatter()

    def log(self, level: int, msg: object, *args: Any, **kwargs: Any) -> None:
        super().log(level, msg, *args, **kwargs)


logging.setLoggerClass(JSONLinesLogger)


def log(
    func: Callable[P, Coroutine[Any, Any, M]]
) -> Callable[P, Coroutine[Any, Any, M]]:
    """
    A decorator that logs the entry and exit of a function.

    Args:
                                                                    func (Callable): The function to be logged.

    Returns:
                                                                    Callable: The logged function.
    """

    @wraps(func)
    async def wrapper(*args: P.args, **kwargs: P.kwargs):
        logger = logging.getLogger(func.__module__)
        result = await func(*args, **kwargs)
        logger.log(logging.INFO, result)
        return result

    return wrapper


class Database(Generic[M]):
    def __init__(self, database_path: str, model: Type[M]):
        self.database_path = database_path
        self.model = model

    async def create_collection(self, collection_name: str):
        collection_file = f"{self.database_path}/{collection_name}.jsonl"
        if not os.path.exists(collection_file):
            async with aiofiles.open(collection_file, "w", encoding="utf-8") as file:
                await file.write("")

    async def insert(self, collection_name: str, data: M):
        collection_file = f"{self.database_path}/{collection_name}.jsonl"
        async with aiofiles.open(collection_file, "a", encoding="utf-8") as file:
            await file.write(data.model_dump_json() + "\n")

    async def find_by_id(self, collection_name: str, item_id: str) -> Optional[M]:
        collection_file = f"{self.database_path}/{collection_name}.jsonl"
        async with aiofiles.open(collection_file, "r", encoding="utf-8") as file:
            async for line in file:
                item_data = json.loads(line)
                if item_data.get("id") == item_id:
                    return self.model(**item_data)
        return None

    async def find_all(self, collection_name: str) -> List[M]:
        collection_file = f"{self.database_path}/{collection_name}.jsonl"
        items: List[M] = []
        async with aiofiles.open(collection_file, "r", encoding="utf-8") as file:
            async for line in file:
                item_data = json.loads(line)
                items.append(self.model(**item_data))
        return items

    async def update(
        self, collection_name: str, item_id: str, data: Union[dict[str, Any], M]
    ) -> bool:
        collection_file = f"{self.database_path}/{collection_name}.jsonl"
        temp_file = collection_file + ".tmp"
        async with aiofiles.open(
            collection_file, "r", encoding="utf-8"
        ) as file, aiofiles.open(temp_file, "w", encoding="utf-8") as temp:
            updated = False
            async for line in file:
                item_data = json.loads(line)
                if item_data.get("id") == item_id:
                    updated_data = (
                        data.model_dump() if isinstance(data, BaseModel) else data
                    )
                    item_data.update(updated_data)
                    await temp.write(self.model(**item_data).model_dump_json() + "\n")
                    updated = True
                else:
                    await temp.write(line)
            if not updated:
                os.remove(temp_file)
                return False
        os.replace(temp_file, collection_file)
        return True

    async def delete(self, collection_name: str, item_id: str) -> bool:
        collection_file = f"{self.database_path}/{collection_name}.jsonl"
        temp_file = collection_file + ".tmp"
        async with aiofiles.open(
            collection_file, "r", encoding="utf-8"
        ) as file, aiofiles.open(temp_file, "w", encoding="utf-8") as temp:
            deleted = False
            async for line in file:
                item_data = json.loads(line)
                if item_data.get("id") == item_id:
                    deleted = True
                    continue  # Skip writing this line to effectively delete it
                await temp.write(line)
            if not deleted:
                os.remove(temp_file)
                return False
        os.replace(temp_file, collection_file)
        return True
