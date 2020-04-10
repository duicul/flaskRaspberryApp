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
