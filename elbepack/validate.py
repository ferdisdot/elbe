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
import sys
import elbepack
from lxml import etree
from lxml.etree import XMLParser,parse

def validate_xml(fname):
    schema_file = os.path.join( elbepack.__path__[0], "dbsfed.xsd" )
    parser = XMLParser(huge_tree=True)
    schema_tree = etree.parse(schema_file)
    schema = etree.XMLSchema(schema_tree)

    try:
        xml = parse(fname,parser=parser)

        if schema.validate(xml):
            return True
    except etree.XMLSyntaxError:
        import logging
        logger = logging.getLogger(__name__)
        leffer.exception( "XML Parse error")
        print "XML Parse error"
        print str(sys.exc_info()[1])
        return False
    except:
        import logging
        logger = logging.getLogger(__name__)
        leffer.exception( "Unknown Exception during validation")
        print "Unknown Exception during validation"
        print sys.exc_info()[1]
        return False

    # We have an error... lets print the log.

    for err in schema.error_log:
        print "%s:%d error %s" % (err.filename, err.line, err.message)

    return False

