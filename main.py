from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate

# Inizializzazione modelli Ollama per le diverse fasi
creative_llm = Ollama(base_url="http://localhost:11434", model="deepseek-r1:1.5b")
quality_llm = Ollama(base_url="http://localhost:11434", model="gemma3:1b")
verifier_llm = Ollama(base_url="http://localhost:11434", model="gemma3:1b")

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
story_ideas = idea_chain.invoke({
    "theme": "Create a fantasy story set in a completely original world..."
})

print("🎨 Generated ideas:")
print(story_ideas)

# Fase 2: Scrittura storia
story_prompt = PromptTemplate.from_template("""
Write a complete fantasy story in Italian (1500 words) based on these ideas:
{ideas}

Structure:
1. Introduction of the setting and unusual protagonist
2. Extraordinary event that disrupts the balance
3. Development with mysteries and alliances
4. Confrontation with the antagonist
5. Final twist with philosophical reflection
""")

story_chain = story_prompt | creative_llm
final_story = story_chain.invoke({"ideas": story_ideas})

print("\n📖 Generated story:")
print(final_story)

# Fase 3: Verifica qualità
verification_prompt = PromptTemplate.from_template("""
Analyze this fantasy story and verify:
1. Consistency with the initial requirements
2. Presence of all required elements
3. Quality of the plot
4. Character development
5. Effectiveness of the twist

Story:
{story}

Provide a detailed report with strengths and improvements:
""")

verification_chain = verification_prompt | quality_llm
verification_report = verification_chain.invoke({"story": final_story})

print("\n🔍 Verification report:")
print(verification_report)

# Fase 4: Controllo finale
final_check_prompt = PromptTemplate.from_template("""
Does the following story meet all these requirements? (Answer ONLY with YES/NO)
- Original setting
- Unusual protagonist
- Initial extraordinary event
- Complex antagonist
- Final twist

Story:
{story}
Answer:""")

final_check_chain = final_check_prompt | verifier_llm
approval = final_check_chain.invoke({"story": final_story})

print("\n✅ Final check result:")
print("APPROVED" if "yes" in approval.lower() else "NOT APPROVED")
