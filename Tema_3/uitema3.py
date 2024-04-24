import gradio as gr
import numpy as np
import random
import math

# Import functions from the provided file
from .exercitiul import calculate_vector, generate_matrix, generate_vector_s, QR, bonus


def Calculate(n):
    A = generate_matrix(n)
    s = generate_vector_s(n)
    b = calculate_vector(A, n, s)

    return A, s, b,


def greet(name):
    greeting = "Hello " + name
    return greeting



with gr.Blocks() as exx:
    gr.Markdown("## Ex 1")
    inp = gr.Number()

    gr.Interface(fn=Calculate,
                 inputs=inp,
                 outputs=[gr.Textbox("A"), gr.Textbox("s"), gr.Textbox("b")],

                 )




app = gr.TabbedInterface([exx])
