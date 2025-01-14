# Copyright 2024 VyOS maintainers and contributors <maintainers@vyos.io>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this library.  If not, see <http://www.gnu.org/licenses/>.

from vyos.system import disk, grub, compat

@compat.grub_cfg_update
def set_console_speed(console_speed: str, root_dir: str = '') -> None:
    """Write default console speed to GRUB configuration

    Args:
        console_speed (str): default console speed
        root_dir (str, optional): an optional path to the root directory.
        Defaults to empty.
    """
    if not root_dir:
        root_dir = disk.find_persistence()

    grub.set_console_speed(console_speed, root_dir)

def update_console_speed(console_speed: str, root_dir: str = '') -> None:
    """Update console_speed if different from current value"""

    if not root_dir:
        root_dir = disk.find_persistence()

    vars_file: str = f'{root_dir}/{grub.CFG_VYOS_VARS}'
    vars_current: dict[str, str] = grub.vars_read(vars_file)
    console_speed_current = vars_current.get('console_speed', None)
    if console_speed != console_speed_current:
        set_console_speed(console_speed, root_dir)
