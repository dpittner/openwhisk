#!/usr/bin/env python

#
# Copyright 2015-2016 IBM Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

##
# Helper methods for whisk properties
##

import os
import pkg_resources

def propfile(base):
    if base != '':
        filename = '%s/whisk.properties' % base
        if os.path.isfile(filename) and os.path.exists(filename):
            return filename
        else:
            parent = os.path.dirname(base)
            return propfile(parent) if parent != base else ''
    else:
        return ''

def importPropsIfAvailable(filename):
    thefile = open(filename, 'r') if os.path.isfile(filename) and os.path.exists(filename) else []
    return importProps(thefile)

def importProps(stream):
    props = {}
    for line in stream:
        parts = line.split('=')
        if len(parts) >= 1:
            key = parts[0].strip()
        if len(parts) >= 2:
            val = parts[1].strip()
        if key != '' and val != '':
            props[key.upper().replace('.','_')] = val
        elif key != '':
            props[key.upper().replace('.','_')] = ''
    return props

#
# Returns a triple of (length(requiredProperties), requiredProperties, deferredInfo)
# prints a message if a required property is not found
#
def checkRequiredProperties(requiredPropertiesByName, properties):
    requiredPropertiesByValue = [ getPropertyValue(key, properties) for key in requiredPropertiesByName ]
    requiredProperties = dict(zip(requiredPropertiesByName, requiredPropertiesByValue))
    invalidProperties = [ key for key in requiredPropertiesByName if requiredProperties[key] == None ]
    deferredInfo = ''
    for key, value in requiredProperties.items():
        if value == None or value == '':
            print 'property "%s" not found in environment or property file' % key
        else:
            deferredInfo += 'using %(key)s = %(value)s\n' % {'key': key, 'value': value}
    return (len(invalidProperties) == 0, requiredProperties, deferredInfo)

def getPropertyValue(key, properties):
    evalue = os.environ.get(key)
    value  = evalue if evalue != None and evalue != '' else properties[key] if key in properties else None
    return value
