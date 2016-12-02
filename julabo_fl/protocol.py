# Copyright (C) 2016, see AUTHORS.md
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import slave

from slave.protocol import Protocol
from slave.transport import Timeout

class CommunicationError(Exception):
    pass

class JulaboProtocol(Protocol):

    def __init__(self, logger=None):
        self.logger = logger
        self.encoding = 'ascii'

    def create_message(self, header, *data):
        msg = []
        msg.append(header)
        msg.extend(data)
        msg.append("\r\n")
        return ''.join(msg).encode(self.encoding)

    def clear(self, transport):
        while True:
            try:
                transport.read_bytes(25)
            except Timeout:
                return True

    def _send_message(self, transport, message):
        try:
            raw_message = message + "\r"
            self.logger.debug("Seding message %s", repr(message))
            transport.write(raw_message)
        except slave.transport.Timeout:
            self.logger.exception("Error while sending message")
            raise CommunicationError("Could not send message. timeout")

    def _receive_message(self, transport):
        try:
            msg = transport.read_until("\r\n")
            self.logger.debug("Received message %s", repr(msg))
        except slave.transport.Timeout:
            self.logger.exception("Error while receiving message")
            raise CommunicationError("Could not receive message. timeout")

    def write(self, transport, message):
        self._send_message(transport, message)

    def query(self, transport, message):
        self._send_message(transport, message)
        return self._receive_message(transport)