import os
import arabic_reshaper
import matplotlib.pyplot as plt

from bidi.algorithm import get_display

class Visualizer:

    def ar(self, text):

        return get_display(
            arabic_reshaper.reshape(text)
        )

    def create(self, topic):

        path = os.path.join(
            "output",
            "analysis_chart.png"
        )

        x = [1, 2, 3, 4, 5]
        y = [10, 18, 27, 35, 50]

        plt.figure(figsize=(8, 5))

        plt.plot(x, y, marker="o")

        plt.title(
            self.ar(f"تحليل البحث: {topic}")
        )

        plt.xlabel(self.ar("المراحل"))
        plt.ylabel(self.ar("القيم"))

        plt.grid(True)

        plt.savefig(path, bbox_inches="tight")

        plt.close()

        return [path]