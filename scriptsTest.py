import sys

sys.path.append("..")
from session import *

"""
contains several script of tests
check them before use them, there are today a tool of debug, and can be modified for my needs
"""


def ScriptTest1():
    """
    basic script : test an activity with 2 criteria and 2 active user
    works
    """
    print(Colors.BOLD + " Appel du script de base" + Colors.ENDC)
    data = const.DefaultData(activityName="generatedActivityb.13")
    rmurray = SessionSerpico("rmurray@yopmail.com")
    rmurray.createActivity(data.dataCreationActivity)
    dataC = data.getDataAddCriteria()
    dataC["criterion[weight]"] = 50
    rmurray.addCriterion(dataC)
    dataC = data.getDataAddCriteria("205")
    dataC["criterion[weight]"] = 50
    rmurray.addCriterion(dataC)
    rmurray.addParticipant(data.getDataAddParticipant())
    rmurray.addParticipant(data.getDataAddParticipant(298, leader=False))
    request = rmurray.ValidateActivity(data.dataValidateActivity)
    with open("expected.html", "w") as f:
        f.write(request.text)
    # Notation
    mserre = SessionSerpico(const.MSERRE, stageNumber=rmurray.stageNumber)
    mserre.GradeActivity(data.getDataNotation())
    # sfeder = SessionSerpico(const.SFEDER, stageNumber=rmurray.stageNumber)
    # sfeder.GradeActivity(data.getDataNotation())
    # with open("rd1.html", "w") as f:
    #     f.write(request.text)


def ScriptTest2():
    """
    a simple script with two active teams and 2 criteria
    should work
    """
    print(Colors.BOLD + " Appel du script a deux teams " + Colors.ENDC)
    data = const.DefaultData(activityName="generatedActivityTeam2.36")
    rmurray = SessionSerpico("rmurray@yopmail.com")
    rmurray.createActivity(data=data.dataCreationActivity)
    rmurray.addCriterion(data.getDataAddCriteria())
    rmurray.addCriterion(data.getDataAddCriteria("205"))
    rmurray.addParticipant(data.getDataAddParticipant(8, leader=True, userType="team"))
    rmurray.addParticipant(data.getDataAddParticipant(9, leader=False, userType="team"))
    data.nbUserGraded[0] = 2
    data.nbTeamGraded[0] = 1
    rmurray.ValidateActivity(data.dataValidateActivity)
    # Notations
    rmurray.GradeActivity(data.getDataNotation())
    mserre = SessionSerpico(const.MSERRE, rmurray.stageNumber)
    mserre.GradeActivity(data.getDataNotation())
    sfeder = SessionSerpico(const.SFEDER, rmurray.stageNumber)
    sfeder.GradeActivity(data.getDataNotation())
    # jleblanc = SessionSerpico(const.JLEBLANC, rmurray.stageNumber)
    # jleblanc.GradeActivity(data.getDataNotation())


def ScriptTestControls():
    """
    will check if the constraint to create an activity are correctly checked
    should work, retry once
    """
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


def testDates():
    """
    some test to modify the dates of notation
    @warining check carefully what it does
    """
    print(Colors.BOLD + " Appel du script de check des contraintes d'activity avec les dates" + Colors.ENDC)
    # tests sur les dates (il faut une activity complète)
    data = const.DefaultData(activityName="generatedActivityWithDatePrb2")
    rmurray = SessionSerpico("rmurray@yopmail.com")
    rmurray.createActivity(data.dataCreationActivity)
    rmurray.addCriterion(data.getDataAddCriteria())
    rmurray.addParticipant(data.getDataAddParticipant())
    rmurray.addParticipant(data.getDataAddParticipant(298, leader=False))
    rmurray.ValidateActivity(data=data.dataValidateActivity)
    sfeder = SessionSerpico(const.SFEDER, stageNumber=rmurray.stageNumber)
    request = sfeder.GradeActivity(data=data.getDataNotation())
    with open("rd1.html", "w") as f:
        f.write(request.text)
    data.dataValidateActivity[const.CHAMPS_GS_DATE] = const.DATE_FUTUR
    data.dataValidateActivity[const.CHAMPS_GE_DATE] = const.DATE_FUTUR
    rmurray.ValidateActivity(data=data.dataValidateActivity)
    # # tentative de notation (marche, pas supposé)
    # mserre = SessionSerpico(const.MSERRE, stageNumber=rmurray.stageNumber)
    # request = mserre.GradeActivity(data.getDataNotation())
    # with open("rd2.html", "w") as f:
    #     f.write(request.text)


def testModifActivity():
    """
    test to modify an activity
    @warning : to be test again
    """
    print(Colors.BOLD + " Appel du script de check des contraintes d'activity en cas d'uptdate" + Colors.ENDC)
    data = const.DefaultData(activityName="generatedActivityToUpdate")
    rmurray = SessionSerpico("rmurray@yopmail.com")
    rmurray.createActivity(data.dataCreationActivity)
    rmurray.addCriterion(data.getDataAddCriteria())
    rmurray.addParticipant(data.getDataAddParticipant())
    request = rmurray.addParticipant(data.getDataAddParticipant(298, leader=False, type=0))
    idFeder = request.json()["eid"]
    rmurray.ValidateActivity(data=data.dataValidateActivity)
    # s note
    # sfeder = SessionSerpico(const.SFEDER, stageNumber=rmurray.stageNumber)
    # request = sfeder.GradeActivity(data=data.getDataNotation())
    # with open("rd1.html", "w") as f:
    #     f.write(request.text)
    # # s passe en tiers
    # request = rmurray.addParticipant(data.getDataAddParticipant(298, leader=False, type=1, update=1), userId=idFeder)
    # with open("rd2.html", "w") as f:
    #     f.write(request.text)
    # request = rmurray.ValidateActivity(data=data.dataValidateActivity)
    # with open("rd3.html", "w") as f:
    #     f.write(request.text)
    # s renote
    sfeder = SessionSerpico(const.SFEDER, stageNumber=rmurray.stageNumber)
    request = sfeder.GradeActivity(data=data.getDataNotation())
    with open("rd1.html", "w") as f:
        f.write(request.text)
    # ajout d'un critère
    rmurray.addCriterion(data.getDataAddCriteria(criteriaName="205"))


def scriptTestNotation1():
    """
    Config : 1 user et une team actif
    team : 8 (rmurray + serre)
    user : 298 (sfeder)
    should work properly
    """
    print(Colors.BOLD + " Appel du script de test de notation 1 " + Colors.ENDC)
    print(Colors.BOLD + "config : " + Colors.ENDC + " 1user and 1 team")
    data = const.DefaultData(activityName="generatedActivityNotation1.3")
    rmurray = SessionSerpico("rmurray@yopmail.com")
    rmurray.createActivity(data=data.dataCreationActivity)
    rmurray.addCriterion(data.getDataAddCriteria())
    rmurray.addParticipant(data.getDataAddParticipant(8, leader=True, userType="team"))
    rmurray.addParticipant(data.getDataAddParticipant(298, leader=False, userType="user"))
    data.nbUserGraded[0] = 3
    data.nbTeamGraded[0] = 0
    rmurray.ValidateActivity(data.dataValidateActivity)
    # Notations
    rmurray.GradeActivity(data.getDataNotation())
    mserre = SessionSerpico(const.MSERRE, rmurray.stageNumber)
    mserre.GradeActivity(data.getDataNotation())
    data.nbUserGraded[0] = 1
    data.nbTeamGraded[0] = 1
    sfeder = SessionSerpico(const.SFEDER, rmurray.stageNumber)
    sfeder.GradeActivity(data.getDataNotation())


def scriptTestNotation2():
    """
    Config : 1 team tier et une team passive
    team tiers : 8
    team passive : 9
    should work proprely
    """
    print(Colors.BOLD + " Appel du script de test de notation 2 " + Colors.ENDC)
    print(Colors.BOLD + "config : " + Colors.ENDC + " 1 team tiers et 1 team passive")
    data = const.DefaultData(activityName="generatedActivityNotation2.1")
    rmurray = SessionSerpico("rmurray@yopmail.com")
    rmurray.createActivity(data=data.dataCreationActivity)
    rmurray.addCriterion(data.getDataAddCriteria())
    rmurray.addParticipant(data.getDataAddParticipant(8, leader=True, userType="team", type=0))
    rmurray.addParticipant(data.getDataAddParticipant(9, leader=False, userType="team", type=-1))
    data.nbUserGraded[0] = 0
    data.nbTeamGraded[0] = 1
    rmurray.ValidateActivity(data.dataValidateActivity)
    # Notations
    rmurray.GradeActivity(data.getDataNotation())
    # mserre = SessionSerpico(const.MSERRE, rmurray.stageNumber)
    # mserre.GradeActivity(data.getDataNotation())


def script3Criteria():
    print(Colors.BOLD + " Appel du script de test avec 3 criteria" + Colors.ENDC)
    name = "generatedActivity3Criteria1.1"
    data = const.DefaultData(activityName=name)
    rmurray = SessionSerpico("rmurray@yopmail.com")
    rmurray.createActivity(data=data.dataCreationActivity)
    rmurray.addCriterion(data.getDataAddCriteria(weight=100, weightF=33))
    rmurray.addCriterion(data.getDataAddCriteria("205", weight=50, weightF=33))
    rmurray.addCriterion(data.getDataAddCriteria("206", weight=34, weightF=34))
    rmurray.addParticipant(data.getDataAddParticipant(8, leader=True, userType="team"))
    data.nbUserGraded[0] = 2
    data.nbTeamGraded[0] = 0
    dataValidate = data.dataValidateActivity
    rmurray.ValidateActivity(data=dataValidate)
    rmurray.GradeActivity(data.getDataNotation())



def scriptTestNotationPhaseAndUser():
    """
    Config : 2 teams actives
    Some bug in the app (flush problems)
    """
    print(Colors.BOLD + " Appel du script de test de la phase et des users" + Colors.ENDC)
    print(Colors.BOLD + "config : " + Colors.ENDC + " 2 teams actives, notation de la phase et des users")
    name = "generatedActivityPAU1.1"
    data = const.DefaultData(activityName=name)
    rmurray = SessionSerpico("rmurray@yopmail.com")
    rmurray.createActivity(data=data.dataCreationActivity)
    rmurray.setStageBoth(data=data.getDataUpdateStage(name=name, mode=2))
    rmurray.addCriterion(data.getDataAddCriteria(weight=100, weightF=50))
    rmurray.addCriterion(data.getDataAddCriteria("205", weight=50, weightF=50))
    rmurray.addParticipant(data.getDataAddParticipant(8, leader=True, userType="team"))
    rmurray.addParticipant(data.getDataAddParticipant(9, leader=False, userType="team"))
    data.nbUserGraded[0] = 2
    data.nbTeamGraded[0] = 1
    data.stageGrade = True
    dataValidate = data.dataValidateActivity
    dataValidate["activity_element_form[activeModifiableStages][0][mode]"] = 2
    rmurray.ValidateActivity(data=dataValidate)
    # # Notations
    # rmurray.GradeActivity(data.getDataNotation(firstStage=0))
    # mserre = SessionSerpico(const.MSERRE, rmurray.stageNumber)
    # mserre.GradeActivity(data.getDataNotation(firstStage=2))
    # sfeder = SessionSerpico(const.SFEDER, rmurray.stageNumber)
    # sfeder.GradeActivity(data.getDataNotation(firstStage=4))
    # jleblanc = SessionSerpico(const.JLEBLANC, rmurray.stageNumber)
    # jleblanc.GradeActivity(data.getDataNotation(firstStage=6))


def affichageScriptControl(request, expectedContent):
    if request.text.__contains__(expectedContent):
        print(Colors.OKGREEN + "OK" + Colors.ENDC)
    else:
        with open("erreur1.html", "w") as f:
            f.write(request.text)
        print(Colors.BOLD + "Expected message : '" + Colors.ENDC + expectedContent + Colors.BOLD + "'" + Colors.ENDC)
        print(Colors.FAIL + "ERROR NOT SPOTTED" + Colors.ENDC)


# ScriptTest1()
ScriptTest2()
# ScriptTestControls()
# testDates()
# testModifActivity()
# scriptTestNotation2()
# scriptTestNotationPhaseAndUser()
# script3Criteria()
