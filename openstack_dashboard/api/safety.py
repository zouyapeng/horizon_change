# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from time import strftime,localtime

ISOTIMEFORMAT = '%Y-%m-%d %X'

class H3clogs(object):
    def __init__(self, id, time, type, host, message):
        self.id = id
        self.time = time
        self.type = type
        self.host = host
        self.message = message

class Cisco(object):
    pass


def log_list():
    logs = []
    log1 = H3clogs(1, strftime(ISOTIMEFORMAT, localtime()), 'ARP', '192.168.0.1', u'An attack from MAC 0017-6f18-fd0f was detected on interface GE0/2.')
    log2 = H3clogs(2, strftime(ISOTIMEFORMAT, localtime()), 'CFGMAN', '192.168.0.1', u'Configuration is changed.')
    log3 = H3clogs(3, strftime(ISOTIMEFORMAT, localtime()), 'SHELL', '192.168.0.1', u'Trap 1.3.6.1.4.1.25506.2.2.1.1.3.0.1<hh3cLogIn>: login from VTY.')
    log4 = H3clogs(4, strftime(ISOTIMEFORMAT, localtime()), 'DPATTACK', '192.168.0.1', u'atckType(1016)=(9)ICMP Unreachable;rcvIfName(1023)=GigabitEthernet0/1;srcIPAddr(1017)=112.241.247.76;srcMacAddr(1021)= ;destIPAddr(1019)=58.247.8.188;destMacAddr(1022)= ;atckSpeed(1047)=0;atckTime_cn(1048)=20150810133115')
    log5 = H3clogs(5, strftime(ISOTIMEFORMAT, localtime()), 'WEB', '192.168.0.1', u'admin logged out from 192.168.7.93')

    logs.append(log1)
    logs.append(log2)
    logs.append(log3)
    logs.append(log4)
    logs.append(log5)
    return logs