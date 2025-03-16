# Optimized and structured prompts for Fantasy Book Generation using LLM agents.

# ✅ **Summary Table of Constants**
# 
# | Constant Name                      | Description                                      |
# |------------------------------------|--------------------------------------------------|
# | `IDEA_GENERATION_PROMPT`           | Generates five detailed fantasy story ideas      |
# | `STORY_SYNOPSIS_PROMPT`            | Creates a cohesive 300-word story synopsis       |
# | `QUALITY_VERIFICATION_PROMPT`      | Structured quality assessment of synopsis        |
# | `FINAL_APPROVAL_CHECK_PROMPT`      | YES/NO check against core synopsis criteria      |
# | `BOOK_STRUCTURE_PROMPT`            | Detailed chapter-by-chapter book structure       |
# | `CHAPTER_DRAFT_PROMPT`             | Generates initial draft content for chapters     |
# | `CHAPTER_VERIFICATION_PROMPT`      | Verifies draft alignment with synopsis           |
# | `FINAL_CHAPTER_GENERATION_PROMPT`  | Produces polished final version of chapters      |

# Idea Generation Prompt
IDEA_GENERATION_PROMPT = """
### Instruction ###
You are an expert fantasy author. Generate exactly 5 original and engaging fantasy story ideas based on the following detailed scenario:

### Theme:
{theme}

For each idea, clearly specify:
- A distinct, vividly described setting.
- 2-3 unique magical creatures inhabiting the world.
- Rich cultural traits of the inhabitants.
- A compelling triggering event that disrupts the world's balance.
- A complex antagonist with nuanced motivations.

After listing the five ideas, provide a concise one-sentence summary for each idea clearly highlighting its unique appeal.

Format your response clearly using numbered lists for each idea and summaries.
"""

# Story Synopsis Generation Prompt
STORY_SYNOPSIS_PROMPT = """
Based on the following five fantasy story ideas:

{ideas}

Compose a detailed and engaging synopsis (approximately 300 words) for a fantasy story that includes:

1. Clear introduction of an original setting and an unusual protagonist.
2. A vividly described extraordinary event disrupting the world's balance.
3. Engaging plot developments featuring intriguing mysteries and unlikely alliances.
4. A well-developed antagonist with complex motivations.
5. A thought-provoking final twist that challenges readers' perceptions of magic and destiny.

Ensure clarity, coherence, and narrative tension throughout your synopsis.
"""

# Quality Verification Prompt
QUALITY_VERIFICATION_PROMPT = """
Analyze this fantasy story synopsis carefully and provide a structured quality assessment covering:

1. Consistency: Does it align clearly with initial requirements?
2. Completeness: Are all required elements (setting, protagonist, event, antagonist, twist) explicitly included?
3. Plot Potential: Evaluate narrative depth, character complexity, and reader engagement potential.
4. Originality: Assess uniqueness in setting, characters, and plot elements.

Provide your analysis in two clear sections:
- Strengths: List specific aspects done exceptionally well.
- Improvements: Suggest concrete ways to enhance clarity, originality, or narrative impact.

Synopsis:
{story}
"""

# Final Approval Check Prompt
FINAL_APPROVAL_CHECK_PROMPT = """
Based solely on the following criteria, does this synopsis meet ALL listed requirements?

Requirements checklist:
- ✅ Original and vividly described setting
- ✅ Unusual protagonist clearly introduced
- ✅ Clearly defined extraordinary triggering event
- ✅ Complex antagonist with nuanced motivations
- ✅ Thought-provoking final twist

Synopsis:
{story}

Respond ONLY with "YES" or "NO".
"""

# Book Structure Generation Prompt
BOOK_STRUCTURE_PROMPT = """
You are tasked with creating a detailed chapter-by-chapter structure for a fantasy novel based on the provided synopsis.

Your response must strictly follow this format:

TITLE: [Creative Book Title]

CHAPTER 1: [Engaging Chapter Title]

SYNOPSIS: [Brief chapter synopsis (3-4 sentences)]

KEY EVENTS:
- [Event 1]
- [Event 2]
- [Event 3]

CHARACTERS:
- [Character Name] (brief description)
- [Character Name] (brief description)

Repeat this structure clearly for each of the 5-7 chapters. Ensure each chapter logically progresses from the previous one, maintaining narrative coherence and tension throughout.

Synopsis:
{story}
"""

# Chapter Draft Generation Prompt
CHAPTER_DRAFT_PROMPT = """
### Instruction ###
Draft Chapter {chapter_num}: {chapter_title} for the fantasy book based precisely on this synopsis:

"{chapter_synopsis}"

Requirements:
- Maintain consistency with the overall story arc and previous chapters.
- Write approximately 500-700 words in English.
- Include vivid descriptions of settings and characters.
- Develop engaging dialogues reflecting character personalities.
- Convey emotional depth effectively.

Write ONLY the chapter content without including chapter numbers or titles.
"""

# Chapter Verification Prompt
CHAPTER_VERIFICATION_PROMPT = """
Evaluate whether this draft aligns accurately with the provided synopsis and maintains consistency with the overall book narrative.

Chapter Number: {chapter_num}
Chapter Title: {chapter_title}

Chapter Synopsis:
{chapter_synopsis}

Chapter Content Draft:
{chapter_content}

Clearly state your evaluation as follows:

YES or NO — followed by a concise explanation (1-2 sentences) justifying your decision.
"""

# Final Chapter Generation Prompt
FINAL_CHAPTER_GENERATION_PROMPT = """
Using the approved draft below as inspiration, write a polished FINAL VERSION of Chapter {chapter_num}: "{chapter_title}" adhering strictly to this synopsis:

{chapter_synopsis}

Requirements:
- Length: Approximately 1500-2000 words in English.
- Maintain consistency with overall plot progression and character development from previous chapters.
- Include rich descriptions enhancing immersion into settings and scenes.
- Craft compelling dialogues reflecting character depth and relationships.
- Ensure emotional resonance throughout the narrative.

Write ONLY the chapter content without including chapter numbers or titles.

Approved Draft for Inspiration:
---
{chapter_content_draft}
---
FINAL CHAPTER CONTENT:
"""
