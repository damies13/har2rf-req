*** Settings ***
Library 	Browser


Test Teardown		Close Browser		ALL

*** Variables ***
${Site}			https://opensource-demo.orangehrmlive.com/
${User}			Admin
${Pass}			admin123


*** Test Cases ***
Orangehrm Pass And End If Exists
	Orangehrm Login
	Sleep		10

	Orangehrm PIM
	Sleep		10

	Orangehrm Create Employee Pass		Person		Demo		1313
	Sleep		10

	Orangehrm Leave

	Sleep		10


# Orangehrm Pass And Continue If Exists
# 	Orangehrm Login
#
# 	Orangehrm PIM
#
# 	Orangehrm Create Employee Return		Person		Demo		1313
#
# 	Orangehrm Leave
#
# 	Sleep		10



*** Keywords ***

Orangehrm Login
	New Browser		chromium		False
	${old_timeout} =    Set Browser Timeout    5 m
	${secs} = 	Get Time 	epoch
	${har} =    Create Dictionary     path=${CURDIR}${/}orangehrm_${secs}.har
	New Context		 recordHar=${har}
	New Page		${Site}
	Wait For Elements State		//input[@name="username"]		visible
	Fill Text		//input[@name="username"]		${User}
	Fill Text		//input[@name="password"]		${Pass}
	Click				//button[@type="submit"]
	Wait For Elements State		//*[text()="PIM"]		visible


Orangehrm PIM
	Click		//a/span[text()="PIM"]
	Wait For Elements State		button > i.bi-plus		visible

Orangehrm Leave
	Click		//a/span[text()="Leave"]
	Wait For Elements State		button[type="submit"]		visible

Orangehrm Create Employee Pass
	[Arguments]		${Surname}		${Given1}		${IdNumber}
	Click 	button > i.bi-plus
	Wait For Elements State		input.orangehrm-lastname		visible
	Fill Text		input.orangehrm-lastname		${Surname}
	Fill Text		input.orangehrm-firstname		${Given1}
	Fill Text		//label[text()="Employee Id"]/../..//input		${IdNumber}

	Click 	button[type="submit"]

	# //label[text()="Employee Id"]/../..//span
	# span.oxd-input-field-error-message
	${exists}= 	Run Keyword And Return Status 	Wait For Elements State		//label[text()="Employee Id"]/../..//span		visible		10
	IF		${exists}
		${msg}=    Get Text    //label[text()="Employee Id"]/../..//span
		IF		"${msg}" == "Employee Id already exists"
			Pass Execution				${msg}
		ELSE
			Fail		${msg}
		END
	END

	Log 	Fill in rest of the User Details

	Fill Text		//label[text()="Date of Birth"]/../..//input		1999-06-06
	Click 	button[type="submit"]

	Click		//a/span[text()="PIM"]


Orangehrm Create Employee Return
	[Arguments]		${Surname}		${Given1}		${IdNumber}
	Click 	button > i.bi-plus
	Wait For Elements State		input.orangehrm-lastname		visible
	Fill Text		input.orangehrm-lastname		${Surname}
	Fill Text		input.orangehrm-firstname		${Given1}
	Fill Text		//label[text()="Employee Id"]/../..//input		${IdNumber}

	Click 	button[type="submit"]

	# //label[text()="Employee Id"]/../..//span
	# span.oxd-input-field-error-message
	${exists}= 	Run Keyword And Return Status 	Wait For Elements State		//label[text()="Employee Id"]/../..//span		visible		10
	IF		${exists}
		${msg}=    Get Text    //label[text()="Employee Id"]/../..//span
		IF		"${msg}" == "Employee Id already exists"
			Return From Keyword		${msg}
		ELSE
			Fail		${msg}
		END
	END

	Log 	Fill in rest of the User Details

	Fill Text		//label[text()="Date of Birth"]/../..//input		1999-06-06
	Click 	button[type="submit"]

	Click		//a/span[text()="PIM"]
