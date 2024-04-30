import gradio as gr
import sys
from design import purple_triangle
sys.path.append("..")

from Tema_1.uitema1 import app as ui1
from Tema_2.uitema2 import app as ui2
from Tema_3.uitema3 import app as ui3
from Tema_4.uitema4 import app as ui4
from Tema_6.uitema6 import app as ui6

demo = gr.TabbedInterface([ui1, ui2, ui3, ui4, ui6], ["Homework 1", "Homework 2", "Homework3", "Homework 4", "Homework 6"], title="CN Homeworks", theme=purple_triangle)

if __name__ == "__main__":
    demo.launch()