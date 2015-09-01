from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _

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
    template_name = 'monitor/network_monitor/equipment_detail.html'

    def get_data(self):
        interfaces = api.monitor.get_interface(self.request, self.kwargs["equipment_id"])

        return interfaces

class InterfaceDetailView(tables.DataTableView):
    table_class = project_tables.SyslogListTable
    template_name = 'monitor/network_monitor/interface_detail.html'

    def has_more_data(self, table):
        return self._more

    def get_data(self):
        interface = self.kwargs['interface'].split("-")
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

class FilterOptClass(object):
    attack_type = None
    addr = None
    priority = None
    destip = None
    srcip = None
    StartTime = None
    EndTime = None
    tag_list = None

    def __init__(self, dict):
        self.addr = dict["addr"]
        if dict["attack_type"] != 'Any':
            self.attack_type = dict["attack_type"]
        if dict["priority"] != 'Any':
            self.priority = dict["priority"]
        if dict["StartTime"]:
            self.StartTime = dict["StartTime"]
        if dict["EndTime"]:
            self.EndTime = dict["EndTime"]
        if dict["destip"]:
            self.destip = dict["destip"]
        if dict["srcip"]:
            self.srcip = dict["srcip"]
        self.tag_list = self.get_tag_list()

    def get_tag_list(self):
        return ['Newtouch-H3C', ]


def get_filter_opt(post_dict):
    filteropt = FilterOptClass(post_dict)
    return filteropt

class NetworkMonitorFilterActionView(tables.DataTableView):
    table_class = project_tables.SyslogListTable
    template_name = 'monitor/network_monitor/detail.html'

    def has_more_data(self, table):
        return self._more

    def get_data(self):
        # print self.request.method
        import pprint
        # pprint.pprint(self.request.POST)
        filter_opt = get_filter_opt(self.request.POST)
        print(filter_opt.priority,filter_opt.attack_type,filter_opt.StartTime,filter_opt.tag_list)
        # interface = ["GigabitEthernet0", "1", "192.168.202.1", "Connected"]
        marker = self.request.GET.get('marker')
        syslogs, self._more, count = api.monitor.filter_syslog_list(self.request,
                                               marker=marker,
                                               paginate=True,
                                               opt = filter_opt)
        # syslogs = []
        # self._more = False
        # count = "0"
        messages.info(self.request, "Find %s Logs" % (count))

        return syslogs