import arcpy, os, sys
from datetime import datetime
import xml.dom.minidom as DOM

arcpy.env.overwriteOutput = True

# Define global variables from User Input
wrkspc = 'D:\pytest'
mapDoc = arcpy.mapping.MapDocument(wrkspc + '\\' + 'fire.mxd')
con = 'GIS Servers/dans6443(admin).ags'
serviceName = 'KYEM'
# shareLevel = 'PRIVATE' # Options: PUBLIC or PRIVATE
# shareOrg = 'NO_SHARE_ORGANIZATION' # Options: SHARE_ORGANIZATION and NO_SHARE_ORGANIZATION
# shareGroups = '' # Options: Valid groups that user is member of


tempPath = sys.path[0]

# SignInToPortal function does not work in 10.2
# for 10.1: uncomment below line to enable sign in
# for 10.2: (1): Sign in to arcgis desktop and check 'sign in automatically'
# (2): Schedule task to run publishFS.py script, using same user as in step 1
##arcpy.SignInToPortal_server('','','http://www.arcgis.com/')

sdDraft = wrkspc + '\\' + serviceName + '.sddraft'
newSDdraft = 'updatedDraft.sddraft'
SD = wrkspc + '\\' + serviceName + '.sd'
summary = 'fire point by County'
tags = 'county, counties, population, density, census'
print "SD==" + SD + ",,sdDraft==" + sdDraft

try:
    print'create service definition draft'
    # create service definition draft
    analysis = arcpy.mapping.CreateMapSDDraft(mapDoc, sdDraft, serviceName, 'ARCGIS_SERVER', con, False, None, summary,
                                              tags)
    print'create draft success'

    # Read the contents of the original SDDraft into an xml parser
    doc = DOM.parse(sdDraft)

    # Change service type from map service to feature service
    typeNames = doc.getElementsByTagName('TypeName')
    for typeName in typeNames:
        if typeName.firstChild.data == 'FeatureServer':
            typeName.parentNode.getElementsByTagName('Enabled')[0].firstChild.data = 'true'

    # Write the new draft to disk
    f = open(newSDdraft, 'w')
    doc.writexml(f)
    f.close()

    # Analyze the service
    analysis = arcpy.mapping.AnalyzeForSD(newSDdraft)
    for key in ('messages', 'warnings', 'errors'):
        print "----" + key.upper() + "---"
        vars = analysis[key]
        for ((message, code), layerlist) in vars.iteritems():
            print "    ", message, " (CODE %i)" % code
            print "       applies to:",
            for layer in layerlist:
                print layer.name,
            print

    if analysis['errors'] == {}:
        print 'analysis true'
        # Stage the service
        arcpy.StageService_server(newSDdraft, SD)

        # Upload the service. The OVERRIDE_DEFINITION parameter allows you to override the
        # sharing properties set in the service definition with new values.
        arcpy.UploadServiceDefinition_server(SD, con)

        print 'Service successfully published'

        # Write messages to a Text File
        txtFile = open(wrkspc + '/{}-log.txt'.format(serviceName), "a")
        txtFile.write(str(datetime.now()) + " | " + "Uploaded and publish service" + "\n")
        txtFile.close()

    else:
        # If the sddraft analysis contained errors, display them and quit.
        print analysis['errors']

        # Write messages to a Text File
        txtFile = open(wrkspc + '/{}-log.txt'.format(serviceName), "a")
        txtFile.write(str(datetime.now()) + " | " + analysis['errors'] + "\n")
        txtFile.close()

except:

    print arcpy.GetMessages()
    # Write messages to a Text File
    txtFile = open(wrkspc + '/{}-log.txt'.format(serviceName), "a")
    txtFile.write(str(datetime.now()) + " | Last Chance Message:" + arcpy.GetMessages() + "\n")
    txtFile.close()