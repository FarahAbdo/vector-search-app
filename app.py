import streamlit as st
import requests
from datetime import datetime

# Set up the page
st.set_page_config(
    page_title="Vector Search App",
    page_icon="🔍",
    layout="wide"
)

# Initialize session state
if 'search_history' not in st.session_state:
    st.session_state.search_history = []

def add_document():
    st.subheader("Add New Document")
    
    # Input form
    with st.form("add_document_form"):
        text = st.text_area("Document Text")
        category_type = st.selectbox(
            "Category",
            ["documentation", "tutorial", "guide", "other"]
        )
        
        # Show text input for custom category if "other" is selected
        if category_type == "other":
            custom_category = st.text_input("Enter custom category")
            category = custom_category if custom_category else "other"
        else:
            category = category_type
        
        submitted = st.form_submit_button("Add Document")
        
        if submitted and text:
            if category_type == "other" and not custom_category:
                st.error("Please enter a custom category")
                return
                
            # Prepare the request
            payload = {
                "query": {
                    "text": text,
                    "category": category
                }
            }
            
            try:
                # Make API call to your vectorize endpoint
                response = requests.post(
                    "http://localhost:8000/api/v1/vectorize",
                    json=payload
                )
                
                if response.status_code == 200:
                    st.success("Document added successfully!")
                else:
                    st.error(f"Error: {response.json()['detail']}")
            except Exception as e:
                st.error(f"Error: {str(e)}")

def search_documents():
    st.subheader("Search Documents")
    
    # Search form
    with st.form("search_form"):
        query = st.text_input("Search Query")
        category_type = st.selectbox(
            "Filter by Category",
            ["documentation", "tutorial", "guide", "other"]
        )
        
        # Show text input for custom category if "other" is selected
        if category_type == "other":
            custom_category = st.text_input("Enter custom category")
            category = custom_category if custom_category else "other"
        else:
            category = category_type
            
        top_k = st.slider("Number of Results", 1, 10, 3)
        
        submitted = st.form_submit_button("Search")
        
        if submitted and query:
            if category_type == "other" and not custom_category:
                st.error("Please enter a custom category")
                return
                
            payload = {
                "query": query,
                "top_k": top_k,
                "category": category
            }
            
            try:
                response = requests.post(
                    "http://localhost:8000/api/v1/search",
                    json=payload
                )
                
                if response.status_code == 200:
                    data = response.json()
                    results = data.get('results', {}).get('results', [])
                    
                    # Add to search history
                    st.session_state.search_history.append({
                        "query": query,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "results": len(results)
                    })
                    
                    # Display results
                    st.write(f"Found {len(results)} results:")
                    
                    for idx, result in enumerate(results, 1):
                        try:
                            with st.expander(f"Result {idx}"):
                                st.write(f"**Text:** {result.get('text', 'N/A')}")
                                st.write(f"**Category:** {result.get('category', 'N/A')}")
                                st.write(f"**ID:** {result.get('id', 'N/A')}")
                        except Exception as e:
                            st.error(f"Error displaying result {idx}: {str(e)}")
                else:
                    st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
            except Exception as e:
                st.error(f"Error: {str(e)}")

def show_history():
    st.subheader("Search History")
    
    if not st.session_state.search_history:
        st.info("No search history yet")
        return
        
    # Display history in a table
    history_data = {
        "Timestamp": [h["timestamp"] for h in st.session_state.search_history],
        "Query": [h["query"] for h in st.session_state.search_history],
        "Results Found": [h["results"] for h in st.session_state.search_history]
    }
    
    st.dataframe(history_data)

def main():
    st.title("Vector Search Application 🔍")
    
    # Create tabs
    tab1, tab2, tab3 = st.tabs(["Search", "Add Document", "History"])
    
    with tab1:
        search_documents()
    
    with tab2:
        add_document()
    
    with tab3:
        show_history()

if __name__ == "__main__":
    main()




# import streamlit as st
# import requests
# from datetime import datetime

# # Set up the page
# st.set_page_config(
#     page_title="Vector Search App",
#     page_icon="🔍",
#     layout="wide"
# )

# # Initialize session state
# if 'search_history' not in st.session_state:
#     st.session_state.search_history = []

# def add_document():
#     st.subheader("Add New Document")
    
#     # Input form
#     with st.form("add_document_form"):
#         text = st.text_area("Document Text")
#         category = st.selectbox(
#             "Category",
#             ["documentation", "tutorial", "guide", "other"]
#         )
        
#         submitted = st.form_submit_button("Add Document")
        
#         if submitted and text:
#             # Prepare the request
#             payload = {
#                 "query": {
#                     "text": text,
#                     "category": category
#                 }
#             }
            
#             try:
#                 # Make API call to your vectorize endpoint
#                 response = requests.post(
#                     "http://localhost:8000/api/v1/vectorize",
#                     json=payload
#                 )
                
#                 if response.status_code == 200:
#                     st.success("Document added successfully!")
#                 else:
#                     st.error(f"Error: {response.json()['detail']}")
#             except Exception as e:
#                 st.error(f"Error: {str(e)}")

# def search_documents():
#     st.subheader("Search Documents")
    
#     # Search form
#     with st.form("search_form"):
#         query = st.text_input("Search Query")
#         category = st.selectbox(
#             "Filter by Category",
#             ["All"] + ["documentation", "tutorial", "guide", "other"]
#         )
#         top_k = st.slider("Number of Results", 1, 10, 3)
        
#         submitted = st.form_submit_button("Search")
        
#         if submitted and query:
#             payload = {
#                 "query": query,
#                 "top_k": top_k,
#                 "category": None if category == "All" else category
#             }
            
#             try:
#                 response = requests.post(
#                     "http://localhost:8000/api/v1/search",
#                     json=payload
#                 )
                
#                 if response.status_code == 200:
#                     data = response.json()
#                     results = data.get('results', {}).get('results', [])
                    
#                     # Add to search history
#                     st.session_state.search_history.append({
#                         "query": query,
#                         "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#                         "results": len(results)
#                     })
                    
#                     # Display results
#                     st.write(f"Found {len(results)} results:")
                    
#                     for idx, result in enumerate(results, 1):
#                         try:
#                             with st.expander(f"Result {idx}"):
#                                 st.write(f"**Text:** {result.get('text', 'N/A')}")
#                                 st.write(f"**Category:** {result.get('category', 'N/A')}")
#                                 st.write(f"**ID:** {result.get('id', 'N/A')}")
#                         except Exception as e:
#                             st.error(f"Error displaying result {idx}: {str(e)}")
#                 else:
#                     st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
#             except Exception as e:
#                 st.error(f"Error: {str(e)}")


# def show_history():
#     st.subheader("Search History")
    
#     if not st.session_state.search_history:
#         st.info("No search history yet")
#         return
        
#     # Display history in a table
#     history_data = {
#         "Timestamp": [h["timestamp"] for h in st.session_state.search_history],
#         "Query": [h["query"] for h in st.session_state.search_history],
#         "Results Found": [h["results"] for h in st.session_state.search_history]
#     }
    
#     st.dataframe(history_data)

# def main():
#     st.title("Vector Search Application 🔍")
    
#     # Create tabs
#     tab1, tab2, tab3 = st.tabs(["Search", "Add Document", "History"])
    
#     with tab1:
#         search_documents()
    
#     with tab2:
#         add_document()
    
#     with tab3:
#         show_history()

# if __name__ == "__main__":
#     main()
