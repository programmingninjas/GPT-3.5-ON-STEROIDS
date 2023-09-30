# GPT 3.5 ON STEROIDS: Autonomous Agent with knowledge beyond 2021

Welcome to GPT 3.5 ON STEROID, an open-source project that enhances the capabilities of GPT by integrating it with various Python libraries and APIs for advanced text generation.

## Requirements

Make sure you have the following Python libraries installed:
- `openai`
- `google-serp-api`
- `tiktoken`
- `wikipedia`
- `trafilatura`
- `streamlit`
- `google-search-results`

Additionally, you'll need API keys for the following services:
- [SerpAPI](https://serpapi.com/)
- [OpenAI](https://openai.com/)

## Running Streamlit

To run the Streamlit application, execute the following command in your terminal:

```bash
streamlit run app.py
```

## Integrated Python Functions (Tools)

GPT 3.5 ON STEROID incorporates various Python functions that GPT can call and use, including:

- **Web Scraping:** Utilizing `google-serp-api` and `trafilatura` for dynamic data retrieval.
- **Natural Language Processing:** Using `tiktoken` for language processing tasks.
- **Information Retrieval:** Accessing data from `wikipedia` for comprehensive information retrieval.
- **User Interface:** Employing `streamlit` for creating a user-friendly interface.

**Note:** Whenever a new tool is added, please ensure the following:
- Update the `requirements.txt` file to include the new tool/library.
- Update the `README.md` file to document the newly added tool and its functionality.
- Ensure that your feature does not break the application test before merging.

## Contribution Guidelines

We welcome contributions from the community to make GPT 3.5 ON STEROID even better! Please follow these guidelines:

1. **Fork the repository and create your branch:** `git checkout -b feature/new-contribution`
2. **Make your changes and test thoroughly.**
3. **Commit your changes:** `git commit -m "Add a brief description of your changes"`
4. **Push to your forked repository:** `git push origin feature/new-contribution`
5. **Create a pull request to the main repository.**

### Code of Conduct

Please review our [Code of Conduct](CODE_OF_CONDUCT.md) to understand the community standards.

## Join the Hacktoberfest Fun!

Celebrate Hacktoberfest with us! We encourage developers of all levels to participate. Happy coding!

## License

This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/programmingninjas/GPT-3.5-ON-STEROIDS/blob/main/LICENSE) file for details.
