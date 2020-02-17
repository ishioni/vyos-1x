# Copyright (C) 2019-2020 VyOS maintainers and contributors
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 or later as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import unittest

from vyos.config import Config
from vyos.configsession import ConfigSession, ConfigSessionError
from netifaces import ifaddresses, AF_INET, AF_INET6
from vyos.validate import is_intf_addr_assigned, is_ipv6_link_local
from vyos.interfaces import list_interfaces_of_type

class BasicInterfaceTest:
    class BaseTest(unittest.TestCase):
        def setUp(self):
            self.session = ConfigSession(os.getpid())
            env = self.session.get_session_env()
            self.config = Config(session_env=env)

            self._test_addr = ['192.0.2.1/25', '2001:db8:1::ffff/64']
            self._test_mtu = False

        def tearDown(self):
            self.session.delete(self._base_path)
            self.session.commit()

            del self.session

        def test_add_description(self):
            """
            Check if description can be added to interface
            """
            for intf in self._interfaces:
                test_string='Description-Test-{}'.format(intf)
                self.session.set(self._base_path + [intf, 'description', test_string])
            self.session.commit()

            # Validate interface description
            for intf in self._interfaces:
                test_string='Description-Test-{}'.format(intf)
                with open('/sys/class/net/{}/ifalias'.format(intf), 'r') as f:
                    tmp = f.read().rstrip()
                    self.assertTrue(tmp, test_string)

        def test_add_address(self):
            """
            Check if address can be added to interface
            """

            # Add address
            for intf in self._interfaces:
                for addr in self._test_addr:
                    self.session.set(self._base_path + [intf, 'address', addr])
                self.session.commit()

            # Validate address
            for intf in self._interfaces:
                for af in AF_INET, AF_INET6:
                    for addr in ifaddresses(intf)[af]:
                        # checking link local addresses makes no sense
                        if is_ipv6_link_local(addr['addr']):
                            continue

                        self.assertTrue(is_intf_addr_assigned(intf, addr['addr']))

