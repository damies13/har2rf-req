*** Settings ***
Library	RequestsLibrary
Library	String

*** Variables ***
${accept} 	text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
${accept-language} 	en-GB,en;q=0.9
${sec-ch-ua-mobile} 	?0
${sec-ch-ua-platform} 	"Linux"
${sec-fetch-dest} 	document
${sec-fetch-mode} 	navigate
${sec-fetch-site} 	none
${sec-fetch-user} 	?1
${upgrade-insecure-requests} 	1
${sec-fetch-dest_1} 	script
${sec-fetch-mode_1} 	no-cors
${sec-fetch-site_1} 	same-origin
${accept_1} 	text/css,*/*;q=0.1
${sec-fetch-dest_2} 	style
${sec-fetch-dest_3} 	empty
${x-requested-with} 	XMLHttpRequest
${content-type} 	application/json
${client} 	76d9d2b5-992c-4e46-b1c2-da1ef9676c40

*** Test Cases ***
tryton_1680844256
	Create Session    sess_demo_tryton_org 	https://demo.tryton.org 	disable_warnings=1
	tryton_1680844256 page@2f780477cb30c000b346dbe753276485


*** Keywords ***
Get Substring LRB
	[Documentation] 	Get Substring using Left and Right Boundaries
	[Arguments] 	${string} 	${LeftB} 	${RightB}
	${left}= 	Fetch From Right 	${string} 	${LeftB}
	${match}= 	Fetch From Left 	${left} 	${RightB}
	[Return] 	${match}

tryton_1680844256 page@2f780477cb30c000b346dbe753276485
	[Documentation] 	tryton_1680844256	|	tryton_1680844256 page@2f780477cb30c000b346dbe753276485	|	Tryton
	&{Headers}= 	Create dictionary 	accept=${accept} 	accept-language=${accept-language} 	sec-ch-ua="Not A(Brand";v="24",${EMPTY} "Chromium";v="110" 	sec-ch-ua-mobile=${sec-ch-ua-mobile} 	sec-ch-ua-platform=${sec-ch-ua-platform} 	sec-fetch-dest=${sec-fetch-dest} 	sec-fetch-mode=${sec-fetch-mode} 	sec-fetch-site=${sec-fetch-site} 	sec-fetch-user=${sec-fetch-user} 	upgrade-insecure-requests=${upgrade-insecure-requests} 	user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML,${EMPTY} like Gecko) Chrome/110.0.0.0 Safari/537.36
	&{Cookies}= 	Create dictionary
	Update Session	sess_demo_tryton_org	${Headers}	${Cookies}
	${resp_0}= 	GET On Session 	sess_demo_tryton_org 	url=/ 	expected_status=307 	allow_redirects=${False}
	Set Global Variable 	${location}	${resp_0.headers["location"]}
	${path}= 	Get Substring 	${location} 	0 	-9
	${resp_1}= 	GET On Session 	sess_demo_tryton_org 	url=${path} 	expected_status=200
	${path_2_pathsuf_path_path_1}= 	evaluate 	re.findall("""href=['"]([^'"\?]*)""", """${resp_1.text}""")[0] 	re
	${path_2_pathsuf_path_path}= 	evaluate 	re.findall("""src=['"]([^'"\?]*)""", """${resp_1.text}""")[0] 	re
	${accept_sub}= 	Get Substring LRB 	${accept} 	text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng, 	;q=0.8,application/signed-exchange;v=b3;q=0.7
	&{Req_Headers}= 	Create dictionary 	accept=${accept_sub} 	referer=${path} 	sec-fetch-dest=${sec-fetch-dest_1} 	sec-fetch-mode=${sec-fetch-mode_1} 	sec-fetch-site=${sec-fetch-site_1}
	${location_sub}= 	Fetch From Left 	${location} 	://demo6.6.tryton.org/#demo6.6/
	Set Global Variable 	${location_1}	${resp_0.headers["location"]}
	${path_2_pathpre_pathpre_pathpre_path_pathpre}= 	Get Substring 	${location_1} 	6 	-10
	${resp_2}= 	GET On Session 	sess_demo_tryton_org 	url=${location_sub}:${path_2_pathpre_pathpre_pathpre_path_pathpre}/bower_components/jquery/dist/jquery.min.js${path_2_pathpre_pathpre_pathpre_path_pathpre}/${path_2_pathsuf_path_path} 	headers=${Req_Headers} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	accept=${accept_sub} 	referer=${path} 	sec-fetch-dest=${sec-fetch-dest_1} 	sec-fetch-mode=${sec-fetch-mode_1} 	sec-fetch-site=${sec-fetch-site_1}
	${path_2_pathsuf_path_path_sub}= 	Get Substring LRB 	${path_2_pathsuf_path_path} 	bower_components/jquery 	/jquery.min.js
	${path_2_pathsuf_path_path_sub_1}= 	Fetch From Right 	${path_2_pathsuf_path_path} 	bower_components/jquery/dist/jquery.min.
	${resp_3}= 	GET On Session 	sess_demo_tryton_org 	url=${location_sub}://demo6.6.tryton.org/bower_components/bootstrap${path_2_pathsuf_path_path_sub}//demo6.6.tryton.org/bower_components/bootstrap${path_2_pathsuf_path_path_sub}${EMPTY}/${path_2_pathsuf_path_path_sub_1}//demo6.6.tryton.org/bower_components/bootstrap${path_2_pathsuf_path_path_sub}//demo6.6.tryton.org/bower_components/bootstrap${path_2_pathsuf_path_path_sub}${EMPTY}/${path_2_pathsuf_path_path_sub_1}${EMPTY}/bootstrap.min.js 	headers=${Req_Headers} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	accept=${accept_sub} 	referer=${path} 	sec-fetch-dest=${sec-fetch-dest_1} 	sec-fetch-mode=${sec-fetch-mode_1} 	sec-fetch-site=${sec-fetch-site_1}
	${path_2_pathsuf_path_path_sub_2}= 	Fetch From Left 	${path_2_pathsuf_path_path} 	/jquery/dist/jquery.min.js
	${path_2_pathsuf_path_path_sub_3}= 	Get Substring LRB 	${path_2_pathsuf_path_path} 	bower_components/jquery/dist/jquery. 	.js
	${resp_4}= 	GET On Session 	sess_demo_tryton_org 	url=${location_sub}:${path_2_pathpre_pathpre_pathpre_path_pathpre}/bower_components/moment${path_2_pathpre_pathpre_pathpre_path_pathpre}/${path_2_pathsuf_path_path_sub_2}/moment/${path_2_pathsuf_path_path_sub_3}${path_2_pathpre_pathpre_pathpre_path_pathpre}/bower_components/moment${path_2_pathpre_pathpre_pathpre_path_pathpre}/${path_2_pathsuf_path_path_sub_2}/moment/${path_2_pathsuf_path_path_sub_3}${EMPTY}/moment.min.js 	headers=${Req_Headers} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	accept=${accept_sub} 	referer=${path} 	sec-fetch-dest=${sec-fetch-dest_1} 	sec-fetch-mode=${sec-fetch-mode_1} 	sec-fetch-site=${sec-fetch-site_1}
	${resp_5}= 	GET On Session 	sess_demo_tryton_org 	url=${location_sub}:${path_2_pathpre_pathpre_pathpre_path_pathpre}/bower_components/moment${path_2_pathpre_pathpre_pathpre_path_pathpre}/${path_2_pathsuf_path_path_sub_2}/moment/${path_2_pathsuf_path_path_sub_3}${path_2_pathpre_pathpre_pathpre_path_pathpre}/bower_components/moment${path_2_pathpre_pathpre_pathpre_path_pathpre}/${path_2_pathsuf_path_path_sub_2}/moment/${path_2_pathsuf_path_path_sub_3}${EMPTY}/locales.min.js 	headers=${Req_Headers} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	accept=${accept_sub} 	referer=${path} 	sec-fetch-dest=${sec-fetch-dest_1} 	sec-fetch-mode=${sec-fetch-mode_1} 	sec-fetch-site=${sec-fetch-site_1}
	${resp_6}= 	GET On Session 	sess_demo_tryton_org 	url=${location_sub}://demo6.6.tryton.org/bower_components/gettext.js${path_2_pathsuf_path_path_sub}//demo6.6.tryton.org/bower_components/gettext.js${path_2_pathsuf_path_path_sub}${EMPTY}/gettext.min.js 	headers=${Req_Headers} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	accept=${accept_sub} 	referer=${path} 	sec-fetch-dest=${sec-fetch-dest_1} 	sec-fetch-mode=${sec-fetch-mode_1} 	sec-fetch-site=${sec-fetch-site_1}
	${resp_7}= 	GET On Session 	sess_demo_tryton_org 	url=${location_sub}:${path_2_pathpre_pathpre_pathpre_path_pathpre}/bower_components/d3${path_2_pathpre_pathpre_pathpre_path_pathpre}/${path_2_pathsuf_path_path_sub_2}/d3/d3.min.js 	headers=${Req_Headers} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	accept=${accept_sub} 	referer=${path} 	sec-fetch-dest=${sec-fetch-dest_1} 	sec-fetch-mode=${sec-fetch-mode_1} 	sec-fetch-site=${sec-fetch-site_1}
	${resp_8}= 	GET On Session 	sess_demo_tryton_org 	url=${location_sub}:${path_2_pathpre_pathpre_pathpre_path_pathpre}/bower_components/c3${path_2_pathpre_pathpre_pathpre_path_pathpre}/${path_2_pathsuf_path_path_sub_2}/c3/c3.min.js 	headers=${Req_Headers} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	accept=${accept_sub} 	referer=${path} 	sec-fetch-dest=${sec-fetch-dest_1} 	sec-fetch-mode=${sec-fetch-mode_1} 	sec-fetch-site=${sec-fetch-site_1}
	${resp_9}= 	GET On Session 	sess_demo_tryton_org 	url=${location_sub}:${path_2_pathpre_pathpre_pathpre_path_pathpre}/bower_components/papaparse${path_2_pathpre_pathpre_pathpre_path_pathpre}/${path_2_pathsuf_path_path_sub_2}/papaparse/papaparse.min.js 	headers=${Req_Headers} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	accept=${accept_sub} 	referer=${path} 	sec-fetch-dest=${sec-fetch-dest_1} 	sec-fetch-mode=${sec-fetch-mode_1} 	sec-fetch-site=${sec-fetch-site_1}
	${resp_10}= 	GET On Session 	sess_demo_tryton_org 	url=${location_sub}://demo6.6.tryton.org/bower_components/fullcalendar${path_2_pathsuf_path_path_sub}//demo6.6.tryton.org/bower_components/fullcalendar${path_2_pathsuf_path_path_sub}${EMPTY}/fullcalendar.min.js 	headers=${Req_Headers} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	accept=${accept_sub} 	referer=${path} 	sec-fetch-dest=${sec-fetch-dest_1} 	sec-fetch-mode=${sec-fetch-mode_1} 	sec-fetch-site=${sec-fetch-site_1}
	${resp_11}= 	GET On Session 	sess_demo_tryton_org 	url=${location_sub}://demo6.6.tryton.org/bower_components/fullcalendar${path_2_pathsuf_path_path_sub}//demo6.6.tryton.org/bower_components/fullcalendar${path_2_pathsuf_path_path_sub}${EMPTY}/locale-all.js 	headers=${Req_Headers} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	accept=${accept_sub} 	referer=${path} 	sec-fetch-dest=${sec-fetch-dest_1} 	sec-fetch-mode=${sec-fetch-mode_1} 	sec-fetch-site=${sec-fetch-site_1}
	${resp_12}= 	GET On Session 	sess_demo_tryton_org 	url=${location_sub}:${path_2_pathpre_pathpre_pathpre_path_pathpre}/bower_components/mousetrap${path_2_pathpre_pathpre_pathpre_path_pathpre}/${path_2_pathsuf_path_path_sub_2}/mousetrap/mousetrap.min.js 	headers=${Req_Headers} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	accept=${accept_sub} 	referer=${path} 	sec-fetch-dest=${sec-fetch-dest_1} 	sec-fetch-mode=${sec-fetch-mode_1} 	sec-fetch-site=${sec-fetch-site_1}
	${resp_13}= 	GET On Session 	sess_demo_tryton_org 	url=${location_sub}:${path_2_pathpre_pathpre_pathpre_path_pathpre}/bower_components/Sortable${path_2_pathpre_pathpre_pathpre_path_pathpre}/${path_2_pathsuf_path_path_sub_2}/Sortable/Sortable.min.js 	headers=${Req_Headers} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	accept=${accept_1} 	referer=${path} 	sec-fetch-dest=${sec-fetch-dest_2} 	sec-fetch-mode=${sec-fetch-mode_1} 	sec-fetch-site=${sec-fetch-site_1}
	${resp_14}= 	GET On Session 	sess_demo_tryton_org 	url=${location_sub}:${path_2_pathpre_pathpre_pathpre_path_pathpre}/bower_components/c3${path_2_pathpre_pathpre_pathpre_path_pathpre}/${path_2_pathsuf_path_path_sub_2}/c3/c3.min.css 	headers=${Req_Headers} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	accept=${accept_1} 	referer=${path} 	sec-fetch-dest=${sec-fetch-dest_2} 	sec-fetch-mode=${sec-fetch-mode_1} 	sec-fetch-site=${sec-fetch-site_1}
	${resp_15}= 	GET On Session 	sess_demo_tryton_org 	url=${location_sub}://demo6.6.tryton.org/bower_components/fullcalendar${path_2_pathsuf_path_path_sub}//demo6.6.tryton.org/bower_components/fullcalendar${path_2_pathsuf_path_path_sub}${EMPTY}/fullcalendar.min.css 	headers=${Req_Headers} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	accept=${accept_sub} 	referer=${path} 	sec-fetch-dest=${sec-fetch-dest_1} 	sec-fetch-mode=${sec-fetch-mode_1} 	sec-fetch-site=${sec-fetch-site_1}
	${resp_16}= 	GET On Session 	sess_demo_tryton_org 	url=${location_sub}:${path_2_pathpre_pathpre_pathpre_path_pathpre}${path_2_pathsuf_path_path_sub}/tryton-sao.min.js 	headers=${Req_Headers} 	expected_status=200
	${method_4}= 	Get Substring LRB 	${resp_16.text} 	tItem("sao_device_cookies")),e=t&&this.database in t?t[this.database][this.login]:null,e=Sao.rpc({method:" 	",params:[e,{}]},this);e.done(e=>{t=(t=JSON.parse(localStorage.getItem("sao_device_cookies")))||{},t
	Set Global Variable 	${method_4}
	${method_3}= 	Get Substring LRB 	${resp_16.text} 	ase]&&(o=n[this.database][this.login]);return new Sao.Login(function(e){return e.device_cookie=o,{method:" 	",params:[i,e,Sao.i18n.getlang()]}},this).run().then(e=>{this.login=i,this.user_id=e[0],this.session
	Set Global Variable 	${method_3}
	${method_2}= 	Get Substring LRB 	${resp_16.text} 	on.processing.show();return jQuery.ajax({contentType:"application/json",data:JSON.stringify({id:0,method:" 	",params:[]}),dataType:"json",url:"/",type:"post",complete:[function(){Sao.common.processing.hide(e)
	Set Global Variable 	${method_2}
	${regx_match}= 	evaluate 	re.search("on\\.processing\\.show\\(\\);return\\ jQuery\\.ajax\\(\\{contentType:\\"application/json\\",data:JSON\\.stringify\\(\\{id:0,method:\\"(.*?)\\",params:\\[\\]\\}\\),dataType:\\"json\\",url:\\"/\\",type:\\"post\\",complete:\\[function\\(\\)\\{Sao\\.common\\.processing\\.hide\\(e\\)", """${resp_16.text}""").group(0) 	re
	${method_1}= 	Get Substring LRB 	${regx_match} 	on.processing.show();return jQuery.ajax({contentType:"application/json",data:JSON.stringify({id:0,method:" 	",params:[]}),dataType:"json",url:"/",type:"post",complete:[function(){Sao.common.processing.hide(e)
	Set Global Variable 	${method_1}
	${regx_match}= 	evaluate 	re.search("on\\.processing\\.show\\(\\);return\\ jQuery\\.ajax\\(\\{contentType:\\"application/json\\",data:JSON\\.stringify\\(\\{id:0,method:\\"(.*?)\\",params:\\[\\]\\}\\),dataType:\\"json\\",url:\\"/\\",type:\\"post\\",complete:\\[function\\(\\)\\{Sao\\.common\\.processing\\.hide\\(e\\)", """${resp_16.text}""").group(0) 	re
	${method}= 	Get Substring LRB 	${regx_match} 	on.processing.show();return jQuery.ajax({contentType:"application/json",data:JSON.stringify({id:0,method:" 	",params:[]}),dataType:"json",url:"/",type:"post",complete:[function(){Sao.common.processing.hide(e)
	Set Global Variable 	${method}
	&{Req_Headers}= 	Create dictionary 	accept=${accept_1} 	referer=${path} 	sec-fetch-dest=${sec-fetch-dest_2} 	sec-fetch-mode=${sec-fetch-mode_1} 	sec-fetch-site=${sec-fetch-site_1}
	${resp_17}= 	GET On Session 	sess_demo_tryton_org 	url=${location_sub}:${path_2_pathpre_pathpre_pathpre_path_pathpre}${path_2_pathsuf_path_path_sub}/tryton-sao.min.css 	headers=${Req_Headers} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	accept=${accept_sub} 	referer=${path} 	sec-fetch-dest=${sec-fetch-dest_1} 	sec-fetch-mode=${sec-fetch-mode_1} 	sec-fetch-site=${sec-fetch-site_1}
	${resp_18}= 	GET On Session 	sess_demo_tryton_org 	url=${location_sub}:${path_2_pathpre_pathpre_pathpre_path_pathpre}/custom.js 	headers=${Req_Headers} 	expected_status=405
	&{Req_Headers}= 	Create dictionary 	accept=${accept_1} 	referer=${path} 	sec-fetch-dest=${sec-fetch-dest_2} 	sec-fetch-mode=${sec-fetch-mode_1} 	sec-fetch-site=${sec-fetch-site_1}
	${resp_19}= 	GET On Session 	sess_demo_tryton_org 	url=${location_sub}:${path_2_pathpre_pathpre_pathpre_path_pathpre}/custom.css 	headers=${Req_Headers} 	expected_status=405
	${accept_sub_1}= 	Get Substring LRB 	${accept} 	text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng, 	q=0.8,application/signed-exchange;v=b3;q=0.7
	${sec-fetch-mode_1_sub}= 	Fetch From Right 	${sec-fetch-mode_1} 	no-
	&{Req_Headers}= 	Create dictionary 	accept=application/json,${EMPTY} text/javascript,${EMPTY} ${accept_sub_1} q=0.01 	referer=${path} 	sec-fetch-dest=${sec-fetch-dest_3} 	sec-fetch-mode=${sec-fetch-mode_1_sub} 	sec-fetch-site=${sec-fetch-site_1} 	x-requested-with=${x-requested-with}
	${resp_20}= 	GET On Session 	sess_demo_tryton_org 	url=${location_sub}:${path_2_pathpre_pathpre_pathpre_path_pathpre}/locale/en_GB.json 	headers=${Req_Headers} 	expected_status=405
	${accept_sub_2}= 	Get Substring LRB 	${accept} 	text/html,application/xhtml+xml,application/xml;q=0.9, 	,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
	${accept_sub_3}= 	Get Substring LRB 	${accept} 	text/html,application/xhtml+xml,application/xml;q=0.9,image/avif, 	,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
	${accept_sub_4}= 	Get Substring LRB 	${accept} 	text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp, 	,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
	${accept_sub_5}= 	Get Substring LRB 	${accept} 	text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng, 	,application/signed-exchange;v=b3;q=0.7
	${accept_sub_6}= 	Get Substring LRB 	${accept} 	text/html,application/xhtml+xml,application/xml;q=0.9, 	/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
	&{Req_Headers}= 	Create dictionary 	accept=${accept_sub_2},${accept_sub_3},${accept_sub_4},image/svg+xml,image/*,${accept_sub_5} 	referer=${path} 	sec-fetch-dest=${accept_sub_6} 	sec-fetch-mode=${sec-fetch-mode_1} 	sec-fetch-site=${sec-fetch-site_1}
	${resp_21}= 	GET On Session 	sess_demo_tryton_org 	url=${location_sub}:${path_2_pathpre_pathpre_pathpre_path_pathpre}/images/tryton-icon.png${path_2_pathpre_pathpre_pathpre_path_pathpre}/${path_2_pathsuf_path_path_1} 	headers=${Req_Headers} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	accept=application/json,${EMPTY} text/javascript,${EMPTY} ${accept_sub_1} q=0.01 	referer=${path} 	sec-fetch-dest=${sec-fetch-dest_3} 	sec-fetch-mode=${sec-fetch-mode_1_sub} 	sec-fetch-site=${sec-fetch-site_1} 	x-requested-with=${x-requested-with}
	${resp_22}= 	GET On Session 	sess_demo_tryton_org 	url=${location_sub}:${path_2_pathpre_pathpre_pathpre_path_pathpre}/locale/en.json 	headers=${Req_Headers} 	expected_status=405
	Set Global Variable 	${location_2}	${resp_0.headers["location"]}
	${origin}= 	Get Substring 	${location_2} 	0 	-10
	&{Req_Headers}= 	Create dictionary 	accept=application/json,${EMPTY} text/javascript,${EMPTY} ${accept_sub_1} q=0.01 	content-type=${content-type} 	origin=${origin} 	referer=${path} 	sec-fetch-dest=${sec-fetch-dest_3} 	sec-fetch-mode=${sec-fetch-mode_1_sub} 	sec-fetch-site=${sec-fetch-site_1} 	x-requested-with=${x-requested-with}
	${accept_sub_7}= 	Get Substring LRB 	${accept} 	text/html,application/xhtml+xml,application/xml;q= 	.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
	@{json_23_params}= 	Create List
	&{json_23}= 	Create Dictionary 	id=${accept_sub_7} 	method=${method} 	params=${json_23_params}
	&{postdata_23}= 	Create dictionary
	${resp_23}= 	POST On Session 	sess_demo_tryton_org 	url=${path} 	headers=${Req_Headers} 	expected_status=200 	json=${json_23} 	data=${postdata_23}
	&{Req_Headers}= 	Create dictionary 	accept=${content-type},${EMPTY} text/javascript,${EMPTY} ${accept_sub_1} q=0.01 	content-type=${content-type} 	origin=${origin} 	referer=${path} 	sec-fetch-dest=${sec-fetch-dest_3} 	sec-fetch-mode=${sec-fetch-mode_1_sub} 	sec-fetch-site=${sec-fetch-site_1} 	x-requested-with=${x-requested-with}
	${accept_sub_8}= 	Get Substring LRB 	${accept} 	text/html,application/xhtml+xml,application/xml;q= 	.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
	@{json_24_params}= 	Create List
	&{json_24}= 	Create Dictionary 	id=${accept_sub_8} 	method=${method_1} 	params=${json_24_params}
	&{postdata_24}= 	Create dictionary
	${resp_24}= 	POST On Session 	sess_demo_tryton_org 	url=${path} 	headers=${Req_Headers} 	expected_status=200 	json=${json_24} 	data=${postdata_24}
	&{Req_Headers}= 	Create dictionary 	accept=${content-type},${EMPTY} text/javascript,${EMPTY} ${accept_sub_1} q=0.01 	content-type=${content-type} 	origin=${origin} 	referer=${path} 	sec-fetch-dest=${sec-fetch-dest_3} 	sec-fetch-mode=${sec-fetch-mode_1_sub} 	sec-fetch-site=${sec-fetch-site_1} 	x-requested-with=${x-requested-with}
	${accept_sub_9}= 	Get Substring LRB 	${accept} 	text/html,application/xhtml+xml,application/xml;q= 	.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
	@{json_25_params}= 	Create List
	&{json_25}= 	Create Dictionary 	id=${accept_sub_9} 	method=${method_2} 	params=${json_25_params}
	&{postdata_25}= 	Create dictionary
	${resp_25}= 	POST On Session 	sess_demo_tryton_org 	url=${path} 	headers=${Req_Headers} 	expected_status=200 	json=${json_25} 	data=${postdata_25}
	&{Req_Headers}= 	Create dictionary 	accept=${content-type},${EMPTY} text/javascript,${EMPTY} ${accept_sub_1} q=0.01 	content-type=${content-type} 	origin=${origin} 	referer=${path} 	sec-fetch-dest=${sec-fetch-dest_3} 	sec-fetch-mode=${sec-fetch-mode_1_sub} 	sec-fetch-site=${sec-fetch-site_1} 	x-requested-with=${x-requested-with}
	${location_sub_1}= 	Get Substring LRB 	${location} 	https:// 	6.6.tryton.org/#demo6.6/
	${accept-language_sub}= 	Fetch From Left 	${accept-language} 	-GB,en;q=0.9
	${accept_sub_10}= 	Get Substring LRB 	${accept} 	text/html,application/xhtml+xml,application/xml;q= 	.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
	&{json_26_params_1}= 	Create Dictionary 	device_cookie=${None}
	@{json_26_params}= 	Create List 	${location_sub_1} 	${json_26_params_1} 	${accept-language_sub}
	&{json_26}= 	Create Dictionary 	method=${method_3} 	params=${json_26_params} 	id=${accept_sub_10}
	&{postdata_26}= 	Create dictionary
	${accept_sub_11}= 	Get Substring LRB 	${accept} 	text 	html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
	${resp_26}= 	POST On Session 	sess_demo_tryton_org 	url=${location_sub}://demo6.6.tryton.org/demo6.6${accept_sub_11}//demo6.6.tryton.org/demo6.6${accept_sub_11}${EMPTY} 	headers=${Req_Headers} 	expected_status=200 	json=${json_26} 	data=${postdata_26}
	&{Req_Headers}= 	Create dictionary 	accept=${content-type},${EMPTY} text/javascript,${EMPTY} ${accept_sub_1} q=0.01 	authorization=Session ${location_sub_1}:2:8808b94b84e817fe8d342585f1076bcbf42bf4b9f26febb24a8b046f885d7143 	content-type=${content-type} 	origin=${origin} 	referer=${path} 	sec-fetch-dest=${sec-fetch-dest_3} 	sec-fetch-mode=${sec-fetch-mode_1_sub} 	sec-fetch-site=${sec-fetch-site_1} 	x-requested-with=${x-requested-with}
	${accept_sub_12}= 	Get Substring LRB 	${accept} 	text/html,application/xhtml+xml,application/xml;q= 	.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
	&{json_27_params_1}= 	Create Dictionary 	client=${client}
	@{json_27_params}= 	Create List 	 	${json_27_params_1}
	&{json_27}= 	Create Dictionary 	id=${accept_sub_12} 	method=${method_4} 	params=${json_27_params}
	&{postdata_27}= 	Create dictionary
	${accept_sub_13}= 	Get Substring LRB 	${accept} 	text 	html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
	${resp_27}= 	POST On Session 	sess_demo_tryton_org 	url=${location_sub}://demo6.6.tryton.org/demo6.6${accept_sub_13}//demo6.6.tryton.org/demo6.6${accept_sub_13}${EMPTY} 	headers=${Req_Headers} 	expected_status=200 	json=${json_27} 	data=${postdata_27}


