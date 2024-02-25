#  Pyrogram-Dev - Telegram MTProto API Client Library for Python
#  Copyright (C) 2024-present Aditya <https://github.com/AdityaHalder>
#
#  This file is part of Pyrogram-Dev.
#
#  Pyrogram-Dev is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrogram-Dev is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrogram-Dev.  If not, see <http://www.gnu.org/licenses/>.


import asyncio
import inspect
from typing import Optional, Union

import pyrogram
from pyrogram.errors import (
    ListenerTimeout,
)
from pyrogram.filters import Filter
from pyrogram.types import Identifier, Listener, ListenerTypes
from pyrogram.utils import PyroDevConfig


class Listen:
    async def listen(
        self: "pyrogram.Client",
        filters: Optional[Filter] = None,
        listener_type: ListenerTypes = ListenerTypes.MESSAGE,
        timeout: Optional[int] = None,
        unallowed_click_alert: bool = True,
        chat_id: Optional[Union[int, str, list[Union[int, str]]]] = None,
        user_id: Optional[Union[int, str, list[Union[int, str]]]] = None,
        message_id: Optional[Union[int, list[int]]] = None,
        inline_message_id: Optional[Union[str, list[str]]] = None,
    ) -> Union["pyrogram.types.Message", "pyrogram.types.CallbackQuery"]:
        """
        Creates a listener and waits for it to be fulfilled.

        Parameters:
            filters (``Optional[Filter]``):
                A filter to check if the listener should be fulfilled.

            listener_type (``ListenerTypes``):
                The type of listener to create. Defaults to :attr:`pyrogram.types.ListenerTypes.MESSAGE`.

            timeout (``Optional[int]``):
                The maximum amount of time to wait for the listener to be fulfilled. Defaults to ``None``.

            unallowed_click_alert (``bool``):
                Whether to alert the user if they click on a button that is not intended for them. Defaults to ``True``.

            chat_id (``Optional[Union[int, str], List[Union[int, str]]]``):
                The chat ID(s) to listen for. Defaults to ``None``.

            user_id (``Optional[Union[int, str], List[Union[int, str]]]``):
                The user ID(s) to listen for. Defaults to ``None``.

            message_id (``Optional[Union[int, List[int]]]``):
                The message ID(s) to listen for. Defaults to ``None``.

            inline_message_id (``Optional[Union[str, List[str]]]``):
                The inline message ID(s) to listen for. Defaults to ``None``.

        Returns:
            ``Union[Message, CallbackQuery]``: The Message or CallbackQuery that fulfilled the listener.
        """
        pattern = Identifier(
            from_user_id=user_id,
            chat_id=chat_id,
            message_id=message_id,
            inline_message_id=inline_message_id,
        )

        loop = asyncio.get_event_loop()
        future = loop.create_future()

        listener = Listener(
            future=future,
            filters=filters,
            unallowed_click_alert=unallowed_click_alert,
            identifier=pattern,
            listener_type=listener_type,
        )

        future.add_done_callback(lambda _future: self.remove_listener(listener))

        self.listeners[listener_type].append(listener)

        try:
            return await asyncio.wait_for(future, timeout)
        except asyncio.exceptions.TimeoutError:
            if callable(PyroDevConfig.timeout_handler):
                if inspect.iscoroutinefunction(PyroDevConfig.timeout_handler.__call__):
                    await PyroDevConfig.timeout_handler(pattern, listener, timeout)
                else:
                    await self.loop.run_in_executor(
                        None, PyroDevConfig.timeout_handler, pattern, listener, timeout
                    )
            elif PyroDevConfig.throw_exceptions:
                raise ListenerTimeout(timeout)
