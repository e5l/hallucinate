from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from llm_adapter import generate_prompts

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/generate/{prompt}")
async def get_image(prompt):
    prompts = generate_prompts(prompt)

    return {"prompts": prompts}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
