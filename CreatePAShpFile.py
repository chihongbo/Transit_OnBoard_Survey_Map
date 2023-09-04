#break up OutShp to folder and name
import arcpy
import os
import sys
arcpy.env.overwriteOutput = True
arcpy.env.workspace="C:/Users/akumar/Desktop/BCT_SurveyDataDrivenPlanning_r1/MAP"
PATH1=arcpy.env.workspace+"/ShpFile"
InFile = PATH1+"/BCTPA.csv"
OutShp1 = PATH1+"/Production.shp"
OutShp2 = PATH1+"/Attraction.shp"

EPSG   = "4269"   #NAD 1983
try:
    SR = arcpy.SpatialReference(int(EPSG))# create a spatial reference from EPSG definition
except:
    arcpy.AddWarning(arcpy.GetMessages())
    arcpy.AddError("Unable to create spatial reference with code %s" % EPSG)
    sys.exit(0)
    
#break up OutShp to folder and name
OutFolder1 = os.path.dirname(OutShp1)
OutFolder2 = os.path.dirname(OutShp2)
OutName1   = os.path.basename(OutShp1)
OutName2   = os.path.basename(OutShp2)

# Create the output feature class
arcpy.CreateFeatureclass_management(OutFolder1,OutName1,"POINT",has_z="DISABLED",spatial_reference=SR)
# add fields to store the values
arcpy.AddField_management(OutShp1,"Route","INTEGER")
arcpy.AddField_management(OutShp1,"FLIP","INTEGER")
arcpy.AddField_management(OutShp1,"PROD_LAT","DOUBLE")
arcpy.AddField_management(OutShp1,"PROD_LONG","DOUBLE")
arcpy.AddField_management(OutShp1,"ATTR_LAT","DOUBLE")
arcpy.AddField_management(OutShp1,"ATTR_LONG","DOUBLE")

## the following is for the Production shp file
with open(InFile,'r') as srcFile:
    next(srcFile)   ## Skip the header line added by Hongbo
    with arcpy.da.InsertCursor(OutShp1,["SHAPE@","Route","FLIP","PROD_LAT","PROD_LONG","ATTR_LAT","ATTR_LONG"]) as InsCur:
        for fileLine in srcFile:
            lSplit = fileLine.split(",")
            if len(lSplit) > 1:
                # more than just one word on the line
                pointsOK = True
                try:
                    Route=int(lSplit[0])
                    FLIP=int(lSplit[1])
                    PROD_LAT = float(lSplit[2])
                    PROD_LONG = float(lSplit[3])
                    ATTR_LAT=float(lSplit[4])
                    ATTR_LONG=float(lSplit[5])
                except:
                    arcpy.AddWarning("Unable to translate points")
                    pointsOK = False
                if pointsOK:
                    # create a point geometry from the 2 coordinates
                    newGeom  = arcpy.PointGeometry(arcpy.Point(PROD_LONG,PROD_LAT))
                    newGeom.spatial_reference = SR # set spatial reference                    
                    InsCur.insertRow([newGeom,Route,FLIP,PROD_LAT,PROD_LONG,ATTR_LAT,ATTR_LONG])# insert this point into the feature class
del InsCur


# Create the output feature class
arcpy.CreateFeatureclass_management(OutFolder2,OutName2,"POINT",has_z="DISABLED",spatial_reference=SR)
# add fields to store the values
arcpy.AddField_management(OutShp2,"Route","INTEGER")
arcpy.AddField_management(OutShp2,"FLIP","INTEGER")
arcpy.AddField_management(OutShp2,"PROD_LAT","DOUBLE")
arcpy.AddField_management(OutShp2,"PROD_LONG","DOUBLE")
arcpy.AddField_management(OutShp2,"ATTR_LAT","DOUBLE")
arcpy.AddField_management(OutShp2,"ATTR_LONG","DOUBLE")

## the following is for the attraction shp file
with open(InFile,'r') as srcFile:
    next(srcFile)   ## Skip the header line added by Hongbo
    with arcpy.da.InsertCursor(OutShp2,["SHAPE@","Route","FLIP","PROD_LAT","PROD_LONG","ATTR_LAT","ATTR_LONG"]) as InsCur:
        for fileLine in srcFile:
            lSplit = fileLine.split(",")
            if len(lSplit) > 1:
                # more than just one word on the line
                pointsOK = True
                try:
                    Route=int(lSplit[0])
                    FLIP=int(lSplit[1])
                    PROD_LAT = float(lSplit[2])
                    PROD_LONG = float(lSplit[3])
                    ATTR_LAT=float(lSplit[4])
                    ATTR_LONG=float(lSplit[5])
                except:
                    arcpy.AddWarning("Unable to translate points")
                    pointsOK = False
                if pointsOK:
                    # create a point geometry from the 2 coordinates
                    newGeom  = arcpy.PointGeometry(arcpy.Point(ATTR_LONG,ATTR_LAT))
                    newGeom.spatial_reference = SR # set spatial reference                     
                    InsCur.insertRow([newGeom,Route,FLIP,PROD_LAT,PROD_LONG,ATTR_LAT,ATTR_LONG])# insert this point into the feature class
del InsCur
