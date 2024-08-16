'''
Created on Jul 28, 2020

@author: duicul
'''
import sqlite3
import logging 
import traceback
import requests
from mailapi import send_mail, read_mail_config
from weather import Weather
import json 
from data_classes import Table_Data
from config_class import Config_Handler

mock_value = {"addr":0, "batt_charge_current":14, "battery_voltage":3027, "bms_01cell_voltage":0, "bms_02cell_voltage":0, "bms_03cell_voltage":0, "bms_04cell_voltage":0, "bms_05cell_voltage":0, "bms_06cell_voltage":0, "bms_07cell_voltage":0, "bms_08cell_voltage":0, "bms_09cell_voltage":0, "bms_10cell_voltage":0, "bms_11cell_voltage":0, "bms_12cell_voltage":0, "bms_13cell_voltage":0, "bms_14cell_voltage":0, "bms_15cell_voltage":0, "bms_16cell_voltage":0, "bms_battery_current":0, "bms_battery_soc":0, "bms_battery_voltage":0, "bts_temperature":25, "buck_topology":"3-normal_mode", "buck_topology_initial_finished":1, "bus_n_grid_voltage_match":0, "bus_ok":0, "bus_voltage":4565, "charge_finish":0, "command":768, "data_size":148, "disable_utility":0, "eq_charge_ready":0, "eq_charge_start":0, "fan1_speed_percent":0, "fan2_speed_percent":0, "floating_charge":0, "grid_current":0, "grid_freq":0, "grid_pll_ok":0, "grid_voltage":0, "hi0004":0, "hi0004_":0, "hi0013":0, "inv_current":3, "inv_freq":5000, "inv_va":0, "inv_voltage":4, "inverter_topology":"0-standby_mode", "inverter_topology_initial_finished":1, "inverter_va_percent":0, "inverter_voltage_dc_component":0, "inverter_watt_percent":0, "llc_topology":"8-charge_mode", "llc_topology_initial_finished":1, "lo0004":26, "lo0013":0, "lo0013_":0, "load_current":3, "load_va":0, "load_watt":0, "log_number":0, "low_load_current":0, "no_battery":1, "ntc2_temperature":54, "ntc3_temperature":31, "ntc4_temperature":44, "parallel_current":0, "parallel_frequency":0, "parallel_lock_phase_ok":0, "parallel_voltage":0, "proto":20872, "pv_current":22, "pv_excess":0, "pv_input_ok":1, "pv_power":35, "pv_topology":"3-normal_mode", "pv_topology_initial_finished":0, "pv_voltage":2738, "run_mode":13184, "software_version":5903, "system_initial_finished":1, "system_power":0, "t0002":0, "t0003":16, "t0005":0, "t0006":0, "t0007":0, "t0008":0, "t0009":0, "t0010":0, "t0011":0, "t0016":0, "t0017":0, "t0018":0, "t0019":0, "t0020":0, "t0026":0, "t0032":0, "t0041":0, "t0042":0, "t0047":0, "t0048":6, "w6":0, "words":1073672736}
mock_energy_value = {"duration":30531, "load_energy":0.0, "load_watt":0, "pv_energy":119.63, "pv_power":35, "t0026_total_energy":0.0, "t0026_total_power":0}


class PowLand_Data(Table_Data):
    data = {"OperationMode": 3,
            "EffectiveMainsVoltage": 0,
            "MainsFrequency": 0,
            "AverageMainsPower": 0,
            "EffectiveInverterVoltage": 230,
            "EffectiveInverterCurrent": 1.5,
            "InverterFrequency": 50,
            "AverageInverterPower": 230,
            "InverterChargingPower": 0,
            "OutputEffectiveVoltage": 230,
            "OutputEffectiveCurrent": 1,
            "OutputFrequency": 50,
            "OutputActivePower": 213,
            "OutputApparentPower": 230,
            "BatteryAverageVoltage": 26,
            "BatteryAverageCurrent": -9.800000191,
            "BatteryAveragePower": -254,
            "PVAverageVoltage": 26.200000760000003,
            "PVAverageCurrent": 0,
            "PVAveragePower": 0,
            "PVChargingAveragePower": 0,
            "LoadPercentage": 5,
            "DCDCTemperature": 37,
            "InverterTemperature": 39,
            "BatteryStateOfCharge": 68,
            "BatteryAverageCurrentFlow": -9.800000191,
            "InverterChargingAverageCurrent": 0,
            "PVChargingAverageCurrent": 0
        }
    
    data_types={'duration':int,
                'timestamp':str,
                "OperationMode": int,
                "EffectiveMainsVoltage": float,
                "MainsFrequency": float,
                "AverageMainsPower": float,
                "EffectiveInverterVoltage": float,
                "EffectiveInverterCurrent": float,
                "InverterFrequency": float,
                "AverageInverterPower": float,
                "InverterChargingPower": float,
                "OutputEffectiveVoltage": float,
                "OutputEffectiveCurrent": float,
                "OutputFrequency": float,
                "OutputActivePower": float,
                "OutputApparentPower": float,
                "BatteryAverageVoltage": float,
                "BatteryAverageCurrent": float,
                "BatteryAveragePower": float,
                "PVAverageVoltage": float,
                "PVAverageCurrent": float,
                "PVAveragePower": float,
                "PVChargingAveragePower": float,
                "LoadPercentage": float,
                "DCDCTemperature": float,
                "InverterTemperature": float,
                "BatteryStateOfCharge": float,
                "BatteryAverageCurrentFlow": float,
                "InverterChargingAverageCurrent": float,
                "PVChargingAverageCurrent": float,
                "AverageInverterEnergy": float,
                "AverageMainsEnergy": float,
                "BatteryAverageEnergy": float,
                "InverterChargingEnergy": float,
                "OutputActiveEnergy": float,
                "OutputApparentEnergy": float,
                "PVAverageEnergy": float,
                "PVChargingAverageEnergy": float,
                "AverageInverterEnergyTotal": float,
                "AverageMainsEnergyTotal": float,
                "BatteryAverageEnergyTotal": float,
                "InverterChargingEnergyTotal": float,
                "OutputActiveEnergyTotal": float,
                "OutputApparentEnergyTotal": float,
                "PVAverageEnergyTotal": float,
                "PVChargingAverageEnergyTotal": float               
            }
    
    """cols = ['duration', 'timestamp', 'batt_charge_current', 'battery_voltage', 'batt_power', 'batt_energy', 'bms_01cell_voltage', 'bms_02cell_voltage', 'bms_03cell_voltage', 'bms_04cell_voltage', 'bms_05cell_voltage', 'bms_06cell_voltage', 'bms_07cell_voltage',
            'bms_08cell_voltage', 'bms_09cell_voltage', 'bms_10cell_voltage', 'bms_11cell_voltage', 'bms_12cell_voltage', 'bms_13cell_voltage', 'bms_14cell_voltage', 'bms_15cell_voltage', 'bms_16cell_voltage', 'bms_battery_current',
            'bms_battery_soc', 'bms_battery_voltage', 'bts_temperature', 'buck_topology', 'buck_topology_initial_finished', 'bus_n_grid_voltage_match', 'bus_ok', 'charge_finish', 'disable_utility', 'eq_charge_ready', 'eq_charge_start',
            'fan1_speed_percent', 'fan2_speed_percent', 'floating_charge', 'grid_current', 'grid_freq', 'grid_pll_ok', 'grid_voltage', 'hi0004', 'hi0004_', 'hi0013', 'inv_current', 'inv_freq', 'inv_va', 'inv_voltage', 'inverter_topology',
            'inverter_topology_initial_finished', 'inverter_va_percent', 'inverter_voltage_dc_component', 'inverter_watt_percent', 'llc_topology', 'llc_topology_initial_finished', 'lo0004', 'lo0013', 'lo0013_',
            'load_current', 'load_energy', 'load_energy_dur', 'load_va', 'load_watt', 'log_number', 'low_load_current', 'no_battery', 'ntc2_temperature', 'ntc3_temperature', 'ntc4_temperature',
            'parallel_current', 'parallel_frequency', 'parallel_lock_phase_ok', 'parallel_voltage', 'pv_current', 'pv_energy', 'pv_energy_dur', 'pv_excess', 'pv_input_ok', 'pv_power', 'pv_topology', 'pv_topology_initial_finished', 'pv_voltage',
            'software_version', 'system_initial_finished', 'system_power', 't0010', 't0011', 't0002', 't0003', 't0005', 't0006', 't0007', 't0008', 't0009', 't0016', 't0017', 't0018', 't0019', 't0020', 't0026', 't0026_total_energy', 't0026_total_energy_dur', 't0032', 't0041', 't0042', 't0047', 't0048', 'w6']"""
    
    #convDataFactors = {"batt_charge_current":10, "battery_voltage":100, "bms_01cell_voltage":100, "bms_02cell_voltage":100, "bms_03cell_voltage":100, "bms_04cell_voltage":100,
    #                   "bms_05cell_voltage":100, "bms_06cell_voltage":100, "bms_07cell_voltage":100, "bms_08cell_voltage":100, "bms_09cell_voltage":100, "bms_10cell_voltage":100, "bms_11cell_voltage":100, "bms_12cell_voltage":100,
    #                   "bms_13cell_voltage":100, "bms_14cell_voltage":100, "bms_15cell_voltage":100, "bms_16cell_voltage":100, "bms_battery_current":100, "bms_battery_soc":100, "bms_battery_voltage":100, "bus_voltage":10,
    #                   "grid_current":100, "grid_freq":100, "grid_voltage":10, "inv_current":100, "inv_freq":100, "inv_voltage":10, "load_current":100, "pv_current":100, "pv_voltage":10}
    #"SELECT *,LAG(pv_energy_total,1) OVER (ORDER BY TIMESTAMP) as pv_energy_total_prev,pv_energy_total-LAG(pv_energy_total,1) OVER (ORDER BY TIMESTAMP) as pv_energy_total_diff  FROM PowMr_Data Group by strftime('%Y-%m-%d %H',timestamp);"
    
    energy_cols = [{'name':"AverageInverterEnergyTotal", 'type':'REAL'},
                   {'name':"AverageMainsEnergyTotal", 'type':'REAL'},
                   {'name':"BatteryAverageEnergyTotal", 'type':'REAL'},
                   {'name':"InverterChargingEnergyTotal", 'type':'REAL'},
                   {'name':"OutputActiveEnergyTotal", 'type':'REAL'},
                   {'name':"OutputApparentEnergyTotal", 'type':'REAL'},
                   {'name':"PVAverageEnergyTotal", 'type':'REAL'},
                   {'name':"PVChargingAverageEnergyTotal", 'type':'REAL'}]
        
    average_columns = [{'name':"AverageInverterEnergyTotal_Average", 'type':'REAL','average_col':"AverageInverterEnergyTotal"},
                   {'name':"AverageMainsEnergyTotal_Average", 'type':'REAL','average_col':"AverageMainsEnergyTotal"},
                   {'name':"BatteryAverageEnergyTotal_Average", 'type':'REAL','average_col':"BatteryAverageEnergyTotal"},
                   {'name':"InverterChargingEnergyTotal_Average", 'type':'REAL','average_col':"InverterChargingEnergyTotal"},
                   {'name':"OutputActiveEnergyTotal_Average", 'type':'REAL','average_col':"OutputActiveEnergyTotal"},
                   {'name':"OutputApparentEnergyTotal_Average", 'type':'REAL','average_col':"OutputApparentEnergyTotal"},
                   {'name':"PVAverageEnergyTotal_Average", 'type':'REAL','average_col':"PVAverageEnergyTotal"},
                   {'name':"PVChargingAverageEnergyTotal_Average", 'type':'REAL','average_col':"PVChargingAverageEnergyTotal"}]    
        #{'name':'load_energy_total', 'type':'REAL'}, {'name':'pv_energy_total', 'type':'REAL'}
        #           , {'name':'t0026_total_energy_total', 'type':'REAL'}, {'name':'batt_energy_total', 'type':'REAL'}, {'name':'batt_energy_charge_total', 'type':'REAL'}, {'name':'batt_energy_discharge_total', 'type':'REAL'}]
    energy_opt_vals = ["energyhour", "energyday", "energyweek", "energymonth", "energyyear"]
    BatteryStateOfChargeReal = [{'name':'BatteryStateOfChargeReal', 'type':'REAL'}]
    #average_columns =[]
    
    '''average_columns = [{'name':'load_power_average', 'type':'REAL', 'average_col':'load_energy'}, {'name':'pv_power_average', 'type':'REAL', 'average_col':'pv_energy'}
                   , {'name':'t0026_total_power_average', 'type':'REAL', 'average_col':'t0026_total_energy'}, {'name':'batt_power_average', 'type':'REAL', 'average_col':'batt_energy'},
                   {'name':'batt_power_charge_average', 'type':'REAL', 'average_col':'batt_energy_charge'},{'name':'batt_power_discharge_average', 'type':'REAL', 'average_col':'batt_energy_discharge'}]
    '''
    def __init__(self, database, logger_name):
        self.database = database
        self.logger_name = logger_name
        self.table_name = "PowLand_Data"
        self.create_table()
        ch = Config_Handler("json/monitor_config.json", 'monitor_logger')
        self.config = ch.loadUsingFile()
    
    '''def convertData(self, powmr_data):
        if self.config.converData:
            for key in PowMr_Data.convDataFactors.keys():
                if key in powmr_data.keys() and powmr_data[key] is not None :
                    powmr_data[key] /= PowMr_Data.convDataFactors[key]
        return powmr_data'''
        
    def current_timestamp(self):
        conn = sqlite3.connect(self.database)
        mycursor = conn.cursor()
        querry = "SELECT datetime('now','localtime') "
        mycursor.execute(querry)
        result = ""
        try:
            result = mycursor.fetchall()
            mycursor.close()
            conn.close()
        except:
            logging.getLogger(self.logger_name).error(str(traceback.format_exc()))
        return result   
    
    def delete_table(self):
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()
        sql = "DROP TABLE IF EXISTS " + self.table_name
        print(sql)
        try:
            cursor.execute(sql)
            logging.getLogger(self.logger_name).debug(self.table_name + " created ")
            cursor.close()
            conn.close()
        except:
            logging.getLogger(self.logger_name).warning(str(traceback.format_exc()))
    
    def create_table(self):
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()
        sql = "CREATE TABLE IF NOT EXISTS " + self.table_name + " ("
        sql += "ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT ,"
        sql += "TIMESTAMP timestamp with time zone NOT NULL DEFAULT (datetime('now','localtime')),"
        col_names = list(PowLand_Data.data_types.keys())
        #print(col_names)
        sql += col_names[0] + " " + self.typeToSQL(PowLand_Data.data_types[col_names[0]])
        #if 'Total' in col_names[0] or PowLand_Data.data_types[col_names[0]] in [int,float]:
        #    sql += " DEFAULT 0"
        
        for i in range(1, len(col_names)):
            cname = col_names[i]
            if not cname in ['timestamp', 'duration', 'id']:
                sql += " , " + cname + " " + self.typeToSQL(PowLand_Data.data_types[cname])
            if 'Total' in cname or PowLand_Data.data_types[col_names[0]] in [int,float] :
                sql += " DEFAULT 0" 
        sql += ");"
        print(sql)
        try:
            cursor.execute(sql)
            logging.getLogger(self.logger_name).debug(self.table_name + " created ")
            cursor.close()
            conn.close()
        except:
            logging.getLogger(self.logger_name).warning(str(traceback.format_exc()))
        
    def remove_wrong_value(self):
        ''' Remove incorrect values from the database '''
        pass
    
    def extract_all_between(self, fdate, ldate, energy_opt=None):
        condition = " WHERE date(TIMESTAMP) BETWEEN '" + str(fdate) + "' AND  '" + str(ldate) + "' "
        conn = sqlite3.connect(self.database)
        mycursor = conn.cursor()
        # querry = "SELECT * FROM " + self.table_name + " " + condition
        querry = "SELECT "
        if energy_opt is None:
            querry += "*"
        else:
            querry += "ID"
            for ene_col in self.energy_cols:
                querry += "," + ene_col['name'] + " - coalesce(LAG(" + ene_col['name'] + ",1) OVER (ORDER BY TIMESTAMP ASC) ,0) "
            querry += ",TIMESTAMP"
        querry += " FROM " 
        if energy_opt is None:
            querry += self.table_name
        else:
            querry += " (SELECT * FROM " + self.table_name + "  ORDER BY TIMESTAMP DESC ) "
        # querry += " " + condition
        if energy_opt is not None:
            if energy_opt == "energyhour":
                querry += " Group by strftime('%Y-%m-%d %H',timestamp)"
            elif energy_opt == "energyday":
                querry += " Group by strftime('%Y-%m-%d',timestamp)"
            elif energy_opt == "energyweek":
                querry += " Group by strftime('%Y-%W',timestamp)"
            elif energy_opt == "energymonth":
                querry += " Group by strftime('%Y-%m',timestamp)"
            elif energy_opt == "energyyear":
                querry += " Group by strftime('%Y',timestamp)"
        querry = "SELECT * FROM (" + querry + ")" + condition      
        logging.info(querry)
        logging.getLogger(self.logger_name).info(querry)
        mycursor.execute(querry)
        try:
            result = mycursor.fetchall()
            mycursor.close()
            conn.close()
        except:
            logging.getLogger(self.logger_name).error(str(traceback.format_exc()))
        return result
    
    def extractCompare(self, date1, date2):
        condition = " WHERE date(TIMESTAMP) ='" + str(date1) + "' OR  date(TIMESTAMP)='" + str(date2) + "' ;"
        conn = sqlite3.connect(self.database)
        mycursor = conn.cursor()
        querry = "SELECT * FROM " + self.table_name + " " + condition
        logging.info(querry)
        logging.getLogger(self.logger_name).info(querry)
        mycursor.execute(querry)
        try:
            result = mycursor.fetchall()
            mycursor.close()
            conn.close()
        except:
            logging.getLogger(self.logger_name).error(str(traceback.format_exc()))
        return result
    
    def extract_all_interval(self, items, energy_opt=None):
        ''' Returns last items rows from the table '''
        condition = ""
        # print(items)
        if items == "0":
            condition = " WHERE date(TIMESTAMP) BETWEEN date('now','0 days' ,'localtime') AND  date('now','localtime') "
        elif items == "1":
            condition = " WHERE date(TIMESTAMP) BETWEEN date('now','-1 days' ,'localtime') AND  date('now','localtime') "
        elif items == "2":
            condition = " WHERE date(TIMESTAMP) BETWEEN date('now','-2 days' ,'localtime') AND  date('now','localtime') "
        elif items == "3":
            condition = " WHERE date(TIMESTAMP) BETWEEN date('now','-3 days' ,'localtime') AND  date('now','localtime') "
        elif items == "4":
            condition = " WHERE date(TIMESTAMP) BETWEEN date('now','-4 days' ,'localtime') AND  date('now','localtime') "
        elif items == "5":
            condition = " WHERE date(TIMESTAMP) BETWEEN date('now','-5 days','localtime') AND  date('now','localtime') "
        elif items == "6":
            condition = " WHERE date(TIMESTAMP) BETWEEN date('now','-6 days' ,'localtime') AND  date('now','localtime') "  
        elif items == "7":
            condition = " WHERE date(TIMESTAMP) BETWEEN date('now','-7 days' ,'localtime') AND  date('now','localtime') "
        elif items == "8":
            condition = " WHERE date(TIMESTAMP) BETWEEN date('now','-8 days' ,'localtime') AND  date('now','localtime') "
        elif items == "9":
            condition = " WHERE date(TIMESTAMP) BETWEEN date('now','-9 days' ,'localtime') AND  date('now','localtime') "
        elif items == "10":
            condition = " WHERE date(TIMESTAMP) BETWEEN date('now','-10 days','localtime' ) AND  date('now','localtime') "
        elif items == "1m":
            condition = " WHERE date(TIMESTAMP) BETWEEN DATE('now','start of month','localtime') AND  date('now','localtime') "    
        elif items == "2m":
            condition = " WHERE date(TIMESTAMP) BETWEEN DATE('now','start of month','-1 month','localtime') AND  date('now','localtime') "
            # condition=" WHERE date(TIMESTAMP) BETWEEN date('now','-2 months' ) AND  date('now') "
        elif items == "3m":
            condition = " WHERE date(TIMESTAMP) BETWEEN DATE('now','start of month','-2 month','localtime') AND  date('now','localtime') "                
        # try:
        #    items=int(items)
        # except:
        #    logging.getLogger(self.logger_name).error(str(traceback.format_exc()))
        #    return []
        # logging.getLogger(self.logger_name).info(condition)
        # print(condition)
        # if(items!=-1):
        #    condition=querry #" WHERE ID >= ((SELECT MAX(ID)  FROM "+self.table_name+") - "+str(items)+")"
        # else:
        #    condition=""
        conn = sqlite3.connect(self.database)
        mycursor = conn.cursor()
        querry = "SELECT "
        if energy_opt is None:
            querry += "*"
        else:
            querry += "ID"
            for ene_col in self.energy_cols:
                querry += "," + ene_col['name'] + " - coalesce(LAG(" + ene_col['name'] + ",1) OVER (ORDER BY TIMESTAMP ASC) ,0) "
            querry += ",TIMESTAMP"
        querry += " FROM " 
        if energy_opt is None:
            querry += self.table_name
        else:
            querry += " (SELECT * FROM " + self.table_name + "  ORDER BY TIMESTAMP DESC ) "
        # querry += " " + condition
        if energy_opt is not None:
            if energy_opt == "energyhour":
                querry += " Group by strftime('%Y-%m-%d %H',timestamp)"
            elif energy_opt == "energyday":
                querry += " Group by strftime('%Y-%m-%d',timestamp)"
            elif energy_opt == "energyweek":
                querry += " Group by strftime('%Y-%W',timestamp)"
            elif energy_opt == "energymonth":
                querry += " Group by strftime('%Y-%m',timestamp)"
            elif energy_opt == "energyyear":
                querry += " Group by strftime('%Y',timestamp)"
                
        querry = "SELECT * FROM (" + querry + ")" + condition        
        
        logging.getLogger(self.logger_name).info(querry)
        mycursor.execute(querry)
        try:
            result = mycursor.fetchall()
            mycursor.close()
            conn.close()
        except:
            logging.getLogger(self.logger_name).error(str(traceback.format_exc()))
        return result
    
    def extract_last(self):
        """Extracts the latest row from the table"""
        conn = sqlite3.connect(self.database)
        mycursor = conn.cursor()
        querry = "SELECT * FROM " + self.table_name + " ORDER BY timestamp DESC LIMIT 1;"
        print(querry)
        mycursor.execute(querry)
        try:
            result = mycursor.fetchall()
            mycursor.close()
            conn.close()
        except:
            logging.getLogger(self.logger_name).error(str(traceback.format_exc()))
        if result is not None and len(result) > 0:
            data = self.dbResptoDict(result, self.getColumnNames())[0]
            logging.getLogger(self.logger_name).info("PowMr_Data extract_last " + " result: " + json.dumps(data))
            return data
        return None
    
    def insert(self, values:dict):
        if len(values.keys()) == 0:return
        conn = sqlite3.connect(self.database)
        mycursor = conn.cursor()
        sql = "INSERT INTO " + self.table_name
        vals = list(map(lambda x:values[x], values.keys()))
        sql += " ("
        sql += ",".join(values.keys())
        sql += ") VALUES ("
        sql += ",".join(['?'] * len(values.keys()))
        sql += ")"
        logging.getLogger(self.logger_name).info("PowMr_Data polled " + " result: " + str(sql) + " " + str(vals))
        print(sql + " " + str(vals))
        # print(vals)
        mycursor.executemany(sql, [tuple(vals)])
        try:
            conn.commit()
            mycursor.close()
            conn.close()
        except:
            logging.getLogger(self.logger_name).error(str(traceback.format_exc()))
    
    def poll_value(self, powmr_url, timeout=10, mock=True):
        headers = {}
        if mock:
            powmr_data = mock_value
            powmr_data_energy = mock_energy_value
        else:
            try:
                logging.getLogger(self.logger_name).info("powmr sending requests")
                print(powmr_url + "/modbus")
                powmr_data = requests.get(powmr_url + "/modbus", headers=headers, timeout=timeout).json()
                #print(str(powmr_data))
                print(str(powmr_data)+ "/modbus_energy_clean")
                powmr_data_energy = requests.get(powmr_url + "/modbus_energy_clean", headers=headers, timeout=timeout).json()
                #print(str(powmr_data))
                logging.getLogger(self.logger_name).info("requests sent")
            except Exception as e:
                print(e)
                logging.getLogger(self.logger_name).error(str(traceback.format_exc()))
                return False
        ins_data = {}
        logging.getLogger(self.logger_name).info("powmr_data")
        #print("powmr_data")
        logging.getLogger(self.logger_name).info(powmr_data)
        #print(powmr_data)
        logging.getLogger(self.logger_name).info(powmr_data_energy)
        #print(powmr_data_energy)
        col_names = list(map(lambda x:x.lower(),PowLand_Data.data_types.keys()))
        '''if 'resp' in powmr_data.keys() and powmr_data['resp'] != 1:
            #ins_data['inverter_status_on'] = False
        else:'''
        if 'values' in powmr_data.keys():
            powmr_data = powmr_data['values']
            #print("values")
            #print(powmr_data)
        for ent in powmr_data.keys():
            #print(ent)
            if ent.lower() in col_names:
                #print(ent)
                ins_data[ent] = powmr_data[ent]
        #print()
        #ins_data['inverter_status_on'] = True
        for ent in powmr_data_energy.keys():
            # print(ent)
            if ent.lower() in col_names:
                # print(ent)
                ins_data[ent] = powmr_data_energy[ent]
        lastValue = self.extract_last()
        # print("lastValue")
        # print(lastValue)
        # lastValue = self.dbResptoDict(lastValue, self.getColumnNames())
        #print("energy total "+json.dumps(ins_data))
        if lastValue is not None:
            ins_data['AverageInverterEnergyTotal'] = lastValue['AverageInverterEnergyTotal'] + ins_data['AverageInverterEnergy']
            ins_data['AverageMainsEnergyTotal'] = lastValue['AverageMainsEnergyTotal'] + ins_data['AverageMainsEnergy']
            ins_data['BatteryAverageEnergyTotal'] = lastValue['BatteryAverageEnergyTotal'] + ins_data['BatteryAverageEnergy']
            ins_data['InverterChargingEnergyTotal'] = lastValue['InverterChargingEnergyTotal'] + ins_data['InverterChargingEnergy']
            
            ins_data['OutputActiveEnergyTotal'] = lastValue['OutputActiveEnergyTotal'] + ins_data['OutputActiveEnergy']
            ins_data['OutputApparentEnergyTotal'] = lastValue['OutputApparentEnergyTotal'] + ins_data['OutputApparentEnergy']
            ins_data['PVAverageEnergyTotal'] = lastValue['PVAverageEnergyTotal'] + ins_data['PVAverageEnergy']
            ins_data['PVChargingAverageEnergyTotal'] = lastValue['PVChargingAverageEnergyTotal'] + ins_data['PVChargingAverageEnergy']
            
        logging.getLogger(self.logger_name).info("PowMr_Data polled " + " result: " + json.dumps(ins_data))
        #ins_data = self.convertData(ins_data)
        #print(ins_data)        
        
        return self.insert(ins_data)
    
    def restart_device(self, home_station_url):
        logging.getLogger(self.logger_name).info("Restart")
        requests.get(home_station_url + "/restart")
    
    def getColumnNames(self):
        colnames = super().getColumnNames()  # self.average_columns + 
        # colnames.sort(key=lambda x:x.get("name",""))
        return colnames
    
    def calculate_capacity_lifepo4(self,bat_volt):
        volt_val=[20,24,25,25.6,25.8,26,26.2,26.4,26.6,26.8,27.2]
        bat_cap=[0,9,14,17,20,30,40,70,90,99,100]
        if bat_volt >= volt_val[len(volt_val)-1]:
            return 100
        if bat_volt <= volt_val[0]:
            return 0
        for i in range(len(volt_val)):
            if volt_val[i]>bat_volt:
                break
        #print("upper "+str(volt_val[i]))
        #print("upper "+str(bat_cap[i]))
        percent_interval_voltage = (bat_volt-volt_val[i-1])/(volt_val[i]-volt_val[i-1])
        #print(percent_interval_voltage)
        #print(bat_cap[i]-bat_cap[i-1])
        bat_cap = (percent_interval_voltage * (bat_cap[i]-bat_cap[i-1]))+bat_cap[i-1]
        return int(bat_cap)
    
    def dbResptoDict(self, dbresp, colnames,addAverage=True):
        if dbresp is None:
            return []
        resp = []
        colnameslist = list(map(lambda x:x["name"], colnames))
        # print("colnames "+str(len(colnames)))
        for dbrow in dbresp:
            dictResp = {}
            dbrow = list(dbrow)
            # print("dbrow "+str(len(dbrow)))
            for i in range(len(colnameslist)):
                cn = colnameslist[i]
                if "type" in colnames[i].keys() and colnames[i]["type"] == "BOOLEAN" and not isinstance(dbrow[i], bool):
                    cnval = (dbrow[i] == 1)
                else:
                    cnval = dbrow[i]
                # print(str(cn)+ " "+str(cnval))
                dictResp[cn] = cnval
            if addAverage:
                for average_col in self.average_columns:
                    if 'average_col' in average_col.keys() and average_col['average_col'] in dictResp.keys() and  dictResp.get('duration', 0) > 0:
                        dictResp[average_col['name']] = dictResp[average_col['average_col']] / (dictResp['duration'] / 3600)
            dictResp["BatteryStateOfChargeReal"] = self.calculate_capacity_lifepo4(dictResp["BatteryAverageVoltage"])
            resp.append(dictResp)
        return resp

    def extractAllValues(self):
        conn = sqlite3.connect(self.database)
        mycursor = conn.cursor()
        querry = "SELECT * FROM " + self.table_name + "  ORDER BY TIMESTAMP DESC"
        mycursor.execute(querry)
        try:
            result = mycursor.fetchall()
            mycursor.close()
            conn.close()
        except:
            logging.getLogger(self.logger_name).error(str(traceback.format_exc()))
        data = self.dbResptoDict(result, self.getColumnNames(),addAverage=False)
        return data

if __name__ == '__main__':
    import logging.handlers
    handler = logging.handlers.RotatingFileHandler(
        'logs/error_monitor.log',
        maxBytes=1024 * 1024)
    handler.setFormatter(logging.Formatter('[%(asctime)s] %(levelname)s in %(module)s: %(message)s'))
    logger = logging.getLogger('monitor_logger')
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    # ac=AC_Data("measure.db","random","random")
    # ac.insert(221,6.3,170,5478)
    tsd = PowLand_Data("db/measure_powmr.db", 'monitor_logger')
    tsd.create_table()
    tableData = tsd.extractAllValues()
    print(json.dumps(tableData))
    tsd.delete_table()
    tsd.create_table()
    for entry in tableData:
        tsd.insert(entry)
    #q = {}
    # for ent in col_names:
    #    if ent!='TIMESTAMP':
    #        q[ent]=0
    # tsd.insert(q)
    tsd.poll_value('http://192.168.0.11', mock=False)
    # tsd.insert(1,42.3)
    #print(tsd.extract_all_interval(""))
    #print(tsd.getColumnNames())
    print(json.dumps(tsd.dbResptoDict(tsd.extract_all_interval(""), tsd.getColumnNames())))
    # tsd.convert_old()
    # td.insert(20,30)
    # print(ac.extract_last())
    # print(ac.extract_all_interval(2))
    pass
