import arcpy, updateGRB

class Toolbox(object):
    def __init__(self):
        self.label =  "GRB update tools"
        self.alias  = "GRB_Update"

        # List of tool classes associated with this toolbox
        self.tools = [Update_GRB] 

class Update_GRB(object):
    def __init__(self):
        self.label       = "Update GRB with Diff-files"
        self.description = """Update GRB using diffence shapefiles downloaded from the AGIV site, they must be unzipted. 
 ( https://download.agiv.be/Producten/Detail?id=1&title=GRBgis )"""

    def getParameterInfo(self):
        #Define parameter definitions

        # Input Features parameter
        grb_workspace = arcpy.Parameter(
            displayName="GRB Workspace",
            name="grb_workspace",
            datatype="DEWorkspace",
            parameterType="Required",
            direction="Input")

        # Sinuosity Field parameter
        grb_update_dir = arcpy.Parameter(
            displayName="Folder with GRB-dif-files as downloaded from AGIV",
            name="grb_update_dir",
            datatype="DEFolder",
            parameterType="Required",
            direction="Input")
        
        # Derived Output Features parameter
        grb_prefix = arcpy.Parameter(
            displayName="Prefix of GRB-entities Features classes in database",
            name="grb_prefix",
            datatype="GPString",
            parameterType="Optional",
            direction="Input")
        grb_prefix.value = "sdedactua.THEMA.GRB_"

        parameters = [grb_workspace, grb_update_dir, grb_prefix]
        
        return parameters

    def execute(self, parameters, messages):
        grb_workspace  = parameters[0].valueAsText
        grb_update_dir = parameters[1].valueAsText
        grb_prefix     = parameters[2].valueAsText
   
        entities = ['ANO','ADP','GBA','GBG','KNW','GVP','GVL','MKP','MKV','SBN','TRN','WBN', 
                    'WGA','WGO','WGR','WKN','WLAS','WLI','WPI','WRI','WRL','WTI','WTZ','WVB']

        updateGRB.updateWorkspace(grb_workspace, grb_update_dir, grb_prefix, entities)
        