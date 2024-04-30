import numpy as np
import pandas as pd
import gradio as gr
import copy

from Tema_7.exercitiul1 import Calculate_Roots, helper_function, helper_bonus, save_solution


def launch_interface():
    with gr.Blocks() as iface:
        with gr.Tabs():
            with gr.TabItem(""):
                vector_examples = gr.Dropdown(
                    label="Coefficients Examples",
                    choices=["Example 1", "Example 2"],
                    value=None,
                    allow_custom_value=False,
                    interactive=True
                )

                random_vector = gr.Checkbox(label="Generate Random Polynom")

                n_input = gr.Number(label="Size of the polynom", value=4, precision=0, interactive=True)

                with gr.Row():
                    vector_input = gr.Dataframe(
                        label="Polynom Input",
                        value=pd.DataFrame(np.zeros((4,)), columns=["0"]),
                        row_count=3,
                        col_count=1,
                        type="pandas",
                        interactive=True
                    )
                bonus_checkbox = gr.Checkbox(label="Bonus")
                with gr.Row():
                    file_input = gr.Textbox(label="File Name")

                btn = gr.Button("Submit")

                with gr.Row():
                   output_text = gr.Textbox(label="Sol with Muller:")
                   output_roots = gr.Textbox(label="Roots:")


                with gr.Row():
                   output_bonus = gr.Textbox(label="Results bonus")

                def populate_vector(example):
                    if example == "Example 1":
                        vector = pd.DataFrame([1, -6, 11, -6], columns=["0"])
                    elif example == "Example 2":
                        vector = pd.DataFrame([8, -38, 49, -22, 3], columns=["0"])
                    else:
                        vector = pd.DataFrame(np.zeros((4,)), columns=["0"])
                    return vector

                vector_examples.change(populate_vector, inputs=[vector_examples], outputs=[vector_input])

                def process_ex(random_vector, n, vector_input, bonus_checkbox, file_input):
                    if random_vector:
                        a = np.random.randint(-100, 100, size=(n,)).tolist()
                    elif vector_examples.value is not None:
                        a = vector_input.values.flatten().tolist()
                    else:
                        a = vector_input.values.flatten().tolist()
                    results = ""
                    R = Calculate_Roots(a, n)
                    sol = helper_function(a, n, R)
                    if file_input:
                        save_solution(sol, file_input)
                    roots = ""
                    roots += "-" + str(R) + ", "+ str(R) + "\n"

                    results += "Sol: " + str(sol) + "\n"
                    bonuss = ""
                    if bonus_checkbox:
                        bonuss += str(helper_bonus(a, R, n)) + "\n"
                    return results, roots, bonuss

                btn.click(process_ex, inputs=[random_vector, n_input, vector_input, bonus_checkbox, file_input],
                            outputs=[output_text, output_roots, output_bonus])


            return iface


app = launch_interface()
