import arcpy

class grbEntity(object):
    "Class to represent a single GRB-Entity-feature class"
    def __init__(self, fc):
        self.fc = fc
        self.fields = self.listFields(fc, [u'OBJECTID', 'OID', 'FID', 'SHAPE', u'SHAPE_Length', u'SHAPE_Area'] )

    def listFields(self, fc, exclude=[] ):
       "return all fields of th feature class"
       ds = arcpy.Describe( fc )
       fields = [n.name for n in ds.fields if n.name not in exclude]     
       return ['SHAPE@'] + fields

    def removeFeaturesWithID(self, UIDNs = [] ):
        "remove all features with UIDN in array "
        with arcpy.da.UpdateCursor(self.fc, "UIDN") as cursor:
            for row in cursor: 
               if row[0] in UIDNs: cursor.deleteRow()

    def insertFeaturesFromFC(self, updateFC ):
        "insert features in grbEntity from feature class updateFC, if field with UIDN not exists"
        ##TODO: replace with append?
        #find all fields that are present in both files
        fields = [n for n in self.listFields(updateFC) if n in self.fields ]
        
        #make sure UIDN is the first value
        fields.remove("UIDN")
        fields = ["UIDN"] + fields

        with arcpy.da.InsertCursor(self.fc, fields) as cursor:
           for row in arcpy.da.SearchCursor(updateFC, fields):
              qry = '"UIDN" = ' + str( int( row[0] )) 
              duplicates= len([r for r in arcpy.da.SearchCursor(self.fc,"UIDN",qry)])
              if duplicates == 0: cursor.insertRow(row)

    def updateFeaturesFromFC(self, updateFC):
        "Update the grbEntity with features from updateFC "
        #find all fields that are present in both files
        fields = [n for n in self.listFields(updateFC) if n in self.fields ]

        #make sure UIDN is the first value
        fields.remove("UIDN")
        fields = ["UIDN"] + fields
 
        for srow in arcpy.da.SearchCursor(updateFC, fields):
           qry = '"UIDN" = ' + str( int( srow[0] )) 
           with arcpy.da.UpdateCursor(self.fc, fields, qry) as cursor:
              for urow in cursor:
                  cursor.updateRow(srow)

