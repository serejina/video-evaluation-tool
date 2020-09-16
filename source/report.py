"""
Module contains functions to create reports
"""
from jinja2 import Template

# FIXME: hardcode path
_template_name = "./source/templates/base_template.html"


def _read_template():
    """
    Opens template file and returns Template object
    :return:    Template object
    """
    with open(_template_name, "r") as file:
        return Template(file.read())


def create_report(report_name, report_data):
    """
    Creates report with provided data
    :param report_name: the file name of the report
    :param report_data: data to be insert to the report
    :return:     The report file with provided name
    """
    template = _read_template()
    # FIXME: will not render iterable objects except of 'PSNR': [(fr_id, psnr), ...] and strings
    # FIXME: total_videos = number of test cases and metrics as [{test_case_id: {max: <max>, min: <min>, ...}}]
    output = template.render(total_videos=report_data["total_videos"], metrics=report_data["metrics"])
    with open(report_name, "w") as file:
        file.write(output)
