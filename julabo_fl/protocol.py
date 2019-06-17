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

from e21_util.error import CommunicationError
from e21_util.interface import Loggable
from e21_util.serial_connection import AbstractTransport, SerialTimeoutException

class JulaboProtocol(Loggable):

    def __init__(self, transport, logger):
        super(JulaboProtocol, self).__init__(logger)
        assert isinstance(transport, AbstractTransport)

        self._transport = transport
        self.encoding = 'ascii'

    def create_message(self, header, *data):
        msg = []
        msg.append(header)
        msg.extend(data)
        msg.append("\r\n")
        return ''.join(msg).encode(self.encoding)

    def clear(self):
        with self._transport:
            while True:
                try:
                    self._transport.read_bytes(25)
                except SerialTimeoutException:
                    return True

    def _send_message(self, message):
        try:
            raw_message = message + "\r"
            self._logger.debug("Sending message %s", repr(message))
            self._transport.write(raw_message)
        except SerialTimeoutException:
            self._logger.exception("Error while sending message")
            raise CommunicationError("Could not send message. timeout")

    def _receive_message(self):
        try:
            msg = self._transport.read_until("\r\n")
            self._logger.debug("Received message %s", repr(msg))
            return "".join(map(chr, msg))
        except SerialTimeoutException:
            self._logger.exception("Error while receiving message")
            raise CommunicationError("Could not receive message. Timeout")

    def write(self, message):
        with self._transport:
            self._send_message(message)

    def query(self, message):
        with self._transport:
            self._send_message(message)
            return self._receive_message()
