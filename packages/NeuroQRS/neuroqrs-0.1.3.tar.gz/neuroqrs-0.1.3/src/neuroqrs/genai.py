import openai, json
from typing import List
from pydantic import BaseModel

client = openai.AsyncOpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    # or set/uncomment below
    #api_key="<api key>"
)

class SuggestedQueries(BaseModel):
    """Suggested Queries model"""
    suggestions: List[str]

async def get_genai_suggestions(partial_query: str, context: dict, fields_info: dict, n_queries: int = 10) -> SuggestedQueries:
    """Get genai suggestions for the given partial query, context and fields_info, Uses latest function call architecture.

    :param partial_query: The partial query for which suggestions are needed
    :param context: The context for the query
    :param fields_info: The fields information
    :param n_queries: Number of queries to suggest, defaults to 10
    :type partial_query: str\
    :type context: dict
    :type fields_info: dict
    :type n_queries: int, optional
    :return: Suggested queries
    :rtype: :class:`SuggestedQueries`
    """
    response = await client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an AI assistant guiding user towards better ecommerce search. You are given a partial query and some context (might not be avaliable), Use it to generate query autocompletion for the user, Important: Only give autocompletions, ie keep the prefix same and suggest change the suffix, Make only coherent meaningful sentences."},
            {"role": "user", "content": f"Call function with {n_queries} autocompletions, Partial Query: {partial_query}, Supporting Data: {json.dumps(context)} and avaliable fields: {json.dumps(fields_info)}"}
        ],
        functions=[
            {
            "name": "get_suggested_queries",
            "description": "Get autocompletion queries for the user based on the partial query and context",
            "parameters": SuggestedQueries.model_json_schema()
            }
        ],
        function_call={"name": "get_suggested_queries"},
        temperature=0.5,
    )

    output = json.loads(response.choices[0].message.function_call.arguments)
    return SuggestedQueries(**output)