import datetime
import time


def create_file():
    filename = "Mesuartment_logs" + str(datetime.datetime.now().year)+str(datetime.datetime.now().month)+str(datetime.datetime.now().day)+str(datetime.datetime.now().hour)+str(datetime.datetime.now().minute)+ '.csv'
    print(filename)
    return filename

def create_write_line(data1,data2,data3,data4,data5, file): # ":ID_USI,ID_Sensor,ADC_param,Mesuare,Le_Si,MesuredTime;"
    Line_to_go = ':'+str(data1)+','+str(data2)+','+str(data3)+','+str(data4)+','+str(data5)+','+str(datetime.datetime.now())+';'
    file.write(Line_to_go+'\n')

def Main_logging(filename,data1,data2,data3,data4,data5,Time_in_minut):
    log=open(filename,'w')
    time_start = datetime.datetime.now().minute
    print  (time_start)
    while ((datetime.datetime.now().minute - time_start)<Time_in_minut):
        print(datetime.datetime.now().minute)
        #create_write_line(data1,data2,data3,data4,data5,log)
        create_write_line(data1, data2, data3, data4, data5, log)
        time.sleep(2)
    print("End_Log")
    log.close()


if __name__=='__main__':
    naming = create_file()
    print(str(datetime.datetime.now()))
    Main_logging(naming,1,2,3,4,5,1)