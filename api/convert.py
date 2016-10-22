import os
from subprocess import Popen, PIPE, TimeoutExpired

def convert_file(file, filename, UPLOAD_FOLDER):
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    # Fix file naming (see issue #11)
    temp_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(temp_path)
    print("Saved temporary file to", temp_path)

    # LibreOffice doesn't take STDIN
    args = ["lowriter", "--convert-to", "pdf", "--outdir", UPLOAD_FOLDER,
            temp_path]
    p = Popen(args, stdout=PIPE, stderr=PIPE)
    try:
        outs, errs = p.communicate(timeout=10)
        print("convert errs:", errs)
        print("convert outs:", outs)

        if outs:  # Assume successful
            print_path = temp_path.rsplit('.', 1)[0] + ".pdf"
            return print_path
    
    except TimeoutExpired:
        p.kill()
        print("Convert to PDF timed out")

    return None


if __name__ == "__main__":
    # Testing conversion
    from werkzeug.datastructures import FileStorage
    file = FileStorage(stream=open("examples/cube wallpaper.png", 'rb'))
    print(convert_file(file, "cube_wallpaper.png", "/tmp/print/"))
