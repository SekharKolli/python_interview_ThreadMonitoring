'''Objective of this program is to demonstrate how threads get created, handled, automatically revivied in case of failure'''

import random
import time

NO_OF_RUNS = 30  # Maximum number of numbers before we exit the loop
TIME_CONSUMED_FOR_CALC = 0.1


def worker_thread(job_id: int):
    '''
    A worker function which will crash b'cos of divide by zero or 30 

    :param worker_id: Id provided to identify worker
    :type worker_id: int
    '''
    divisions_completed = 0
    tries = NO_OF_RUNS

    print(f"{job_id=:03}{":✅ Starting":.<15}")

    while tries >= 0:
        tries -= 1

        try:
            task = random.randint(0, 5)
            divisions_completed += 1
            print(
                f"{job_id=:03}:{f"[{divisions_completed:02}/{NO_OF_RUNS:02}] performing 1/{task}":_<15}", end="")
            print(f": {1/task}")
            # simulating time taken to perform operation
            time.sleep(TIME_CONSUMED_FOR_CALC)
        except ZeroDivisionError:
            print(f"{":⚠️  Exception":.<15}")
            break

    print(f"{job_id=:03}{":✅ Exiting":.<15} : {divisions_completed=:02}")
    return (job_id, divisions_completed)


def main() -> None:

    worker_thread(1)
    worker_thread(2)
    worker_thread(3)


if __name__ == "__main__":
    main()
