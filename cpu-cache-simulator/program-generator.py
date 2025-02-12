import csv
import random

def generate_program_switching_test():
    tests = []
    # Generate 1000 test sequences
    for test_id in range(1000):
        # Simulate 3-4 different programs
        num_programs = random.randint(3, 4)
        programs = {}
        
        # Generate memory footprint for each program
        for prog_id in range(num_programs):
            # Each program has its own working set of addresses
            start_addr = prog_id * 256  # Separate address spaces
            num_addresses = random.randint(10, 20)
            programs[prog_id] = random.sample(range(start_addr, start_addr + 256), num_addresses)
        
        # Simulate program switching behavior
        for switch_count in range(30):  # 30 program switches
            # Select a program to "run"
            active_program = random.randint(0, num_programs - 1)
            # Access its memory locations
            for _ in range(random.randint(5, 15)):  # Variable number of accesses per program
                addr = random.choice(programs[active_program])
                tests.append({
                    'test_id': test_id,
                    'access_type': 'program_switching',
                    'address': addr,
                    'program_id': active_program,
                    'switch_count': switch_count
                })
    
    # Write to CSV
    with open('program_switching_pattern.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['test_id', 'access_type', 'address', 'program_id', 'switch_count'])
        writer.writeheader()
        writer.writerows(tests)

if __name__ == "__main__":
    generate_program_switching_test()