# ELBE - Debian Based Embedded Rootfilesystem Builder
# Copyright (C) 2013  Linutronix GmbH
#
# This file is part of ELBE.
#
# ELBE is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ELBE is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ELBE.  If not, see <http://www.gnu.org/licenses/>.

import os
from subprocess import Popen, PIPE, STDOUT
import logging

log_cmd_msg = """CMD: %(cmd)s
%(sep)s
IN:
%(stdin)s
%(sep)s
OUT:
%(stdout)s
%(sep)s
ERR:
%(stderr)s
%(sep)s
RET: %(retval)i
"""
sep = '-'*80


class CommandError(Exception):
    def __init__(self, cmd, returncode):
        Exception.__init__(self)
        self.returncode = returncode
        self.cmd = cmd

    def __repr__(self):
        return "Error: %d returned from Command %s" % (
                                             self.returncode, self.cmd)

def system(cmd, allow_fail=False):
    ret = os.system(cmd)

    if ret != 0:
        if not allow_fail:
            raise CommandError(cmd, ret)


def command_out(cmd, input=None):
    log = logging.getLogger(__name__)
    log.debug("Execute command '%(cmd)s'", dict(cmd=cmd))
    if input is None:
        p = Popen(cmd, shell=True, stdout=PIPE, stderr=STDOUT )
        output, stderr = p.communicate()
    else:
        p = Popen(cmd, shell=True, stdout=PIPE, stderr=STDOUT, stdin=PIPE)
        output, stderr = p.communicate(input=input)
    if p.returncode == 0:
        log.info(log_cmd_msg, dict(sep=sep, cmd=cmd, retval=p.returncode, stdin=input, stdout=output, stderr=stderr))
    else:
        log.error(log_cmd_msg, dict(sep=sep, cmd=cmd, retval=p.returncode, stdin=input, stdout=output, stderr=stderr))

    return p.returncode, output

def system_out(cmd, input=None, allow_fail=False):
    code, out = command_out(cmd,input)

    if code != 0:
        if not allow_fail:
            raise CommandError(cmd, code)

    return out

def command_out_stderr(cmd, input=None):
    log = logging.getLogger(__name__)
    log.debug("Execute command '%(cmd)s'", dict(cmd=cmd))
    if input is None:
        p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE )
        output, stderr = p.communicate()
    else:
        p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE, stdin=PIPE)
        output, stderr = p.communicate(input=input)
    if p.returncode == 0:
        log.info(log_cmd_msg, dict(sep=sep, cmd=cmd, retval=p.returncode, stdin=input, stdout=output, stderr=stderr))
    else:
        log.error(log_cmd_msg, dict(sep=sep, cmd=cmd, retval=p.returncode, stdin=input, stdout=output, stderr=stderr))

    return p.returncode, output, stderr

def system_out_stderr(cmd, input=None, allow_fail=False):
    code, out, err = command_out(cmd,input)

    if code != 0:
        if not allow_fail:
            raise CommandError(cmd, code)

    return out, err
