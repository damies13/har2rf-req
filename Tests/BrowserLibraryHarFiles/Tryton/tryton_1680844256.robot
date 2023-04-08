*** Settings ***
Library	RequestsLibrary
Library	String

*** Variables ***
${accept} 	text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
${accept-language} 	en-GB,en;q=0.9
${sec-ch-ua} 	"Not A(Brand";v="24", "Chromium";v="110"
${sec-ch-ua-mobile} 	?0
${sec-ch-ua-platform} 	"Linux"
${sec-fetch-dest} 	document
${sec-fetch-mode} 	navigate
${sec-fetch-site} 	none
${sec-fetch-user} 	?1
${user-agent} 	Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36
${sec-fetch-dest_1} 	script
${sec-fetch-mode_1} 	no-cors
${sec-fetch-site_1} 	same-origin
${path_path} 	/bower_components/jquery/dist/jquery.min.js
${path_path_1} 	/bower_components/bootstrap/dist/js/bootstrap.min.js
${path_path_2} 	/bower_components/moment/min/moment.min.js
${path_path_3} 	/bower_components/gettext.js/dist/gettext.min.js
${path_path_4} 	/bower_components/d3/d3.min.js
${path_path_5} 	/bower_components/c3/c3.min.js
${path_path_6} 	/bower_components/papaparse/papaparse.min.js
${path_path_7} 	/bower_components/fullcalendar/dist/fullcalendar.min.js
${path_path_8} 	/bower_components/mousetrap/mousetrap.min.js
${path_path_9} 	/bower_components/Sortable/Sortable.min.js
${accept_1} 	text/css,*/*;q=0.1
${sec-fetch-dest_2} 	style
${path_path_10} 	/custom.js
${path_path_11} 	/custom.css
${accept_2} 	application/json, text/javascript, */*; q=0.01
${sec-fetch-dest_3} 	empty
${x-requested-with} 	XMLHttpRequest
${path_path_12} 	/locale/en_GB.json
${accept_3} 	image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8
${path_path_13} 	/images/tryton-icon.png
${authorization} 	Session ZGVtbzoyOjg4MDhiOTRiODRlODE3ZmU4ZDM0MjU4NWYxMDc2YmNiZjQyYmY0YjlmMjZmZWJiMjRhOGIwNDZmODg1ZDcxNDM=
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
	${sec-ch-ua_sub}= 	Get Substring LRB 	${sec-ch-ua} 	"Not A(Brand";v="24", "Chromium";v=" 	10"
	&{Headers}= 	Create dictionary 	accept=${accept} 	accept-language=${accept-language} 	sec-ch-ua=${sec-ch-ua} 	sec-ch-ua-mobile=${sec-ch-ua-mobile} 	sec-ch-ua-platform=${sec-ch-ua-platform} 	sec-fetch-dest=${sec-fetch-dest} 	sec-fetch-mode=${sec-fetch-mode} 	sec-fetch-site=${sec-fetch-site} 	sec-fetch-user=${sec-fetch-user} 	upgrade-insecure-requests=${sec-ch-ua_sub} 	user-agent=${user-agent}
	&{Cookies}= 	Create dictionary
	Update Session	sess_demo_tryton_org	${Headers}	${Cookies}
	${sec-ch-ua_sub_1}= 	Get Substring LRB 	${sec-ch-ua} 	"Not A(Brand";v="24", "Chromium";v=" 	10"
	&{Req_Headers}= 	Create dictionary 	upgrade-insecure-requests=${sec-ch-ua_sub_1}
	${resp_0}= 	GET On Session 	sess_demo_tryton_org 	url=/ 	headers=${Req_Headers} 	expected_status=307 	allow_redirects=${False}
	${sec-ch-ua_sub_2}= 	Get Substring LRB 	${sec-ch-ua} 	"Not A(Brand";v="24", "Chromium";v=" 	10"
	&{Req_Headers}= 	Create dictionary 	upgrade-insecure-requests=${sec-ch-ua_sub_2}
	Set Global Variable 	${location}	${resp_0.headers["location"]}
	${path}= 	Get Substring 	${location} 	0 	-9
	${resp_1}= 	GET On Session 	sess_demo_tryton_org 	url=${path} 	headers=${Req_Headers} 	expected_status=200
	${accept_sub}= 	Get Substring LRB 	${accept} 	text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng, 	;q=0.8,application/signed-exchange;v=b3;q=0.7
	&{Req_Headers}= 	Create dictionary 	accept=${accept_sub} 	referer=${path} 	sec-fetch-dest=${sec-fetch-dest_1} 	sec-fetch-mode=${sec-fetch-mode_1} 	sec-fetch-site=${sec-fetch-site_1}
	${location_sub}= 	Fetch From Left 	${location} 	://demo6.6.tryton.org/#demo6.6/
	${location_sub_1}= 	Get Substring LRB 	${location} 	https:// 	/#demo6.6/
	${resp_2}= 	GET On Session 	sess_demo_tryton_org 	url=${location_sub}://${location_sub_1}${path_path} 	headers=${Req_Headers} 	expected_status=200
	${accept_sub_1}= 	Get Substring LRB 	${accept} 	text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng, 	;q=0.8,application/signed-exchange;v=b3;q=0.7
	&{Req_Headers}= 	Create dictionary 	accept=${accept_sub_1} 	referer=${path} 	sec-fetch-dest=${sec-fetch-dest_1} 	sec-fetch-mode=${sec-fetch-mode_1} 	sec-fetch-site=${sec-fetch-site_1}
	${location_sub_2}= 	Fetch From Left 	${location} 	://demo6.6.tryton.org/#demo6.6/
	${resp_3}= 	GET On Session 	sess_demo_tryton_org 	url=${location_sub_2}://${location_sub_1}${path_path_1} 	headers=${Req_Headers} 	expected_status=200
	${accept_sub_2}= 	Get Substring LRB 	${accept} 	text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng, 	;q=0.8,application/signed-exchange;v=b3;q=0.7
	&{Req_Headers}= 	Create dictionary 	accept=${accept_sub_2} 	referer=${path} 	sec-fetch-dest=${sec-fetch-dest_1} 	sec-fetch-mode=${sec-fetch-mode_1} 	sec-fetch-site=${sec-fetch-site_1}
	${location_sub_3}= 	Fetch From Left 	${location} 	://demo6.6.tryton.org/#demo6.6/
	${resp_4}= 	GET On Session 	sess_demo_tryton_org 	url=${location_sub_3}://${location_sub_1}${path_path_2} 	headers=${Req_Headers} 	expected_status=200
	${accept_sub_3}= 	Get Substring LRB 	${accept} 	text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng, 	;q=0.8,application/signed-exchange;v=b3;q=0.7
	&{Req_Headers}= 	Create dictionary 	accept=${accept_sub_3} 	referer=${path} 	sec-fetch-dest=${sec-fetch-dest_1} 	sec-fetch-mode=${sec-fetch-mode_1} 	sec-fetch-site=${sec-fetch-site_1}
	${location_sub_4}= 	Fetch From Left 	${location} 	://demo6.6.tryton.org/#demo6.6/
	${path_path_2_sub}= 	Fetch From Left 	${path_path_2} 	/moment.min.js
	${resp_5}= 	GET On Session 	sess_demo_tryton_org 	url=${location_sub_4}://${location_sub_1}${path_path_2_sub}/locales.min.js 	headers=${Req_Headers} 	expected_status=200
	${accept_sub_4}= 	Get Substring LRB 	${accept} 	text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng, 	;q=0.8,application/signed-exchange;v=b3;q=0.7
	&{Req_Headers}= 	Create dictionary 	accept=${accept_sub_4} 	referer=${path} 	sec-fetch-dest=${sec-fetch-dest_1} 	sec-fetch-mode=${sec-fetch-mode_1} 	sec-fetch-site=${sec-fetch-site_1}
	${location_sub_5}= 	Fetch From Left 	${location} 	://demo6.6.tryton.org/#demo6.6/
	${resp_6}= 	GET On Session 	sess_demo_tryton_org 	url=${location_sub_5}://${location_sub_1}${path_path_3} 	headers=${Req_Headers} 	expected_status=200
	${accept_sub_5}= 	Get Substring LRB 	${accept} 	text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng, 	;q=0.8,application/signed-exchange;v=b3;q=0.7
	&{Req_Headers}= 	Create dictionary 	accept=${accept_sub_5} 	referer=${path} 	sec-fetch-dest=${sec-fetch-dest_1} 	sec-fetch-mode=${sec-fetch-mode_1} 	sec-fetch-site=${sec-fetch-site_1}
	${location_sub_6}= 	Fetch From Left 	${location} 	://demo6.6.tryton.org/#demo6.6/
	${resp_7}= 	GET On Session 	sess_demo_tryton_org 	url=${location_sub_6}://${location_sub_1}${path_path_4} 	headers=${Req_Headers} 	expected_status=200
	${accept_sub_6}= 	Get Substring LRB 	${accept} 	text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng, 	;q=0.8,application/signed-exchange;v=b3;q=0.7
	&{Req_Headers}= 	Create dictionary 	accept=${accept_sub_6} 	referer=${path} 	sec-fetch-dest=${sec-fetch-dest_1} 	sec-fetch-mode=${sec-fetch-mode_1} 	sec-fetch-site=${sec-fetch-site_1}
	${location_sub_7}= 	Fetch From Left 	${location} 	://demo6.6.tryton.org/#demo6.6/
	${resp_8}= 	GET On Session 	sess_demo_tryton_org 	url=${location_sub_7}://${location_sub_1}${path_path_5} 	headers=${Req_Headers} 	expected_status=200
	${accept_sub_7}= 	Get Substring LRB 	${accept} 	text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng, 	;q=0.8,application/signed-exchange;v=b3;q=0.7
	&{Req_Headers}= 	Create dictionary 	accept=${accept_sub_7} 	referer=${path} 	sec-fetch-dest=${sec-fetch-dest_1} 	sec-fetch-mode=${sec-fetch-mode_1} 	sec-fetch-site=${sec-fetch-site_1}
	${location_sub_8}= 	Fetch From Left 	${location} 	://demo6.6.tryton.org/#demo6.6/
	${resp_9}= 	GET On Session 	sess_demo_tryton_org 	url=${location_sub_8}://${location_sub_1}${path_path_6} 	headers=${Req_Headers} 	expected_status=200
	${accept_sub_8}= 	Get Substring LRB 	${accept} 	text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng, 	;q=0.8,application/signed-exchange;v=b3;q=0.7
	&{Req_Headers}= 	Create dictionary 	accept=${accept_sub_8} 	referer=${path} 	sec-fetch-dest=${sec-fetch-dest_1} 	sec-fetch-mode=${sec-fetch-mode_1} 	sec-fetch-site=${sec-fetch-site_1}
	${location_sub_9}= 	Fetch From Left 	${location} 	://demo6.6.tryton.org/#demo6.6/
	${resp_10}= 	GET On Session 	sess_demo_tryton_org 	url=${location_sub_9}://${location_sub_1}${path_path_7} 	headers=${Req_Headers} 	expected_status=200
	${accept_sub_9}= 	Get Substring LRB 	${accept} 	text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng, 	;q=0.8,application/signed-exchange;v=b3;q=0.7
	&{Req_Headers}= 	Create dictionary 	accept=${accept_sub_9} 	referer=${path} 	sec-fetch-dest=${sec-fetch-dest_1} 	sec-fetch-mode=${sec-fetch-mode_1} 	sec-fetch-site=${sec-fetch-site_1}
	${location_sub_10}= 	Fetch From Left 	${location} 	://demo6.6.tryton.org/#demo6.6/
	${path_path_7_sub}= 	Fetch From Left 	${path_path_7} 	/fullcalendar.min.js
	${resp_11}= 	GET On Session 	sess_demo_tryton_org 	url=${location_sub_10}://${location_sub_1}${path_path_7_sub}/locale-all.js 	headers=${Req_Headers} 	expected_status=200
	${accept_sub_10}= 	Get Substring LRB 	${accept} 	text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng, 	;q=0.8,application/signed-exchange;v=b3;q=0.7
	&{Req_Headers}= 	Create dictionary 	accept=${accept_sub_10} 	referer=${path} 	sec-fetch-dest=${sec-fetch-dest_1} 	sec-fetch-mode=${sec-fetch-mode_1} 	sec-fetch-site=${sec-fetch-site_1}
	${location_sub_11}= 	Fetch From Left 	${location} 	://demo6.6.tryton.org/#demo6.6/
	${resp_12}= 	GET On Session 	sess_demo_tryton_org 	url=${location_sub_11}://${location_sub_1}${path_path_8} 	headers=${Req_Headers} 	expected_status=200
	${accept_sub_11}= 	Get Substring LRB 	${accept} 	text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng, 	;q=0.8,application/signed-exchange;v=b3;q=0.7
	&{Req_Headers}= 	Create dictionary 	accept=${accept_sub_11} 	referer=${path} 	sec-fetch-dest=${sec-fetch-dest_1} 	sec-fetch-mode=${sec-fetch-mode_1} 	sec-fetch-site=${sec-fetch-site_1}
	${location_sub_12}= 	Fetch From Left 	${location} 	://demo6.6.tryton.org/#demo6.6/
	${resp_13}= 	GET On Session 	sess_demo_tryton_org 	url=${location_sub_12}://${location_sub_1}${path_path_9} 	headers=${Req_Headers} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	accept=${accept_1} 	referer=${path} 	sec-fetch-dest=${sec-fetch-dest_2} 	sec-fetch-mode=${sec-fetch-mode_1} 	sec-fetch-site=${sec-fetch-site_1}
	${location_sub_13}= 	Fetch From Left 	${location} 	://demo6.6.tryton.org/#demo6.6/
	${path_path_5_sub}= 	Fetch From Left 	${path_path_5} 	/c3.min.js
	${resp_14}= 	GET On Session 	sess_demo_tryton_org 	url=${location_sub_13}://${location_sub_1}${path_path_5_sub}/c3.min.css 	headers=${Req_Headers} 	expected_status=200
	&{Req_Headers}= 	Create dictionary 	accept=${accept_1} 	referer=${path} 	sec-fetch-dest=${sec-fetch-dest_2} 	sec-fetch-mode=${sec-fetch-mode_1} 	sec-fetch-site=${sec-fetch-site_1}
	${location_sub_14}= 	Fetch From Left 	${location} 	://demo6.6.tryton.org/#demo6.6/
	${resp_15}= 	GET On Session 	sess_demo_tryton_org 	url=${location_sub_14}://${location_sub_1}${path_path_7_sub}/fullcalendar.min.css 	headers=${Req_Headers} 	expected_status=200
	${accept_sub_12}= 	Get Substring LRB 	${accept} 	text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng, 	;q=0.8,application/signed-exchange;v=b3;q=0.7
	&{Req_Headers}= 	Create dictionary 	accept=${accept_sub_12} 	referer=${path} 	sec-fetch-dest=${sec-fetch-dest_1} 	sec-fetch-mode=${sec-fetch-mode_1} 	sec-fetch-site=${sec-fetch-site_1}
	${location_sub_15}= 	Fetch From Left 	${location} 	://demo6.6.tryton.org/#demo6.6/
	${path_path_sub}= 	Get Substring LRB 	${path_path} 	/bower_components/jquery 	/jquery.min.js
	${resp_16}= 	GET On Session 	sess_demo_tryton_org 	url=${location_sub_15}://${location_sub_1}${path_path_sub}/tryton-sao.min.js 	headers=${Req_Headers} 	expected_status=200
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
	${location_sub_16}= 	Fetch From Left 	${location} 	://demo6.6.tryton.org/#demo6.6/
	${path_path_sub_1}= 	Get Substring LRB 	${path_path} 	/bower_components/jquery 	/jquery.min.js
	${resp_17}= 	GET On Session 	sess_demo_tryton_org 	url=${location_sub_16}://${location_sub_1}${path_path_sub_1}/tryton-sao.min.css 	headers=${Req_Headers} 	expected_status=200
	${accept_sub_13}= 	Get Substring LRB 	${accept} 	text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng, 	;q=0.8,application/signed-exchange;v=b3;q=0.7
	&{Req_Headers}= 	Create dictionary 	accept=${accept_sub_13} 	referer=${path} 	sec-fetch-dest=${sec-fetch-dest_1} 	sec-fetch-mode=${sec-fetch-mode_1} 	sec-fetch-site=${sec-fetch-site_1}
	${location_sub_17}= 	Fetch From Left 	${location} 	://demo6.6.tryton.org/#demo6.6/
	${resp_18}= 	GET On Session 	sess_demo_tryton_org 	url=${location_sub_17}://${location_sub_1}${path_path_10} 	headers=${Req_Headers} 	expected_status=405
	&{Req_Headers}= 	Create dictionary 	accept=${accept_1} 	referer=${path} 	sec-fetch-dest=${sec-fetch-dest_2} 	sec-fetch-mode=${sec-fetch-mode_1} 	sec-fetch-site=${sec-fetch-site_1}
	${location_sub_18}= 	Fetch From Left 	${location} 	://demo6.6.tryton.org/#demo6.6/
	${resp_19}= 	GET On Session 	sess_demo_tryton_org 	url=${location_sub_18}://${location_sub_1}${path_path_11} 	headers=${Req_Headers} 	expected_status=405
	${sec-fetch-mode_1_sub}= 	Fetch From Right 	${sec-fetch-mode_1} 	no-
	&{Req_Headers}= 	Create dictionary 	accept=${accept_2} 	referer=${path} 	sec-fetch-dest=${sec-fetch-dest_3} 	sec-fetch-mode=${sec-fetch-mode_1_sub} 	sec-fetch-site=${sec-fetch-site_1} 	x-requested-with=${x-requested-with}
	${location_sub_19}= 	Fetch From Left 	${location} 	://demo6.6.tryton.org/#demo6.6/
	${resp_20}= 	GET On Session 	sess_demo_tryton_org 	url=${location_sub_19}://${location_sub_1}${path_path_12} 	headers=${Req_Headers} 	expected_status=405
	${accept_sub_14}= 	Get Substring LRB 	${accept} 	text/html,application/xhtml+xml,application/xml;q=0.9, 	/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
	&{Req_Headers}= 	Create dictionary 	accept=${accept_3} 	referer=${path} 	sec-fetch-dest=${accept_sub_14} 	sec-fetch-mode=${sec-fetch-mode_1} 	sec-fetch-site=${sec-fetch-site_1}
	${location_sub_20}= 	Fetch From Left 	${location} 	://demo6.6.tryton.org/#demo6.6/
	${resp_21}= 	GET On Session 	sess_demo_tryton_org 	url=${location_sub_20}://${location_sub_1}${path_path_13} 	headers=${Req_Headers} 	expected_status=200
	${sec-fetch-mode_1_sub_1}= 	Fetch From Right 	${sec-fetch-mode_1} 	no-
	&{Req_Headers}= 	Create dictionary 	accept=${accept_2} 	referer=${path} 	sec-fetch-dest=${sec-fetch-dest_3} 	sec-fetch-mode=${sec-fetch-mode_1_sub_1} 	sec-fetch-site=${sec-fetch-site_1} 	x-requested-with=${x-requested-with}
	${location_sub_21}= 	Fetch From Left 	${location} 	://demo6.6.tryton.org/#demo6.6/
	${path_path_12_sub}= 	Fetch From Left 	${path_path_12} 	/en_GB.json
	${resp_22}= 	GET On Session 	sess_demo_tryton_org 	url=${location_sub_21}://${location_sub_1}${path_path_12_sub}/en.json 	headers=${Req_Headers} 	expected_status=405
	${accept_2_sub}= 	Fetch From Left 	${accept_2} 	, text/javascript, */*; q=0.01
	${location_sub_22}= 	Fetch From Left 	${location} 	/#demo6.6/
	${sec-fetch-mode_1_sub_2}= 	Fetch From Right 	${sec-fetch-mode_1} 	no-
	&{Req_Headers}= 	Create dictionary 	accept=${accept_2} 	content-type=${accept_2_sub} 	origin=${location_sub_22} 	referer=${path} 	sec-fetch-dest=${sec-fetch-dest_3} 	sec-fetch-mode=${sec-fetch-mode_1_sub_2} 	sec-fetch-site=${sec-fetch-site_1} 	x-requested-with=${x-requested-with}
	${accept_sub_15}= 	Get Substring LRB 	${accept} 	text/html,application/xhtml+xml,application/xml;q= 	.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
	@{json_23_params}= 	Create List
	&{json_23}= 	Create Dictionary 	id=${accept_sub_15} 	method=${method} 	params=${json_23_params}
	&{postdata_23}= 	Create dictionary
	${resp_23}= 	POST On Session 	sess_demo_tryton_org 	url=${path} 	headers=${Req_Headers} 	expected_status=200 	json=${json_23} 	data=${postdata_23}
	${sec-fetch-mode_1_sub_3}= 	Fetch From Right 	${sec-fetch-mode_1} 	no-
	&{Req_Headers}= 	Create dictionary 	accept=${accept_2} 	content-type=${accept_2_sub} 	origin=${location_sub_22} 	referer=${path} 	sec-fetch-dest=${sec-fetch-dest_3} 	sec-fetch-mode=${sec-fetch-mode_1_sub_3} 	sec-fetch-site=${sec-fetch-site_1} 	x-requested-with=${x-requested-with}
	${accept_sub_16}= 	Get Substring LRB 	${accept} 	text/html,application/xhtml+xml,application/xml;q= 	.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
	@{json_24_params}= 	Create List
	&{json_24}= 	Create Dictionary 	id=${accept_sub_16} 	method=${method_1} 	params=${json_24_params}
	&{postdata_24}= 	Create dictionary
	${resp_24}= 	POST On Session 	sess_demo_tryton_org 	url=${path} 	headers=${Req_Headers} 	expected_status=200 	json=${json_24} 	data=${postdata_24}
	${sec-fetch-mode_1_sub_4}= 	Fetch From Right 	${sec-fetch-mode_1} 	no-
	&{Req_Headers}= 	Create dictionary 	accept=${accept_2} 	content-type=${accept_2_sub} 	origin=${location_sub_22} 	referer=${path} 	sec-fetch-dest=${sec-fetch-dest_3} 	sec-fetch-mode=${sec-fetch-mode_1_sub_4} 	sec-fetch-site=${sec-fetch-site_1} 	x-requested-with=${x-requested-with}
	${accept_sub_17}= 	Get Substring LRB 	${accept} 	text/html,application/xhtml+xml,application/xml;q= 	.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
	@{json_25_params}= 	Create List
	&{json_25}= 	Create Dictionary 	id=${accept_sub_17} 	method=${method_2} 	params=${json_25_params}
	&{postdata_25}= 	Create dictionary
	${resp_25}= 	POST On Session 	sess_demo_tryton_org 	url=${path} 	headers=${Req_Headers} 	expected_status=200 	json=${json_25} 	data=${postdata_25}
	${sec-fetch-mode_1_sub_5}= 	Fetch From Right 	${sec-fetch-mode_1} 	no-
	&{Req_Headers}= 	Create dictionary 	accept=${accept_2} 	content-type=${accept_2_sub} 	origin=${location_sub_22} 	referer=${path} 	sec-fetch-dest=${sec-fetch-dest_3} 	sec-fetch-mode=${sec-fetch-mode_1_sub_5} 	sec-fetch-site=${sec-fetch-site_1} 	x-requested-with=${x-requested-with}
	${location_sub_23}= 	Get Substring LRB 	${location} 	https:// 	6.6.tryton.org/#demo6.6/
	${accept-language_sub}= 	Fetch From Left 	${accept-language} 	-GB,en;q=0.9
	${accept_sub_18}= 	Get Substring LRB 	${accept} 	text/html,application/xhtml+xml,application/xml;q= 	.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
	&{json_26_params_1}= 	Create Dictionary 	device_cookie=${None}
	@{json_26_params}= 	Create List 	${location_sub_23} 	${json_26_params_1} 	${accept-language_sub}
	&{json_26}= 	Create Dictionary 	method=${method_3} 	params=${json_26_params} 	id=${accept_sub_18}
	&{postdata_26}= 	Create dictionary
	${location_sub_24}= 	Fetch From Left 	${location} 	://demo6.6.tryton.org/#demo6.6/
	${location_sub_25}= 	Get Substring LRB 	${location} 	https:/ 	.tryton.org/#demo6.6/
	${accept_sub_19}= 	Get Substring LRB 	${accept} 	text 	html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
	${resp_26}= 	POST On Session 	sess_demo_tryton_org 	url=${location_sub_24}://${location_sub_1}${location_sub_25}${accept_sub_19} 	headers=${Req_Headers} 	expected_status=200 	json=${json_26} 	data=${postdata_26}
	${sec-fetch-mode_1_sub_6}= 	Fetch From Right 	${sec-fetch-mode_1} 	no-
	&{Req_Headers}= 	Create dictionary 	accept=${accept_2} 	authorization=${authorization} 	content-type=${accept_2_sub} 	origin=${location_sub_22} 	referer=${path} 	sec-fetch-dest=${sec-fetch-dest_3} 	sec-fetch-mode=${sec-fetch-mode_1_sub_6} 	sec-fetch-site=${sec-fetch-site_1} 	x-requested-with=${x-requested-with}
	${accept_sub_20}= 	Get Substring LRB 	${accept} 	text/html,application/xhtml+xml,application/xml;q= 	.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
	&{json_27_params_1}= 	Create Dictionary 	client=${client}
	@{json_27_params}= 	Create List 	 	${json_27_params_1}
	&{json_27}= 	Create Dictionary 	id=${accept_sub_20} 	method=${method_4} 	params=${json_27_params}
	&{postdata_27}= 	Create dictionary
	${location_sub_26}= 	Fetch From Left 	${location} 	://demo6.6.tryton.org/#demo6.6/
	${location_sub_27}= 	Get Substring LRB 	${location} 	https:/ 	.tryton.org/#demo6.6/
	${accept_sub_21}= 	Get Substring LRB 	${accept} 	text 	html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
	${resp_27}= 	POST On Session 	sess_demo_tryton_org 	url=${location_sub_26}://${location_sub_1}${location_sub_27}${accept_sub_21} 	headers=${Req_Headers} 	expected_status=200 	json=${json_27} 	data=${postdata_27}


