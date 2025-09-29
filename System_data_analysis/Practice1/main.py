from abc import ABC, abstractmethod

class PsyHospital:
    pass
class Staff:
    pass
class HeadHosp:
    pass
class AdmHosp:
    pass
class WorkerHosp:
    pass
class RoomHosp:
    pass


class PsyHospital(ABC):
    pass

class Staff(PsyHospital):
    pass

class HeadHosp(Staff):
    def __init__(self, name: str, post: str):
        self.name = name
        self.post = post
        self.subs = []

    def print_subs(self):
        print(f"Подчинённые {self.name}({self.post}):")
        for obj in self.subs:
            print(f"\t{obj.name}\t({obj.post})")

    def find_boss(self, boss_name):
        if (self.boss.name == boss_name):
            return f"{self.boss.name} ({self.boss.post})"
        else:
            return None
    
    def find_staff (self, staff_name):
        for obj in self.subs:
            if (obj.name == staff_name):
                return f"{self.name} ({self.post}) управляет {obj.name} ({obj.post})"
            else:
                find_staff = obj.find_staff(staff_name)
                if (find_staff != None):
                    return f"{self.name} ({self.post}) управляет " + find_staff
        return None

class AdmHosp(Staff):
    def __init__(self, name: str, post: str, boss: HeadHosp):
        self.name = name
        self.post = post
        self.boss = boss
        self.subs = []
        boss.subs.append(self)

    def print_subs(self):
        print(f"Подчинённые {self.name}({self.post}):")
        for obj in self.subs:
            print(f"\t{obj.name}\t({obj.post})")

    def print_boss(self):
        print(f"{self.name} подчинён {self.boss.name}({self.boss.post})")

    def find_boss(self, boss_name):
        if (self.boss.name == boss_name):
            return f"{self.name} ({self.post}) подчиняется {self.boss.name} ({self.boss.post})"
        else:
            boss_of_boss = self.boss.find_boss(boss_name)
            if (boss_of_boss != None):
                return f"{self.name} ({self.post}) подчиняется " + boss_of_boss
            else:
                return None
            
    def find_staff (self, staff_name):
        for obj in self.subs:
            if (obj.name == staff_name):
                return f"{self.name} ({self.post}) управляет {obj.name} ({obj.post})"
            else:
                find_staff = obj.find_staff(staff_name)
                if (find_staff != None):
                    return f"{self.name} ({self.post}) управляет " + find_staff
        return None

class WorkerHosp(Staff):
    def __init__(self, name: str, post: str, boss: AdmHosp):
        self.name = name
        self.post = post
        self.boss = boss
        boss.subs.append(self)

    def print_boss(self):
        print(f"{self.name} подчинён {self.boss.name}({self.boss.post})")

    def find_boss(self, boss_name):
        if (self.boss.name == boss_name):
            return f"{self.name} ({self.post}) подчиняется {self.boss.name} ({self.boss.post})"
        else:
            boss_of_boss = self.boss.find_boss(boss_name)
            if (boss_of_boss != None):
                return f"{self.name} ({self.post}) подчиняется " + boss_of_boss
            else:
                return None
    
    def find_staff (self, staff_name):
        return None

class RoomHosp(PsyHospital):
    def __init__(self, name: str, boss: AdmHosp):
        self.name = name
        self.boss = boss
        self.post = "Помещение"
        boss.subs.append(self)

    def print_boss(self):
        print(f"{self.name} управляется {self.boss.name}({self.boss.post})")

    def find_boss(self, boss_name):
        if (self.boss.name == boss_name):
            return f"{self.name} управляется {self.boss.name} ({self.boss.post})"
        else:
            boss_of_boss = self.boss.find_boss(boss_name)
            if (boss_of_boss != None):
                return f"{self.name} управляется " + boss_of_boss
            else:
                return None
            
    def find_staff (self, staff_name):
        return None


if __name__ == '__main__':
    # Глава руководства
    Head =          HeadHosp("Иванов И.И.",     "Главный врач")

    # Руководство
    MainNurse =     AdmHosp("Долгова Д.Д.",     "Главная медсестра",        Head)
    HeadOfRooms =   AdmHosp("Дубинкин Д.Д.",    "Заведующий отделениями",   Head)
    HeadOfStaff =   AdmHosp("Рощин Р.Р.",       "Заведующий персоналом",    Head)

    # Штат
    Secur =         WorkerHosp("Листьев Л.Л.",  "Охранник",                 HeadOfStaff)
    MedBrat =       WorkerHosp("Петров П.П.",   "Санитар",                  MainNurse)
    Cleaner =       WorkerHosp("Сидоров С.С.",  "Уборщик",                  HeadOfStaff)
    Nurse =         WorkerHosp("Смирнова С.С.", "Медсестра",                MainNurse)

    # Помещения
    MainHall =      RoomHosp("Главный зал",         HeadOfRooms)
    MedRoom =       RoomHosp("Лечебная палата",     MainNurse)
    Reception =     RoomHosp("Приёмный зал",        HeadOfRooms)
    WalkingArea =   RoomHosp("Прогулочная зона",    HeadOfRooms)

    Head.print_subs()
    MainNurse.print_boss()
    WalkingArea.print_boss()

    print(WalkingArea.find_boss("Иванов И.И."))
    print(Head.find_staff("Приёмный зал"))