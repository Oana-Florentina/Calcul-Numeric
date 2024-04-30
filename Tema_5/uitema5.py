import numpy as np
import pandas as pd
import gradio as gr
import copy
import scipy.linalg as cholesky

from .bonus import calculate_A_final_bonus, calculate_eigenvalues, return_matrix_from_vector, jacobi2, \
    calculate_p_q_bonus, print_matrix_from_vector
from .exercitiul1 import generate_symmetric_matrix, jacobi, matrix_norm
from .exercitiul2 import generate_positive_definite_matrix, is_positive_definite, process_this
from .exercitiul3 import calculate_singular_values, calculate_rank, calculate_condition_number, \
    calculate_moore_penrose_pseudoinverse, calculate_least_squares_pseudoinverse, calculate_norm


def launch_interface():
    with gr.Blocks() as iface:
        with gr.Tabs():
            with gr.TabItem("Ex 1"):
                matrix_examples = gr.Dropdown(
                    label="Matrix Examples",
                    choices=["Example 1", "Example 2", "Example 3"],
                    value=None,
                    allow_custom_value=False,
                    interactive=True
                )



                random_matrix = gr.Checkbox(label="Generate Random Matrix")


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






                btn = gr.Button("Submit")

                with gr.Row():
                    output_matrix1 = gr.Dataframe(label="Processed Matrix A")
                    output_matrix2 = gr.Dataframe(label="Processed Matrix U")
                with gr.Row():
                    output_matrix3 = gr.Dataframe(label="Processed Matrix A_final")
                with gr.Row():
                    output_text = gr.Textbox(label="Norm Difference")


                def update_matrix_size(n):
                    n = int(n)
                    new_matrix = pd.DataFrame(np.zeros((n, n)), columns=[str(i) for i in range(n)])
                    new_vector = pd.DataFrame(np.zeros((n,)), columns=["0"])
                    return new_matrix, new_vector

                n_input.change(update_matrix_size, inputs=[n_input], outputs=[matrix_input])

                def populate_matrix(example):
                    if example == "Example 1":
                        matrix = pd.DataFrame([[0, 0, 1], [0, 0, 1], [1, 1, 1]], columns=["0", "1", "2"])
                    elif example == "Example 2":
                        matrix = pd.DataFrame([[2.5, 2, 2], [5, 6, 5], [5, 6, 6.5]], columns=["0", "1", "2"])
                    elif example == "Example 3":
                        matrix = pd.DataFrame([[3, 1, 4], [2, 5, 1], [6, 3, 2]], columns=["0", "1", "2"])
                    else:
                        matrix = pd.DataFrame(np.zeros((3, 3)), columns=["0", "1", "2"])
                    return matrix

                matrix_examples.change(populate_matrix, inputs=[matrix_examples], outputs=[matrix_input])

                def process_functions(random_matrix, n, matrix_input):
                    if random_matrix:
                        A = generate_symmetric_matrix(n).tolist()
                    else:
                        A = matrix_input.values.tolist()



                    A_init = np.copy(A)
                    A, U = jacobi(A)
                    A_final = np.dot(np.dot(U.T, A_init), U)
                    eigenvalues = np.diag(A)
                    norm_difference = matrix_norm(np.dot(A_init, U) - np.dot(U, np.diag(eigenvalues)))




                    return pd.DataFrame(A, columns=[str(i) for i in range(n)]), pd.DataFrame(U, columns=[str(i) for i in range(n)]), pd.DataFrame(A_final, columns=[str(i) for i in range(n)]), norm_difference

                btn.click(process_functions, inputs=[random_matrix, n_input, matrix_input],

                          outputs=[output_matrix1, output_matrix2, output_matrix3,  output_text])

            with gr.TabItem("Ex 2"):
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
                with gr.Row():
                    output_text = gr.Textbox(label="Results:")
                    output_norm = gr.Textbox(label="Norm:")


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

                def process_ex2(random_matrix, n, matrix_input):
                    if random_matrix:
                        A = generate_positive_definite_matrix(n).tolist()
                    else:
                        A = matrix_input.values.tolist()
                    result, norm  = process_this(A)
                    return result, norm

                btn_2.click(process_ex2, inputs=[random_matrix_2, n_input_2, matrix_input_2],
                            outputs=[output_text, output_norm])

            with gr.TabItem("Ex 3"):
                matrix_examples = gr.Dropdown(
                    label="Matrix Examples",
                    choices=["Example 1", "Example 2", "Example 3"],
                    value=None,
                    allow_custom_value=False,
                    interactive=True
                )



                random_matrix = gr.Checkbox(label="Generate Random Matrix")


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






                btn = gr.Button("Submit")

                with gr.Row():
                    output_text1 = gr.Textbox(label="Valorile singulare ale matricei A:")
                    output_text2 = gr.Textbox(label="Rangul matricei A:")
                    output_text3 = gr.Textbox(label="Numărul de condiționare al matricei A:")
                with gr.Row():
                    output_matrix1 = gr.Dataframe(label="Pseudoinversa Moore-Penrose a matricei A")

                    output_matrix2 = gr.Dataframe(label="Matricea pseudo-inversă în sensul celor mai mici pătrate a matricei A:")
                with gr.Row():
                    output_text4 = gr.Textbox(label="Norma diferenței:")


                def update_matrix_size(n):
                    n = int(n)
                    new_matrix = pd.DataFrame(np.zeros((n, n)), columns=[str(i) for i in range(n)])
                    new_vector = pd.DataFrame(np.zeros((n,)), columns=["0"])
                    return new_matrix, new_vector

                n_input.change(update_matrix_size, inputs=[n_input], outputs=[matrix_input])

                def populate_matrix(example):
                    if example == "Example 1":
                        matrix = pd.DataFrame([[0, 0, 1], [0, 0, 1], [1, 1, 1]], columns=["0", "1", "2"])
                    elif example == "Example 2":
                        matrix = pd.DataFrame([[2.5, 2, 2], [5, 6, 5], [5, 6, 6.5]], columns=["0", "1", "2"])
                    elif example == "Example 3":
                        matrix = pd.DataFrame([[3, 1, 4], [2, 5, 1], [6, 3, 2]], columns=["0", "1", "2"])
                    else:
                        matrix = pd.DataFrame(np.zeros((3, 3)), columns=["0", "1", "2"])
                    return matrix

                matrix_examples.change(populate_matrix, inputs=[matrix_examples], outputs=[matrix_input])

                def process_function3(random_matrix, n, matrix_input):
                    if random_matrix:
                        A = generate_symmetric_matrix(n)
                    else:
                        A = matrix_input.values.tolist()

                    singular_values = calculate_singular_values(A)
                    rank_A = calculate_rank(A)
                    condition_number = calculate_condition_number(A)
                    pseudo_inverse_moore_penrose = calculate_moore_penrose_pseudoinverse(A)
                    pseudo_inverse_least_squares = calculate_least_squares_pseudoinverse(A)
                    norm_difference = calculate_norm(pseudo_inverse_moore_penrose, pseudo_inverse_least_squares)

                    return singular_values, rank_A, condition_number, pd.DataFrame(pseudo_inverse_moore_penrose, columns=[str(i) for i in range(n)]), pd.DataFrame(pseudo_inverse_least_squares, columns=[str(i) for i in range(n)]), norm_difference
                btn.click(process_function3, inputs=[random_matrix, n_input, matrix_input],

                          outputs=[output_text1, output_text2, output_text3, output_matrix1, output_matrix2, output_text4])

            with gr.TabItem("Bonus"):


                vector_examples = gr.Dropdown(
                    label="Vector Examples",
                    choices=["Example 1", "Example 2", "Example 3"],
                    value=None,
                    allow_custom_value=False,
                    interactive=True
                )


                random_vector = gr.Checkbox(label="Generate Random Vector")

                n_input = gr.Number(label="Size of the matrix", value=3, precision=0, interactive=True)

                with gr.Row():

                    vector_input = gr.Dataframe(
                        label="Vector Input",
                        value=pd.DataFrame(np.zeros((3,)), columns=["0"]),
                        row_count=3,
                        col_count=1,
                        type="pandas",
                        interactive=True
                    )

                btn = gr.Button("Submit")

                with gr.Row():
                    output_matrix1 = gr.Dataframe(label="A:")
                    output_matrix2 = gr.Dataframe(label="U:")
                    output_matrix3 = gr.Dataframe(label="A_final:")
                with gr.Row():
                    output_text4 = gr.Textbox(label="Norma diferenței:")


                def populate_vector(example):
                    if example == "Example 1":
                        vector = pd.DataFrame([1, 1, 1, 2, 2, 2], columns=["0"])
                    elif example == "Example 2":
                        vector = pd.DataFrame([0, 0, 0, 1, 1, 1], columns=["0"])
                    elif example == "Example 3":
                        vector = pd.DataFrame([0, 0, 0, 2, 1, 1], columns=["0"])
                    else:
                        vector = pd.DataFrame(np.zeros((3,)), columns=["0"])
                    return vector

                vector_examples.change(populate_vector, inputs=[vector_examples], outputs=[vector_input])

                def process_function_bonus(random_vector, n, vector_input):
                    if random_vector:
                        A = np.random.randint(-10, 10, size=(n,)).tolist()
                    else:
                        A = vector_input.values.flatten().tolist()


                    A_init = np.copy(A)
                    calculate_p_q_bonus(A)
                    A, U = jacobi2(A)
                    print("resulttttttttttttttttt:")
                    print_matrix_from_vector(A, n)
                    A_matrix = return_matrix_from_vector(A, n)
                    print("nouuuuuuuuuu")
                    print(A_matrix)
                    U_matrix = return_matrix_from_vector(U, n)
                    A_final = calculate_A_final_bonus(A_init, U, n)
                    A_final_matrix = return_matrix_from_vector(A_final,n)
                    norm = calculate_eigenvalues(A_init, U, n)
                    return pd.DataFrame(A_matrix, columns=[str(i) for i in range(n)]), pd.DataFrame(U_matrix, columns=[str(i) for i in range(n)]), pd.DataFrame(A_final_matrix, columns=[str(i) for i in range(n)]), norm
                btn.click(process_function_bonus, inputs=[random_vector, n_input, vector_input],

                          outputs=[output_matrix1, output_matrix2, output_matrix3, output_text4])
            return iface


app = launch_interface()
