from django.utils.translation import ugettext_lazy as _

import horizon

from openstack_dashboard.dashboards.monitor import dashboard


class Overview(horizon.Panel):
    name = _("Overview")
    slug = "overview"


dashboard.Monitor.register(Overview)
