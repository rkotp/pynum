def write_in_file(message):

    # IMPORTS
    import pathlib
    import datetime
    
    # OPEN THE FILE TO APPEND
    filename = str(pathlib.Path(__file__).parent.parent.absolute()) + "/pynum.log"
    f = open(filename, "a")

    # GET THE DATETIME
    year = str(datetime.datetime.now().year)
    month_aux = datetime.datetime.now().month
    if ( month_aux < 10 ):
        month = "0"
    else:
        month = ""
    month = month + str(month_aux)
    day_aux = datetime.datetime.now().day
    if ( day_aux < 10 ):
        day = "0"
    else:
        day = ""
    day = day + str(day_aux)
    hour_aux = datetime.datetime.now().hour
    if ( hour_aux < 10 ):
        hour = "0"
    else:
        hour = ""
    hour = hour + str(hour_aux)
    minute_aux = datetime.datetime.now().minute
    if ( minute_aux < 10 ):
        minute = "0"
    else:
        minute = ""
    minute = minute + str(minute_aux)
    second_aux = datetime.datetime.now().second
    if ( second_aux < 10 ):
        second = "0"
    else:
        second = ""
    second = second + str(second_aux)
    str_date = " [ " + month + "/" + day + "/" + year + " - " + hour + ":" + minute + ":" + second + " ] "

    # WRITE THE DATETIME AND THE MESSAGE
    f.write("[*]" + str_date + message + "\n")

    # CLOSE THE FILE
    f.close()