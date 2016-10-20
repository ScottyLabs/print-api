from subprocess import Popen, PIPE

def convert_file(file_path):
    # LibreOffice doesn't take STDIN
    args = ["lowriter", "--convert-to", "pdf", file_path]
    p = Popen(args, stdout=PIPE, stderr=PIPE)
    try:
        outs, errs = p.communicate(timeout=10)
        print("errs:", errs)
        print("outs:", outs)

        if outs:  # Assume successful
            return True
    except TimeoutExpired:
        p.kill()
        print("Convert to PDF timed out")

    return False


if __name__ == "__main__":
    print(convert_file("examples/cube wallpaper.png"))


