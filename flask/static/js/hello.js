function draw_gauge(){
$.ajax({url: "/read_sensor/dummy/43", success: function(result){
    //console.log(result);
    gauges=[];
    div_html="";
    result=JSON.parse(result)
    result.forEach(function(item,index){
                      div_html+=item["name"]+"  "+item["val"]+"</br>";
		      div_html+="<div id=\"gauge"+item["name"]+"\"></div></br>";}
                   );
    $("#graphdiv").html(div_html);
	result.forEach(function(item,index){
                      var radial = new RadialGauge({
							renderTo: 'gauge-id',
							width: 400,
							height: 400,
							units: 'Km/h',
							title: false,
							value: item["val"],
							minValue: 0,
							maxValue: 220,
							majorTicks: ['-10','-5','0','5','10','15','20','25','30','35','40'],
							minorTicks: 2,
							strokeTicks: false,
							highlights: [
								{ from: 0, to: 50, color: 'rgba(0,255,0,.15)' },
								{ from: 50, to: 100, color: 'rgba(255,255,0,.15)' },
								{ from: 100, to: 150, color: 'rgba(255,30,0,.25)' },
								{ from: 150, to: 200, color: 'rgba(255,0,225,.25)' },
								{ from: 200, to: 220, color: 'rgba(0,0,255,.25)' }
							],
							colorPlate: '#222',
							colorMajorTicks: '#f5f5f5',
							colorMinorTicks: '#ddd',
							colorTitle: '#fff',
							colorUnits: '#ccc',
							colorNumbers: '#eee',
							colorNeedle: 'rgba(240, 128, 128, 1)',
							colorNeedleEnd: 'rgba(255, 160, 122, .9)',
							valueBox: true,
							animationRule: 'bounce',
							animationDuration: 500
					});
					radial.draw();
					}
                   );

    }});
}


function draw_graph(){
	countries_checked=verifycheck();
	var data=[]
	//console.log(countries_checked)
	countries_checked.forEach(function(item,index){
		
		$.ajax({url:"https://api.covid19api.com/dayone/country/"+item+"/status/confirmed/live",success : function(result)
	    {	datapdata=[]
			datapgrowth=[]
			datapgrowthchange=[]
			prev_val=0
			prev_growth=0
			result.forEach(function(item){
				if(item["Province"] ==""){
					date_now= new Date(item["Date"]);
					year=date_now.getFullYear()
					if(year==2020 || year==2021){
						growth=item["Cases"]-prev_val
						datapdata.push({x: new Date(item["Date"]),y:item["Cases"]});
						datapgrowth.push({x: new Date(item["Date"]),y:(growth)});
						datapgrowthchange.push({x: new Date(item["Date"]),y:(growth-prev_growth)});
						prev_val=item["Cases"];
						prev_growth=growth;
					}
				
				}
			});
			$("#graph").html("");
			datapdata.pop()
			datapgrowth.pop()
			datapgrowthchange.pop()
			data_type=$("#data_type").val()
			if(data_type == "data"){
				count_data={type: "line",dataPoints:datapdata,name: item,showInLegend: true,};
				data.push(count_data);
			}
			if(data_type == "growth"){
				count_growth={type: "line",dataPoints:datapgrowth,name: item+" growth",showInLegend: true,};
				data.push(count_growth);
			}
			if(data_type == "growthchange"){
				count_growthchange={type: "line",dataPoints:datapgrowthchange,name: item,showInLegend: true,};
				data.push(count_growthchange);
			}
			
			//console.log(data);
			if(data.length==countries_checked.length){
				var chart = new CanvasJS.Chart("graph", {
					animationEnabled: true,
					title:{	text: "Cases"},
					toolTip: {
						shared: true
					},
					legend: {
						horizontalAlign: "left", // "center" , "right"
						verticalAlign: "center",  // "top" , "bottom"
						fontSize: 15
						},
					axisY:{includeZero: true},
					data:eval(data)
				});
				chart.render();
			}
		}
	    });
		
		
	});	
}
function draw_graph_local(){
	api=$("#api_source").val();
	countries_checked=[]
	if(api=="covid19api")
		countries_checked=verifycheck();
	var data=[]
	data_type=$("#data_type").val()
	//console.log(api)
	//console.log(countries_checked)
	pol_grade=$("#pol_grade").val()
	case_type=$("#case_type_select").val();
	//console.log(case_type);
	var url="/covid_data/"+case_type+"/"+api+"/"+data_type;
	//console.log(api)
	if(pol_grade!="None"){
		pred_len=$("#pred_select").val()
		url="/covid_data_all/"+case_type+"/"+api+"/"+data_type+"/"+pred_len+"/"+pol_grade;
	}
	var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                $("#graph").html("");
				//console.log(xmlhttp.responseText)
				//console.log(eval(xmlhttp.responseText))
				var chart = new CanvasJS.Chart("graph", {
					animationEnabled: true,
					title:{	text: "Cases"},
					toolTip: {
						shared: true
					},
					legend: {
						horizontalAlign: "center", // "left" , "right"
						verticalAlign: "bottom",  // "top" , "center"
						fontSize: 15
						},
					axisY:{includeZero: true},
					data:eval(xmlhttp.responseText)
				});
				chart.render();
			}
        };
    var formData = new FormData();
    formData.append("countries",JSON.stringify(countries_checked));
    xmlhttp.open("POST",url, true);
    xmlhttp.send(formData);
	
	/*
	$.get("/covid_data/Confirmed/"+data_type,{countries: countries_checked},function(data, status){
	$("#graph").html("");
    var chart = new CanvasJS.Chart("graph", {
					animationEnabled: true,
					title:{	text: "Cases"},
					toolTip: {
						shared: true
					},
					legend: {
						horizontalAlign: "left", // "center" , "right"
						verticalAlign: "center",  // "top" , "bottom"
						fontSize: 15
						},
					axisY:{includeZero: true},
					data:eval(data)
				});
				chart.render();
	
  });*/
}
var prev_pol="None"
function displaypredlength(){
pol_grade=$("#pol_grade").val()
//console.log(pol_grade)
if(pol_grade=="None"){
	$("#pred_len").html("");
	prev_pol=pol_grade
	return;}
if(prev_pol=="None"){
	data="Prediction length : </br>";
	data+="<select id=\"pred_select\">";
	for(i=1;i<=30;i++){
		data+="<option value=\""+i*10+"\">";
		data+=i*10+" Days</option>";
	}
	$("#pred_len").html(data);}
prev_pol=pol_grade
}
var apis=[{"name":"covid19api","display":"api.covid19api.com"},{"name":"geospatial","display":"covid19.geo-spatial (Romania)"}]


function show_api_options(){
api=$("#api_source").val()
if(api=="covid19api"){
load_countries();
data="Case Type: </br>";
data+="<select id=\"case_type_select\">";
data+="<option value=\"Confirmed\">";
data+="Confirmed</option>";
data+="</select><hr>";
api=$("#case_type").html(data)
}
else if(api=="geospatial"){
	$("#country_list").html("");
	data="Case Type: </br>";
	data+="<select id=\"case_type_select\">";
	data+="<option value=\"Active\">";
	data+="Active</option>";
	data+="<option value=\"Confirmed\">";
	data+="Confirmed</option>";
	data+="</select><hr>";
	api=$("#case_type").html(data)
	return;}

}

function load_main_menu(){
	data="<button onClick=\"draw_graph_local()\">Display</button></br> ";
		data+="Data to show: </br>";
                data+="<select id=\"data_type\">";
		data+="<option value=\"data\">";
		data+="Cases data</option>";
		data+="<option value=\"growth\">";
		data+="Cases growth</option>";
		data+="<option value=\"growth_change\">";
		data+="Cases growth change</option>";
		data+="</select><hr>";
		
		data+="Polinomial Aproximation : </br>";
        data+="<select id=\"pol_grade\" onchange=displaypredlength();>";
		data+="<option value=\"None\">";
		data+="None</option>";
		for(i=1;i<=10;i++){
			data+="<option value=\""+i+"\">";
			data+="Grade "+i+"</option>";}
		data+="</select>";
		data+="<div id=\"pred_len\"></div>";
		data+="<hr>";
		
		data+="<div id=\"case_type\">"
		data+="Case Type: </br>";
        data+="<select id=\"case_type_select\">";
		data+="<option value=\"Confirmed\">";
		data+="Confirmed</option>";
		data+="</select><hr>";
		data+="</div>"
		
		data+="API source : </br>";
        data+="<select id=\"api_source\" onchange=show_api_options();>";
		for(i=0;i<apis.length;i++){
			data+="<option value=\""+apis[i]["name"]+"\">";
			data+=apis[i]["display"]+"</option>";}
		data+="</select>"
		
		data+="<div id=\"country_list\"></div>";
		
		$("#main_menu").html(data);
		
		show_api_options();
}


var countries=[];
function load_countries(){
	$.ajax({url:"https://api.covid19api.com/countries",success : function(result)
	    {data="<div class=\"\" style=\"width:300px;height:500px;overflow:auto;\">";
		result.sort(function(a,b){return a["Country"]> b["Country"]});
		result.forEach(function(item,index){
			countries.push(item["Slug"]);
			data+="<input type=\"checkbox\"id=\"country"+item["Slug"]+"\">";
			data+="<label>"+item["Country"]+"</label>";
			data+="</br>";
		});	
		data+="</div> ";
		$("#country_list").html(data);
		}
	    });
		

}

function verifycheck(){
	checked=[]
	countries.forEach(function (item,index){
		if($("#country"+item).is(":checked")){
			//console.log("checked "+item);
			checked.push(item);
		}
	});
	return checked;
}

var interval_calls;
function hello(){
alert("hello");
$("#messfunc").html("hello");
 //document.getElementById("messfunc").innerHTML = "hello";
 }

function goodbye(){
 alert("goodbye");
 $("#messfunc").html("goodbye");
 //document.getElementById("messfunc").innerHTML = "goodbye";
 } 
 var ind=0;

 function init_server(period)
 {//interval_calls=setInterval(ajax_calls,period);
  }

  /*$("#login_form").submit(function( event ) { console.log("loginform");event.preventDefault();login();})
  $("#wifi_form").submit(function( event ) { console.log("configform");event.preventDefault();setwifidata();})
  $("#config_form").submit(function( event ) { console.log("wifiform");event.preventDefault();setconfigdata();})
  $("#logindata_form").submit(function( event ) { console.log("logindataform");event.preventDefault();setpassworddata();})*/
  
function login()
{console.log("logging in ...");
var url="/login";
	var xmlhttp = new XMLHttpRequest();
        xmlhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                if(xmlhttp.responseText == "okay")
		{console.log("logged in");
                window.location.replace("/");}
		else alert("Wrong username/password");
		}
        };
    var formData = new FormData();
    formData.append("user_txt",$("#user_txt").val());
    formData.append("pass_txt",$("#pass_txt").val());
    xmlhttp.open("POST",url, true);
	xmlhttp.send(formData);	
}

function ajax_calls(){
board_status();
update_data();
}

function stopajaxcalls()
{clearInterval(interval_calls);}

function getconfigdata()
 {console.log("getconfigdata");
$.ajax({url: "/getconfigdata", success: function(result){
$("#config").html(result);}})
}
 
function init()
{$("#login_form").submit(function( event ) { console.log("loginform");event.preventDefault();login();})
  $("#wifi_form").submit(function( event ) { console.log("wifiform");event.preventDefault();setwifidata();})
  $("#config_form").submit(function( event ) { console.log("configform");event.preventDefault();setconfigdata();})
  $("#logindata_form").submit(function( event ) { console.log("logindataform");event.preventDefault();setpassworddata();})
}
 
function getpassworddata()
 {console.log("getpassworddata");
$.ajax({url: "/getpassworddata", success: function(result){
$("#passconfig").html(result);}
}

)

}
 
 
function setconfigdata()
 {
var url="/setconfigdata";
        var xmlhttp = new XMLHttpRequest();
        xmlhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                if(xmlhttp.responseText == "okay")
                {getconfigdata();
				 alert("Configuration changed");}}
        };
    var formData = new FormData();
    formData.append("user",$("#username").val());
    formData.append("pass",$("#password").val());
    formData.append("ip",$("#ip").val());
    formData.append("port",$("#port").val());
	formData.append("refresh_in",$("#refresh_in").val());
	formData.append("refresh_out",$("#refresh_out").val());
	formData.append("logtime",$("#logtime").val());
    xmlhttp.open("POST",url, true);
        xmlhttp.send(formData);
}

function setpassworddata()
{var url="/changeuserpassword";
        var xmlhttp = new XMLHttpRequest();
        xmlhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                if(xmlhttp.responseText == "okay")
                {getconfigdata();
				 alert("Password changed");}}
        };
    var formData = new FormData();
    formData.append("user",$("#username").val());
    formData.append("pass",$("#password").val());
    xmlhttp.open("POST",url, true);
        xmlhttp.send(formData);
}


function getwifidata()
 {console.log("getwifidata");
$.ajax({url: "/getwifidata", success: function(result){
       $("#wifi").html(result);}})
}
 
function setwifidata()
 {console.log("setwifidata");
var url="/setwifidata";
        var xmlhttp = new XMLHttpRequest();
        xmlhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                if(xmlhttp.responseText == "okay")
                {getwifidata();
				 alert("Wifi settings changed");}}
        };
    var formData = new FormData();
    formData.append("wifi_ssid",$("#wifi_ssid").val());
    formData.append("wifi_psk",$("#wifi_psk").val());
    xmlhttp.open("POST",url, true);
        xmlhttp.send(formData);
}

 function board_status()
 {$.ajax({url: "/board_status", success: function(result){
       $("#board_status").html(result+" "+ind);
	   ind++;}});	 }

function update_data(){
  $.ajax({url:"/data_retr",success : function(result)
     {$("#data_status").html(result+" "+ind);}});  }

 function loginstatus(){
 $.ajax({url: "/loginstatus.py", success: function(result){
       alert(result);
	   $("#login_form").submit(function( event ) { console.log("loginform");event.preventDefault();login();})
    }}); } 
	
	
