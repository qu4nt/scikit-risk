import os
import snakemd

from .utils import node_title


DEFAULT_PLOT_PALETTE = [
    "#30a2da",
    "#fc4f30",
    "#e5ae38",
    "#6d904f",
    "#8b8b8b",
]

DEFAULT_PLOT_STYLE = "darkgrid"


def skrisk_report(risk_project, file: str, skip: list, histogram_bins: int):
    report = snakemd.new_doc(file)
    for node in risk_project.nodes():
        if node not in skip and risk_project.nodes[node]["node_type"] != "input":
            report.add_header(node_title(node))
            if os.path.exists("./" + node + ".md"):
                node_info = open(node + ".md", "r")
                report.add_paragraph(node_info.read())

            if risk_project.nodes[node]["graphtype"] == "histogram":
                risk_project.generate_histogram(
                    node,
                    title=node_title(node),
                    file_path="./",
                    bins=histogram_bins,
                    legend=True,
                )
            elif risk_project.nodes[node]["graphtype"] == "pie":
                risk_project.generate_piechart(
                    node, title=node_title(node), file_path="./"
                )

            print(risk_project.last_generated_graphic)
            img = [
                snakemd.InlineText(
                    "", url=risk_project.last_generated_graphic, image=True
                )
            ]
            report.add_element(snakemd.Paragraph(img))

            if risk_project.nodes[node]["stats"] is not None:
                report.add_table(
                    ["Stats", "Values"],
                    [[i, j] for i, j in risk_project.nodes[node]["stats"].items()],
                )

            report.add_paragraph(risk_project.nodes[node]["description"])
    report.output_page()
    return report
