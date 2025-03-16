from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
import os
import re

# Function to initialize Ollama models
def initialize_ollama_model(model_name):
    """Initializes an Ollama model with a given name and returns it."""
    return Ollama(base_url="http://localhost:11434", model=model_name)

# Inizializzazione modelli Ollama per le diverse fasi
creative_llm = initialize_ollama_model("deepseek-r1:1.5b")
quality_llm = initialize_ollama_model("gemma3:1b")
verifier_llm = initialize_ollama_model("gemma3:1b")
structure_llm = initialize_ollama_model("deepseek-r1:1.5b")
chapter_llm = initialize_ollama_model("mistral:latest") # Changed to mistral:latest for chapter generation
chapter_verifier_llm = initialize_ollama_model("gemma3:1b")

# Fase 1: Generazione idee
idea_prompt = PromptTemplate.from_template("""
Generate 5 creative ideas for a fantasy story based on the following theme:
{theme}
Include:
- Unique setting
- 2-3 magical creatures
- Culture of the inhabitants
- Triggering event
- Complex antagonist
""")

idea_chain = idea_prompt | creative_llm
print("🎨 Generating story ideas...")
story_ideas = idea_chain.invoke({
    "theme": "Create a fantasy story set in a completely original world. Describe in detail the landscape, magical creatures, and cultures that inhabit it. The protagonist should be an unusual character, such as an inventor of magical artifacts or a guardian of living ancient libraries. Start the story with an extraordinary event that disrupts the balance of the world, such as the appearance of a comet that grants unpredictable powers or the discovery of a submerged city. Develop an engaging plot that includes mysteries to solve, unlikely alliances, and a great antagonist with complex motivations. Conclude the story with a twist that leaves the reader reflecting on the meaning of magic and destiny."
})

print("✅ Story ideas generated.")

# Fase 2: Verifica iniziale 
story_prompt = PromptTemplate.from_template("""
Based on these ideas, create a brief synopsis of a fantasy story in English (300 words):
{ideas}

It must include:
1. Introduction of the setting and unusual protagonist
2. Extraordinary event that disrupts the balance
3. Development with mysteries and alliances
4. Complex antagonist
5. Final twist 
""")

story_chain = story_prompt | creative_llm
print("📖 Generating synopsis...")
story_synopsis = story_chain.invoke({"ideas": story_ideas})
print("✅ Synopsis generated.")

# Fase 3: Verifica qualità
verification_prompt = PromptTemplate.from_template("""
Analyze this synopsis and verify:
1. Consistency with the initial requirements
2. Presence of all required elements
3. Potential of the plot
4. Originality of the idea

Synopsis:
{story}

Provide a detailed report with strengths and improvements:
""")

verification_chain = verification_prompt | quality_llm
print("🔍 Generating verification report...")
verification_report = verification_chain.invoke({"story": story_synopsis})
print("✅ Verification report generated.")

# Fase 4: Controllo finale
final_check_prompt = PromptTemplate.from_template("""
Does the following synopsis meet all these requirements? (Answer ONLY with YES/NO)
- Original setting
- Unusual protagonist 
- Initial extraordinary event
- Complex antagonist
- Final twist

Synopsis:
{story}
Answer:""")

final_check_chain = final_check_prompt | verifier_llm
print("✅ Performing final check...")
approval = final_check_chain.invoke({"story": story_synopsis})

is_approved = "yes" in approval.lower()
print("✅ Final check complete.")
print("APPROVED" if is_approved else "NOT APPROVED")

# Se la storia è approvata, procediamo con la strutturazione in capitoli
if is_approved:
    # Fase 5: Strutturazione in capitoli
    structure_prompt = PromptTemplate.from_template("""
    Create a detailed structure for a fantasy book with 5-7 chapters based on this synopsis.
    
    For each chapter, provide:
    1. An engaging title
    2. A brief synopsis (3-4 sentences)
    3. Key events that must occur in the chapter
    4. Characters involved
    
    Start with a general title for the book.
    
    Synopsis:
    {story}
    
    Format the response like this:
    TITLE: [Book Title]
    
    CHAPTER 1: [Chapter Title]
    SYNOPSIS: [Brief chapter synopsis]
    KEY EVENTS: [List of key events]
    CHARACTERS: [List of characters involved]
    
    CHAPTER 2: ...
    """)
    
    structure_chain = structure_prompt | structure_llm
    print("📚 Generating book structure...")
    book_structure = structure_chain.invoke({"story": story_synopsis})
    print("✅ Book structure generated.")
    
    # Estrai il titolo del libro
    book_title_match = re.search(r"TITLE:\s*(.+?)(?:\n|$)", book_structure)
    book_title = "Fantasy_Book"
    if book_title_match:
        book_title = book_title_match.group(1).strip()
        book_title = re.sub(r'[\\/*?:"<>|]', "_", book_title)  # Sanitizza nome file
    
    # Crea directory per il libro
    book_dir = os.path.join("generated", book_title)
    os.makedirs(book_dir, exist_ok=True)
    
    # Salva la struttura del libro
    with open(os.path.join(book_dir, "structure.md"), "w", encoding="utf-8") as f:
        f.write(book_structure)
    print(f"💾 Book structure saved to {os.path.join(book_dir, 'structure.md')}")
    
    # Estrai capitoli dalla struttura
    chapter_pattern = r"CHAPTER (\d+): ([^\n]+)\nSYNOPSIS: ([^\n]+(?:\n[^\n]+)*?)(?=\nKEY EVENTS:|\n\nCHAPTER|\Z)"
    chapters = re.findall(chapter_pattern, book_structure, re.DOTALL)
    
   # Fase 6: Generazione e verifica dei capitoli
    for chapter_num, chapter_title, chapter_synopsis in chapters:
        print(f"\n🖋️ Generating Chapter {chapter_num}: {chapter_title}")

        chapter_approved = False
        max_attempts = 3
        attempt = 0

        while not chapter_approved and attempt < max_attempts:
            attempt += 1
            print(f"  Attempt {attempt}/{max_attempts}")

            # Generazione del capitolo (Draft)
            chapter_prompt = PromptTemplate.from_template("""
            DRAFT: Write Chapter {chapter_num}: {chapter_title} for the fantasy book.

            This chapter must follow this synopsis: {chapter_synopsis}

            The chapter must be consistent with the overall story and previous chapters.
            Write in English, with rich descriptions, engaging dialogues, and emotional depth.
            The chapter should be about 500-700 words.

            Write only the content of the chapter, without including the chapter number or title.
            """)

            chapter_chain = chapter_prompt | chapter_llm
            print("  ✍️ Generating chapter draft...")
            chapter_content_draft = chapter_chain.invoke({
                "chapter_num": chapter_num,
                "chapter_title": chapter_title,
                "chapter_synopsis": chapter_synopsis
            })
            print("  ✅ Chapter draft generated.")

            # Verifica del capitolo (Draft)
            chapter_verification_prompt = PromptTemplate.from_template("""
            Verify if this chapter draft is consistent with the synopsis and overall story.

            Chapter Number: {chapter_num}
            Chapter Title: {chapter_title}
            Chapter Synopsis: {chapter_synopsis}

            Chapter Content:
            {chapter_content}

            Respond ONLY with YES or NO, followed by a brief explanation:
            """)

            chapter_verification_chain = chapter_verification_prompt | chapter_verifier_llm
            print("  🔍 Verifying chapter draft...")
            chapter_verification = chapter_verification_chain.invoke({
                "chapter_num": chapter_num,
                "chapter_title": chapter_title,
                "chapter_synopsis": chapter_synopsis,
                "chapter_content": chapter_content_draft
            })
            print("  ✅ Chapter draft verified.")

            print(f"  Verification result: {chapter_verification}")

            # Controlla se il capitolo è approvato
            chapter_approved = "yes" in chapter_verification.lower()

            if chapter_approved:
                # Generazione del capitolo (Final)
                chapter_prompt_final = PromptTemplate.from_template("""
                FINAL: Write Chapter {chapter_num}: {chapter_title} for the fantasy book.

                This chapter must follow this synopsis: {chapter_synopsis}

                This chapter must be consistent with the overall story and previous chapters.
                Write in English, with rich descriptions, engaging dialogues, and emotional depth.
                The chapter should be about 1500-2000 words.

                Write only the content of the chapter, without including the chapter number or title.
                Take inspiration from the following draft: {chapter_content_draft}
                """)

                chapter_chain_final = chapter_prompt_final | chapter_llm
                print("  ✍️ Generating final chapter content...")
                chapter_content = chapter_chain_final.invoke({
                    "chapter_num": chapter_num,
                    "chapter_title": chapter_title,
                    "chapter_synopsis": chapter_synopsis,
                    "chapter_content_draft": chapter_content_draft
                })
                print("  ✅ Final chapter content generated.")
                # Salva il capitolo approvato
                chapter_filename = f"{chapter_num}.md"
                with open(os.path.join(book_dir, chapter_filename), "w", encoding="utf-8") as f:
                    f.write(f"# {chapter_title}\n\n{chapter_content}")
                print(f"  ✅ Chapter {chapter_num} approved and saved")
            else:
                print(f"  ❌ Chapter {chapter_num} rejected. Regenerating...")

        if not chapter_approved:
            print(f"  ⚠️ Unable to generate an approved version of Chapter {chapter_num} after {max_attempts} attempts")
    
    print(f"\n📕 Book generation completed! Files saved in {book_dir}")
else:
    print("Book generation cancelled because the initial synopsis was not approved.")
