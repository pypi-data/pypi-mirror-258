import os, requests, json, time, sys
import multiprocessing

def get_plain_text_from_url(url):
    from bs4 import BeautifulSoup
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup.get_text()
    except:
        return ""


def llm_answer(question, relevant_content, llm):
    return llm(f"""
    {relevant_content}

    Given the above, concisely, in as few words as possible, answer the following question:
    {question}
    """)

def parallel(func, args):
    t0 = time.time()
    cpus = multiprocessing.cpu_count()
    with multiprocessing.Pool(processes=cpus) as pool:
        result = pool.map(func, args)
    t1 = time.time()
    print(f"Parallel execution took {t1-t0} seconds for {str(func)} on {len(args)} items")
    return result

def research(question: str, llm):
    from ragatouille import RAGPretrainedModel
    from ragatouille.data import CorpusProcessor
    from duckduckgo_search import DDGS

    t_start = time.time()
    t0 = time.time()
    query = question
    ddgs = DDGS()
    results = ddgs.text(query)
    urls = [result['href'] for result in results]
    t1 = time.time()
    print(f"Got {len(urls)} search results in {t1-t0} seconds..")

    content = parallel(get_plain_text_from_url, urls)
    print(f"Got {len(content)} documents.. splitting into chunks")

    t0 = time.time()
    corpus_processor = CorpusProcessor()
    documents = [x["content"] for x in corpus_processor.process_corpus(content, chunk_size=200)]
    t1 = time.time()
    print(f"Processed {len(documents)} documents in {t1-t0} seconds.. reranking with Colbert")

    t0 = time.time()
    colbert = RAGPretrainedModel.from_pretrained("colbert-ir/colbertv2.0")
    relevant_content = [x["content"] for x in colbert.rerank(query=query, documents=documents, k=3)]
    t1 = time.time()
    print(f"Got {len(relevant_content)} relevant documents in {t1-t0} seconds.. answering w/ LLM")

    #answers = parallel(llm, relevant_content)

    t0 = time.time()
    final_answer = llm_answer(query, "\n\n...".join(relevant_content), llm)
    t1 = time.time()
    print(f"{final_answer} \n\nLLM returned in {t1-t0} seconds..")
    t_end = time.time()
    print(f"Total time: {t_end-t_start} seconds..")
