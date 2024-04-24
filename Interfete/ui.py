import gradio as gr
import sys

sys.path.append("..")

from Tema_1.uitema1 import app as ui1
from Tema_2.uitema2 import app as ui2
from Tema_4.uitema4 import app as ui4

demo = gr.TabbedInterface([ui1, ui2, ui4], ["Homework 1", "Homework 2", "Homework 4"], title="CN Homeworks")
if __name__ == "__main__":
    demo.launch()
