import arcpy
import os
import csv
import sys
arcpy.env.workspace="C:/Users/akumar/Desktop/BCT_SurveyDataDrivenPlanning_r1/MAP"
arcpy.env.overwriteOutput =True
routeno="2"
SurveyYear="2012"
PATH1=arcpy.env.workspace.replace("/Map","")

## A fix for the route 01, 02 and so on in the SQL query
if(len(routeno)<2):
    routenostr="0"+routeno
else:
    routenostr=routeno
mxdfile=PATH1+"/MAP/ShpFile/BCT_ProdAttr.mxd"
mxd=arcpy.mapping.MapDocument(mxdfile)
## Production Data Frame
df=arcpy.mapping.ListDataFrames(mxd)[0]
lyr1=arcpy.mapping.ListLayers(mxd,"*Routes",df)[0]
lyr1.name="BCT Route "+routeno
lyr1.definitionQuery='"ROUTE"='+"'"+routenostr+"'"      
lyr2=arcpy.mapping.ListLayers(mxd,"Production",df)[0]   ## for Production Layer
lyr2.definitionQuery='"Route"='+routeno
## Attraction Data Frame
df=arcpy.mapping.ListDataFrames(mxd)[1]
lyr1=arcpy.mapping.ListLayers(mxd,"*Routes",df)[0]
lyr1.name="BCT Route "+routeno
lyr1.definitionQuery='"ROUTE"='+"'"+routenostr+"'"      
lyr2=arcpy.mapping.ListLayers(mxd,"Attraction",df)[0]   ## for Attraction Layer
lyr2.definitionQuery='"Route"='+routeno

## Set the Legend Title
legend = arcpy.mapping.ListLayoutElements(mxd, "LEGEND_ELEMENT", "Legend")[1]
legend.title = "Production Locations"
legend = arcpy.mapping.ListLayoutElements(mxd, "LEGEND_ELEMENT", "Legend")[0]
legend.title = "Attraction Locations"

arcpy.RefreshActiveView()
title=arcpy.mapping.ListLayoutElements(mxd,"TEXT_ELEMENT")[1]
Temptext="Year " +SurveyYear+ " Survey - Production Trip Ends"
title.text=Temptext
title=arcpy.mapping.ListLayoutElements(mxd,"TEXT_ELEMENT")[0]
Temptext="Year "+SurveyYear+ " Survey - Attraction Trip Ends"
title.text=Temptext
arcpy.mapping.MapDocument(mxdfile).activeView = "PAGE_LAYOUT"   ## Shift between Data Frame and Layout to refresh the Stack chart
arcpy.RefreshActiveView()
arcpy.RefreshTOC()
#filenameMxd=str(routenostr) +"_"+row+".mxd"
filename=PATH1+"/OutputResults/BCTRoute"+str(routeno)+"_"+"ProdAttr"+".jpg"
try:
    if os.path.isfile(filename):
        os.remove(filename)
except:
    print "Please close the JPG file: "+filename
    os.system("pause")
    sys.exit(1)
arcpy.mapping.ExportToJPEG(mxd,filename,resolution=200)
del mxd



