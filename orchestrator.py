import json

from agents.strategist import Strategist
from agents.researcher import Researcher
from agents.writer import Writer
from agents.visualizer import Visualizer
from agents.compiler import Compiler

from database import get_cache, save_cache

async def generate_thesis(topic, progress=None):

    async def update(step, total, text):

        if progress:
            await progress(f"📊 [{step}/{total}] {text}")

    TOTAL = 6

    cache = await get_cache(topic)

    if cache:
        await update(1, TOTAL, "تم جلب البحث من الكاش")
        return cache

    await update(1, TOTAL, "تحليل الموضوع")

    strategist = Strategist()
    outline = strategist.build_outline(topic)

    try:
        outline = json.loads(outline)
    except Exception:

        outline = {
            "chapters": [
                {"title": "المقدمة"},
                {"title": "الدراسة النظرية"},
                {"title": "التحليل"},
                {"title": "الخاتمة"}
            ]
        }

    await update(2, TOTAL, "جمع المعلومات")

    researcher = Researcher()
    research = researcher.collect(topic)

    await update(3, TOTAL, "كتابة الفصول")

    writer = Writer()

    chapters = {}

    total_chapters = len(outline["chapters"])

    for idx, chapter in enumerate(outline["chapters"], start=1):

        title = chapter["title"]

        await update(
            3,
            TOTAL,
            f"كتابة الفصل {idx}/{total_chapters}: {title}"
        )

        chapters[title] = writer.write(
            title,
            research
        )

    await update(4, TOTAL, "إنشاء الرسوم")

    viz = Visualizer()
    charts = viz.create(topic)

    await update(5, TOTAL, "إنشاء PDF")

    compiler = Compiler()

    pdf_path = compiler.compile(
        topic,
        chapters,
        charts
    )

    await save_cache(topic, pdf_path)

    await update(6, TOTAL, "اكتمل البحث ✅")

    return pdf_path