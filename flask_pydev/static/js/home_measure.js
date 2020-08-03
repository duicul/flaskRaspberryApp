var temp_opt={"temp1":{"name":"Temperature1","checked":true},"temp2":{"name":"Temperature2","checked":true}};
var volt_opt={"volt1":{"name":"Voltage","checked":false}};
var ac_opt={"voltage":{"name":"Voltage","checked":false},"current":{"name":"Current","checked":false},"power":{"name":"Power","checked":true},"energy":{"name":"Energy - KWh ","checked":false},"energyday":{"name":"Energy Daily - Wh","checked":false},"energyhour":{"name":"Energy Hourly - Wh","checked":false},"energysample":{"name":"Energy between Samples - Wh","checked":false}};

function show_opt(){
    data="";
    checked=temp_opt["temp1"]["checked"]==true? "checked=\"checked\"" : "";
    data+="<input type=\"checkbox\" "+checked+" onchange=\"check_state('temp',1,this)\">";
    data+="<label>"+temp_opt["temp1"]["name"]+"</label></br>";
    
    checked=temp_opt["temp2"]["checked"]==true? "checked=\"checked\"" : "";
    data+="<input type=\"checkbox\" "+checked+" onchange=\"check_state('temp',2,this)\">";
    data+="<label>"+temp_opt["temp2"]["name"]+"</label></br>";
    
    checked=volt_opt["volt1"]["checked"]==true? "checked=\"checked\"" : "";
    data+="<input type=\"checkbox\" "+checked+" onchange=\"check_state('volt',1,this)\">";
    data+="<label>"+volt_opt["volt1"]["name"]+"</label></br>";
    
    $("#temp_volt_opt").html(data);
}

function show_opt_ac(){
    data="";
    checked=ac_opt["voltage"]["checked"]==true? "checked=\"checked\"" : "";
    data+="<input type=\"checkbox\" "+checked+" onchange=\"check_state_ac('voltage',this)\">";
    data+="<label>"+ac_opt["voltage"]["name"]+"</label></br>";
    
    checked=ac_opt["current"]["checked"]==true? "checked=\"checked\"" : "";
    data+="<input type=\"checkbox\" "+checked+" onchange=\"check_state_ac('current',this)\">";
    data+="<label>"+ac_opt["current"]["name"]+"</label></br>";
    
    checked=ac_opt["power"]["checked"]==true? "checked=\"checked\"" : "";
    data+="<input type=\"checkbox\" "+checked+" onchange=\"check_state_ac('power',this)\">";
    data+="<label>"+ac_opt["power"]["name"]+"</label></br>";
    
    checked=ac_opt["energy"]["checked"]==true? "checked=\"checked\"" : "";
    data+="<input type=\"checkbox\" "+checked+" onchange=\"check_state_ac('energy',this)\">";
    data+="<label>"+ac_opt["energy"]["name"]+"</label></br>";
    
    checked=ac_opt["energyday"]["checked"]==true? "checked=\"checked\"" : "";
    data+="<input type=\"checkbox\" "+checked+" onchange=\"check_state_ac('energyday',this)\">";
    data+="<label>"+ac_opt["energyday"]["name"]+"</label></br>";
    
    checked=ac_opt["energyhour"]["checked"]==true? "checked=\"checked\"" : "";
    data+="<input type=\"checkbox\" "+checked+" onchange=\"check_state_ac('energyhour',this)\">";
    data+="<label>"+ac_opt["energyhour"]["name"]+"</label></br>";
    
    checked=ac_opt["energysample"]["checked"]==true? "checked=\"checked\"" : "";
    data+="<input type=\"checkbox\" "+checked+" onchange=\"check_state_ac('energysample',this)\">";
    data+="<label>"+ac_opt["energysample"]["name"]+"</label></br>";
    
    $("#ac_opt").html(data);
}

function check_state(type,index,elem){
    if(type=="temp"){
        if(index==1)
            temp_opt["temp1"]["checked"]=elem.checked
        else if(index==2)
            temp_opt["temp2"]["checked"]=elem.checked
        }
    else if(type=="volt"){
            if(index==1)
                volt_opt["volt1"]["checked"]=elem.checked
            }
    //console.log(temp_opt)
    //console.log(volt_opt)
}   

function check_state_ac(type,elem){
    ac_opt[type]["checked"]=elem.checked
    //console.log(ac_opt)
} 

function init(){
	draw_gauge_temperature();
	draw_gauge_voltage();
	draw_gauge_ac();
	draw_graph();
	show_opt();
	show_opt_ac();
	setInterval(function(){ draw_gauge_temperature();
							draw_gauge_voltage();
							draw_gauge_ac()
							//draw_graph();
							}, 300000);
}

function force_refresh(){
$.ajax({url: "/force_poll", success: function(result){
	draw_gauge_temperature();
	draw_gauge_voltage();
	draw_gauge_ac();
	draw_graph();
	}});
}

function draw_gauge_temperature(){
$.ajax({url: "/temperature", success: function(result){
	//console.log(result)
    //result=JSON.parse(result)
	div_html=""
	div_html+=new Date(result["date"]).toString()+"</br>"
	div_html+="<canvas id=\"gauge_temp_1\"></canvas>";
	div_html+="<canvas id=\"gauge_temp_2\"></canvas>";
    $("#draw_gauge_temperature").html(div_html);
    var radial1 = new RadialGauge({
							renderTo: 'gauge_temp_1',
							width: 200,
							height: 200,
							units: 'C',
							title: false,
							value: result["temp1"],
							minValue: -10,
							maxValue: 110,
							majorTicks: ['-10','5','20','35','50','65','80','95','110'],
							minorTicks: 4,
							strokeTicks: false,
							highlights: [
								{ from: -10, to: 5, color: 'rgba(0,0,255,.15)' },
								{ from: 5, to: 20, color: 'rgba(0,0,100,.15)' },
								{ from: 20, to: 35, color: 'rgba(0,200,0,.25)' },
								{ from: 35, to: 50, color: 'rgba(0,100,0,.25)' },
								{ from: 50, to: 65, color: 'rgba(50,100,0,.15)' },
								{ from: 65, to: 80, color: 'rgba(100,100,0,.15)' },
								{ from: 80, to: 95, color: 'rgba(150,100,0,.25)' },
								{ from: 95, to: 110, color: 'rgba(200,100,0,.25)' },
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
	radial1.draw();
	var radial2 = new RadialGauge({
							renderTo: 'gauge_temp_2',
							width: 200,
							height: 200,
							units: 'C',
							title: false,
							value: result["temp2"],
							minValue: -10,
							maxValue: 110,
							majorTicks: ['-10','5','20','35','50','65','80','95','110'],
							minorTicks: 4,
							strokeTicks: false,
							highlights: [
								{ from: -10, to: 5, color: 'rgba(0,0,255,.15)' },
								{ from: 5, to: 20, color: 'rgba(0,0,100,.15)' },
								{ from: 20, to: 35, color: 'rgba(0,200,0,.25)' },
								{ from: 35, to: 50, color: 'rgba(0,100,0,.25)' },
								{ from: 50, to: 65, color: 'rgba(50,100,0,.15)' },
								{ from: 65, to: 80, color: 'rgba(100,100,0,.15)' },
								{ from: 80, to: 95, color: 'rgba(150,100,0,.25)' },
								{ from: 95, to: 110, color: 'rgba(200,100,0,.25)' },
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
	radial2.draw();

    }});
}

function draw_gauge_voltage(){
    $.ajax({url: "/voltage", success: function(result){
	div_html=""
	div_html+=new Date(result["date"]).toString()+"</br>"
	div_html+="<canvas id=\"gauge_voltage\"></canvas>";
    $("#draw_gauge_voltage").html(div_html);
    var radial1 = new RadialGauge({
							renderTo: 'gauge_voltage',
							width: 200,
							height: 200,
							units: 'V',
							title: "Battery",
							value: result["volt1"],
							minValue: 0,
							maxValue: 40,
							majorTicks: ['0','10','20','30','40'],
							minorTicks: 10,
							strokeTicks: true,
							highlights: [
								{ from: 0, to: 10, color: 'rgba(0,0,155,.15)' },
								{ from: 10, to: 20, color: 'rgba(0,255,255,.15)' },
								{ from: 20, to: 30, color: 'rgba(0,155,0,.15)' },
								{ from: 30, to: 40, color: 'rgba(255,30,0,.25)' }
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
	radial1.draw();
    }});
}

function draw_gauge_ac(){
    $.ajax({url: "/ac", success: function(result){
    div_html=""
    div_html+=new Date(result["date"]).toString()+"</br>"
    div_html+="<canvas id=\"gauge_ac_voltage\"></canvas>";
    div_html+="<canvas id=\"gauge_ac_current\"></canvas>";
    div_html+="<canvas id=\"gauge_ac_power\"></canvas>";
    div_html+="<canvas id=\"gauge_ac_energy\"></canvas>";
    $("#draw_gauge_ac").html(div_html);
    var radial1 = new RadialGauge({
                            renderTo: 'gauge_ac_voltage',
                            width: 200,
                            height: 200,
                            units: 'V',
                            title: "Voltage",
                            value: result["voltage"],
                            minValue: 0,
                            maxValue: 320,
                            majorTicks: ['0','80','160','240','320'],
                            minorTicks: 10,
                            strokeTicks: true,
                            highlights: [
                                { from: 0, to: 80, color: 'rgba(0,0,155,.15)' },
                                { from: 80, to: 160, color: 'rgba(0,255,255,.15)' },
                                { from: 160, to: 240, color: 'rgba(0,155,0,.15)' },
                                { from: 240, to: 320, color: 'rgba(255,30,0,.25)' }
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
    radial1.draw();
    
    var radial2 = new RadialGauge({
                            renderTo: 'gauge_ac_current',
                            width: 200,
                            height: 200,
                            units: 'A',
                            title: "Current",
                            value: result["current"],
                            minValue: 0,
                            maxValue: 4,
                            majorTicks: ['0','1','2','3','4'],
                            minorTicks: 10,
                            strokeTicks: true,
                            highlights: [
                                { from: 0, to: 1, color: 'rgba(0,0,155,.15)' },
                                { from: 1, to: 2, color: 'rgba(0,255,255,.15)' },
                                { from: 2, to: 3, color: 'rgba(0,155,0,.15)' },
                                { from: 3, to: 4, color: 'rgba(255,30,0,.25)' }
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
    radial2.draw();
    
    var radial3 = new RadialGauge({
                            renderTo: 'gauge_ac_power',
                            width: 200,
                            height: 200,
                            units: 'W',
                            title: "Power",
                            value: result["power"],
                            minValue: 0,
                            maxValue: 600,
                            majorTicks: ['0','100','200','300','400','500','600'],
                            minorTicks: 10,
                            strokeTicks: true,
                            highlights: [
                                { from: 0, to: 100, color: 'rgba(0,0,155,.15)' },
                                { from: 100, to: 200, color: 'rgba(0,255,255,.15)' },
                                { from: 200, to: 300, color: 'rgba(0,155,0,.15)' },
                                { from: 300, to: 400, color:  'rgba(255,230,0,.25)'},
                                { from: 400, to: 500, color: 'rgba(255,100,0,.25)' },
                                { from: 500, to: 600, color: 'rgba(255,30,0,.25)' }
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
    radial3.draw();    
    
    energy_val=result["energy"]/1000
    floor_energy_val=Math.floor(energy_val/1000)*1000
    var radial4 = new RadialGauge({
                            renderTo: 'gauge_ac_energy',
                            width: 200,
                            height: 200,
                            units: 'KWh',
                            title: "Energy",
                            value: result["energy"]/1000,
                            minValue: floor_energy_val,
                            maxValue: floor_energy_val+1000,
                            majorTicks: [floor_energy_val,floor_energy_val+200,floor_energy_val+400,floor_energy_val+600,floor_energy_val+800,floor_energy_val+1000],
                            minorTicks: 10,
                            strokeTicks: true,
                            highlights: [
                                { from: floor_energy_val, to: floor_energy_val+200, color: 'rgba(0,0,155,.15)' },
                                { from: floor_energy_val+200, to: floor_energy_val+400, color: 'rgba(0,255,255,.15)' },
                                { from: floor_energy_val+400, to: floor_energy_val+600, color: 'rgba(0,155,0,.15)' },
                                { from: floor_energy_val+600, to: floor_energy_val+800, color: 'rgba(255,230,0,.25)' },
                                { from: floor_energy_val+800, to: floor_energy_val+1000, color: 'rgba(255,30,0,.25)' }
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
    radial4.draw();
    
    }});
}


function draw_graph(){
    items=$("#items_interval").val()
    
    url_temp="/home_station/temperature_data?items="+items
    url_volt="/home_station/voltage_data?items="+items

    data_array=[]

    data_array[0]={type:"line",
            axisYType: "secondary",
            name: "Temperature1",
            showInLegend: true,
            markerSize: 0,
            dataPoints: []}

    data_array[1]={type:"line",
            axisYType: "secondary",
            name: "Temperature2",
            showInLegend: true,
            markerSize: 0,
            dataPoints: []}

    data_array[2]={type:"line",
            axisYType: "secondary",
            name: "Voltage1",
            showInLegend: true,
            markerSize: 0,
            dataPoints: []}

    var chart = new CanvasJS.Chart("graph", {
                    animationEnabled: true,
                    title:{ text: "Measurements"},
                    toolTip: {
                        shared: true,
                        contentFormatter: function(e){
                            //console.log(e.entries)
                            var str = "";
                            str = str.concat(e.entries[0].dataPoint.x);
                            str = str.concat("</br>");
                            for (var i = 0; i < e.entries.length; i++){
                                var  temp = "<div style=\"color: "+e.entries[i].dataSeries.color+";\">"+e.entries[i].dataSeries.name + " <strong>"+  e.entries[i].dataPoint.y + "</strong></div>" ; 
                                str = str.concat(temp);
                            }
                        return (str);
                        }
                    },
                    legend: {
                        horizontalAlign: "left", // "center" , "right"
                        verticalAlign: "top", //"center", "bottom"
                        fontSize: 15
                        },
                    axisX:{  
                        valueFormatString: "DD MMM HH:mm"
                    },
                    axisY:{includeZero: true},
                    data:eval(data_array)
                });

    chart["data"]=eval(data_array)
    
    if(temp_opt["temp1"]["checked"] || temp_opt["temp2"]["checked"])        
    $.ajax({url: url_temp, success: function(result){
	    result=JSON.parse(result)
	    result.forEach(function(item){
		  if(item["temp1"]!=-127 && temp_opt["temp1"]["checked"])
			data_array[0]["dataPoints"].push({x:new Date(item["date"]),y:item["temp1"]})
		  if(item["temp2"]!=-127 && temp_opt["temp2"]["checked"])
			data_array[1]["dataPoints"].push({x:new Date(item["date"]),y:item["temp2"]})
	       })
	    chart["data"][0]=eval(data_array)[0]
	    chart["data"][1]=eval(data_array)[1]
	    chart.render();
	}});
	
	if(volt_opt["volt1"]["checked"])
    $.ajax({url: url_volt, success: function(result){
        result=JSON.parse(result)
        result.forEach(function(item){
                if(volt_opt["volt1"]["checked"])
                    data_array[2]["dataPoints"].push({x:new Date(item["date"]),y:item["volt1"]})
        })
        chart["data"][2]=eval(data_array)[2]
        chart.render();
        }});    
    }
    
    
function draw_graph_ac(){
    items=$("#items_interval_ac").val()
    
    url_ac="/home_station/ac_data?items="+items
    
    data_array=[]

    data_array[0]={type:"line",
            axisYType: "secondary",
            name: "Voltage",
            showInLegend: true,
            markerSize: 0,
            dataPoints: []}

    data_array[1]={type:"line",
            axisYType: "secondary",
            name: "Current",
            showInLegend: true,
            markerSize: 0,
            dataPoints: []}

    data_array[2]={type:"line",
            axisYType: "secondary",
            name: "Power",
            showInLegend: true,
            markerSize: 0,
            dataPoints: []}
            
    data_array[3]={type:"line",
            axisYType: "secondary",
            name: "Energy",
            showInLegend: true,
            markerSize: 0,
            dataPoints: []}
    
    data_array[4]={type:"column",
            axisYType: "secondary",
            name: "Energy Daily",
            showInLegend: true,
            markerSize: 0,
            dataPoints: []}
    
    data_array[5]={type:"column",
            axisYType: "secondary",
            name: "Energy Hourly",
            showInLegend: true,
            markerSize: 0,
            dataPoints: []}
            
    data_array[6]={type:"line",
            axisYType: "secondary",
            name: "Energy between Samples",
            showInLegend: true,
            markerSize: 0,
            dataPoints: []}

    var chart = new CanvasJS.Chart("graph", {
                    animationEnabled: true,
                    title:{ text: "Measurements"},
                    toolTip: {
                        shared: true,
                        contentFormatter: function(e){
                            //console.log(e.entries)
                            var str = "";
                            str = str.concat(e.entries[0].dataPoint.x);
                            str = str.concat("</br>");
                            for (var i = 0; i < e.entries.length; i++){
                                var  temp = "<div style=\"color: "+e.entries[i].dataSeries.color+";\">"+e.entries[i].dataSeries.name + " <strong>"+  e.entries[i].dataPoint.y + "</strong></div>" ; 
                                str = str.concat(temp);
                            }
                        return (str);
                        }
                    },
                    legend: {
                        horizontalAlign: "left", // "center" , "right"
                        verticalAlign: "top", //"center", "bottom"
                        fontSize: 15
                        },
                    axisX:{  
                        valueFormatString: "DD MMM HH:mm"
                    },
                    axisY:{includeZero: true},
                    data:eval(data_array)
                });

    chart["data"]=eval(data_array)
    //console.log(chart["data"])
    //console.log(ac_opt)
    if(ac_opt["voltage"]["checked"] || ac_opt["current"]["checked"]||ac_opt["power"]["checked"] || ac_opt["energy"]["checked"] || ac_opt["energyday"]["checked"] || ac_opt["energyhour"]["checked"] || ac_opt["energysample"]["checked"])        
    $.ajax({url: url_ac, success: function(result){
        result=JSON.parse(result)
        
        sample_energy=[]
        daily_energy=[]
        hourly_energy=[]
        
        result.forEach(function(item){
            d=new Date(item["date"])
            if(ac_opt["voltage"]["checked"])
                data_array[0]["dataPoints"].push({x:d,y:item["voltage"]})
            if(ac_opt["current"]["checked"])
                data_array[1]["dataPoints"].push({x:d,y:item["current"]})
            if(ac_opt["power"]["checked"])
                data_array[2]["dataPoints"].push({x:d,y:item["power"]})
            if(ac_opt["energy"]["checked"])
                data_array[3]["dataPoints"].push({x:d,y:item["energy"]/1000})
            
            if(ac_opt["energysample"]["checked"])
            if(sample_energy.length==0)
                sample_energy.push({x:new Date(item["date"]),y:item["energy"]})
            else{
                sample_energy[sample_energy.length-1].y=item["energy"]-sample_energy[sample_energy.length-1].y
                sample_energy[sample_energy.length-1].x=new Date(item["date"])
                sample_energy.push({x:new Date(item["date"]),y:item["energy"]})}
                
            if(ac_opt["energyday"]["checked"])
            if(daily_energy.length==0)
                daily_energy.push({x:new Date(item["date"]),y:item["energy"]})
            else if(daily_energy[daily_energy.length-1].x.getDate()!=d.getDate()){
                daily_energy[daily_energy.length-1].y=item["energy"]-daily_energy[daily_energy.length-1].y
                daily_energy[daily_energy.length-1].x=new Date(item["date"])
                daily_energy.push({x:new Date(item["date"]),y:item["energy"]})}
            
            if(ac_opt["energyhour"]["checked"])    
            if(hourly_energy.length==0)
                hourly_energy.push({x:new Date(item["date"]),y:item["energy"]})
            else if(hourly_energy[hourly_energy.length-1].x.getDate()!=d.getDate()||hourly_energy[hourly_energy.length-1].x.getHours()!=d.getHours()){
                hourly_energy[hourly_energy.length-1].y=item["energy"]-hourly_energy[hourly_energy.length-1].y
                hourly_energy[hourly_energy.length-1].x=new Date(item["date"])
                hourly_energy.push({x:new Date(item["date"]),y:item["energy"]})}            
            
           });
        
        last_item=result[result.length-1]
        
         if(ac_opt["energysample"]["checked"]&&sample_energy.length!=0){
            lt=sample_energy.pop()
            last_sample=sample_energy[sample_energy.length-1]
            sample_energy.push({x:new Date(lt["x"]),y:(last_sample["y"])})
            //console.log("last_sample ")
            //console.log(sample_energy)
            }
        
         if(ac_opt["energyday"]["checked"]&&daily_energy.length!=0){
            lt=daily_energy.pop()
            last_daily=daily_energy[daily_energy.length-1]
            daily_energy.push({x:new Date(lt["x"]),y:(last_daily["y"])})
            daily_energy.push({x:new Date(last_item["date"]),y:(last_item["energy"]-lt["y"])})
            //console.log("last_daily ")
            //console.log(daily_energy)
            }
         if(ac_opt["energyhour"]["checked"]&&hourly_energy.length!=0){
            lt=hourly_energy.pop()
            last_hourly=hourly_energy[hourly_energy.length-1]
            hourly_energy.push({x:new Date(lt["x"]),y:(last_hourly["y"])})
            hourly_energy.push({x:new Date(last_item["date"]),y:(last_item["energy"]-lt["y"])})
            //console.log("last_hourly ")
            //console.log(hourly_energy)
            }
        
        //console.log(last_item)
        //console.log(daily_energy)
        //console.log(hourly_energy)
        
        data_array[4]["dataPoints"]=daily_energy
        data_array[5]["dataPoints"]=hourly_energy
        data_array[6]["dataPoints"]=sample_energy
        
        chart["data"][0]=eval(data_array)[0]
        chart["data"][1]=eval(data_array)[1]
        chart["data"][2]=eval(data_array)[2]
        chart["data"][3]=eval(data_array)[3]
        chart["data"][4]=eval(data_array)[4]
        chart["data"][5]=eval(data_array)[5]
        
        chart.render();
    }});  
    
    
    }
	