from subprocess import Popen, PIPE

def convert_file(file_path, write_path):
    # LibreOffice doesn't take STDIN
    args = ["lowriter", "--convert-to", "pdf", "--outdir", write_path,
            file_path]
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
    # Testing
    print(convert_file("examples/cube wallpaper.png"))


