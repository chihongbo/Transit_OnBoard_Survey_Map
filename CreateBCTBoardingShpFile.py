#break up OutShp to folder and name
import arcpy
import os
import sys
arcpy.env.overwriteOutput = True
arcpy.env.workspace="C:/Projects/NORTA_Tool_v1/MAP"
PATH1=arcpy.env.workspace+"/ShpFile"
InFile = PATH1+"/BCTBoardings.csv"
OutShp = PATH1+"/BCTBoardings.Shp"

EPSG   = "4269"   #NAD 1983
try:
    SR = arcpy.SpatialReference(int(EPSG))# create a spatial reference from EPSG definition
except:
    arcpy.AddWarning(arcpy.GetMessages())
    arcpy.AddError("Unable to create spatial reference with code %s" % EPSG)
    sys.exit(0)
    
#break up OutShp to folder and name
OutFolder = os.path.dirname(OutShp)
OutName   = os.path.basename(OutShp)

# Create the output feature class
arcpy.CreateFeatureclass_management(OutFolder,OutName,"POINT",has_z="DISABLED",spatial_reference=SR)
# add fields to store the values
arcpy.AddField_management(OutShp,"Route","INTEGER")
arcpy.AddField_management(OutShp,"DIRECTION","TEXT", field_length = 10)
arcpy.AddField_management(OutShp,"Stop_Seque","FLOAT")
arcpy.AddField_management(OutShp,"Stop_ID","INTEGER")
arcpy.AddField_management(OutShp,"Stop_Name","TEXT", field_length = 50)
arcpy.AddField_management(OutShp,"Boardings","DOUBLE")
arcpy.AddField_management(OutShp,"Alightings","DOUBLE")
arcpy.AddField_management(OutShp,"Ycoord","DOUBLE")
arcpy.AddField_management(OutShp,"Xcoord","DOUBLE")
arcpy.AddField_management(OutShp,"Routes","TEXT", field_length = 10)

with open(InFile,'r') as srcFile:
    next(srcFile)   ## Skip the header line added by Hongbo
    with arcpy.da.InsertCursor(OutShp,["SHAPE@","Route","DIRECTION","Stop_Seque","Stop_ID","Stop_Name","Boardings","Alightings","Xcoord","Ycoord","Routes"]) as InsCur:
        for fileLine in srcFile:
            # split the line up into a list
            # 1 337172.8 4278952.4 85.7334909091 becomes [1,337172.8,4278952.4,85.7334909091]
            # try a few common delimiters: tab, space, comma, pipe..
            lSplit = fileLine.split(",")

            if len(lSplit) > 1:
                # more than just one word on the line
                pointsOK = True
                try:
                    Xcoord = float(lSplit[8])
                    Ycoord = float(lSplit[7])
                    Route=int(lSplit[0])
                    DIRECTION=lSplit[1]
                    Stop_Seque=float(lSplit[4])
                    Stop_ID=int(lSplit[2])
                    Stop_Name=lSplit[3]
                    Boardings=float(lSplit[5])
                    Alightings=float(lSplit[6])
                    if(Route<10):
                        Routes="0"+str(Route)
                    else:
                        Routes=str(Route)

                except:
                    arcpy.AddWarning("Unable to translate points")
                    pointsOK = False

                if pointsOK:
                    # create a point geometry from the 2 coordinates
                    newGeom  = arcpy.PointGeometry(arcpy.Point(Xcoord,Ycoord))
                    newGeom.spatial_reference = SR # set spatial reference
                    # you could project here using newGeom.projectAs(SpatialRef)
                    # if you needed them in a different spatial reference                        
                    InsCur.insertRow([newGeom,Route,DIRECTION,Stop_Seque,Stop_ID,Stop_Name,Boardings,Alightings,Xcoord,Ycoord,Routes])# insert this point into the feature class
del InsCur
