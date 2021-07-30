import speedtest  

def run_test(tries=1):
    total=[]
    down_total=0
    up_total=0
    ping_total=0
    for i in range(tries):
        data={}
        st = speedtest.Speedtest()
        down=st.download()
        down_total+=down/1000000
        data["download"]=down/1000000
        up=st.upload()
        up_total+=up/1000000
        data["upload"]=up/1000000
        servernames =[]  
        st.get_servers(servernames)
        ping=st.results.ping
        ping_total+=ping
        data["ping"]=ping
        total.append(data)
    total.append({"download_average":down_total/tries,"upload_average":up_total/tries,"ping_average":ping_total/tries})
    return total
if __name__ == '__main__':
    run_test(3)
