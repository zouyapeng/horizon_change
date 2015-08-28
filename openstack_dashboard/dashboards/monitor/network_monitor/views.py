from horizon import tabs

from openstack_dashboard.dashboards.monitor.network_monitor import tags as project_tags

class IndexView(tabs.TabbedTableView):
    # A very simple class-based view...
    tab_group_class = project_tags.NetworkMonitorTabs
    template_name = 'monitor/network_monitor/index.html'

    def get_data(self, request, context, *args, **kwargs):
        # Add data to the context here...
        return context
