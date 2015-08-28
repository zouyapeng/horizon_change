from django.utils.translation import ugettext_lazy as _

from horizon import tables

class EquipmentListAction(tables.FilterAction):
    name = "filter"

class EquipmentListTable(tables.DataTable):
    name = tables.Column("name", verbose_name=_("Name"))
    type = tables.Column("type", verbose_name=_("Type"))
    descrition = tables.Column("descrition", verbose_name=_("Descrition"))

    ip = tables.Column('ip',verbose_name=_("Ip"))
    status = tables.Column("status", verbose_name=_("Status"))

    class Meta:
        name = "equipment_list"
        verbose_name = _("Equipment List")
        table_actions = (EquipmentListAction, )