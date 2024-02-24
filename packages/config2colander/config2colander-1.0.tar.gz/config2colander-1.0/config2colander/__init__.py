import json
import logging
l = logging.getLogger(__name__)

import sys
PY2 = sys.version_info[0] == 2
if not PY2:
    unicode = str


from importlib import import_module

import colander
import deform
from deform.interfaces import FileUploadTempStore 
from .custominsert import simpleCSVParser,doNothing,multiJSONEncode
from .customfill import multiJSONDencode

import os

#tmpstore = FileUploadTempStore()
class MemoryTmpStore(dict):
    """ Instances of this class implement the
    :class:`deform.interfaces.FileUploadTempStore` interface"""

    def preview_url(self, uid):
        return None

tmpstore = MemoryTmpStore()

__customfillmapping = {
  'jsonarraydecode':multiJSONDencode
}

__custominsertmapping = {
  "simplecsv":simpleCSVParser,
  "donothing":doNothing,
  "multijsonencode":multiJSONEncode
}

def setCustomInsertMethod(key,callable):
  __custominsertmapping[key] = callable

__datatypemapping = {
  "string": colander.String,
  "hidden":(colander.String,deform.widget.HiddenWidget()),
  "text": (colander.String,deform.widget.TextAreaWidget() ),
  "integer": colander.Integer,
  "date":colander.Date,
  "list":colander.List,
  "file": (deform.FileData, deform.widget.FileUploadWidget(tmpstore)  ),
}

__enrichschema= {}
__custominsert={}
__customfill = {}

__customjsaction = {}


def getCustomJs(schema,name=None,default=[]):
  if name is None:
    name = schema.__class__.__name__
    l.info("no name provided, using {}".format(name))
  return __customjsaction.get(name,default)

def getCustomFill(schema,name=None,default={}):
  if name is None:
    name = schema.__class__.__name__
    l.info("no name provided, using {}".format(name))
  return __customfill.get(name,default)
  
def getCustomInsert(schema,name=None,default={}):
  if name is None:
    name = schema.__class__.__name__
    l.info("no name provided, using {}".format(name))
  return __custominsert.get(name,default)

def enrichSchema(schema,name=None):
  if name is None:
    name = schema.__class__.__name__
    l.info("no name provided, using {}".format(name))
    
  if name in __enrichschema:
    l.debug("enriching schema {}".format(name))
    __enrichschema[name](schema)
  else:
    l.info("no enrichment found for {}".format(name))
  return schema

def createClass(name,baseclass=object):
  class Foo(baseclass):
    pass

  Foo.__name__ = name
  Foo.__qualname__ = name
  Foo.__tablename__ = name
  return Foo

def createMultiInheritClass(name = "Foo",baseclasses = (),props = {} ):
  newclass= type(name,baseclasses,props)
  return newclass

def createMethod(mylambda):
  def method(self,*args):
    print (self.__class__.__name__,args)
    return mylambda(*args)

  return method

def createDeferedSelectSet(theset,datatype,propertyname,title,valkey=0,labelkey=1,options={}):
  def getData(theset):
    l.info("deferred get data from set {}".format(theset))
    res= [(row[valkey],row[labelkey]) for row in theset]
    return res

  @colander.deferred
  def select(node,kw):
    choices = getData(theset)
    multiple = ("multiselect" in options) and (options["multiselect"])
    return deform.widget.SelectWidget(values=choices,multiple=multiple)
    #return colander.deferred( deform.widget.SelectWidget(values=choices,multiple=False) )


  return colander.SchemaNode(
            datatype(),
            #colander.String(),
            widget = select(None,{}),
            name=propertyname,
            missing="",
            null_value="ppssvoid",
            title = title
            )


def createDeferedSelectTable(baseclass,datatype,propertyname,colval,collabel,title,options={}):
  def getData(session):
    l.info("deferred get data from table")
    cs = session.query(baseclass).all()
    res = [(getattr(c,colval),getattr(c,collabel) ) for c in cs]
    return res
    
  @colander.deferred
  def select(node,kw):
    l.info("in select")
    dbsession = kw.get("dbsession")
    choices = getData(dbsession)
    return deform.widget.SelectWidget(values=choices,multiple=False)

  datasrc = colander.deferred(select)
  l.info("deferred = {}".format(datasrc))
  return colander.SchemaNode(
            datatype(),
            #colander.String(),
            name=propertyname,
            null_value="",
            required="false",
            title = title
            )


def enricher(additionalfields):

  def addfields(schema):
    for x in additionalfields:
      schema.add(x)
    return schema


  return addfields

def createSchema(targetclass,fields):
  global __datatypemapping
  l.info("createSchema ({},{})".format(targetclass,fields))
  additionalfields = []
  custominsert = {}
  customfill = {}
  customjs = []
  for f in fields:
    l.info("create colander scheme for {}".format(f) )
    title = None
    fieldname = f[0]
    if len(f)>=3:
      params = f[2]

      if 'customfill' in params:
        if type(params['customfill']) == list:
          key,defaults = params['customfill']
        else:
          key = params['customfill']
          defaults={}

        if key is None:
          customfill[f[0]] = [None,{}]
        else:
          customfill[f[0]] = [__customfillmapping[key],defaults]
          #params['customfill']
      if 'custominsert' in params:
        if type(params['custominsert']) == list:
          key,defaults = params['custominsert']
        else:
          key = params['custominsert']
          defaults={}
        if key in __custominsertmapping:
          custominsert[f[0]] = (__custominsertmapping[key],defaults)
      if 'customjs' in params:
        fnlist = [params['customjs'],] if type(params['customjs']) != list else params['customjs']
        for basefn in fnlist:
          fn = os.path.join(basefn)
          if os.path.isfile(fn):
            with open(fn,'r') as ifile:
              customjs.append( ifile.read().replace("{fieldname}",fieldname) )
          else:
            l.error(f"{fn} is not a file wit cwd={os. getcwd()}")
      if 'title' in params:
        title = params['title']
    if title is None:
        title = f[0]
    if f[1] in __datatypemapping:
      if type(__datatypemapping [f[1]]) == tuple:
        datatype,wg = __datatypemapping [f[1]]
      else:
        datatype,wg = __datatypemapping [f[1]],None      
      ds = colander.SchemaNode(datatype(),missing=colander.drop,name=f[0],widget=wg,title=title)
      additionalfields.append( ds )
      l.info("***** column {} of type {}(origtype:{},widget:{}) added to class {}".format(f[0],ds,targetclass,datatype,wg)  )
    elif f[1] == "select":
      if len(f)>3:
        options = f[-1]
      else:
        options = {}
      if "datatype" in f[2]:
        datatype = __datatypemapping [f[2]["datatype"]]
      else:
        datatype = __datatypemapping["integer"]

      ##switch by type of select field
      # case tableclass
      if "tableclass" in f[2]:
        tc = getClassFromFullName(f[2]["tableclass"] )
        ds = createDeferedSelectTable(tc,datatype,f[0],f[2]["colval"],f[2]["collabel"],title,options)
        additionalfields.append(ds)
        ##setattr(targetclass,f[0],ds)
        l.info("***** column {} of type {} added to class {}".format(f[0],ds,targetclass)  )

      # case hardocoded dataset
      elif "dataset" in f[2]:
        ds = createDeferedSelectSet(
          f[2]["dataset"],
          datatype,
          f[0],
          title,
          f[2].get("colval",0),
          f[2].get("collabel",1),
          options)
        additionalfields.append(ds)
        l.info("***** column {} of type {} added to class {}".format(f[0],ds,targetclass)  )
    

  __enrichschema[targetclass.__name__] = enricher(additionalfields)
  __custominsert[targetclass.__name__] = custominsert
  __customfill[targetclass.__name__] = customfill
  __customjsaction[targetclass.__name__] = customjs


def getClassFromFullName(fullname):
  try:
    baseclasspath= fullname.split(".")
    classmodule = import_module(".".join(baseclasspath[:-1] ))
    baseclass = getattr(classmodule,baseclasspath[-1])
  except Exception as e:
    l.exception("something went wrong prcessing '{}': {}".format(fullname,e) )
    raise e
  return baseclass

def createSchemaFromJson(fn):
  with (open(fn,'r',encoding='utf-8')) as fd:
    jsonmodel = json.load(fd)

  for e in jsonmodel.get("extensions",[]):
    l.info("configuring extension {}".format(e)  )

    baseclasspath= e["name"].split(".")
    classmodule = import_module(".".join(baseclasspath[:-1] ))
    baseclass = getattr(classmodule,baseclasspath[-1])
    createSchema(baseclass, e.get("fields",[]))
  pass

configured = False
here = "./"
def includeme(config):
    global configured
    global here
    if configured:
        return
    configured = True
    l.debug("configuring config2colander")
    settings = config.get_settings()
    myfile = settings.get("config2colander.json","")
    here = settings.get("confdir",here)
    l.info(f"************ here is {here}")
    if myfile:
      createSchemaFromJson(myfile)

if __name__ == '__main__':
  createSchemaFromJson(sys.argv[-1])

