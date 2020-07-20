import sys

sys.path.append("..")


class URLConst:
    URL_LOCAL_HOST = "http://localhost:8888/fr/"
    URL_CREATION_ACTIVITY = URL_LOCAL_HOST + "institution/activity/process/0"
    URL_GET_TOKEN = URL_LOCAL_HOST + "activity/"
    URL_GET_DATA = URL_LOCAL_HOST + "institution/activity/config/"
    URL_AJOUT_CRITERION_L = URL_LOCAL_HOST + "activity/"
    URL_AJOUT_CRITERION_M = "/stage/"
    URL_AJOUT_CRITERION_R = "/criterion/validate/0"
    URL_AJOUT_USER_L = URL_LOCAL_HOST + "activity/stage/"
    URL_AJOUT_USER_R = "/participant/validate/0"
    URL_SAVE_ACTIVITY = URL_LOCAL_HOST + "activity/"
    URL_GET_GRADE_TOKEN_L = URL_LOCAL_HOST + "activity/"
    URL_GET_GRADE_TOKEN_R = "/grade"
    DELETE_URL = "http://localhost:8888/ajax/activity/delete/"

    @staticmethod
    def URL_AJOUT_USER(stageNumber):
        return URLConst.URL_AJOUT_USER_L + str(stageNumber) + URLConst.URL_AJOUT_USER_R

    @staticmethod
    def URL_AJOUT_CRITERION(activityNumber, stageNumber):
        return URLConst.URL_AJOUT_CRITERION_L + str(activityNumber) + URLConst.URL_AJOUT_CRITERION_M + str(stageNumber) \
               + URLConst.URL_AJOUT_CRITERION_R

    @staticmethod
    def URL_GET_GRADE_TOKEN(stageNumber):
        return URLConst.URL_GET_GRADE_TOKEN_L + str(stageNumber) + URLConst.URL_GET_GRADE_TOKEN_R


class DefaultData:

    ID = {'_password': "Serpico2019", '_remember_me': "on", '_target_path': "home"}
    DATA_INIT = {"fi": 1, "up": 1, "m": 1, "an": "generatedActivity", "im": 0}
    DATA_ADD_PARTICIPANT = {"precomment": ""}
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
    DATA_POST_GRADE = {"stage_unique_participations[userGradableParticipations][0][receivedGrades][0][value]": 3.50,
                       "stage_unique_participations[userGradableParticipations][0][receivedGrades][0][comment]": "",
                       "stage_unique_participations[finalize]": "",
                       }

    def __init__(self, mail="rmurray@yopmail.com", activityName="generatedActivity"):
        self.connection_data = DefaultData.ID
        self.connection_data["_username"] = mail
        self.dataCreationActivity = DefaultData.DATA_INIT
        self.dataCreationActivity["an"] = activityName
        self.dataValidateActivity = DefaultData.DATA_VALIDATE_ACTIVITY
        self.dataValidateActivity["activity_element_form[name]"] = activityName
        self.indexCriteria = [0]
        self.indexParticipant = [0]

    def getDataAddCriteria(self, criteriaName="204", lowerbound="0", upperbound="5", weight="100", stageIndex=0):
        dataAddCriteria = DefaultData.DATA_ADD_CRITERIA
        dataAddCriteria["lowerbound"] = lowerbound
        dataAddCriteria["upperbound"] = upperbound
        dataAddCriteria["weight"] = weight
        # Set the validation data
        keyBase = "activity_element_form[activeModifiableStages][" + str(stageIndex) + "][criteria][" + str(
            self.indexCriteria[stageIndex]) + "]["
        keyWeight = keyBase + "weight]"
        self.dataValidateActivity[keyWeight] = 100
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
        return dataAddCriteria

    def getDataAddParticipant(self, participantId=303, type=1, leader=True, userType="user", stage=0):
        dataAddParticipant = DefaultData.DATA_ADD_PARTICIPANT
        dataAddParticipant["pElmtType"] = userType
        dataAddParticipant["pElmtId"] = participantId
        dataAddParticipant["type"] = type
        if leader:
            dataAddParticipant["leader"] = True
        # Add data in validation data
        keyBase = "activity_element_form[activeModifiableStages][" + str(stage) + "][independantUniqueIntParticipations][" + str(self.indexParticipant[stage]) + "]["
        keyDirectUser = keyBase + "directUser]"
        self.dataValidateActivity[keyDirectUser] = participantId
        keyType = keyBase + "type]"
        self.dataValidateActivity[keyType] = type
        keyPreco = keyBase + "precomment]"
        self.dataValidateActivity[keyPreco] = ""
        if leader:
            keyLeader = keyBase + "leader]"
            self.dataValidateActivity[keyLeader] = 1
        self.indexParticipant[stage] += 1
        return dataAddParticipant

    DATA_INIT_TEAM = {"fi": 1, "up": 1, "m": 1, "an": "generatedActivityTeam", "im": 0}
    DATA_ADD_MEMBER = {
        "pElmtType": "user", "pElmtId": 303, "type": 1, "precomment": "", "leader": True}
    DATA_ADD_MEMBER_2 = {"pElmtType": "user", "pElmtId": 298, "type": 1, "precomment": ""}

    DATA_ADD_TEAM_23 = {"pElmtType": "team", "pElmtId": 8, "type": 1, "precomment": "", "leader": True}
    DATA_ADD_TEAM_DREAM_TEAM = {"pElmtType": "team", "pElmtId": 9, "type": 1, "precomment": ""}

    DATA_SAVE_ACTIVITY = {
        "clicked-btn": "update",
        "activity_element_form[name]": "generatedActivity",
        "activity_element_form[activeModifiableStages][0][activeWeight]": 100,
        "activity_element_form[activeModifiableStages][0][name]": "generatedActivity",
        "activity_element_form[activeModifiableStages][0][startdate]": "20/07/2020",
        "activity_element_form[activeModifiableStages][0][gstartdate]": "20/07/2020",
        "activity_element_form[activeModifiableStages][0][enddate]": "20/07/2020",
        "activity_element_form[activeModifiableStages][0][genddate]": "20/07/2020",
        "activity_element_form[activeModifiableStages][0][mode]": 1,
        "activity_element_form[activeModifiableStages][0][visibility]": 3,
        "activity_element_form[activeModifiableStages][0][criteria][0][weight]": 100,
        "activity_element_form[activeModifiableStages][0][criteria][0][cName]": 204,
        "activity_element_form[activeModifiableStages][0][criteria][0][type]": 1,
        "activity_element_form[activeModifiableStages][0][criteria][0][forceCommentSign]": "smaller",
        "activity_element_form[activeModifiableStages][0][criteria][0][forceCommentValue]": "",
        "activity_element_form[activeModifiableStages][0][criteria][0][lowerbound]": 0,
        "activity_element_form[activeModifiableStages][0][criteria][0][upperbound]": 5,
        "activity_element_form[activeModifiableStages][0][criteria][0][step]": 0.5,
        "activity_element_form[activeModifiableStages][0][criteria][0][targetValue]": "",
        "activity_element_form[activeModifiableStages][0][criteria][0][comment]": "",
        "activity_element_form[activeModifiableStages][0][independantUniqueIntParticipations][0][directUser]": 303,
        "activity_element_form[activeModifiableStages][0][independantUniqueIntParticipations][0][leader]": 1,
        "activity_element_form[activeModifiableStages][0][independantUniqueIntParticipations][0][type]": 1,
        "activity_element_form[activeModifiableStages][0][independantUniqueIntParticipations][0][precomment]": "",
        "activity_element_form[activeModifiableStages][0][independantUniqueIntParticipations][1][directUser]": 298,
        "activity_element_form[activeModifiableStages][0][independantUniqueIntParticipations][1][type]": 1,
        "activity_element_form[activeModifiableStages][0][independantUniqueIntParticipations][1][precomment]": ""
    }

    DATA_SAVE_TEAM_ACTIVITY = {
        "activity_element_form[name]": "generatedActivityTeam",
        "activity_element_form[activeModifiableStages][0][activeWeight]	": 100,
        "activity_element_form[activeModifiableStages][0][name]	": "generatedActivityTeam",
        "activity_element_form[activeModifiableStages][0][startdate]": "20/07/2020",
        "activity_element_form[activeModifiableStages][0][gstartdate]": "20/07/2020",
        "activity_element_form[activeModifiableStages][0][enddate]": "20/07/2020",
        "activity_element_form[activeModifiableStages][0][genddate]": "20/07/2020",
        "activity_element_form[activeModifiableStages][0][mode]	": 1,
        "activity_element_form[activeModifiableStages][0][visibility": 3,
        "activity_element_form[activeModifiableStages][0][criteria][0][weight": 100,
        "activity_element_form[activeModifiableStages][0][criteria][0][cName]": 204,
        "activity_element_form[activeModifiableStages][0][criteria][0][type]": 1,
        "activity_element_form[activeModifiableStages][0][criteria][0][forceCommentSign]": "smaller",
        "activity_element_form[activeModifiableStages][0][criteria][0][forceCommentValue]": "",
        "activity_element_form[activeModifiableStages][0][criteria][0][lowerbound]": "0",
        "activity_element_form[activeModifiableStages][0][criteria][0][upperbound]": "5",
        "activity_element_form[activeModifiableStages][0][criteria][0][step]": 0.5,
        "activity_element_form[activeModifiableStages][0][criteria][0][targetValue]": "",
        "activity_element_form[activeModifiableStages][0][criteria][0][comment]": "",
        "activity_element_form[activeModifiableStages][0][independantUniqueTeamParticipations][0][team]": 8,
        "activity_element_form[activeModifiableStages][0][independantUniqueTeamParticipations][0][leader]": 1,
        "activity_element_form[activeModifiableStages][0][independantUniqueTeamParticipations][0][type]": 1,
        "activity_element_form[activeModifiableStages][0][independantUniqueTeamParticipations][0][precomment]": "",
        "activity_element_form[activeModifiableStages][0][independantUniqueTeamParticipations][1][team]": 9,
        "activity_element_form[activeModifiableStages][0][independantUniqueTeamParticipations][1][type]": 1,
        "activity_element_form[activeModifiableStages][0][independantUniqueTeamParticipations][1][precomment]": "",
        "clicked-btn": "update",
    }


    @staticmethod
    def getID(mail):
        id = DefaultData.ID
        id["_username"] = mail
        return id
