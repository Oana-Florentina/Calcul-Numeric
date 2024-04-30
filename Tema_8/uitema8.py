import gradio as gr
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import inspect
import random
from Tema_8.main import function_1, function_2, function_3, function_4, analytic_gradient_dictionary, \
    approximate_gradient, algorithm, analytic_gradient
from Tema_8.main import function_1_analytic_gradient, function_2_analytic_gradient, function_3_analytic_gradient, \
    function_4_analytic_gradient

import gradio as gr
import math
import random
import numpy as np


# Funcțiile și dicționarul analytic_gradient_dictionary rămân la fel

def run_algorithm(function, gradient_type, x_min, x_max, y_min, y_max, learning_rate, max_k, max_p, max_product,
                  learning_rate_checkbox):
    x, y = random.uniform(x_min, x_max), random.uniform(y_min, y_max)
    print(f"Initial point: ({x}, {y})")

    if gradient_type == "Approximate Gradient":
        gradient_function = approximate_gradient
    else:
        gradient_function = analytic_gradient

    if learning_rate_checkbox:
        type_ = 2
    else:
        type_ = 1
    return algorithm(function, gradient_function, x, y, learning_rate, max_k, max_p, type_, max_product)


def gradio_interface():
    function_dropdown = gr.Dropdown(label="Select Function", choices=[
        "x ** 2 + y ** 2 - 2 * x - 4 * y - 1", "3 * x ** 2 - 12 * x + 2 * y ** 2 + 16 * y - 10",
        "x ** 2 - 4 * x * y + 5 * y ** 2 - 4 * y + 3", "x * y ** 2 - 2 * x * y ** 2 + 3 * x * y + 4"])

    gradient_radio = gr.Radio(label="Gradient Type", choices=["Approximate Gradient", "Analytic Gradient"])

    x_min = gr.Number(label="x_min", value=-10)
    x_max = gr.Number(label="x_max", value=10)
    y_min = gr.Number(label="y_min", value=-10)
    y_max = gr.Number(label="y_max", value=10)

    learning_rate_checkbox = gr.Checkbox(label="Use Given Learning Rate")
    learning_rate = gr.Number(label="Learning Rate", value=0.001)

    max_k = gr.Number(label="Max Iterations (k)", value=300000)
    max_p = gr.Number(label="Max Learning Rate Adjustments (p)", value=8)
    max_product = gr.Number(label="Max Product of Learning Rate and Norm", value=10 ** 10)

    function_mapping = {
        "x ** 2 + y ** 2 - 2 * x - 4 * y - 1": function_1,
        "3 * x ** 2 - 12 * x + 2 * y ** 2 + 16 * y - 10": function_2,
        "x ** 2 - 4 * x * y + 5 * y ** 2 - 4 * y + 3": function_3,
        "x * y ** 2 - 2 * x * y ** 2 + 3 * x * y + 4": function_4
    }

    output = gr.Textbox(label="Output")

    def wrapper(function, gradient_type, x_min, x_max, y_min, y_max, learning_rate_checkbox, learning_rate, max_k,
                max_p, max_product):
        selected_function = function_mapping[function]
        if not learning_rate_checkbox:
            learning_rate = None
        output_text = run_algorithm(selected_function, gradient_type, x_min, x_max, y_min, y_max, learning_rate, max_k,
                                    max_p,
                                    max_product, learning_rate_checkbox)

        return output_text

    inputs = [function_dropdown, gradient_radio, x_min, x_max, y_min, y_max, learning_rate_checkbox, learning_rate,
              max_k, max_p, max_product]
    outputs = [output]

    interface = gr.Interface(fn=wrapper, inputs=inputs, outputs=outputs, title="Gradient Descent Algorithm")

    return interface


app = gradio_interface()

if __name__ == "__main__":
    app.launch()
