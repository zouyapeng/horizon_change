# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import tabs

from openstack_dashboard.dashboards.safety.net_monitor import tables
from openstack_dashboard.api import safety

class InterfaceTab(tabs.TableTab):
    table_classes = (tables.InterfaceTable, )
    name = _("Interface")
    slug = "interface"
    template_name = "horizon/common/_detail_table.html"

    def get_interface_data(self):
        interfaces = []
        try:
            interfaces = safety.get_interface(self.request)
        except Exception:
            exceptions.handle(self.request,
                _('Unable to retrieve hypervisor information.'))

        return interfaces


class NetMonitorTabs(tabs.TabGroup):
    slug = "net_monitor"
    tabs = (InterfaceTab, )
    sticky = True
