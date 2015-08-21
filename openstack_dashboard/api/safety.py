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

import MySQLdb
import netsnmp
from uuid import uuid4

from horizon.utils import functions as utils

MYSQL_HOST = 'localhost'
MYSQL_SYSLOG_DB_NAME = 'syslog'
MYSQL_SYSLOG_DB_USER = 'syslog'
MYSQL_SYSLOG_DB_PASSWD = '123456'

ifDescr = ".1.3.6.1.2.1.2.2.1.2"
ifType = ".1.3.6.1.2.1.2.2.1.3"
ifSpeed = ".1.3.6.1.2.1.2.2.1.5"
ifAdminStatus = ".1.3.6.1.2.1.2.2.1.7"
ifOperStatus = ".1.3.6.1.2.1.2.2.1.8"

def get_syslogs(limit = None,
                marker = None,
                system_tag = None,
                interface = None):
    '''
    Get syslogs from mysql
    :param limit:
    :param marker:
    :param system_tag:
    :return:
    '''
    syslogs = []
    syslogdb = MySQLdb.connect(MYSQL_HOST,MYSQL_SYSLOG_DB_USER,
                               MYSQL_SYSLOG_DB_PASSWD,MYSQL_SYSLOG_DB_NAME)
    cursor = syslogdb.cursor()

    if marker:
        sql = "SELECT * FROM SystemEvents WHERE (SysLogTag = {0} AND Priority <= 4 AND ID < {1}) ORDER BY id DESC limit {2}"
        row = cursor.execute(sql.format(system_tag, int(marker), limit))
    else:
        sql = "SELECT * FROM SystemEvents WHERE (SysLogTag = {0} AND Priority <= 4) order by id DESC limit {1}"
        row = cursor.execute(sql.format(system_tag, limit))

    if row:
        results = cursor.fetchmany(row)
        for syslog in results:
            tag, sep, message  = syslog[7].partition(":")

            if (-1 != tag.find("message repeated")):
                message = message.strip().lstrip("[").rstrip("]")
                tag, sep, message = message.partition(":")

            type = tag.strip().lstrip("%%10")
            message_list = message.split(";")
            dev_type_value = ""
            interface_type_value = ""
            srcip_type_value = ""
            destip_type_value = ""
            for message in message_list:
                if -1 != message.find("DEV_TYPE"):
                    tag, sep , dev_type_value = message.partition("=")
                    dev_type_value = dev_type_value.strip()
                elif -1 != message.find("atckType"):
                    tag, sep , atck_type_value = message.partition("=")
                    atck_type_value = atck_type_value.strip()
                elif -1 != message.find("rcvIfName"):
                    tag, sep , interface_type_value = message.partition("=")
                    interface_type_value = interface_type_value.strip()
                elif -1 != message.find("srcIPAddr"):
                    tag, sep , srcip_type_value = message.partition("=")
                    srcip_type_value = srcip_type_value.strip()
                elif -1 != message.find("srcMacAddr"):
                    tag, sep , srcmac_type_value = message.partition("=")
                    srcmac_type_value = srcmac_type_value.strip()
                elif -1 != message.find("destIPAddr"):
                    tag, sep , destip_type_value = message.partition("=")
                    destip_type_value = destip_type_value.strip()
                elif -1 != message.find("destMacAddr"):
                    tag, sep , destmac_type_value = message.partition("=")
                    destmac_type_value = destmac_type_value.strip()
                else:
                    pass

            syslog_dict = dict(id=syslog[0], time=syslog[2], priority=syslog[5], host=syslog[6], message=syslog[7],
                               type=type, dev_type=dev_type_value, interface=interface_type_value,
                               src_ip=srcip_type_value, dest_ip=destip_type_value)
            syslogs.append(Logs(syslog_dict))

    cursor.close()
    syslogdb.close()

    return syslogs

class Logs(object):
    def __init__(self, dict):
        self.id = dict['id']
        self.time = dict['time']
        self.type = dict['type']
        self.host = dict['host']
        if 0 == dict['priority']:
            self.priority = "Emergency"
        elif 1 == dict['priority']:
            self.priority = "Alert"
        elif 2 == dict['priority']:
            self.priority = "Critical"
        elif 3 == dict['priority']:
            self.priority = "Error"
        elif 4 == dict['priority']:
            self.priority = "Warning"
        elif 5 == dict['priority']:
            self.priority = "Notice"
        elif 6 == dict['priority']:
            self.priority = "Informational"
        elif 7 == dict['priority']:
            self.priority = "Debug"
        else:
            self.priority = None
        self.interface = dict['interface']
        self.src_ip = dict['src_ip']
        self.dev_type = dict['dev_type']
        self.dest_ip = dict['dest_ip']
        self.message = dict['message']

    def __str__(self):
        return "%s-%s-%s" % (self.time, self.type, self.priority)

def logs_list(request,
              marker = None,
              paginate = False,
              interface = None):
    '''
    :return:syslog class list
    '''
    limit = 200
    page_size = utils.get_page_size(request)

    if paginate:
        request_size = page_size + 1
    else:
        request_size = limit

    syslogs = get_syslogs(limit=request_size,
                          marker = marker,
                          system_tag="\'Newtouch-H3C\'" ,
                          interface = interface)
    # has_prev_data = False
    has_more_data = False
    if paginate:
        # images = list(itertools.islice(images_iter, request_size))
        # first and middle page condition
        if len(syslogs) > page_size:
            syslogs.pop(-1)
            has_more_data = True
            # middle page condition
            if marker is not None:
                pass
                # has_prev_data = True
        # last page condition
        elif marker is not None:
            pass
            # has_prev_data = True

    return (syslogs, has_more_data)

class LogDetail(object):
    def __init__(self, message):
        self.message = message
        self.id = 1

def logs_detail(request, id):
    message = []
    syslogdb = MySQLdb.connect(MYSQL_HOST,MYSQL_SYSLOG_DB_USER,
                               MYSQL_SYSLOG_DB_PASSWD,MYSQL_SYSLOG_DB_NAME)
    cursor = syslogdb.cursor()
    sql = "SELECT * FROM SystemEvents WHERE ID = {0}"
    cursor.execute(sql.format(id))
    result = cursor.fetchone()

    message.append(LogDetail(result[7].strip().lstrip("%%10")))

    cursor.close()
    syslogdb.close()
    return message


class InterFace(object):
    def __init__(self, name, status):
        self.id = uuid4()
        self.name = name
        self.description = None
        if '1' == status:
            self.status = "Connected"
        elif '2' == status:
            self.status = "Not Connected"
        else:
            self.status = "Unknown"

def get_interface(request):
    interfaces = []
    interfaces_name = netsnmp.snmpwalk(ifDescr,
                                       Version = 2,
                                       DestHost = "192.168.202.1",
                                       Community = "newtouch")
    interfaces_status = netsnmp.snmpwalk(ifOperStatus,
                                         Version = 2,
                                         DestHost = "192.168.202.1",
                                         Community = "newtouch")

    for interface in interfaces_name:
        if (-1 == interface.find("NULL")) & (-1 == interface.find("Vlan")):
            interfaces.append(InterFace(interface, interfaces_status[interfaces_name.index(interface)]))

    return interfaces
