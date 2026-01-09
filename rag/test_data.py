from data_processing import load_and_split_data

docs = load_and_split_data("data")
print("TOTAL CHUNKS:", len(docs))
