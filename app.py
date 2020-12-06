import streamlit as st
import os
import time
from src.search import SearchClient


@st.cache(allow_output_mutation=True)
def load_search_client(compression_type="uncompressed"):
    if compression_type == "uncompressed":
        return SearchClient(
            os.path.join("data", "inverted_index.pkl"), os.path.join("data", "news.csv")
        )
    elif compression_type == "elias_gamma":
        return SearchClient(
            os.path.join("data", "inverted_index_gamma_compressed.pkl"),
            os.path.join("data", "news.csv"),
        )
    elif compression_type == "elias_delta":
        return SearchClient(
            os.path.join("data", "inverted_index_delta_compressed.pkl"),
            os.path.join("data", "news.csv"),
        )
    else:
        raise Exception(f"Wrong compression type: {compression_type}")


def main():
    st.sidebar.title("Compression")
    compression_type = st.sidebar.radio(
        "", options=("uncompressed", "elias_gamma", "elias_delta")
    )
    search_client = load_search_client(compression_type=compression_type)

    st.sidebar.title("Search")
    query = st.sidebar.text_input("Query")
    run_button = st.sidebar.button("Run")

    if run_button:
        start_time = time.perf_counter()
        result = search_client.search(query)
        elapsed_time = time.perf_counter() - start_time
        st.sidebar.text(f"Elapsed time: {elapsed_time:.5f}")
        st.title("Found TOP-10")
        if result:
            st.write(result)
        else:
            st.write("Nothing found")


if __name__ == "__main__":
    main()
