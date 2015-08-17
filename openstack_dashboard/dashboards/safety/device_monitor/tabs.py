# Copyright 2012 Nebula, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import tabs
from openstack_dashboard.api import keystone
from openstack_dashboard.api import nova
from openstack_dashboard.dashboards.safety.device_monitor import constants
from openstack_dashboard.dashboards.safety.device_monitor import tables


class NetDeviceTab(tabs.TableTab):
    table_classes = (tables.ServicesTable,)
    name = _("Net Device")
    slug = "net_device"
    template_name = constants.INFO_DETAIL_TEMPLATE_NAME

    def get_services_data(self):
        request = self.tab_group.request
        services = []
        for i, service in enumerate(request.user.service_catalog):
            service['id'] = i
            services.append(
                keystone.Service(service, request.user.services_region))
        return services


class ComputerNodeTab(tabs.TableTab):
    table_classes = (tables.NovaServicesTable,)
    name = _("Compute Nodes")
    slug = "compute_nodes"
    template_name = constants.INFO_DETAIL_TEMPLATE_NAME
    permissions = ('openstack.services.compute',)

    def get_nova_services_data(self):
        try:
            services = nova.service_list(self.tab_group.request)
        except Exception:
            msg = _('Unable to get nova services list.')
            exceptions.check_message(["Connection", "refused"], msg)
            exceptions.handle(self.request, msg)
            services = []
        return services


class ControllerNodeTab(tabs.TableTab):
    table_classes = (tables.NovaServicesTable,)
    name = _("Controller Nodes")
    slug = "controller_nodes"
    template_name = constants.INFO_DETAIL_TEMPLATE_NAME
    permissions = ('openstack.services.compute',)

    def get_nova_services_data(self):
        try:
            services = nova.service_list(self.tab_group.request)
        except Exception:
            msg = _('Unable to get nova services list.')
            exceptions.check_message(["Connection", "refused"], msg)
            exceptions.handle(self.request, msg)
            services = []
        return services


class DeviceMonitorTabs(tabs.TabGroup):
    slug = "device_monitor"
    tabs = (NetDeviceTab, ControllerNodeTab, ComputerNodeTab)
    sticky = True
