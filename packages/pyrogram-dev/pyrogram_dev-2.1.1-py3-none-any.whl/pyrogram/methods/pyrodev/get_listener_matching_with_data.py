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


from typing import Optional

import pyrogram
from pyrogram.types import Identifier, Listener, ListenerTypes


class GetListenerMatchingWithData:
    def get_listener_matching_with_data(
        self: "pyrogram.Client", data: Identifier, listener_type: ListenerTypes
    ) -> Optional[Listener]:
        """
        Gets a listener that matches the given data.

        Parameters:
            data (:obj:`~pyrogram.types.Identifier`):
                The data to match against.

            listener_type (:obj:`~pyrogram.types.ListenerTypes`):
                The type of listener to get.

        Returns:
            :obj:`~pyrogram.types.Listener`: The listener that matches the given data or ``None`` if no listener matches.
        """
        matching = [
            listener
            for listener in self.listeners[listener_type]
            if listener.identifier.matches(data)
        ]

        # in case of multiple matching listeners, the most specific should be returned
        def count_populated_attributes(listener_item: Listener):
            return listener_item.identifier.count_populated()

        return max(matching, key=count_populated_attributes, default=None)
