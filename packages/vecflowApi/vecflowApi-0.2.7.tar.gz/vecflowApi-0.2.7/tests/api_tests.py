"""Tests for pip module"""

import time

from vecflowapi.Client import Client

client = Client()

api_list = client.generate_api_key("testuser1221", "testpassword")
auth_client = Client(api_list)

test_pipeline = auth_client.get_pipeline("clement_test12e2wssysw")

# test_pipeline = auth_client.create_pipeline(
#     "clement_test12e2wssysw",
#     splitter_args={"chunk_size": 400, "chunk_overlap": 40, "length_function": "len"},
#     embedder_type="OpenAI_003_Small",
#     embedder_args={"api_key": "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"},
#     vector_store_args={
#         "api_key": "371b67fa-0889-44e1-b538-e66208a6769b",
#         "environment": "us-east-1-aws",
#         "index": "apis",
#     },
# )

test_pipeline.upload("test.txt")

proceed = input("Should I proceed? (yes/no): ").lower()
if proceed != "yes":
    exit()


start_time = time.time()

res = test_pipeline.query(
    query="What are Lina Khan's criticism's of Prime?",
    llm_config={
        "provider": "together_ai",
        "model": "zero-one-ai/Yi-34B-Chat",
        "api_key": "28b655a6430d7b94996808735856408a47928a37a1c32f10751fcb6e8bde7805",
    },
    retrieval_method={
        "type": "Simple",
        "dense_search_top_k": 10,
        "reranker_top_k": 5,
        "num_neighbors": 1,
    },
    prompt="given this information:{retrieved}, answer this question: {query}",
    history=[],
)
print(res["Reply"])

end_time = time.time()
time_taken = end_time - start_time
print("Time taken for query response:", time_taken)
