from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import tabs

from openstack_dashboard import api
from openstack_dashboard.dashboards.monitor.network_monitor import tables


class InstanceTab(tabs.TableTab):
    name = _("Instances Tab")
    slug = "instances_tab"
    table_classes = (tables.EquipmentListTable,)
    template_name = ("horizon/common/_detail_table.html")
    preload = False

    def has_more_data(self, table):
        return self._has_more

    def get_equipment_list_data(self):
        try:
            marker = self.request.GET.get(
                        tables.EquipmentListTable._meta.pagination_param, None)

            # instances, self._has_more = api.nova.server_list(
            #     self.request,
            #     search_opts={'marker': marker, 'paginate': True})
            instances = []
            self._has_more = False

            return instances
        except Exception:
            self._has_more = False
            error_message = _('Unable to get instances')
            exceptions.handle(self.request, error_message)

            return []

class NetworkMonitorTabs(tabs.TabGroup):
    slug = "network_monitor_tabs"
    tabs = (InstanceTab,)
    sticky = True
