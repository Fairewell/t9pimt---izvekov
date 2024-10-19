from cfg_full import CFG	
import time

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