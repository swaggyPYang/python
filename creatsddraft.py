import arcpy
mapDoc = arcpy.mapping.MapDocument('D:/arcgis/Tutorial/ArcTutor/Parcel Editing/ParcelEditing.mxd') 
service = 'Counties'
sddraft = 'D:/arcgis/Tutorial/ArcTutor/Parcel Editing/123.sddraft'
        
analysis = arcpy.mapping.CreateMapSDDraft(mapDoc, sddraft, service, 'ARCGIS_SERVER')
for key in ('messages', 'warnings', 'errors'):
  print "----" + key.upper() + "---"
  vars = analysis[key]
  for ((message, code), layerlist) in vars.iteritems():
    print "    ", message, " (CODE %i)" % code
    print "       applies to:",
    for layer in layerlist:
        print layer.name,
    print
arcpy.StageService_server("D:/arcgis/Tutorial/ArcTutor/Parcel Editing/123.sddraft", "D:/arcgis/Tutorial/ArcTutor/Parcel Editing/123.sd")