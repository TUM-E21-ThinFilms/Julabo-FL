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

from slave.driver import Driver, Command

from protocol import JulaboProtocol

class JulaboDriver(object):

    def __init__(self, transport, protocol=None):

        if protocol is None:
            protocol = JulaboProtocol()

        self._transport = transport
        self._protocol = protocol

    def clear(self):
        self._protocol.clear(self._transport)

    def _query(self, cmd):
        return self._protocol.query(self._transport, cmd)

    def _write(self, cmd):
        return self._protocol.write(self._transport, cmd)

    def set_setpoint(self, temperature):
        if temperature > 40 or temperature < 5:
            raise ValueError("temperature must be in range [5, 40]")

        # only 2 digits behind . allowed
        if int(temperature * 100) != temperature * 100:
            raise ValueError("temperature too precise")

        self._write('OUT_SP_00 ' + str(temperature))

    def turn_on(self):
        self._write('OUT_MODE_05 1')

    def turn_off(self):
        self._write('OUT_MODE_05 0')

    def get_version(self):
        return self._query('VERSION')

    def get_status(self):
        return self._query('STATUS')

    def get_setpoint(self):
        return float(self._query('IN_SP_00'))

    def get_temperature(self):
        return float(self._query('IN_PV_00'))

    def get_on(self):
        return int(self._query('IN_MODE_05'))
