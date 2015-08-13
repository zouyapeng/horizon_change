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
from horizon.utils import functions as utils

ISOTIMEFORMAT = '%Y-%m-%d %X'

class H3C(object):
    def __init__(self, id, time, type, host, message):
        self.id = id
        self.time = time
        self.type = type
        self.host = host
        self.message = message


class Cisco(object):
    pass


def get_logs_date(request_size = None, prev_marker = None,
                  marker = None, tag = None):
    '''
    :param request:
    :param paginate:
    :param request_size:
    :param tag:
    :return:
    '''
    logs = []
    syslogdb = MySQLdb.connect("localhost","syslog","123456","syslog")
    cursor = syslogdb.cursor()

    if marker:
        row = cursor.execute('SELECT * FROM SystemEvents WHERE (SysLogTag = {0} AND ID < {1})order by id DESC limit {2}'.format(tag, int(marker), request_size))
    elif prev_marker:
        row = cursor.execute('SELECT * FROM SystemEvents WHERE (SysLogTag = {0} AND ID < {1})order by id DESC limit {2}'.format(tag, int(prev_marker) + 20, request_size))
    else:
        row = cursor.execute('SELECT * FROM SystemEvents WHERE SysLogTag = {0} order by id DESC limit {1}'.format(tag, request_size))

    log_results = cursor.fetchmany(row)

    for log in log_results:
        logs.append(H3C(log[0], log[2], 'FILTER', log[6], log[7]))

    cursor.close()
    syslogdb.close()

    return logs

def log_list(request, prev_marker = None, marker = None, paginate = False):
    '''
    :return:syslog class list
    '''
    limit = 200
    page_size = utils.get_page_size(request)

    if paginate:
        request_size = page_size + 1
    else:
        request_size = limit

    logs = get_logs_date(request_size=request_size, prev_marker = prev_marker, marker = marker, tag="\'Newtouch-H3C\'" )
    # has_prev_data = False
    has_more_data = False
    if paginate:
        # images = list(itertools.islice(images_iter, request_size))
        # first and middle page condition
        if len(logs) > page_size:
            logs.pop(-1)
            has_more_data = True
            # middle page condition
            if marker is not None:
                pass
                # has_prev_data = True
        # last page condition
        elif marker is not None:
            pass
            # has_prev_data = True

    return (logs, has_more_data)