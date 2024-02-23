"""Execute a shell command with stream output (one line at a time)."""
import subprocess
import sys

from rich.console import Console

console = Console()


# Function to execute shell commands
# https://github.com/zsxkib/Cog-in-Colab-Notebook-Examples/blob/main/SDv2_Cog_in_Colab.ipynb
# def execute_command(cmd):
def run_cmd_stream(cmd):
    process = subprocess.Popen(
        cmd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf8",
    )

    # https://stackoverflow.com/questions/4417546/constantly-print-subprocess-output-while-process-is-running
    # Poll process for new output until finished
    nextline = ""
    while True:
        if process.stdout is not None:  # to please typing/pyright
            nextline = process.stdout.readline()
        if nextline == "" and process.poll() is not None:
            break
        sys.stdout.write(nextline)
        sys.stdout.flush()

    stdout, stderr = process.communicate()
    if process.returncode != 0:
        msg = f"[red bold]Command failed with error: {stderr}"
        console.print(msg)
        raise Exception(msg)

    # noop, stdout buffer is already read hence empty
    # print("====")
    # print(f"{stdout=}")


if __name__ == "__main__":
    run_cmd_stream("ping -n 10 google.com")
