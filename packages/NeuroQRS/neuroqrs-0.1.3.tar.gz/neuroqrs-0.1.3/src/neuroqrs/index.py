import faiss, os
from neuroqrs.utils import create_empty_faiss_index, get_faiss_index, get_text_queries, save_index, save_text_queries, add_doc_to_index, search_index

class NeuroIndex:
    "Faiss powered index for searching through the dataset"
    def __init__(self, namespace: str = "", dim: int = 768):
        """Initialize the NeuroIndex
        
        :param namespace: Namespace for the index, defaults to ""
        :param dim: Dimension of the index, defaults to 768
        :type namespace: str
        :type dim: int
        """
        self.namespace = namespace
        self.dim = dim

        try:
            # Load the index from namespace if it exists
            self.index = get_faiss_index(namespace)
            self.queries = get_text_queries(namespace)
        except Exception as err:
            # Create a new index if it doesn't exist
            self.index = create_empty_faiss_index(dim)
            self.queries = []

    def add(self, document_text: str, embedded_document_text):
        """Add a document to the index and save the query

        :param document_text: Document text
        :param embedded_document_text: Embedded document text
        :type document_text: str
        :type embedded_document_text: list
        """
        add_doc_to_index(self.index, embedded_document_text)
        self.queries.append(document_text)

    def search(self, embedded_query: list, k: int = 5, return_scores: bool = False):
        """Search the index for the given query

        :param embedded_query: Embedded query
        :param k: Number of results to return
        :param return_scores: Return scores or not
        :type embedded_query: list
        :type k: int
        :type return_scores: bool
        :return: List of results
        :rtype: list
        """
        return search_index(embedded_query, self.index, self.queries, k=k, return_scores=return_scores)

    def save(self):
        "Save the index to the namespace"
        # Make folders if they don't exist
        if not os.path.exists(os.path.dirname(self.namespace)):
            if os.path.dirname(self.namespace):
                os.makedirs(os.path.dirname(self.namespace))
    
        save_index(self.index, self.namespace)
        save_text_queries(self.queries, self.namespace)

    @staticmethod
    def from_namespace(namespace: str, dim: int = 768):
        "Create a new index from existing namespace"
        return NeuroIndex(namespace=namespace, dim=dim)