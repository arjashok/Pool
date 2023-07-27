"""
    Linter helper script to center headings.
"""

# imports #
import re
import sys


# define functionality #
def center_comments(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    for i in range(len(lines)):
        match = re.match(r'^\s*#\s*-\s*(.*?)\s*-\s*#\s*$', lines[i])
        if match:
            heading = match.group(1)
            padding = (80 - len(heading) - 4) // 2
            centered_heading = f"# {'-' * padding} {heading} {'-' * padding} #\n"
            lines[i] = centered_heading

    with open(filename, 'w') as file:
        file.writelines(lines)


# run as script #
if __name__ == '__main__':
    for filename in sys.argv[1:]:
        center_comments(filename)


"""
    To add:
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v3.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files

  # custom hook for comments centering
  - repo: local
    hooks:
      - id: center-comments
        name: Center Comments
        entry: python center_comments.py
        language: python
        types: [python]

"""

