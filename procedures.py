
class Procedure:
    def __init__(self):
        pass

    def getAllSurveyData(self):
        strQueryTemplateForAnswerColumn = '''
            COALESCE(
                    (
                        SELECT a.Answer_Value
                        FROM Answer as a
                        WHERE
                            a.UserId = u.UserId
                            AND a.SurveyId = <SURVEY_ID>
                            AND a.QuestionId = <QUESTION_ID>
                    ), -1) AS ANS_Q<QUESTION_ID> 
        '''
        strQueryTemplateForNullColumnn = 'NULL AS ANS_Q<QUESTION_ID> '
        strQueryTemplateOuterUnionQuery = '''
            SELECT
                        UserId
                        , <SURVEY_ID> as SurveyId
                        , <DYNAMIC_QUESTION_ANSWERS>
                FROM
                    [User] as u
                WHERE EXISTS
                (
                        SELECT *
                        FROM Answer as a
                        WHERE u.UserId = a.UserId
                        AND a.SurveyId = <SURVEY_ID>
                )
        '''
        currentSurveyId = 0
        strCurrentUnionQueryBlock = ''
        strFinalQuery = ''

        surveyCursor = 'SELECT SurveyId FROM Survey ORDER BY SurevyId' # cursor
        # fetch all rows
        while (surveyCursor):
            pass

