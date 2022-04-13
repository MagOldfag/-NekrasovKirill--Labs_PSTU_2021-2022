
class Engine:           #Класс двигателей

    def __init__(self,name):
        self.name = name

class Servo(Engine):    #Класс Сервомоторов

    def __init__ (self,name,speed):
        super().__init__(name)
        self.speed = speed

    def __str__(self):
        return f"Наименование: {self.name}\nскорость вращения: {self.speed}"
    
    def __repr__(self):
        return f"Servo({self.name}, {self.speed})"
    
    def __eq__(self,other):
        return self.speed==other.speed

    def __lt__(self,other):
        return self.speed<other.speed

    def __le__(self,other):
        return self.speed<=other.speed

class Stepper(Engine):      #Класс шаговых двигателей

    def __init__(self,name,step):
        super().__init__(name)
        self.step = step

    def __str__(self):
        return f'Наменование: {self.name}\nшаг: {self.step}'

    def __repr__(self):
        return f'Stepper({self.name}, {self.step})'

    def __eq__(self,other):
        return self.step==other.step

    def __lt__(self,other):
        return self.step<other.step

    def __le__(self,other):
        return self.step<=other.step

class Unit:         #Класс звеньев манипулятора

    special_names = {'Поступательное':1,'Вращательное':2,'Рабочий орган':3}

    def __init__(self,type,left_part,right_part):
        self.type = type
        self.left_part = left_part
        self.right_part = right_part

    def __str__(self):
        return f'Тип звена: {self.type}\nЛевая часть: {self.left_part}\nПравая часть: {self.right_part}'

    def __repr__(self):
        return f'Unit({self.type}, {self.left_part}, {self.right_part})'
    
    def  __lt__(self,other):
        type_point_other = Unit.special_names.get(other.type)
        type_point_self = Unit.special_names.get(self.type)
        if type_point_other == 3:
            return type_point_self<type_point_other
        else:
            return False

class Manipulator:      #Класс манпуляторов

    def __init__(self, name, robot_type,*args):
        self.name = name
        self.robot_type = robot_type
        self.units = []
        for unit in args:
            self.units.append(unit)
        self.n = len(args)

    def __str__(self):
        for unit in self.units:
            print(unit)
        return f'Модель манипулятора: {self.name}\nТип манипулятора: {self.robot_type}\nКоличество звеньев: {self.n}'
    def __repr__(self):
        return f'Manipulator({self.name}, {self.robot_type}, {self.units})'
    def __eq__(self,other):
        return self.n==other.n

    def __lt__(self,other):
        return self.n<other.n

    def __le__(self,other):
        return self.n<=other.n

import datetime

if __name__ == '__main__':
  d = datetime.date.today()
  print(str(d))
  print(repr(d))
serv1 = Servo('Fukuta SB', 30)
serv2 = Servo('KEB F6',60)
stepper1 = Stepper('17HS4401', 3)
stepper2 = Stepper('57HS76', 3)
unit_1 = Unit('Поступательное', serv1, serv2)
unit_2 = Unit('Вращательное', serv2, stepper1)
unit_3 = Unit('Рабочий орган', stepper1,'Захват')
manipula1 = Manipulator('Манипула 1','Погрузочный',unit_1,unit_2,unit_3)
print(repr(manipula1))
