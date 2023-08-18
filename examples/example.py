"""
Provides example for myllm
"""

import asyncio
import sys

import uvicorn
from fastapi import FastAPI
from loguru import logger

from myllm import MyLLM

logger.remove()
logger.add(sys.stderr, level="DEBUG")


async def main():
    """Main"""
    talky = MyLLM()
    logger.info(await talky.talk())

    # Once upon a time, in a small village nestled among rolling hills, 
    # there lived a young girl named Lily. Lily was known for her kind heart 
    # and adventurous spirit. One sunny day, as she was exploring the nearby 
    # forest, she stumbled upon a hidden path she had never seen before.
    # Curiosity getting the best of her, Lily decided to follow the path. 
    # As she walked deeper into the forest, she noticed the trees becoming 
    # taller and the air growing cooler. Suddenly, she came across a clearing 
    # with a sparkling pond in the center.
    # Lily approached the pond and saw a beautiful golden fish swimming gracefully. 
    # he fish spoke to her in a gentle voice, "Hello, young one. I am the guardian 
    # of this enchanted pond. If you can answer my riddle correctly, 
    # I will grant you a wish."
    # Excited by the opportunity, Lily eagerly accepted the challenge. 
    # The golden fish posed its riddle, "I speak without a mouth and hear without ears. 
    # I have no body, but I come alive with wind. What am I?"
    # Lily pondered for a moment and then confidently replied, "An echo!"
    # The golden fish smiled and granted Lily her wish. She wished for the 
    # forest to always remain a place of wonder and beauty for everyone to enjoy. 
    # From that day forward, the forest became a sanctuary for all creatures, and
    #  people from far and wide would visit to experience its magic.
    # Lily's adventure taught her the power of curiosity, kindness, and the 
    # importance of preserving nature's wonders. She continued to explore the world,
    #  spreading joy and making a difference wherever she went.
    # And so, the story of Lily and the enchanted forest became a legend, 
    # reminding us all to embrace our curiosity and protect the beauty 
    # of our surroundings.

    logger.info(await talky.chat(
        prompt="My name is Jack"))

    logger.info(await talky.chat(
            prompt="tell me who is president of the united states?"))
    # The current President of the United States is Joe Biden.
    
    logger.info(await talky.chat(prompt="what is my name"))
    # your name is Jack

app = FastAPI()


@app.on_event("startup")
async def start():
    """startup"""
    asyncio.create_task(main())


@app.get("/")
def read_root():
    """root"""
    return {"online"}


@app.get("/health")
def health_check():
    """healthcheck"""
    return {"online"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8089)
