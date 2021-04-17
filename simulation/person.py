class Person:

    # Initialization function, sets all parameters at once.
    # TODO: have some default parameters if we can't set all of them at once, for initializing them with synthpops.
    def __init__(self, ID, age=0, sex=0, householdLocation=0,
            householdContacts=[], comorbidities=0, demographicInfo=0,
            severityRisk=0, currentLocation=0, infectionState=-1, mortality=0, incubation=0):
        self.setAllParameters(ID, age, sex, householdLocation,
                             householdContacts, comorbidities,
                             demographicInfo, severityRisk, currentLocation,
                             infectionState, mortality, incubation)

    # Sets all parameters.
    def setAllParameters(self, ID, age=0, sex=0, householdLocation=0,
            householdContacts=[], comorbidities=0, demographicInfo=0,
            severityRisk=0, currentLocation=0, infectionState=0, mortality=0, incubation=0):
        self.ID = ID
        self.age = age
        self.sex = sex
        self.householdLocation = householdLocation
        self.householdContacts = householdContacts
        self.comorbidities = comorbidities
        self.demographicInfo = demographicInfo
        self.severityRisk = severityRisk
        self.currentLocation = currentLocation
        # 0: susceptible, 1: asymptomatic, 2: mild, 3: severe, 4: critical, 5: recovered
        self.infectionState = infectionState
        self.mortality = mortality
        self.incubation = incubation
        self.disease = []

    def getID(self):
        return self.ID

    # sets specific parameters from the info available in the synthpops generated population.
    #householdLocation = location, householdMembers = contacts
    """
        age, household ID (hhid), school ID (scid), workplace ID (wpid), workplace industry code (wpindcode) if available, and the IDs of their contacts in different layers. Different layers
        available are households ('H'), schools ('S'), and workplaces ('W'). Contacts in these layers are clustered and thus form a network composed of groups of people interacting with each other. For example, all
        household members are contacts of each other, and everyone in the same school is a contact of each other. Else, return None.
    """
    def setSynthPopParameters(self, synthPopsPersonDict):
        for k, v in synthPopsPersonDict.items():
            setattr(self, k, v)
        self.householdContacts = self.contacts['H']
        self.schoolContacts = self.contacts['S']
        self.workplaceContacts = self.contacts['W']

    # setters for remaining variables
    def setComorbidities(self, comorbidity):
        self.comorbidities = comorbidity

    def setDemographicInfo(self, demographic):
        self.demographicInfo = demographic

    def setSeverityRisk(self):
        self.severityRisk = calcSeverityRisk(self)

    def setMortality(self):
        self.mortality = calcMortality(self)

    def setCurrentLocation(self, location):
        self.currentLocation = location

    # if providing a state
    def setInfectionState(self, state):
        self.infectionState = state

    # no state provided, must calc a state
    def calcInfectionState(self):
        self.infectionState = calcInfectionState(self)


    def setIncubation(self, incubation):
        self.incubation = incubation

    # calculate severity risk based on demographic factors, as of now calculation is undefined.
    def calcSeverityRisk(self):
        numComorbidities = len(self.comorbidities)
        # sex not currently accounted for
        sevRisk = open("diseasedata/severity_risk.dat", "r")
        distrWithComorbidities = {}
        distrWithoutComorbidities = {}
        for lines in sevRisk:
            brackets = lines.split(",")
            distrWithComorbidities[int(brackets[0])] = float(brackets[2])
            distrWithoutComorbidities[int(brackets[0])] = float(brackets[1])
        ageCategory = (self.age / 10) * 10
        if numComorbidities == 0:
            srScore = distrWithoutComorbidities[ageCategory]
        else:
            srScore = distrWithComorbidities[ageCategory] * pow(0.75, numComorbidities)
        close(sevRisk)
        return srScore
 
    def calcInfectionState(self):
        infectionStateByScore = {
            0: [0.7, 0.1, 0.05, 0.05],
            10: [0.6, 0.2, 0.1, 0.1],
            20: [0.5, 0.3, 0.1, 0.1],
            30: [0.4, 0.3, 0.2, 0.1],
            40: [0.3, 0.2, 0.2, 0.1],
            50: [0.3, 0.2, 0.2, 0.1],
            60: [0.2, 0.2, 0.3, 0.3],
            70: [0.1, 0.2, 0.4, 0.3],
            80: [0.05, 0.05, 0.3, 0.6],
            90: [0.05, 0.05, 0.2, 0.7]
        }
        severityScoreCategory = (self.calcSeverityRisk / 10) * 10
        n = np.random.randint(0, 1)
        threshold = (infectionStateByScore[severityScoreCategory])[0]
        if n < threshold:
            return 0 # 0 = asymptomatic
        threshold += (infectionStateByScore[severityScoreCategory])[1]
        if n < threshold:
            return 1 # 1 = mild
        threshold += (infectionStateByScore[severityScoreCategory])[2]
        if n < threshold:
            return 2 # 2 = severe
        else:
            return 3 # 3 = critical

    def calcMortality(self):
        # patient is hospitalized if they are recognized as severe/critical
        if self.infectionState == 2 or self.infectionState == 3:
            probICU = 0.1  # we might need to change this number for probICU
            probVent = 0.76
            probDeathWithVent = 0.339
            probDeathWoutVent = 0.286
            n = np.random.randint(0, 1)
            if  n < probICU:
                #patient is in ICU
                m = np.random.randint(0, 1)
                #patient is using ventilator
                if m < probVent:
                    s = np.random.randint(0, 1)
                    if s < probDeathWithVent:
                        return 1
                #not using ventilator
                else:
                    s = np.random.randint(0, 1)
                    if s < probDeathWoutVent:
                        return 1
            return 0

    # getters for all variables
    def getAge(self):
        return self.age

    def getSex(self):
        return self.sex

    def getComorbidities(self):
        return self.comorbidities

    def getDemographicInfo(self):
        return self.demographicInfo

    def getHouseholdLocation(self):
        return self.householdLocation

    def getHouseholdMembers(self):
        return self.householdMembers

    def getSeverityRisk(self):
        return self.severityRisk

    def getCurrentLocation(self):
        return self.currentLocation

    def getInfectionState(self):
        return self.infectionState

    def getMortality(self):
        return self.mortality

    def getIncubation(self):
        return self.incubation

    def updateIncubation(self):
        self.incubation = self.incubation - 1

    def updateState(self):
        return self.incubation + self.severityRisk

    def addDisease(self, disease):
        self.disease.append(disease)

    def getConditions(self):
        return self.disease

