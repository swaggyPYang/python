import arcpy
# define local variables
wrkspc = 'D:/arcgis/Tutorial/ArcTutor/Parcel Editing/'
mapDoc = arcpy.mapping.MapDocument(wrkspc + 'ParcelEditing.mxd')
con = 'C:/Users/Esri/Desktop10.5/AppData/Roaming/ESRI/ArcCatalog/arcgis on liy.esrichina.com_6443 (admin).ags' 
service = 'ParcelEditing'
sddraft = wrkspc + service + '.sddraft'
sd = wrkspc + service + '.sd'
summary = 'Population Density by County'
tags = 'county, counties, population, density, census'
# create service definition draft
analysis = arcpy.mapping.CreateMapSDDraft(mapDoc, sddraft, service, 'ARCGIS_SERVER', 
                                          con, True, None, summary, tags)
# stage and upload the service if the sddraft analysis did not contain errors
if analysis['errors'] == {}:
    # Execute StageService
    arcpy.StageService_server(sddraft, sd)
    # Execute UploadServiceDefinition
    arcpy.UploadServiceDefinition_server(sd, con)
else: 
    # if the sddraft analysis contained errors, display them
    print analysis['errors']