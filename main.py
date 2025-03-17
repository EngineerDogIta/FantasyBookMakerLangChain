from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
import os
import re

# Importing prompts from prompts.py
from prompts import (
    IDEA_GENERATION_PROMPT,
    STORY_SYNOPSIS_PROMPT,
    QUALITY_VERIFICATION_PROMPT,
    FINAL_APPROVAL_CHECK_PROMPT,
    BOOK_STRUCTURE_PROMPT,
    CHAPTER_DRAFT_PROMPT,
    CHAPTER_VERIFICATION_PROMPT,
    FINAL_CHAPTER_GENERATION_PROMPT,
)

# Function to initialize Ollama models
def initialize_ollama_model(model_name):
    """Initializes an Ollama model with a given name and returns it."""
    return Ollama(base_url="http://localhost:11434", model=model_name)

# Initializing Ollama models for different phases
creative_llm = initialize_ollama_model("deepseek-r1:1.5b")
quality_llm = initialize_ollama_model("gemma3:1b")
verifier_llm = initialize_ollama_model("gemma3:1b")
structure_llm = initialize_ollama_model("gemma3:1b")
chapter_llm = initialize_ollama_model("mistral:latest")  # Changed to mistral:latest for chapter generation
chapter_verifier_llm = initialize_ollama_model("gemma3:1b")

# Phase 1: Generating ideas
idea_prompt = PromptTemplate.from_template(IDEA_GENERATION_PROMPT)
idea_chain = idea_prompt | creative_llm

print("🎨 Generating story ideas...")
story_ideas = idea_chain.invoke({
    "theme": "Create a fantasy story set in a completely original world. Describe in detail the landscape, magical creatures, and cultures that inhabit it. The protagonist should be an unusual character, such as an inventor of magical artifacts or a guardian of living ancient libraries. Start the story with an extraordinary event that disrupts the balance of the world, such as the appearance of a comet that grants unpredictable powers or the discovery of a submerged city. Develop an engaging plot that includes mysteries to solve, unlikely alliances, and a great antagonist with complex motivations. Conclude the story with a twist that leaves the reader reflecting on the meaning of magic and destiny."
})
print(f"💡 Story ideas generated. Summary: {story_ideas[:100]}...")  # Print a snippet of the ideas

# Phase 2: Generating synopsis
story_prompt = PromptTemplate.from_template(STORY_SYNOPSIS_PROMPT)
story_chain = story_prompt | creative_llm

print("📖 Generating synopsis...")
story_synopsis = story_chain.invoke({"ideas": story_ideas})
print(f"📜 Synopsis generated. Summary: {story_synopsis[:100]}...")  # Print a snippet of the synopsis

# Phase 3: Quality verification
verification_prompt = PromptTemplate.from_template(QUALITY_VERIFICATION_PROMPT)
verification_chain = verification_prompt | quality_llm

print("🔍 Generating verification report...")
verification_report = verification_chain.invoke({"story": story_synopsis})
print(f"🔎 Verification report generated. Summary: {verification_report[:100]}...")  # Print a snippet of the report

# Phase 4: Final approval check
final_check_prompt = PromptTemplate.from_template(FINAL_APPROVAL_CHECK_PROMPT)
final_check_chain = final_check_prompt | verifier_llm

print("✅ Performing final check...")
approval = final_check_chain.invoke({"story": story_synopsis})
is_approved = "yes" in approval.lower()
print(f"✅ Final check complete. Approved: {'YES' if is_approved else 'NO'}")

# If approved, proceed with chapter structuring
if is_approved:
    # Phase 5: Structuring chapters
    structure_prompt = PromptTemplate.from_template(BOOK_STRUCTURE_PROMPT)
    structure_chain = structure_prompt | structure_llm

    print("📚 Generating book structure...")
    book_structure = structure_chain.invoke({"story": story_synopsis})
    print(f"🗂️ Book structure generated. Summary: {book_structure[:100]}...")

    # Extract book title
    book_title_match = re.search(r"TITLE:\s*(.+?)(?:\n|$)", book_structure)
    book_title = "Fantasy_Book"
    if book_title_match:
        book_title = book_title_match.group(1).strip()
        book_title = re.sub(r'[\\/*?:"<>|]', "_", book_title)  # Sanitize file name

    # Create directory for the book
    book_dir = os.path.join("generated", book_title)
    os.makedirs(book_dir, exist_ok=True)

    # Save book structure
    with open(os.path.join(book_dir, "structure.md"), "w", encoding="utf-8") as f:
        f.write(book_structure)
    print(f"💾 Book structure saved to {os.path.join(book_dir, 'structure.md')}")

    # Extract chapters from structure
    chapter_pattern = r"CHAPTER\s+(\d+):\s+([^\n]+)\s*\nSYNOPSIS:\s+([^K]+?)(?=\s*KEY EVENTS:|\s*\nCHAPTER|\s*$)"
    chapters = re.findall(chapter_pattern, book_structure, re.DOTALL)

    # Clean up extracted synopses by removing extra whitespace
    chapters = [(num, title.strip(), synopsis.strip()) for num, title, synopsis in chapters]

    # Debug output to verify extraction
    print(f"📊 Found {len(chapters)} chapters in the structure")
    for i, (num, title, synopsis) in enumerate(chapters):
        print(f"  Chapter {num}: {title} - Synopsis length: {len(synopsis)} chars")

    # Phase 6: Chapter generation and verification
    for chapter_num, chapter_title, chapter_synopsis in chapters:
        print(f"\n🖋️ Generating Chapter {chapter_num}: {chapter_title}")
        chapter_approved = False
        max_attempts = 3
        attempt = 0

        while not chapter_approved and attempt < max_attempts:
            attempt += 1
            print(f" Attempt {attempt}/{max_attempts}")

            # Generate chapter draft
            chapter_prompt_draft = PromptTemplate.from_template(CHAPTER_DRAFT_PROMPT)
            chapter_chain_draft = chapter_prompt_draft | chapter_llm

            print(" ✍️ Generating chapter draft...")
            try:
                chapter_content_draft = chapter_chain_draft.invoke({
                    "chapter_num": chapter_num,
                    "chapter_title": chapter_title,
                    "chapter_synopsis": chapter_synopsis,
                })
                print(f" ✅ Chapter draft generated. Summary: {chapter_content_draft[:100]}...")
            except Exception as e:
                print(f" ❌ Error generating chapter draft: {e}")
                continue  # Skip to next attempt

            # Verify draft consistency
            chapter_verification_prompt_instance = PromptTemplate.from_template(CHAPTER_VERIFICATION_PROMPT)
            chapter_verification_chain_instance = chapter_verification_prompt_instance | chapter_verifier_llm

            print(" 🔍 Verifying chapter draft...")
            try:
                chapter_verification_result = chapter_verification_chain_instance.invoke({
                    "chapter_num": chapter_num,
                    "chapter_title": chapter_title,
                    "chapter_synopsis": chapter_synopsis,
                    "chapter_content": chapter_content_draft,
                })
                print(f" ✅ Chapter draft verified. Summary: {chapter_verification_result[:100]}...")
            except Exception as e:
                print(f" ❌ Error verifying chapter draft: {e}")
                continue  # Skip to next attempt

            print(f" Verification result: {chapter_verification_result}")
            chapter_approved = "yes" in chapter_verification_result.lower()

        if not chapter_approved:
            print(f" ⚠️ Unable to generate an approved version of Chapter {chapter_num} after {max_attempts} attempts")
            continue
        
        # Generate final polished version of the approved draft
        final_chapter_prompt_instance = PromptTemplate.from_template(FINAL_CHAPTER_GENERATION_PROMPT)
        final_chapter_chain_instance = final_chapter_prompt_instance | chapter_llm

        print(" ✍️ Generating final polished content...")
        try:
            final_chapter_content = final_chapter_chain_instance.invoke({
                "chapter_num": chapter_num,
                "chapter_title": chapter_title,
                "chapter_synopsis": chapter_synopsis,
                "chapter_content_draft": chapter_content_draft,
            })
            print(f" ✅ Final polished content generated. Summary: {final_chapter_content[:100]}...")
        except Exception as e:
            print(f" ❌ Error generating final polished content for Chapter {chapter_num}: {e}")
            continue
        
        # Save approved final content for this chapter
        if final_chapter_content:
            chapter_filename = f"{chapter_num}.md"
            try:
                with open(os.path.join(book_dir, chapter_filename), "w", encoding="utf-8") as f:
                    f.write(f"# {chapter_title}\n\n{final_chapter_content}")
                print(f" ✅ Chapter {chapter_num} approved and saved to {os.path.join(book_dir, chapter_filename)}")
            except Exception as e:
                print(f" ❌ Error saving Chapter {chapter_num}: {e}")

else:
    print("Book generation cancelled because the initial synopsis was not approved.")
