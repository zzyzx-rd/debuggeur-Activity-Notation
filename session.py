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
    open a connexion with the main app Serpico (simulate a httpclient)
    provide automatic requests to create and grade activities
    Attributes :
        - headers : contains necessary data for the request (otherwise doesn't work) (should not be modified, and must
                    be used for all request
        - cookies : contains the necessary cookies to be recognized by the app
        - stageNumber : the number of the stage, necessary for some URLs
        - activityNumber : same as stageNumber
        - stage_token, activity_token, grade_token, and criteria_token : token used by the app to create/ modify a stage
        - log : parameter of almost all function. if true, display some information about the called function
        - data : contains all the data necessary for a function, you should use the DefaultData from constantes.py, and
                modify them with the adequate function, only if youn know what you do
        (Serpico is quite complex, and it's very easy to send the wrong data, there is some redundancy for ex)
    """

    def __init__(self, usermail, stageNumber=0, log=True):
        """
        Create a session, connect it to Serpico
        @param : usermail : the mail of the used session (some are defined in constants.py, should be used
        @stageNumber : default 0 (if the stage is not yet created, get the stage id if you create an other session
                       working on the same activity.
        """
        self.headers = {"Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7"}
        self.stageNumber = stageNumber
        with requests.Session() as session:
            # 1 login 1
            if log:
                print(Colors.OKBLUE + "connection " + Colors.ENDC)
            x = session.get(const.URLConst.URL_LOCAL_HOST, headers=self.headers)
            # 2 login 2
            data = const.DefaultData.getID(usermail)
            x = session.post("http://localhost:8888/admin/login_check", cookies=session.cookies, headers=self.headers,
                             data=data)
            self.cookies = session.cookies

    def createActivity(self, data=const.DefaultData.DATA_INIT, log=True):
        """
        Create an activity (the first request, when you go on the setting page.
        Will also get all the token necessary to create an activity, and the activity/stageNumber
        """
        #  Creation
        if log:
            print(Colors.OKBLUE + "creation activity" + Colors.ENDC)
        x = requests.post(const.URLConst.URL_CREATION_ACTIVITY, data=data, cookies=self.cookies,
                          headers=self.headers)
        # get the information
        if log:
            print(Colors.OKBLUE + "get data activity" + Colors.ENDC)
        self.activityNumber = x.text[-6:-2]
        if log:
            print(Colors.OKBLUE + "get data activity" + Colors.ENDC)
        if self.activityNumber == " one":
            print(Colors.FAIL + 'activity already exist : ' + Colors.ENDC + self.activityNumber)
        cookieAccessData = self.cookies
        cookieAccessData["sorting_type"] = "p"
        cookieAccessData["view_type"] = "p"
        x = requests.post(const.URLConst.URL_GET_DATA + str(self.activityNumber), cookies=cookieAccessData,
                          headers=self.headers)
        self.stageNumber = x.json()["activeStages"][0]["id"]
        # Le get du token_stage
        if log:
            print(Colors.OKBLUE + "recuperation des token" + Colors.ENDC)
        x = requests.get(const.URLConst.URL_GET_TOKEN + str(self.activityNumber), cookies=self.cookies,
                         headers=self.headers)
        with open('rd5.html', 'w') as f:
            f.write(x.text)
        indice_token_stage = x.text.find('"stage[_token]" value="') + 23
        indice_token_stage_fin = x.text[indice_token_stage:].find('"') + indice_token_stage
        self.stage_token = x.text[indice_token_stage:indice_token_stage_fin]
        if log:
            print(Colors.BOLD + "token_stage : " + Colors.ENDC + self.stage_token)
        # le get du token_critere
        indice_token_criteria = x.text.find('"criterion[_token]" value="') + 27
        indice_token_criteria_fin = x.text[indice_token_criteria:].find('"') + indice_token_criteria
        self.criteria_token = x.text[indice_token_criteria:indice_token_criteria_fin]
        if log:
            print(Colors.BOLD + "token_criteria : " + Colors.ENDC + self.criteria_token)
        # le get du yoken d'activity
        indice_token_activity = x.text.find('"activity_element_form[_token]" value="') + 39
        indice_token_activity_fin = x.text[indice_token_activity:].find('"') + indice_token_activity
        self.activity_token = x.text[indice_token_activity:indice_token_activity_fin]
        if log:
            print(Colors.BOLD + "token_activity : " + Colors.ENDC + self.activity_token)

    def addParticipant(self, data, log=True, userId=0):
        """
        add a participant to the activity
        """
        if log:
            print(Colors.OKBLUE + "ajout membres" + Colors.ENDC)
        with open("rd4.html", "w") as f:
            f.write(json.dumps(data, indent=4))
        x = requests.post(const.URLConst.URL_AJOUT_USER(stageNumber=self.stageNumber, userId=userId),
                          data=data,
                          headers=self.headers,
                          cookies=self.cookies)
        return x

    def addCriterion(self, data, log=True):
        """
        add a criterion to the activity
        """
        if log:
            print(Colors.OKBLUE + "ajout criteria" + Colors.ENDC)
        data["criterion[_token]"] = self.criteria_token
        x = requests.post(const.URLConst.URL_AJOUT_CRITERION(self.activityNumber, self.stageNumber),
                          data=data,
                          cookies=self.cookies, headers=self.headers)

    def setStageBoth(self, data, log=True):
        """
        make the request to modify a stage, for example to change the mode, or the weight
        """
        if log:
            print(Colors.OKBLUE + "Modification stage" + Colors.ENDC)
        data["stage[_token]"] = self.stage_token
        x = requests.post(const.URLConst.URL_UPDATE_STAGE(self.activityNumber, self.stageNumber),
                          data=data,
                          cookies=self.cookies,
                          headers=self.headers)
        if x.json()["message"] != "Success!":
            print(Colors.FAIL + "modification de stage : failed" + Colors.ENDC)
        elif log:
            print(Colors.OKGREEN + "modification de stage : success" + Colors.ENDC)

    def ValidateActivity(self, data, log=True):
        """
        make the request to validate an activity (requires tha the precedent functions have been called, otherwise
        it won't work
        """
        if log:
            print(Colors.OKBLUE + "finalisation activity" + Colors.ENDC)
        dataSaveActivity = data
        dataSaveActivity["activity_element_form[_token]"] = self.activity_token
        with open("tiers.html", 'w') as f:
            f.write(json.dumps(dataSaveActivity, indent=4, sort_keys=True))
        x = requests.post(const.URLConst.URL_SAVE_ACTIVITY + str(self.activityNumber), data=dataSaveActivity,
                          cookies=self.cookies, headers=self.headers)
        return x

    def GradeActivity(self, data, log=True):
        """
        request to grade an activity, and get the grade_token
        """
        if log:
            print(Colors.OKBLUE + "Get du token de notation" + Colors.ENDC)
        x = requests.get(url=const.URLConst.URL_GET_GRADE_TOKEN(self.stageNumber), headers=self.headers,
                         cookies=self.cookies)
        with open('rd10.html', 'w') as f:
            f.write(x.text)
        indice_token_grade = x.text.find('"stage_unique_participations[_token]" value="') + 45
        indice_token_grade_fin = x.text[indice_token_grade:].find('"') + indice_token_grade
        grade_token = x.text[indice_token_grade:indice_token_grade_fin]
        if log:
            print(Colors.BOLD + "token_grade : " + Colors.ENDC + grade_token)

            # Send de la note
            print(Colors.OKBLUE + "Envoie de la note" + Colors.ENDC)
        dataPostGrade = data
        dataPostGrade["stage_unique_participations[_token]"] = grade_token
        with open("dataNotation", "w") as f:
            f.write(json.dumps(dataPostGrade, indent=4))
        x = requests.post(const.URLConst.URL_GET_GRADE_TOKEN(self.stageNumber), headers=self.headers,
                          cookies=self.cookies, data=dataPostGrade)
        return x

    def deleteActivity(self, log=True):
        if log:
            print(Colors.OKBLUE + "Suppression de l'activty" + Colors.ENDC)
        x = requests.post(const.URLConst.URL_DELETE(self.activityNumber), headers=self.headers,
                          cookies=self.cookies)