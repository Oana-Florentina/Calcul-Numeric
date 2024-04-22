import gradio as gr


app = gr.Interface(lambda name: "Bye " + name, "text", "text")
