import os
from http import HTTPStatus
import json

from groq import Groq
from pydantic import BaseModel

from resources.exceptions import Exceptions
from global_utilities import logging_utilities

class Score(BaseModel):
    positive: float
    negative: float
    neutral: float


class LLMUtilities:
    def __init__(self):
        self.logger = logging_utilities.logger
        self.logger.info("Trying to fetch Groq API KEY")
        self.api_key = os.environ.get("API_KEY")

        if not self.api_key:
            self.logger.error(f"Groq API KEY env variable is missing")
            raise Exceptions(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                message="Internal Server Error. Please try after some tome"
            )
        self.logger.info("Successfully fetched Groq API KEY")

        self.groq_client = Groq(api_key=self.api_key)
        self.logger.info("Successfully created Groq client")

    def get_analysis(self, statement: str) -> dict:
        chat_completion = self.groq_client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a Sentiment Analysis API that outputs recipes in JSON.\n"
                    # Pass the json schema to the model. Pretty printing improves results.
                               f" The JSON object must use the schema: {json.dumps(Score.model_json_schema(), indent=2)}",
                },
                {
                    "role": "user",
                    "content": f"{statement}",
                },
            ],
            model="llama3-8b-8192",
            temperature=0,
            # Streaming is not supported in JSON mode
            stream=False,
            # Enable JSON mode by setting the response format
            response_format={"type": "json_object"},
        )
        score = Score.model_validate_json(chat_completion.choices[0].message.content)
        return {
            "positive": score.positive,
            "negative": score.negative,
            "neutral": score.neutral
        }



