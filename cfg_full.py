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
    def __init__(self, rules_file, max_depth=10):
        self.rules = {}
        self.terminals = set()
        self.variables = set()
        self.start_variable = None
        self.max_depth = max_depth
        self.load_rules(rules_file)
        self.generate_counter = 0
        self.generation_steps = 0
        self.validation_steps = 0
        logging.info('CFG initialized with rules from %s', rules_file)

    def load_rules(self, rules_file):
        with open(rules_file, 'r') as f:
            lines = f.readlines()

        section = None
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            if line.startswith('G'):
                # Извлечение терминалов и нетерминалов
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

        logging.info('Loaded rules: %s', self.rules)

    def generate(self, symbol=None, depth=0):
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

            if len(result) < 100:  # Задайте длину в зависимости от ваших требований
                logging.info('Generated valid string: %s', result)
                total_gen_time = time.time() - start_time
                logging.info('Total time taken for all counters: %.6f seconds', total_gen_time)
                return result, self.generate_counter, total_gen_time, self.generation_steps
            else:
                logging.warning('Generated string is too long (%d characters): %s', len(result), result)

    def _generate_recursive(self, symbol, depth):
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
                result += self._generate_recursive(sym, depth + 1)
            return result

        return ''

    def is_valid_string(self, string):
        self.validation_steps = 0
        start_time = time.time()
        valid = self._match(self.start_variable, string, max_depth=len(string) + 10)
        end_time = time.time()
        logging.info('Checking validity of string: %s - %s', string, valid)
        logging.info('Time taken for validation: %.6f seconds, Steps: %d', end_time - start_time, self.validation_steps)
        return valid

    def _match(self, variable, string, max_depth):
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
        print_lines = []
        print_lines.append("Start variable (S): {}".format(self.start_variable))
        print_lines.append("Rules (R):")
        for key, value in self.rules.items():
            print_lines.append(f"{key} -> {' | '.join(value)}")
        return "\n".join(print_lines)


cfg = CFG('rules/with_G_Pt.txt', max_depth=10)
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
