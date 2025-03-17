# Fantasy Book Generator

This project generates a fantasy book using Large Language Models (LLMs) from the LangChain community. The process involves generating story ideas, creating a synopsis, structuring chapters, and drafting and verifying chapter content.

## Project Structure

```
.
├── .gitignore
├── main.py
├── prompts.py
├── generated/
```

## Requirements

- Python 3.8 or higher
- LangChain library
- Ollama models

## Setup

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/fantasy-book-generator.git
    cd fantasy-book-generator
    ```

2. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

3. Ensure the Ollama models are running locally on `http://localhost:11434`.

## Usage

To generate a fantasy book, run the `main.py` script:
```sh
python main.py
```

The script will go through the following phases:

1. **Generating Story Ideas**: Creates five detailed fantasy story ideas.
2. **Generating Synopsis**: Composes a detailed synopsis based on the generated ideas.
3. **Quality Verification**: Analyzes the synopsis for consistency, completeness, plot potential, and originality.
4. **Final Approval Check**: Checks if the synopsis meets all the required criteria.
5. **Structuring Chapters**: Generates a detailed chapter-by-chapter structure for the book.
6. **Chapter Generation and Verification**: Drafts and verifies each chapter based on the structure.
7. **Final Chapter Generation**: Produces a polished final version of each chapter.

Generated content will be saved in the `generated/` directory.

## Prompts

The prompts used for generating and verifying content are defined in `prompts.py`. They include:

- `IDEA_GENERATION_PROMPT`
- `STORY_SYNOPSIS_PROMPT`
- `QUALITY_VERIFICATION_PROMPT`
- `FINAL_APPROVAL_CHECK_PROMPT`
- `BOOK_STRUCTURE_PROMPT`
- `CHAPTER_DRAFT_PROMPT`
- `CHAPTER_VERIFICATION_PROMPT`
- `FINAL_CHAPTER_GENERATION_PROMPT`

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.