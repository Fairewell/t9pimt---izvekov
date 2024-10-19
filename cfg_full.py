import random
import logging
import time

# Настройка логирования
logging.basicConfig(
    filename='cfg_generations.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class CFG:
    """
    Класс для работы с контекстно-свободной грамматикой (CFG).

    Этот класс загружает правила из файла, генерирует строки на основе этих правил
    и проверяет, являются ли сгенерированные строки допустимыми согласно грамматике.

    Атрибуты
    ----------
        rules (dict) : Словарь правил продукции, где ключи - нетерминалы, 
                      а значения - списки возможных преобразований.
        terminals (set): Множество терминалов грамматики.
        variables (set): Множество нетерминалов грамматики.
        start_variable (str): Стартовый символ (нетерминал) для генерации строк.
        max_depth (int): Максимальная глубина рекурсии при генерации строк.
        max_length (int): Максимальная длина генерируемой строки.
        end_symbol (str): Символ, добавляемый в конец генерируемой строки.
        generate_counter (int): Счетчик попыток генерации строк.
        generation_steps (int): Количество шагов, выполненных во время генерации.
        validation_steps (int): Количество шагов, выполненных при проверке строки.
        comment (str): Комментарий из файла правил.

    Методы
    ----------
        load_rules(rules_file): Загружает правила из указанного файла.
        generate(symbol=None, depth=0): Генерирует строку, начиная с указанного символа.
        is_valid_string(string): Проверяет, является ли указанная строка допустимой.
    
    Использование
    ----------
        cfg = CFG(rules_file) # Путь к файлу с правилами
        cfg.generate()
    """
    
    def __init__(self, rules_file, max_depth=10):
        """
        Инициализирует объект CFG, загружая правила из указанного файла.

        Параметры:
        ----------
            rules_file (str): Путь к файлу с правилами.
            max_depth (int): Максимальная глубина рекурсии (по умолчанию 10).
        """
        self.rules = {}
        self.terminals = set()
        self.variables = set()
        self.start_variable = None
        self.max_depth = max_depth
        self.max_length = 50
        self.end_symbol = '.'
        self.load_rules(rules_file)
        self.generate_counter = 0
        self.generation_steps = 0
        self.validation_steps = 0
        self.comment = ''
        logging.info('CFG initialized with rules from %s', rules_file)

    def load_rules(self, rules_file):
        """
        Загружает правила из указанного файла.

        Параметры
        ----------
            rules_file (str): Путь к файлу с правилами.

        Исключения
        ----------
            ValueError: Если в файле отсутствуют правила продукции (Pn).
        """
        with open(rules_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        section = None
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                self.comment = line
                print(self.comment)    
                continue
            
            if line.startswith('env:'):
                section = 'env'

            if line.startswith('G'):
                # Извлечение терминалов, нетерминалов, стартового символа и максимальной длины
                section = 'G'
                term_start = line.find('{') + 1
                term_end = line.find('}')
                variables_start = line.find('{', term_end) + 1
                variables_end = line.find('}', term_end)
                self.terminals = set(line[term_start:term_end].split(', '))
                self.variables = set(line[variables_start:variables_end].split(', '))
                continue

            if line.startswith('Pn:'):
                section = 'Pn'
                continue

            if line.startswith('Pt:'):
                section = 'Pt'
                continue

            if section == 'Pn':
                # Парсинг правил для нетерминалов
                left, right = line.split('->')
                non_terminal = left.strip()
                transformations = [r.strip() for r in right.split('|')]
                self.rules[non_terminal] = transformations
                if self.start_variable is None:
                    self.start_variable = non_terminal  # Первый нетерминал становится стартовым

            elif section == 'Pt':
                # Парсинг правил для терминалов
                left, right = line.split('->')
                terminal = left.strip()
                self.rules[terminal] = [r.strip() for r in right.split('|')]

            elif section == 'env':
                # Извлечение стартового символа, максимальной длины и символа окончания из секции env
                parts = line[4:].strip().split('|')
                if len(parts) > 0:
                    self.start_variable = parts[0].strip() if parts[0] else None
                    print(f"Start symbol from env: {self.start_variable}")
                if len(parts) > 1:
                    self.max_length = int(parts[1].strip()) if parts[1] else 50
                    print(f"Max length from env: {self.max_length}")
                if len(parts) > 2:
                    self.end_symbol = parts[2].strip() if parts[2] else '.'
                    print(f"End symbol from env: {self.end_symbol}")
                continue

        # Проверка наличия правил Pn и Pt
        if not self.rules:
            raise ValueError(f'В файле {rules_file} отсутствуют правила продукции (Pn).')

        if section == 'Pt' and not self.rules.get('Pt'):
            logging.warning(f'В файле {rules_file} отсутствуют правила для терминалов (Pt).')

        # Логирование загруженных правил
        logging.info('Loaded rules: %s', self.rules)
        logging.info('Terminals: %s', self.terminals)
        logging.info('Variables: %s', self.variables)

    def generate(self, symbol=None, depth=0):
        """
        Генерирует строку, начиная с указанного символа.

        Параметры
        ----------
            symbol (str): Символ, с которого начинать генерацию (по умолчанию None).
            depth (int): Текущая глубина рекурсии (по умолчанию 0).

        Возвращает
        ----------
            tuple: Сгенерированная строка, количество попыток генерации, общее время генерации и количество шагов генерации.
        """
        if symbol is None:
            symbol = self.start_variable

        start_time = time.time()
        result = ''
        self.generation_steps = 0
        while True:  
            single_gen_start_time = time.time()
            self.generate_counter += 1
            logging.info('Generate attempt: %d', self.generate_counter)
            result = self._generate_recursive(symbol, depth)
            single_gen_end_time = time.time()

            logging.info('Time taken for counter %d: %.6f seconds, Steps: %d', 
                         self.generate_counter, single_gen_end_time - single_gen_start_time, self.generation_steps)

            if len(result) < self.max_length:
                logging.info('Generated valid string: %s', result)
                total_gen_time = time.time() - start_time
                logging.info('Total time taken for all counters: %.6f seconds', total_gen_time)
                return (result + self.end_symbol), self.generate_counter, total_gen_time, self.generation_steps
            else:
                logging.warning('Generated string is too long (%d characters): %s', len(result), result)

    def _generate_recursive(self, symbol, depth):
        """
        Рекурсивно генерирует строку на основе указанного символа.

        Параметры
        ----------
            symbol (str): Символ, который необходимо развернуть.
            depth (int): Текущая глубина рекурсии.

        Возвращает
        ----------
            str: Сгенерированная строка для данного символа.
        """
        self.generation_steps += 1
        if depth > self.max_depth:
            return ''
        if symbol in self.terminals:
            return symbol

        if symbol in self.rules:
            productions = self.rules[symbol]
            chosen_index = random.randint(0, len(productions) - 1)
            chosen_production = productions[chosen_index]
            print(f"{symbol} -> {chosen_production} (choice index: {chosen_index})")
            result = ''
            for sym in chosen_production.split():
                result += self._generate_recursive(sym, depth + 1) + ' '
            return result.strip()  # Убираем лишний пробел в конце

        return ''

    def is_valid_string(self, string):
        """
        Проверяет, является ли указанная строка допустимой согласно грамматике.

        Параметры
        ----------
            string (str): Строка, которую необходимо проверить.

        Возвращает
        ----------
            bool: True, если строка допустима, иначе False.
        """
        self.validation_steps = 0
        start_time = time.time()
        valid = self._match(self.start_variable, string, max_depth=len(string) + 10)
        end_time = time.time()
        logging.info('Checking validity of string: %s - %s', string, valid)
        logging.info('Time taken for validation: %.6f seconds, Steps: %d', end_time - start_time, self.validation_steps)
        return valid

    def _match(self, variable, string, max_depth):
        """
        Проверяет, соответствует ли строка указанной переменной грамматике.

        Параметры
        ----------
            variable (str): Нетерминал, который необходимо проверить.
            string (str): Строка, которую необходимо проверить.
            max_depth (int): Максимальная глубина рекурсии.

        Возвращает
        ----------
            bool: True, если строка соответствует переменной, иначе False.
        """
        self.validation_steps += 1
        if max_depth <= 0:
            return False
            
        if variable not in self.rules:
            return variable == string

        for production in self.rules[variable]:
            if self._match_production(production, string, max_depth - 1):
                return True
        return False

    def _match_production(self, production, string, max_depth):
        """
        Проверяет, соответствует ли часть строки указанному производству.

        Параметры
        ----------
            production (str): Производство, которое необходимо проверить.
            string (str): Строка, которую необходимо проверить.
            max_depth (int): Максимальная глубина рекурсии.

        Возвращает
        ----------
            bool: True, если часть строки соответствует производству, иначе False.
        """
        self.validation_steps += 1
        if not production and not string:
            return True
        if not production or not string:
            return False

        first_symbol = production.split()[0]
        if first_symbol in self.variables:
            for i in range(1, len(string) + 1):
                if self._match(first_symbol, string[:i], max_depth - 1) and self._match_production(production[len(first_symbol):], string[i:], max_depth - 1):
                    return True
        else:
            if string.startswith(first_symbol):
                return self._match_production(production[len(first_symbol):], string[len(first_symbol):], max_depth - 1)
        
        return False

    def __str__(self):
        """
        Возвращает строковое представление объекта CFG.

        Возвращает
        ----------
            str: Строка, содержащая стартовый символ и правила продукции.
        """
        print_lines = []
        print_lines.append("Start variable (S): {}".format(self.start_variable))
        print_lines.append("Rules (R):")
        for key, value in self.rules.items():
            print_lines.append(f"{key} -> {' | '.join(value)}")
        return "\n".join(print_lines)

