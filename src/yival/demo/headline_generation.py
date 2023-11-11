"""
Demo code for headline generation using GPT-3.
"""

import os

from openai import OpenAI

from yival.logger.token_logger import TokenLogger
from yival.schemas.experiment_config import MultimodalOutput
from yival.states.experiment_state import ExperimentState
from yival.wrappers.string_wrapper import StringWrapper


def headline_generation(
    tech_startup_business: str, state: ExperimentState
) -> MultimodalOutput:
    """
    Demo code for headline generation using GPT-3.
    """
    logger = TokenLogger()
    logger.reset()
    # Ensure you have your OpenAI API key set up
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    # Use the chat-based completion
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{
            "role":
            "system",
            "content":
            "You are a helpful assistant that help company grow."
        }, {
            "role":
            "user",
            "content":
            str(
                StringWrapper(
                    template="""
                Generate landing one page headline for {tech_startup_business}
                """,
                    variables={
                        "tech_startup_business": tech_startup_business,
                    },
                    name="task",
                    state=state,
                )
            )
        }]
    )
    res = MultimodalOutput(text_output=response.choices[0].message.content)
    if response.usage is not None:
        token_usage = response.usage.total_tokens
    else:
        token_usage = 0
    logger.log(token_usage)
    return res
