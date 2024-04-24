import gradio as gr
import numpy as np
import matplotlib.pyplot as plt
from Tema_6.main import progressive_newton_interpolation, least_squares_method, horner_method, plot_polynomial


def progressive_newton_interpolation_ui(x_list, y_list, x, y_, num_intervals):
    x_list = list(map(float, x_list.split(',')))
    y_list = list(map(float, y_list.split(',')))
    x = float(x)
    y_ = float(y_)

    result = progressive_newton_interpolation(x_list, y_list, x)
    print(x_list, y_list, x, y_, result)
    print(max(x_list), min(x_list))
    x_values = np.linspace(min(x_list), max(x_list), num_intervals)
    y_values = [progressive_newton_interpolation(x_list, y_list, x_el) for x_el in x_values]

    plt.figure()
    plot_polynomial(x_list, y_list, "f(x)", "Function")
    plot_polynomial(x_values, y_values, "L_n(x)", "Progressive Newton interpolation")
    plt.tight_layout()

    return plt.gcf(), f"L_n(x) = {result}", f"|L_x - f(x)| = {abs(result - y_)}"


def least_squares_method_ui(a, b, n, m, x_, function, num_intervals):
    a = float(a)
    b = float(b)
    n = int(n)
    m = int(m)
    x_ = float(x_)

    h = (b - a) / n
    x = [a + i * h for i in range(n + 1)]
    y = [eval(function.replace("x", str(x_val))) for x_val in x]

    c = least_squares_method(n, m, x_, x, y)
    result = horner_method(c, x_)

    x_values = np.linspace(a, b, num_intervals)
    y_values = [eval(function.replace("x", str(x_val))) for x_val in x_values]
    y_approx = [horner_method(c, x_el) for x_el in x_values]

    plt.figure()
    plot_polynomial(x_values, y_values, "f(x)", "Function")
    plot_polynomial(x_values, y_approx, "P(x)", "Least squares method")
    plt.tight_layout()

    difference = sum(abs(horner_method(c, x_el) - eval(function.replace("x", str(x_el)))) for x_el in x)

    return plt.gcf(), f"P(x) = {result}", f"|P(x) - f(x)| = {abs(result - eval(function.replace('x', str(x_))))}", f"Sum of differences = {difference}"


iface = gr.Interface(
    progressive_newton_interpolation_ui,
    [
        gr.Textbox(label="x_list (comma-separated)", value="0, 1, 2, 3, 4, 5"),
        gr.Textbox(label="y_list (comma-separated)", value="50, 47, -2, -121, -310, -545"),
        gr.Number(label="x", value=1.5),
        gr.Number(label="y_", value=30.3125),
        gr.Number(label="Number of intervals", value=5)
    ],
    [
        gr.Plot(label="Plot"),
        gr.Textbox(label="L_n(x)"),
        gr.Textbox(label="|L_x - f(x)|")
    ],
    title="Progressive Newton Interpolation"
)

iface2 = gr.Interface(
    least_squares_method_ui,
    [
        gr.Number(label="a", value=0),
        gr.Number(label="b", value=5),
        gr.Number(label="n", precision=0, value=5),
        gr.Number(label="m", precision=0, value=4),
        gr.Number(label="x_", value=1.5),
        gr.Textbox(label="Function f(x)", value="x ** 4 - 12 * x ** 3 + 30 * x ** 2 + 12"),
        gr.Slider(minimum=1, maximum=1000, step=1, value=10, label="Number of intervals")
    ],
    [
        gr.Plot(label="Plot"),
        gr.Textbox(label="P(x)"),
        gr.Textbox(label="|P(x) - f(x)|"),
        gr.Textbox(label="Sum of differences")
    ],
    title="Least Squares Method"
)

app = gr.TabbedInterface([iface, iface2], ["Progressive Newton Interpolation", "Least Squares Method"])

if __name__ == "__main__":
    app.launch()
