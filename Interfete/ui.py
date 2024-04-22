
import gradio as gr
import sys
sys.path.append("..")

from Tema_1.uitema1 import app as ui1
from Tema_2.uitema2 import app as ui2

demo = gr.TabbedInterface([ui2, ui1], ["Hello World", "Bye World"], title="Demo")
if __name__ == "__main__":
    demo.launch()

