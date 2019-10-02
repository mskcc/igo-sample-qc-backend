sharedColumns = {
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
    "InvestigatorDecision": {
        "limsField": "InvestigatorDecision",
        "data": "investigatorDecision",
        "columnHeader": "Investigator Decision",
        "type": "dropdown",
        "trimDropdown": "false",
        "picklistName": "InvestigatorDecision",
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
        "columnHeader": "Volume",
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
        "columnHeader": "Din",
        "readOnly": "true",
    },
    "PercentHuman": {
        "limsField": "PercentHuman",
        "data": "percentHuman",
        "columnHeader": "%Human",
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
}

libraryColumns = {
    "AvgSize": {
        "limsField": "AvgSize",
        "data": "avgSize",
        "columnHeader": "Average Size",
        "readOnly": "true",
    },
    "TumorOrNormal": {
        "limsField": "TumorOrNormal",
        "data": "tumorOrNormal",
        "columnHeader": "Tumor/Normal",
        "readOnly": "true",
    },
}

attachmentColumns = {
    "FileName": {
        "limsField": "FilePath",
        "data": "fileName",
        "columnHeader": "File Name",
        "readOnly": "true",
    },
    "Action": {"data": "action", "columnHeader": "Action"},
    "RecordId": {
        "limsField": "RecordId",
        "data": "recordId",
        "columnHeader": "Record ID",
        "readOnly": "true",
    },
}

# last column is always RecordId. Needed to set investigator decision efficiently
dnaOrder = [
    "Recipe",
    "IgoQcRecommendation",
    "Comments",
    "InvestigatorDecision",
    "SampleId",
    "OtherSampleId",
    "Concentration",
    "Volume",
    "TotalMass",
    "Din",
    "SpecimenType",
    "PercentHuman",
    "TumorOrNormal",
    "Preservation",
    "RecordId",
]

rnaOrder = [
    "Recipe",
    "IgoQcRecommendation",
    "Comments",
    "InvestigatorDecision",
    "SampleId",
    "OtherSampleId",
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
    "Recipe",
    "IgoQcRecommendation",
    "Comments",
    "InvestigatorDecision",
    "SampleId",
    "OtherSampleId",
    "AvgSize",
    "Concentration",
    "Volume",
    "TotalMass",
    "TumorOrNormal",
    "RecordId",
]

attachmentOrder = ["FileName", "Action", "RecordId"]
