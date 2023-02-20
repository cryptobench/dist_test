import asyncio
from typing import AsyncIterable
from datetime import datetime, timedelta
from yapapi import Golem, Task, WorkContext
from yapapi.log import enable_default_logger
from yapapi.payload import vm
import pathlib
import sys

# examples_dir = pathlib.Path(__file__).resolve().parent.parent
# sys.path.append(str(examples_dir))

async def worker(ctx: WorkContext, tasks: AsyncIterable[Task]):
    script = ctx.new_script(timeout=timedelta(minutes=10))
    script.upload_file('USA_Housing.csv','/Golem/input/USA_Housing.csv')

    async for task in tasks:
        future_result = script.run("/bin/bash", "-c", "chmod 777 /code/run-model.sh && chmod +x /code/run-model.sh")
        # future_result = script.run("/code/run-model.sh")
        # future_result = script.run("/bin/bash", "-c", "/code/run-model.sh")
        script.download_file(f"mse_data.csv", "output/mse_data.csv")
        script.download_file(f"coefficient_data.csv", "output/coefficient_data.csv")
        yield script
        task.accept_result(result=await future_result)


async def main():
    package = await vm.repo(
        image_hash="b1dbf1dda4d3c9628d8cd144b64c8ea7c6793ccaf6fb5f58d64a373a",
    )

    tasks = [Task(data=None)]

    async with Golem(budget=2.0, subnet_tag="public") as golem:
        async for completed in golem.execute_tasks(worker, tasks, payload=package):
            print(completed.result.stdout)


if __name__ == "__main__":
    enable_default_logger()

    loop = asyncio.get_event_loop()
    task = loop.create_task(main())
    loop.run_until_complete(task)

#How is the data being passed on the upload and download file. What is the mechanism.
#What happens if I lose my internet conections? 
#Can people see what is on my image hash? 
#Can other people run on my image hash? Is it private only to me?
#Is it encrypted? If so how is the other party decrypting it?

#How does the consensur mechanisum work?

