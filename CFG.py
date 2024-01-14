class CFG:
    vector_db_path = 'Vector_dbs'
    model_name = 'mistralai/Mistral-7B-Instruct-v0.1'
    temperature = 0.05
    top_p = 0.1
    repetition_penalty = 1.11
    do_sample = True
    max_new_tokens = 200
    num_return_sequences = 1

    # Деление на чанки
    split_chunk_size = 200
    split_overlap = 1
    embeddings_model_repo = 'sentence-transformers/all-MiniLM-L6-v2'
    k = 3



