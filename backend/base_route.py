from flask import current_app as app

@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Backend Dummy Page - Quiz Master</title>
        <!-- Bootstrap CDN -->
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body {
                background-color: #f4f7f9;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
                font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
                position: relative;
                overflow: hidden;
            }
            .background-text {
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                font-size: 200px; /* Increased size for full-page effect */
                font-weight: bold;
                color: rgba(0, 0, 0, 0.08); /* Subtle opacity for watermark effect */
                white-space: nowrap;
                z-index: 0;
                text-align: center;
            }
            .container {
                z-index: 1; /* Ensure it stays above the background text */
                text-align: center;
                padding: 40px;
                background-color: rgba(255, 255, 255, 0.75); /* Increased transparency */
                border-radius: 15px;
                box-shadow: 0px 6px 25px rgba(0, 0, 0, 0.1);
                max-width: 600px;
                width: 90%;
            }
            .container h1 {
                font-size: 32px;
                color: #333333;
            }
            .container p {
                color: #444444;
                font-size: 18px;
                line-height: 1.8;
            }
            .btn-custom {
                background-color: #007bff;
                color: white;
                padding: 12px 25px;
                font-size: 18px;
                border: none;
                border-radius: 8px;
                transition: all 0.3s ease;
            }
            .btn-custom:hover {
                background-color: #0056b3;
                color: #ffffff;
            }
            .footer {
                margin-top: 20px;
                font-size: 14px;
                color: #777777;
            }
        </style>
    </head>
    <body>
        <!-- Background Text -->
        <div class="background-text">Quiz Master</div>

        <!-- Main Container -->
        <div class="container">
            <h1>Welcome to Quiz Master!</h1>
            <p class="lead">Your ultimate platform for interactive and engaging quizzes.</p>
            <p>
                Dive into a world of exciting challenges, test your knowledge, and compete with others. 
                Whether you're here to learn, have fun, or prove your skills, 
                Quiz Master is the perfect place for you!
            </p>
            <a href="http://localhost:8080" target="_blank" class="btn btn-custom">Go to Main Page</a>
            <div class="footer">
                Powered by Flask (Backend) and Vue.js (Frontend)
            </div>
        </div>

        <!-- Bootstrap Bundle with Popper -->
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/js/bootstrap.bundle.min.js"></script>
    </body>
    </html>
    """
