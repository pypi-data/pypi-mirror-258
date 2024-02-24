# (c) Copyright 2022 CERN for the benefit of the LHCb Collaboration. 
#                                                                             
# This software is distributed under the terms of the GNU General Public
# Licence version 3 (GPL Version 3), copied verbatim in the file "LICENCE".
#                                                                             
# In applying this licence, CERN does not waive the privileges and immunities
# granted to it by virtue of its status as an Intergovernmental Organization  
# or submit itself to any jurisdiction.

from typing import Optional

def serialize_to_xml_etree(name: Optional[str] = None, **kwargs):
  """Serialize a configuration to XML using ElementTree format.

  """
  import xml.etree.ElementTree as e3

  if name is None:
    return e3.Element("root")

  def serialize(parent_node):
    node = e3.SubElement(parent_node, name)
    flatten_attrs = {
        k: ";".join(v) if isinstance(v, (tuple, list, set)) else str(v)
        for k, v in kwargs.items()
        }

    e3.SubElement(node, name, attrs=flatten_attrs)

    return node

  return serialize


