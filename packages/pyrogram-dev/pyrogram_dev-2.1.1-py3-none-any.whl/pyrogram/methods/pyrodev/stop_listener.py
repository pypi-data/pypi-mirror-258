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


import inspect

import pyrogram
from pyrogram.errors import (
    ListenerStopped,
)
from pyrogram.types import Listener
from pyrogram.utils import PyroDevConfig


class StopListener:
    async def stop_listener(self: "pyrogram.Client", listener: Listener):
        """
        Stops a listener, calling stopped_handler if applicable or raising ListenerStopped if throw_exceptions is True.

        Parameters:
            listener (:obj:`~pyrogram.types.Listener`):
                The :class:`pyrogram.types.Listener` to stop.

        Returns:
            None

        Raises:
            ListenerStopped: If throw_exceptions is True.
        """
        self.remove_listener(listener)

        if listener.future.done():
            return

        if callable(PyroDevConfig.stopped_handler):
            if inspect.iscoroutinefunction(PyroDevConfig.stopped_handler.__call__):
                await PyroDevConfig.stopped_handler(None, listener)
            else:
                await self.loop.run_in_executor(
                    None, PyroDevConfig.stopped_handler, None, listener
                )
        elif PyroDevConfig.throw_exceptions:
            listener.future.set_exception(ListenerStopped())
