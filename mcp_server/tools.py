import httpx

FASTAPI_URL = "http://127.0.0.1:8000"


async def call(endpoint: str):

    async with httpx.AsyncClient(timeout=120) as client:

        response = await client.get(
            f"{FASTAPI_URL}/{endpoint}"
        )

        response.raise_for_status()

        return response.json()


async def coach(handle: str):

    return await call(
        f"coach/{handle}"
    )


async def profile(handle: str):

    return await call(
        f"profile/{handle}"
    )


async def analytics(handle: str):

    return await call(
        f"analytics/{handle}"
    )


async def recommendations(handle: str):

    return (
        await coach(handle)
    )["recommendations"]


async def contest_analysis(handle: str):

    return (
        await coach(handle)
    )["contest_analysis"]


async def practice_plan(handle: str):

    return (
        await coach(handle)
    )["practice_plan"]