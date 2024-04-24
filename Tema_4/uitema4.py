import gradio as gr
from Tema_4.main import process_files_gauss_seidel_norm, process_files_sum_comparison
from Tema_4.main_2 import process_files_gauss_seidel_norm_2, process_files_sum_comparison_2


def launch_ui():
    method = gr.Radio(["Method 1", "Method 2"], label="Choose Method", value="Method 1")
    method2 = gr.Radio(["Method 1", "Method 2"], label="Choose Method", value="Method 1")

    def process_files_gauss_seidel_norm_wrapper(method1, a_file, b_file, operations):
        if method1 == "Method 1":
            return process_files_gauss_seidel_norm(a_file, b_file, operations)
        else:
            return process_files_gauss_seidel_norm_2(a_file, b_file, operations)

    def process_files_sum_comparison_wrapper(method2, a_file, b_file, aplusb_file, operations):
        if method2 == "Method 1":
            return process_files_sum_comparison(a_file, b_file, aplusb_file, operations)
        else:
            return process_files_sum_comparison_2(a_file, b_file, aplusb_file, operations)

    iface_gauss_seidel_norm = gr.Interface(
        fn=process_files_gauss_seidel_norm_wrapper,
        inputs=[
            method,
            gr.File(label="Matrix A File (.txt)"),
            gr.File(label="Vector B File (.txt)"),
            gr.CheckboxGroup(["Gauss-Seidel", "Norm"], label="Operations")
        ],
        outputs=gr.Textbox(label="Results"),
        title="Gauss-Seidel and Norm",
        description="Upload matrix files and select the desired operations.",
        allow_flagging='never'
    )

    iface_sum_comparison = gr.Interface(
        fn=process_files_sum_comparison_wrapper,
        inputs=[
            method2,
            gr.File(label="Matrix A File (.txt)"),
            gr.File(label="Matrix B File (.txt)"),
            gr.File(label="A+B File (.txt)"),
            gr.CheckboxGroup(["Sum of Matrices", "Verify Sum"], label="Operations")
        ],
        outputs=gr.Textbox(label="Results"),
        title="Sum and Comparison",
        description="Upload matrix files and select the desired operations",
        allow_flagging='never'
    )

    iface = gr.TabbedInterface([iface_gauss_seidel_norm, iface_sum_comparison],
                               ["Gauss-Seidel and Norm", "Sum and Comparison"],
                               title="Matrix Operations")

    # iface.launch()
    return iface

app = launch_ui()

# if __name__ == "__main__":
#     launch_ui()
