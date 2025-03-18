# Fantasy Book Generator

![Python Version](https://img.shields.io/badge/python-3.13.2-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![GitHub Issues](https://img.shields.io/github/issues/EngineerDogIta/fantasy-book-generator)

This project generates a fantasy book using Large Language Models (LLMs) from the LangChain community. The process involves generating story ideas, creating a synopsis, structuring chapters, and drafting and verifying chapter content.

## Project Structure

The repository contains the following key files and folders:

- **main.py**: The main script that orchestrates the story generation process.
- **prompts.py**: Contains the prompt templates for various phases (idea generation, synopsis, quality verification, etc.).
- **generated/**: When the `main.py` script is executed and a synopsis is approved, this folder is created (if it doesn't already exist) with:
  - A subdirectory named after the book title (e.g., `Echoes of the Veil`), containing:
    - `structure.md`: A file outlining the detailed book structure and chapter breakdown.
    - One Markdown file per chapter (e.g., `1.md`, `2.md`, etc.) with the final polished chapter content.
- **README.md**: This documentation file.
- **requirements.txt**: Lists the required dependencies for the project.
- **LICENSE**: The project’s license file.

## Requirements

- Python 3.13.2 or higher
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

3. Install Ollama and the required models:
    - Download and install [Ollama](https://ollama.ai) following their official instructions.
    - Ensure the following models are installed and available:
        - deepseek-r1:1.5b
        - gemma3:1b
        - mistral:latest
    - Start the Ollama models locally on `http://localhost:11434`.

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

Generated content will be saved in the `generated/` directory under a subfolder corresponding to the book title.

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

## LLMs to Pull from Ollama

Ensure the following LLMs are pulled and available from Ollama:

- `deepseek-r1:1.5b` for creative idea generation
- `gemma3:1b` for quality verification and structure generation
- `mistral:latest` for chapter generation