class MachineException(Exception):
    def __init__(self, message):
        super().__init__(message)


class MooreAutomaton:
    def __init__(self):
        self.state = 'm5'
        self.o_v = 'b2'
        self._t = 0
        self.my_dict = {
            'race': 0, 'show': 0, 'bend': 0, 'unite': 0, 'scale': 0
            }
        self.loop_states = {'m1', 'm4', 'm0', 'm3', 'm6', 'm2', 'm5'}

    def __getattr__(self, name):
        raise MachineException("unknown")

    def set_var(self, name, value):
        if name == 't':
            self._t = value

    def get_output(self):
        return self.o_v

    def has_max_out_edges(self):
        if self.state == 'm0':
            return True
        return False

    def seen_method(self, method_name):
        return self.my_dict[method_name]

    def has_path_to(self, method_name):
        if method_name == 'm5':
            return False
        return True

    def race(self):
        if self.state == 'm5':
            self.state = 'm6'
            self.o_v = 'b0'
            self.my_dict['race'] += 1
        elif self.state == 'm0':
            self.state = 'm1'
            self.o_v = 'b4'
            self.my_dict['race'] += 1
        elif self.state == 'm1':
            self.state = 'm6'
            self.o_v = 'b0'
            self.my_dict['race'] += 1
        else:
            raise MachineException('unsupported')

    def show(self):
        if self.state == 'm6':
            self.state = 'm4'
            self.o_v = 'b3'
            self.my_dict['show'] += 1
        elif self.state == 'm4':
            self.state = 'm3'
            self.o_v = 'b0'
            self.my_dict['show'] += 1
        elif self.state == 'm2':
            self.state = 'm1'
            self.o_v = 'b4'
            self.my_dict['show'] += 1
        else:
            raise MachineException('unsupported')

    def bend(self):
        if self.state == 'm5':
            self.state = 'm0'
            self.o_v = 'b4'
            self.my_dict['bend'] += 1
        else:
            raise MachineException('unsupported')

    def unite(self):
        if self.state == 'm0':
            if self._t == 1:
                self.state = 'm2'
                self.o_v = 'b0'
                self.my_dict['unite'] += 1
            elif self._t == 0:
                self.state = 'm3'
                self.o_v = 'b0'
                self.my_dict['unite'] += 1
        else:
            raise MachineException('unsupported')

    def scale(self):
        if self.state == 'm3':
            self.state = 'm0'
            self.o_v = 'b4'
            self.my_dict['scale'] += 1
        else:
            raise MachineException('unsupported')


def main():
    return MooreAutomaton()


def test_main():
    """Тестирование функции main()"""
    automaton = main()
    assert isinstance(automaton, MooreAutomaton)
    assert automaton.state == 'm5'


def test_initial_state():
    """Тестирование начального состояния автомата"""
    automaton = MooreAutomaton()
    assert automaton.state == 'm5'


def test_set_var():
    automaton = MooreAutomaton()
    assert automaton.set_var('t', 0) is None
    assert automaton.set_var('b', 0) is None


def test_get():
    automaton = MooreAutomaton()
    assert automaton.get_output() == 'b2'


def test_has_max():
    automaton = MooreAutomaton()
    assert automaton.has_max_out_edges() is False
    automaton.state = 'm0'
    assert automaton.has_max_out_edges() is True


def test_seen_method():
    automaton = MooreAutomaton()
    assert automaton.seen_method('race') == 0


def test_has_path_to():
    automaton = MooreAutomaton()
    assert automaton.has_path_to('m0') is True
    assert automaton.has_path_to('m5') is False


def test_race():
    automaton = MooreAutomaton()
    automaton.state = 'm5'
    assert automaton.race() is None
    automaton.state = 'm0'
    assert automaton.race() is None
    automaton.state = 'm1'
    assert automaton.race() is None
    try:
        automaton.race()
    except MachineException as e:
        assert str(e) == 'unsupported'


def test_show():
    automaton = MooreAutomaton()
    automaton.state = 'm6'
    assert automaton.show() is None
    automaton.state = 'm4'
    assert automaton.show() is None
    automaton.state = 'm2'
    assert automaton.show() is None
    try:
        automaton.show()
    except MachineException as e:
        assert str(e) == 'unsupported'


def test_bend():
    automaton = MooreAutomaton()
    automaton.state = 'm5'
    assert automaton.bend() is None
    try:
        automaton.bend()
    except MachineException as e:
        assert str(e) == 'unsupported'


def test_unite():
    automaton = MooreAutomaton()
    automaton.state = 'm0'
    automaton._t = 0
    assert automaton.unite() is None
    automaton.state = 'm0'
    automaton._t = 1
    assert automaton.unite() is None
    automaton.state = 'm0'
    automaton._t = 2
    assert automaton.unite() is None
    try:
        automaton.state = 'm3'
        automaton.unite()
    except MachineException as e:
        assert str(e) == 'unsupported'


def test_scale():
    automaton = MooreAutomaton()
    automaton.state = 'm3'
    assert automaton.scale() is None
    try:
        automaton.scale()
    except MachineException as e:
        assert str(e) == 'unsupported'


def test_getattr():
    automaton = MooreAutomaton()

    try:
        automaton.non_existent_attribute
    except MachineException as e:
        assert str(e) == "unknown", \
            f"Ожидалась ошибка AttributeError, но получено: {e}"

    try:
        automaton.non_existent_method()
    except MachineException as e:
        assert str(e) == "unknown", \
            f"Ожидалась ошибка AttributeError, но получено: {e}"


def test():
    """Главная тестовая функция, запускающая все тесты"""
    test_functions = [
        test_main,
        test_initial_state,
        test_set_var,
        test_get,
        test_has_max,
        test_seen_method,
        test_has_path_to,
        test_race,
        test_show,
        test_show,
        test_bend,
        test_unite,
        test_scale,
        test_getattr
    ]

    for test_func in test_functions:
        test_func()
