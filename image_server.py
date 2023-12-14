from io import BytesIO

from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

import torch
from diffusers import AutoPipelineForText2Image

pipe = AutoPipelineForText2Image.from_pretrained(
    "stabilityai/sdxl-turbo", torch_dtype=torch.float16, variant="fp16"
)
pipe = pipe.to("cuda")


def image_to_bytes(image):
    byte_stream = BytesIO()
    image.save(byte_stream, format="JPEG")
    byte_stream.seek(0)
    return byte_stream.getvalue()


@app.get("/generate/{prompt}")
async def serve_image(prompt):
    image = pipe(prompt=prompt, num_inference_steps=1, guidance_scale=0).images[0]
    raw_image = image_to_bytes(image)

    return Response(raw_image, media_type="image/jpeg")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)
