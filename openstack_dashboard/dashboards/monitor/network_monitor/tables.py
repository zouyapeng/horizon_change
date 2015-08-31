from django.utils.translation import ugettext_lazy as _

from horizon import tables

class NetworkMonitorFilterAction(tables.LinkAction):
    name = "filter"
    verbose_name = _("Filter")
    url = "horizon:monitor:network_monitor:filter"
    # classes = ("",)
    icon = "search"


class SyslogFilterAction(tables.FilterAction):
    name = "filter"


class EquipmentListTable(tables.DataTable):
    id = tables.Column("id", verbose_name=_("ID"), hidden=True)
    name = tables.Column("name",
                         verbose_name=_("Name"),
                         link="horizon:monitor:network_monitor:equipment")
    type = tables.Column("type", verbose_name=_("Type"))
    descrition = tables.Column("descrition", verbose_name=_("Descrition"))

    ip = tables.Column('ip',verbose_name=_("Ip"))
    status = tables.Column("status", verbose_name=_("Status"))

    def get_object_id(self, datum):
        return "%s" % (datum.id)

    class Meta:
        name = "equipment_list"
        verbose_name = _("Equipment List")
        table_actions = (NetworkMonitorFilterAction, )
        multi_select = True


class InterfaceListTable(tables.DataTable):
    id = tables.Column("id", hidden=True)
    name = tables.Column("name",
                         verbose_name=_("Name"),
                         link="horizon:monitor:network_monitor:interface")
    description = tables.Column("description", verbose_name=_("Description"))
    desthost = tables.Column("desthost", verbose_name=_("DestHost"))
    status = tables.Column("status", verbose_name=_("Status"))

    def get_object_id(self, obj):
        return "%s-%s-%s" % (obj.id, obj.desthost, obj.status)

    class Meta:
        name = 'interface list'
        verbose_name = _("InterfaceList")
        multi_select = False

class SyslogListTable(tables.DataTable):
    id = tables.Column("id", verbose_name=_('Id'))
    time = tables.Column("time", verbose_name=_('Time'))
    type = tables.Column("type", verbose_name=_('Type'))
    priority = tables.Column("priority", verbose_name=_('Priority'))
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