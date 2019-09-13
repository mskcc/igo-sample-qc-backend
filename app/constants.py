sharedColumns = {
    "sampleId": {
        "limsField": "SampleId",
        "field": "sampleId",
        "columnHeader": "IGO ID",
        "readOnly": True,
    },
    "otherSampleId": {
        "limsField": "OtherSampleId",
        "field": "otherSampleId",
        "columnHeader": "Sample Name",
        "readOnly": True,
    },
    # "altId": {"limsField": "AltId", "field": "altId", "columnHeader": "AltId","readOnly":True,},
    "userSampleID": {
        "limsField": "UserSampleID",
        "field": "userSampleID",
        "columnHeader": "UserSampleID",
        "readOnly": True,
    },
    "concentrationUnits": {
        "limsField": "ConcentrationUnits",
        "field": "concentrationUnits",
        "columnHeader": "ConcentrationUnits",
        "readOnly": True,
    },
    "preservation": {
        "limsField": "Preservation",
        "field": "preservation",
        "columnHeader": "Preservation",
        "readOnly": True,
    },
    "recipe": {
        "limsField": "Recipe",
        "field": "recipe",
        "columnHeader": "Recipe",
        "readOnly": True,
    },
    "igoQcRecommendation": {
        "limsField": "IgoQcRecommendation",
        "field": "igoQcRecommendation",
        "columnHeader": "IgoQcRecommendation",
        "readOnly": True,
    },
    "comments": {
        "limsField": "Comments",
        "field": "comments",
        "columnHeader": "Comments",
        "readOnly": True,
    },
    "dateCreated": {
        "limsField": "DateCreated",
        "field": "dateCreated",
        "columnHeader": "Date Created",
        "readOnly": True,
    },
    "concentration": {
        "limsField": "Concentration",
        "field": "concentration",
        "columnHeader": "Concentration",
        "readOnly": True,
    },
    "volume": {
        "limsField": "Volume",
        "field": "volume",
        "columnHeader": "Volume",
        "readOnly": True,
    },
    "totalMass": {
        "limsField": "TotalMass",
        "field": "totalMass",
        "columnHeader": "Total Mass",
        "readOnly": True,
    },
}

dnaColumns = {
    "din": {
        "limsField": "Din",
        "field": "din",
        "columnHeader": "Din",
        "readOnly": True,
    },
    "percentHuman": {
        "limsField": "PercentHuman",
        "field": "percentHuman",
        "columnHeader": "%Human",
        "readOnly": True,
    },
    "tumorOrNormal": {
        "limsField": "TumorOrNormal",
        "field": "tumorOrNormal",
        "columnHeader": "Tumor/Normal",
        "readOnly": True,
    },
    "specimenType": {
        "limsField": "SpecimenType",
        "field": "specimenType",
        "columnHeader": "CMO Sample Type",
        "readOnly": True,
    },
}

rnaColumns = {
    "rin": {
        "limsField": "Rin",
        "field": "rin",
        "columnHeader": "RIN",
        "readOnly": True,
    },
    "rqn": {
        "limsField": "Rqn",
        "field": "rqn",
        "columnHeader": "RQN",
        "readOnly": True,
    },
    "dV200": {
        "limsField": "DV200",
        "field": "dV200",
        "columnHeader": "DV200",
        "readOnly": True,
    },
}

libraryColumns = {
    "avgSize": {
        "limsField": "AvgSize",
        "field": "avgSize",
        "columnHeader": "Average Size",
        "readOnly": True,
    },
    "tumorOrNormal": {
        "limsField": "TumorOrNormal",
        "field": "tumorOrNormal",
        "columnHeader": "Tumor/Normal",
        "readOnly": True,
    },
}

dnaOrder = ["Recipe", "IgoQcRecommendation", "Comments", "SampleId", "OtherSampleId", "Concentration", "ConcentrationUnits", "Volume", "TotalMass", "DIN", "SpecimenType", "TumorOrNormal", "Preservation"]

rnaOrder = ["Recipe", "IgoQcRecommendation", "Comments", "SampleId", "OtherSampleId", "Concentration", "ConcentrationUnits", "Volume", "TotalMass", "RIN", "DV200", "Preservation", "RQN"]

libraryOrder = ["Recipe", "IgoQcRecommendation", "Comments", "SampleId", "OtherSampleId", "AvgSize", "Concentration", "ConcentrationUnits", "Volume", "TotalMass", "TumorOrNormal"]


