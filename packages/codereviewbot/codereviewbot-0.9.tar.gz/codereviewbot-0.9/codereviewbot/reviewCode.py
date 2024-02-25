import openai
import subprocess
import re
from rich.console import Console
from rich.markdown import Markdown
from rich.text import Text
from rich.syntax import Syntax
from rich import print as rich_print
from .read_config import read_config
import os
# Import the required constants from constants.py
from .constants import MODEL_NAME

# Now you can use these constants in your code

# Read configs from init.cfg file


def review_code(file, diff_chunks):
    # Get configuration details from read_config function
    api_key, source_branch_name, local_repo_path = read_config()

# Initialize OpenAI API with your API key
    openai.api_key = api_key
    all_review_comments = f"Review comments for {file}:\n"
    for chunk in diff_chunks:
        # Extract the starting line number from the chunk
        starting_line_number_match = re.search(r'^@@ -\d+,\d+ \+(\d+),', chunk, re.MULTILINE)
        if starting_line_number_match:
            starting_line_number = int(starting_line_number_match.group(1))
        else:
            starting_line_number = "Unknown"  # Fallback if the line number can't be determined

        #prompt =PROMPT_FOR_REVIEW
        prompt = f""""Review the code from line {starting_line_number} in '{file}'.
 Provide only critical feedback: identify security issues, redundancies, potential bugs, and necessary checks.
 Highlight up to 5 major concerns or improvements, focusing on negative aspects without general context assumptions. 
 If no issues, respond with 'No comments'. Limit: 7 comments.        
{chunk}
---
Review Comments:
"""

        response = openai.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": "Developer who will send code for review"},
            ],
            max_tokens=2000,
            n=1,
            temperature=0.3,
        )

        review_comment = response.choices[0].message.content.strip()
        # Include starting line number in the review comments if known
        if starting_line_number != "Unknown":
            all_review_comments += f"Starting from line {starting_line_number}:\n{review_comment}\n\n"
        else:
            all_review_comments += f"{review_comment}\n\n"
            
    return all_review_comments


def split_diff_output_into_chunks(diff_output, token_limit=2000):
    chunks = []
    current_chunk = []
    current_length = 0
    for line in diff_output.splitlines(keepends=True):
        line_length = len(line)
        if current_length + line_length > token_limit:
            chunks.append(''.join(current_chunk))
            current_chunk = [line]
            current_length = line_length
        else:
            current_chunk.append(line)
            current_length += line_length
    if current_chunk:
        chunks.append(''.join(current_chunk))
    return chunks

def highlight_subjects_in_comments(comments):
    """Apply styling to subjects within the comments."""
    highlighted_comments = ""
    for line in comments.split('\n'):
        if line.endswith(":"):  # Assuming subjects end with a colon
            # Apply a specific style to subjects
            highlighted_comments += f"[bold magenta]{line}[/bold magenta]\n"
        else:
            highlighted_comments += line + "\n"
    return highlighted_comments

def display_comments(comments, file, diff_output,repo_path):
    console = Console()
    absolute_path = os.path.join(repo_path, file)
    file_link = f"[link=file:///{absolute_path}]{absolute_path}[/link]"

    subject = "[bold blue]Review comments for "+file_link+":[/bold blue]\n"
    
    # Highlight the code snippet
    syntax = Syntax(diff_output, "python", theme="monokai", line_numbers=False)

    # Prepare the review comments with syntax-highlighted code displayed first
    comments_text = f"{subject}Associated Code Changes:\n"

    # Display the syntax-highlighted code snippet first
    console.print(comments_text, markup=True)
    console.print(syntax)

    # Process and highlight subjects within comments
    highlighted_comments = highlight_subjects_in_comments(comments)

    console.print("\nReview Comments:\n")
    subject = "[bold blue]File: "+file_link+":[/bold blue]\n"
    console.print(subject, markup=True)
    console.print(highlighted_comments, markup=True)  # Display highlighted comments


# Extensions to ignore
IGNORED_EXTENSIONS = [
    '.md',  # Markdown files
    '.txt',  # Text files
    '.json',  # JSON files
    '.vsproj',  # Visual Studio project files
    '.sln',  # Visual Studio Solution files
    '.csproj',  # C# Project files
    '.vbproj',  # Visual Basic Project files
    '.fsproj',  # F# Project files
    '.config',  # Configuration files
    '.xml',  # XML files
    # Add any other project-related or non-code file extensions as needed
]


def filter_ignored_sections(diff_output):
    """Filter out sections enclosed by ai_ignore start and ai_ignore end tags."""
    filtered_output = []
    ignoring = False
    
    start_tag = "ai_ignore start"
    end_tag = "ai_ignore end" 

    for line in diff_output.splitlines(keepends=True):
         if start_tag in line:
            ignoring = True
            continue
         elif end_tag in line:
            ignoring = False
            continue
         if not ignoring:
            filtered_output.append(line)
    return ''.join(filtered_output)

def get_branch_diff_with_source(current_branch, source_branch, repo_path):
    """Get branch diff with source, ignoring specified file extensions."""
    original_cwd = os.getcwd()
    os.chdir(repo_path)
    branch_files_with_diff = {}
    try:
        git_diff_output = subprocess.check_output(
            ["git", "diff", source_branch, current_branch, "--name-only", "--"],
            stderr=subprocess.STDOUT
        ).decode("utf-8").splitlines()
    except subprocess.CalledProcessError as e:
        print(f"Error getting diff between {source_branch} and {current_branch}: {e.output.decode()}")
        return {}
    finally:
        os.chdir(original_cwd)

    for file in git_diff_output:
        file_extension = os.path.splitext(file)[1]
        if file_extension in IGNORED_EXTENSIONS:
            continue  # Skip files with extensions to be ignored
        try:
            os.chdir(repo_path)
            diff_output = subprocess.check_output(
                ["git", "diff", source_branch, current_branch, "--unified=0", "--", file],
                stderr=subprocess.STDOUT
            ).decode("utf-8")
            branch_files_with_diff[file] = diff_output
        except subprocess.CalledProcessError as e:
            print(f"Error getting diff for file {file}: {e.output.decode()}")
            continue  # Skipping files that cause errors
        finally:
            os.chdir(original_cwd)
    return branch_files_with_diff

# Modification in the main function to use the new diff function
def reviewCode(current_branch, source_branch, repo_path):
    """Main function to review code."""
    print('source branch:', source_branch)
    branch_files_with_diff = get_branch_diff_with_source(current_branch, source_branch, repo_path)
    if branch_files_with_diff:
        for file, diff_output in branch_files_with_diff.items():
            diff_output = filter_ignored_sections(diff_output)  # Filter out ignored sections
            diff_chunks = split_diff_output_into_chunks(diff_output)
            all_review_comments = review_code(file, diff_chunks)
            display_comments(all_review_comments, file, diff_output,repo_path)  # Pass the entire diff output for syntax highlighting
    else:
        rich_print("[bold red]No differences found with the source branch.[/bold red]")