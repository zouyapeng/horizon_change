from django.utils.translation import ugettext_lazy as _
from django.template import defaultfilters as filters

from horizon import tables

class NetworkMonitorFilterAction(tables.LinkAction):
    name = "filter"
    verbose_name = _("Filter")
    url = "horizon:monitor:network_monitor:filter"
    # classes = ("",)
    icon = "search"


class SyslogFilterAction(tables.FilterAction):
    name = "filter"
    # def filter(self, table, sysloglist, filter_string):
    #     """Really naive case-insensitive search."""
    #     q = filter_string.lower()
    #
    #     def comp(sysloglist):
    #         return q in sysloglist.name.lower()
    #
    #     return filter(comp, sysloglist)
    filter_type = "server"
    filter_choices = (('id', _("ID ="), True),
                      ('time', _('Time ='), True),
                      ('type', _('Type ='), True),
                      ('priority', _('Priority ='), True),)

class NetworkMonitorEditAction(tables.LinkAction):
    name = "config"
    verbose_name = _("Config")
    url = "#"
    # classes = ("",)
    # icon = "search"


class EquipmentListTable(tables.DataTable):
    id = tables.Column("id", verbose_name=_("ID"), hidden=True)
    name = tables.Column("name",
                         verbose_name=_("Name"),
                         link="horizon:monitor:network_monitor:equipment")
    type = tables.Column("type", verbose_name=_("Type"))
    descrition = tables.Column("descrition", verbose_name=_("Descrition"))

    ip = tables.Column('ip', verbose_name=_("Ip"))
    cpu_usage = tables.Column('cpu_usage', verbose_name=_("CpuUsage"))
    mem_usage = tables.Column('mem_usage', verbose_name=_("MemUsage"))
    status = tables.Column("status", verbose_name=_("Status"))

    def get_object_id(self, datum):
        return "%s" % (datum.id)

    class Meta:
        name = "equipment_list"
        verbose_name = _("Equipment List")
        row_actions = (NetworkMonitorEditAction, )
        table_actions = (NetworkMonitorFilterAction, )
        multi_select = False


class InterfaceListTable(tables.DataTable):
    id = tables.Column("id", hidden=True)
    name = tables.Column("name",
                         verbose_name=_("Name"),
                         link="horizon:monitor:network_monitor:interface")
    description = tables.Column("description", verbose_name=_("Description"))
    desthost = tables.Column("desthost", verbose_name=_("DestHost"))
    status = tables.Column("status", verbose_name=_("Status"))

    def get_object_id(self, obj):
        return "%s-%s" % (obj.id, obj.desthost)

    class Meta:
        name = 'interface list'
        verbose_name = _("InterfaceList")
        multi_select = False

class SyslogListTable(tables.DataTable):
    id = tables.Column("id",
                       verbose_name=_('Id'),
                       link="horizon:monitor:network_monitor:detail",
                       filters=(filters.title,))
    time = tables.Column("time",
                         verbose_name=_('Time'),
                         filters=(filters.title,))
    type = tables.Column("type",
                         verbose_name=_('Type'),
                         filters=(filters.title,))
    priority = tables.Column("priority",
                             verbose_name=_('Priority'),
                             filters=(filters.title,))
    dev_type = tables.Column("dev_type", verbose_name=_('DevType'))
    interface = tables.Column("interface", verbose_name=_('Interface'))
    src_ip = tables.Column("src_ip", verbose_name=_('SrcIP'))
    dest_ip = tables.Column("dest_ip", verbose_name=_('DestIP'))

    def get_object_id(self, obj):
        return "%s" % (obj.id)

    class Meta:
        name = "syslogs"
        verbose_name = _("Syslogs")
        table_actions = (SyslogFilterAction, )
        multi_select = False

class MessageDetailTable(tables.DataTable):
    id = tables.Column("id", verbose_name=_('Id'), hidden=True)
    message = tables.Column("message", verbose_name=_("Message"))

    class Meta:
        name = "message_detail"
        verbose_name = _("MessageDetail")