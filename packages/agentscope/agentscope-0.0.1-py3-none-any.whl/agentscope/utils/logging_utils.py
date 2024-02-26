# -*- coding: utf-8 -*-
"""Logging utilities."""
import json
import os
import sys
from typing import Optional, Literal, Union, Any

from loguru import logger

LOG_LEVEL = Literal[
    "TRACE",
    "DEBUG",
    "INFO",
    "SUCCESS",
    "WARNING",
    "ERROR",
    "CRITICAL",
]

LEVEL_CHAT_LOG = "CHAT_LOG"
LEVEL_CHAT_SAVE = "CHAT_SAVE"


class _Stream:
    """Redirect stderr to logging"""

    def write(self, message: str) -> None:
        """Redirect to logging.

        Args:
            message (`str`):
                The message to be logged.
        """
        logger.error(message, enqueue=True)

    def flush(self) -> None:
        """Flush the stream."""


_SPEAKER_COLORS = [
    ("<blue>", "</blue>"),
    ("<cyan>", "</cyan>"),
    ("<green>", "</green>"),
    ("<magenta>", "</magenta>"),
    ("<red>", "</red>"),
    ("<white>", "</white>"),
    ("<yellow>", "</yellow>"),
]

_SPEAKER_TO_COLORS = {}


def _get_speaker_color(speaker: str) -> tuple[str, str]:
    """Get the color markers for a speaker. If the speaker is new, assign a
    new color. Otherwise, return the color that was assigned to the speaker.

    Args:
        speaker (`str`):
            The speaker to be assigned a color.

    Returns:
        `tuple[str, str]`: A color marker tuple, e.g. ("<blue>", "</blue>").
    """
    global _SPEAKER_COLORS, _SPEAKER_TO_COLORS
    if speaker in _SPEAKER_TO_COLORS:
        return _SPEAKER_TO_COLORS[speaker]
    else:
        markers = _SPEAKER_COLORS[
            (len(_SPEAKER_TO_COLORS) + 1)
            % len(
                _SPEAKER_COLORS,
            )
        ]
        # Record the color for this speaker
        _SPEAKER_TO_COLORS[speaker] = markers
        return markers


# add chat function for logger
def _chat(message: Union[str, dict], *args: Any, **kwargs: Any) -> None:
    """Log a chat message with the format of"<speaker>: <content>".

    Args:
        message (`Union[str, dict]`):
            The message to be logged. If it is a string, it will be logged
            directly. If it's a dict, it should have "name"(or "role") and
            "content" keys, and the message will be logged as "<name/role>:
            <content>".
    """
    # Save message into file
    logger.log(LEVEL_CHAT_SAVE, json.dumps(message), *args, **kwargs)

    # Print message in terminal with specific format
    if isinstance(message, dict):
        contain_name_or_role = "name" in message or "role" in message
        contain_content = "content" in message
        contain_url = "url" in message

        # print content if contain name or role and contain content
        if contain_name_or_role:
            speaker = message.get("name", None) or message.get("role", None)
            (m1, m2) = _get_speaker_color(speaker)

            print_str = []
            if contain_content:
                print_str.append(
                    f"{m1}<b>{speaker}</b>{m2}: {message['content']}",
                )

            if contain_url:
                print_str.append(f"{m1}<b>{speaker}</b>{m2}: {message['url']}")

            if len(print_str) > 0:
                print_str = (
                    "\n".join(print_str).replace("{", "{{").replace("}", "}}")
                )
                logger.log(LEVEL_CHAT_LOG, print_str, *args, **kwargs)
                return

    message = str(message).replace("{", "{{").replace("}", "}}")
    logger.log(LEVEL_CHAT_LOG, message, *args, **kwargs)


def _level_format(record: dict) -> str:
    """Format the log record."""
    if record["level"].name == LEVEL_CHAT_LOG:
        return record["message"] + "\n"
    else:
        return (
            "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{"
            "level: <8}</level> | <cyan>{name}</cyan>:<cyan>{"
            "function}</cyan>:<cyan>{line}</cyan> - <level>{"
            "message}</level>\n"
        )


def setup_logger(
    path_log: Optional[str] = None,
    level: LOG_LEVEL = "INFO",
) -> None:
    r"""Setup `loguru.logger` and redirect stderr to logging.

    Args:
        path_log (`str`, defaults to `""`):
            The directory of log files.
        level (`str`, defaults to `"INFO"`):
            The logging level, which is one of the following: `"TRACE"`,
            `"DEBUG"`, `"INFO"`, `"SUCCESS"`, `"WARNING"`, `"ERROR"`,
            `"CRITICAL"`.
    """
    # avoid reinit in subprocess
    if hasattr(logger, "chat"):
        return

    # redirect stderr to record errors in logging
    sys.stderr = _Stream()

    # add chat function for logger
    logger.level(LEVEL_CHAT_LOG, no=21)
    logger.level(LEVEL_CHAT_SAVE, no=0)
    logger.chat = _chat

    # set logging level
    logger.remove()
    # standard output for all logging except chat
    logger.add(
        sys.stdout,
        filter=lambda record: record["level"].name != LEVEL_CHAT_SAVE,
        format=_level_format,
        enqueue=True,
        level=level,
    )

    if path_log is not None:
        if not os.path.exists(path_log):
            os.makedirs(path_log)
        path_log_file = os.path.join(path_log, "logging.log")
        path_chat_file = os.path.join(
            path_log,
            "logging.chat",
        )

        # save all logging into file
        logger.add(
            path_log_file,
            filter=lambda record: record["level"].name != LEVEL_CHAT_SAVE,
            format=_level_format,
            enqueue=True,
            level=level,
        )

        logger.add(
            path_chat_file,
            filter=lambda record: record["level"].name == LEVEL_CHAT_SAVE,
            format="{message}",
            enqueue=True,
            level=LEVEL_CHAT_SAVE,
        )
