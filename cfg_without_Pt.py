import random
import logging
import time

# Настройка логирования
logging.basicConfig(
    filename='cfg_generations.log',  # Файл для логов
    level=logging.INFO,              # Уровень логирования
    format='%(asctime)s - %(levelname)s - %(message)s'  # Формат сообщений
)

class CFG:
    def __init__(self, rules_file, max_depth=10):
        self.rules = self.load_rules(rules_file)
        self.start_variable = list(self.rules.keys())[0]
        self.max_depth = max_depth
        self.operators = {'+', '-', '*', '/'}
        self.terminals = {'a', 'b'}
        self.brackets = {'(', ')'}
        self.variables = set(self.rules.keys())
        self.generate_counter = 0
        self.generation_steps = 0  # Подсчет шагов для генерации
        self.validation_steps = 0  # Подсчет шагов для валидации
        logging.info('CFG initialized with rules from %s', rules_file)

    def load_rules(self, rules_file):
        rules = {}
        with open(rules_file, 'r') as f:
            for line in f:
                if '->' in line:
                    left, right = line.split('->')
                    non_terminal = left.strip()
                    transformations = [r.strip() for r in right.split('|')]
                    rules[non_terminal] = transformations
        logging.info('Loaded rules: %s', rules)
        return rules

    def generate(self, symbol=None, depth=0):
        if symbol is None:
            symbol = self.start_variable

        start_time = time.time()  # Время начала генерации всех строк
        result = ''
        self.generation_steps = 0  # Обнуление счетчика шагов для генерации
        while True:  
            single_gen_start_time = time.time()  # Время начала генерации одной строки
            self.generate_counter += 1
            logging.info('Generate attempt: %d', self.generate_counter)
            result = self._generate_recursive(symbol, depth)
            single_gen_end_time = time.time()  # Время окончания генерации одной строки

            # Логирование времени генерации одной строки и шагов
            logging.info('Time taken for counter %d: %.6f seconds, Steps: %d', 
                         self.generate_counter, single_gen_end_time - single_gen_start_time, self.generation_steps)

            if len(result) < 10:
                logging.info('Generated valid string: %s', result)
                total_gen_time = time.time() - start_time  # Время окончания генерации всех строк
                logging.info('Total time taken for all counters: %.6f seconds', total_gen_time)
                return result, self.generate_counter, total_gen_time, self.generation_steps  # Если строка меньше 10 символов, возвращаем её
            else:
                logging.warning('Generated string is too long (%d characters): %s', len(result), result)

    def _generate_recursive(self, symbol, depth):
        self.generation_steps += 1  # Увеличение счетчика шагов генерации
        if depth > self.max_depth:
            return ''
        if symbol in self.terminals or symbol in self.operators or symbol in self.brackets:
            return symbol

        if symbol in self.rules:
            productions = self.rules[symbol]
            chosen_index = random.randint(0, len(productions) - 1)
            chosen_production = productions[chosen_index]
            
            result = ''
            for sym in chosen_production:
                if sym.isspace():
                    continue
                result += self._generate_recursive(sym, depth + 1)
            return result

        return ''
    
    def is_valid_string(self, string):
        self.validation_steps = 0  # Обнуление счетчика шагов для валидации
        start_time = time.time()  # Время начала проверки строки
        valid = self._match(self.start_variable, string, max_depth=len(string) + 10)
        end_time = time.time()  # Время окончания проверки строки
        logging.info('Checking validity of string: %s - %s', string, valid)
        logging.info('Time taken for validation: %.6f seconds, Steps: %d', end_time - start_time, self.validation_steps)
        return valid

    def _match(self, variable, string, max_depth):
        self.validation_steps += 1  # Увеличение счетчика шагов валидации
        if max_depth <= 0:
            return False
            
        if variable not in self.rules:
            return variable == string

        for production in self.rules[variable]:
            if self._match_production(production, string, max_depth - 1):
                return True
        return False

    def _match_production(self, production, string, max_depth):
        self.validation_steps += 1  # Увеличение счетчика шагов валидации
        if not production and not string:
            return True
        if not production or not string:
            return False

        first_symbol = production[0]
        if first_symbol in self.variables:
            for i in range(1, len(string) + 1):
                if self._match(first_symbol, string[:i], max_depth - 1) and self._match_production(production[1:], string[i:], max_depth - 1):
                    return True
        else:
            if string.startswith(first_symbol):
                return self._match_production(production[1:], string[len(first_symbol):], max_depth - 1)
        
        return False

    def __str__(self):
        print_lines = []
        print_lines.append("Start variable (S): {}".format(self.start_variable))
        print_lines.append("Rules (R):")
        for key, value in self.rules.items():
            print_lines.append(f"{key} -> {' | '.join(value)}")
        return "\n".join(print_lines)


cfg = CFG('rules/without_G_Pt.txt', max_depth=10)
generated_string, counter, total_time, generation_steps = cfg.generate()
print(f"Generated string: {generated_string}\nCounter: {counter}\nTotal generation time: {total_time:.6f} seconds\nSteps for generation: {generation_steps}")

start_valid_time = time.time()
valid = cfg.is_valid_string(generated_string)
end_valid_time = time.time()
print(f"Validation time: {end_valid_time - start_valid_time:.6f} seconds\nValidation steps: {cfg.validation_steps}")

if valid:
    print("The generated string is valid according to the grammar.")
else:
    print("The generated string is not valid.")
