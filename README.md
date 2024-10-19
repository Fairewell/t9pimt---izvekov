# Контекстно-свободная грамматика (CFG) на Python

Этот проект представляет собой реализацию контекстно-свободной грамматики (CFG) на Python. Он позволяет загружать правила из файла, генерировать строки на основе этих правил и проверять, являются ли сгенерированные строки допустимыми согласно грамматике.

## Оглавление

- [Установка](#установка)
- [Использование](#использование)
- [Формат файла правил](#формат-файла-правил)
- [Методы](#методы)
- [Логирование](#логирование)
- [Пример](#пример)

## Установка

1. Скопируйте или клонируйте этот репозиторий на свой компьютер.
2. Убедитесь, что у вас установлен Python (версия 3.6 и выше).
3. Установите необходимые зависимости, если таковые имеются.

## Использование

```python
from cfg_full import CFG

# Создайте объект CFG, передав путь к файлу с правилами
cfg = CFG('путь_к_файлу_с_правилами.txt')

# Сгенерируйте строку на основе грамматики
generated_string, attempts, total_time, steps = cfg.generate()

print(f"Сгенерированная строка: {generated_string}")
print(f"Количество попыток: {attempts}, Время генерации: {total_time:.6f} секунд, Шаги генерации: {steps}")

# Проверьте, является ли строка допустимой
is_valid = cfg.is_valid_string(generated_string)
print(f"Строка допустима: {is_valid}")
```

## Формат файла правил

Файл правил должен содержать следующие секции:

- `#`: Строка комментария.
- `G`: Определение терминалов, нетерминалов, стартового символа и максимальной длины.
- `Pn`: Правила продукции для нетерминалов.
- `Pt`: Правила для терминалов (опционально).
- `env`: Стартовый символ, Максимальная длина, символ в конце сообщения.

Пример формата файла правил:

```mathematica
G({терминал1, терминал2}, {нетерминал1, нетерминал2})
Pn:
S → NP VP
NP → Det Adj N | Det N | Adj PropN | PropN
VP → Vi | Vt NP | Vc Comp S
Pt:
Det → the | a | some | any | every
Adj → green | young | tired | confused
N → dog | cat
PropN → John | Mary
Vi → sleeps | walks
Vt → loves | hates
Vc → says | thinks | believes
Comp → that
env: S | 50 | ?
```

## Методы

- `load_rules(rules_file)`: Загружает правила из указанного файла.
- `generate(symbol=None, depth=0)`: Генерирует строку, начиная с указанного символа.
- `is_valid_string(string)`: Проверяет, является ли указанная строка допустимой.

## Логирование

Все операции записываются в файл `cfg_generations.log`, который содержит информацию о попытках генерации, времени выполнения и прочих важных событиях.
Как это выглядит:
```yaml
2024-10-20 00:37:14,572 - INFO - Loaded rules: {'S': ['NP VP'], 'NP': ['Det Adj N', 'Det N', 'Adj PropN', 'PropN'], 'VP': ['Vi', 'Vt NP', 'Vc Comp S'], 'Det': ['the', 'a', 'some', 'any', 'every'], 'Adj': ['green', 'young', 'tired', 'confused'], 'N': ['dog', 'cat'], 'PropN': ['John', 'Mary'], 'Vi': ['sleeps', 'walks'], 'Vt': ['loves', 'hates'], 'Vc': ['says', 'thinks', 'believes'], 'Comp': ['that']}
2024-10-20 00:37:14,572 - INFO - Terminals: {'thinks', 'loves', 'Mary', 'the', 'every', 'cat', 'some', 'John', 'walks', 'says', 'tired', 'green', 'young', 'a', 'believes', 'sleeps', 'confused', 'hates', 'that', 'any', 'dog'}
2024-10-20 00:37:14,572 - INFO - Variables: {''}
2024-10-20 00:37:14,572 - INFO - CFG initialized with rules from rules/with_G_Pt.txt
2024-10-20 00:37:14,572 - INFO - Generate attempt: 1
2024-10-20 00:37:14,572 - INFO - Time taken for counter 1: 0.000000 seconds, Steps: 10
2024-10-20 00:37:14,572 - INFO - Generated valid string: Mary hates John
2024-10-20 00:37:14,572 - INFO - Total time taken for all counters: 0.000000 seconds
2024-10-20 00:37:14,572 - INFO - Checking validity of string: Mary hates John. - True
```

## Пример

Пример использования класса CFG и его методов можно найти в разделе [Использование](#использование).
