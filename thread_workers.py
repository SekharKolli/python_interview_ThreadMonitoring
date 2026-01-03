'''Objective of this program is to demonstrate how threads get created, handled, automatically revivied in case of failure'''

import random
import time


def worker_thread(worker_id: int):
    numbers_generated = 0
    tries = 30  # Maximum number of numbers before we exit the loop

    print(f"{worker_id=:02} Normal_Start...")

    while tries >= 0:
        tries -= 1

        try:
            task = random.randint(0, 5)
            numbers_generated += 1
            print(f"{worker_id=:02} Working on : {1/task=}")
            time.sleep(0.1)  # simulating time taken to perform operation
        except ZeroDivisionError:
            print(f"{worker_id=:02} Exception_Crash...")
            break

    print(f"{worker_id=:02} Normal_Exit... {numbers_generated=}")
    return numbers_generated


def main() -> None:

    worker_thread(1)
    worker_thread(2)
    worker_thread(3)


if __name__ == "__main__":
    main()
