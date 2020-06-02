
function init(){
	draw_gauge_temperature();
	draw_gauge_voltage();
	setInterval(function(){ draw_gauge_temperature();
							draw_gauge_voltage();}, 30000);
}
function draw_gauge_temperature(){
$.ajax({url: "/temperature", success: function(result){
	console.log(result)
    //result=JSON.parse(result)
	div_html=""
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
							maxValue: 120,
							majorTicks: ['-10','20','60','90','120'],
							minorTicks: 2,
							strokeTicks: false,
							highlights: [
								{ from: -10, to: 20, color: 'rgba(0,255,0,.15)' },
								{ from: 20, to: 60, color: 'rgba(255,255,0,.15)' },
								{ from: 60, to: 90, color: 'rgba(255,30,0,.25)' },
								{ from: 90, to: 120, color: 'rgba(255,0,225,.25)' },
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
							maxValue: 120,
							majorTicks: ['-10','20','60','90','120'],
							minorTicks: 2,
							strokeTicks: false,
							highlights: [
								{ from: -10, to: 20, color: 'rgba(0,255,0,.15)' },
								{ from: 20, to: 60, color: 'rgba(255,255,0,.15)' },
								{ from: 60, to: 90, color: 'rgba(255,30,0,.25)' },
								{ from: 90, to: 120, color: 'rgba(255,0,225,.25)' },
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
							maxValue: 50,
							majorTicks: ['0','20','40','50'],
							minorTicks: 2,
							strokeTicks: false,
							highlights: [
								{ from: 0, to: 20, color: 'rgba(0,255,0,.15)' },
								{ from: 20, to: 40, color: 'rgba(255,255,0,.15)' },
								{ from: 40, to: 50, color: 'rgba(255,30,0,.25)' }
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