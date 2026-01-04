'''Objective of this program is to demonstrate how threads get created, handled, automatically revivied in case of failure'''

import random
import time

# Amount of time each iteration waits to simulate a computation task
TASK_PROCESSING_DELAY = 0.3
NO_OF_RUNS = 30  # Defined globally for the print statements


def big_computing_job(job_id: str | int, remaining_runs: int = 30):
    '''
    A worker function. This simulates work and a crash. We have a random int generator, which could generate a zero causing it to crash. 
    :param worker_id: Id which identifies the worker provided to identify worker
    :type worker_id: int
    '''
    divisions_completed = 0 if remaining_runs == NO_OF_RUNS else remaining_runs  # Tracks how many tasks are complete

    print(f"{job_id=:03}{":✅ Starting":.<15}")

    while remaining_runs > 0:
        remaining_runs -= 1

        try:
            divisor = random.randint(0, 5)
            divisions_completed += 1
            print(
                f"{job_id=:03}:{f"[{divisions_completed:02}/{NO_OF_RUNS:02}] Crunching 1/{divisor}":_<15}", end="")
            print(f": {1/divisor:0.6f}")
            # simulating time taken to perform operation
            time.sleep(TASK_PROCESSING_DELAY)
        except ZeroDivisionError:
            print(f"{":⚠️ Exception⚠️":.<15}")
            break

    print(f"{job_id=:03}{":❎ Exiting":.<15} : {divisions_completed=:02}")
    return (job_id, divisions_completed)


def demo_threading() -> None:
    '''Function that demos the use of threads. Here we manually initiate the start and then join them'''
    import threading

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


def demo_auto_thread_revival() -> None:
    '''Demos how to auto revive the thread if the job is not complete'''
    from concurrent.futures import ThreadPoolExecutor, as_completed

    job_ids = ["🐮", "🐯", "🐰"]

    with ThreadPoolExecutor(max_workers=5) as executor:
        job_queue = {executor.submit(big_computing_job, jid): jid
                     for jid in job_ids}

        while job_queue:
            # as_completed yields futures as they resolve (either finish or crash)
            for job in as_completed(job_queue):
                job_id = job_queue.pop(job)
                try:
                    result = job["result"]

                    if not result["success"]:
                        print(
                            f"--- 🔄 Reviving Job {job_id} ({result["remaining"]} runs left) ---")
                        # Re-submit the job with the remaining count
                        new_job = executor.submit(
                            big_computing_job, job_id, result["remaining"])
                        job_queue[new_job] = job_id
                    else:
                        print(f"--- ✨ Job {job_id} Finished Successfully ---")

                except Exception as e:
                    print(f"--- 💀 Fatal Error in {job_id}: {e} ---")


if __name__ == "__main__":
    # demo_threading()
    # demo_auto_threading()
    demo_auto_thread_revival()
