
# ProductProse - AI Product Description Generator

Welcome to **ProductProse**, an AI-powered tool for generating and customizing product descriptions using IBM Granite LLMs.

## Features

- **Generate Product Descriptions**: Create professional and engaging product descriptions based on input data.
- **Translate Descriptions**: Translate generated descriptions into multiple languages.
- **Customize Descriptions**: Tailor descriptions to match your brand's tone and style.
- **SEO Optimization**: Add keywords to optimize descriptions for search engines.
- **User Feedback**: Collect feedback on the quality of generated descriptions.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/IIPatel/ProductProse
    cd ProductProse
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up your IBM WatsonX API credentials:
    - Create a `.env` file in the root directory.
    - Add your `WATSONX_PROJECT_ID` and `WATSONX_API_KEY` to the `.env` file:
        ```env
        WATSONX_PROJECT_ID=your_project_id
        WATSONX_API_KEY=your_api_key
        ```

## Usage

1. Run the Streamlit app:
    ```bash
    streamlit run app.py
    ```

2. Open your web browser and go to `http://localhost:8501`.

3. Input your product data in the sidebar:
    - **Product Name**
    - **Product Features**
    - **Product Benefits**
    - **Product Specifications**

4. Select the target language for translation.

5. Follow the steps to generate, translate, and customize your product description.

## Steps

### Step 1: Generate Product Description

- Click the "Generate Description" button to create a product description based on the input data.

### Step 2: Translate Product Description

- Click the "Translate Description" button to translate the generated description into the selected language.

### Step 3: Customize Product Description

- Input customization requests and click the "Customize Description" button to tailor the description to your brand's tone and style.

### Step 4: Provide Feedback

- Rate the quality of the generated description and provide additional comments.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [IBM WatsonX](https://www.ibm.com/watsonx) for providing the AI models and API.
- [Streamlit](https://streamlit.io) for the web app framework.

---
