class MealyException(Exception):
    def __init__(self, message):
        super().__init__(message)


class MealyAutomaton:
    def __init__(self):
        self.state = 'z6'
        self._x = 0
        self._u = 0
        self._m = 0
        self.visited_methods = set()
        self.step_counter = 0

        self.loop_states = {'z1', 'z4', 'z0', 'z3', 'z6', 'z7', 'z2', 'z5'}

    def get_step(self):
        return self.step_counter

    def seen_method(self, method_name):
        return method_name in self.visited_methods

    def part_of_loop(self):
        return self.state in self.loop_states

    def x(self, value):
        self._x = value

    def u(self, value):
        self._u = value

    def m(self, value):
        self._m = value

    def state_z0(self, method_name):
        if method_name == 'hurry':
            self.state = 'z3'
            self.step_counter += 1
            self.visited_methods.add(method_name)
            return 'J1'
        else:
            raise MealyException('unsupported')

    def state_z1(self, method_name):
        if method_name == 'scan':
            self.step_counter += 1
            self.visited_methods.add(method_name)
            return 'J0'
        if method_name == 'hurry':
            if self._u == 0:
                self.state = 'z5'
            elif self._u == 1:
                self.state = 'z4'
            self.step_counter += 1
            self.visited_methods.add(method_name)
            return 'J0'
        else:
            raise MealyException('unsupported')

    def state_z2(self, method_name):
        if method_name == 'build':
            self.state = 'z5'
            self.step_counter += 1
            self.visited_methods.add(method_name)
            return 'J2'
        else:
            raise MealyException('unsupported')

    def state_z3(self, method_name):
        if method_name == 'tread':
            self.state = 'z6'
            self.step_counter += 1
            self.visited_methods.add(method_name)
            return 'J2'
        else:
            raise MealyException('unsupported')

    def state_z4(self, method_name):
        if method_name == 'pull':
            if self._x == 0:
                self.state = 'z0'
                self.step_counter += 1
                self.visited_methods.add(method_name)
                return 'J1'
            elif self._x == 1:
                self.state = 'z6'
                self.step_counter += 1
                self.visited_methods.add(method_name)
                return 'J2'
        else:
            raise MealyException('unsupported')

    def state_z5(self, method_name):
        if method_name == 'build':
            if self._m == 0:
                self.state = 'z1'
            elif self._m == 1:
                self.state = 'z3'
            self.step_counter += 1
            self.visited_methods.add(method_name)
            return 'J3'
        else:
            raise MealyException('unsupported')

    def state_z6(self, method_name):
        if method_name == 'hurry':
            self.state = 'z7'
            self.step_counter += 1
            self.visited_methods.add(method_name)
            return 'J3'
        else:
            raise MealyException('unsupported')

    def state_z7(self, method_name):
        if method_name == 'tread':
            self.state = 'z2'
            self.step_counter += 1
            self.visited_methods.add(method_name)
            return 'J3'
        else:
            raise MealyException('unsupported')

    def run(self, method_name):
        if method_name not in ['hurry', 'tread', 'build', 'pull', 'scan']:
            raise MealyException('unknown')

        if (self.state == 'z0'):
            return self.state_z0(method_name)

        elif (self.state == 'z1'):
            return self.state_z1(method_name)

        elif (self.state == 'z2'):
            return self.state_z2(method_name)

        elif (self.state == 'z3'):
            return self.state_z3(method_name)

        elif (self.state == 'z4'):
            return self.state_z4(method_name)

        elif (self.state == 'z5'):
            return self.state_z5(method_name)

        elif (self.state == 'z6'):
            return self.state_z6(method_name)

        else:
            return self.state_z7(method_name)


def main():
    return MealyAutomaton()


def test_main():
    """Тестирование функции main()"""
    automaton = main()
    assert isinstance(automaton, MealyAutomaton)
    assert automaton.state == 'z6'
    assert automaton.get_step() == 0
    assert automaton.part_of_loop()


def test_initial_state():
    """Тестирование начального состояния автомата"""
    automaton = MealyAutomaton()
    assert automaton.state == 'z6'
    assert automaton.get_step() == 0
    assert automaton.part_of_loop()


def test_seen_method():
    """Тестирование метода seen_method()"""
    automaton = MealyAutomaton()
    assert not automaton.seen_method('hurry')
    automaton.run('hurry')
    assert automaton.seen_method('hurry')
    assert not automaton.seen_method('tread')


def test_part_of_loop():
    """Тестирование метода part_of_loop()"""
    automaton = MealyAutomaton()
    automaton.state = 'z1'
    assert automaton.part_of_loop()
    automaton.state = 'z4'
    assert automaton.part_of_loop()
    automaton.state = 'invalid_state'
    assert not automaton.part_of_loop()


def test_setters():
    """Тестирование методов установки значений (x, u, m)"""
    automaton = MealyAutomaton()
    assert automaton._x == 0
    assert automaton._u == 0
    assert automaton._m == 0

    automaton.x(5)
    automaton.u(10)
    automaton.m(15)
    assert automaton._x == 5
    assert automaton._u == 10
    assert automaton._m == 15

    automaton.x(0)
    automaton.u(0)
    automaton.m(0)
    assert automaton._x == 0
    assert automaton._u == 0
    assert automaton._m == 0

    automaton.x(-1)
    automaton.u(-2)
    automaton.m(-3)
    assert automaton._x == -1
    assert automaton._u == -2
    assert automaton._m == -3


def test_unknown_method():
    """Тестирование обработки неизвестного метода"""
    automaton = MealyAutomaton()
    try:
        automaton.run('unknown')
    except MealyException as e:
        assert str(e) == 'unknown'


def test_z0_state():
    """Тестирование состояния z0"""
    automaton = MealyAutomaton()
    automaton.state = 'z0'
    try:
        automaton.run('scan')
    except MealyException as e:
        assert str(e) == 'unsupported'
    assert automaton.run('hurry') == 'J1'


def test_z1_state():
    """Тестирование состояния z1"""
    automaton = MealyAutomaton()
    automaton.state = 'z1'
    try:
        automaton.run('build')
    except MealyException as e:
        assert str(e) == 'unsupported'
    assert automaton.run('scan') == 'J0'

    automaton._u = 0
    assert automaton.run('hurry') == 'J0'

    automaton.state = 'z1'
    automaton._u = 1
    assert automaton.run('hurry') == 'J0'

    automaton.state = 'z1'
    automaton._u = 2
    assert automaton.run('hurry') == 'J0'


def test_z2_state():
    """Тестирование состояния z2"""
    automaton = MealyAutomaton()
    automaton.state = 'z2'
    try:
        automaton.run('scan')
    except MealyException as e:
        assert str(e) == 'unsupported'
    assert automaton.run('build') == 'J2'


def test_z3_state():
    """Тестирование состояния z3"""
    automaton = MealyAutomaton()
    automaton.state = 'z3'
    try:
        automaton.run('scan')
    except MealyException as e:
        assert str(e) == 'unsupported'
    assert automaton.run('tread') == 'J2'


def test_z4_state():
    """Тестирование состояния z4"""
    automaton = MealyAutomaton()
    automaton.state = 'z4'
    try:
        automaton.run('scan')
    except MealyException as e:
        assert str(e) == 'unsupported'

    automaton._x = 0
    assert automaton.run('pull') == 'J1'

    automaton.state = 'z4'
    automaton._x = 1
    assert automaton.run('pull') == 'J2'

    automaton.state = 'z4'
    automaton._x = 3
    assert automaton.run('pull') is None


def test_z5_state():
    """Тестирование состояния z5"""
    automaton = MealyAutomaton()
    automaton.state = 'z5'
    try:
        automaton.run('scan')
    except MealyException as e:
        assert str(e) == 'unsupported'

    automaton._m = 0
    assert automaton.run('build') == 'J3'

    automaton.state = 'z5'
    automaton._m = 1
    assert automaton.run('build') == 'J3'

    automaton.state = 'z5'
    automaton._m = 3
    assert automaton.run('build') == 'J3'


def test_z6_state():
    """Тестирование состояния z6"""
    automaton = MealyAutomaton()
    automaton.state = 'z6'
    try:
        automaton.run('scan')
    except MealyException as e:
        assert str(e) == 'unsupported'
    assert automaton.run('hurry') == 'J3'


def test_z7_state():
    """Тестирование состояния z7"""
    automaton = MealyAutomaton()
    automaton.state = 'z7'
    try:
        automaton.run('scan')
    except MealyException as e:
        assert str(e) == 'unsupported'
    assert automaton.run('tread') == 'J3'


def test():
    """Главная тестовая функция, запускающая все тесты"""
    test_functions = [
        test_main,
        test_initial_state,
        test_seen_method,
        test_part_of_loop,
        test_setters,
        test_unknown_method,
        test_z0_state,
        test_z1_state,
        test_z2_state,
        test_z3_state,
        test_z4_state,
        test_z5_state,
        test_z6_state,
        test_z7_state
    ]

    for test_func in test_functions:
        test_func()





'''
obj = main()
# print(obj.run('fade')) # MealyException: 'unknown'
print(obj.m(0)) # None
# print(obj.run('tread')) # MealyException: 'unsupported'
print(obj.part_of_loop()) # True
print(obj.get_step()) # 0
print(obj.u(0)) # None
# print(obj.run('tread')) # MealyException: 'unsupported'
print(obj.seen_method('build')) # False
print(obj.run('hurry')) # 'J3'
print(obj.run('tread')) # 'J3'
print(obj.run('build')) # 'J2'
print(obj.run('build')) # 'J3'
print(obj.part_of_loop()) # True
print(obj.m(1)) # None
print(obj.run('hurry')) # 'J0'
print(obj.run('build')) # 'J3'
# print(obj.run('pull')) # MealyException: 'unsupported'
print(obj.part_of_loop()) # True
print(obj.run('tread')) # 'J2'
print(obj.run('hurry')) # 'J3'
print(obj.part_of_loop()) # True
print(obj.run('tread')) # 'J3'
# print(obj.run('pull')) # MealyException: 'unsupported'
'''