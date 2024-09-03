import csv
import random


class Factor(object):
    def __init__(self, id, name, status, time):
        self.id = id
        self.name = name
        self.status = status
        self.time = time

    def show(self):
        print("id: " + str(self.id) + "; name: " + str(self.name) + "; status: " + str(self.status) + "; time: " + str(self.time))
        return


class Person(Factor):
    def __init__(self, habit, location):
        self.disease = None
        self.habit = habit
        self.location = location


    def move(self):
        return

    def getIn(self):
        return

    def getOut(self):
        return

    def use(self):
        return


class HomeAppliance(Factor):
    def __init__(self, location, effectLevel):
        self.location = location
        self.effectLevel = effectLevel

    def setStatus(self):
        return


class Environment(Factor):
    def __init__(self, temperature, humidity, ilumination, noiseLevel):
        self.temperature = temperature
        self.humidity = humidity
        self.ilumination = ilumination
        self.noiseLevel = noiseLevel

    def getEnvironmentInfo(self):
        print("temperature: " + str(self.temperature) + "; humidity: " + str(self.humidity) + "; ilumination: " + str(self.ilumination) + "; noiseLevel: " + str(self.noiseLevel))
        return


class Internal(Environment):
    def __init__(self, size):
        self.size = size

    def getEnvironmentFromApplianceEffect(self):
        return


class Weather(Environment):
    def __init__(self, level):
        self.level = level

    def setEffect(self):
        return


class VirtualSpace(object):
    def __init__(self, size, location, people,appliances,environment):
        self.factors = None
        self.size = size
        self.location = location
        self.people=people
        self.appliances=appliances
        self.environment=environment


    def show(self):
        print("size: " + str(self.size) + "; location: " + str(self.location) + "; factors: " + str(self.factors))
        return

    def getEvent(self):
        return


class Reasoning(object):
    def __init__(self, dbConnection, refSmartHome, casesFile):
        self.dbConnection = dbConnection
        self.refSmartHome = refSmartHome
        self.casesFile = casesFile

    def getCases(self):

        # Read the CSV file and assign diseases and severities to people in VirtualSpace
        try:
            with open(self.casesFile, 'r') as csvfile:
                csvreader = csv.DictReader(csvfile)
                # Convert the CSV rows into a list so we can iterate over it
                cases_list = list(csvreader)
                
                # Iterate over each person in VirtualSpace and assign diseases
                for i in range(0,len(cases_list)):
                    #Create new person for each case
                    person = Person("","")
                    case = cases_list[i]

                    # Assign the disease and severity to the person
                    person.disease = Disease(case['severity'], case['disease'])

                    self.refSmartHome.people.append(person)

                
                # Note: If there are more people than diseases, it will loop back to the start of the disease list.

        except FileNotFoundError:
            raise(FileNotFoundError)

    def doReasoning(self):
        return

    def caseMatching(self):
        return

    def getEnvironmentInfo(self):
        return self.refSmartHome.environment

    def determineDisease(self):
        diseaseNames = [
            
                    "heatstroke", "hypothermia", "frostbite",
                    "asthma", "influenza", "allergies",
                    "common cold", "hay fever", "headache",
                    "dehydration", "skin rash", "sunburn"
                ]
        env = self.getEnvironmentInfo()
        dangerFactor = 0
        seve = "none"

        if env.temperature > 42 or env.temperature < -20 and env.noiseLevel > 80:
            dangerFactor = random.randint(5, 10)
        elif env.temperature > 38 or env.temperature < -15 and env.noiseLevel > 70:
            dangerFactor = random.randint(4, 9)
        elif env.temperature > 35 or env.temperature < -10 and env.noiseLevel > 70:
            dangerFactor = random.randint(3, 7)
        elif env.temperature > 32 and env.noiseLevel > 60:
            dangerFactor = random.randint(1, 4)
        else:
            dangerFactor = random.randint(0, 1)

        if dangerFactor > 8:
            seve = "emergency"
        elif dangerFactor > 6:
            seve = "warning"
        elif dangerFactor > 3:
            seve = "normal"
        elif dangerFactor > 0:
            seve = "low"

        if seve == "none":
            name = "healthy"
        else:
            name = random.choice(diseaseNames)

        dis = Disease(seve, name)

        return dis

    def assignDiseases(self):
        pers = self.refSmartHome.people
        for Person in pers:
            Person.disease = self.determineDisease()


class DBConnection(object):
    def __init__(self, connectionString):
        self.connectionString = connectionString

    def read(self):
        return

    def write(self):
        return

    def close(self):
        return


class Disease(object):
    def __init__(self, severity, name):
        self.name = name
        self.severity = severity

if __name__ == "DataAnalysisModule":
    pass