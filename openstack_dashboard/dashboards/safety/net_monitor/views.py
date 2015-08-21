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

from horizon import tables,tabs
from openstack_dashboard.api import safety

from openstack_dashboard.dashboards.safety.net_monitor import constants
from openstack_dashboard.dashboards.safety.net_monitor import tables as project_tables
from openstack_dashboard.dashboards.safety.net_monitor import tags as project_tags


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
    tables_class = project_tables.SyslogsTable
    template_name = constants.SAFETY_TEMPLATE_NAME

    def has_more_data(self, table):
        return self._more

    def get_data(self):
        marker = self.request.GET.get('marker')
        syslogs, self._more = safety.logs_list(self.request,
                                               marker=marker,
                                               paginate=True,
                                               interface = self.kwargs['interface'])

        return syslogs

class DetailView(tables.DataTableView):
    table_class = project_tables.SyslogsDetailTable
    template_name = constants.SAFETY_DETAIL_TEMPLATE_NAME

    def get_data(self):
        message = []
        message = safety.logs_detail(self.request, self.kwargs['log_id'])

        return message
