sharedColumns = {
    "SampleId": {
        "limsField": "SampleId",
        "data": "sampleId",
        "columnHeader": "IGO ID",
        "readOnly": "true",
        "type": "numeric",
    },
    "RecordId": {
        "limsField": "RecordId",
        "data": "recordId",
        "columnHeader": "Record ID",
        "readOnly": "true",
    },
    "OtherSampleId": {
        "limsField": "OtherSampleId",
        "data": "otherSampleId",
        "columnHeader": "Sample Name",
        "readOnly": "true",
        "renderer": "html"
    },
    # "UserSampleID": "altId": {"limsField": "AltId", "data": "altId", "columnHeader": "AltId","readOnly":"true",},
    "UserSampleID": {
        "limsField": "UserSampleID",
        "data": "userSampleID",
        "columnHeader": "UserSampleID",
        "readOnly": "true",
    },
    "ConcentrationUnits": {
        "limsField": "ConcentrationUnits",
        "data": "concentrationUnits",
        "columnHeader": "ConcentrationUnits",
        "readOnly": "true",
    },
    "Preservation": {
        "limsField": "Preservation",
        "data": "preservation",
        "columnHeader": "Preservation",
        "readOnly": "true",
    },
    "Recipe": {
        "limsField": "Recipe",
        "data": "recipe",
        "columnHeader": "Recipe",
        "readOnly": "true",
    },
    "IgoQcRecommendation": {
        "limsField": "IgoQcRecommendation",
        "data": "igoQcRecommendation",
        "columnHeader": "IGO Recommendation",
        "readOnly": "true",
        "renderer": "html",
    },
    
    "Comments": {
        "limsField": "Comments",
        "data": "comments",
        "columnHeader": "IGO Comments",
        "readOnly": "true",
    },
    "DateCreated": {
        "limsField": "DateCreated",
        "data": "dateCreated",
        "columnHeader": "Date Created",
        "readOnly": "true",
    },
    "Concentration": {
        "limsField": "Concentration",
        "data": "concentration",
        "columnHeader": "Concentration",
        "readOnly": "true",
    },
    "Volume": {
        "limsField": "Volume",
        "data": "volume",
        "columnHeader": "Volume (uL)",
        "readOnly": "true",
    },
    "TotalMass": {
        "limsField": "TotalMass",
        "data": "totalMass",
        "columnHeader": "Total Mass",
        "readOnly": "true",
    },
}

dnaColumns = {
    "Din": {
        "limsField": "Din",
        "data": "din",
        "columnHeader": "DIN",
        "readOnly": "true",
    },
    "HumanPercentage": {
        "limsField": "HumanPercentage",
        "data": "humanPercentage",
        "columnHeader": "Human %",
        "readOnly": "true",
    },
    "TumorOrNormal": {
        "limsField": "TumorOrNormal",
        "data": "tumorOrNormal",
        "columnHeader": "Tumor/Normal",
        "readOnly": "true",
    },
    "SpecimenType": {
        "limsField": "SpecimenType",
        "data": "specimenType",
        "columnHeader": "CMO Sample Type",
        "readOnly": "true",
    },
    "InvestigatorDecision": {
        "limsField": "InvestigatorDecision",
        "data": "investigatorDecision",
        "columnHeader": "Investigator Decision",
        "readOnly": "true",
        "type": "autocomplete",
        "strict": "true",
        "allowInvalid": "false",
        "trimDropdown": "false",
        "picklistName": "InvestigatorDecisionCustomers",
    },
}

rnaColumns = {
    "Rin": {
        "limsField": "Rin",
        "data": "rin",
        "columnHeader": "RIN",
        "readOnly": "true",
    },
    "Rqn": {
        "limsField": "Rqn",
        "data": "rqn",
        "columnHeader": "RQN",
        "readOnly": "true",
    },
    "DV200": {
        "limsField": "DV200",
        "data": "dV200",
        "columnHeader": "DV200",
        "readOnly": "true",
    },
    "InvestigatorDecision": {
        "limsField": "InvestigatorDecision",
        "data": "investigatorDecision",
        "columnHeader": "Investigator Decision",
        "readOnly": "true",
        "type": "autocomplete",
        "strict": "true",
        "allowInvalid": "false",
        "trimDropdown": "false",
        "picklistName": "InvestigatorDecisionCustomers",
    },
}

libraryColumns = {
    "AvgSize": {
        "limsField": "AvgSize",
        "data": "avgSize",
        "columnHeader": "Average Size (bp)",
        "readOnly": "true",
    },
    "TumorOrNormal": {
        "limsField": "TumorOrNormal",
        "data": "tumorOrNormal",
        "columnHeader": "Tumor/Normal",
        "readOnly": "true",
    },
    "InvestigatorDecision": {
        "limsField": "InvestigatorDecision",
        "data": "investigatorDecision",
        "columnHeader": "Investigator Decision",
        "readOnly": "true",
        "type": "autocomplete",
        "strict": "true",
        "allowInvalid": "false",
        "trimDropdown": "false",
        "picklistName": "InvestigatorDecisionCustomers",
    },
}
pathologyColumns = {
    "SampleId": {
        "limsField": "SampleId",
        "data": "sampleId",
        "columnHeader": "IGO ID",
        "readOnly": "true",
    },
    "RecordId": {
        "limsField": "RecordId",
        "data": "recordId",
        "columnHeader": "Record ID",
        "readOnly": "true",
    },
    "OtherSampleId": {
        "limsField": "OtherSampleId",
        "data": "otherSampleId",
        "columnHeader": "Sample Name",
        "readOnly": "true",
    },
    # "UserSampleID": "altId": {"limsField": "AltId", "data": "altId", "columnHeader": "AltId","readOnly":"true",},
    "SampleStatus": {
        "limsField": "SampleStatus",
        "data": "sampleStatus",
        "columnHeader": "QC Status",
        "readOnly": "true",
        "renderer": "html",
    },
}


attachmentColumns = {
    "FileName": {
        "limsField": "FilePath",
        "data": "fileName",
        "columnHeader": "File Name",
        "readOnly": "true",
    },
    "Action": {
        "data": "action",
        "columnHeader": "Action",
        "renderer": "html",
        'readOnly': "true",
    },
    "RecordId": {
        "limsField": "RecordId",
        "data": "recordId",
        "columnHeader": "Record ID",
        "readOnly": "true",
    },
}

# last column is always RecordId. Needed to set investigator decision efficiently
dnaOrder = [
    "OtherSampleId",
    "Recipe",
    "IgoQcRecommendation",
    "Comments",
    "InvestigatorDecision",
    "SampleId",
    "Concentration",
    "Volume",
    "TotalMass",
    "Din",
    "SpecimenType",
    "HumanPercentage",
    "TumorOrNormal",
    "Preservation",
    "RecordId",
]

rnaOrder = [
    "OtherSampleId",
    "Recipe",
    "IgoQcRecommendation",
    "Comments",
    "InvestigatorDecision",
    "SampleId",
    "Concentration",
    "Volume",
    "TotalMass",
    "Rin",
    "DV200",
    "Preservation",
    "Rqn",
    "RecordId",
]

libraryOrder = [
    "OtherSampleId",
    "Recipe",
    "IgoQcRecommendation",
    "Comments",
    "InvestigatorDecision",
    "SampleId",
    "AvgSize",
    "Concentration",
    "Volume",
    "TotalMass",
    "TumorOrNormal",
    "RecordId",
]

pathologyOrder = ["OtherSampleId", "SampleStatus", "SampleId", "RecordId"]

attachmentOrder = ["FileName", "Action", "RecordId"]


pending_order = [
    "Request",
    "First notification",
    "Most recent notification",
    "Report",
    "Author",
    "Lab Notifications",
    "PM Notifications",
    "User Replies",
    "Recipients",
    "Show",
]

user_pending_order = [
    "Request",
    "First notification",
    "Most recent notification",
    "Report",
    "Show",
]

# initial_email_template = {
#     "from": "igoski@mskcc.org",
#     "subject": "%s QC results pending further action",
#     "body": "Hello,\nIGO has completed %s QC on project %s. \nPlease proceed to igo.mskcc.og/sample-qc and search the Request ID to ask any questions, download related documents, and to indicate which sample(s) should continue with processing.\n\nThank you,",
#     "footer": "\n%s\n%s\nIntegrated Genomics Operation\nMemorial Sloan Kettering Cancer Center\nT 646.888.3765\nFollow us on Instagram and Twitter!\n",
# }
initial_email_template_html = {
    "from": "igoski@mskcc.org",
    "subject": "[SampleQC Beta-Test] %s %s QC results available%s",
    "body": "Hello,<br><br>IGO has completed %s QC on project %s. <br><br>Please proceed to <a href='https://igo.mskcc.org/sample-qc/request/%s'>igo.mskcc.org/sample-qc/request/%s</a> to ask any questions, download related documents, and to indicate which sample(s) should continue with processing.<br><br>Thank you,",
    "footer": "<br><br><span style='color:#f29934; font-weight:bold;'>%s</span><br>%s<br><a href='http://cmo.mskcc.org/cmo/igo/'>Integrated Genomics Operation</a><br><a href='https://www.mskcc.org'>Memorial Sloan Kettering Cancer Center</a><br>T 646.888.3765<br>Follow us on <a href='https://www.instagram.com/genomics212/?hl=en'>Instagram</a> and <a href='https://twitter.com/genomics212?lang=en'>Twitter</a>!<br>",
}

# notification_email_template = {
#     "from": "igoski@mskcc.org",
#     "subject": "[SampleQC Beta-Test] %s New Comment",
#     "body": "Hello,\n\nThe following comment has been added to %s QC on project %s by %s.\n\n\"%s\"\n\nPlease proceed to igo.mskcc.og/sample-qc and search for your project if you would like to reply.\n\nBest,",
#     "footer": "\n%s\n%s\nIntegrated Genomics Operation\nMemorial Sloan Kettering Cancer Center\nT 646.888.3765\nFollow us on Instagram and Twitter!\n",
# }

notification_email_template_html = {
    "from": "igoski@mskcc.org",
    "subject": "[SampleQC Beta-Test] %s New Comment",
    "body": "Hello,<br><br>The following comment has been added to %s QC on project %s by %s.<br><br>\"%s\"<br><br>Please proceed to <a href='https://igo.mskcc.org/sample-qc/request/%s'>igo.mskcc.org/sample-qc/request/%s</a> if you would like to reply.<br><br>Thank you,",
    "footer": "<br><a href='http://cmo.mskcc.org/cmo/igo/'>Integrated Genomics Operation</a><br><a href='https://www.mskcc.org'>Memorial Sloan Kettering Cancer Center</a><br>T 646.888.3765<br>Follow us on <a href='https://www.instagram.com/genomics212/?hl=en'>Instagram</a> and <a href='https://twitter.com/genomics212?lang=en'>Twitter</a>!<br>",
}

decision_notification_email_template_html = {
    "from": "igoski@mskcc.org",
    "subject": "[SampleQC Beta-Test] %s Decisions Submitted for %s",
    "body": "Hello,<br><br>Decisions have been submitted for project %s by %s.<br><br><span style='font-weight:bold;'> To make any changes to the decisions, please reach out to IGO at zzPDL_CMO_IGO@mskcc.org.</span><br>You can find the project at <a href='https://igo.mskcc.org/sample-qc/request/%s'>igo.mskcc.org/sample-qc/request/%s</a>.<br>Thank you,",
    "footer": "<br><a style='color:#f29934; font-weight:bold;' href='http://cmo.mskcc.org/cmo/igo/'>Integrated Genomics Operation</a><br><a href='https://www.mskcc.org'>Memorial Sloan Kettering Cancer Center</a><br>T 646.888.3765<br>Follow us on <a href='https://www.instagram.com/genomics212/?hl=en'>Instagram</a> and <a href='https://twitter.com/genomics212?lang=en'>Twitter</a>!<br>",
}

user_training_string = "Unfamiliar with IGO's new process for sharing QC results? Watch our 5 minute how-to video <a href='https://igodev.mskcc.org/sample-qc/instructions'>here</a> or stop by IGO's Smartboard (located near the ZRC 3rd floor elevator bank) from 3-4 PM until Feb 5th, for an in-person training."