import json
import sys

sys.path.append("..")
import requests
from Constantes import constantes as const


class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class SessionSerpico:
    """
    ouvre une connexion
    """

    def __init__(self, usermail, stageNumber=0, affichage=True):
        self.headers = {"Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7"}
        self.fileIndex = 1
        self.stageNumber = stageNumber
        with requests.Session() as session:
            # 1 login 1
            if affichage:
                print(Colors.OKBLUE + "connection " + Colors.ENDC)
            x = session.get(const.URLConst.URL_LOCAL_HOST, headers=self.headers)
            # 2 login 2
            data = const.DefaultData.getID(usermail)
            x = session.post("http://localhost:8888/admin/login_check", cookies=session.cookies, headers=self.headers,
                             data=data)
            self.cookies = session.cookies

    def createActivity(self, data=const.DefaultData.DATA_INIT, affichage=True):
        #  Creation
        if affichage:
            print(Colors.OKBLUE + "creation activity" + Colors.ENDC)
        x = requests.post(const.URLConst.URL_CREATION_ACTIVITY, data=data, cookies=self.cookies,
                          headers=self.headers)
        # recuperation des infos
        if affichage:
            print(Colors.OKBLUE + "get data activity" + Colors.ENDC)
        self.activityNumber = x.text[-6:-2]
        if affichage:
            print(Colors.FAIL + 'activity : ' + Colors.ENDC + self.activityNumber)
        cookieAccessData = self.cookies
        cookieAccessData["sorting_type"] = "p"
        cookieAccessData["view_type"] = "p"
        x = requests.post(const.URLConst.URL_GET_DATA + str(self.activityNumber), cookies=cookieAccessData,
                          headers=self.headers)
        self.stageNumber = x.json()["activeStages"][0]["id"]
        # Le get du token_stage
        if affichage:
            print(Colors.OKBLUE + "recuperation des token" + Colors.ENDC)
        x = requests.get(const.URLConst.URL_GET_TOKEN + str(self.activityNumber), cookies=self.cookies,
                         headers=self.headers)
        with open('rd5.html', 'w') as f:
            f.write(x.text)
        indice_token_stage = x.text.find('"stage[_token]" value="') + 23
        indice_token_stage_fin = x.text[indice_token_stage:].find('"') + indice_token_stage
        self.stage_token = x.text[indice_token_stage:indice_token_stage_fin]
        if affichage:
            print(Colors.BOLD + "indice_token_stage : " + Colors.ENDC + str(indice_token_stage))
            print(Colors.BOLD + "indice_token_stage_fin : " + Colors.ENDC + str(indice_token_stage_fin))
            print(Colors.FAIL + "token_stage : " + Colors.ENDC + self.stage_token)
        # le get du token_critere
        indice_token_criteria = x.text.find('"criterion[_token]" value="') + 27
        indice_token_criteria_fin = x.text[indice_token_criteria:].find('"') + indice_token_criteria
        self.criteria_token = x.text[indice_token_criteria:indice_token_criteria_fin]
        if affichage:
            print(Colors.BOLD + "indice_token_criteria : " + Colors.ENDC + str(indice_token_criteria))
            print(Colors.BOLD + "indice_token_criteria_fin : " + Colors.ENDC + str(indice_token_criteria_fin))
            print(Colors.FAIL + "token_criteria : " + Colors.ENDC + self.criteria_token)
        # le get du yoken d'activity
        indice_token_activity = x.text.find('"activity_element_form[_token]" value="') + 39
        indice_token_activity_fin = x.text[indice_token_activity:].find('"') + indice_token_activity
        self.activity_token = x.text[indice_token_activity:indice_token_activity_fin]
        if affichage:
            print(Colors.BOLD + "indice_token_activity : " + Colors.ENDC + str(indice_token_activity))
            print(Colors.BOLD + "indice_token_activity_fin : " + Colors.ENDC + str(indice_token_activity_fin))
            print(Colors.FAIL + "token_activity : " + Colors.ENDC + self.activity_token)
        self.writeContent(x.text)

    def addParticipant(self, data, affichage=True):
        if affichage:
            print(Colors.OKBLUE + "ajout membres" + Colors.ENDC)
        x = requests.post(const.URLConst.URL_AJOUT_USER(self.stageNumber), data=data,
                          headers=self.headers,
                          cookies=self.cookies)
        self.writeContent(x.text)
        return x

    def addCriterion(self, data, affichage=True):
        if affichage:
            print(Colors.OKBLUE + "ajout criteria" + Colors.ENDC)
        data["criterion[_token]"] = self.criteria_token
        x = requests.post(const.URLConst.URL_AJOUT_CRITERION(self.activityNumber, self.stageNumber),
                          data=data,
                          cookies=self.cookies, headers=self.headers)

    def ValidateActivity(self, data, affichage=True):
        if affichage:
            print(Colors.OKBLUE + "finalisation activity" + Colors.ENDC)
        dataSaveActivity = data
        dataSaveActivity["activity_element_form[_token]"] = self.activity_token
        with open("tiers.html", 'w') as f:
            f.write(json.dumps(dataSaveActivity, indent=4, sort_keys=True))
        x = requests.post(const.URLConst.URL_SAVE_ACTIVITY + str(self.activityNumber), data=dataSaveActivity,
                          cookies=self.cookies, headers=self.headers)
        return x

    def GradeActivity(self, data, affichage=True):
        if affichage:
            print(Colors.OKBLUE + "Get du token de notation" + Colors.ENDC)
        x = requests.get(url=const.URLConst.URL_GET_GRADE_TOKEN(self.stageNumber), headers=self.headers,
                         cookies=self.cookies)
        with open('rd10.html', 'w') as f:
            f.write(x.text)
        indice_token_grade = x.text.find('"stage_unique_participations[_token]" value="') + 45
        indice_token_grade_fin = x.text[indice_token_grade:].find('"') + indice_token_grade
        grade_token = x.text[indice_token_grade:indice_token_grade_fin]
        if affichage:
            print(Colors.BOLD + "indice_token_grade : " + Colors.ENDC + str(indice_token_grade))
            print(Colors.BOLD + "indice_token_grade_fin : " + Colors.ENDC + str(indice_token_grade_fin))
            print(Colors.FAIL + "token_grade : " + Colors.ENDC + grade_token)

        # Send de la note
            print(Colors.OKBLUE + "Envoie de la note" + Colors.ENDC)
        dataPostGrade = data
        dataPostGrade["stage_unique_participations[_token]"] = grade_token
        x = requests.post(const.URLConst.URL_GET_GRADE_TOKEN(self.stageNumber), headers=self.headers,
                          cookies=self.cookies, data=dataPostGrade)

    def deleteActivity(self, affichage=True):
        if affichage:
            print(Colors.OKBLUE + "Suppression de l'activty" + Colors.ENDC)
        x = requests.post(const.URLConst.URL_DELETE(self.activityNumber), headers=self.headers,
                          cookies=self.cookies)

    def writeContent(self, text):
        nameFile = 'rd' + str(self.fileIndex) + '.html'
        with open(nameFile, 'w') as f:
            f.write(text)


def ScriptTest1():
    print(Colors.BOLD + " Appel du script de base" + Colors.ENDC)
    data = const.DefaultData(activityName="generatedActivity")
    rmurray = SessionSerpico("rmurray@yopmail.com")
    rmurray.createActivity(data.dataCreationActivity)
    rmurray.addCriterion(data.getDataAddCriteria())
    rmurray.addParticipant(data.getDataAddParticipant())
    rmurray.addParticipant(data.getDataAddParticipant(298, leader=False))
    request = rmurray.ValidateActivity(data.dataValidateActivity)
    with open("expected.html", "w") as f:
        f.write(request.text)
    # Notation
    mserre = SessionSerpico("mserre@yopmail.com", rmurray.stageNumber)
    mserre.GradeActivity(data.getDataNotation())


def ScriptTest2():
    print(Colors.BOLD + " Appel du script a deux teams " + Colors.ENDC)
    data = const.DefaultData(activityName="generatedActivityTeam")
    rmurray = SessionSerpico("rmurray@yopmail.com", af)
    rmurray.createActivity(data=data.dataCreationActivity)
    rmurray.addCriterion(data.getDataAddCriteria())
    rmurray.addParticipant(data.getDataAddParticipant(8, leader=True, userType="team"))
    rmurray.addParticipant(data.getDataAddParticipant(9, leader=False, userType="team"))
    rmurray.ValidateActivity(data.dataValidateActivity)
    # Notations


def ScriptTestControls():
    print(Colors.BOLD + " Appel du script de check des contraintes d'activity " + Colors.ENDC)
    data = const.DefaultData(activityName="generatedActivityWithErrors")
    rmurray = SessionSerpico(const.RMURRAY, affichage=False)
    rmurray.createActivity(data.dataCreationActivity, affichage=False)
    # Activity sans rien
    request = rmurray.ValidateActivity(data.dataValidateActivity, affichage=False)
    print(Colors.BOLD + "Activity sans critere ni participant : " + Colors.ENDC, end=" ")
    affichageScriptControl(request, const.ERROR_ACTIVITY_VIDE)
    # Activity sans critere (avec un tiers)
    rmurray.addParticipant(data.getDataAddParticipant(type=0), affichage=False)
    request = rmurray.ValidateActivity(data.dataValidateActivity, affichage=False)
    print(Colors.BOLD + "Activity sans critere : " + Colors.ENDC, end=" ")
    affichageScriptControl(request, const.ERROR_ACTIVITY_VIDE)
    # Test qu'avec des tiers (rajout critere)
    rmurray.addParticipant(data.getDataAddCriteria(), affichage=False)
    request = rmurray.ValidateActivity(data.dataValidateActivity, affichage=False)
    print(Colors.BOLD + "Activity sans graded : " + Colors.ENDC, end=" ")
    affichageScriptControl(request, const.ERROR_ACTIVITY_VIDE)
    # reset, pas le choix
    rmurray.deleteActivity(affichage=False)
    rmurray = SessionSerpico(const.RMURRAY, affichage=False)
    data = const.DefaultData(activityName="generatedActivityWithErrors2")
    rmurray.createActivity(data.dataCreationActivity, affichage=False)
    # Tests sans participant
    rmurray.addCriterion(data.getDataAddCriteria(), affichage=False)
    request = rmurray.ValidateActivity(data.dataValidateActivity, affichage=False)
    print(Colors.BOLD + "Activity sans participant : " + Colors.ENDC, end=" ")
    affichageScriptControl(request, const.ERROR_ACTIVITY_VIDE)
    # Test sans owner
    rmurray.addParticipant(data.getDataAddParticipant(leader=False), affichage=False)
    request = rmurray.ValidateActivity(data.dataValidateActivity, affichage=False)
    print(Colors.BOLD + "Activity sans owner : " + Colors.ENDC, end=" ")
    affichageScriptControl(request, const.ERROR_NO_OWNER)
    rmurray.deleteActivity()

def affichageScriptControl(request, expectedContent):
    if request.text.__contains__(expectedContent):
        print(Colors.OKGREEN + "OK" + Colors.ENDC)
    else:
        with open("erreur1.html", "w") as f:
            f.write(request.text)
        print(Colors.BOLD + "Expected message : '" + Colors.ENDC + expectedContent + Colors.BOLD + "'" + Colors.ENDC )
        print(Colors.FAIL + "ERROR NOT SPOTTED" + Colors.ENDC)
# ScriptTest1()
ScriptTestControls()
