
function init(){
	draw_gauge_temperature();
	draw_gauge_voltage();
	draw_graph();
	setInterval(function(){ draw_gauge_temperature();
							draw_gauge_voltage();
							draw_graph();
							}, 30000);
}

function force_refresh(){
$.ajax({url: "/force_poll", success: function(result){
	draw_gauge_temperature();
	draw_gauge_voltage();
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
	console.log(result)
    //result=JSON.parse(result)
	div_html=""
	div_html+=new Date(result["date"]).toString()+"</br>"
	div_html+="<canvas id=\"gauge_voltage\"></canvas>";
    $("#draw_gauge_voltage").html(div_html);
    var radial1 = new RadialGauge({
							renderTo: 'gauge_voltage',
							width: 200,
							height: 200,
							units: 'V',
							title: false,
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

function draw_graph(){
items=$("#items_interval").val()
//if(!Number.isInteger(items))
//	return;
//console.log(items)
url="/home_station/data?items="+items
$.ajax({url: url, success: function(result){
	//console.log(result)
    result=JSON.parse(result)
	data=[]
	data.push({type:"line",
			axisYType: "secondary",
			name: "Temperature1",
			showInLegend: true,
			markerSize: 0,
			dataPoints: []})
	data.push({type:"line",
			axisYType: "secondary",
			name: "Temperature2",
			showInLegend: true,
			markerSize: 0,
			dataPoints: []})
	data.push({type:"line",
			axisYType: "secondary",
			name: "Voltage1",
			showInLegend: true,
			markerSize: 0,
			dataPoints: []})
	result.forEach(function(item){
		//console.log(item["date"])
		data[0]["dataPoints"].push({x:new Date(item["date"]),y:item["temp1"]})
		data[1]["dataPoints"].push({x:new Date(item["date"]),y:item["temp2"]})
		data[2]["dataPoints"].push({x:new Date(item["date"]),y:item["volt1"]})
		
	})
    var chart = new CanvasJS.Chart("graph", {
					animationEnabled: true,
					title:{	text: "Measurements"},
					toolTip: {
						shared: true,
						contentFormatter: function(e){
							console.log(e.entries)
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
						valueFormatString: "DD MMM YYYY HH : mm"
					},
					axisY:{includeZero: true},
					data:eval(data)
				});
				chart.render();
    }});
}
	