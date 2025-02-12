import csv
import subprocess
from collections import defaultdict

class CacheTestRunner:
    def __init__(self, memory_size=10, cache_size=7, block_size=3, mapping=2):
        self.memory_size = memory_size
        self.cache_size = cache_size
        self.block_size = block_size
        self.mapping = mapping
        self.policies = ['LRU', 'LFU', 'FIFO', 'RAND']
        self.results = defaultdict(lambda: defaultdict(list))

    def run_test_sequence(self, addresses, policy='LRU', write_policy='WT'):
        """Run a sequence of memory accesses and return hit ratio"""
        commands = [f"read {addr}" for addr in addresses]
        commands.append('stats')
        commands.append('quit')
        
        # Run simulator
        process = subprocess.Popen(
            ['python', 'simulator.py', 
             str(self.memory_size), str(self.cache_size), 
             str(self.block_size), str(self.mapping), 
             policy, write_policy],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            text=True
        )
        
        # Send commands
        input_text = '\n'.join(commands) + '\n'
        output, _ = process.communicate(input_text)
        
        # Parse hit ratio
        for line in output.split('\n'):
            if 'Hit/Miss Ratio:' in line:
                ratio = float(line.split(':')[1].strip().rstrip('%'))
                return ratio
        return 0.0

    def test_pattern_file(self, filename, pattern_name):
        """Test a pattern from CSV file with all policies"""
        # Read addresses from CSV
        with open(filename, 'r') as f:
            reader = csv.DictReader(f)
            test_sequences = defaultdict(list)
            for row in reader:
                test_sequences[int(row['test_id'])].append(int(row['address']))
        
        # Run tests for each policy
        for policy in self.policies:
            print(f"Testing {pattern_name} with {policy}...")
            for test_id, addresses in test_sequences.items():
                if test_id < 50:  # Test first 10 sequences for each pattern
                    ratio = self.run_test_sequence(addresses, policy)
                    self.results[pattern_name][policy].append(ratio)
        
        # Save results
        self.save_results(f"{pattern_name}_results.csv")

    def save_results(self, filename):
        """Save test results to CSV"""
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Pattern', 'Policy', 'Test_ID', 'Hit_Ratio'])
            for pattern in self.results:
                for policy in self.policies:
                    for test_id, ratio in enumerate(self.results[pattern][policy]):
                        writer.writerow([pattern, policy, test_id, ratio])

# Run tests
runner = CacheTestRunner()

# Test each pattern
patterns = [
    ('sequential_access_pattern.csv', 'Sequential'),
    ('repeated_access_pattern.csv', 'Repeated'),
    ('program_switching_pattern.csv', 'Program_Switching')
]

for filename, pattern_name in patterns:
    runner.test_pattern_file(filename, pattern_name)