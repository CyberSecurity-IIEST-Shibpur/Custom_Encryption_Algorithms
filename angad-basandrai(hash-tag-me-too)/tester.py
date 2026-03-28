import random
import string
import json
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor, as_completed
from funcs import hasher, brute_force

SAMPLES = 25
MAX_WORKERS = 8

def random_string(length):
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))

def worker(args):
    length, idx = args
    s = random_string(length)
    h = hasher(s)
    result, t = brute_force(h, max_len=length)
    return {
        "index": idx,
        "string": s,
        "found": result,
        "time": t.total_seconds()
    }

def run_tests():
    results = {}

    for length in range(1, 6):
        print(f"\n[DEBUG] Starting tests for length = {length}")

        times = []
        tasks = [(length, i) for i in range(SAMPLES)]

        with ProcessPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = [executor.submit(worker, t) for t in tasks]

            for future in tqdm(as_completed(futures), total=SAMPLES, desc=f"Length {length}"):
                res = future.result()

                print(f"[DEBUG] Test {res['index']+1} | String: {res['string']} | Found: {res['found']} | Time: {res['time']:.6f}s")

                times.append(res["time"])

        avg_time = sum(times) / len(times)

        print(f"[DEBUG] Length {length} average time: {avg_time:.6f}s")

        results[length] = {
            "samples": SAMPLES,
            "average_time_seconds": avg_time
        }

    return results

if __name__ == "__main__":
    data = run_tests()

    with open("results.json", "w") as f:
        json.dump(data, f, indent=4)

    print("\n[DEBUG] Results saved to results.json")