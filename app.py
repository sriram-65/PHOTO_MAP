from flask import Flask, render_template_string, request
from deepface import DeepFace
import cloudinary
import cloudinary.uploader



app = Flask(__name__)


cloudinary.config(
     cloud_name="dbrmvywb0",
    api_key="799647841433247",
    api_secret="XLtCOYXxRTnjZqwaF2oFnQ0AK7k"
)


index_html = '''
<!DOCTYPE html>
<html>
<head><title>Upload Family Photo</title></head>
<body>
    <h2>Upload a Family Photo</h2>
    <form method="POST" enctype="multipart/form-data">
        <input type="file" name="photo" required>
        <button type="submit">Upload</button>
    </form>
</body>
</html>
'''

mindmap_html = '''
<!DOCTYPE html>
<html>
<head>
    <title>Family Mindmap</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
</head>
<body>
    <h2>Uploaded Family Photo</h2>
    <img src="{{ image_url }}" width="400"><br><br>
    
    <div class="mermaid">
        graph TD;
        {% for person in faces %}
            {{ person.id }}["{{ person.id }} ({{ person.gender }}, {{ person.age }})"]
        {% endfor %}
        {% for i in range(faces|length - 1) %}
            {{ faces[i].id }} --> {{ faces[i+1].id }}
        {% endfor %}
    </div>

    <script>mermaid.initialize({ startOnLoad: true });</script>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        uploaded_file = request.files['photo']
        if uploaded_file.filename != '':
         
            result = cloudinary.uploader.upload(uploaded_file)
            image_url = result['secure_url']

         
            faces_data = DeepFace.extract_faces(img_path=image_url, enforce_detection=False)
            face_info = []

            for i, face in enumerate(faces_data):
                face_info.append({
                    'id': f'Person_{i+1}',
                    'age': face['age'],
                    'gender': face['dominant_gender']
                })

            return render_template_string(mindmap_html, faces=face_info, image_url=image_url)
    return render_template_string(index_html)

if __name__ == '__main__':
    app.run()
