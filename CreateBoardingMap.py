#### Definition Query
import arcpy
import os
import csv
arcpy.env.workspace="C:/Projects/MAP"
PATH1=arcpy.env.workspace.replace("/Map","")
lyrStop1="BCTBoardings"
lyrRoute="BCT_Bus_Routes"
fc=PATH1+"/MAP/ShpFile/BCTBoardings.shp"
fcrows=arcpy.da.SearchCursor(fc ,["Routes","Direction","Boardings","Alightings"])

## read the BCT Route Direction CSV file
routecsv=PATH1+"/MAP/ShpFile/BCTRouteDB.csv"
f=open(routecsv)
csv_f=csv.reader(f)
##csv_f.next() ## Skip the header line of the CSV file
filenameAll=PATH1+"/BCTSurvey_ONsOFFs1.pdf"
if os.path.exists(filenameAll):
    os.remove(filenameAll)
pdfdoc=arcpy.mapping.PDFDocumentCreate(filenameAll)
for row in csv_f:
    route = str(row[0])
    if(len(route)<2):
        routeno="0"+route
    else:
        routeno=route
    direction = row[2]
    if("EW" in str(direction)):
        mxdfile=PATH1+"/MAP/ShpFile/BCT_ONOFF_Landscape_Page31.mxd"
        direction1="EB"
        direction2="WB"
    else:
        mxdfile=PATH1+"/MAP/ShpFile/BCT_ONOFF_Portrait_Page31.mxd"
        direction1="NB"
        direction2="SB"
        
    mxd=arcpy.mapping.MapDocument(mxdfile)
    lyrTemp=PATH1+"/MAP/ShpFile/BCTBoardingsRT"+ route+".lyr"     ## the Template layer file
    styleItem = arcpy.mapping.ListStyleItems("ESRI.style", "Legend Items", "Horizontal Single Symbol Label Only")[0]

    ## for the First Data Frame    
    df=arcpy.mapping.ListDataFrames(mxd)[0]
    lyr1=arcpy.mapping.ListLayers(mxd,lyrStop1,df)[0]  ## for ons/off figure
    lyr2=arcpy.mapping.ListLayers(mxd,lyrRoute,df)[0] ## for route layer

    arcpy.mapping.RemoveLayer(df, lyr1)      ## remove the current Layer1
    addLayer = arcpy.mapping.Layer(lyrTemp)  ## Add the Template Layer
    arcpy.mapping.AddLayer(df, addLayer, "TOP")
    lyr1 = arcpy.mapping.ListLayers(mxd, lyrStop1, df)[0]
    lyr1.visible=True

    ## Perform the SQL Selection on the Selected Route    
    lyr1.definitionQuery='"Routes"='+"'"+routeno+"'"+' and "Direction"='+"'"+direction1+"'"
    lyr2.definitionQuery='"Route"='+"'"+routeno+"'"
    arcpy.RefreshActiveView()
    extent_object=lyr2.getExtent()

    extent_object.XMin=extent_object.XMin*(1-0.004)
    extent_object.YMin=extent_object.YMin*(1-0.004)
    extent_object.XMax=extent_object.XMax*(1+0.004)
    extent_object.YMax=extent_object.YMax*(1+0.004)
    df.extent=extent_object
    lyr2.name="BCT Route " +route

     ## Update the Legend Style for the first data frame
    legend = arcpy.mapping.ListLayoutElements(mxd, "LEGEND_ELEMENT")[1] ## the first Data frame
    legend.updateItem(lyr1, styleItem)    
     ## Update the Title
    if("EW" in str(direction)):
        ##title=arcpy.mapping.ListLayoutElements(mxd,"TEXT_ELEMENT")[1]
        ##Temptext="BCT Route "+str(route)+" "+ "Eastbound"+ " Boardings and Alightings"
        ##title.text=Temptext
        legend.title="Eastbound"
    else:
        legend.title="Northbound"

    ## for the Second Data Frame    
    df=arcpy.mapping.ListDataFrames(mxd)[1]
    lyr1=arcpy.mapping.ListLayers(mxd,lyrStop1,df)[0]  ## for ons/off figure
    lyr2=arcpy.mapping.ListLayers(mxd,lyrRoute,df)[0] ## for route layer

    arcpy.mapping.RemoveLayer(df, lyr1)      ## remove the current Layer1
    addLayer = arcpy.mapping.Layer(lyrTemp)  ## Add the Template Layer
    arcpy.mapping.AddLayer(df, addLayer, "TOP")
    lyr1 = arcpy.mapping.ListLayers(mxd, lyrStop1, df)[0]
    lyr1.visible=True

    ## Perform the SQL Selection on the Selected Route    
    lyr1.definitionQuery='"Routes"='+"'"+routeno+"'"+' and "Direction"='+"'"+direction2+"'"
    lyr2.definitionQuery='"Route"='+"'"+routeno+"'"
    arcpy.RefreshActiveView()
    extent_object=lyr2.getExtent()

    extent_object.XMin=extent_object.XMin*(1-0.004)
    extent_object.YMin=extent_object.YMin*(1-0.004)
    extent_object.XMax=extent_object.XMax*(1+0.004)
    extent_object.YMax=extent_object.YMax*(1+0.004)
    df.extent=extent_object
    lyr2.name="BCT Route " +route

     ## Update the Legend Style for second Dataframe
    legend = arcpy.mapping.ListLayoutElements(mxd, "LEGEND_ELEMENT")[0] ##The second data frame
    legend.updateItem(lyr1, styleItem)    
     ## Update the Title
    if("EW" in str(direction)):
        ##title=arcpy.mapping.ListLayoutElements(mxd,"TEXT_ELEMENT")[0]
        ##Temptext="BCT Route "+str(route)+" "+ "Westbound"+ " Boardings and Alightings"
        ##title.text=Temptext
        legend.title="Westbound"
    else:
        ##title=arcpy.mapping.ListLayoutElements(mxd,"TEXT_ELEMENT")[0]
        ##Temptext="BCT Route "+str(route)+ " Boardings and Alightings"
        ##title.text=Temptext
        legend.title="Southbound"

    arcpy.RefreshActiveView()
    arcpy.RefreshTOC()
    #filenameMxd=PATH1+"/"+str(routeno)+ str(direction) + "Boardings.mxd"
    #mxd.saveACopy(filenameMxd) ## do not save the file for this moment

    filename=PATH1+"/OutputResults/BCT"+str(routeno)+"BoardAlight.pdf" ## Based on UID
    arcpy.mapping.ExportToPDF(mxd,filename)
    pdfdoc.appendPages(filename)
    os.remove(filename)
    filename=PATH1+"/OutputResults/BCTRoute"+str(route)+"_"+"Boarding"+".jpg"
    arcpy.mapping.ExportToJPEG(mxd,filename,resolution=200)    
    del mxd
del row, csv_f, f,fcrows
pdfdoc.saveAndClose()
del pdfdoc



