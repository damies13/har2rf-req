*** Settings ***
Library	RequestsLibrary
Library	String

*** Variables ***
${Accept} 	text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
${Accept-Language} 	en-GB,en;q=0.9
${Connection} 	keep-alive
${Host} 	opensource-demo.orangehrmlive.com
${Sec-Fetch-Dest} 	document
${Sec-Fetch-Mode} 	navigate
${Sec-Fetch-Site} 	none
${Sec-Fetch-User} 	?1
${Upgrade-Insecure-Requests} 	1
${User-Agent} 	Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36
${sec-ch-ua} 	"Not A(Brand";v="24", "Chromium";v="110"
${sec-ch-ua-mobile} 	?0
${sec-ch-ua-platform} 	"Linux"
${Accept_1} 	text/css,*/*;q=0.1
${Referer} 	https://opensource-demo.orangehrmlive.com/web/index.php/auth/login
${Sec-Fetch-Dest_1} 	style
${Sec-Fetch-Mode_1} 	no-cors
${Sec-Fetch-Site_1} 	same-origin
${Accept_2} 	*/*
${Sec-Fetch-Dest_2} 	script
${Sec-Fetch-Dest_3} 	empty
${Sec-Fetch-Mode_2} 	cors
${Accept_4} 	image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8
${Sec-Fetch-Dest_4} 	image
${Referer_1} 	https://opensource-demo.orangehrmlive.com/web/dist/css/app.css?1672659722816
${Origin} 	https://opensource-demo.orangehrmlive.com
${Referer_2} 	https://opensource-demo.orangehrmlive.com/web/dist/css/chunk-vendors.css?1672659722816
${Sec-Fetch-Dest_5} 	font
${Cache-Control} 	max-age=0
${username} 	Admin
${password} 	admin123
${Referer_3} 	https://opensource-demo.orangehrmlive.com/web/index.php/dashboard/index
${If-None-Match} 	"lJyzdvp9dVw7AABygfsIuOb9dNUb5bV3iXeF0n5J6+s="
${timezoneOffset} 	10
${currentTime} 	19:57
${sortOrder} 	DESC
${sortField} 	share.createdAtUtc
${Referer_4} 	https://opensource-demo.orangehrmlive.com/web/index.php/pim/viewEmployeeList
${If-None-Match_1} 	"P2cce+UXjeBpq9iWKfHdQlYTyOgflCghtVN0ewu0gZM="
${limit_1} 	50
${Referer_5} 	https://opensource-demo.orangehrmlive.com/web/index.php/pim/addEmployee
${firstName} 	Demo
${lastName} 	Person
${employeeId} 	1313
${Referer_6} 	https://opensource-demo.orangehrmlive.com/web/index.php/pim/viewPersonalDetails/empNumber/165
${fromDate} 	2023-01-01
${toDate} 	2023-12-31

*** Test Cases ***
orangehrm_1678960667
	Create Session    sess_opensource-demo_orangehrmlive_com 	https://opensource-demo.orangehrmlive.com 	disable_warnings=1
	orangehrm_1678960667 page@b5d221672615da98b56f8383fa96976b


*** Keywords ***
Get Substring LRB
	[Documentation] 	Get Substring using Left and Right Boundaries
	[Arguments] 	${string} 	${LeftB} 	${RightB}
	${left}= 	Fetch From Right 	${string} 	${LeftB}
	${match}= 	Fetch From Left 	${left} 	${RightB}
	[Return] 	${match}

orangehrm_1678960667 page@b5d221672615da98b56f8383fa96976b
	[Documentation] 	orangehrm_1678960667	|	orangehrm_1678960667 page@b5d221672615da98b56f8383fa96976b	|	OrangeHRM
	&{Headers}= 	Create dictionary 	Accept=${Accept} 	Accept-Language=${Accept-Language} 	Connection=${Connection} 	Host=${Host} 	Sec-Fetch-Dest=${Sec-Fetch-Dest} 	Sec-Fetch-Mode=${Sec-Fetch-Mode} 	Sec-Fetch-Site=${Sec-Fetch-Site} 	Sec-Fetch-User=${Sec-Fetch-User} 	Upgrade-Insecure-Requests=${Upgrade-Insecure-Requests} 	User-Agent=${User-Agent} 	sec-ch-ua=${sec-ch-ua} 	sec-ch-ua-mobile=${sec-ch-ua-mobile} 	sec-ch-ua-platform=${sec-ch-ua-platform}
	&{Cookies}= 	Create dictionary
	Update Session	sess_opensource-demo_orangehrmlive_com	${Headers}	${Cookies}
	${resp_0}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/ 	expected_status=302 	allow_redirects=${False}
	${resp_1}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/index.php/auth/login 	expected_status=200
	${_token}= 	Get Substring LRB 	${resp_1.text} 	:token="&quot; 	&quot;"
	Set Global Variable 	${_token}
	${NoKey}= 	Get Substring LRB 	${resp_1.text} 	<link rel="icon" href="/web/dist/favicon.ico? 	">
	Set Global Variable 	${NoKey}
	&{Req_Headers}= 	Create dictionary 	Accept=${Accept_1} 	Referer=${Referer} 	Sec-Fetch-Dest=${Sec-Fetch-Dest_1} 	Sec-Fetch-Mode=${Sec-Fetch-Mode_1} 	Sec-Fetch-Site=${Sec-Fetch-Site_1}
	&{params_2}= 	Create dictionary 	${EMPTY}=${NoKey}
	${resp_2}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/dist/css/chunk-vendors.css 	headers=${Req_Headers} 	params=${params_2} 	expected_status=200
	${offset}= 	Get Substring LRB 	${resp_2.text} 	-column:span 1}.--offset-column-1{grid-column-start:1}.--offset-row-1{grid-row-start:1}}@media(min-width:8 	0px){.--span-column-2{grid-column:span 2}.--offset-column-2{grid-column-start:2}.--offset-row-2{grid
	Set Global Variable 	${offset}
	&{Req_Headers}= 	Create dictionary 	Accept=${Accept_1} 	Referer=${Referer} 	Sec-Fetch-Dest=${Sec-Fetch-Dest_1} 	Sec-Fetch-Mode=${Sec-Fetch-Mode_1} 	Sec-Fetch-Site=${Sec-Fetch-Site_1}
	&{params_3}= 	Create dictionary 	${EMPTY}=${NoKey}
	${resp_3}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/dist/css/app.css 	headers=${Req_Headers} 	params=${params_3} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	Accept=${Accept_2} 	Referer=${Referer} 	Sec-Fetch-Dest=${Sec-Fetch-Dest_2} 	Sec-Fetch-Mode=${Sec-Fetch-Mode_1} 	Sec-Fetch-Site=${Sec-Fetch-Site_1}
	&{params_4}= 	Create dictionary 	${EMPTY}=${NoKey}
	${resp_4}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/dist/js/chunk-vendors.js 	headers=${Req_Headers} 	params=${params_4} 	expected_status=200
	${regx_match}= 	evaluate 	re.search("ll:\\"none\\",stroke:\\"currentColor\\",\\"stroke\\-linecap\\":\\"round\\",\\"stroke\\-linejoin\\":\\"round\\",\\"stroke\\-miterlimit\\":\\"1(.*?)\\",\\"stroke\\-width\\":\\"19px\\"\\},x1:\\"210\\.846\\",x2:\\"146\\.186\\",y1:\\"198\\.917\\",y2:\\"198\\.917\\"\\},null,\\-1\\),ao=Object\\(o\\[\\"", """${resp_4.text}""").group(0) 	re
	${limit_2}= 	Get Substring LRB 	${regx_match} 	ll:"none",stroke:"currentColor","stroke-linecap":"round","stroke-linejoin":"round","stroke-miterlimit":"1 	","stroke-width":"19px"},x1:"210.846",x2:"146.186",y1:"198.917",y2:"198.917"},null,-1),ao=Object(o["
	Set Global Variable 	${limit_2}
	${limit}= 	Get Substring LRB 	${resp_4.text} 	:"round","stroke-miterlimit":"10","stroke-width":"19px"},x1:"220.083",x2:"220.083",y1:"143.494",y2:"134.2 	7"},null,-1),uo=Object(o["createElementVNode"])("line",{style:{fill:"none",stroke:"currentColor","st
	Set Global Variable 	${limit}
	${Accept_5}= 	Get Substring LRB 	${resp_4.text} 	gth:-1,env:{FormData:n("4581")},validateStatus:function(e){return e>=200&&e<300},headers:{common:{Accept:" 	"}}};r.forEach(["delete","get","head"],(function(e){h.headers[e]={}})),r.forEach(["post","put","patc
	Set Global Variable 	${Accept_5}
	${Content-Type}= 	Get Substring LRB 	${resp_4.text} 	n){"use strict";(function(t){var r=n("c532"),o=n("c8af"),i=n("7917"),s=n("cafa"),a=n("e467"),c={"Content-Type":" 	"};function l(e,t){!r.isUndefined(e)&&r.isUndefined(e["Content-Type"])&&(e["Content-Type"]=t)}functi
	Set Global Variable 	${Content-Type}
	${Accept_3}= 	Get Substring LRB 	${resp_4.text} 	gth:-1,env:{FormData:n("4581")},validateStatus:function(e){return e>=200&&e<300},headers:{common:{Accept:" 	, text/plain, */*"}}};r.forEach(["delete","get","head"],(function(e){h.headers[e]={}})),r.forEach(["
	Set Global Variable 	${Accept_3}
	&{Req_Headers}= 	Create dictionary 	Accept=${Accept_2} 	Referer=${Referer} 	Sec-Fetch-Dest=${Sec-Fetch-Dest_2} 	Sec-Fetch-Mode=${Sec-Fetch-Mode_1} 	Sec-Fetch-Site=${Sec-Fetch-Site_1}
	&{params_5}= 	Create dictionary 	${EMPTY}=${NoKey}
	${resp_5}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/dist/js/app.js 	headers=${Req_Headers} 	params=${params_5} 	expected_status=200
	${screen}= 	Get Substring LRB 	${resp_5.text} 	ee-layout");return Object(a["openBlock"])(),Object(a["createBlock"])(f,{"employee-id":o.empNumber,screen:" 	"},{default:Object(a["withCtx"])(()=>[Object(a["createElementVNode"])("div",gb,[Object(a["createVNod
	Set Global Variable 	${screen}
	${model_1}= 	Get Substring LRB 	${resp_5.text} 	r=e=>e>=200&&e<300||403===e,i=async()=>{t.request({type:"GET",url:"api/v2/leave/workweek",params:{model:" 	"},validateStatus:r}).then(({data:t})=>{null!==t&&void 0!==t&&t.data&&(e.attributes=Object.keys(t.da
	Set Global Variable 	${model_1}
	${sortOrder_1}= 	Get Substring LRB 	${resp_5.text} 	tion:t,sortField:o,sortOrder:l,onSort:n}}const Kt={jobTitleName:"",jobDescription:""},Zt={"jt.jobTitleName":" 	"};var eo={components:{"delete-confirmation":Yt},setup(){const e=Object(a["ref"])({...Kt}),{sortDefi
	Set Global Variable 	${sortOrder_1}
	${sortField_1}= 	Get Substring LRB 	${resp_5.text} 	yee.employeeId",style:{flex:1}},{name:"firstAndMiddleName",title:this.$t("pim.first_middle_name"),sortField:" 	",style:{flex:1}},{name:"lastName",title:this.$t("general.last_name"),sortField:"employee.lastName",
	Set Global Variable 	${sortField_1}
	${includeEmployees}= 	Get Substring LRB 	${resp_5.text} 	ee:null,employeeId:"",empStatusId:null,supervisor:null,jobTitleId:null,subunitId:null,includeEmployees:{id:1,param:" 	",label:t("general.current_employees_only")}}),{sortDefinition:n,sortField:r,sortOrder:i,onSort:c}=X
	Set Global Variable 	${includeEmployees}
	${model}= 	Get Substring LRB 	${resp_5.text} 	r,sortOrder:i,onSort:c}=Xt({sortDefinition:pb}),d=Object(a["computed"])(()=>{var e,t,o,a,n;return{model:" 	",nameOrId:"string"===typeof l.value.employee?l.value.employee:void 0,empNumber:null===(e=l.value.em
	Set Global Variable 	${model}
	${Cache-Control_1}= 	Get Substring LRB 	${resp_5.text} 	ex=new RegExp(e)}getAll(e){const t={"Content-Type":"application/json",Accept:"application/json","Cache-Control":" 	"};return this._http.get(this._apiSection,{headers:t,params:e})}get(e,t){const o={"Content-Type":"ap
	Set Global Variable 	${Cache-Control_1}
	${contentType}= 	Get Substring LRB 	${resp_5.text} 	.baseUrl,e.resourceUrl);return{init:function(){return new Promise(e=>{t.request({method:"GET",headers:{Accept:"application/json",contentType:" 	",...!1}}).then(e=>{const{data:t}=e,o={};for(const a in t)o[a]=t[a].t
	Set Global Variable 	${contentType}
	&{Req_Headers}= 	Create dictionary 	Accept=${Accept_3} 	Referer=${Referer} 	Sec-Fetch-Dest=${Sec-Fetch-Dest_3} 	Sec-Fetch-Mode=${Sec-Fetch-Mode_2} 	Sec-Fetch-Site=${Sec-Fetch-Site_1} 	contentType=${contentType}
	${resp_6}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/index.php/core/i18n/messages 	headers=${Req_Headers} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	Accept=${Accept_4} 	Referer=${Referer} 	Sec-Fetch-Dest=${Sec-Fetch-Dest_4} 	Sec-Fetch-Mode=${Sec-Fetch-Mode_1} 	Sec-Fetch-Site=${Sec-Fetch-Site_1}
	&{params_7}= 	Create dictionary 	${EMPTY}=${NoKey}
	${resp_7}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/dist/favicon.ico 	headers=${Req_Headers} 	params=${params_7} 	expected_status=200
	Set Global Variable 	${Content-Type_1}	${resp_7.headers["Content-Type"]}
	&{Req_Headers}= 	Create dictionary 	Accept=${Accept_4} 	Referer=${Referer} 	Sec-Fetch-Dest=${Sec-Fetch-Dest_4} 	Sec-Fetch-Mode=${Sec-Fetch-Mode_1} 	Sec-Fetch-Site=${Sec-Fetch-Site_1}
	&{params_8}= 	Create dictionary 	${EMPTY}=${NoKey}
	${resp_8}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/images/ohrm_branding.png 	headers=${Req_Headers} 	params=${params_8} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	Accept=${Accept_4} 	Referer=${Referer} 	Sec-Fetch-Dest=${Sec-Fetch-Dest_4} 	Sec-Fetch-Mode=${Sec-Fetch-Mode_1} 	Sec-Fetch-Site=${Sec-Fetch-Site_1}
	${resp_9}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/images/ohrm_logo.png 	headers=${Req_Headers} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	Accept=${Accept_4} 	Referer=${Referer_1} 	Sec-Fetch-Dest=${Sec-Fetch-Dest_4} 	Sec-Fetch-Mode=${Sec-Fetch-Mode_1} 	Sec-Fetch-Site=${Sec-Fetch-Site_1}
	${resp_10}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/dist/img/blob.svg 	headers=${Req_Headers} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	Accept=${Accept_2} 	Origin=${Origin} 	Referer=${Referer_2} 	Sec-Fetch-Dest=${Sec-Fetch-Dest_5} 	Sec-Fetch-Mode=${Sec-Fetch-Mode_2} 	Sec-Fetch-Site=${Sec-Fetch-Site_1}
	${resp_11}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/dist/fonts/nunito-sans-v6-latin-ext_latin-800.woff2 	headers=${Req_Headers} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	Accept=${Accept_2} 	Origin=${Origin} 	Referer=${Referer_2} 	Sec-Fetch-Dest=${Sec-Fetch-Dest_5} 	Sec-Fetch-Mode=${Sec-Fetch-Mode_2} 	Sec-Fetch-Site=${Sec-Fetch-Site_1}
	${resp_12}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/dist/fonts/nunito-sans-v6-latin-ext_latin-regular.woff2 	headers=${Req_Headers} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	Accept=${Accept_2} 	Origin=${Origin} 	Referer=${Referer_2} 	Sec-Fetch-Dest=${Sec-Fetch-Dest_5} 	Sec-Fetch-Mode=${Sec-Fetch-Mode_2} 	Sec-Fetch-Site=${Sec-Fetch-Site_1}
	${resp_13}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/dist/fonts/bootstrap-icons.woff2 	headers=${Req_Headers} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	Accept=${Accept_2} 	Origin=${Origin} 	Referer=${Referer_2} 	Sec-Fetch-Dest=${Sec-Fetch-Dest_5} 	Sec-Fetch-Mode=${Sec-Fetch-Mode_2} 	Sec-Fetch-Site=${Sec-Fetch-Site_1}
	${resp_14}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/dist/fonts/nunito-sans-v6-latin-ext_latin-600.woff2 	headers=${Req_Headers} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	Cache-Control=${Cache-Control} 	Content-Type=${Content-Type} 	Origin=${Origin} 	Referer=${Referer} 	Sec-Fetch-Site=${Sec-Fetch-Site_1}
	&{postdata_15}= 	Create dictionary 	_token=${_token} 	username=${username} 	password=${password}
	${resp_15}= 	POST On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/index.php/auth/validate 	headers=${Req_Headers} 	expected_status=302 	allow_redirects=${False} 	data=${postdata_15}
	&{Req_Headers}= 	Create dictionary 	Cache-Control=${Cache-Control} 	Referer=${Referer} 	Sec-Fetch-Site=${Sec-Fetch-Site_1}
	${resp_16}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/index.php/dashboard/index 	headers=${Req_Headers} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	Referer=${Referer_3}
	&{params_17}= 	Create dictionary 	${EMPTY}=${NoKey}
	${resp_17}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/dist/css/chunk-vendors.css 	headers=${Req_Headers} 	params=${params_17} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	Referer=${Referer_3}
	&{params_18}= 	Create dictionary 	${EMPTY}=${NoKey}
	${resp_18}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/dist/css/app.css 	headers=${Req_Headers} 	params=${params_18} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	Referer=${Referer_3}
	&{params_19}= 	Create dictionary 	${EMPTY}=${NoKey}
	${resp_19}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/dist/js/chunk-vendors.js 	headers=${Req_Headers} 	params=${params_19} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	Referer=${Referer_3}
	&{params_20}= 	Create dictionary 	${EMPTY}=${NoKey}
	${resp_20}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/dist/js/app.js 	headers=${Req_Headers} 	params=${params_20} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	Accept=${Accept_3} 	Cache-Control=${Cache-Control} 	If-None-Match=${If-None-Match} 	Referer=${Referer_3} 	Sec-Fetch-Dest=${Sec-Fetch-Dest_3} 	Sec-Fetch-Mode=${Sec-Fetch-Mode_2} 	Sec-Fetch-Site=${Sec-Fetch-Site_1} 	contentType=${contentType}
	${resp_21}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/index.php/core/i18n/messages 	headers=${Req_Headers} 	expected_status=304
	&{Req_Headers}= 	Create dictionary 	Referer=${EMPTY}
	${resp_22}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/dist/fonts/bootstrap-icons.woff2 	headers=${Req_Headers} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	Referer=${EMPTY}
	${resp_23}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/dist/fonts/nunito-sans-v6-latin-ext_latin-regular.woff2 	headers=${Req_Headers} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	Referer=${EMPTY}
	${resp_24}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/dist/fonts/nunito-sans-v6-latin-ext_latin-600.woff2 	headers=${Req_Headers} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	Referer=${EMPTY}
	${resp_25}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/dist/fonts/nunito-sans-v6-latin-ext_latin-800.woff2 	headers=${Req_Headers} 	expected_status=200
	&{params_26}= 	Create dictionary 	${EMPTY}=${NoKey}
	${resp_26}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/dist/favicon.ico 	params=${params_26} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	Accept=${Accept_4} 	Referer=${Referer_3} 	Sec-Fetch-Dest=${Sec-Fetch-Dest_4} 	Sec-Fetch-Mode=${Sec-Fetch-Mode_1} 	Sec-Fetch-Site=${Sec-Fetch-Site_1}
	&{params_27}= 	Create dictionary 	${EMPTY}=${NoKey}
	${resp_27}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/images/orange.png 	headers=${Req_Headers} 	params=${params_27} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	Accept=${Accept_2} 	Origin=${Origin} 	Referer=${Referer_2} 	Sec-Fetch-Dest=${Sec-Fetch-Dest_5} 	Sec-Fetch-Mode=${Sec-Fetch-Mode_2} 	Sec-Fetch-Site=${Sec-Fetch-Site_1}
	${resp_28}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/dist/fonts/nunito-sans-v6-latin-ext_latin-700.woff2 	headers=${Req_Headers} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	Accept=${Accept_2} 	Origin=${Origin} 	Referer=${Referer_2} 	Sec-Fetch-Dest=${Sec-Fetch-Dest_5} 	Sec-Fetch-Mode=${Sec-Fetch-Mode_2} 	Sec-Fetch-Site=${Sec-Fetch-Site_1}
	${resp_29}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/dist/fonts/nunito-sans-v6-latin-ext_latin-italic.woff2 	headers=${Req_Headers} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	Accept=${Accept_4} 	Referer=${Referer_3} 	Sec-Fetch-Dest=${Sec-Fetch-Dest_4} 	Sec-Fetch-Mode=${Sec-Fetch-Mode_1} 	Sec-Fetch-Site=${Sec-Fetch-Site_1}
	&{params_30}= 	Create dictionary 	${EMPTY}=${NoKey}
	${resp_30}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/images/orangehrm-logo.png 	headers=${Req_Headers} 	params=${params_30} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	Accept=${Accept_4} 	Referer=${Referer_3} 	Sec-Fetch-Dest=${Sec-Fetch-Dest_4} 	Sec-Fetch-Mode=${Sec-Fetch-Mode_1} 	Sec-Fetch-Site=${Sec-Fetch-Site_1}
	${resp_31}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/index.php/pim/viewPhoto/empNumber/7 	headers=${Req_Headers} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	Accept=${Accept_4} 	Referer=${Referer_3} 	Sec-Fetch-Dest=${Sec-Fetch-Dest_4} 	Sec-Fetch-Mode=${Sec-Fetch-Mode_1} 	Sec-Fetch-Site=${Sec-Fetch-Site_1}
	${resp_32}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/images/dashboard_empty_widget_watermark.png 	headers=${Req_Headers} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	Accept=${Accept_3} 	Cache-Control=${Cache-Control_1} 	Referer=${Referer_3} 	Sec-Fetch-Dest=${Sec-Fetch-Dest_3} 	Sec-Fetch-Mode=${Sec-Fetch-Mode_2} 	Sec-Fetch-Site=${Sec-Fetch-Site_1}
	${yr} 	${mth} 	${dy} 	${hr} 	${min} 	${sec}= 	Get Time 	year,month,day,hour,min,sec
	${currentDate}=		Set Variable		${yr}-${mth}-${dy}
	Set Global Variable		${currentDate} 	${currentDate}
	&{params_33}= 	Create dictionary 	timezoneOffset=${timezoneOffset} 	currentDate=${currentDate} 	currentTime=${currentTime}
	${resp_33}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/index.php/api/v2/dashboard/employees/time-at-work 	headers=${Req_Headers} 	params=${params_33} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	Accept=${Accept_3} 	Cache-Control=${Cache-Control_1} 	Referer=${Referer_3} 	Sec-Fetch-Dest=${Sec-Fetch-Dest_3} 	Sec-Fetch-Mode=${Sec-Fetch-Mode_2} 	Sec-Fetch-Site=${Sec-Fetch-Site_1}
	${resp_34}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/index.php/api/v2/dashboard/employees/action-summary 	headers=${Req_Headers} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	Accept=${Accept_3} 	Cache-Control=${Cache-Control_1} 	Referer=${Referer_3} 	Sec-Fetch-Dest=${Sec-Fetch-Dest_3} 	Sec-Fetch-Mode=${Sec-Fetch-Mode_2} 	Sec-Fetch-Site=${Sec-Fetch-Site_1}
	${resp_35}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/index.php/api/v2/dashboard/shortcuts 	headers=${Req_Headers} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	Accept=${Accept_5} 	Referer=${Referer_3} 	Sec-Fetch-Dest=${Sec-Fetch-Dest_3} 	Sec-Fetch-Mode=${Sec-Fetch-Mode_2} 	Sec-Fetch-Site=${Sec-Fetch-Site_1}
	&{params_36}= 	Create dictionary 	limit=${limit} 	offset=${offset} 	sortOrder=${sortOrder} 	sortField=${sortField}
	${resp_36}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/index.php/api/v2/buzz/feed 	headers=${Req_Headers} 	params=${params_36} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	Accept=${Accept_3} 	Cache-Control=${Cache-Control_1} 	Referer=${Referer_3} 	Sec-Fetch-Dest=${Sec-Fetch-Dest_3} 	Sec-Fetch-Mode=${Sec-Fetch-Mode_2} 	Sec-Fetch-Site=${Sec-Fetch-Site_1}
	${yr} 	${mth} 	${dy} 	${hr} 	${min} 	${sec}= 	Get Time 	year,month,day,hour,min,sec
	${date}=		Set Variable		${yr}-${mth}-${dy}
	Set Global Variable		${date} 	${date}
	&{params_37}= 	Create dictionary 	date=${date}
	${resp_37}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/index.php/api/v2/dashboard/employees/leaves 	headers=${Req_Headers} 	params=${params_37} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	Accept=${Accept_3} 	Cache-Control=${Cache-Control_1} 	Referer=${Referer_3} 	Sec-Fetch-Dest=${Sec-Fetch-Dest_3} 	Sec-Fetch-Mode=${Sec-Fetch-Mode_2} 	Sec-Fetch-Site=${Sec-Fetch-Site_1}
	${resp_38}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/index.php/api/v2/dashboard/employees/subunit 	headers=${Req_Headers} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	Accept=${Accept_3} 	Cache-Control=${Cache-Control_1} 	Referer=${Referer_3} 	Sec-Fetch-Dest=${Sec-Fetch-Dest_3} 	Sec-Fetch-Mode=${Sec-Fetch-Mode_2} 	Sec-Fetch-Site=${Sec-Fetch-Site_1}
	${resp_39}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/index.php/api/v2/dashboard/employees/locations 	headers=${Req_Headers} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	Accept=${Accept_3} 	Origin=${Origin} 	Referer=${Referer_3} 	Sec-Fetch-Dest=${Sec-Fetch-Dest_3} 	Sec-Fetch-Mode=${Sec-Fetch-Mode_2} 	Sec-Fetch-Site=${Sec-Fetch-Site_1}
	${resp_40}= 	POST On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/index.php/events/push 	headers=${Req_Headers} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	Referer=${Referer_3} 	Sec-Fetch-Site=${Sec-Fetch-Site_1}
	${resp_41}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/index.php/pim/viewPimModule 	headers=${Req_Headers} 	expected_status=302 	allow_redirects=${False}
	&{Req_Headers}= 	Create dictionary 	Referer=${Referer_3} 	Sec-Fetch-Site=${Sec-Fetch-Site_1}
	${resp_42}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/index.php/pim/viewEmployeeList 	headers=${Req_Headers} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	Referer=${Referer_4}
	&{params_43}= 	Create dictionary 	${EMPTY}=${NoKey}
	${resp_43}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/dist/css/chunk-vendors.css 	headers=${Req_Headers} 	params=${params_43} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	Referer=${Referer_4}
	&{params_44}= 	Create dictionary 	${EMPTY}=${NoKey}
	${resp_44}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/dist/css/app.css 	headers=${Req_Headers} 	params=${params_44} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	Referer=${Referer_4}
	&{params_45}= 	Create dictionary 	${EMPTY}=${NoKey}
	${resp_45}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/dist/js/chunk-vendors.js 	headers=${Req_Headers} 	params=${params_45} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	Referer=${Referer_4}
	&{params_46}= 	Create dictionary 	${EMPTY}=${NoKey}
	${resp_46}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/dist/js/app.js 	headers=${Req_Headers} 	params=${params_46} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	Accept=${Accept_3} 	Cache-Control=${Cache-Control} 	If-None-Match=${If-None-Match} 	Referer=${Referer_4} 	Sec-Fetch-Dest=${Sec-Fetch-Dest_3} 	Sec-Fetch-Mode=${Sec-Fetch-Mode_2} 	Sec-Fetch-Site=${Sec-Fetch-Site_1} 	contentType=${contentType}
	${resp_47}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/index.php/core/i18n/messages 	headers=${Req_Headers} 	expected_status=304
	&{Req_Headers}= 	Create dictionary 	Referer=${EMPTY}
	${resp_48}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/dist/fonts/bootstrap-icons.woff2 	headers=${Req_Headers} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	Referer=${EMPTY}
	${resp_49}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/dist/fonts/nunito-sans-v6-latin-ext_latin-regular.woff2 	headers=${Req_Headers} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	Referer=${EMPTY}
	${resp_50}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/dist/fonts/nunito-sans-v6-latin-ext_latin-italic.woff2 	headers=${Req_Headers} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	Referer=${EMPTY}
	${resp_51}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/dist/fonts/nunito-sans-v6-latin-ext_latin-600.woff2 	headers=${Req_Headers} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	Referer=${EMPTY}
	${resp_52}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/dist/fonts/nunito-sans-v6-latin-ext_latin-700.woff2 	headers=${Req_Headers} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	Referer=${EMPTY}
	${resp_53}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/dist/fonts/nunito-sans-v6-latin-ext_latin-800.woff2 	headers=${Req_Headers} 	expected_status=200
	&{params_54}= 	Create dictionary 	${EMPTY}=${NoKey}
	${resp_54}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/dist/favicon.ico 	params=${params_54} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	Referer=${Referer_4}
	&{params_55}= 	Create dictionary 	${EMPTY}=${NoKey}
	${resp_55}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/images/orange.png 	headers=${Req_Headers} 	params=${params_55} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	Referer=${Referer_4}
	&{params_56}= 	Create dictionary 	${EMPTY}=${NoKey}
	${resp_56}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/images/orangehrm-logo.png 	headers=${Req_Headers} 	params=${params_56} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	Accept=${Accept_4} 	If-None-Match=${If-None-Match_1} 	Referer=${Referer_4} 	Sec-Fetch-Dest=${Sec-Fetch-Dest_4} 	Sec-Fetch-Mode=${Sec-Fetch-Mode_1} 	Sec-Fetch-Site=${Sec-Fetch-Site_1}
	${resp_57}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/index.php/pim/viewPhoto/empNumber/7 	headers=${Req_Headers} 	expected_status=304
	&{Req_Headers}= 	Create dictionary 	Accept=${Accept_3} 	Cache-Control=${Cache-Control_1} 	Referer=${Referer_4} 	Sec-Fetch-Dest=${Sec-Fetch-Dest_3} 	Sec-Fetch-Mode=${Sec-Fetch-Mode_2} 	Sec-Fetch-Site=${Sec-Fetch-Site_1}
	&{params_58}= 	Create dictionary 	limit=${limit_1} 	offset=${offset} 	model=${model} 	includeEmployees=${includeEmployees} 	sortField=${sortField_1} 	sortOrder=${sortOrder_1}
	${resp_58}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/index.php/api/v2/pim/employees 	headers=${Req_Headers} 	params=${params_58} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	Accept=${Accept_3} 	Cache-Control=${Cache-Control_1} 	Referer=${Referer_4} 	Sec-Fetch-Dest=${Sec-Fetch-Dest_3} 	Sec-Fetch-Mode=${Sec-Fetch-Mode_2} 	Sec-Fetch-Site=${Sec-Fetch-Site_1}
	&{params_59}= 	Create dictionary 	limit=${limit_2}
	${resp_59}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/index.php/api/v2/admin/employment-statuses 	headers=${Req_Headers} 	params=${params_59} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	Accept=${Accept_3} 	Cache-Control=${Cache-Control_1} 	Referer=${Referer_4} 	Sec-Fetch-Dest=${Sec-Fetch-Dest_3} 	Sec-Fetch-Mode=${Sec-Fetch-Mode_2} 	Sec-Fetch-Site=${Sec-Fetch-Site_1}
	&{params_60}= 	Create dictionary 	limit=${limit_2}
	${resp_60}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/index.php/api/v2/admin/job-titles 	headers=${Req_Headers} 	params=${params_60} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	Accept=${Accept_3} 	Cache-Control=${Cache-Control_1} 	Referer=${Referer_4} 	Sec-Fetch-Dest=${Sec-Fetch-Dest_3} 	Sec-Fetch-Mode=${Sec-Fetch-Mode_2} 	Sec-Fetch-Site=${Sec-Fetch-Site_1}
	${resp_61}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/index.php/api/v2/admin/subunits 	headers=${Req_Headers} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	Referer=${Referer_4} 	Sec-Fetch-Site=${Sec-Fetch-Site_1}
	${resp_62}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/index.php/pim/addEmployee 	headers=${Req_Headers} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	Referer=${Referer_5}
	&{params_63}= 	Create dictionary 	${EMPTY}=${NoKey}
	${resp_63}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/dist/css/chunk-vendors.css 	headers=${Req_Headers} 	params=${params_63} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	Referer=${Referer_5}
	&{params_64}= 	Create dictionary 	${EMPTY}=${NoKey}
	${resp_64}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/dist/css/app.css 	headers=${Req_Headers} 	params=${params_64} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	Referer=${Referer_5}
	&{params_65}= 	Create dictionary 	${EMPTY}=${NoKey}
	${resp_65}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/dist/js/chunk-vendors.js 	headers=${Req_Headers} 	params=${params_65} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	Referer=${Referer_5}
	&{params_66}= 	Create dictionary 	${EMPTY}=${NoKey}
	${resp_66}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/dist/js/app.js 	headers=${Req_Headers} 	params=${params_66} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	Accept=${Accept_3} 	Cache-Control=${Cache-Control} 	If-None-Match=${If-None-Match} 	Referer=${Referer_5} 	Sec-Fetch-Dest=${Sec-Fetch-Dest_3} 	Sec-Fetch-Mode=${Sec-Fetch-Mode_2} 	Sec-Fetch-Site=${Sec-Fetch-Site_1} 	contentType=${contentType}
	${resp_67}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/index.php/core/i18n/messages 	headers=${Req_Headers} 	expected_status=304
	&{Req_Headers}= 	Create dictionary 	Referer=${EMPTY}
	${resp_68}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/dist/fonts/bootstrap-icons.woff2 	headers=${Req_Headers} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	Referer=${EMPTY}
	${resp_69}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/dist/fonts/nunito-sans-v6-latin-ext_latin-regular.woff2 	headers=${Req_Headers} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	Referer=${EMPTY}
	${resp_70}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/dist/fonts/nunito-sans-v6-latin-ext_latin-italic.woff2 	headers=${Req_Headers} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	Referer=${EMPTY}
	${resp_71}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/dist/fonts/nunito-sans-v6-latin-ext_latin-600.woff2 	headers=${Req_Headers} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	Referer=${EMPTY}
	${resp_72}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/dist/fonts/nunito-sans-v6-latin-ext_latin-700.woff2 	headers=${Req_Headers} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	Referer=${EMPTY}
	${resp_73}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/dist/fonts/nunito-sans-v6-latin-ext_latin-800.woff2 	headers=${Req_Headers} 	expected_status=200
	&{params_74}= 	Create dictionary 	${EMPTY}=${NoKey}
	${resp_74}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/dist/favicon.ico 	params=${params_74} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	Referer=${Referer_5}
	&{params_75}= 	Create dictionary 	${EMPTY}=${NoKey}
	${resp_75}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/images/orange.png 	headers=${Req_Headers} 	params=${params_75} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	Referer=${Referer_5}
	&{params_76}= 	Create dictionary 	${EMPTY}=${NoKey}
	${resp_76}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/images/orangehrm-logo.png 	headers=${Req_Headers} 	params=${params_76} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	Accept=${Accept_4} 	If-None-Match=${If-None-Match_1} 	Referer=${Referer_5} 	Sec-Fetch-Dest=${Sec-Fetch-Dest_4} 	Sec-Fetch-Mode=${Sec-Fetch-Mode_1} 	Sec-Fetch-Site=${Sec-Fetch-Site_1}
	${resp_77}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/index.php/pim/viewPhoto/empNumber/7 	headers=${Req_Headers} 	expected_status=304
	&{Req_Headers}= 	Create dictionary 	Accept=${Accept_4} 	Referer=${Referer_5} 	Sec-Fetch-Dest=${Sec-Fetch-Dest_4} 	Sec-Fetch-Mode=${Sec-Fetch-Mode_1} 	Sec-Fetch-Site=${Sec-Fetch-Site_1}
	${resp_78}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/dist/img/user-default-400.png 	headers=${Req_Headers} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	Accept=${Accept_3} 	Cache-Control=${Cache-Control_1} 	Referer=${Referer_5} 	Sec-Fetch-Dest=${Sec-Fetch-Dest_3} 	Sec-Fetch-Mode=${Sec-Fetch-Mode_2} 	Sec-Fetch-Site=${Sec-Fetch-Site_1}
	${resp_79}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/index.php/api/v2/pim/employees 	headers=${Req_Headers} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	Accept=${Accept_5} 	Referer=${Referer_5} 	Sec-Fetch-Dest=${Sec-Fetch-Dest_3} 	Sec-Fetch-Mode=${Sec-Fetch-Mode_2} 	Sec-Fetch-Site=${Sec-Fetch-Site_1}
	${resp_80}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/index.php/api/v2/admin/users 	headers=${Req_Headers} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	Accept=${Accept_3} 	Content-Type=${Content-Type_1} 	Origin=${Origin} 	Referer=${Referer_5} 	Sec-Fetch-Dest=${Sec-Fetch-Dest_3} 	Sec-Fetch-Mode=${Sec-Fetch-Mode_2} 	Sec-Fetch-Site=${Sec-Fetch-Site_1}
	&{json_81}= 	Create Dictionary 	firstName=${firstName} 	middleName=${EMPTY} 	lastName=${lastName} 	empPicture=${None} 	employeeId=${employeeId}
	&{postdata_81}= 	Create dictionary
	${resp_81}= 	POST On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/index.php/api/v2/pim/employees 	headers=${Req_Headers} 	expected_status=200 	json=${json_81} 	data=${postdata_81}
	&{Req_Headers}= 	Create dictionary 	Referer=${Referer_5} 	Sec-Fetch-Site=${Sec-Fetch-Site_1}
	${resp_82}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/index.php/pim/viewPersonalDetails/empNumber/165 	headers=${Req_Headers} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	Referer=${Referer_6}
	&{params_83}= 	Create dictionary 	${EMPTY}=${NoKey}
	${resp_83}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/dist/css/chunk-vendors.css 	headers=${Req_Headers} 	params=${params_83} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	Referer=${Referer_6}
	&{params_84}= 	Create dictionary 	${EMPTY}=${NoKey}
	${resp_84}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/dist/css/app.css 	headers=${Req_Headers} 	params=${params_84} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	Referer=${Referer_6}
	&{params_85}= 	Create dictionary 	${EMPTY}=${NoKey}
	${resp_85}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/dist/js/chunk-vendors.js 	headers=${Req_Headers} 	params=${params_85} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	Referer=${Referer_6}
	&{params_86}= 	Create dictionary 	${EMPTY}=${NoKey}
	${resp_86}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/dist/js/app.js 	headers=${Req_Headers} 	params=${params_86} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	Accept=${Accept_3} 	Cache-Control=${Cache-Control} 	If-None-Match=${If-None-Match} 	Referer=${Referer_6} 	Sec-Fetch-Dest=${Sec-Fetch-Dest_3} 	Sec-Fetch-Mode=${Sec-Fetch-Mode_2} 	Sec-Fetch-Site=${Sec-Fetch-Site_1} 	contentType=${contentType}
	${resp_87}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/index.php/core/i18n/messages 	headers=${Req_Headers} 	expected_status=304
	&{Req_Headers}= 	Create dictionary 	Referer=${EMPTY}
	${resp_88}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/dist/fonts/bootstrap-icons.woff2 	headers=${Req_Headers} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	Referer=${EMPTY}
	${resp_89}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/dist/fonts/nunito-sans-v6-latin-ext_latin-regular.woff2 	headers=${Req_Headers} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	Referer=${EMPTY}
	${resp_90}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/dist/fonts/nunito-sans-v6-latin-ext_latin-italic.woff2 	headers=${Req_Headers} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	Referer=${EMPTY}
	${resp_91}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/dist/fonts/nunito-sans-v6-latin-ext_latin-600.woff2 	headers=${Req_Headers} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	Referer=${EMPTY}
	${resp_92}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/dist/fonts/nunito-sans-v6-latin-ext_latin-700.woff2 	headers=${Req_Headers} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	Referer=${EMPTY}
	${resp_93}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/dist/fonts/nunito-sans-v6-latin-ext_latin-800.woff2 	headers=${Req_Headers} 	expected_status=200
	&{params_94}= 	Create dictionary 	${EMPTY}=${NoKey}
	${resp_94}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/dist/favicon.ico 	params=${params_94} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	Referer=${Referer_6}
	&{params_95}= 	Create dictionary 	${EMPTY}=${NoKey}
	${resp_95}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/images/orange.png 	headers=${Req_Headers} 	params=${params_95} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	Referer=${Referer_6}
	&{params_96}= 	Create dictionary 	${EMPTY}=${NoKey}
	${resp_96}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/images/orangehrm-logo.png 	headers=${Req_Headers} 	params=${params_96} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	Accept=${Accept_4} 	If-None-Match=${If-None-Match_1} 	Referer=${Referer_6} 	Sec-Fetch-Dest=${Sec-Fetch-Dest_4} 	Sec-Fetch-Mode=${Sec-Fetch-Mode_1} 	Sec-Fetch-Site=${Sec-Fetch-Site_1}
	${resp_97}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/index.php/pim/viewPhoto/empNumber/7 	headers=${Req_Headers} 	expected_status=304
	&{Req_Headers}= 	Create dictionary 	Accept=${Accept_4} 	Referer=${Referer_6} 	Sec-Fetch-Dest=${Sec-Fetch-Dest_4} 	Sec-Fetch-Mode=${Sec-Fetch-Mode_1} 	Sec-Fetch-Site=${Sec-Fetch-Site_1}
	${resp_98}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/index.php/pim/viewPhoto/empNumber/165 	headers=${Req_Headers} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	Accept=${Accept_3} 	Cache-Control=${Cache-Control_1} 	Referer=${Referer_6} 	Sec-Fetch-Dest=${Sec-Fetch-Dest_3} 	Sec-Fetch-Mode=${Sec-Fetch-Mode_2} 	Sec-Fetch-Site=${Sec-Fetch-Site_1}
	${resp_99}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/index.php/api/v2/pim/employees/165/personal-details 	headers=${Req_Headers} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	Accept=${Accept_5} 	Referer=${Referer_6} 	Sec-Fetch-Dest=${Sec-Fetch-Dest_3} 	Sec-Fetch-Mode=${Sec-Fetch-Mode_2} 	Sec-Fetch-Site=${Sec-Fetch-Site_1}
	${resp_100}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/index.php/api/v2/pim/employees/165 	headers=${Req_Headers} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	Accept=${Accept_5} 	Referer=${Referer_6} 	Sec-Fetch-Dest=${Sec-Fetch-Dest_3} 	Sec-Fetch-Mode=${Sec-Fetch-Mode_2} 	Sec-Fetch-Site=${Sec-Fetch-Site_1}
	&{params_101}= 	Create dictionary 	model=${model_1}
	${resp_101}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/index.php/api/v2/leave/workweek 	headers=${Req_Headers} 	params=${params_101} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	Accept=${Accept_5} 	Referer=${Referer_6} 	Sec-Fetch-Dest=${Sec-Fetch-Dest_3} 	Sec-Fetch-Mode=${Sec-Fetch-Mode_2} 	Sec-Fetch-Site=${Sec-Fetch-Site_1}
	&{params_102}= 	Create dictionary 	model=${model_1}
	${resp_102}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/index.php/api/v2/leave/workweek 	headers=${Req_Headers} 	params=${params_102} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	Accept=${Accept_3} 	Cache-Control=${Cache-Control_1} 	Referer=${Referer_6} 	Sec-Fetch-Dest=${Sec-Fetch-Dest_3} 	Sec-Fetch-Mode=${Sec-Fetch-Mode_2} 	Sec-Fetch-Site=${Sec-Fetch-Site_1}
	&{params_103}= 	Create dictionary 	screen=${screen}
	${resp_103}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/index.php/api/v2/pim/employees/165/custom-fields 	headers=${Req_Headers} 	params=${params_103} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	Accept=${Accept_3} 	Cache-Control=${Cache-Control_1} 	Referer=${Referer_6} 	Sec-Fetch-Dest=${Sec-Fetch-Dest_3} 	Sec-Fetch-Mode=${Sec-Fetch-Mode_2} 	Sec-Fetch-Site=${Sec-Fetch-Site_1}
	&{params_104}= 	Create dictionary 	limit=${limit_1} 	offset=${offset}
	${resp_104}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/index.php/api/v2/pim/employees/165/screen/personal/attachments 	headers=${Req_Headers} 	params=${params_104} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	Accept=${Accept_5} 	Referer=${Referer_6} 	Sec-Fetch-Dest=${Sec-Fetch-Dest_3} 	Sec-Fetch-Mode=${Sec-Fetch-Mode_2} 	Sec-Fetch-Site=${Sec-Fetch-Site_1}
	&{params_105}= 	Create dictionary 	fromDate=${fromDate} 	toDate=${toDate}
	${resp_105}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/index.php/api/v2/leave/holidays 	headers=${Req_Headers} 	params=${params_105} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	Accept=${Accept_5} 	Referer=${Referer_6} 	Sec-Fetch-Dest=${Sec-Fetch-Dest_3} 	Sec-Fetch-Mode=${Sec-Fetch-Mode_2} 	Sec-Fetch-Site=${Sec-Fetch-Site_1}
	&{params_106}= 	Create dictionary 	fromDate=${fromDate} 	toDate=${toDate}
	${resp_106}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/index.php/api/v2/leave/holidays 	headers=${Req_Headers} 	params=${params_106} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	Accept=${Accept_5} 	Referer=${Referer_6} 	Sec-Fetch-Dest=${Sec-Fetch-Dest_3} 	Sec-Fetch-Mode=${Sec-Fetch-Mode_2} 	Sec-Fetch-Site=${Sec-Fetch-Site_1}
	${resp_107}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/index.php/api/v2/pim/employees 	headers=${Req_Headers} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	Referer=${EMPTY}
	${resp_108}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/dist/fonts/bootstrap-icons.woff2 	headers=${Req_Headers} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	Referer=${EMPTY}
	${resp_109}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/dist/fonts/nunito-sans-v6-latin-ext_latin-regular.woff2 	headers=${Req_Headers} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	Referer=${EMPTY}
	${resp_110}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/dist/fonts/nunito-sans-v6-latin-ext_latin-italic.woff2 	headers=${Req_Headers} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	Referer=${EMPTY}
	${resp_111}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/dist/fonts/nunito-sans-v6-latin-ext_latin-600.woff2 	headers=${Req_Headers} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	Referer=${EMPTY}
	${resp_112}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/dist/fonts/nunito-sans-v6-latin-ext_latin-700.woff2 	headers=${Req_Headers} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	Referer=${EMPTY}
	${resp_113}= 	GET On Session 	sess_opensource-demo_orangehrmlive_com 	url=/web/dist/fonts/nunito-sans-v6-latin-ext_latin-800.woff2 	headers=${Req_Headers} 	expected_status=200


