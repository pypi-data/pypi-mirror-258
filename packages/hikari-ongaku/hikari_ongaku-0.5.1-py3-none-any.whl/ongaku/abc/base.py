"""Payload bases.

All of the payload base related objects.
"""

from __future__ import annotations

import abc
import json
import logging
import typing as t

import hikari
import pydantic
from pydantic.alias_generators import to_camel

from .. import internal

__all__ = (
    "_string_to_snowflake",
    "_snowflake_to_string",
    "PayloadBase",
    "PayloadBaseApp",
)

_logger = internal.logger.getChild("abc.base")

BaseT = t.TypeVar("BaseT", t.Mapping[str, t.Any], t.Sequence[t.Any])

INTERNAL_LOGGER = logging.getLogger(__name__)


class Payload(abc.ABC, pydantic.BaseModel, t.Generic[BaseT]):
    """
    Main payload.

    The main payload, that all payload types are inherited from.
    """


def _string_to_snowflake(
    guild_id: str,
    handler: pydantic.ValidatorFunctionWrapHandler,
    info: pydantic.ValidationInfo,
) -> hikari.Snowflake:
    try:
        return hikari.Snowflake(int(guild_id))
    except:
        raise


def _snowflake_to_string(
    guild_id: hikari.Snowflake,
    handler: pydantic.SerializerFunctionWrapHandler,
    info: pydantic.SerializationInfo,
) -> str:
    return str(guild_id)


class PayloadBase(Payload[BaseT], abc.ABC):
    """
    Payload base.

    The payload base, that allows for converting back into payloads to transfer.
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True, populate_by_name=True
    )

    @classmethod
    def _from_payload(cls, payload: BaseT) -> t.Self:
        """From payload.

        Converts the payload, into the current object.

        Raises
        ------
        TypeError
            When the type the value wanted, is incorrect.
        ValueError
            When the value is none.
        """
        name = cls.__qualname__
        _logger.log(internal.Trace.LEVEL, f"Validating payload: {payload} to {name}")
        if isinstance(payload, str):
            cls = cls.model_validate_json(payload, strict=True)
        else:
            cls = cls.model_validate_json(json.dumps(payload), strict=True)
        _logger.log(
            internal.Trace.LEVEL,
            f"Payload validation to {name} completed successfully.",
        )
        return cls

    @property
    def _to_payload(self) -> t.Mapping[str, t.Any]:
        """To payload.

        Converts your object, to a payload.
        """
        return self.model_dump(by_alias=True, mode="json")


class PayloadBaseApp(Payload[BaseT]):
    """
    Payload base application.

    The payload base, that supports an application/bot.
    """

    model_config = pydantic.ConfigDict(
        ignored_types=(hikari.RESTAware, hikari.GatewayBotAware),
        arbitrary_types_allowed=True,
        alias_generator=to_camel,
        populate_by_name=True,
        loc_by_alias=True,
    )

    bot_app: t.Annotated[hikari.RESTAware, pydantic.Field(default=None, exclude=True)]

    @property
    def app(self) -> hikari.RESTAware:
        """The application the event is attached too."""
        return self.bot_app

    @classmethod
    def _from_payload(cls, payload: BaseT | str, app: hikari.RESTAware) -> t.Self:
        """
        From payload.

        Converts the payload, into the current object.
        """
        name = cls.__class__.__name__

        _logger.log(internal.Trace.LEVEL, f"Validating payload: {payload} to {name}")
        if isinstance(payload, str):
            cls = cls.model_validate_json(payload, strict=True)
        else:
            cls = cls.model_validate_json(json.dumps(payload), strict=True)
        cls.bot_app = app
        _logger.log(
            internal.Trace.LEVEL,
            f"Payload validation to {name} completed successfully.",
        )
        return cls

    @property
    def _to_payload(self) -> t.Mapping[str, t.Any]:
        """To payload.

        Converts your object, to a payload.
        """
        _logger.log(
            internal.Trace.LEVEL, f"converting {self.__class__.__name__} to payload..."
        )
        return self.model_dump(by_alias=True, mode="json")


# MIT License

# Copyright (c) 2023 MPlatypus

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
