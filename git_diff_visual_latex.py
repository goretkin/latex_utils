#!/usr/bin/env python3
"""Utility for visually diffing latex projects.

Example calls:
git_diff_visual_latex git:HEAD dir:.
git_diff_visual_latex git:HEAD^1 git:HEAD
git_diff_visual_latex git:5f4a4b git:~/Desktop/paper
"""

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


def make_pdf_dir(latex_dir, output_pdf_path):
    with tempfile.TemporaryDirectory() as output_dir:
      run(["latexmk", "-pdf", f"-output-directory={output_dir}", "main.tex"], cwd=latex_dir, check=True)
      # TODO check latex error
      shutil.copy2(os.path.join(output_dir, "main.pdf"), output_pdf_path)
      return None


def make_pdf_git(commit_ref, output_pdf_path):
  with tempfile.TemporaryDirectory() as output_dir:
    do_checkout(output_dir, commit_ref)
    return make_pdf_dir(output_dir, output_pdf_path)


def make_pdf_dispatch(latex_project_spec, output_pdf_path):
  (kind, spec) = latex_project_spec.split(":", 1)
  method_name = f"make_pdf_{kind}"
  method = globals()[method_name]
  return method(spec, output_pdf_path)


if __name__ == "__main__":
  print(__doc__)
  parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
  parser.add_argument("ref_from", help="ref from")
  parser.add_argument("ref_to", help="ref to")
  args = parser.parse_args()

  diff_dir = "pdf_diff"
  for i in [0,1]:
    spec = args.references[i]
    print(f"make {spec}")
    make_pdf_dispatch(args.references[i], os.path.join(diff_dir, f"main__{i}.pdf"))
  print(f"done making pdfs at {diff_dir}")

  diffpdf_sh = os.path.normpath(os.path.join(os.path.realpath(__file__), "../diffpdf.sh"))
  run([diffpdf_sh, "main__0.pdf", "main__1.pdf"], cwd=diff_dir, check=False)