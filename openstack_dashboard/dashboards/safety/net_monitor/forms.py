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

"""
Views for managing images.
"""
from django.conf import settings
from django.forms import ValidationError  # noqa
from django.forms.widgets import HiddenInput  # noqa
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon import messages

from openstack_dashboard.api import safety
from openstack_dashboard import policy

class AdvancedFilterForm(forms.SelfHandlingForm):
    priority = forms.ChoiceField(
        label=_('Priority'),
        required=False,
        choices=[('Emergency', _('Emergency')),
                 ('Alert', _('Alert')),
                 ('Critical', _('Critical')),
                 ('Error', _('Error')),
                 ('Warning', _('Warning')),
                 ('Notice', _('Notice')),
                 ('Informational', _('Informational')),
                 ('Debug', _('Debug'))])

    attack_type = forms.ChoiceField(
        label=_('Attack Type'),
        required=False,
        choices=[('SHELL', _('SHELL')),
                 ('DPATTACK', _('DPATTACK')),
                 ('FILTER', _('FILTER')),
                 ('DPURPF', _('DPURPF')),
                 ('ARP', _('ARP')),
                 ('WEB', _('WEB')),
                 ('SOCKET', _('SOCKET')),
                 ('CFGMAN', _('CFGMAN')),
                 ('CFM', _('CFM'))]
    )

    srcip = forms.CharField(max_length=15,
                            label=_('SrcIP'),
                            required=False)

    destip = forms.CharField(max_length=15,
                            label=_('DestIP'),
                            required=False)

    def __init__(self, request, *args, **kwargs):
        super(AdvancedFilterForm, self).__init__(request, *args, **kwargs)

    def clean(self):
        return super(AdvancedFilterForm, self).clean()

    def handle(self, request, data):
        meta = {'priority': data['priority'],
                'attack_type': data['attack_type'],
                'srcip': (data['srcip']),
                'destip': (data['destip'])}

        try:
            # image = api.glance.image_create(request, **meta)
            filter = []
            messages.success(request,
                _('--------------------'))
            return filter
        except Exception:
            exceptions.handle(request, _('Unable to create new image.'))

