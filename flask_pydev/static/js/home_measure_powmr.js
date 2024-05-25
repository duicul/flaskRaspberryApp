    var blade_length = 1;
    var temp_opt = {
        "temp1": {
            "name": "Temperature1 [C]",
            "checked": true,
            
        },
        "temp1_grad": {
            "name": "Temperature1 change [C]",
            "checked": false,
            "type":"stepArea"
        },
        "temp2": {
            "name": "Temperature2 [C]",
            "checked": true,
            "type":"line"
        },
        "temp2_grad": {
            "name": "Temperature2 change [C]",
            "checked": false,
            "type":"stepArea"
        },
        "temp_out": {
            "name": "Temperature outside [C]",
            "checked": true,
            "type":"line"
        },
        "humid_out": {
            "name": "Humidity Outside [%]",
            "checked": false,
            "type":"line"
        },
        "wind_speed": {
            "name": "Wind Speed [m/s]",
            "checked": false,
            "type":"line"
        },
        "wind_power": {
            "name": ("Wind power [w] " + blade_length + " m"),
            "checked": false,
            "type":"line"
        }
    };


    var volt_opt = {
        "volt1": {
            "name": "Voltage DC [V]",
            "checked": false,
            "type":"line"
        }
    };
    var ac_opt = {
        "voltage": {
            "name": "Voltage AC [V]",
            "checked": false,
            "type":"line"
        },
        "current": {
            "name": "Current AC [A]",
            "checked": false,
            "type":"line"
        },
        "power": {
            "name": "Power [W]",
            "checked": false,
            "type":"line"
        },
        "power_average": {
            "name": "Power Average [W]",
            "checked": false,
            "type":"line"
        },
        "energy": {
            "name": "Energy [KWh]",
            "checked": false,
            "type":"line"
        },
        "energyday": {
            "name": "Energy Daily [Wh]",
            "checked": false,
            "type":"column"
        },
        "energyhour": {
            "name": "Energy Hourly [Wh]",
            "checked": false,
            "type":"column"
        },
        "energysample": {
            "name": "Energy between Samples [Wh]",
            "checked": false,
            "type":"line"
        },
        "energymonth": {
            "name": "Energy Monthly [KWh]",
            "checked": false,
            "type":"column"
        }
    };
    
    var ac_powmr_opt={
        "energyhour": {
            "name": "Energy Hourly [Wh]",
            "checked": false,
            "type":"column"
        },
        "energyday": {
            "name": "Energy Daily [Wh]",
            "checked": false,
            "type":"column"
        },
        "energyweek": {
            "name": "Energy Weekly [Wh]",
            "checked": false,
            "type":"column"
        },
        "energymonth": {
            "name": "Energy Monthly [KWh]",
            "checked": false,
            "type":"column"
        },
        "energyyear": {
            "name": "Energy Yearly [KWh]",
            "checked": false,
            "type":"column"
        }
    };
    
    var ac_opt_powmr ={};
    var ac_skip = ['bms_01cell_voltage', 'bms_02cell_voltage', 'bms_03cell_voltage', 'bms_04cell_voltage', 'bms_05cell_voltage', 'bms_06cell_voltage', 'bms_07cell_voltage', 'bms_08cell_voltage', 'bms_09cell_voltage', 'bms_10cell_voltage', 'bms_10cell_voltage', 'bms_11cell_voltage', 'bms_12cell_voltage', 'bms_13cell_voltage', 'bms_14cell_voltage', 'bms_15cell_voltage', 'bms_16cell_voltage'];
    var energy_cols = ['load_energy_total','pv_energy_total','t0026_total_energy_total'];
    function show_opt() {
        data = "";
        return;
        checked = temp_opt["temp_out"]["checked"] == true ? "checked=\"checked\"" : "";
        data += "<input type=\"checkbox\" " + checked + " onchange=\"check_state('temp_out',1,this)\">";
        data += "<label>" + temp_opt["temp_out"]["name"] + "</label></br>";

        checked = temp_opt["humid_out"]["checked"] == true ? "checked=\"checked\"" : "";
        data += "<input type=\"checkbox\" " + checked + " onchange=\"check_state('humid_out',1,this)\">";
        data += "<label>" + temp_opt["humid_out"]["name"] + "</label></br>";

        checked = temp_opt["wind_speed"]["checked"] == true ? "checked=\"checked\"" : "";
        data += "<input type=\"checkbox\" " + checked + " onchange=\"check_state('wind_speed',1,this)\">";
        data += "<label>" + temp_opt["wind_speed"]["name"] + "</label></br>";

        data += "Blade length: <input type=\"number\" id=\"blade_length\" step=\"0.01\"><br/>";

        checked = temp_opt["wind_power"]["checked"] == true ? "checked=\"checked\"" : "";
        data += "<input type=\"checkbox\" " + checked + " onchange=\"check_state('wind_power',1,this)\">";
        data += "<label>" + temp_opt["wind_power"]["name"] + "</label></br>";

        checked = temp_opt["temp1"]["checked"] == true ? "checked=\"checked\"" : "";
        data += "<input type=\"checkbox\" " + checked + " onchange=\"check_state('temp',1,this)\">";
        data += "<label>" + temp_opt["temp1"]["name"] + "</label></br>";

        checked = temp_opt["temp1_grad"]["checked"] == true ? "checked=\"checked\"" : "";
        data += "<input type=\"checkbox\" " + checked + " onchange=\"check_state('temp_grad',1,this)\">";
        data += "<label>" + temp_opt["temp1_grad"]["name"] + "</label></br>";

        checked = temp_opt["temp2"]["checked"] == true ? "checked=\"checked\"" : "";
        data += "<input type=\"checkbox\" " + checked + " onchange=\"check_state('temp',2,this)\">";
        data += "<label>" + temp_opt["temp2"]["name"] + "</label></br>";

        checked = temp_opt["temp2_grad"]["checked"] == true ? "checked=\"checked\"" : "";
        data += "<input type=\"checkbox\" " + checked + " onchange=\"check_state('temp_grad',2,this)\">";
        data += "<label>" + temp_opt["temp2_grad"]["name"] + "</label></br>";

        checked = volt_opt["volt1"]["checked"] == true ? "checked=\"checked\"" : "";
        data += "<input type=\"checkbox\" " + checked + " onchange=\"check_state('volt',1,this)\">";
        data += "<label>" + volt_opt["volt1"]["name"] + "</label></br>";

        $("#temp_volt_opt").html(data);
        $("#blade_length").val(blade_length);
        $("#blade_length").change(function() {
            blade_length = parseFloat($("#blade_length").val());
        });
    }

    function show_opt_ac() {


        $.ajax({
            url: "/home_station/powmr_cols",
            success: function(result) {
                data = "";
                
                for (var i = 0; i < result.length; i++) {
                    col = result[i];
                    //console.log(col);
                    if (col.type == "REAL" && !ac_skip.includes(col.name)) {
                        checked = false;
                        data += "<input type=\"checkbox\" " + checked + " onchange=\"check_state_ac('" + col.name + "',this)\">";
                        data += "<label>" + col.name + "</label></br>";
                    }

                }
                ac_powmr_opt_keys = Object.keys(ac_powmr_opt);
                for (var i1 = 0; i1 < ac_powmr_opt_keys.length; i1++) {
                    key = ac_powmr_opt_keys[i1];
                    col=ac_powmr_opt[key];
                    //console.log(col);
                    checked = false;
                        data += "<input type=\"checkbox\" " + checked + " onchange=\"check_state_ac_energy('" + key + "',this)\">";
                        data += "<label>" + col.name + "</label></br>";
                    

                }
                //console.log(result);
                //console.log("data "+data);
                $("#ac_opt").html(data);
            }
        });

    }

    function check_state(type, index, elem) {
        if (type == "temp_out")
            temp_opt["temp_out"]["checked"] = elem.checked
        if (type == "humid_out")
            temp_opt["humid_out"]["checked"] = elem.checked
        if (type == "wind_speed")
            temp_opt["wind_speed"]["checked"] = elem.checked
        if (type == "wind_power")
            temp_opt["wind_power"]["checked"] = elem.checked
        if (type == "temp") {
            if (index == 1)
                temp_opt["temp1"]["checked"] = elem.checked
            else if (index == 2)
                temp_opt["temp2"]["checked"] = elem.checked
        } else if (type == "temp_grad") {
            if (index == 1)
                temp_opt["temp1_grad"]["checked"] = elem.checked
            else if (index == 2)
                temp_opt["temp2_grad"]["checked"] = elem.checked
        } else if (type == "volt") {
            if (index == 1)
                volt_opt["volt1"]["checked"] = elem.checked
        }
        //console.log(temp_opt)
        //console.log(volt_opt)
    }

    function check_state_ac(type, elem) {
        if (ac_opt_powmr[type] == undefined)
            ac_opt_powmr[type] = {};
        ac_opt_powmr[type]["checked"] = elem.checked;
        console.log(ac_opt_powmr)
    }
    
    function check_state_ac_energy(type, elem) {
        if (ac_powmr_opt[type] == undefined)
            ac_powmr_opt[type] = {};
        ac_powmr_opt[type]["checked"] = elem.checked;
        console.log(ac_powmr_opt)
    }

    function init() {
        draw_gauge_temperature();
        draw_gauge_voltage();
        draw_gauge_ac();
        //draw_graph_all();
        show_opt();
        show_opt_ac();
        draw_weather();
        display_rpi_data();
        /*setInterval(function(){ draw_gauge_temperature();
    							draw_gauge_voltage();
    							draw_gauge_ac()
    							draw_weather();
    							//draw_graph();
    							}, 300000);
    	setInterval(function(){ display_rpi_data();
                                }, 60000);*/
    }

    function force_refresh() {
        $.ajax({
            url: "/force_poll",
            success: function(result) {
                draw_gauge_temperature();
                draw_gauge_voltage();
                draw_gauge_ac();
                draw_graph();
            }
        });
    }

    function draw_gauge_temperature() {
        $.ajax({
            url: "/temperature",
            success: function(result) {
                //result=JSON.parse(result)

                //console.log(result)

                //console.log(result[0]["date"])
                //console.log(result[1]["date"])
                div_html = ""
                div_html += "Temperature " + result[0]["temp_id"] + " : " + new Date(result[0]["date"]).toString() + "</br>"
                div_html += "Temperature " + result[1]["temp_id"] + " : " + new Date(result[1]["date"]).toString() + "</br>"
                div_html += "<canvas id=\"gauge_temp_1\"></canvas>";
                div_html += "<canvas id=\"gauge_temp_2\"></canvas>";
                $("#draw_gauge_temperature").html(div_html);
                var radial1 = new RadialGauge({
                    renderTo: 'gauge_temp_1',
                    width: 200,
                    height: 200,
                    units: 'C',
                    title: "Temperature " + result[0]["temp_id"],
                    value: result[0]["temp"],
                    minValue: -10,
                    maxValue: 110,
                    majorTicks: ['-10', '5', '20', '35', '50', '65', '80', '95', '110'],
                    minorTicks: 4,
                    strokeTicks: false,
                    highlights: [{
                        from: -10,
                        to: 5,
                        color: 'rgba(0,0,255,.15)'
                    }, {
                        from: 5,
                        to: 20,
                        color: 'rgba(0,0,100,.15)'
                    }, {
                        from: 20,
                        to: 35,
                        color: 'rgba(0,200,0,.25)'
                    }, {
                        from: 35,
                        to: 50,
                        color: 'rgba(0,100,0,.25)'
                    }, {
                        from: 50,
                        to: 65,
                        color: 'rgba(50,100,0,.15)'
                    }, {
                        from: 65,
                        to: 80,
                        color: 'rgba(100,100,0,.15)'
                    }, {
                        from: 80,
                        to: 95,
                        color: 'rgba(150,100,0,.25)'
                    }, {
                        from: 95,
                        to: 110,
                        color: 'rgba(200,100,0,.25)'
                    }, ],
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
                    title: "Temperature " + result[1]["temp_id"],
                    value: result[1]["temp"],
                    minValue: -10,
                    maxValue: 110,
                    majorTicks: ['-10', '5', '20', '35', '50', '65', '80', '95', '110'],
                    minorTicks: 4,
                    strokeTicks: false,
                    highlights: [{
                        from: -10,
                        to: 5,
                        color: 'rgba(0,0,255,.15)'
                    }, {
                        from: 5,
                        to: 20,
                        color: 'rgba(0,0,100,.15)'
                    }, {
                        from: 20,
                        to: 35,
                        color: 'rgba(0,200,0,.25)'
                    }, {
                        from: 35,
                        to: 50,
                        color: 'rgba(0,100,0,.25)'
                    }, {
                        from: 50,
                        to: 65,
                        color: 'rgba(50,100,0,.15)'
                    }, {
                        from: 65,
                        to: 80,
                        color: 'rgba(100,100,0,.15)'
                    }, {
                        from: 80,
                        to: 95,
                        color: 'rgba(150,100,0,.25)'
                    }, {
                        from: 95,
                        to: 110,
                        color: 'rgba(200,100,0,.25)'
                    }, ],
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

            }
        });
    }

    function draw_weather() {
        $.ajax({
            url: "/weather",
            success: function(result) {
                //console.log(result)
                const weather_data = result;
                //console.log(weather_data)
                html_val = "<div class=\"row\">"
                html_val += "<div class=\"col-md-2\">"
                html_val += "<img src=\"" + weather_data["current"]["condition"]["icon"] + "\" /><br/>"
                html_val += "</div>"
                html_val += "<div class=\"col-md-3\">"
                html_val += "Temp : " + weather_data["current"]["temp_c"] + " &#8451; <br/>"
                html_val += "Feels like : " + weather_data["current"]["feelslike_c"] + " &#8451; <br/>"
                html_val += "Humidity : " + weather_data["current"]["humidity"] + " % <br/>"
                html_val += "Wind : " + weather_data["current"]["wind_kph"] + " km/h " + weather_data["current"]["wind_dir"] + " <br/>"
                html_val += "Clouds : " + weather_data["current"]["cloud"] + " % <br/>";
                html_val += "</div>"
                html_val += "<div class=\"col-md-7\">"
                html_val += "City : " + weather_data["location"]["name"] + "<br/>"
                html_val += "</div></div>"
                $("#weather_status").html(html_val);
            }
        });
    }

    function draw_gauge_voltage() {
        $.ajax({
            url: "/voltage",
            success: function(result) {

                //console.log(result);

                //console.log(result["date"]);
                div_html = ""
                div_html += new Date(result["date"]).toString() + "</br>"
                div_html += "<canvas id=\"gauge_voltage\"></canvas>";
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
                    majorTicks: ['0', '10', '20', '30', '40'],
                    minorTicks: 10,
                    strokeTicks: true,
                    highlights: [{
                        from: 0,
                        to: 10,
                        color: 'rgba(0,0,155,.15)'
                    }, {
                        from: 10,
                        to: 20,
                        color: 'rgba(0,255,255,.15)'
                    }, {
                        from: 20,
                        to: 30,
                        color: 'rgba(0,155,0,.15)'
                    }, {
                        from: 30,
                        to: 40,
                        color: 'rgba(255,30,0,.25)'
                    }],
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
            }
        });
    }

    function draw_gauge_ac() {
        $.ajax({
            url: "/powmr",
            success: function(result) {
                //console.log(result);
                //console.log(result["date"]);
                div_html = ""
                div_html += new Date(result["TIMESTAMP"]).toString() + "</br>"
                div_html += "<canvas id=\"pv_power\"></canvas>";
                div_html += "<canvas id=\"load_watt\"></canvas>";
                div_html += "<canvas id=\"t0026\"></canvas>";
                div_html += "<canvas id=\"battery_voltage\"></canvas>";
                div_html += "<canvas id=\"batt_charge_current\"></canvas>";
                div_html += "<canvas id=\"pv_current\"></canvas>";
                div_html += "<canvas id=\"pv_voltage\"></canvas>";
                $("#draw_gauge_ac").html(div_html);
                var radial1 = new RadialGauge({
                    renderTo: 'pv_power',
                    width: 200,
                    height: 200,
                    units: 'W',
                    title: "pv_power",
                    value: result["pv_power"],
                    minValue: 0,
                    maxValue: 6500,
                    majorTicks: ['0', '1000', '2000', '3000', '4000', '5000', '6000'],
                    minorTicks: 10,
                    strokeTicks: true,
                    highlights: [{
                        from: 0,
                        to: 1500,
                        color: 'rgba(0,0,155,.15)'
                    }, {
                        from: 1500,
                        to: 3000,
                        color: 'rgba(0,255,255,.15)'
                    }, {
                        from: 3000,
                        to: 4500,
                        color: 'rgba(0,155,0,.15)'
                    }, {
                        from: 4500,
                        to: 6000,
                        color: 'rgba(255,30,0,.25)'
                    }],
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
                    renderTo: 'load_watt',
                    width: 200,
                    height: 200,
                    units: 'W',
                    title: "load_watt",
                    value: result["load_watt"],
                    minValue: 0,
                    maxValue: 5000,
                    majorTicks: ['0', '1000', '2000', '3000', '4000', '5000'],
                    minorTicks: 10,
                    strokeTicks: true,
                    highlights: [{
                        from: 0,
                        to: 1250,
                        color: 'rgba(0,0,155,.15)'
                    }, {
                        from: 1250,
                        to: 2500,
                        color: 'rgba(0,255,255,.15)'
                    }, {
                        from: 2500,
                        to: 3750,
                        color: 'rgba(0,155,0,.15)'
                    }, {
                        from: 3750,
                        to: 5000,
                        color: 'rgba(255,30,0,.25)'
                    }],
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
                    renderTo: 't0026',
                    width: 200,
                    height: 200,
                    units: 'W',
                    title: "TotalPower",
                    value: result["t0026"],
                    minValue: 0,
                    maxValue: 6500,
                    majorTicks: ['0', '1000', '2000', '3000', '4000', '5000', '6000'],
                    minorTicks: 10,
                    strokeTicks: true,
                    highlights: [{
                        from: 0,
                        to: 1000,
                        color: 'rgba(0,0,155,.15)'
                    }, {
                        from: 1000,
                        to: 2000,
                        color: 'rgba(0,255,255,.15)'
                    }, {
                        from: 2000,
                        to: 3000,
                        color: 'rgba(0,155,0,.15)'
                    }, {
                        from: 3000,
                        to: 4000,
                        color: 'rgba(255,230,0,.25)'
                    }, {
                        from: 4000,
                        to: 5000,
                        color: 'rgba(255,100,0,.25)'
                    }, {
                        from: 5000,
                        to: 6000,
                        color: 'rgba(255,30,0,.25)'
                    }],
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

                var radial4 = new RadialGauge({
                    renderTo: 'battery_voltage',
                    width: 200,
                    height: 200,
                    units: 'V',
                    title: "battery_voltage",
                    value: result["battery_voltage"],
                    minValue: 0,
                    maxValue: 40,
                    majorTicks: [0, 5, 10, 15, 20, 25, 30, 35],
                    minorTicks: 5,
                    strokeTicks: true,
                    highlights: [{
                        from: 0,
                        to: 7,
                        color: 'rgba(0,0,155,.15)'
                    }, {
                        from: 7,
                        to: 14,
                        color: 'rgba(0,255,255,.15)'
                    }, {
                        from: 14,
                        to: 21,
                        color: 'rgba(0,155,0,.15)'
                    }, {
                        from: 21,
                        to: 28,
                        color: 'rgba(255,230,0,.25)'
                    }, {
                        from: 28,
                        to: 35,
                        color: 'rgba(255,30,0,.25)'
                    }],
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

                var radial5 = new RadialGauge({
                    renderTo: 'batt_charge_current',
                    width: 200,
                    height: 200,
                    units: 'A',
                    title: "batt_charge_current",
                    value: result["batt_charge_current"],
                    minValue: 0,
                    maxValue: 150,
                    majorTicks: [0, 25, 50, 75, 100, 125, 150],
                    minorTicks: 5,
                    strokeTicks: true,
                    highlights: [{
                        from: 0,
                        to: 30,
                        color: 'rgba(0,0,155,.15)'
                    }, {
                        from: 30,
                        to: 60,
                        color: 'rgba(0,255,255,.15)'
                    }, {
                        from: 60,
                        to: 90,
                        color: 'rgba(0,155,0,.15)'
                    }, {
                        from: 90,
                        to: 120,
                        color: 'rgba(255,230,0,.25)'
                    }, {
                        from: 120,
                        to: 150,
                        color: 'rgba(255,30,0,.25)'
                    }],
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
                radial5.draw();

                var radial6 = new RadialGauge({
                    renderTo: 'pv_current',
                    width: 200,
                    height: 200,
                    units: 'A',
                    title: "pv_current",
                    value: result["pv_current"],
                    minValue: 0,
                    maxValue: 40,
                    majorTicks: [0, 5, 10, 15, 20, 25, 30, 35],
                    minorTicks: 5,
                    strokeTicks: true,
                    highlights: [{
                        from: 0,
                        to: 7,
                        color: 'rgba(0,0,155,.15)'
                    }, {
                        from: 7,
                        to: 14,
                        color: 'rgba(0,255,255,.15)'
                    }, {
                        from: 14,
                        to: 21,
                        color: 'rgba(0,155,0,.15)'
                    }, {
                        from: 21,
                        to: 28,
                        color: 'rgba(255,230,0,.25)'
                    }, {
                        from: 28,
                        to: 35,
                        color: 'rgba(255,30,0,.25)'
                    }],
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
                radial6.draw();

                var radial7 = new RadialGauge({
                    renderTo: 'pv_voltage',
                    width: 200,
                    height: 200,
                    units: 'V',
                    title: "pv_voltage",
                    value: result["pv_voltage"],
                    minValue: 0,
                    maxValue: 450,
                    majorTicks: [0, 50, 100, 150, 200, 250, 300, 350, 400, 450],
                    minorTicks: 10,
                    strokeTicks: true,
                    highlights: [{
                        from: 0,
                        to: 90,
                        color: 'rgba(0,0,155,.15)'
                    }, {
                        from: 90,
                        to: 180,
                        color: 'rgba(0,255,255,.15)'
                    }, {
                        from: 180,
                        to: 270,
                        color: 'rgba(0,155,0,.15)'
                    }, {
                        from: 270,
                        to: 360,
                        color: 'rgba(255,230,0,.25)'
                    }, {
                        from: 360,
                        to: 450,
                        color: 'rgba(255,30,0,.25)'
                    }],
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
                radial7.draw();

            }
        });
    }



    function draw_graph_all(interval, compare) {

        data_array = []

        /*data_array[0]={type:"line",
                axisYType: "secondary",
                name: "Temperature1 [C]",
                showInLegend: true,
                markerSize: 0,
                dataPoints: []}
    
        data_array[1]={type:"line",
                axisYType: "secondary",
                name: "Temperature2 [C]",
                showInLegend: true,
                markerSize: 0,
                dataPoints: []}
                
        data_array[2]={type:"stepArea",
                axisYType: "secondary",
                name: "Temperature1 change [C]",
                showInLegend: true,
                markerSize: 0,
                dataPoints: []}
        
        data_array[3]={type:"stepArea",
                axisYType: "secondary",
                name: "Temperature2 change [C]",
                showInLegend: true,
                markerSize: 0,
                dataPoints: []}
        
        
        data_array[4]={type:"line",
                axisYType: "secondary",
                name: "Temperature1 predicted [C]",
                showInLegend: true,
                markerSize: 0,
                dataPoints: []}
    
        data_array[5]={type:"line",
                axisYType: "secondary",
                name: "Temperature2 predicted [C]",
                showInLegend: true,
                markerSize: 0,
                dataPoints: []}
        
    
        data_array[6]={type:"line",
                axisYType: "secondary",
                name: "Voltage DC [V]",
                showInLegend: true,
                markerSize: 0,
                dataPoints: []}
        
        data_array[7]={type:"line",
                axisYType: "secondary",
                name: "Voltage AC [V]",
                showInLegend: true,
                markerSize: 0,
                dataPoints: []}
    
        data_array[8]={type:"line",
                axisYType: "secondary",
                name: "Current AC [A]",
                showInLegend: true,
                markerSize: 0,
                dataPoints: []}
    
        data_array[9]={type:"line",
                axisYType: "secondary",
                name: "Power [W]",
                showInLegend: true,
                markerSize: 0,
                dataPoints: []}
                
        data_array[10]={type:"line",
                axisYType: "secondary",
                name: "Energy [KWh]",
                showInLegend: true,
                markerSize: 0,
                dataPoints: []}
        
        data_array[11]={type:"column",
                axisYType: "secondary",
                name: "Energy Daily [Wh]",
                showInLegend: true,
                markerSize: 0,
                dataPoints: []}
        
        data_array[12]={type:"column",
                axisYType: "secondary",
                name: "Energy Hourly [Wh]",
                showInLegend: true,
                markerSize: 0,
                dataPoints: []}
                
        data_array[13]={type:"line",
                axisYType: "secondary",
                name: "Energy between Samples [Wh]",
                showInLegend: true,
                markerSize: 0,
                dataPoints: []}
        
        data_array[14]={type:"column",
                axisYType: "secondary",
                name: "Energy Monthly [KWh]",
                showInLegend: true,
                markerSize: 0,
                dataPoints: []}
        
        data_array[15]={type:"line",
                axisYType: "secondary",
                name: "Temperature outside [C]",
                showInLegend: true,
                markerSize: 0,
                dataPoints: []}
                
        data_array[16]={type:"line",
                axisYType: "secondary",
                name: "Humidity Outside [%]",
                showInLegend: true,
                markerSize: 0,
                dataPoints: []}
        
        data_array[17]={type:"line",
                axisYType: "secondary",
                name: "Wind Speed [m/s]",
                showInLegend: true,
                markerSize: 0,
                dataPoints: []}
        
        data_array[18]={type:"line",
                axisYType: "secondary",
                name: "Wind Power [W] - "+blade_length+" m",
                showInLegend: true,
                markerSize: 0,
                dataPoints: []}
        
        data_array[19]={type:"line",
                axisYType: "secondary",
                name: "Power Average [W]",
                showInLegend: true,
                markerSize: 0,
                dataPoints: []}*/

        /*chart = new CanvasJS.Chart("graph", {
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
                        data:[]//eval(data_array)
                    });*/
                    
                    
        //draw_graph(chart,data_array,interval,compare);
        draw_graph_ac(data_array, interval, compare);
    }

    function draw_graph(chart, data_array, interval, compare) {

        if (interval == true) {
            fdate = $("#fdate").val()
            ldate = $("#ldate").val()
            url_temp = "/home_station/temperature_data?fdate=" + fdate + "&ldate=" + ldate + "&interval=true";
            url_volt = "/home_station/voltage_data?fdate=" + fdate + "&ldate=" + ldate + "&interval=true";
        } else {
            if (compare == true) {
                date1 = $("#date1").val()
                date2 = $("#date2").val()
                url_temp = "/home_station/temperature_data?date1=" + date1 + "&date2=" + date1 + "&interval=false&compare=true";
                url_volt = "/home_station/voltage_data?date1=" + date1 + "&date2=" + date2 + "&interval=false&compare=true";
            } else {
                items = $("#items_interval").val()
                    //console.log(items)    
                url_temp = "/home_station/temperature_data?items=" + items + "&interval=false&compare=false";
                url_volt = "/home_station/voltage_data?items=" + items + "&interval=false&compare=false";
            }
        }


        //chart["data"]=eval(data_array)

        if (temp_opt["temp1"]["checked"] || temp_opt["temp2"]["checked"] || temp_opt["temp1_grad"]["checked"] || temp_opt["temp2_grad"]["checked"] || temp_opt["humid_out"]["checked"] || temp_opt["wind_speed"]["checked"] || temp_opt["wind_power"]["checked"] || temp_opt["temp_out"]["checked"])
            $.ajax({
                url: url_temp,
                success: function(result) {
                    result_rec = result["recorded"]
                    temp1_data = result_rec[1]
                    temp2_data = result_rec[2]
                    temp3_temp_out = result_rec[3]
                    temp4_humid_out = result_rec[4]
                    temp5_wind_speed = result_rec[5]
                    result_pred = result["predict"]
                    temp1_init = 0
                    temp1_date = null
                    temp2_init = 0
                    temp2_date = null
                        //console.log(result_rec)
                    temp1_data.forEach(function(item) {
                        if (item["value"] != -127) {
                            if (temp_opt["temp1"]["checked"])
                                data_array[0]["dataPoints"].push({
                                    x: new Date(item["date"]),
                                    y: item["value"]
                                })
                            if (temp_opt["temp1_grad"]["checked"]) {
                                if (temp1_date == null) {
                                    temp1_date = new Date(item["date"])
                                    temp1_init = item["value"]
                                } else {
                                    var diffMins = Math.round((((new Date(item["date"]) - temp1_init) % 86400000) % 3600000) / 60000);
                                    data_array[2]["dataPoints"].push({
                                        x: temp1_date,
                                        y: item["value"] - temp1_init /*/diffMins*/
                                    })
                                    temp1_date = new Date(item["date"])
                                    temp1_init = item["value"]
                                }
                            }
                        }
                    })
                    temp2_data.forEach(function(item) {
                        if (item["value"] != -127) {
                            if (temp_opt["temp2"]["checked"])
                                data_array[1]["dataPoints"].push({
                                    x: new Date(item["date"]),
                                    y: item["value"]
                                })
                            if (temp_opt["temp2_grad"]["checked"]) {
                                if (temp1_date == null) {
                                    temp1_date = new Date(item["date"])
                                    temp1_init = item["value"]
                                } else {
                                    var diffMins = Math.round((((new Date(item["date"]) - temp1_init) % 86400000) % 3600000) / 60000);
                                    data_array[3]["dataPoints"].push({
                                        x: temp1_date,
                                        y: item["value"] - temp1_init /*/diffMins*/
                                    })
                                    temp1_date = new Date(item["date"])
                                    temp1_init = item["value"]
                                }
                            }
                        }
                    })

                    if (temp_opt["temp_out"]["checked"])
                        temp3_temp_out.forEach(function(item) {
                            data_array[15]["dataPoints"].push({
                                x: new Date(item["date"]),
                                y: item["value"]
                            })
                        })

                    if (temp_opt["humid_out"]["checked"])
                        temp4_humid_out.forEach(function(item) {
                            data_array[16]["dataPoints"].push({
                                x: new Date(item["date"]),
                                y: item["value"]
                            })
                        })

                    if (temp_opt["wind_speed"]["checked"])
                        temp5_wind_speed.forEach(function(item) {
                            data_array[17]["dataPoints"].push({
                                x: new Date(item["date"]),
                                y: item["value"]
                            });
                        })

                    if (temp_opt["wind_power"]["checked"])
                        temp5_wind_speed.forEach(function(item) {
                            data_array[18]["dataPoints"].push({
                                x: new Date(item["date"]),
                                y: Math.PI / 2 * blade_length * blade_length * item["value"] * item["value"] * item["value"] * 1.2 * 0.4
                            })
                        })

                    result_pred.forEach(function(item) {
                            if (item["temp_id"] == 1 && item["temp"] != -127 && temp_opt["temp1"]["checked"])
                                if (item["temp_id"] == 2 && item["temp"] != -127 && temp_opt["temp2"]["checked"])
                                    data_array[5]["dataPoints"].push({
                                        x: new Date(item["date"]),
                                        y: item["temp2"]
                                    })
                        })
                        //console.log(data_array)
                    chart["data"] = eval(data_array)
                    chart.render();

                }
            });

        if (volt_opt["volt1"]["checked"])
            $.ajax({
                url: url_volt,
                success: function(result) {
                    result.forEach(function(item) {
                            if (volt_opt["volt1"]["checked"])
                                data_array[6]["dataPoints"].push({
                                    x: new Date(item["date"]),
                                    y: item["volt1"]
                                })
                        })
                        //console.log(data_array)
                    chart["data"] = eval(data_array)
                    chart.render();
                }
            });
    }


    function draw_graph_ac(data_array, interval, compare) {
        ac_powmr_opt_keys = Object.keys(ac_powmr_opt);
        ac_opt = []
        for (var i1 = 0; i1 < ac_powmr_opt_keys.length; i1++) {
            key = ac_powmr_opt_keys[i1];
            col=ac_powmr_opt[key];
            if(col.checked)
                ac_opt.push(key);
        }
        ac_opt_str = "";
        if(ac_opt.length>0){
            ac_opt_str="&energy_opt="+ac_opt.join(',')
        }
        
        if (interval == true) {
            fdate = $("#fdate").val()
            ldate = $("#ldate").val()
            url_ac = "/home_station/powmr_data?fdate=" + fdate + "&ldate=" + ldate + "&interval=true&compare=false"+ac_opt_str;
        } else {
            if (compare == true) {
                date1 = $("#date1").val()
                date2 = $("#date2").val()
                url_ac = "/home_station/powmr_data?date1=" + date1 + "&date2=" + date2 + "&interval=false&compare=true"+ac_opt_str;
            } else {
                items = $("#items_interval").val()
                    //console.log(items)
                url_ac = "/home_station/powmr_data?items=" + items + "&interval=false&compare=false"+ac_opt_str;
            }
        }
        //console.log(chart["data"])
        //console.log(ac_opt)
        //if(ac_opt["voltage"]["checked"] || ac_opt["current"]["checked"]||ac_opt["power"]["checked"] || ac_opt["energy"]["checked"] || ac_opt["energyday"]["checked"] || ac_opt["energyhour"]["checked"] || ac_opt["energysample"]["checked"] || ac_opt["power_average"]["checked"] || ac_opt["energymonth"]["checked"])        
        $.ajax({
            url: url_ac,
            success: function(result) {
                console.log(result);
                var showKeys = [],showKeys_energy=[];
                ac_opt_powmr_keys = Object.keys(ac_opt_powmr);
                ac_powmr_opt_keys = Object.keys(ac_powmr_opt);
                var graph_ind = 0;
                data_array_powmr = [];
                showkeys_graph_position = {}
                for (var i = 0; i < ac_opt_powmr_keys.length; i++) {
                    if (ac_opt_powmr[ac_opt_powmr_keys[i]].checked == true)
                        showKeys.push(ac_opt_powmr_keys[i])
                }
                
                for (var i = 0; i < ac_powmr_opt_keys.length; i++) {
                    if (ac_powmr_opt[ac_powmr_opt_keys[i]].checked == true)
                        showKeys_energy.push(ac_powmr_opt_keys[i])
                } 
                console.log(showKeys);
                for (var i = 0; i < showKeys.length; i++) {
                    data_array_powmr[i] = {
                        type: "line",
                        axisYType: "secondary",
                        name: showKeys[i],
                        showInLegend: true,
                        markerSize: 2,
                        dataPoints: []
                    }
                    showkeys_graph_position[showKeys[i]] = i;
                }
                
                for (i = showKeys.length,j=i,t=i; t < showKeys.length+showKeys_energy.length; t++) {
                    for(var q=0;q<energy_cols.length;q++){
                        data_array_powmr[j] = {
                            type: "stepArea",
                            axisYType: "secondary",
                            name: energy_cols[q]+"_"+showKeys_energy[t-i],
                            showInLegend: true,
                            markerSize: 2,
                            dataPoints: []
                        }
                        showkeys_graph_position[energy_cols[q]+"_"+showKeys_energy[t-i]] = j++;
                    }
                }
                
                console.log(showkeys_graph_position);
                console.log(data_array_powmr);
                console.log(showKeys);
                console.log(showKeys_energy);
                for (var i = 0; i < result.length; i++) {
                    var item = result[i];
                    for (var j = 0; j < Object.keys(item).length; j++) {
                        itemrow = Object.keys(item)[j];
                        if (showKeys.includes(itemrow)||showKeys_energy.includes(itemrow)) {
                            console.log(itemrow);
                            console.log(showkeys_graph_position[itemrow]);
                            data_array_powmr[showkeys_graph_position[itemrow]].dataPoints.push({
                                x: new Date(item["TIMESTAMP"]),
                                y: item[itemrow]
                            });
                        }
                    }
                }
                console.log(data_array_powmr);
                chart = new CanvasJS.Chart("graph", {
                    animationEnabled: true,
                    title: {
                        text: "Measurements"
                    },
                    toolTip: {
                        shared: true,
                        contentFormatter: function(e) {
                            //console.log(e.entries)
                            var str = "";
                            str = str.concat(e.entries[0].dataPoint.x);
                            str = str.concat("</br>");
                            for (var i = 0; i < e.entries.length; i++) {
                                var temp = "<div style=\"color: " + e.entries[i].dataSeries.color + ";\">" + e.entries[i].dataSeries.name + " <strong>" + e.entries[i].dataPoint.y + "</strong></div>";
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
                    axisX: {
                        valueFormatString: "DD MMM HH:mm"
                    },
                    axisY: {
                        includeZero: true
                    },
                    data: eval(data_array_powmr) //eval(data_array)
                });
                //console.log(data_array_powmr);
                //chart["data"] = 
                console.log(chart);
                chart.render();
            }
        });
    }

    function display_rpi_data() {
        $("#rpi_data").html("")
        $.ajax({
            url: "/memory_usage",
            success: function(result) {
                $("#rpi_data").html($("#rpi_data").html() + "<br><hr>" + result);
            }
        });
        $.ajax({
            url: "/cpu_gpu_temp",
            success: function(result) {
                $("#rpi_data").html($("#rpi_data").html() + "<br><hr>" + result);
            }
        });
        $.ajax({
            url: "/disk_usage",
            success: function(result) {
                $("#rpi_data").html($("#rpi_data").html() + "<br><hr>" + result);
            }
        });

    }