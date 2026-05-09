from gemini_client import generate

class Writer:

    def write(self, title, context):

        prompt = f'''
اكتب فصل أكاديمي احترافي بعنوان:

{title}

اعتماداً على:

{context}

الشروط:
- أكاديمي
- احترافي
- منظم
- طويل
- عربي فصيح
'''

        return generate(prompt)