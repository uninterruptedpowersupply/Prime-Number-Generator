import asyncio
import math
import threading
import time
import cupy as cp

# Function to check if a number is prime using normal CPU (for comparison)
def is_prime_cpu(n):
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

# CUDA-accelerated function to check if a number is prime using GPU
def is_prime_gpu(n):
    if n <= 1:
        return False
    max_val = int(cp.sqrt(n)) + 1
    divisors = cp.arange(2, max_val)
    mod = cp.mod(n, divisors)
    if cp.any(mod == 0):
        return False
    return True

# Async function to handle multiple prime checks concurrently
async def check_prime_async(number, use_cuda=False):
    if use_cuda:
        result = await asyncio.to_thread(is_prime_gpu, number)
    else:
        result = await asyncio.to_thread(is_prime_cpu, number)
    return number, result

# Function to check prime numbers starting from a given start point (no end point)
def check_primes(start=1, use_cuda=False):
    async def main():
        number = start
        while True:
            result = await check_prime_async(number, use_cuda)
            if result[1]:
                print(f"{result[0]} is prime.")
            number += 1
            await asyncio.sleep(0)  # To avoid CPU overload in infinite loop
    
    # Run the async function
    asyncio.run(main())

# Function to handle multithreaded execution
def start_threaded_prime_check(start=1, use_cuda=False):
    thread = threading.Thread(target=check_primes, args=(start, use_cuda))
    thread.start()
    thread.join()

# Start the prime checking process with multithreading and CUDA
if __name__ == "__main__":
    start_point = int(input("Enter the starting point: "))
    
    use_cuda = input("Use CUDA for GPU acceleration? (yes/no): ").strip().lower() == "yes"
    
    start_time = time.time()
    start_threaded_prime_check(start_point, use_cuda)
    end_time = time.time()
    
    print(f"Prime check started... Press Ctrl+C to stop.")
