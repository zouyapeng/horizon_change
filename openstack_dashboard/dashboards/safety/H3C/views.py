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
import json
import logging

from horizon import tables

from openstack_dashboard import api

from openstack_dashboard.dashboards.safety.H3C import constants
from openstack_dashboard.dashboards.safety.H3C import tables as project_tables
from django.utils.translation import ugettext_lazy as _

LOG = logging.getLogger(__name__)

class IndexView(tables.DataTableView):
    table_class = project_tables.ServicesTable
    template_name = constants.INFO_TEMPLATE_NAME

    # def has_prev_data(self, table):
    #     return self._prev

    def has_more_data(self, table):
        return self._more

    def get_data(self):
        marker = self.request.GET.get('marker')
        # prev_marker = self.request.GET('prev_marker')
        h3clogs, self._more = api.safety.log_list(self.request, prev_marker=None ,marker=marker,paginate=True)
        return h3clogs

