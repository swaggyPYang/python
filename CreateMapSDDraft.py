import arcpy
mapDoc = arcpy.mapping.MapDocument('C:/Project/counties.mxd') 
service = 'Counties'
sddraft = 'C:/Project/' + service + '.sddraft'
        
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