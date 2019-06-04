#!/usr/bin/env python3

import subprocess
from subprocess import run
import tempfile
import os
import shutil
import argparse

def make_checkout_args(output_dir, commit_ref):
  return ["git", f"--work-tree={output_dir}", "checkout", f"{commit_ref}", "--", "."]


def do_checkout(output_dir, commit_ref):
  return run(make_checkout_args(output_dir, commit_ref), check=True)


def do_latex(latex_dir, output_pdf_path):
    with tempfile.TemporaryDirectory() as output_dir:
      run(["latexmk", "-pdf", f"-output-directory={output_dir}", "main.tex"], cwd=latex_dir, check=True)
      # TODO check latex error
      shutil.copy2(os.path.join(output_dir, "main.pdf"), output_pdf_path)


def make_pdf(commit_ref, output_pdf_path):
  with tempfile.TemporaryDirectory() as output_dir:
    do_checkout(output_dir, commit_ref)
    do_latex(output_dir, output_pdf_path)


def make_pdf_worktree(output_pdf_path):
    latex_dir = os.getcwd()
    do_latex(latex_dir, output_pdf_path)


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("commits", nargs="*")
  args = parser.parse_args()

  diff_dir = "pdf_diff"
  print(diff_dir)
  #make_pdf(args.commits[0], os.path.join(diff_dir, "main__a.pdf"))
  #make_pdf(args.commits[1], os.path.join(diff_dir, "main__b.pdf"))
  print(f"done making pdfs at {diff_dir}")

  diffpdf_sh = os.path.normpath(os.path.join(os.path.realpath(__file__), "../diffpdf.sh"))
  run([diffpdf_sh, "main__a.pdf", "main__b.pdf"], cwd=diff_dir, check=False)