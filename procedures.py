""" DocumentationProcedure
    Description:
        a class used to replicate the functionalities of get_all_survey_data stored procedure
        then returns a string sql query for all surveys data.

    Constructor Parameters:
      db_connection (object): pyodbc object connection object to execute sql queries with connected with database.
"""


class Procedure:
    def __init__(self, db_connection):
        self._dbc = db_connection
        self._str_query_template_for_answer_column = '''
            COALESCE(
            (
                SELECT  a.Answer_Value
                FROM    Answer as a
                WHERE   a.UserId = u.UserId
                        AND a.SurveyId = <SURVEY_ID>
                        AND a.QuestionId = <QUESTION_ID>
            ), 
            -1
            ) AS ANS_Q<QUESTION_ID>
        '''
        self._str_query_template_for_null_column = ' NULL AS ANS_Q<QUESTION_ID> '
        self._str_query_template_outer_union_query = '''
            SELECT
                    UserId
                    , <SURVEY_ID> as SurveyId
                    , <DYNAMIC_QUESTION_ANSWERS>
            FROM    [User] as u
            WHERE EXISTS
            (
                SELECT  *
                FROM    Answer as a
                WHERE   u.UserId = a.UserId
                        AND a.SurveyId = <SURVEY_ID>
            )
        '''
        self._str_final_query = ''

    """ Documentation
    Description:
        get_all_survey_data returns a string sql query for all surveys data

    Parameters:
      argument1 (int): Description of arg1

    Returns:
      string: sql query if you executed it then it will return all surveys data.
    """
    def get_all_survey_data(self):
        self._survey_cursor()
        return self._str_final_query

    """ Documentation
       Description:
           _survey_cursor private method, it replicate the work of survey cursor in the stored procedure
    """
    def _survey_cursor(self):
        survey_cursor_query = '''
            SELECT      SurveyId
            FROM        Survey
            ORDER BY    SurveyId;
        '''

        survey_cursor_df = self._dbc.run(survey_cursor_query)
        survey_cursor_df_length = len(survey_cursor_df)

        for surveyIndex, surveyRow in survey_cursor_df.iterrows():
            current_survey_id = surveyRow['SurveyId']

            str_columns_query_part = self._current_question_cursor(current_survey_id)

            str_current_union_query_block = self._str_query_template_outer_union_query.replace(
                '<DYNAMIC_QUESTION_ANSWERS>'
                , str_columns_query_part
            )

            str_current_union_query_block = str_current_union_query_block.replace(
                '<SURVEY_ID>'
                , str(current_survey_id)
            )

            self._str_final_query += str_current_union_query_block

            if survey_cursor_df_length > surveyIndex + 1:
                self._str_final_query += ' UNION '

    """ Documentation
      Description:
          _current_question_cursor: a private method, returns sql query, if it executed then will return all data related 
          to survey with provided id as a parameter  

      Parameters:
        current_survey_id (int): Id of survey in the Survey table.

      Returns:
        string: sql query if you executed it it will return the information about this survey.
    """
    def _current_question_cursor(self, current_survey_id):
        current_question_cursor_query = f'''
            SELECT  *
            FROM
            (
                SELECT  SurveyId
                        , QuestionId
                        , 1 as InSurvey
                FROM    SurveyStructure
                WHERE   SurveyId = {current_survey_id}
                UNION
                    SELECT  {current_survey_id} as SurveyId
                            , Q.QuestionId
                            , 0 as InSurvey
                    FROM    Question as Q
                    WHERE NOT EXISTS
                    (
                        SELECT  *
                        FROM    SurveyStructure as S
                        WHERE   S.SurveyId = {current_survey_id} 
                        AND S.QuestionId = Q.QuestionId
                    )
            ) as t
            ORDER BY QuestionId;
        '''

        current_question_cursor_df = self._dbc.run(current_question_cursor_query)
        current_question_cursor_df_length = len(current_question_cursor_df)

        str_columns_query_part = ''
        for currentQuestionIndex, currentQuestionRow in current_question_cursor_df.iterrows():
            current_question_id = currentQuestionRow['QuestionId']
            current_in_survey = currentQuestionRow['InSurvey']

            if current_in_survey == 0:
                str_columns_query_part += self._str_query_template_for_null_column.replace(
                    '<QUESTION_ID>'
                    , str(current_question_id)
                )
            else:
                str_columns_query_part += self._str_query_template_for_answer_column.replace(
                    '<QUESTION_ID>'
                    , str(current_question_id)
                )

            if current_question_cursor_df_length > (currentQuestionIndex + 1):
                str_columns_query_part += ' , '

        return str_columns_query_part
