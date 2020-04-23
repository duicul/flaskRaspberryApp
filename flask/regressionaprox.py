import numpy as np
import json
import traceback
import requests
import datetime
import time
import os
import random
import concurrent.futures
import math

def extract_country_data_covid19(country,case_type):
    xaux=[]
    yaux=[]
    ygrowa=[]
    ygrowch=[]
    cnt=0
    init=0
    date_init=None
    prev_app=0
    prev_app_gr=0
    remove0_conf="Confirmed"
    #print(case_type)
    try:
        if case_type=="Active":
            r = requests.get('https://api.covid19api.com/live/country/'+country+'/status/active')
            remove0_conf="Confirmed"
        elif case_type=="Confirmed":
            r = requests.get('https://api.covid19api.com/dayone/country/'+country+'/status/confirmed/live')
            remove0_conf="Cases"
            case_type="Cases"
        else:
            return (xaux,yaux,ygrowa,ygrowch,country,case_type)
    except:
        return (xaux,yaux,ygrowa,ygrowch,country,case_type)
    if country=="united-states" or country=="china":
        for rec in r.json():
            d=datetime.datetime.strptime(rec["Date"], "%Y-%m-%dT%H:%M:%SZ")
            if date_init != None and date_init.year == d.year and  date_init.month == d.month and date_init.day == d.day:
                init+=abs(int(rec[case_type]))
            else :
                #init+=rec[data_type]
                xaux.append(d)
                yaux.append(abs(init))
                ygrowa.append(init-prev_app)
                curr_grow=init-prev_app
                ygrowch.append(curr_grow-prev_app_gr)
                prev_app_gr=curr_grow
                prev_app=init
                init=0
                date_init=d
    else:
        for rec in r.json():
            #print(remove0_conf)
            if int(rec[remove0_conf]) == 0:
                continue
            try:
                prov=rec["Province"]
                if len(rec["Province"])!=0:
                    continue
            except KeyError:
                pass
            d=datetime.datetime.strptime(rec["Date"], "%Y-%m-%dT%H:%M:%SZ")
            xaux.append(d)
            yaux.append(abs(rec[case_type]))
            curr_grow=rec[case_type]-prev_app
            ygrowa.append(curr_grow)
            ygrowch.append(curr_grow-prev_app_gr)
            prev_app_gr=curr_grow
            prev_app=abs(rec[case_type])
    if len(xaux)>0:
        xaux.pop()
    if len(yaux)>0:
        yaux.pop()
    if len(ygrowa)>0:
        ygrowa.pop()
    if len(ygrowch)>0:
        ygrowch.pop()
        
    return (xaux,yaux,ygrowa,ygrowch,country,case_type)


def extract_country_data_geospatial(case_type):
    xaux=[]
    yaux=[]
    ygrowa=[]
    ygrowch=[]
    cnt=0
    init=0
    date_init=None
    prev_app=0
    prev_app_gr=0
    remove0_conf="Confirmed"
    #print(case_type)
    r = requests.get('https://covid19.geo-spatial.org/api/dashboard/getDailyCases')
    try:
        simple=True
        if case_type=="Active":
            case_type="Cazuri active"
        elif case_type=="Confirmed":
            case_type="Total"
        elif case_type=="Recuperated":
            case_type="Vindecati"
        elif case_type=="Dead":
            case_type="Morti"
        elif case_type=="Tests":
            case_type="Nr de teste"
        elif case_type=="TestsperCase":
            simple=False
            pass
        else:
            return (xaux,yaux,ygrowa,ygrowch,"romania",case_type)
    except:
        return (xaux,yaux,ygrowa,ygrowch,country,case_type)
    for rec in r.json()["data"]["data"]:
            d=datetime.datetime.strptime(rec["Data"], "%Y-%m-%d")
            xaux.append(d)
            if simple and rec[case_type]==None:
                curr_val=0
            if case_type=="TestsperCase":
                test_no=abs(rec["Nr de teste pe zi"]) if rec["Nr de teste pe zi"]!=None else 0
                curr_val=(test_no/abs(rec["Cazuri"])) if  test_no!=0 else abs(rec["Cazuri"])
            else :
                curr_val=abs(rec[case_type]) if rec[case_type] != None else 0
            yaux.append(curr_val)
            if case_type=="TestsperCase":
                ygrowa.append(curr_val)
                ygrowch.append(curr_val)
                continue
            curr_grow=curr_val-prev_app
            ygrowa.append(curr_grow)
            ygrowch.append(curr_grow-prev_app_gr)
            prev_app_gr=curr_grow
            prev_app=curr_val
      
    return (xaux,yaux,ygrowa,ygrowch,"romania",case_type)


def extract_countries_data(countries,case_type,api):
    x=[]
    y=[]
    ygrow=[]
    ygrowchange=[]
    threads=[]
    print("extract data "+str(api))
    if api=="covid19api":
        for c in countries:
            print(c)
            with concurrent.futures.ThreadPoolExecutor() as executor:
                t1 = executor.submit(extract_country_data_covid19,c,case_type)
            threads.append(t1)
    elif api=="geospatial":
        with concurrent.futures.ThreadPoolExecutor() as executor:
            t1 = executor.submit(extract_country_data_geospatial,case_type)
        threads.append(t1)
    return join_threads(threads)

def join_threads(thread_list):
    x=[]
    y=[]
    ygrow=[]
    ygrowch=[]
    case_type=[]
    countries=[]
    for thread in thread_list:
        while not thread.done():
                pass
        (x1,y1,ygrow1,ygrowch1,country1,case_type1)=thread.result()
        x.append(x1)
        y.append(y1)
        ygrow.append(ygrow1)
        ygrowch.append(ygrowch1)
        case_type.append(case_type1)
        countries.append(country1)
    #print(x)
    #print(y)
    #print(ygrow)
    #print(ygrowch)
    return (x,y,ygrow,ygrowch,countries)

def convert_to_js(x,y):
    #print(x)
    #print(y)
    data="["
    for i in range(len(x)):
        data+="{x:new Date('"+str(x[i])+"'),y:"+str(y[i])+"},"
    data+="]"
    return data
        
def data_point(datapoint,name):
    return "{type: 'line',dataPoints:"+str(datapoint)+",name: '"+str(name)+"',showInLegend: true}"

def aggregate_data(pol_grade,countries,data_type,case_type,predict_len,api):
    (x,y,ygrow,ygrowch,countries)=extract_countries_data(countries,case_type,api)
    #print(x)
    ret_data="["
    predict_len=int(predict_len)
    pol_grade=int(pol_grade)
    #print(countries)
    for i in range(len(x)):
        if len(x[i])==0:
            continue
        curr_data=[]
        initdate=x[i][0]
        datasetlen=len(x[i])
        
        #print(initdate + datetime.timedelta(days=1))
        daterange=[(initdate + datetime.timedelta(days=xi)) for xi in range(datasetlen+predict_len)]
        if data_type=="data":
            curr_data.append(data_point(convert_to_js(x[i],y[i]),str(countries[i])+"_"+str(data_type)+"_"+str(case_type)))
            if pol_grade>0:
                poly_fit = np.poly1d(np.polyfit(range(datasetlen),y[i],pol_grade))
                pol_regr_y=[poly_fit(xi) for xi in range(datasetlen+predict_len)]
                curr_data.append(data_point(convert_to_js(daterange,pol_regr_y),str(countries[i])+"regression"+str(pol_grade)+"_"+str(data_type)+"_"+str(case_type)))
                                     
        elif data_type=="growth":
            data_point(convert_to_js(x,ygrow),str(countries[i])+"_"+str(data_type)+"_"+str(case_type))
            curr_data.append(data_point(convert_to_js(x[i],ygrow[i]),str(countries[i])+"_"+str(data_type)+"_"+str(case_type)))
            if pol_grade>0:
                poly_fit = np.poly1d(np.polyfit(range(datasetlen),ygrow[i],pol_grade))
                pol_regr_ygrow=[poly_fit(xi) for xi in range(datasetlen+predict_len)]
                curr_data.append(data_point(convert_to_js(daterange,pol_regr_ygrow),str(countries[i])+"regression"+str(pol_grade)+"_"+str(data_type)+"_"+str(case_type)))

        elif data_type=="growth_change":
            curr_data.append(data_point(convert_to_js(x[i],ygrowch[i]),str(countries[i])+"_"+str(data_type)+"_"+str(case_type)))
            if pol_grade>0:
                poly_fit = np.poly1d(np.polyfit(range(datasetlen),ygrowch[i],pol_grade))
                pol_regr_ygrowch=[poly_fit(xi) for xi in range(datasetlen+predict_len)]
                curr_data.append(data_point(convert_to_js(daterange,pol_regr_ygrowch),str(countries[i])+"regression"+str(pol_grade)+"_"+str(data_type)+"_"+str(case_type)))
        #print(curr_data)
        for d1 in curr_data:
            ret_data+=d1+","
    ret_data+="]"
    #print(ret_data)
    return str(ret_data)

if __name__ == "__main__":
    print(aggregate_data(1,["austria"],"growth","Confirmed",1,"covid19"))
