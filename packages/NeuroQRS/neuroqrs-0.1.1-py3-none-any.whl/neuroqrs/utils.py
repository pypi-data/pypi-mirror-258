import faiss

def create_empty_faiss_index(dim):
    "Create a new index"
    return faiss.IndexFlatIP(dim)

def get_faiss_index(loc):
    "Get the index"
    try:
        return faiss.read_index(loc + ".index")
    except FileNotFoundError as err:
        raise f"Unable to find {loc}, does the file exist? from {err}"

def add_doc_to_index(index: faiss.IndexFlatIP, embedded_document_text):
    "Add doc to index"
    index.add(embedded_document_text)

def search_index(embedded_query, index: faiss.IndexFlatIP, doc_map, k=5, minimum_score_threshold: float = 0.7, return_scores: bool = True,):
    "Search through the index"
    D, I = index.search(embedded_query, k)
    print(D, I)
    if return_scores:
        value = [{doc_map[idx]: str(score)} for idx, score in zip(I[0], D[0]) if (idx < len(doc_map) and float(score) > minimum_score_threshold)]
    else:
        value = [doc_map[idx] for idx, score in zip(I[0], D[0]) if (idx < len(doc_map) and float(score) > minimum_score_threshold)]
    return value

def save_index(index, loc):
    "Save the index and dataset pickle file to local"
    try:
        faiss.write_index(index, loc + ".index")
    except Exception as err:
        raise err
    
def get_text_queries(loc):
    "Get the text queries"
    try:
        with open(loc + ".txt", 'r') as file:
            return file.read().splitlines()
    except FileNotFoundError as err:
        raise f"Unable to find {loc}, does the file exist? from {err}"
    except Exception as err:
        raise err
    
def save_text_queries(queries, loc):
    "Save the text queries"
    with open(loc + ".txt", 'w') as file:
        file.write('\n'.join(queries))