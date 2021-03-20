USE [Survey_Sample_A19]
GO
/****** Object:  StoredProcedure [dbo].[getAllSurveyData]    Script Date: 3/20/2021 5:33:45 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
-- =============================================
-- Author:		<Author,,Name>
-- Create date: <Create Date,,>
-- Description:	<Description,,>
-- =============================================
ALTER PROCEDURE [dbo].[getAllSurveyData]
	AS
BEGIN
	-- SET NOCOUNT ON added to prevent extra result sets from
	-- interfering with SELECT statements.
	SET NOCOUNT ON;

	DECLARE @strQueryTemplateForAnswerColumn nvarchar(max);
	DECLARE @strQueryTemplateForNullColumnn nvarchar(max);
	DECLARE @strQueryTemplateOuterUnionQuery nvarchar(max);
	DECLARE @currentSurveyId int;

	-- WHEN YOU WRITE DYNAMIC SQL IN STRING VARIABLES
	-- IT'S LIKELY THAT YOU WILL CONCATENATE STRINGS LATER ON IN THE PROCESS
	-- SO, BE CAREFULL OF LEAVING SPACES BEFORE AND AFTER THE QUERY TEXT
	SET @strQueryTemplateForAnswerColumn = '
			COALESCE(
				(
					SELECT a.Answer_Value
					FROM Answer as a
					WHERE
						a.UserId = u.UserId
						AND a.SurveyId = <SURVEY_ID>
						AND a.QuestionId = <QUESTION_ID>
				), -1) AS ANS_Q<QUESTION_ID> ';

	SET @strQueryTemplateForNullColumnn = ' NULL AS ANS_Q<QUESTION_ID> '

	SET @strQueryTemplateOuterUnionQuery = '
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
	';

	DECLARE @strCurrentUnionQueryBlock nvarchar(max);
	SET @strCurrentUnionQueryBlock = ''


	DECLARE @strFinalQuery nvarchar(max);
	SET @strFinalQuery = ''

	--Cursor variables are the only ones to not have an @ in front of their names
	DECLARE surveyCursor CURSOR FOR
							SELECT SurveyId
							FROM Survey
							ORDER BY SurveyId;

	OPEN surveyCursor; -- when opened, the cursor is before the first row
	FETCH NEXT FROM surveyCursor INTO @currentSurveyId; --first row read

	WHILE @@FETCH_STATUS = 0 --AS LONG AS FETCH_STATUS IS EQUAL TO 0 --> there's a row to read
	BEGIN

		-- MAIN LOOP, OVER ALL THE SURVEYS

		-- FOR EACH SURVEY, IN @currentSurveyId, WE NEED TO CONSTRUCT THE ANSWER COLUMN QUERIES

		-- Another iteration, over the questions of the survey
		-- inner loop, another cursor

		--I want a resultset of SurveyId, QuestionId, flag InSurvey indicating whether
		-- the question is in the survey structure
		DECLARE currentQuestionCursor CURSOR FOR
			SELECT *
					FROM
					(
						SELECT
							SurveyId,
							QuestionId,
							1 as InSurvey
						FROM
							SurveyStructure
						WHERE
							SurveyId = @currentSurveyId
						UNION
						SELECT
							@currentSurveyId as SurveyId,
							Q.QuestionId,
							0 as InSurvey
						FROM
							Question as Q
						WHERE NOT EXISTS
						(
							SELECT *
							FROM SurveyStructure as S
							WHERE S.SurveyId = @currentSurveyId AND S.QuestionId = Q.QuestionId
						)
					) as t
					ORDER BY QuestionId;

		DECLARE @currentSurveyIdInQuestion int;
		DECLARE @currentQuestionID int;
		DECLARE @currentInSurvey int;

		OPEN currentQuestionCursor;
		--When fetching into local variable, the column order of the select clause must be followed
		FETCH NEXT FROM currentQuestionCursor INTO @currentSurveyIdInQuestion,
													@currentQuestionID,
													@currentInSurvey;

		DECLARE @strColumnsQueryPart nvarchar(max);

		SET @strColumnsQueryPart = '';
		WHILE @@FETCH_STATUS = 0
		BEGIN
			--the "global" variable @@FETCH_STATUS GETS LOCALISED BETWEEN BEGIN --- END BLOCK

			--INNER LOOP IETERATES OVER THE QUESTION

			--IS THE CURRENT QUESTION (inner loop) IN THE CURRENT SURVEY (outer loop)

			IF @currentInSurvey = 0 -- CURRENT QUESTION IS NOT IN THE CURRENT SURVEY
			BEGIN
				--THEN BLOCK
				-- SPECIFICATION: THE VALUES IN THIS COLUMN WILL BE NULL
				SET @strColumnsQueryPart = @strColumnsQueryPart +
						REPLACE(@strQueryTemplateForNullColumnn, '<QUESTION_ID>',
								@currentQuestionID);
			END
			ELSE
			BEGIN
				SET @strColumnsQueryPart = @strColumnsQueryPart +
					REPLACE(@strQueryTemplateForAnswerColumn, '<QUESTION_ID>',
							@currentQuestionID);
			END;

			FETCH NEXT FROM currentQuestionCursor INTO @currentSurveyIdInQuestion,
													@currentQuestionID,
													@currentInSurvey;

		IF @@FETCH_STATUS = 0
		BEGIN
			-- Place a comma between column statements, except for the last one
			SET @strColumnsQueryPart = @strColumnsQueryPart + ' , ';
		END;

		END; -- END OF CLOSE INNER LOOP WHILE
		CLOSE currentQuestionCursor;
		DEALLOCATE currentQuestionCursor;


		--BACK IN THE OUTER LOOP OVER SURVEYS
		SET @strCurrentUnionQueryBlock =
			REPLACE(@strQueryTemplateOuterUnionQuery,
					'<DYNAMIC_QUESTION_ANSWERS>',
					@strColumnsQueryPart);

		SET @strCurrentUnionQueryBlock =
			REPLACE(@strCurrentUnionQueryBlock,
						'<SURVEY_ID>', @currentSurveyId);

		SET @strFinalQuery = @strFinalQuery + @strCurrentUnionQueryBlock

		FETCH NEXT FROM surveyCursor INTO @currentSurveyId;

		IF @@FETCH_STATUS = 0
		BEGIN
			SET @strFinalQuery = @strFinalQuery + ' UNION ' ;
		END;

	END;

	CLOSE surveyCursor;
	DEALLOCATE surveyCursor;

	--SELECT @strFinalQuery;

	--calling the system store procedure sp_executesql
	--recommended by Microsoft should the text of your dynamic query > 4000 chars

	PRINT @strFinalQuery;
	-- EXEC sp_executesql @strFinalQuery;
END
