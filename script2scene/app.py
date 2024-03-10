from flask import Flask, render_template, request, send_from_directory, redirect, url_for
import os
import subprocess
import tempfile
import shutil
import time

app = Flask(__name__, template_folder='../templates')

def move_mp4_files(src_dir, dest_dir, exclude_dir):
    for root, dirs, files in os.walk(src_dir):
        if exclude_dir in dirs:
            dirs.remove(exclude_dir)

        for file in files:
            if file.endswith(".mp4") and not root.endswith(exclude_dir):
                src_path = os.path.join(root, file)
                dest_path = os.path.join(dest_dir, 'animation.mp4')
                shutil.move(src_path, dest_path)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Delete the 'videos/' directory before generating the animation
        videos_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../videos')
        if os.path.exists(videos_dir):
            # Remove all files in 'videos/' directory
            for root, dirs, files in os.walk(videos_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    os.remove(file_path)

            # Remove all subdirectories in 'videos/' directory
            for root, dirs, files in os.walk(videos_dir, topdown=False):
                for dir in dirs:
                    dir_path = os.path.join(root, dir)
                    shutil.rmtree(dir_path)

        manim_code = request.form['manim_code']
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.py', dir=tempfile.gettempdir()) as tmp_file:
            tmp_file.write(manim_code)
            tmp_file_path = tmp_file.name

        try:
            # Use manim render command with --media_dir option
            subprocess.run(['manim', 'render', tmp_file_path, '--media_dir', '../videos'], check=True)

            # Move generated MP4 files up to the 'videos/' directory and rename to 'animation.mp4'
            move_mp4_files('../videos', '../videos', 'partial_movie_files')

            # Generate a unique identifier (timestamp in this example)
            some_unique_value = int(time.time())

            return render_template('index.html', some_unique_value=some_unique_value)
        except subprocess.CalledProcessError as e:
            print(f"Manim rendering failed with error: {e.stderr.decode()}")
        finally:
            # Remove the temporary files
            for ext in ['.py', '.mp4']:
                tmp_file = tmp_file_path.replace('.py', ext)
                if os.path.exists(tmp_file):
                    os.remove(tmp_file)

    return render_template('index.html')

@app.route('/videos/<filename>')
def serve_video(filename):
    return send_from_directory(os.path.join(app.root_path, '../videos'), filename)

if __name__ == '__main__':
    app.run(debug=True)
