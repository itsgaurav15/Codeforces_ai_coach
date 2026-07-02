import asyncio

import tools

async def main():

    result = await tools.coach("Psycho__coder075")

    print(result["profile"]["handle"])

asyncio.run(main())