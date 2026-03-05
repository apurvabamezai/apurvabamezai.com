#!/usr/bin/env python3
"""
Generate PDF CVs from data/cv.yaml using Jinja2 + LaTeX.

Usage:
    python cv-generator/generate.py

Outputs:
    static/files/Bamezai_CV.pdf       (full academic CV)
    static/files/Bamezai_Resume.pdf    (short 1-2 page resume)
"""

import os
import sys
import subprocess
import tempfile
import shutil
import yaml
from jinja2 import Environment, FileSystemLoader

# Paths (relative to project root)
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(ROOT, "data", "cv.yaml")
TEMPLATE_DIR = os.path.join(ROOT, "cv-generator", "templates")
OUTPUT_DIR = os.path.join(ROOT, "static", "files")


def load_data():
    """Load cv.yaml."""
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def render_template(template_name, data):
    """Render a Jinja2 LaTeX template with CV data."""
    env = Environment(
        loader=FileSystemLoader(TEMPLATE_DIR),
        # Use different delimiters to avoid conflict with LaTeX braces
        block_start_string="<%",
        block_end_string="%>",
        variable_start_string="<<",
        variable_end_string=">>",
        comment_start_string="<#",
        comment_end_string="#>",
        autoescape=False,
    )
    template = env.get_template(template_name)
    return template.render(cv=data)


def compile_latex(tex_content, output_name):
    """Compile LaTeX content to PDF."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    with tempfile.TemporaryDirectory() as tmpdir:
        tex_path = os.path.join(tmpdir, "cv.tex")
        with open(tex_path, "w", encoding="utf-8") as f:
            f.write(tex_content)

        # Run pdflatex twice for cross-references
        for _ in range(2):
            result = subprocess.run(
                ["pdflatex", "-interaction=nonstopmode", "-output-directory", tmpdir, tex_path],
                capture_output=True,
                text=True,
            )
            if result.returncode != 0:
                print(f"LaTeX compilation error for {output_name}:")
                print(result.stdout[-2000:] if len(result.stdout) > 2000 else result.stdout)
                sys.exit(1)

        # Copy PDF to output
        pdf_src = os.path.join(tmpdir, "cv.pdf")
        pdf_dst = os.path.join(OUTPUT_DIR, output_name)
        shutil.copy2(pdf_src, pdf_dst)
        print(f"Generated: {pdf_dst}")


def main():
    data = load_data()

    # Full academic CV
    print("Generating full academic CV...")
    tex = render_template("full_cv.tex.j2", data)
    compile_latex(tex, "Bamezai_CV.pdf")

    # Short resume
    print("Generating short resume...")
    tex = render_template("resume.tex.j2", data)
    compile_latex(tex, "Bamezai_Resume.pdf")

    print("Done!")


if __name__ == "__main__":
    main()
