#
#  wb_drupal_schema_grt.py
#  MySQLWorkbench
#
#  Edit and completed by zkday on 24/May/2011
#

import re

# import the wb module, must be imported this way for the automatic module setup to work
from wb import *
# import the grt module
import grt

# define this Python module as a GRT module
ModuleInfo = DefineModule(name= "CSVGenarel", author= "zkday", version="0.1")

def getColumnDef(col):
  """docstring for getColumnDef"""
  '''opts = [] '''
  p = re.search('([a-z]+)(?:\(([0-9]+)\))?', col.formattedType.lower())
  mtype = p.group(1)
  
  type = mtype
  comment = ""
  notnull = ""

  if col.isNotNull:
    notnull = "TRUE"
  else:
    notnull = ""
  
  if col.comment:
    comment = col.comment
  else:
    comment = ""

  if col.length > -1:
    type += "(" + str(col.length) + ")"
    '''''opts.insert(1, "'length' => %d" % col.length)'''
  
  cols =  "," + col.name + "," + type + "," + notnull + "," + comment + ",\n"
  return cols
	


def getTableSchema(table):
  """Print table specifications with drupal schema structure"""
  ret = ''
  fields, indexes, uniques, primaryKeys = [], [], [], []
  ret = table.name + ",FieldName,Type,NOTNULL,Descriptions,FieldAPI\n"
  for column in table.columns:
    ret += getColumnDef(column)

  ret += "\n"
 
  return ret

@ModuleInfo.plugin("wb.catalog.util.CSV", caption= "Export to CSV - All Tables", input= [wbinputs.currentCatalog()], pluginMenu= "Catalog")
@ModuleInfo.export(grt.INT, grt.classes.db_Catalog)
def PrintDrupalSchemas(catalog):
  output = ''
  for schema in catalog.schemata:
    for table in schema.tables:
      output += getTableSchema(table)
      output += "\n"
  
  c_title = 'Copy to clipboard?'
  c_message = 'The csv file be viewed at Output Window, but if you want, you can copy to clipboard.'
  if grt.modules.Workbench.confirm(c_title, c_message):
    grt.modules.Workbench.copyToClipboard(output)
  
  print output

  return 0
