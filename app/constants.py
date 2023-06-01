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
        "renderer": "html",
    },
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
    "SourceSampleId": {
        "limsField": "SourceSampleId",
        "data": "sourceSampleId",
        "columnHeader": "Source Sample ID",
        "readOnly": "true",
    },
    "A260230": {
        "limsField": "A260230",
        "data": "A260230",
        "columnHeader": "260/230",
        "readOnly": "true",
    },
    "A260280": {
        "limsField": "A260280",
        "data": "A260280",
        "columnHeader": "260/280",
        "readOnly": "true",
    }
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
     "SourceSampleId": {
        "limsField": "SourceSampleId",
        "data": "sourceSampleId",
        "columnHeader": "Source Sample ID",
        "readOnly": "true",
    },
    "A260230": {
        "limsField": "A260230",
        "data": "A260230",
        "columnHeader": "260/230",
        "readOnly": "true",
    },
    "A260280": {
        "limsField": "A260280",
        "data": "A260280",
        "columnHeader": "260/280",
        "readOnly": "true",
    }
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
     "SourceSampleId": {
        "limsField": "SourceSampleId",
        "data": "sourceSampleId",
        "columnHeader": "Source Sample ID",
        "readOnly": "true",
    },
    "NumOfReads": {
        "limsField": "NumOfReads",
        "data": "numOfReads",
        "columnHeader": "Number of Reads",
        "readOnly": "true",
    }
}

poolColumns = {
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

covidColumns = {
    "RecordId": {
        "limsField": "RecordId",
        "data": "recordId",
        "columnHeader": "Record ID",
        "readOnly": "true",
    },
    "OtherSampleId": {
        "limsField": "OtherSampleId",
        "data": "otherSampleId",
        "columnHeader": "OtherSampleId",
        "readOnly": "true",
    },
    "UserSampleId": {
        "limsField": "UserSampleID",
        "data": "userSampleId",
        "columnHeader": "UserSampleId",
        "readOnly": "true",
    },
    "AssayResult": {
        "limsField": "AssayResult",
        "data": "assayResult",
        "columnHeader": "Assay Result",
        "readOnly": "true",
    },
    "CqN1": {
        "limsField": "CqN1",
        "data": "cqN1",
        "columnHeader": "CqN1",
        "readOnly": "true",
    },
    "CqN2": {
        "limsField": "CqN2",
        "data": "cqN2",
        "columnHeader": "CqN2",
        "readOnly": "true",
    },
    "CqRP": {
        "limsField": "CqRP",
        "data": "cqRP",
        "columnHeader": "CqRP",
        "readOnly": "true",
    },
}

covidOrder = ["UserSampleId", "AssayResult", "CqN1", "CqN2", "CqRP", "OtherSampleId", "RecordId"]


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
    "SourceSampleId",
    "A260230",
    "A260280",
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
    "SourceSampleId",
    "A260230",
    "A260280",
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
    "SourceSampleId",
    "RecordId",
    "NumOfReads",
]

poolOrder = [
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

initial_email_template_html = {
    "from": "igoski@mskcc.org",
    "dev_subject": "[SampleQC Beta-Test] %s %s QC results available%s",
    "subject": "[IGO SampleQC] %s %s QC results available%s",
    "covid_subject": "[IGO SampleQC] %s %s qPCR results available%s",
    "body": "Hello,<br><br>IGO has completed %s QC on project %s. <br><br>Please proceed to <a href='https://igo.mskcc.org/sample-qc/request/%s'>igo.mskcc.org/sample-qc/request/%s</a> to ask any questions, download related documents, and to indicate which sample(s) should continue with processing.<br><br>Thank you,",
    "covid_body": "Hello,<br><br>IGO has completed %s qPCR on project %s. <br><br>Please proceed to <a href='https://igo.mskcc.org/sample-qc/request/%s'>igo.mskcc.org/sample-qc/request/%s</a> to ask any questions or download related documents.<br><br>Thank you,",
    "cmo_pm_body": "Hello,<br><br>IGO has completed %s QC on project %s. <br><br>You can view the results at <a href='https://igo.mskcc.org/sample-qc/request/%s'>igo.mskcc.org/sample-qc/request/%s</a>. Your Project Manager will be handling any QC related decisions and questions.<br><br>Thank you,",
    "footer": "<br><br><span style='color:#f29934; font-weight:bold;'>%s</span><br>%s<br><a href='http://cmo.mskcc.org/cmo/igo/'>Integrated Genomics Operation</a><br><a href='https://www.mskcc.org'>Memorial Sloan Kettering Cancer Center</a><br>T 646.888.3765<br>Follow us on <a href='https://www.instagram.com/genomics212/?hl=en'>Instagram</a> and <a href='https://twitter.com/genomics212?lang=en'>Twitter</a>!<br>",
}

notification_email_template_html = {
    "from": "igoski@mskcc.org",
    "dev_subject": "[SampleQC Beta-Test] %s New Comment",
    "subject": "[IGO SampleQC] %s New Comment",
    "body": "Hello,<br><br>The following comment has been added to %s QC on project %s by %s.<br><br>\"%s\"<br><br>Please proceed to <a href='https://igo.mskcc.org/sample-qc/request/%s'>igo.mskcc.org/sample-qc/request/%s</a> if you would like to reply.<br><br>Thank you,",
    "footer": "<br><a href='http://cmo.mskcc.org/cmo/igo/'>Integrated Genomics Operation</a><br><a href='https://www.mskcc.org'>Memorial Sloan Kettering Cancer Center</a><br>T 646.888.3765<br>Follow us on <a href='https://www.instagram.com/genomics212/?hl=en'>Instagram</a> and <a href='https://twitter.com/genomics212?lang=en'>Twitter</a>!<br>",
}

decision_notification_email_template_html = {
    "from": "igoski@mskcc.org",
    "dev_subject": "[SampleQC Beta-Test] %s Decisions Submitted for %s",
    "subject": "[IGO SampleQC] %s Decisions Submitted for %s",
    "body": "Hello,<br><br>Decisions have been submitted for project %s by %s.<br><br><span style='font-weight:bold;'> To make any changes to the decisions, please reach out to IGO at zzPDL_IGO_Staff@mskcc.org.</span><br>You can find the project at <a href='https://igo.mskcc.org/sample-qc/request/%s'>igo.mskcc.org/sample-qc/request/%s</a>.<br><br>Thank you,",
    "footer": "<br><a style='color:#f29934; font-weight:bold;' href='http://cmo.mskcc.org/cmo/igo/'>Integrated Genomics Operation</a><br><a href='https://www.mskcc.org'>Memorial Sloan Kettering Cancer Center</a><br>T 646.888.3765<br>Follow us on <a href='https://www.instagram.com/genomics212/?hl=en'>Instagram</a> and <a href='https://twitter.com/genomics212?lang=en'>Twitter</a>!<br>",
}

stop_processing_notification_email_template_html = {
    "from": "igoski@mskcc.org",
    "dev_subject": "[SampleQC Beta-Test] %s Stop Processing Decision(s) Submitted for %s",
    "subject": "[IGO SampleQC] %s Stop Processing Decision(s) Submitted for %s",
    "body": "Hello,<br><br>For project %s Stop Processing decision(s) have been submitted by %s.<br><br><span style='font-weight:bold;'> This is to notify you to check if the iLab proper charges for these samples are present.</span><br>You can find the project at <a href='https://igo.mskcc.org/sample-qc/request/%s'>igo.mskcc.org/sample-qc/request/%s</a>.<br><br>Thank you,",
    "footer": "<br><a style='color:#f29934; font-weight:bold;' href='http://cmo.mskcc.org/cmo/igo/'>Integrated Genomics Operation</a><br><a href='https://www.mskcc.org'>Memorial Sloan Kettering Cancer Center</a><br>T 646.888.3765<br>Follow us on <a href='https://www.instagram.com/genomics212/?hl=en'>Instagram</a> and <a href='https://twitter.com/genomics212?lang=en'>Twitter</a>!<br>",
}

user_training_string = "Unfamiliar with this new process for sharing QC results? Watch our 5 minute <a href='https://igo.mskcc.org/sample-qc/instructions'>how-to video</a>."
