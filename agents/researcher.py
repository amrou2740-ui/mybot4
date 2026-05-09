from gemini_client import generate

class Researcher:

    def collect(self, topic):

        prompt = f'''
اكتب دراسة أكاديمية مفصلة عن:

{topic}

تتضمن:
- مقدمة
- شرح علمي
- أمثلة
- تطبيقات
- نتائج
- خاتمة
- مراجع APA
'''

        return generate(prompt)