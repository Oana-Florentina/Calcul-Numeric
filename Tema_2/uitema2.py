import numpy as np
import pandas as pd
import gradio as gr
from Tema_2.main import process_matrix


def launch_interface():
    with gr.Blocks() as iface:
        n_input = gr.Number(label="Size of the matrix", value=3, precision=0, interactive=True)

        random_matrix = gr.Checkbox(label="Generate Random Matrix")
        random_vector = gr.Checkbox(label="Generate Random Vector")

        matrix_input = gr.Dataframe(
            label="Matrix Input",
            value=pd.DataFrame(np.zeros((3, 3)), columns=["0", "1", "2"]),
            row_count=3,
            col_count=3,
            type="pandas",
            interactive=True
        )

        vector_input = gr.Dataframe(
            label="Vector Input",
            value=pd.DataFrame(np.zeros((3,)), columns=["0"]),
            row_count=3,
            col_count=1,
            type="pandas",
            interactive=True
        )

        output_matrix = gr.Dataframe(label="Processed Matrix")
        output_vector = gr.Dataframe(label="Processed Vector")
        output_text = gr.Textbox(label="Results")

        def update_matrix_size(n):
            n = int(n)
            new_matrix = pd.DataFrame(np.zeros((n, n)), columns=[str(i) for i in range(n)])
            new_vector = pd.DataFrame(np.zeros((n,)), columns=["0"])
            return new_matrix, new_vector

        n_input.change(update_matrix_size, inputs=[n_input], outputs=[matrix_input, vector_input])

        btn = gr.Button("Submit")
        btn.click(process_matrix, inputs=[random_matrix, random_vector, n_input, matrix_input, vector_input],
                  outputs=[output_matrix, output_vector, output_text])

    # iface.launch()
    return iface


app = launch_interface()
