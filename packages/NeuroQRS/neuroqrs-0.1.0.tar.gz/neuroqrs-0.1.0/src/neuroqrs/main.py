import os
from typing import Union
import numpy as np
from sentence_transformers import SentenceTransformer

from neuroqrs.index import NeuroIndex
from neuroqrs.genai import get_genai_suggestions

index_caches = {}

class NeuroQRS:
    "NeuroQRS main class"
    def __init__(self, embedding_model = "all-mpnet-base-v2", model_dim: int = 768):
        """Initialize the NeuroQRS
        
        :param embedding_model: SentenceTransformer model to use, defaults to "all-mpnet-base-v2"
        :param model_dim: Dimension of the model, defaults to 768
        :type embedding_model: str
        :type model_dim: int
        """
        self.model = SentenceTransformer(embedding_model)
        self.model_dim = model_dim

    async def quick_query(self, query: Union[str, np.array], namespace: str, k: int = 5):
        """Quickly query the index

        :param query: partial query to search or embedded query
        :param namespace: Namespace associated
        :param k: Number of results to return
        :type query: str
        :type index: str
        :type k: int
        :return: List of results
        :rtype: list
        """

        if namespace not in index_caches:
            index_caches[namespace] = NeuroIndex.from_namespace(namespace, dim=self.model_dim)

        if isinstance(query, str):
            query = self.model.encode([query], convert_to_numpy=True)

        return index_caches[namespace].search(query, k=k)
    

    async def query_and_index(self, query: str, namespace: str, extra_documents_data: dict, fields_info: dict = {}, k: int = 5):
        """Query and index the document (slow, uses even genai to improve context)

        :param query: partial query to search
        :param namespace: Namespace associated
        :param extra_documents_data: extra supporting data, simply dumped to llm prompt
        :param fields_info: fields information (ie what filters are avaliable for the search)
        :param k: Number of results to return
        :type query: str
        :type namespace: str
        :type extra_documents_data: dict
        :type fields_info: dict
        :type k: int
        :return: List of results
        :rtype: list
        """
    
        if namespace not in index_caches:
            index_caches[namespace] = NeuroIndex.from_namespace(namespace, dim=self.model_dim)

        query_embeddings = self.model.encode([query], convert_to_numpy=True)

        # First use genai and prompting to build more results context XD
        # Then index the document
        suggestions = (await get_genai_suggestions(query, extra_documents_data, fields_info)).suggestions
        for suggestion in suggestions:
            index_caches[namespace].add(suggestion, self.model.encode([suggestion], convert_to_numpy=True))

        # Also save the index
        index_caches[namespace].save()

        return index_caches[namespace].search(query_embeddings, k=k)
    
    async def query_maybe_index(self, query: str, namespace: str, extra_documents_data: dict, fields_info: dict = {}, k: int = 5):
        """Query the document quickly for results, if not enough results then index the document and query again (might be slow)
        
        :param query: partial query to search
        :param namespace: Namespace associated
        :param extra_documents_data: extra supporting data, simply dumped to llm prompt
        :param fields_info: fields information (ie what filters are avaliable for the search)
        :param k: Number of results to return
        :type query: str
        :type namespace: str
        :type extra_documents_data: dict
        :type fields_info: dict
        :type k: int
        :return: List of results
        :rtype: list
        """

        # First try to quickly query the index
        results = await self.quick_query(query, namespace, k=k)
        if results and len(results) > 3:
            return results
        else:
            print("Quick query failed, trying to index the document")
            return await self.query_and_index(query, namespace, extra_documents_data, fields_info, k=k)

if __name__ == "__main__":
    neuroqrs = NeuroQRS()
    async def main():
        print(await neuroqrs.query_maybe_index("nike good", "indexeess/nike", extra_documents_data={}, fields_info={"color": ["red", "blue", "green"], "size": ["small", "medium", "large"], "category": ["shoes", "clothes", "accessories", "sandals"], "division": ["men", "women"]}))

    import asyncio
    asyncio.run(main())