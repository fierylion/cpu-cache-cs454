import subprocess
import csv
from collections import defaultdict

def run_cache_test(memory_size, cache_size, block_size, mapping, replace_policy, write_policy, commands):
    """Run cache simulator with specific configuration and commands"""
    process = subprocess.Popen(
        ['python', 'simulator.py', str(memory_size), str(cache_size), 
         str(block_size), str(mapping), replace_policy, write_policy],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Send each command
    for cmd in commands:
        process.stdin.write(cmd + '\n')
    
    # Get stats
    process.stdin.write('stats\n')
    process.stdin.write('quit\n')
    process.stdin.flush()
    
    output = process.stdout.read()
    return parse_stats(output)

def parse_stats(output):
    """Parse hit/miss stats from simulator output"""
    stats = {'ratio': 0.0, 'hits': 0, 'misses': 0}
    lines = output.split('\n')
    for line in lines:
        if 'Hits:' in line:
            # Parse line like "Hits: X | Misses: Y"
            parts = line.split('|')
            stats['hits'] = int(parts[0].split(':')[1].strip())
            stats['misses'] = int(parts[1].split(':')[1].strip())
        elif 'Hit/Miss Ratio:' in line:
            stats['ratio'] = float(line.split(':')[1].strip().rstrip('%'))
    return stats

def generate_sequential_access(start_addr, length):
    """Generate sequential read commands"""
    return [f"read {i}" for i in range(start_addr, start_addr + length)]

def generate_repeated_access(addresses, repetitions):
    """Generate repeated access to specific addresses"""
    commands = []
    for _ in range(repetitions):
        for addr in addresses:
            commands.append(f"read {addr}")
    return commands

def generate_pattern_access(patterns, repetitions):
    """Generate pattern-based access"""
    commands = []
    for _ in range(repetitions):
        for pattern in patterns:
            commands.extend([f"read {addr}" for addr in pattern])
    return commands

if __name__ == "__main__":
    # Test configurations
    configs = {
        'memory_size': 10,  # 2^10 bytes
        'cache_size': 7,    # 2^7 bytes
        'block_size': 3,    # 2^3 bytes
        'mapping': 2,       # 4-way associative
        'write_policy': 'WT'
    }

    replacement_policies = ['LRU', 'LFU', 'FIFO', 'RAND']
    results = defaultdict(lambda: defaultdict(dict))

    # Test Pattern 1: Sequential Access
    sequential_commands = generate_sequential_access(0, 100)

    # Test Pattern 2: Repeated Access
    repeated_commands = generate_repeated_access([0, 8, 16, 24, 32], 20)

    # Test Pattern 3: Program Switching Pattern
    pattern1 = [0, 8, 16, 24]  # "Program 1"
    pattern2 = [128, 136, 144, 152]  # "Program 2"
    switching_commands = generate_pattern_access([pattern1, pattern2], 10)

    patterns = {
        'Sequential': sequential_commands,
        'Repeated': repeated_commands,
        'Program_Switching': switching_commands
    }

    # Run tests for each pattern and policy
    for pattern_name, commands in patterns.items():
        print(f"\nTesting {pattern_name} pattern...")
        for policy in replacement_policies:
            stats = run_cache_test(
                configs['memory_size'],
                configs['cache_size'],
                configs['block_size'],
                configs['mapping'],
                policy,
                configs['write_policy'],
                commands
            )
            results[pattern_name][policy] = stats
            print(f"{policy}: {stats['ratio']:.2f}% hit ratio "
                  f"(Hits: {stats['hits']}, Misses: {stats['misses']})")

    # Save results to CSV
    with open('cache_results.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Pattern', 'Policy', 'Hit_Ratio', 'Hits', 'Misses', 'Total_Accesses'])
        for pattern in results:
            for policy, stats in results[pattern].items():
                total_accesses = stats['hits'] + stats['misses']
                writer.writerow([
                    pattern, 
                    policy, 
                    f"{stats['ratio']:.2f}%",
                    stats['hits'],
                    stats['misses'],
                    total_accesses
                ])

    # Print summary table
    print("\nSummary of Results:")
    print("-" * 80)
    print(f"{'Pattern':<20} {'Policy':<8} {'Hit Ratio':<12} {'Hits':<8} {'Misses':<8} {'Total':<8}")
    print("-" * 80)
    for pattern in results:
        for policy, stats in results[pattern].items():
            total = stats['hits'] + stats['misses']
            print(f"{pattern:<20} {policy:<8} {stats['ratio']:>6.2f}% {stats['hits']:>8} "
                  f"{stats['misses']:>8} {total:>8}")
    print("-" * 80)