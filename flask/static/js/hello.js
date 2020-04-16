function draw_gauge(){
$.ajax({url: "/read_sensor/dummy/43", success: function(result){
    console.log(result);
    gauges=[];
    div_html="";
    result=JSON.parse(result)
    result.forEach(function(item,index){
                      div_html+=item["name"]+"  "+item["val"]+"</br>";}
                   );
    $("#graphdiv").html(div_html);

    }});
}


function draw_graph(){
	countries_checked=verifycheck();
	var data=[]
	console.log(countries_checked)
	countries_checked.forEach(function(item,index){
		
		$.ajax({url:"https://api.covid19api.com/dayone/country/"+item+"/status/confirmed/live",success : function(result)
	    {	datap=[]
			result.forEach(function(item){
				if(item["Province"] ==""){
					date_now= new Date(item["Date"]);
					year=date_now.getFullYear()
					if(year==2020 || year==2021)
						datap.push({x: new Date(item["Date"]),y:item["Cases"]});
				
				}
			});
			$("#graph").html("");
			count={type: "line",dataPoints:datap,name: item,showInLegend: true,};
			data.push(count);
			console.log(data);
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
	    });
		
		
	});	
}
var countries=[];
function load_countries(){
	$.ajax({url:"https://api.covid19api.com/countries",success : function(result)
	    {data="<button onClick=\"draw_graph()\">Display</button></br> ";
		data+="<div class=\"\" style=\"width:300px;height:500px;overflow:auto;\">";
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
			console.log("checked "+item);
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
	
	
