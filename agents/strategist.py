from gemini_client import generate

class Strategist:

    def build_outline(self, topic):

        prompt = f'''
أنشئ خطة بحث أكاديمية بصيغة JSON فقط.

{{
 "chapters":[
   {{"title":"..."}},
   {{"title":"..."}}
 ]
}}

الموضوع:
{topic}
'''

        return generate(prompt)