'''Objective of this program is to demonstrate how threads get created, handled, automatically revivied in case of failure'''

import random
import time

NO_OF_RUNS = 30  # Maximum number of numbers before we exit the loop
TIME_CONSUMED_FOR_CALC = 0.3


def big_computing_job(job_id: str | int, no_of_runs: int = 30):
    '''
    A worker function. This simulates work and a crash. We have a random int generator, which could generate a zero causing it to crash. 
    :param worker_id: Id which identifies the worker provided to identify worker
    :type worker_id: int
    '''
    divisions_completed = 0

    print(f"{job_id=:03}{":✅ Starting":.<15}")

    while no_of_runs >= 0:
        no_of_runs -= 1

        try:
            task = random.randint(0, 5)
            divisions_completed += 1
            print(
                f"{job_id=:03}:{f"[{divisions_completed:02}/{NO_OF_RUNS:02}] Crunching 1/{task}":_<15}", end="")
            print(f": {1/task:0.6f}")
            # simulating time taken to perform operation
            time.sleep(TIME_CONSUMED_FOR_CALC)
        except ZeroDivisionError:
            print(f"{":⚠️ Exception⚠️":.<15}")
            break

    print(f"{job_id=:03}{":❎ Exiting":.<15} : {divisions_completed=:02}")
    return (job_id, divisions_completed)


def demo_threading() -> None:
    '''Function that demos the use of threads. Here we manually initiate the start and then join them'''
    import threading

    # 🐮🐯🐰🐱
    t1 = threading.Thread(target=big_computing_job, args="🐮")
    t2 = threading.Thread(target=big_computing_job, args="🐯")
    t3 = threading.Thread(target=big_computing_job, args="🐰")

    t1.start()
    t2.start()
    t3.start()

    t1.join()
    t2.join()
    t3.join()


def demo_auto_threading() -> None:
    '''Demos how to create a thread pool which automatically manages the threads '''

    from concurrent.futures import ThreadPoolExecutor

    with ThreadPoolExecutor(max_workers=5) as executor:
        executor.submit(big_computing_job, "🐮")
        executor.submit(big_computing_job, "🐯")
        executor.submit(big_computing_job, "🐰")


if __name__ == "__main__":
    # demo_threading()
    demo_auto_threading()
