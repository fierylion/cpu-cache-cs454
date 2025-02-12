import csv
import random

def generate_repeated_test():
    tests = []
    # Generate 1000 test sequences
    for test_id in range(1000):
        # Generate a set of 5-10 frequently accessed addresses
        num_hot_addresses = random.randint(5, 10)
        hot_addresses = random.sample(range(0, 1024), num_hot_addresses)
        
        # Access each hot address multiple times
        for iteration in range(50):  # 50 iterations of accessing hot addresses
            # Randomize order within each iteration
            random.shuffle(hot_addresses)
            for addr in hot_addresses:
                tests.append({
                    'test_id': test_id,
                    'access_type': 'repeated',
                    'address': addr,
                    'iteration': iteration,
                    'hot_set_size': num_hot_addresses
                })
    
    # Write to CSV
    with open('repeated_access_pattern.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['test_id', 'access_type', 'address', 'iteration', 'hot_set_size'])
        writer.writeheader()
        writer.writerows(tests)

if __name__ == "__main__":
    generate_repeated_test()