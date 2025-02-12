import csv
import random

def generate_sequential_test():
    tests = []
    # Generate 1000 test sequences
    for test_id in range(1000):
        # Random starting point for sequential access
        start_addr = random.randint(0, 900)  # Leave room for sequence
        # Generate sequence of 100 consecutive addresses
        sequence = list(range(start_addr, start_addr + 100))
        
        for addr in sequence:
            tests.append({
                'test_id': test_id,
                'access_type': 'sequential',
                'address': addr,
                'sequence_position': addr - start_addr
            })
    
    # Write to CSV
    with open('sequential_access_pattern.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['test_id', 'access_type', 'address', 'sequence_position'])
        writer.writeheader()
        writer.writerows(tests)

if __name__ == "__main__":
    generate_sequential_test()