*** Settings ***
Library 	Browser


Test Teardown		Close Browser		ALL

*** Variables ***
#  https://www.tryton.org/download

${Site}			https://demo.tryton.org/
${User}			demo
${Pass}			demo


*** Test Cases ***
Tryton Create Sale
	Tryton Login
	Sleep    10
	Expand Sales Catagory
	Sleep    10
	Open Sales
	Sleep    10
	Click New Sale
	Sleep    10
	Enter Party		a
	Sleep    10
	Add Product 	A4 	13
	Sleep    10
	Click Button 	Quote
	Sleep    10
	Click Button 	Confirm
	Wait For Elements State		//button[@title="Process"]		visible
	Sleep    10

*** Keywords ***

Tryton Login
	New Browser		chromium		False
	# ${old_timeout} =    Set Browser Timeout    5 m
	${old_timeout} =    Set Browser Timeout    1 m
	${secs} = 	Get Time 	epoch
	${har} =    Create Dictionary     path=${CURDIR}${/}tryton_${secs}.har
	New Context		 recordHar=${har}
	New Page		${Site}
	Wait For Elements State		//input[@name="login"]		visible
	Fill Text		//input[@name="login"]		${User}
	# Fill Text		//input[@name="password"]		${Pass}
	Click				//button[@type="submit"]
	# wait for menu to load
	Wait For Elements State		(//img[@style="margin-left: 0em;"])[1]		visible

Expand Sales Catagory
	Click				(//div[@class="column-char" and @title="Sales"])[1]
	Wait For Elements State		(//div[@class="column-char" and @title="Sales"])[2]		visible

Open Sales
	# (//div[@title="Sales"])[2]		//div[@class="column-char" and @title="Sales"]
	Click				(//div[@class="column-char" and @title="Sales"])[2]
	Wait For Elements State		//a[@data-toggle="tab" and text()="Draft "]		visible

Click New Sale
	Click				//button[@title="New"]
	Wait For Elements State		//input[@name="party"]		visible

Enter Party
		[Arguments] 	${party}
		Fill Text		//input[@name="party"] 	${party}
		Wait For Elements State		(//input[@name="party"]/../ul/li)[1]		visible
		Click				(//input[@name="party"]/../ul/li)[1]

Add Product
	[Arguments] 	${productname} 	${quantity}
	Click 	(//button[@title="New"])[2]
	Wait For Elements State		//input[@name="product"]		visible
	Fill Text		//input[@name="product"] 	${productname}
	Wait For Elements State		(//input[@name="product"]/../ul/li)[1]		visible
	Click				(//input[@name="product"]/../ul/li)[1]

	Fill Text		(//input[@name="quantity"])[1] 	${quantity}

	Click				//button[@title="OK"]
	Wait For Elements State		//td[@data-title="Quantity: "]//div[text()="${quantity}"]		visible

Click Button
	[Arguments] 	${name}
	Click				//button[@title="${name}"]





		#
