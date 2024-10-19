### CFG Generator
This is a Python implementation of a Context-Free Grammar (CFG) generator. The generator reads rules from an input file, generates strings based on the rules, and validates them. The input file follows a specific format, allowing you to define terminals, non-terminals, and transformation rules for the grammar.

### Features
- Grammar Input: The CFG class accepts a file with a custom format specifying terminals, non-terminals, and their transformation rules.
- String Generation: Generates strings based on the grammar rules using recursive methods, ensuring the string length is controlled.
- Validation: Validates whether a generated string matches the grammar rules.
- Logging: Logs each step of the generation and validation processes.
- Performance Tracking: Tracks the time taken and the number of steps involved in generating and validating strings.

### File Format
The input file for the grammar should have the following structure:

```makefile
G({Terminals}, {Non-Terminals})
Pn:
Rules for non-terminals
Pt:
Rules for terminals (if any)
```
### Example (`cfg_rules.txt`)
```mathematica
G({the, a, some, any, every, green, young, tired, confused, dog, cat, John, Mary, sleeps, walks, loves, hates, says, thinks, believes, that}, {S, NP, VP, Det, Adj, N, PropN, Vi, Vt, Vc, Comp})
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
```
- G({Terminals}, {Non-Terminals}): This line defines the terminals and non-terminals used in the grammar.
- Pn:: Section for non-terminal rules. Each rule specifies transformations for a non-terminal symbol.
- Pt:: Section for terminal rules (optional). Specifies how terminals are defined.

### How to Use
- Create a file (`cfg_rules.txt`) with your grammar rules following the specified format.
- Run the script:
```bash
python cfg_full.py
```
### Output
The program will generate a string based on the grammar and display whether it is valid. Additionally, it will log information about each step of the generation and validation process in `cfg_generations.log`.

### Example Output
```yaml
Generated string: some young dog walks
Counter: 5
Total generation time: 0.123456 seconds
Steps for generation: 42
Validation time: 0.234567 seconds
Validation steps: 58
The generated string is valid according to the grammar.
```
### Logging
The program logs important information such as:

The number of attempts (`Counter`) made to generate a valid string.
The time taken for each generation attempt and the total time.
The number of steps involved in both generation and validation.
Whether the generated string was valid.
Logs are stored in a file called `cfg_generations.log.`

### Dependencies
- Python 3.x
No additional libraries are required.

### Customization
- Max Depth: You can adjust the maximum recursion depth when generating strings by changing the `max_depth` parameter when initializing the `CFG` class:
```python
cfg = CFG('cfg_rules.txt', max_depth=15)
```
- Grammar Rules: Modify `cfg_rules.txt` to suit your specific language needs.
### Notes
- Ensure the grammar file follows the correct format. Incorrect formatting may cause errors during parsing.
- Be mindful of setting an appropriate `max_depth` value to avoid infinite recursion or overly long generation times.
### License
This project is open-source and available for use and modification.