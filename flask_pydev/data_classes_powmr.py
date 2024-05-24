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


class PowMr_Data(Table_Data):
    data = {"addr":0, "batt_charge_current":14, "battery_voltage":3028, "bms_01cell_voltage":0, "bms_02cell_voltage":0, "bms_03cell_voltage":0, "bms_04cell_voltage":0, "bms_05cell_voltage":0, "bms_06cell_voltage":0, "bms_07cell_voltage":0, "bms_08cell_voltage":0,
            "bms_09cell_voltage":0, "bms_10cell_voltage":0, "bms_11cell_voltage":0, "bms_12cell_voltage":0, "bms_13cell_voltage":0, "bms_14cell_voltage":0, "bms_15cell_voltage":0, "bms_16cell_voltage":0, "bms_battery_current":0, "bms_battery_soc":0, "bms_battery_voltage":0,
            "bts_temperature":25, "buck_topology":"3-normal_mode", "buck_topology_initial_finished":1, "bus_n_grid_voltage_match":0, "bus_ok":0, "bus_voltage":4565, "charge_finish":0, "command":768, "data_size":148, "disable_utility":0, "eq_charge_ready":0, "eq_charge_start":0,
            "fan1_speed_percent":0, "fan2_speed_percent":0, "floating_charge":0, "grid_current":0, "grid_freq":0, "grid_pll_ok":0, "grid_voltage":0, "hi0004":0, "hi0004_":0, "hi0013":0, "inv_current":3, "inv_freq":5000, "inv_va":0, "inv_voltage":4,
            "inverter_topology":"0-standby_mode", "inverter_topology_initial_finished":1, "inverter_va_percent":0, "inverter_voltage_dc_component":0, "inverter_watt_percent":0, "llc_topology":"8-charge_mode", "llc_topology_initial_finished":1,
            "lo0004":26, "lo0013":0, "lo0013_":0, "load_current":1, "load_va":0, "load_watt":0, "log_number":0, "low_load_current":0, "no_battery":1, "ntc2_temperature":49, "ntc3_temperature":31, "ntc4_temperature":35, "parallel_current":0, "parallel_frequency":0, "parallel_lock_phase_ok":0, "parallel_voltage":0,
            "proto":20872, "pv_current":17, "pv_excess":0, "pv_input_ok":1, "pv_power":32, "pv_topology":"3-normal_mode", "pv_topology_initial_finished":0, "pv_voltage":2855, "run_mode":13184, "software_version":5903, "system_initial_finished":1, "system_power":0,
            "t0002":0, "t0003":16, "t0005":0, "t0006":0, "t0007":0, "t0008":0, "t0009":0, "t0010":0, "t0011":0, "t0016":0, "t0017":0, "t0018":0, "t0019":0, "t0020":0, "t0026":0, "t0032":0, "t0041":0, "t0042":0, "t0047":0, "t0048":6, "w6":0, "words":1073672736}
    
    data_types = {'duration':int,
                  'timestamp':str,
                  'batt_charge_current':float,
                  'battery_voltage':float,
                  'bms_01cell_voltage':float,
                  'bms_02cell_voltage':float,
                  'bms_03cell_voltage':float,
                  'bms_04cell_voltage':float,
                  'bms_05cell_voltage':float,
                  'bms_06cell_voltage':float,
                  'bms_07cell_voltage':float,
                  'bms_08cell_voltage':float,
                  'bms_09cell_voltage':float,
                  'bms_10cell_voltage':float,
                  'bms_11cell_voltage':float,
                  'bms_12cell_voltage':float,
                  'bms_13cell_voltage':float,
                  'bms_14cell_voltage':float,
                  'bms_15cell_voltage':float,
                  'bms_16cell_voltage':float,
                  'bms_battery_current':float,
                  'bms_battery_soc':float,
                  'bms_battery_voltage':float,
                  'bts_temperature':int,
                  'buck_topology':int,
                  'buck_topology_initial_finished':bool,
                  'bus_n_grid_voltage_match':bool,
                  'bus_ok':bool,
                  'charge_finish':bool,
                  'disable_utility':bool,
                  'eq_charge_ready':bool,
                  'eq_charge_start':bool,
                  'fan1_speed_percent':int,
                  'fan2_speed_percent':int,
                  'floating_charge':bool,
                  'grid_current':float,
                  'grid_freq':float,
                  'grid_pll_ok':bool,
                  'grid_voltage':float,
                  'hi0004':int,
                  'hi0004_':int,
                  'hi0013':bool,
                  'inv_current':float,
                  'inv_freq':float,
                  'inv_va':float,
                  'inv_voltage':float,
                  'inverter_topology':int,
                  'inverter_topology_initial_finished':bool,
                  'inverter_va_percent':float,
                  'inverter_voltage_dc_component':float,
                  'inverter_watt_percent':float,
                  'llc_topology':int,
                  'llc_topology_initial_finished':bool,
                  'lo0004':int,
                  'lo0013':int,
                  'lo0013_':int,
                  'load_current':float,
                  'load_energy':float,
                  'load_energy_total':float,
                  'load_va':float,
                  'load_watt':float,
                  'log_number':int,
                  'low_load_current':float,
                  'no_battery':bool,
                  'ntc2_temperature':int,
                  'ntc3_temperature':int,
                  'ntc4_temperature':int,
                  'parallel_current':float,
                  'parallel_frequency':float,
                  'parallel_lock_phase_ok':bool,
                  'parallel_voltage':float,
                  'pv_current':float,
                  'pv_energy':float,
                  'pv_energy_total':float,
                  'pv_excess':bool,
                  'pv_input_ok':bool,
                  'pv_power':float,
                  'pv_topology':int,
                  'pv_topology_initial_finished':bool,
                  'pv_voltage':float,
                  'software_version':int,
                  'system_initial_finished':bool,
                  'system_power':bool,
                  't0010':int,
                  't0011':int,
                  't0002':int,
                  't0003':int,
                  't0005':int,
                  't0006':int,
                  't0007':int,
                  't0008':int,
                  't0009':int,
                  't0016':int,
                  't0017':int,
                  't0018':int,
                  't0019':int,
                  't0020':int,
                  't0026':float,
                  't0026_total_energy':float,
                  't0026_total_energy_total':float,
                  't0032':float,
                  't0041':float,
                  't0042':float,
                  't0047':float,
                  't0048':float,
                  'w6':int,
                  'inverter_status_on':bool}
    
    cols = ['duration', 'timestamp', 'batt_charge_current', 'battery_voltage', 'bms_01cell_voltage', 'bms_02cell_voltage', 'bms_03cell_voltage', 'bms_04cell_voltage', 'bms_05cell_voltage', 'bms_06cell_voltage', 'bms_07cell_voltage',
            'bms_08cell_voltage', 'bms_09cell_voltage', 'bms_10cell_voltage', 'bms_11cell_voltage', 'bms_12cell_voltage', 'bms_13cell_voltage', 'bms_14cell_voltage', 'bms_15cell_voltage', 'bms_16cell_voltage', 'bms_battery_current',
            'bms_battery_soc', 'bms_battery_voltage', 'bts_temperature', 'buck_topology', 'buck_topology_initial_finished', 'bus_n_grid_voltage_match', 'bus_ok', 'charge_finish', 'disable_utility', 'eq_charge_ready', 'eq_charge_start',
            'fan1_speed_percent', 'fan2_speed_percent', 'floating_charge', 'grid_current', 'grid_freq', 'grid_pll_ok', 'grid_voltage', 'hi0004', 'hi0004_', 'hi0013', 'inv_current', 'inv_freq', 'inv_va', 'inv_voltage', 'inverter_topology',
            'inverter_topology_initial_finished', 'inverter_va_percent', 'inverter_voltage_dc_component', 'inverter_watt_percent', 'llc_topology', 'llc_topology_initial_finished', 'lo0004', 'lo0013', 'lo0013_',
            'load_current', 'load_energy', 'load_energy_dur', 'load_va', 'load_watt', 'log_number', 'low_load_current', 'no_battery', 'ntc2_temperature', 'ntc3_temperature', 'ntc4_temperature',
            'parallel_current', 'parallel_frequency', 'parallel_lock_phase_ok', 'parallel_voltage', 'pv_current', 'pv_energy', 'pv_energy_dur', 'pv_excess', 'pv_input_ok', 'pv_power', 'pv_topology', 'pv_topology_initial_finished', 'pv_voltage',
            'software_version', 'system_initial_finished', 'system_power', 't0010', 't0011', 't0002', 't0003', 't0005', 't0006', 't0007', 't0008', 't0009', 't0016', 't0017', 't0018', 't0019', 't0020', 't0026', 't0026_total_energy', 't0026_total_energy_dur', 't0032', 't0041', 't0042', 't0047', 't0048', 'w6']    
    
    convDataFactors = {"batt_charge_current":10, "battery_voltage":100, "bms_01cell_voltage":100, "bms_02cell_voltage":100, "bms_03cell_voltage":100, "bms_04cell_voltage":100,
                       "bms_05cell_voltage":100, "bms_06cell_voltage":100, "bms_07cell_voltage":100, "bms_08cell_voltage":100,"bms_09cell_voltage":100, "bms_10cell_voltage":100, "bms_11cell_voltage":100, "bms_12cell_voltage":100,
                       "bms_13cell_voltage":100, "bms_14cell_voltage":100, "bms_15cell_voltage":100, "bms_16cell_voltage":100,"bms_battery_current":100, "bms_battery_soc":100, "bms_battery_voltage":100, "bus_voltage":10,
                       "grid_current":100, "grid_freq":100, "grid_voltage":10,"inv_current":100, "inv_freq":100, "inv_voltage":10,"load_current":100, "pv_current":100, "pv_voltage":10}
    
    def __init__(self, database, logger_name):
        self.database = database
        self.logger_name = logger_name
        self.table_name = "PowMr_Data"
        self.create_table()
        ch = Config_Handler("json/monitor_config.json", 'monitor_logger')
        self.config = ch.loadUsingFile()
    
    def convertData(self, powmr_data):
        if self.config.converData:
            for key in PowMr_Data.convDataFactors.keys():
                if key in powmr_data.keys():
                    powmr_data[key]/=PowMr_Data.convDataFactors[key]
    
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
        col_names = list(PowMr_Data.data_types.keys())
        
        sql += col_names[0] + " " + self.typeToSQL(PowMr_Data.data_types[col_names[0]])
        if 'total' in col_names[0]:
            sql += " DEFAULT 0"
        
        for i in range(1, len(col_names)):
            cname = col_names[i]
            if not cname in ['timestamp', 'duration', 'id']:
                sql += " , " + cname + " " + self.typeToSQL(PowMr_Data.data_types[cname])
            if 'total' in cname:
                sql += " DEFAULT 0" 
        sql += ");"
        # print(sql)
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
    
    def extract_all_between(self, fdate, ldate):
        condition = " WHERE date(TIMESTAMP) BETWEEN '" + str(fdate) + "' AND  '" + str(ldate) + "' ;"
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
    
    def extract_all_interval(self, items):
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
        querry = "SELECT * FROM " + self.table_name + " " + condition
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
        if len(result) > 0:
            return self.convertData(self.dbResptoDict(result, self.getColumnNames())[0])
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
        print(sql + " " + str(vals))
        # print(vals)
        mycursor.executemany(sql, [tuple(vals)])
        try:
            conn.commit()
            mycursor.close()
            conn.close()
        except:
            logging.getLogger(self.logger_name).error(str(traceback.format_exc()))
    
    def poll_value(self, powmr_url, mock=True):
        headers = {}
        if mock:
            powmr_data = mock_value
            powmr_data_energy = mock_energy_value
        else:
            try:
                powmr_data = requests.get(powmr_url + "/powmr", headers=headers).json()
                powmr_data_energy = requests.get(powmr_url + "/powmr_energy_clean", headers=headers).json()
            except Exception as e:
                print(e)
                logging.getLogger(self.logger_name).error(str(traceback.format_exc()))
                return False
        ins_data = {}
        print("powmr_data")
        print(powmr_data)
        print(powmr_data_energy)
        col_names = list(PowMr_Data.data_types.keys())
        if 'status' in powmr_data.keys() and powmr_data['status'] == 'disconnected':
            ins_data['inverter_status_on'] = False
        else:
            for ent in powmr_data.keys():
                # print(ent)
                if ent.lower() in col_names:
                    # print(ent)
                    ins_data[ent.lower()] = powmr_data[ent.lower()]
            print()
            ins_data['inverter_status_on'] = True
        for ent in powmr_data_energy.keys():
            # print(ent)
            if ent.lower() in col_names:
                # print(ent)
                ins_data[ent.lower()] = powmr_data_energy[ent.lower()]
        lastValue = self.extract_last()
        # print("lastValue")
        # print(lastValue)
        # lastValue = self.dbResptoDict(lastValue, self.getColumnNames())
        if lastValue is not None:
            ins_data['load_energy_total'] = lastValue['load_energy_total'] + ins_data['load_energy']
            ins_data['pv_energy_total'] = lastValue['pv_energy_total'] + ins_data['pv_energy']
            ins_data['t0026_total_energy_total'] = lastValue['t0026_total_energy_total'] + ins_data['t0026_total_energy']
        
        self.convertData(ins_data)
        print(ins_data)        
        
        return self.insert(ins_data)
    
    def restart_device(self, home_station_url):
        logging.getLogger(self.logger_name).info("Restart")
        requests.get(home_station_url + "/restart")

        
if __name__ == '__main__':
    # ac=AC_Data("measure.db","random","random")
    # ac.insert(221,6.3,170,5478)
    tsd = PowMr_Data("db/measure_powmr.db", "random")
    # tsd.delete_table()
    tsd.create_table()
    q = {}
    # for ent in col_names:
    #    if ent!='TIMESTAMP':
    #        q[ent]=0
    # tsd.insert(q)
    tsd.poll_value('http://ipnfofuxpslepnbjo.go.ro:5000/home_station', mock=False)
    # tsd.insert(1,42.3)
    print(tsd.extract_all_interval(""))
    print(tsd.getColumnNames())
    print(json.dumps(tsd.dbResptoDict(tsd.extract_all_interval(""), tsd.getColumnNames())))
    # tsd.convert_old()
    # td.insert(20,30)
    # print(ac.extract_last())
    # print(ac.extract_all_interval(2))
    pass
