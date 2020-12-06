import streamlit as st
import os
from src.search import SearchClient


@st.cache(allow_output_mutation=True)
def load_search_client():
    return SearchClient(
        os.path.join("data", "inverted_index.pkl"), os.path.join("data", "news.csv")
    )


def main():
    search_client = load_search_client()

    st.sidebar.title("Search")
    query = st.sidebar.text_input("Query")
    run_button = st.sidebar.button("Run")

    if run_button:
        result = search_client.search(query)
        st.title("Found TOP-10")
        if result:
            st.write(result)
        else:
            st.write("Nothing found")


if __name__ == "__main__":
    main()
