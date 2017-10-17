import psutil
#function of Get CPU State    
def getCPUstate(interval=1):    
    return (" CPU: " + str(psutil.cpu_percent(interval)) + "%")