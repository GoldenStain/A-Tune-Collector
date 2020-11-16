#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Copyright (c) 2019 Huawei Technologies Co., Ltd.
# A-Tune is licensed under the Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan PSL v2.
# You may obtain a copy of Mulan PSL v2 at:
#     http://license.coscl.org.cn/MulanPSL2
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY OR FIT FOR A PARTICULAR
# PURPOSE.
# See the Mulan PSL v2 for more details.
# Create: 2019-10-29

"""
The sub class of the monitor, used to collect the storage stat info.
"""
import inspect
import logging
import subprocess
import getopt
import re
from ..common import Monitor

LOGGER = logging.getLogger(__name__)


class IoStat(Monitor):
    """To collect the storage stat info"""
    _module = "STORAGE"
    _purpose = "STAT"
    _option = "-xmt {int} 2"

    def __init__(self, user=None):
        Monitor.__init__(self, user)
        self.__cmd = "iostat"
        self.__interval = 1
        self.format.__func__.__doc__ = Monitor.format.__doc__ % ("json")
        self.decode.__func__.__doc__ = Monitor.decode.__doc__ % (
            "--device=x, --fields=dev/rs/ws/rMBs/wMBs/"
            "rrqms/wrqms/rrqm/wrqm/r_await/w_await/aqu-sz/rareq-sz/wareq-sz/svctm/util")

    def _get(self, para=None):
        """
        get the result of the operation by iostat
        :param para:  command line argument
        :returns output:  the result returned by the command
        """
        if para is not None:
            opts, _ = getopt.getopt(para.split(), None, ['interval='])
            for opt, val in opts:
                if opt in '--interval':
                    if val.isdigit():
                        self.__interval = int(val)
                    else:
                        err = ValueError(
                            "Invalid parameter: {opt}={val}".format(
                                opt=opt, val=val))
                        LOGGER.error("%s.%s: %s", self.__class__.__name__,
                                     inspect.stack()[0][3], str(err))
                        raise err
                    continue

        output = subprocess.check_output(
            "{cmd} {opt}".format(
                cmd=self.__cmd,
                opt=self._option.format(
                    int=self.__interval)).split())
        return output.decode()

    def format(self, info, fmt):
        """
        format the result of the operation
        :param info:  content that needs to be converted
        :param fmt:  converted format
        :returns output:  converted result
        """
        if fmt == "json":
            o_json = subprocess.check_output(
                "{cmd} -o JSON {opt}".format(
                    cmd=self.__cmd, opt=self._option.format(
                        int=self.__interval)).split())
            return o_json.decode()
        return Monitor.format(self, info, fmt)

    def decode(self, info, para):
        """
        decode the result of the operation
        :param info:  content that needs to be decoded
        :param para:  command line argument
        :returns ret:  operation result
        """
        if para is None:
            return info

        keys = []
        dev = "sd.*?"
        ret = ""
        resplitobj = re.compile(r'\s*\n')
        device_data = {}

        opts, _ = getopt.getopt(para.split(), None, ['nic=', 'fields=', 'device='])
        for opt, val in opts:
            if opt in '--device':
                dev = val
                continue
            if opt in '--fields':
                keys.append(val)
                continue

        rows_contents = resplitobj.split(info)
        dev = "Device|" + dev
        search_obj = []
        pattern = re.compile("^(" + dev + r").+", re.ASCII)
        for row in rows_contents:
            if pattern.match(row):
                search_obj.append([data for data in row.split()])

        if len(search_obj) < 3:
            err = LookupError("Fail to find data for {}".format(dev))
            LOGGER.error("%s.%s: %s", self.__class__.__name__,
                         inspect.stack()[0][3], str(err))
            raise err

        for i, _ in enumerate(search_obj[0]):
            device_data[re.sub("/|%", "", search_obj[0][i])] = search_obj[-1][i]
        for i in keys:
            ret = ret + " " + device_data[i]
        return ret
