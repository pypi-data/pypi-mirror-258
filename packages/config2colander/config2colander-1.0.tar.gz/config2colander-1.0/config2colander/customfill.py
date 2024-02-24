import json
import logging
l = logging.getLogger(__name__)



def multiJSONDencode(target,**kwargs):
  field = kwargs.get("field")  
  vals = getattr(target,field)
  if vals is None:
    vals = "[]"
  vals = json.loads(vals)
  return [str(c) for c in vals]
  
  