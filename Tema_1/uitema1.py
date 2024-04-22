import gradio as gr
from .exercitiul1 import find_u
from .exercitiul2 import verify_operation_multiply
from .exercitiul2 import verify_operation_plus
from .exercitiul3 import return_top
from .bonus import return_app_sin
from .bonus import return_app_cos

ex1 = gr.Interface(inputs=None, fn=find_u, outputs=gr.Number())

plus = gr.Interface(inputs=None, fn=verify_operation_plus, outputs=gr.Textbox(), title="verify if operation plus is not associative")
multiply = gr.Interface(inputs=[gr.Number(), gr.Number(), gr.Number()], fn=verify_operation_multiply, outputs=gr.Textbox(), title="is (x * y) * z != x * (y * z) ??")

ex2 = gr.TabbedInterface([plus, multiply], ["verify operation plus", "verify operation multiply"])
ex3 = gr.Interface(inputs=None, fn=return_top, outputs=gr.Textbox())
sin = gr.Interface(inputs=None, fn=return_app_sin, outputs=gr.Text())
cos = gr.Interface(inputs=None, fn=return_app_cos, outputs=gr.Text())
bonus = gr.TabbedInterface([sin, cos], ["sin", "cos"])

app = gr.TabbedInterface([ex1, ex2, ex3, bonus], ["Ex 1", "Ex 2", "Ex 3", "Bonus"])

