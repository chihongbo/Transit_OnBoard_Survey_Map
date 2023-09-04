import arcpy
import os
import csv
import sys
arcpy.env.workspace="C:/Users/akumar/Desktop/NO/NORTA_SurveyDataDrivenPlanning_v1/MAP"
arcpy.env.overwriteOutput =True
routeno="94"
vfieldList=["2010","2015"]
PATH1=arcpy.env.workspace.replace("/Map","")
fc=PATH1+"/MAP/Shpfile/MPO0000TAZPopEmp.shp"
filenameAll=PATH1+"/OutputResults/BCTRoute"+routeno+"POPEmpMap.pdf"
try:
    if os.path.isfile(filenameAll):
        os.remove(filenameAll)
except:
    print "Please close the PDF file: "+filenameAll
    os.system("pause")
    sys.exit(1)
pdfdoc=arcpy.mapping.PDFDocumentCreate(filenameAll)
for row in vfieldList:
    ## A fix for the route 01, 02 and so on in the SQL query
    PrjYear="20"+row[-2:]
    if(len(routeno)<2):
        routenostr="0"+routeno
    else:
        routenostr=routeno
    mxdfile=PATH1+"/MAP/ShpFile/BCT_SE_Profile_Page41.mxd"
    mxd=arcpy.mapping.MapDocument(mxdfile)

    ## For Population Data Frame
    df=arcpy.mapping.ListDataFrames(mxd)[0]
    lyr1=arcpy.mapping.ListLayers(mxd,"*Route",df)[0]
    lyr1.definitionQuery='"ROUTE"='+"'"+routenostr+"'"
    lyr1.name="BCT Route "+routeno
    lyr2=arcpy.mapping.ListLayers(mxd,"SE Data",df)[0]   ## for SE Data layer
    SEField="POP"+row[-2:]
    lyr2.symbology.valueField = SEField
    lyr3=arcpy.mapping.ListLayers(mxd,"*Buffer",df)[0]
    lyr3.definitionQuery='"ROUTE"='+"'"+routenostr+"'" 
    ## get the max value of the value field
    theitems=[]
    rows=arcpy.SearchCursor(fc)
    ## find the min and max of the lyr6
    for row1 in rows:
        theitems.append(row1.getValue(SEField))
    del rows
    del row1
    theitems.sort()
    min=theitems[0]
    max=theitems[-1]
    lyr2.symbology.classBreakValues = [0,200, 1000, 2500, 5000, max]
    lyr2.symbology.classBreakLabels = ["0 to 200", "201 to 1,000", 
                                    "1,001 to 2,500", "2,501 to 5,000","5,001 to "+"{:,}".format(max)]
    ## For Employment Data Frame
    df=arcpy.mapping.ListDataFrames(mxd)[1]
    lyr1=arcpy.mapping.ListLayers(mxd,"*Route",df)[0]
    lyr1.name="BCT Route "+routeno
    lyr1.definitionQuery='"ROUTE"='+"'"+routenostr+"'"      
    lyr2=arcpy.mapping.ListLayers(mxd,"SE Data",df)[0]   ## for SE Data layer
    SEField="EMP"+row[-2:]
    lyr2.symbology.valueField = SEField
    lyr3=arcpy.mapping.ListLayers(mxd,"*Buffer",df)[0]
    lyr3.definitionQuery='"ROUTE"='+"'"+routenostr+"'" 
    ## get the max value of the value field
    theitems=[]
    rows=arcpy.SearchCursor(fc)
    ## find the min and max of the lyr6
    for row1 in rows:
        theitems.append(row1.getValue(SEField))
    del rows
    del row1
    theitems.sort()
    min=theitems[0]
    max=theitems[-1]
    lyr2.symbology.classBreakValues = [0,200, 1000, 2500, 5000, max]
    lyr2.symbology.classBreakLabels = ["0 to 200", "201 to 1,000", 
                                    "1,001 to 2,500", "2,501 to 5,000","5,001 to "+"{:,}".format(max)]
    legend = arcpy.mapping.ListLayoutElements(mxd, "LEGEND_ELEMENT")[0]
    legend.title = "Employment "+PrjYear
    legend = arcpy.mapping.ListLayoutElements(mxd, "LEGEND_ELEMENT")[1]
    legend.title = "Population "+PrjYear

    title=arcpy.mapping.ListLayoutElements(mxd,"TEXT_ELEMENT")[0]
    Temptext="Route "+str(routeno)+" - Year " + PrjYear+" Population and Employment by TAZ"
    title.text=Temptext
    
    arcpy.mapping.MapDocument(mxdfile).activeView = "PAGE_LAYOUT"   ## Shift between Data Frame and Layout to refresh the Stack chart
    arcpy.RefreshActiveView()
    arcpy.RefreshTOC()
    filename=PATH1+"/OutputResults/BCT"+str(routeno)+".pdf"
    filenameJPG=PATH1+"/OutputResults/BCT"+str(routeno)+"_"+PrjYear+"POPEMP"+".jpg" 
    arcpy.mapping.ExportToPDF(mxd,filename)
    arcpy.mapping.ExportToJPEG(mxd,filenameJPG,resolution=200)
    pdfdoc.appendPages(filename)
    os.remove(filename)          
    del mxd
del row
pdfdoc.saveAndClose()
del pdfdoc



