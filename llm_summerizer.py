import os
from groq import Groq
from dotenv import load_dotenv
load_dotenv()


client = Groq(
        api_key = os.getenv('GROQ_API_KEY')
    )


PROMPTS = {
"English": {
        "general": """You are an expert content summarizer. Create a concise, high-value summary of the video transcript.
STRUCTURE:
📌 Overview (2-3 sentences)
💡 Key Takeaways (5-7 bullet points with concrete details, numbers, or examples)
⚠️ Guidelines: Preserve context, avoid fluff, maintain original tone, output entirely in English.
TRANSCRIPT: {text}""",
        "educational": """You are an expert instructional designer. Create a pedagogically sound summary aligned with Bloom's Taxonomy.
STRUCTURE:
📌 Learning Objectives
📚 Core Knowledge
💡 Conceptual Understanding
🔢 Worked Examples & Applications
⚠️ Common Misconceptions
✅ Practice Guide
OUTPUT entirely in English. Focus on actionable learning. TRANSCRIPT: {text}"""
    },
    "Arabic": {
        "general": """أنت خبير تلخيص محتوى. أنشئ ملخصاً دقيقاً وشاملاً للنص التالي.
الهيكل المطلوب:
📌 نظرة عامة (جملتان إلى 3)
💡 النقاط الأساسية (5-7 نقاط مع تفاصيل محددة وأرقام)
⚠️ التزم باللغة العربية الفصحى، تجنب الحشو، حافظ على التسلسل المنطقي.
النص: {text}""",
        "educational": """أنت مصمم تعليمي خبير. أنشئ تحليلاً تربوياً يتوافق مع تصنيف بلوم.
الهيكل المطلوب:
📌 أهداف التعلم
📚 الفكرة الرئيسية
💡 فهم المفاهيم
🔢 الأمثلة والتطبيقات
⚠️ المفاهيم الخاطئة
✅ دليل التطبيق

اذا كان هناك مصلحات علمية بالانجليزية اكتبها كما هي بالانجليزية.
اشرح الموضوع بالتفصيل واضف صور توضيحية ان امكن حتى يتمكن المستخدم من اخذ فكرة واضحة عن المادة العلمية المتناولة
اكتب باللغة العربية الفصحى فقط، ركّز على النقل المعرفي والتطبيق العملي. النص: {text}"""
    }
}


def summarizer(text:str , lang:str = 'English', mode:str = 'general'):
    prompt_template = PROMPTS.get(lang, PROMPTS['English']).get(mode, PROMPTS['English']['general'])
    prompt = prompt_template.format(text=text)
    
    response = client.chat.completions.create(
        messages=[
        {'role':'user', 'content':prompt}
        ],
        model = 'llama-3.3-70b-versatile',
        temperature=0.1,                      
        top_p=0.9,                     
        stream=True  
    )

    for chunk in response:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content