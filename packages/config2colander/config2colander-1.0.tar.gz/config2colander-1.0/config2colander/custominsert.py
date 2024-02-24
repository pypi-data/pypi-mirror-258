from ppss_pyramidutils import FileManager
import csv,json
import logging
l = logging.getLogger(__name__)

def doNothing(paramname,fileobj,**kwargs):
  return None

def multiJSONEncode(paramname,fieldvalue,**kwargs):
  l.warn("multiJSONEncode({},{},{})".format(paramname,fieldvalue,kwargs))
  v = json.dumps(fieldvalue)
  target = kwargs.get('target',None)
  if target is None:
    return None
  setattr(target,kwargs.get("field"),v)
  return None

def simpleCSVParser(paramname,fileobj,**kwargs):
  #l.warn("************************************ eccomi {}".format(fileobj))
  target = kwargs.get('target',None)
  if target is None or fileobj is None:
    return None
  infile = fileobj['fp']
  name = str(fileobj['filename'])
  #l.warn("name={}, file={}".format(name,dir(infile) ) ) 
  #path = FileManager.moveToDestination(
  #    FileManager.saveToTmp(fileobj),
  #    name + ".csv")
  output_file = open('/tmp/pippo.file', 'wb')
  while True:
    data = infile.read(2<<16)
    if not data:
        break
    output_file.write(data)
  output_file.close()
  #with open('/tmp/pippo.file','r',encoding="utf-8") as infile:
  rows = []
  with open('/tmp/pippo.file','r',encoding="utf-8") as infile:
    reader = csv.reader(infile)
    h= next(reader)
    l.warn("*****header:{}".format(h))
    while True:
      try:
        row=next(reader)
        if row:
          rows.append(row)
        else:
          break
      except Exception as e:
        l.info("end of iteration:{}".format(e))
        break
  l.info("+++++I got {} to save".format(rows))
  setattr(target,kwargs.get("csvfield","labeltext"),
    json.dumps(
      {
      "header":h,
      "data":rows
    })
  )
  #setattr(target,params.get("header","header"),json.dump(h))
  #setattr(target,params.get("data","data"),json.dump(rows))

  return json.dumps(
    {
      "header":h,
      "rows":rows
    })