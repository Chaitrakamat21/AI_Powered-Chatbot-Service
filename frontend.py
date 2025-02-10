from flask import Flask, render_template_string, jsonify, request
import subprocess
import os

app = Flask(__name__)

# Directory of AI Tools
TOOLS_DIRECTORY = r"C:\Users\Chaitra Kamat\Documents\A.FINAL YEAR PROJECT"

# List of tools with real image links and descriptions
TOOLS = {
    "text_to_ppt": ["text_to_ppt.py", "https://img.icons8.com/clouds/200/000000/ms-powerpoint.png", "Convert plain text into engaging PowerPoint presentations automatically."],
    "blog_creator": ["blog_creater.py", "https://img.icons8.com/color/200/000000/blog.png", "Generate high-quality blog posts tailored to your topics in seconds."],
    "chatbot": ["chatbot.py", "https://img.icons8.com/color/200/000000/chat.png", "Build and deploy intelligent chatbots to answer queries 24/7."],
    "email_generator": ["email_generator.py", "https://img.icons8.com/fluency/200/000000/new-post.png", "Create professional emails instantly with AI suggestions and templates."],
    "Slice title generator": ["image_to_text.py", "https://img.icons8.com/dusk/200/000000/image-file.png", "Extract text from images with AI-driven OCR technology."],
    "language_translation": ["Language_Translation.py", "https://th.bing.com/th/id/OIP.RLdkbg-DZUmAO7BnZ460AwHaHa?w=195&h=195&c=7&r=0&o=5&dpr=1.5&pid=1.7", "Translate content seamlessly into multiple languages."],
    "quote_generator": ["quote_generator.py", "https://img.icons8.com/color/200/000000/quote-left.png", "Generate inspirational and motivational quotes at a click."],
    "resume_creator": ["resume_creator.py", "https://img.icons8.com/color/200/000000/resume.png", "Design impressive resumes tailored to your career goals."],
    #"social_media_post_generator": ["social_media_post_generator.py", "https://img.icons8.com/color/200/000000/facebook-like.png", "Create eye-catching social media posts to boost your engagement."],
    "text_to_hashtags": ["text_to_hashtags.py", "https://img.icons8.com/dusk/200/000000/picture.png", "Convert text into creative images with AI-powered tools."]
}

html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Tools Suite</title>
    <style>
        body {
            margin: 0;
            font-family: 'Arial', sans-serif;
            background: #f7f9fc;
            color: #333;
        }
        header {
            background: linear-gradient(90deg, #6A11CB, #2575FC);
            color: white;
            text-align: center;
            padding: 20px;
        }
        nav ul {
            padding: 0;
            list-style: none;
            display: flex;
            justify-content: center;
        }
        nav ul li a {
            color: white;
            text-decoration: none;
            padding: 10px 15px;
            display: block;
        }
        .hero {
            text-align: center;
            padding: 50px 20px;
            background: url('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSx4dL4rB2kPA9G7IczMZ7esjxBI8i9zvpDqg&s') no-repeat center/cover;
            color: white;
        }
        .section {
            padding: 50px 10%;
            text-align: center;
        }
        .section h2 {
            font-size: 2.5rem;
            color: #444;
            margin-bottom: 20px;
        }
        .tools-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 20px;
            justify-items: center;
            margin-top: 20px;
        }
        .tool-card {
            background: white;
            border-radius: 15px;
            box-shadow: 0 8px 15px rgba(0, 0, 0, 0.2);
            padding: 30px;
            text-align: center;
            transition: all 0.3s ease-in-out;
            transform-style: preserve-3d;
            perspective: 1000px;
            background-color: #e0f7fa;
        }
        .tool-card:hover {
            transform: rotateY(15deg) translateY(-10px);
            box-shadow: 0 12px 20px rgba(0, 0, 0, 0.2);
        }
        .tool-card img {
            width: 150px;
            height: 150px;
            margin-bottom: 10px;
        }
        .tool-card h3 {
            font-size: 1.5rem;
            color: #333;
            margin-bottom: 15px;
        }
        .tool-card p {
            color: #777;
            font-size: 1rem;
        }
        button {
            background: #6A11CB;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            transition: background-color 0.3s;
        }
        button:hover {
            background: #2575FC;
        }
        .testimonial, .faq {
            background: #eaf4ff;
            padding: 40px 20px;
            margin: 30px 0;
            text-align: left;
        }
        .testimonial p, .faq p {
            margin: 10px 0;
        }
        footer {
            background: #333;
            color: white;
            padding: 10px;
            text-align: center;
        }
        .rainbow {
            background: radial-gradient(circle, skyblue, lightpurple);
            background-size: 200% 200%;
            animation: bubbleEffect 3s ease-in-out infinite;
            }
            @keyframes bubbleEffect {
                0% {
                    background-position: 0% 0%;
                    }
                    50% {
                        background-position: 100% 100%;
                        }
                        100% {
                            background-position: 0% 0%;
                            }
                            }

        @keyframes rainbow {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        .bot-card {
            background: #fff;
            padding: 20px;
            box-shadow: 0 8px 15px rgba(0, 0, 0, 0.2);
            border-radius: 15px;
            text-align: center;
            transform-style: preserve-3d;
            perspective: 1000px;
            transition: transform 0.3s ease;
            background-color: #f0f4f8;
        }
        .bot-card:hover {
            transform: rotateY(15deg);
            box-shadow: 0 12px 20px rgba(0, 0, 0, 0.2);
        }
        .bot-card img {
            width: 120px;
            height: 120px;
            margin-bottom: 15px;
        }
        .bot-card h4 {
            font-size: 1.2rem;
            margin-bottom: 10px;
            color: #333;
        }
        .bot-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 20px;
            justify-items: center;
        }
    </style>
</head>
<body>
    <header>
        <h1>WELCOME TO CNK's AI POWERED CHATBOT SYSTEM</h1>
        <nav>
            <ul>
                <li><a href="#">Home</a></li>
               <li><a href="http://13.200.6.203:7000/" target="_blank">AI Tools</a></li>

                
            </ul>
        </nav>
    </header>

    <section class="hero">
        <h1>Supercharge Your Workflow with AI</h1>
        <p>Explore tools that automate and simplify your tasks with cutting-edge AI.</p>
    </section>

    <section class="section rainbow">
        <h2>Our Featured AI Tools</h2>
        <div class="tools-grid">
            {% for tool_name, details in tools.items() %}
            <div class="tool-card">
                <img src="{{ details[1] }}" alt="{{ tool_name }}">
                <h3>{{ tool_name.replace("_", " ").title() }}</h3>
                <p>{{ details[2] }}</p>
                <button onclick="runTool('{{ tool_name }}')">Launch Tool</button>
            </div>
            {% endfor %}
        </div>
    </section>

    <section class="section">
        <h2>Our Virtual Bots</h2>
        <div class="bot-grid">
            <div class="bot-card">
                <img src="https://img.icons8.com/fluency/200/000000/chat.png" alt="Chatbot">
                <h4>Chatbot</h4>
                <p>AI-powered virtual assistant that answers queries 24/7.</p>
                <button onclick="runTool('chatbot')">Interact</button>
            </div>
            <div class="bot-card">
                <img src="https://img.icons8.com/fluency/200/000000/email.png" alt="Email Generator">
                <h4>Email Generator</h4>
                <p>Create professional emails instantly with AI suggestions.</p>
                <button onclick="runTool('email_generator')">Generate Email</button>
            </div>
        </div>
    </section>

    <section class="testimonial">
        <h2>What Our Users Say</h2>
        <p>⭐⭐⭐⭐⭐ "These tools have revolutionized how I approach my work. The text-to-PPT tool saved me hours!"</p>
        <p>⭐⭐⭐⭐⭐ "I can't imagine creating resumes manually again. The AI resume creator is a game-changer!"</p>
    </section>

    <section class="faq">
        <h2>Frequently Asked Questions</h2>
        <p><strong>1. Are the tools free to use?</strong> Yes, all tools are free to use and accessible online.</p>
        <p><strong>2. How do I launch a tool?</strong> Simply click on the "Launch Tool" button below each tool card.</p>
        <p><strong>3. Is my data secure?</strong> Absolutely! Your data is handled securely and never shared.</p>
    </section>

    <footer>
        <p>© 2025 AI Tools | Built with CNK❤️</p>
    </footer>

    <script>
        function runTool(toolName) {
            fetch('/run-tool', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ tool: toolName })
            })
            .then(response => response.json())
            .then(data => alert(data.message))
            .catch(error => alert("Error: " + error));
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(html_template, tools=TOOLS)

@app.route('/run-tool', methods=['POST'])
def run_tool():
    data = request.get_json()
    tool_name = data.get("tool")

    if tool_name not in TOOLS:
        return jsonify({"message": "Invalid tool name!"}), 400

    script_path = os.path.join(TOOLS_DIRECTORY, TOOLS[tool_name][0])

    if not os.path.exists(script_path):
        return jsonify({"message": f"Script not found: {script_path}"}), 404

    try:
        subprocess.Popen(['streamlit', 'run', script_path], shell=True)
        return jsonify({"message": f"{tool_name.replace('_', ' ').title()} started successfully!"}), 200
    except Exception as e:
        return jsonify({"message": f"Error running script: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
