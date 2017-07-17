import arcpy , glob, os.path, argparse
from grbEntity import grbEntity

def main():
   GRB_UPDATE_DIR = r"E:\work\grb\Shapefile"
   GRB_WORKSPACE = r"E:\work\grb\grb.gdb"
   GRB_PREFIX = r'GRB_'

   GRB_ENTITY_NAMES = ['ANO','ADP','GBA','GBG','KNW','GVP','GVL','MKP','MKV','SBN','TRN','WBN', 
                       'WGA','WGO','WGR','WKN','WLAS','WLI','WPI','WRI','WRL','WTI','WTZ','WVB']

   parser = argparse.ArgumentParser()
   parser.add_argument("--GRB_WORKSPACE", help="the GRB workspace to update")
   parser.add_argument("--GRB_UPDATE_DIR", help="the folder that cntians the GRB diff-files")
   parser.add_argument("--GRB_PREFIX",  default=GRB_PREFIX, 
                       help="The prefix the GRB_documents have in the database, optional but recommended, default 'GRB_'")
   args = parser.parse_args()
   
   if args.GRB_WORKSPACE: GRB_WORKSPACE = args.GRB_WORKSPACE
   if args.GRB_UPDATE_DIR: GRB_UPDATE_DIR = args.GRB_UPDATE_DIR
   if args.GRB_PREFIX: GRB_PREFIX = args.GRB_PREFIX
   
   updateWorkspace(GRB_WORKSPACE, GRB_UPDATE_DIR, GRB_PREFIX, GRB_ENTITY_NAMES)

def updateWorkspace(grbWorkspace, updateDir, prefix="", grbEntities=[]):
   "update all the features with prefix in grbWorspace with all the diff-files form updatedir for entities in list"
   arcpy.env.workspace = grbWorkspace
   inputEntities = [n for n in arcpy.ListFeatureClasses( prefix + "*" ) if not n.endswith("_RVW") ]

   #start editsession, so database will roll back on error
   edit = arcpy.da.Editor(grbWorkspace)
   edit.startEditing(False, True)
   
   for entityName in grbEntities:
       entityFC =  findEntity(inputEntities , entityName)
       entityDel = glob.glob( os.path.join( updateDir, entityName + '*Del.shp' ) )
       entityAdd = glob.glob( os.path.join( updateDir, entityName + '*Add.shp' ) )

       if entityFC:
          edit.startOperation()
          grbUpdate(entityFC, entityAdd, entityDel)
          edit.stopOperation()
   
   #end editsession
   edit.stopEditing(True)

def grbUpdate(entityFC, entityAdd, entityDel):
    ""
    arcpy.AddMessage( "starting " + entityFC + " ..." )
    entitity = grbEntity( entityFC )
    for grbDel in entityDel:
      count = int( arcpy.GetCount_management(grbDel)[0] )
      if count > 0: entitity.updateFeaturesFromFC( grbDel )
    for grbAdd in entityAdd:
      count = int( arcpy.GetCount_management(grbDel)[0] )
      if count > 0: entitity.insertFeaturesFromFC( grbAdd )
    arcpy.AddMessage( "... done")

def findEntity( inputEntities, entityName ):
    "" 
    entityFCs =  [ n for n in inputEntities if entityName in n.upper()]  
    entityFC = None
    msg = ""  
    if len(entityFCs) == 1: 
       entityFC = entityFCs[0]
    elif  len(entityFCs) == 0:
       msg = entityName + " could not be found"
    else:
       msg = entityName + " multiple entities found: " + ", ".join(entityFCs)

    if msg: arcpy.AddWarning( msg )
    return entityFC
       
if __name__ == "__main__":
   main()