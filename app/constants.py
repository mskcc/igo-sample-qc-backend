sharedColumns = {
    "SampleId": {
        "limsField": "SampleId",
        "field": "sampleId",
        "columnHeader": "IGO ID",
        "readOnly": True,
    },
    "OtherSampleId": {
        "limsField": "OtherSampleId",
        "field": "otherSampleId",
        "columnHeader": "Sample Name",
        "readOnly": True,
    },
    # "UserSampleID": "altId": {"limsField": "AltId", "field": "altId", "columnHeader": "AltId","readOnly":True,},
    "UserSampleID": {
        "limsField": "UserSampleID",
        "field": "userSampleID",
        "columnHeader": "UserSampleID",
        "readOnly": True,
    },
    "ConcentrationUnits": {
        "limsField": "ConcentrationUnits",
        "field": "concentrationUnits",
        "columnHeader": "ConcentrationUnits",
        "readOnly": True,
    },
    "Preservation": {
        "limsField": "Preservation",
        "field": "preservation",
        "columnHeader": "Preservation",
        "readOnly": True,
    },
    "Recipe": {
        "limsField": "Recipe",
        "field": "recipe",
        "columnHeader": "Recipe",
        "readOnly": True,
    },
    "IgoQcRecommendation": {
        "limsField": "IgoQcRecommendation",
        "field": "igoQcRecommendation",
        "columnHeader": "IGO QC Recommendation",
        "readOnly": True,
    },
    "InvestigatorDecision": {
        "limsField": "InvestigatorDecision",
        "field": "investigatorDecision",
        "columnHeader": "Investigator Decision",
        "readOnly": True,
    },
    "Comments": {
        "limsField": "Comments",
        "field": "comments",
        "columnHeader": "Comments",
        "readOnly": True,
    },
    "DateCreated": {
        "limsField": "DateCreated",
        "field": "dateCreated",
        "columnHeader": "Date Created",
        "readOnly": True,
    },
    "Concentration": {
        "limsField": "Concentration",
        "field": "concentration",
        "columnHeader": "Concentration",
        "readOnly": True,
    },
    "Volume": {
        "limsField": "Volume",
        "field": "volume",
        "columnHeader": "Volume",
        "readOnly": True,
    },
    "TotalMass": {
        "limsField": "TotalMass",
        "field": "totalMass",
        "columnHeader": "Total Mass",
        "readOnly": True,
    },
}

dnaColumns = {
    "Din": {
        "limsField": "Din",
        "field": "din",
        "columnHeader": "Din",
        "readOnly": True,
    },
    "PercentHuman": {
        "limsField": "PercentHuman",
        "field": "percentHuman",
        "columnHeader": "%Human",
        "readOnly": True,
    },
    "TumorOrNormal": {
        "limsField": "TumorOrNormal",
        "field": "tumorOrNormal",
        "columnHeader": "Tumor/Normal",
        "readOnly": True,
    },
    "SpecimenType": {
        "limsField": "SpecimenType",
        "field": "specimenType",
        "columnHeader": "CMO Sample Type",
        "readOnly": True,
    },
}

rnaColumns = {
    "Rin": {
        "limsField": "Rin",
        "field": "rin",
        "columnHeader": "RIN",
        "readOnly": True,
    },
    "Rqn": {
        "limsField": "Rqn",
        "field": "rqn",
        "columnHeader": "RQN",
        "readOnly": True,
    },
    "DV200": {
        "limsField": "DV200",
        "field": "dV200",
        "columnHeader": "DV200",
        "readOnly": True,
    },
}

libraryColumns = {
    "AvgSize": {
        "limsField": "AvgSize",
        "field": "avgSize",
        "columnHeader": "Average Size",
        "readOnly": True,
    },
    "TumorOrNormal": {
        "limsField": "TumorOrNormal",
        "field": "tumorOrNormal",
        "columnHeader": "Tumor/Normal",
        "readOnly": True,
    },
}

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
]
