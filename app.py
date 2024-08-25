import streamlit as st
from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.foundation_models.utils.enums import ModelTypes, DecodingMethods
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
import os

# Set up page configuration
st.set_page_config(page_title="ProductProse - AI Product Description Generator", layout="wide")

# Initialize session state to track API responses and user feedback
if 'generated_description' not in st.session_state:
    st.session_state.generated_description = None
if 'translated_description' not in st.session_state:
    st.session_state.translated_description = None
if 'customized_description' not in st.session_state:
    st.session_state.customized_description = None
if 'feedback' not in st.session_state:
    st.session_state.feedback = None

# Sidebar for product data input
st.sidebar.title("Product Data Input")
product_name = st.sidebar.text_input("Product Name", "Example Product")
features = st.sidebar.text_area("Product Features", "Feature 1, Feature 2, Feature 3")
benefits = st.sidebar.text_area("Product Benefits", "Benefit 1, Benefit 2, Benefit 3")
specifications = st.sidebar.text_area("Product Specifications", "Specification 1, Specification 2, Specification 3")

# Select target language for translation
target_language = st.sidebar.selectbox("Target Language for Translation",  ["Arabic", "Chinese", "French", "German", "Japanese", "Portugese", "Russian", "Spanish", "Urdu"])

# Main app title and description
st.title("ProductProse - AI Product Description Generator")
st.markdown("""
Welcome to ProductProse, an AI-powered tool for generating and customizing product descriptions using IBM Granite LLMs.
Simply input your product data and let the AI do the rest, including generating descriptions, translating them into multiple languages, and customizing them to match your brand tone and style.
""")

# IBM WatsonX API Setup
project_id = os.getenv('WATSONX_PROJECT_ID')
api_key = os.getenv('WATSONX_API_KEY')

if api_key and project_id:
    credentials = Credentials(url="https://us-south.ml.cloud.ibm.com", api_key=api_key)
    client = APIClient(credentials)
    client.set.default_project(project_id)

    # Tone Selection for Description Customization
    tone_example = st.sidebar.selectbox("Select Example Tone (Feel free to modify)", ["Formal", "Casual", "Professional", "Playful"])
    st.sidebar.markdown("_Example: You can choose a tone that best fits your brand's style._")

    # Keyword Input for SEO Optimization
    seo_keywords_example = st.sidebar.text_area("SEO Keywords (comma-separated, e.g., 'smart home, automation')", "smart home, intelligent, automation")
    st.sidebar.markdown("_Example: Add keywords to optimize for search engines._")

    # Step 1: Generate Product Description
    st.header("Step 1: Generate Product Description")
    if st.button("Generate Description"):
        if product_name and features and benefits and specifications:
            # Prompt engineering for Granite-13B-Instruct
            prompt = f"""
            You are an AI that generates high-quality product descriptions. Based on the following details, generate a professional and engaging product description:\n
            Product Name: {product_name}\n
            Features: {features}\n
            Benefits: {benefits}\n
            Specifications: {specifications}\n
            Generate only the final product description text, without including any instruction or prompt context.
            """
            try:
                model = ModelInference(model_id=ModelTypes.GRANITE_13B_INSTRUCT_V2, params={
                    GenParams.DECODING_METHOD: DecodingMethods.GREEDY,
                    GenParams.MIN_NEW_TOKENS: 50,
                    GenParams.MAX_NEW_TOKENS: 200,
                    GenParams.STOP_SEQUENCES: ["\n"]
                }, credentials=credentials, project_id=project_id)

                with st.spinner("Generating product description..."):
                    description_response = model.generate_text(prompt=prompt)
                    st.session_state.generated_description = description_response
                    st.session_state.translated_description = None  # Clear previous translations
                    st.success("Product description generated!")
                    st.write(description_response)
            except Exception as e:
                st.error(f"An error occurred while generating the description: {e}")
        else:
            st.warning("Please fill in all the product data fields before generating a description.")

    # Step 2: Translate Product Description
    st.header("Step 2: Translate Product Description")
    if st.session_state.generated_description:
        if st.button("Translate Description"):
            try:
                # Translate the description using Granite-20B-Multilingual
                prompt = f"Translate the following product description into {target_language}:\n{st.session_state.generated_description}"
                model = ModelInference(model_id=ModelTypes.GRANITE_20B_MULTILINGUAL, params={
                    GenParams.DECODING_METHOD: DecodingMethods.GREEDY,
                    GenParams.MIN_NEW_TOKENS: 50,
                    GenParams.MAX_NEW_TOKENS: 200,
                    GenParams.STOP_SEQUENCES: ["\n"]
                }, credentials=credentials, project_id=project_id)

                with st.spinner(f"Translating product description to {target_language}..."):
                    translation_response = model.generate_text(prompt=prompt)
                    st.session_state.translated_description = translation_response
                    st.success(f"Product description translated to {target_language}!")
                    st.write(translation_response)
            except Exception as e:
                st.error(f"An error occurred while translating the description: {e}")

    # Display previous results
    if st.session_state.generated_description:
        st.subheader("Generated Product Description")
        st.write(st.session_state.generated_description)

    if st.session_state.translated_description:
        st.subheader(f"Translated Product Description ({target_language})")
        st.write(st.session_state.translated_description)

    # Step 3: Customize Product Description via Chat Interface
    st.header("Step 3: Customize Product Description")
    customization_prompt = st.text_input("Customize the product description (Feel free to modify the example tone and SEO keywords)")

    if st.session_state.generated_description and customization_prompt:
        if st.button("Customize Description"):
            try:
                # Customize the description using Granite-13B-Chat
                prompt = f"Customize the following product description with a {tone_example} tone, using the following SEO keywords: {seo_keywords_example}.\nProduct Description:\n{st.session_state.generated_description}\nCustomization Request: {customization_prompt}\nGenerate only the final customized product description."
                model = ModelInference(model_id=ModelTypes.GRANITE_13B_CHAT_V2, params={
                    GenParams.DECODING_METHOD: DecodingMethods.GREEDY,
                    GenParams.MIN_NEW_TOKENS: 50,
                    GenParams.MAX_NEW_TOKENS: 200,
                    GenParams.STOP_SEQUENCES: ["\n"]
                }, credentials=credentials, project_id=project_id)

                with st.spinner("Customizing product description..."):
                    customization_response = model.generate_text(prompt=prompt)
                    st.session_state.customized_description = customization_response
                    st.success("Product description customized!")
                    st.write(customization_response)
            except Exception as e:
                st.error(f"An error occurred while customizing the description: {e}")

    # Display customized result if available
    if st.session_state.customized_description:
        st.subheader("Customized Product Description")
        st.write(st.session_state.customized_description)

    # Step 4: Feedback and Quality Scoring
    st.header("Step 4: Provide Feedback")
    feedback = st.slider("Rate the quality of the generated product description (1 = Poor, 5 = Excellent)", 1, 5, 3)
    feedback_comments = st.text_area("Additional Comments")

    if st.button("Submit Feedback"):
        st.session_state.feedback = {"rating": feedback, "comments": feedback_comments}
        st.success("Thank you for your feedback!")
        st.write(st.session_state.feedback)

else:
    st.error("IBM WatsonX API credentials are not set. Please check your environment variables.")