import sys
import json

sys.path.append("..")

# Mails
RMURRAY = "rmurray@yopmail.com"
MSERRE = "mserre@yopmail.com"
SFEDER = "s.federspiel@yopmail.com"
JLEBLANC = "jleblanc@yopmail.com"
#Erroe message
ERROR_ACTIVITY_VIDE = "Assurez-vous qu&#039;au moins une phase possède au minimum un participant qui donne ses " \
                      "retours et un participant qui en reçoit, sur base d&#039;un sondage ou d&#039;un ou plusieurs " \
                      "critères d&#039;évaluation"
ERROR_NO_OWNER = "Assurez-vous qu&#039;au moins une phase configurée ait un participant owner, en droit de la " \
                 "configurer"
# random data
CHAMPS_GS_DATE = "activity_element_form[activeModifiableStages][0][gstartdate]"
CHAMPS_GE_DATE = "activity_element_form[activeModifiableStages][0][genddate]"
DATE_FUTUR = "20/07/2024"


class URLConst:
    """
    provide all the urls
    """
    URL_LOCAL_HOST = "http://localhost:8888/fr/"
    URL_CREATION_ACTIVITY = URL_LOCAL_HOST + "institution/activity/process/0"
    URL_GET_TOKEN = URL_LOCAL_HOST + "activity/"
    URL_GET_DATA = URL_LOCAL_HOST + "institution/activity/config/"
    URL_AJOUT_CRITERION_L = URL_LOCAL_HOST + "activity/"
    URL_AJOUT_CRITERION_M = "/stage/"
    URL_AJOUT_CRITERION_R = "/criterion/validate/0"
    URL_AJOUT_USER_L = URL_LOCAL_HOST + "activity/stage/"
    URL_AJOUT_USER_R = "/participant/validate/"
    URL_UPDATE_STAGE_M = "/stage/validate/"
    URL_SAVE_ACTIVITY = URL_LOCAL_HOST + "activity/"
    URL_GET_GRADE_TOKEN_L = URL_LOCAL_HOST + "activity/"
    URL_GET_GRADE_TOKEN_R = "/grade"
    DELETE_URL = "http://localhost:8888/ajax/activity/delete/"

    @staticmethod
    def URL_AJOUT_USER(stageNumber, userId=0):
        return URLConst.URL_AJOUT_USER_L + str(stageNumber) + URLConst.URL_AJOUT_USER_R + str(userId)

    @staticmethod
    def URL_AJOUT_CRITERION(activityNumber, stageNumber):
        return URLConst.URL_AJOUT_CRITERION_L + str(activityNumber) + URLConst.URL_AJOUT_CRITERION_M + str(stageNumber) \
               + URLConst.URL_AJOUT_CRITERION_R

    @staticmethod
    def URL_UPDATE_STAGE(activityNumber, stageNumber):
        return URLConst.URL_GET_TOKEN + str(activityNumber) + URLConst.URL_UPDATE_STAGE_M + str(stageNumber)

    @staticmethod
    def URL_GET_GRADE_TOKEN(stageNumber):
        return URLConst.URL_GET_GRADE_TOKEN_L + str(stageNumber) + URLConst.URL_GET_GRADE_TOKEN_R

    @staticmethod
    def URL_DELETE(activityNumber):
        return URLConst.DELETE_URL + str(activityNumber)


class DefaultData:
    """
    build the data for the session module
    @WARNING : getAddCriteria and getAddParticipant will modify the validation data,
    don't call them if they are not used to be sent to the app
    """
    ID = {'_password': "Serpico2019", '_remember_me': "on", '_target_path': "home"}
    DATA_INIT = {"fi": 1, "up": 1, "m": 1, "an": "generatedActivity", "im": 0}
    DATA_ADD_CRITERIA = {"criterion[type]": "1",
                         "criterion[lowerbound]": "0",
                         "criterion[upperbound]": "5",
                         "criterion[step]": "1",
                         "criterion[forceCommentSign]": "smaller",
                         "criterion[forceCommentValue]": "",
                         "criterion[targetValue]": "",
                         "criterion[comment]": "",
                         "criterion[weight]": "100",
                         "criterion[cName]": "204"}
    DATA_VALIDATE_ACTIVITY = {
        "clicked-btn": "update",
        "activity_element_form[activeModifiableStages][0][activeWeight]": 100,
        "activity_element_form[activeModifiableStages][0][name]": "generatedActivity",
        "activity_element_form[activeModifiableStages][0][startdate]": "20/07/2020",
        "activity_element_form[activeModifiableStages][0][gstartdate]": "20/07/2020",
        "activity_element_form[activeModifiableStages][0][enddate]": "20/07/2021",
        "activity_element_form[activeModifiableStages][0][genddate]": "20/07/2021",
        "activity_element_form[activeModifiableStages][0][mode]": 1,
        "activity_element_form[activeModifiableStages][0][visibility]": 3,
    }
    DATA_UPDATE_STAGE = {
        "stage[visibility]": 3,
        "stage[name]": "fjlyefam:",
        "stage[activeWeight]": 100,
        "stage[startdate]": "20/07/2020",
        "stage[enddate]": "20/07/2021",
        "stage[gstartdate]": "23/07/2020",
        "stage[genddate]": "23/07/2020",
        "stage[mode]": 2,
    }
    DATA_POST_GRADE = {"stage_unique_participations[userGradableParticipations][0][receivedGrades][0][value]": 3.50,
                       "stage_unique_participations[userGradableParticipations][0][receivedGrades][0][comment]": "",
                       "stage_unique_participations[finalize]": "",
                       }

    def __init__(self, mail="rmurray@yopmail.com", activityName="generatedActivity"):
        self.connection_data = DefaultData.ID
        self.stageGrade = False
        self.connection_data["_username"] = mail
        self.dataCreationActivity = DefaultData.DATA_INIT.copy()
        self.dataCreationActivity["an"] = activityName
        self.dataValidateActivity = DefaultData.DATA_VALIDATE_ACTIVITY.copy()
        self.dataValidateActivity["activity_element_form[name]"] = activityName
        self.dataValidateActivity["activity_element_form[activeModifiableStages][0][name]"] = activityName
        self.indexCriteria = [0]
        self.indexParticipantUser = [0]
        self.indexParticipantTeam = [0]
        self.nbUserGraded = [0]
        self.nbTeamGraded = [0]

    def getDataAddCriteria(self, criteriaName="204", lowerbound="0", upperbound="5", weight=100, weightF=100,
                           stageIndex=0):
        """
        @param weight : the current weight (for the creation)
        @param weightF : the weight for the validation data
        """
        dataAddCriteria = DefaultData.DATA_ADD_CRITERIA.copy()
        dataAddCriteria["criterion[lowerbound]"] = lowerbound
        dataAddCriteria["criterion[upperbound]"] = upperbound
        dataAddCriteria["criterion[weight]"] = weight
        dataAddCriteria["criterion[cName]"] = criteriaName
        # Set the validation data
        keyBase = "activity_element_form[activeModifiableStages][" + str(stageIndex) + "][criteria][" + str(
            self.indexCriteria[stageIndex]) + "]["
        keyWeight = keyBase + "weight]"
        self.dataValidateActivity[keyWeight] = weightF
        keyCName = keyBase + "cName]"
        self.dataValidateActivity[keyCName] = criteriaName
        keyType = keyBase + "type]"
        self.dataValidateActivity[keyType] = 1
        keyCommentSign = keyBase + "forceCommentSign]"
        self.dataValidateActivity[keyCommentSign] = "smaller"
        keyCommentValue = keyBase + "forceCommentValue]"
        self.dataValidateActivity[keyCommentValue] = ""
        keyLowerBound = keyBase + "lowerbound]"
        self.dataValidateActivity[keyLowerBound] = lowerbound
        keyUpperBound = keyBase + "upperbound]"
        self.dataValidateActivity[keyUpperBound] = upperbound
        keyStep = keyBase + "step]"
        self.dataValidateActivity[keyStep] = 0.5
        keyTarget = keyBase + "targetValue]"
        self.dataValidateActivity[keyTarget] = ""
        keyComment = keyBase + "comment]"
        self.dataValidateActivity[keyComment] = ""
        self.indexCriteria[stageIndex] += 1
        # return the data
        with open("rd5.html", "w") as f:
            f.write(json.dumps(dataAddCriteria, indent=4))
        return dataAddCriteria

    """
    update : 0 if creation, else : index of updated one
    """

    def getDataAddParticipant(self, participantId=303, type=1, leader=True, userType="user", stage=0, update=0):
        """
        @param participantId : the id of the add participant (can be a team id)
        @param type : 1 : active, 0 : third, -1 : passive
        @param leader : True if the participant is leader, false else (be carefull, don't make mistakes, or the
                        validation data will be false
        @param userType : value in "user" or "team"
        @param stage : the index of the stage (not the stage Number)
        @param update : @deprecated it's functionality is too hard to implement, so don't use
        """
        dataAddParticipant = {"precomment": "", "pElmtType": userType, "pElmtId": participantId, "type": type}
        if leader:
            dataAddParticipant["leader"] = True
        # Add data in validation data
        if userType == "user":
            indexParticipant = self.indexParticipantUser[stage] * (update == 0) + update
            self.indexParticipantUser[stage] += 1
            keyBase = "activity_element_form[activeModifiableStages][" + str(
                stage) + "][independantUniqueIntParticipations][" + str(indexParticipant) + "]["
            keyDirectUser = keyBase + "directUser]"
        elif userType == "team":
            indexParticipant = self.indexParticipantTeam[stage] * (update == 0) + update
            self.indexParticipantTeam[stage] += 1
            keyBase = "activity_element_form[activeModifiableStages][" + str(
                stage) + "][independantUniqueTeamParticipations][" + str(indexParticipant) + "]["
            keyDirectUser = keyBase + "team]"
        self.dataValidateActivity[keyDirectUser] = participantId
        keyType = keyBase + "type]"
        self.dataValidateActivity[keyType] = type
        keyPreco = keyBase + "precomment]"
        self.dataValidateActivity[keyPreco] = ""
        if leader:
            keyLeader = keyBase + "leader]"
            self.dataValidateActivity[keyLeader] = 1
        if not update:
            if type != 0 and userType == "user":
                self.nbUserGraded[stage] += 1
            elif type != 0 and userType == "team":
                self.nbTeamGraded[stage] += 1
        return dataAddParticipant

    def getDataNotation(self, stage=0, firstStage=0):
        """
        get the grade data (today 3.5 for all the graded user)
        @param firstStage : if the stage is graded, the index doesn't start by 0
        """
        data = {"stage_unique_participations[finalize]": ""}
        leftBaseUserKey = "stage_unique_participations[userGradableParticipations]["
        leftBaseTeamKey = "stage_unique_participations[teamGradableParticipations]["
        leftBaseStagekey = "stage_unique_participations[selfGrades]["
        middleBaseKey = "][receivedGrades]["
        value = "][value]"
        comment = "][comment]"
        for criteria in range(self.indexCriteria[stage]):
            for usergraded in range(self.nbUserGraded[stage]):
                baseKey = leftBaseUserKey + str(usergraded) + middleBaseKey + str(criteria)
                key = baseKey + value
                data[key] = 3.5
                key = baseKey + comment
                data[key] = ""
            for teamgraded in range(self.nbTeamGraded[stage]):
                baseKey = leftBaseTeamKey + str(teamgraded) + middleBaseKey + str(criteria)
                key = baseKey + "][value]"
                data[key] = 3.5
                key = baseKey + "][comment]"
                data[key] = ""
            if self.stageGrade:
                baseKey = leftBaseStagekey + str(criteria + firstStage)
                key = baseKey + value
                data[key] = 3.5
                key = baseKey + comment
                data[key] = ""
        return data

    def getDataUpdateStage(self, name, mode=1, weight=100):
        return {"stage[visibility]": 3, "stage[activeWeight]": weight, "stage[startdate]": "20/07/2020",
                "stage[enddate]": "20/07/2021", "stage[gstartdate]": "23/07/2020", "stage[genddate]": "23/07/2020",
                "stage[mode]": mode, "stage[name]": name}

    @staticmethod
    def getID(mail):
        id = DefaultData.ID
        id["_username"] = mail
        return id
