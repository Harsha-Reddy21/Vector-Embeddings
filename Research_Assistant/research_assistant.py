import os
import streamlit as st
import time
from dotenv import load_dotenv
from utils.pdf_processor import extract_text_from_pdf, chunk_text
from utils.embeddings import get_embedding_model
from utils.vector_store import create_collection, store_chunks
from utils.retrieval import sparse_search, hybrid_retrieval, rerank_results
from utils.web_search import web_search_serper
from utils.response_generator import generate_response
from utils.monitoring import log_query, log_response

# Load environment variables
load_dotenv()

# Check for API keys
if not os.getenv("GROQ_API_KEY"):
    st.error("⚠️ GROQ_API_KEY not found in .env file")
if not os.getenv("SERP_API_KEY"):
    st.error("⚠️ SERP_API_KEY not found in .env file")

# Initialize session state
if "chunks" not in st.session_state:
    st.session_state.chunks = None
if "collection" not in st.session_state:
    st.session_state.collection = None
if "pdf_name" not in st.session_state:
    st.session_state.pdf_name = None
if "query_history" not in st.session_state:
    st.session_state.query_history = []
if "response_history" not in st.session_state:
    st.session_state.response_history = []

# App title and description
st.title("Research Assistant")
st.markdown("""
This app combines PDF document analysis with web search to provide comprehensive answers to your questions.
Upload a PDF document, ask a question, and get answers with citations from both the document and the web.
""")

# Sidebar for configuration
st.sidebar.title("Configuration")
retrieval_method = st.sidebar.selectbox(
    "Retrieval Method",
    ["Hybrid (Dense + Sparse)", "Dense Only", "Sparse Only"]
)
use_reranking = st.sidebar.checkbox("Use Cross-Encoder Reranking", value=True)
web_results_count = st.sidebar.slider("Number of Web Results", 0, 10, 3)
temperature = st.sidebar.slider("Response Temperature", 0.0, 1.0, 0.3)

# File uploader
uploaded_file = st.file_uploader("Upload a PDF document", type="pdf")

if uploaded_file:
    # Process the PDF if it's new or different from the last one
    if st.session_state.pdf_name != uploaded_file.name:
        with st.spinner("Processing PDF..."):
            # Save the uploaded file temporarily
            temp_file_path = f"temp_{uploaded_file.name}"
            with open(temp_file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Extract text from PDF
            text = extract_text_from_pdf(temp_file_path)
            
            # Chunk the text
            chunks = chunk_text(text)
            
            # Get embedding model
            embedding_model = get_embedding_model()
            
            # Create and store embeddings
            collection = create_collection("pdf_chunks")
            store_chunks(chunks, collection, embedding_model)
            
            # Update session state
            st.session_state.chunks = chunks
            st.session_state.collection = collection
            st.session_state.pdf_name = uploaded_file.name
            
            # Clean up
            os.remove(temp_file_path)
        
        st.success(f"✅ Processed {len(chunks)} chunks from {uploaded_file.name}")

    # Query input
    query = st.text_input("Ask a question about the document:")
    
    if query and st.session_state.chunks and st.session_state.collection:
        if query not in st.session_state.query_history:
            with st.spinner("Searching for answers..."):
                # Log the query
                query_id = log_query(query, st.session_state.pdf_name)
                
                # Get embedding model
                embedding_model = get_embedding_model()
                
                # Retrieve relevant chunks based on selected method
                if retrieval_method == "Dense Only":
                    dense_emb = embedding_model.encode(query)
                    results = st.session_state.collection.query(
                        query_embeddings=[dense_emb.tolist()], 
                        n_results=5
                    )
                    top_pdf_chunks = results['documents'][0]
                elif retrieval_method == "Sparse Only":
                    sparse_results = sparse_search(query, st.session_state.chunks)
                    top_pdf_chunks = [chunk for chunk, _ in sparse_results]
                else:  # Hybrid
                    top_pdf_chunks = hybrid_retrieval(
                        query, 
                        st.session_state.chunks, 
                        st.session_state.collection,
                        embedding_model
                    )
                
                # Apply reranking if enabled
                if use_reranking and len(top_pdf_chunks) > 1:
                    top_pdf_chunks = rerank_results(query, top_pdf_chunks)
                
                # Search the web if web results are requested
                if web_results_count > 0:
                    web_results = web_search_serper(query, web_results_count)
                else:
                    web_results = []
                
                # Generate response
                response = generate_response(
                    query, 
                    top_pdf_chunks, 
                    web_results,
                    temperature
                )
                
                # Log the response
                log_response(query_id, response)
                
                # Update session state
                st.session_state.query_history.append(query)
                st.session_state.response_history.append({
                    "query": query,
                    "response": response,
                    "pdf_chunks": top_pdf_chunks,
                    "web_results": web_results
                })
        
        # Display the most recent response
        if st.session_state.response_history:
            latest = st.session_state.response_history[-1]
            st.markdown("### Answer")
            st.write(latest["response"])
            
            # Show sources
            with st.expander("View Sources"):
                st.markdown("#### PDF Sources")
                for i, chunk in enumerate(latest["pdf_chunks"]):
                    st.text_area(f"PDF Chunk {i+1}", chunk, height=100)
                
                st.markdown("#### Web Sources")
                for i, result in enumerate(latest["web_results"]):
                    st.markdown(f"{i+1}. [{result.get('title', 'No title')}]({result.get('link', '#')})")
                    st.write(result.get('snippet', 'No snippet available'))
            
            # Show query history
            with st.expander("Query History"):
                for i, hist in enumerate(st.session_state.response_history):
                    st.markdown(f"**Query {i+1}:** {hist['query']}")
else:
    st.info("Please upload a PDF document to get started.")

# Footer
st.markdown("---")
st.markdown("Research Assistant combines PDF analysis with web search for comprehensive answers.") 