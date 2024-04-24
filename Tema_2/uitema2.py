import numpy as np
import pandas as pd
import gradio as gr
import copy
from Tema_2.main import process_matrix, LU_decomposition, LU_decomposition_2, determinant, verify_euclidian_norm, solve_equation, forward_substitution, backward_substitution


def launch_interface():
    with gr.Blocks() as iface:
        with gr.Tabs():
            with gr.TabItem("LU Decomposition"):
                matrix_examples = gr.Dropdown(
                    label="Matrix Examples",
                    choices=["Example 1", "Example 2", "Example 3"],
                    value=None,
                    allow_custom_value=False,
                    interactive=True
                )

                vector_examples = gr.Dropdown(
                    label="Vector Examples",
                    choices=["Example 1", "Example 2", "Example 3"],
                    value=None,
                    allow_custom_value=False,
                    interactive=True
                )

                random_matrix = gr.Checkbox(label="Generate Random Matrix")
                random_vector = gr.Checkbox(label="Generate Random Vector")

                n_input = gr.Number(label="Size of the matrix", value=3, precision=0, interactive=True)

                with gr.Row():
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

                det_checkbox = gr.Checkbox(label="Compute Determinant")
                norm_checkbox = gr.Checkbox(label="Verify Euclidian Norm")
                solve_checkbox = gr.Checkbox(label="Solve Equation")
                x_y = gr.Checkbox(label="Calculate y and x")

                btn = gr.Button("Submit")

                with gr.Row():
                    output_matrix = gr.Dataframe(label="Processed Matrix")
                    output_vector = gr.Dataframe(label="Processed Vector")

                with gr.Row():
                    output_l = gr.Dataframe(label="L Matrix")
                    output_u = gr.Dataframe(label="U Matrix")
                    output_text = gr.Textbox(label="Results")

                def update_matrix_size(n):
                    n = int(n)
                    new_matrix = pd.DataFrame(np.zeros((n, n)), columns=[str(i) for i in range(n)])
                    new_vector = pd.DataFrame(np.zeros((n,)), columns=["0"])
                    return new_matrix, new_vector

                n_input.change(update_matrix_size, inputs=[n_input], outputs=[matrix_input, vector_input])

                def populate_matrix(example):
                    if example == "Example 1":
                        matrix = pd.DataFrame([[2, 0, 2], [1, 2, 5], [1, 1, 7]], columns=["0", "1", "2"])
                    elif example == "Example 2":
                        matrix = pd.DataFrame([[2.5, 2, 2], [5, 6, 5], [5, 6, 6.5]], columns=["0", "1", "2"])
                    elif example == "Example 3":
                        matrix = pd.DataFrame([[3, 1, 4], [2, 5, 1], [6, 3, 2]], columns=["0", "1", "2"])
                    else:
                        matrix = pd.DataFrame(np.zeros((3, 3)), columns=["0", "1", "2"])
                    return matrix

                matrix_examples.change(populate_matrix, inputs=[matrix_examples], outputs=[matrix_input])

                def populate_vector(example):
                    if example == "Example 1":
                        vector = pd.DataFrame([4, 10, 10], columns=["0"])
                    elif example == "Example 2":
                        vector = pd.DataFrame([2, 2, 2], columns=["0"])
                    elif example == "Example 3":
                        vector = pd.DataFrame([5, 7, 9], columns=["0"])
                    else:
                        vector = pd.DataFrame(np.zeros((3,)), columns=["0"])
                    return vector

                vector_examples.change(populate_vector, inputs=[vector_examples], outputs=[vector_input])

                def process_lu_decomposition(random_matrix, random_vector, n, matrix_input, vector_input, det_checkbox,
                                             norm_checkbox, solve_checkbox, x_y):
                    if random_matrix:
                        A_init = np.random.randint(-10, 10, size=(n, n)).tolist()
                    else:
                        A_init = matrix_input.values.tolist()

                    if random_vector:
                        b = np.random.randint(-10, 10, size=(n,)).tolist()
                    elif vector_examples.value is not None:
                        b = vector_input.values.flatten().tolist()
                    else:
                        b = vector_input.values.flatten().tolist()

                    A = copy.deepcopy(A_init)
                    LU_decomposition(A, A_init, n)

                    L = np.tril(A)
                    U = np.triu(A)
                    np.fill_diagonal(U, 1)

                    results = ""

                    if det_checkbox:
                        det_A = determinant(A)
                        results += f"Determinant of A: {det_A}\n"

                    y = forward_substitution(A, n, b)
                    x = backward_substitution(A, n, y)

                    if x_y:
                        results += f"Y: {y}\nX: {x}\n"

                    if norm_checkbox:
                        norm_result = verify_euclidian_norm(A_init, x, b)
                        results += f"Euclidian Norm Verification:\n{norm_result}\n"

                    if solve_checkbox:
                        solve_result = solve_equation(A_init, b, x)
                        results += f"Solve Equation Comparison:\n{solve_result}\n"

                    return pd.DataFrame(A_init, columns=[str(i) for i in range(n)]), pd.DataFrame(b, columns=[
                        "0"]), pd.DataFrame(L, columns=[str(i) for i in range(n)]), pd.DataFrame(U,
                                                                                                 columns=[str(i) for i
                                                                                                          in range(
                                                                                                         n)]), results

                btn.click(process_lu_decomposition,
                          inputs=[random_matrix, random_vector, n_input, matrix_input, vector_input, det_checkbox,
                                  norm_checkbox, solve_checkbox, x_y],
                          outputs=[output_matrix, output_vector, output_l, output_u, output_text])

            with gr.TabItem("LU Decomposition 2"):
                matrix_examples_2 = gr.Dropdown(
                    label="Matrix Examples",
                    choices=["Example 1", "Example 2", "Example 3"],
                    value=None,
                    allow_custom_value=False,
                    interactive=True
                )
                random_matrix_2 = gr.Checkbox(label="Generate Random Matrix")
                n_input_2 = gr.Number(label="Size of the matrix", value=3, precision=0, interactive=True)

                matrix_input_2 = gr.Dataframe(
                    label="Matrix Input",
                    value=pd.DataFrame(np.zeros((3, 3)), columns=["0", "1", "2"]),
                    row_count=3,
                    col_count=3,
                    type="pandas",
                    interactive=True
                )
                btn_2 = gr.Button("Submit")

                output_matrix_2 = gr.Dataframe(label="Processed Matrix")
                with gr.Row():
                    output_l_vector = gr.Dataframe(label="L Vector")
                    output_u_vector = gr.Dataframe(label="U Vector")

                def update_matrix_size_2(n):
                    n = int(n)
                    new_matrix = pd.DataFrame(np.zeros((n, n)), columns=[str(i) for i in range(n)])
                    return new_matrix

                n_input_2.change(update_matrix_size_2, inputs=[n_input_2], outputs=[matrix_input_2])

                def populate_matrix_2(example):
                    if example == "Example 1":
                        matrix = pd.DataFrame([[2, 0, 2], [1, 2, 5], [1, 1, 7]], columns=["0", "1", "2"])
                    elif example == "Example 2":
                        matrix = pd.DataFrame([[2.5, 2, 2], [5, 6, 5], [5, 6, 6.5]], columns=["0", "1", "2"])
                    elif example == "Example 3":
                        matrix = pd.DataFrame([[3, 1, 4], [2, 5, 1], [6, 3, 2]], columns=["0", "1", "2"])
                    else:
                        matrix = pd.DataFrame(np.zeros((3, 3)), columns=["0", "1", "2"])
                    return matrix

                matrix_examples_2.change(populate_matrix_2, inputs=[matrix_examples_2], outputs=[matrix_input_2])

                def process_lu_decomposition_2(random_matrix, n, matrix_input):
                    if random_matrix:
                        A_init = np.random.randint(-10, 10, size=(n, n)).tolist()
                    else:
                        A_init = matrix_input.values.tolist()

                    L, U = LU_decomposition_2(A_init, n)

                    return pd.DataFrame(A_init, columns=[str(i) for i in range(n)]), pd.DataFrame(L, columns=[
                        "L"]), pd.DataFrame(U, columns=["U"])

                btn_2.click(process_lu_decomposition_2, inputs=[random_matrix_2, n_input_2, matrix_input_2],
                            outputs=[output_matrix_2, output_l_vector, output_u_vector])

            return iface


app = launch_interface()
