# Copyright 2012 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
#
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

from django.core.urlresolvers import reverse_lazy

from horizon import tables,tabs,forms
from horizon import messages
from openstack_dashboard.api import safety

from openstack_dashboard.dashboards.safety.net_monitor import constants
from openstack_dashboard.dashboards.safety.net_monitor import tables as project_tables
from openstack_dashboard.dashboards.safety.net_monitor import tags as project_tags
from openstack_dashboard.dashboards.safety.net_monitor import forms as project_forms


class IndexView(tabs.TabbedTableView):
    tab_group_class = project_tags.NetMonitorTabs
    template_name = constants.SAFETY_TEMPLATE_NAME

# class IndexView(tables.DataTableView):
#     table_class = project_tables.SyslogsTable
#     template_name = constants.SAFETY_TEMPLATE_NAME
#
#     def has_more_data(self, table):
#         return self._more
#
#     def get_data(self):
#         marker = self.request.GET.get('marker')
#         syslogs, self._more = safety.logs_list(self.request, marker=marker, paginate=True)
#
#         return syslogs

class InterfaceView(tables.DataTableView):
    table_class = project_tables.SyslogsTable
    template_name = constants.SAFETY_INTERFACE_TEMPLATE_NAME

    def has_more_data(self, table):
        return self._more

    def get_data(self):
        interface = self.kwargs['interface'].split("-")
        if interface[3] == "Not Connected":
            messages.info(self.request, "%s is %s" %(interface[0] + "/" + interface[1], interface[3]))
            syslogs = []
            self._more = False
        else:
            marker = self.request.GET.get('marker')
            syslogs, self._more, count = safety.logs_list(self.request,
                                                   marker=marker,
                                                   paginate=True,
                                                   interface = self.kwargs['interface'])
            messages.info(self.request, "%s has %s Logs" % (interface[0] + "/" + interface[1], count))

        return syslogs

# class AdvancedFilterView(forms.ModalFormView):
#     form_class = project_forms.AdvancedFilterForm
#     template_name = constants.SAFETY_FILTER_TEMPLATE_NAME
#     context_object_name = 'filter'
#     success_url = reverse_lazy("horizon:safety:net_monitor:index")

class DetailView(tables.DataTableView):
    table_class = project_tables.SyslogsDetailTable
    template_name = constants.SAFETY_DETAIL_TEMPLATE_NAME

    def get_data(self):
        message = []
        message = safety.logs_detail(self.request, self.kwargs['log_id'])

        return message
