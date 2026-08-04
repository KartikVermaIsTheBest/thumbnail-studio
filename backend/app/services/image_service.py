import asyncio
import httpx
from urllib.parse import quote


async def generate_thumbnail_image(prompt: str, width: int = 1280, height: int = 720) -> bytes:
    encoded_prompt = quote(prompt)
    url = (
        f"https://image.pollinations.ai/prompt/{encoded_prompt}"
        f"?width={width}&height={height}&model=flux&nologo=true&safe=true"
    )

    last_error = None
    for attempt in range(3):
        async with httpx.AsyncClient(timeout=90.0) as client:
            response = await client.get(url)
        if response.status_code == 200:
            return response.content
        last_error = response.status_code
        await asyncio.sleep(2)

    raise ValueError(f"Image generation failed after 3 attempts, last status {last_error}")