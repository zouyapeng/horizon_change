# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from django.utils.translation import ugettext_lazy as _

from horizon import tables


SERVICE_ENABLED = "enabled"
SERVICE_DISABLED = "disabled"

SERVICE_STATUS_DISPLAY_CHOICES = (
    (SERVICE_ENABLED, _("Enabled")),
    (SERVICE_DISABLED, _("Disabled")),
)


class SyslogsFilterAction(tables.FilterAction):
    filter_field = 'id'

    def filter(self, table, syslogs, filter_string):
        q = filter_string.lower()

        def comp(syslogs):
            attr = getattr(syslogs, self.filter_field, '')
            if attr is not None and q in attr.lower():
                return True
            return False

        return filter(comp, syslogs)


class SubServiceFilterAction(SyslogsFilterAction):
    filter_field = 'time'


# class SyslogsAdvancedFilterAction(tables.LinkAction):
#     name = "advanced filter"
#     verbose_name = _("Advanced Filter")
#     url = "horizon:safety:net_monitor:filter"
#     classes = ("ajax-modal",)
    # icon = "search"
    # icon = "pencil"
    # policy_rules = (("image", "add_image"),)


class SyslogsTable(tables.DataTable):
    id = tables.Column("id", verbose_name=_('Id'), link="horizon:safety:net_monitor:detail")
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
        table_actions = (SyslogsFilterAction, )
        multi_select = False


class SyslogsDetailTable(tables.DataTable):
    id = tables.Column("id", hidden=True)
    message = tables.Column("message", verbose_name=_("Message"))

    class Meta:
        name = 'syslog detail'
        verbose_name = _("Syslog Detail")
        multi_select = False


class InterfaceTable(tables.DataTable):
    id = tables.Column("id", hidden=True)
    name = tables.Column("name",
                         verbose_name=_("Name"),
                         link="horizon:safety:net_monitor:interface")
    description = tables.Column("description", verbose_name=_("Description"))
    desthost = tables.Column("desthost", verbose_name=_("DestHost"))
    status = tables.Column("status", verbose_name=_("Status"))

    def get_object_id(self, obj):
        return "%s-%s-%s" % (obj.id, obj.desthost, obj.status)

    class Meta:
        name = 'interface'
        verbose_name = _("Interface")
        multi_select = False