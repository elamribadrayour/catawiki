import streamlit

streamlit.title("Machine Learning For Catawiki")

# Introduce yourself
streamlit.write("""
Hello! I am EL AMRI BADRAYOUR, and welcome to my Catawiki Machine Learning Solutions App.

In this application, I aim to provide innovative solutions tailored for Catawiki, focusing on enhancing user experience and platform efficiency through advanced machine learning techniques.
""")

streamlit.header("Project Overview")

# Describe the main objectives in the first person
streamlit.write(
    """In this project, I present a suite of machine learning tools designed to optimize key areas of the Catawiki platform:"""
)

streamlit.page_link(
    page="pages/1_🔍_search.py",
    label="🔍 Search: I aim to enhance the search functionality to deliver more relevant results to users.",
)
streamlit.page_link(
    page="pages/2_🔄_reranking.py",
    label="🔄 Reranking: I implement reranking algorithms to improve the order of items displayed, ensuring the most relevant items are prioritized.",
)
streamlit.page_link(
    page="pages/3_🤝_recommendations.py",
    label="🤝 Recommendations: I develop personalized recommendation systems to suggest items that users are most likely to be interested in.",
)

streamlit.header("Solutions")

streamlit.subheader("1. 🔍 Search Enhancement")
streamlit.write("""
My search solutions utilize natural language processing and advanced search algorithms to improve the accuracy and relevance of search results. By understanding user intent and item characteristics, I strive to deliver a seamless search experience.
""")

streamlit.subheader("2. 🔄 Reranking Algorithms")
streamlit.write("""
The reranking component leverages machine learning models to reorder search results based on predicted relevance and user preferences. This ensures that users see the most pertinent items first.
""")

streamlit.subheader("3. 🤝 Recommendation Systems")
streamlit.write("""
My recommendation systems are designed to personalize the shopping experience. By analyzing user behavior and item features, I provide tailored suggestions that align with individual user interests.
""")

# Optionally, add contact or further information
streamlit.header("Contact & Further Information")
streamlit.write("""
For more details about each solution or to get involved, please feel free to contact me at [badrayour.elamri@protonmail.com](mailto:badrayour.elamri@protonmail.com).
""")
