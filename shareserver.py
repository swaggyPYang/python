import arcpy
result = "c:/gis/gp/Analysis.rlt"
connectionPath = "c:/gis/conections/myServer.ags"
sddraft = "c:/gis/gp/drafts/AnalysisDraft.sddraft"
sd = "c:/gis/gp/sd/AnalysisDraft.sd"
serviceName = "AnalysisService"
# Create service definition draft
arcpy.CreateGPSDDraft(
    result, sddraft, serviceName, server_type="ARCGIS_SERVER",
    connection_file_path=connectionPath, copy_data_to_server=True,
    folder_name=None, summary="Analysis Service", tags="gp",
    executionType="Synchronous", resultMapServer=False,
    showMessages="INFO", maximumRecords=5000, minInstances=2,
    maxInstances=3, maxUsageTime=100, maxWaitTime=10,
    maxIdleTime=180)
# Analyze the service definition draft
analyzeMessages = arcpy.mapping.AnalyzeForSD(sddraft)
# Stage and upload the service if the sddraft analysis did not
# contain errors
if analyzeMessages['errors'] == {}:
    # Execute StageService
    arcpy.StageService_server(sddraft, sd)
    # Execute UploadServiceDefinition
    arcpy.UploadServiceDefinition_server(sd, connectionPath)
else:
    # If the sddraft analysis contained errors, display them
    print(analyzeMessages['errors'])