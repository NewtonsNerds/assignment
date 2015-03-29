Feature: Development logger
  Program allows users to create create and view logs 
  Manaegers are able to view all logs

Scenario: User requests to create new log 
	Given user has requested to create a new log
	Then the new logs view is shown

Scenario: User wants to save where all fields are valid 
	Given user wants to save and all field are valid
		Then user is returned to the new log page with a message

Scenario: User tries to save with an invalid user selected
	Given user tried to save with invalid user selected
		Then user is returned to the new log page with a message

Scenario: User tries to save a log with invalid start time
	Given user tried to save with invalid start time
		Then user is returned to the new log page with a message

Scenario: User tries to save with invalid end time
	Given user tried to save with invalid end time
		Then user is returned to the new log page with a message

Scenario: User tries to save with invalid notes
	Given user tried to save with invalid notes
		Then user is returned to the new log page with a message
