'''Objective of this program is to demonstrate how threads get created, handled, automatically revivied in case of failure'''

import random
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# Amount of time each iteration waits to simulate a computation task
TASK_PROCESSING_DELAY = 0.5
NO_OF_RUNS = 30  # Defined globally for the print statements


def big_computing_job(job_id: str | int, run_job_for: int = NO_OF_RUNS):
    '''
    A worker function. This simulates work (which is divide with a random int) and a crash (which is divide with a zero) 

    :param job_id: An id, which uniquely identifies the job and the call made
    :type job_id: str | int
    :param run_job_for: How many times should the job iterate for? Default is defined in NO_OF_RUNS global variable, which is set to 30.
    :type run_job_for: int
    '''
    print(f"{job_id=:03}{":✅ Starting":.<15}")

    # we track how many we have successfully done in this specific thread call
    divisions_completed = 0
    remaining_runs = run_job_for

    while remaining_runs > 0:

        try:
            task = random.randint(0, 5)
            result = 1/task  # Here is where the crash could occur

            # if it didn't crash, decrement remaining work
            remaining_runs -= 1
            divisions_completed += 1

            # Displaying progress
            progress = NO_OF_RUNS - remaining_runs
            print(
                f"{job_id=:03}:{f'[{progress:02}/{NO_OF_RUNS:02}] Crunching 1/{task}':_<15}: {result:0.6f}")

            # simulating time taken to perform operation
            time.sleep(TASK_PROCESSING_DELAY)

        except ZeroDivisionError:
            print(f"{job_id=:03}{':⚠️ Exception⚠️':.<15}")
            return {"job_id": job_id, "success": False, "remaining": remaining_runs}

    print(f"{job_id=:03}{":❎ Exiting":.<15} : {divisions_completed=:02}")
    return {"job_id": job_id, "success": True, "remaining": 0}


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

    with ThreadPoolExecutor(max_workers=5) as executor:
        executor.submit(big_computing_job, "🐮")
        executor.submit(big_computing_job, "🐯")
        executor.submit(big_computing_job, "🐰")


def demo_auto_thread_revival() -> None:
    '''Demos how to auto revive the thread if the job is not complete'''

    job_ids = ["🐮", "🐯", "🐰"]

    with ThreadPoolExecutor(max_workers=5) as executor:
        # initial submission
        jobs_dict = {executor.submit(big_computing_job, jid, NO_OF_RUNS): jid
                     for jid in job_ids}

        while jobs_dict:
            # Get the next completed future
            futures = list(as_completed(jobs_dict))

            for job_future in futures:
                # Remove from the tracking dict
                job_id = jobs_dict.pop(job_future)
                try:
                    result = job_future.result()

                    if not result["success"]:
                        print(
                            f"--- 🔄 Reviving Job {job_id} ({result["remaining"]} runs left) ---")
                        # Re-submit the job with the remaining count
                        new_job = executor.submit(
                            big_computing_job, job_id, result["remaining"])
                        jobs_dict[new_job] = job_id
                    else:
                        print(f"--- ✨ Job {job_id} Finished Successfully ---")

                except Exception as e:
                    print(f"--- 💀 Fatal Error in {job_id}: {e} ---")


if __name__ == "__main__":
    # demo_threading()
    # demo_auto_threading()
    demo_auto_thread_revival()
