import gradio as gr
from .exercitiul1 import find_u
from .exercitiul2 import verify_operation_multiply
from .exercitiul2 import verify_operation_plus
from .exercitiul3 import return_top
from .bonus import return_app_sin
from .bonus import return_app_cos
from .bonus import approximations, sin_S, cos_S

ex1 = gr.Interface(inputs=None, fn=find_u, outputs=gr.Number())

plus = gr.Interface(inputs=None, fn=verify_operation_plus, outputs=gr.Textbox(),
                    title="verify if operation plus is not associative")
multiply = gr.Interface(inputs=[gr.Number(), gr.Number(), gr.Number()], fn=verify_operation_multiply,
                        outputs=gr.Textbox(), title="is (x * y) * z != x * (y * z) ??")

ex2 = gr.TabbedInterface([plus, multiply], ["verify operation plus", "verify operation multiply"])
ex3 = gr.Interface(inputs=None, fn=return_top, outputs=gr.Textbox())

# sin = gr.Interface(fn=approximations,
#                    inputs=[sin_S, gr.Textbox(label="angle")],
#                    outputs=[gr.Textbox(label="Result")],
#                    title="Sinus")
# cos = gr.Interface(fn=approximations, inputs=[cos_S, gr.Textbox(label="angle")], outputs=[gr.Textbox(label="Result")],
#                    title="Cosinus")

def wrapper_approximations(func_name, a):
    func_dict = {"sin_S": sin_S, "cos_S": cos_S}
    func = func_dict[func_name]
    return approximations(func, a)

bonus = gr.Interface(
    fn=wrapper_approximations,
    inputs=[
        gr.Dropdown(choices=["sin", "cos"], label="Function"),
        gr.Slider(minimum=0, maximum=2*3.14159, step=0.01, label="Angle")
    ],
    outputs=gr.Textbox(label="Result")
)

# bonus = gr.TabbedInterface([sin, cos], ["sin", "cos"])

app = gr.TabbedInterface([ex1, ex2, ex3, bonus], ["Ex 1", "Ex 2", "Ex 3", "Bonus"])
