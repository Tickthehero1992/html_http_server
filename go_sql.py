import sqlite3
import math
import socket_server

import time
id_last = '123'

OPERATORS = {'+': (1, lambda x, y: x + y), '-': (1, lambda x, y: x - y),
             '*': (2, lambda x, y: x * y), '/': (2, lambda x, y: x / y),
             '^':(3, lambda  x,y:  math.pow(x,y)), 'sqrt':(3, lambda x: math.sqrt(x))
             }

class SQL:
    conn = sqlite3.connect('sensor.db')
        #  выставляем курсор
    cursor = conn.cursor()

    def __init__(self):
        pass

    def write_new_sensor(self, SensorID=id_last, SensorName='SensorNew', SensorMath='A+B', SensorType='Sensor228'): #запись нового датчика в таблицу
        # запись данных в таблицу
        new_sensor = SensorID, SensorName, SensorMath, SensorType
        print(new_sensor)
        #self.cursor.execute("""INSERT INTO sensors (SensorID,SensorName,SensorMath,SensorType)
                               #VALUES ('1','hui','huek','penis') """)
        self.cursor.execute("""INSERT INTO sensors (SensorID,SensorName,SensorMath,SensorType)
                     VALUES (?, ?, ?, ?) """, new_sensor)
        #

    def read_one_string(self): #чтение строки
        self.cursor.execute("""SELECT SensorID 
        FROM sensors""")
        hui = self.cursor.fetchall()
        print(hui)

    def commiting_sql(self): #подтверждение изменений в таблице БД
        # Если мы не просто читаем, но и вносим изменения в базу данных - необходимо сохранить транзакцию
        self.conn.commit()
        #
        self.conn.close()

    def take_parameter(self, Parameters_Name, Parameters_value):#поиск строки базы данных по кортежу параметров
        Number_of_parameter=len(Parameters_Name)
        Number_of_values = len(Parameters_value)
        if(Number_of_parameter==Number_of_values):
            string_to_command = ' '
            for i in range (Number_of_parameter):
                string_to_command += Parameters_Name[i]+ '='+"'" +Parameters_value[i]+"'"
                if(i<Number_of_parameter-1):
                    string_to_command+=' '+'AND'+' '
            command = 'SELECT * FROM sensors WHERE' + string_to_command
            self.cursor.execute(command)
            hui = self.cursor.fetchall()
           # print (hui)
            return hui
          #  print (command)
        else :

            pass
            return 0

    def formula_convert(self,formula,ADC): #преобразование формулы для рассчета параметра
        n=len(formula)
        Formula_string = ''
        for i in range(n):
            if formula[i] in 'ABCDEFXYZ':
                Formula_string += str(ADC)
            else:
                Formula_string+=formula[i]
        return (Formula_string)

    def find_USI(self, number):#поиск имени датчка по формуле
        command = 'SELECT * FROM Mesuarments WHERE USI=' + str(number)
        self.cursor.execute(command)
        h=self.cursor.fetchone()
        print(h[2])
        return h[2]

    def find_Sensor_Type(self, name_sensor):#поиск по имени датчика формулы
        command = 'SELECT * FROM sensors WHERE SensorName=' +"'"+name_sensor +"'"
        self.cursor.execute(command)
        h = self.cursor.fetchone()
        print(h[2])
        return h[2]

    def print_data_of_mesuarment(self, number, ADC): #обработка данных
        print (number)
        try:
            string_to_math = self.find_Sensor_Type(self.find_USI(number))
            Mesuarement = calc(shunting_yard(parse(self.formula_convert(string_to_math,ADC))))
            print(Mesuarement)
            Mesuarement_str = "'"+str(Mesuarement)+"'"
            command = """UPDATE Mesuarments SET Mesuarment_Data=? WHERE USI="""+ str(number)
            self.cursor.execute(command, (str(Mesuarement),))
        except:
            pass

def parse(formula_string): #парс сообщения
        number = ''
        for s in formula_string:
            if s in '1234567890.':  # если символ - цифра, то собираем число
                number += s
            elif number:  # если символ не цифра, то выдаём собранное число и начинаем собирать заново
                yield float(number)
                number = ''
            if s in OPERATORS or s in "()":  # если символ - оператор или скобка, то выдаём как есть
                yield s
        if number:  # если в конце строки есть число, выдаём его
            yield float(number)

def shunting_yard(parsed_formula):#преобразование
        stack = []  # в качестве стэка используем список
        for token in parsed_formula:
            # если элемент - оператор, то отправляем дальше все операторы из стека,
            # чей приоритет больше или равен пришедшему,
            # до открывающей скобки или опустошения стека.
            # здесь мы пользуемся тем, что все операторы право-ассоциативны
            if token in OPERATORS:
                while stack and stack[-1] != "(" and OPERATORS[token][0] <= OPERATORS[stack[-1]][0]:
                    yield stack.pop()
                stack.append(token)
            elif token == ")":
                # если элемент - закрывающая скобка, выдаём все элементы из стека, до открывающей скобки,
                # а открывающую скобку выкидываем из стека.
                while stack:
                    x = stack.pop()
                    if x == "(":
                        break
                    yield x
            elif token == "(":
                # если элемент - открывающая скобка, просто положим её в стек
                stack.append(token)
            else:
                # если элемент - число, отправим его сразу на выход
                yield token
        while stack:
            yield stack.pop()

def calc(polish): #подсчет
        stack = []
        for token in polish:
            if token in OPERATORS:  # если приходящий элемент - оператор,
                y, x = stack.pop(), stack.pop()  # забираем 2 числа из стека
                stack.append(OPERATORS[token][1](x, y)) # вычисляем оператор, возвращаем в стек
            else:
                stack.append(token)
        return stack[0] # результат вычисления - единственный элемент в стеке


def Main(Data1, Data2):
    DataBase = SQL()  # объявление экземпляра класса

    DataBase.print_data_of_mesuarment(Data1, Data2)
    DataBase.commiting_sql()  # подтверждение всех операций



if __name__=='__main__': #тест функций

    DataBase = SQL() #объявление экземпляра класса
    socket_server.Main()
    #DataBase.write_new_sensor()#запись нового датчика в БД
    #hui=DataBase.take_parameter(['SensorID','SensorName'], ['1', 'hui']) #поиск строки по параметрам
    #print (hui) DataBase.print_data_of_mesuarment(socket_server.ADRES, socket_server.Parameter)
   # print(calc(shunting_yard(parse('2^2'))))
    #print(calc(shunting_yard(parse(DataBase.formula_convert('192*A+5',1)))))
    #DataBase.take_formula('234*A+3',1)
    #DataBase.find_USI(228)
    #DataBase.find_Sensor_Type('PH')

    while True:

        DataBase.print_data_of_mesuarment(socket_server.ADRES, socket_server.Parameter)
        time.sleep(1)
    DataBase.commiting_sql() #подтверждение всех операций

