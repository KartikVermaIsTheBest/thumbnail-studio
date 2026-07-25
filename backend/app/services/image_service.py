import httpx
from urllib.parse import quote

async def generate_thumbnail_image(prompt: str, width: int = 1280, height: int = 720) -> bytes:
    encoded_prompt = quote(prompt)
    url = (
        f"https://image.pollinations.ai/prompt/{encoded_prompt}"
        f"?width={width}&height={height}&model=flux&enhance=true&nologo=true&safe=true"
    )
    async with httpx.AsyncClient(timeout=90.0) as client:
        response = await client.get(url)
    if response.status_code != 200:
        raise ValueError(f"Image generation failed with status {response.status_code}")
    return response.content