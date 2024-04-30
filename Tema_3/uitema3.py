import gradio as gr
import numpy as np
import pandas as pd
import gradio as gr
import copy
import random
import math

# Import functions from the provided file
from .exercitiul import calculate_vector, generate_matrix, generate_vector_s, QR, bonus, calculate_norm, solve_system, \
    inverse_with_qr, find_x_qr_with_lib, calculate_second_norm, calculate_third_norm, calculate_svd, \
    generate_positive_definite_matrix


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

                ex1_checkbox = gr.Checkbox(label="Calculate vector b")
                ex2_checkbox = gr.Checkbox(label="Calculate Q R and verify norm")
                ex3_checkbox = gr.Checkbox(label="Calculate X Householder")
                ex4_checkbox = gr.Checkbox(label="Calculate norms")
                ex5_checkbox = gr.Checkbox(label="Calculate inverse with QR and verify norm")
                bonus_checkbox = gr.Checkbox(label="Calculate bonus")


                btn = gr.Button("Submit")

                with gr.Row():

                    output_vector = gr.Dataframe(label="Processed Vector")

                with gr.Row():
                    output_Q = gr.Dataframe(label="Q Matrix")
                    output_R = gr.Dataframe(label="R Matrix")
                    output_text = gr.Textbox(label="Results")

                def update_matrix_size(n):
                    n = int(n)
                    new_matrix = pd.DataFrame(np.zeros((n, n)), columns=[str(i) for i in range(n)])
                    new_vector = pd.DataFrame(np.zeros((n,)), columns=["0"])
                    return new_matrix, new_vector

                n_input.change(update_matrix_size, inputs=[n_input], outputs=[matrix_input, vector_input])

                def populate_matrix(example):
                    if example == "Example 1":
                        matrix = pd.DataFrame([[0, 0, 4], [1, 2, 3], [0, 1, 2]], columns=["0", "1", "2"])
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
                        vector = pd.DataFrame([3, 2, 1], columns=["0"])
                    elif example == "Example 2":
                        vector = pd.DataFrame([2, 2, 2], columns=["0"])
                    elif example == "Example 3":
                        vector = pd.DataFrame([5, 7, 9], columns=["0"])
                    else:
                        vector = pd.DataFrame(np.zeros((3,)), columns=["0"])
                    return vector

                vector_examples.change(populate_vector, inputs=[vector_examples], outputs=[vector_input])

                def process_functions(random_matrix, random_vector, n, matrix_input, vector_input, ex1_checkbox,
                                      ex2_checkbox, ex3_checkbox, ex4_checkbox, ex5_checkbox, bonus_checkbox):

                    if random_matrix:
                        A_init = np.random.randint(-10, 10, size=(n, n)).tolist()
                    elif matrix_examples.value is not None:
                        A_init = matrix_input.values.tolist()
                    else:
                        A_init = matrix_input.values.tolist()

                    if random_vector:
                        s = np.random.randint(-10, 10, size=(n,)).tolist()
                    elif vector_examples.value is not None:
                        s = vector_input.values.flatten().tolist()
                    else:
                        s = vector_input.values.flatten().tolist()


                    A = copy.deepcopy(A_init)
                    A_init2 = np.copy(A_init)
                    b = calculate_vector(A, n, s)
                    results = ""
                    b_init = np.copy(b).tolist()
                    Q, R, b = QR(A, n, b)
                    X_house = solve_system(R, n, np.dot(Q.T, b_init))

                    x_QR = find_x_qr_with_lib(A_init, n, b_init)
                    norm = calculate_norm(x_QR, X_house)
                    norm1 = calculate_second_norm(A_init, X_house, b_init)
                    norm2 = calculate_second_norm(A_init, x_QR, b_init)
                    norm3 = calculate_third_norm(X_house, s)
                    norm4 = calculate_third_norm(x_QR, s)
                    inverse_qr = inverse_with_qr(Q, R)
                    inverse_library = np.linalg.inv(A_init2)
                    difference = np.linalg.norm(inverse_qr - inverse_library)

                    if ex3_checkbox:
                        results += f"X Householder:\n{ pd.DataFrame(X_house, columns=['0']) }\n\n"
                        results += f"x_QR:\n{ pd.DataFrame(x_QR, columns=['0']) }\n\n"
                        results += f"Norma:\n{ norm }\n\n"
                    if ex4_checkbox:
                        results += f"norm between A_init * X_house and b_init:\n{ norm1 }\n\n"
                        results += f"norm between A_init * x_QR and b_init:\n{ norm2 }\n\n"
                        results += f"norm between X_house and s:\n{ norm3 }\n\n"
                        results += f"norm between x_QR and s:\n{ norm4 }\n\n"
                    if ex5_checkbox:
                        results += f"Norma diferenței dintre inversa calculată cu QR și inversa din bibliotecă:\n{ difference }\n\n"
                    if bonus_checkbox:
                        A_bonus = generate_positive_definite_matrix(n)
                        _, singular_values, _ = calculate_svd(A_bonus)

                        results += f"Bonus:\n{ bonus(A_bonus) }\n\n"
                        results += f"Singular values:\n{ singular_values }\n\n"

                    return pd.DataFrame(b, columns=[
                        "0"]), pd.DataFrame(Q, columns=[str(i) for i in range(n)]), pd.DataFrame(R, columns=[str(i) for i in range(n)]), results

                btn.click(process_functions,
                         inputs=[random_matrix, random_vector, n_input, matrix_input, vector_input, ex1_checkbox, ex2_checkbox, ex3_checkbox, ex4_checkbox, ex5_checkbox, bonus_checkbox],
                         outputs= [output_vector, output_Q, output_R, output_text])


            return iface


app = launch_interface()
