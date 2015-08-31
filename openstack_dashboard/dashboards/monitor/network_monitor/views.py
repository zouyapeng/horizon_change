from django.core.urlresolvers import reverse_lazy

from horizon import tabs
from horizon import forms
from horizon import tables
from horizon import messages

from openstack_dashboard import api
from openstack_dashboard.dashboards.monitor.network_monitor import tags as project_tags
from openstack_dashboard.dashboards.monitor.network_monitor import forms as project_forms
from openstack_dashboard.dashboards.monitor.network_monitor import tables as project_tables

class IndexView(tabs.TabbedTableView):
    # A very simple class-based view...
    tab_group_class = project_tags.NetworkMonitorTabs
    template_name = 'monitor/network_monitor/index.html'

    # def get_data(self, request, context, *args, **kwargs):
    #     # Add data to the context here...
    #     return context

class EquipmentDetailView(tables.DataTableView):
    table_class = project_tables.InterfaceListTable
    template_name = 'monitor/network_monitor/detail.html'

    def get_data(self):
        interfaces = api.monitor.get_interface(self.request, self.kwargs["equipment_id"])

        return interfaces

class InterfaceDetailView(tables.DataTableView):
    table_class = project_tables.SyslogListTable
    template_name = 'monitor/network_monitor/detail.html'

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
            syslogs, self._more, count = api.monitor.syslog_list(self.request,
                                                   marker=marker,
                                                   paginate=True,
                                                   interface = self.kwargs['interface'])
            messages.info(self.request, "%s has %s Logs" % (interface[0] + "/" + interface[1], count))

        return syslogs

class NetworkMonitorFilterView(forms.ModalFormView):
    form_class = project_forms.FilterForm
    template_name = 'monitor/network_monitor/filter.html'
    context_object_name = 'image'
    success_url = reverse_lazy("horizon:monitor:network_monitor:index")

class NetworkMonitorFilterActionView(tables.DataTableView):
    table_class = project_tables.SyslogListTable
    template_name = 'monitor/network_monitor/detail.html'

    def has_more_data(self, table):
        return self._more

    def get_data(self):
        # print self.request.method
        import pprint
        pprint.pprint(self.request.POST)
        interface = ["GigabitEthernet0", "1", "192.168.202.1", "Connected"]
        if interface[3] == "Not Connected":
            messages.info(self.request, "%s is %s" %(interface[0] + "/" + interface[1], interface[3]))
            syslogs = []
            self._more = False
        else:
            marker = self.request.GET.get('marker')
            syslogs, self._more, count = api.monitor.syslog_list(self.request,
                                                   marker=marker,
                                                   paginate=True,
                                                   interface = "GigabitEthernet0-1-192.168.202.1-Connected")
            messages.info(self.request, "%s has %s Logs" % (interface[0] + "/" + interface[1], count))

        return syslogs