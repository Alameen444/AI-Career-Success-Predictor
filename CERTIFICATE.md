````html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Project Completion Certificate</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Georgia', serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            padding: 20px;
        }
        
        .certificate {
            width: 100%;
            max-width: 900px;
            background: linear-gradient(to bottom, #ffffff 0%, #f5f5f5 100%);
            padding: 60px 80px;
            border: 3px solid #d4af37;
            box-shadow: 0 10px 50px rgba(0, 0, 0, 0.3);
            position: relative;
            text-align: center;
        }
        
        .certificate::before {
            content: "";
            position: absolute;
            top: 20px;
            left: 20px;
            width: 40px;
            height: 40px;
            border-top: 3px solid #d4af37;
            border-left: 3px solid #d4af37;
        }
        
        .certificate::after {
            content: "";
            position: absolute;
            bottom: 20px;
            right: 20px;
            width: 40px;
            height: 40px;
            border-bottom: 3px solid #d4af37;
            border-right: 3px solid #d4af37;
        }
        
        .header {
            margin-bottom: 30px;
        }
        
        .header h1 {
            font-size: 48px;
            color: #667eea;
            font-weight: normal;
            letter-spacing: 3px;
            margin-bottom: 10px;
        }
        
        .header p {
            font-size: 18px;
            color: #764ba2;
            font-style: italic;
            margin-bottom: 20px;
        }
        
        .divider {
            height: 2px;
            background: linear-gradient(to right, transparent, #d4af37, transparent);
            margin: 30px 0;
        }
        
        .content {
            margin: 40px 0;
        }
        
        .content p {
            font-size: 16px;
            color: #333;
            line-height: 1.8;
            margin-bottom: 20px;
        }
        
        .recipient {
            font-size: 32px;
            color: #764ba2;
            font-weight: bold;
            margin: 30px 0;
            text-decoration: underline;
            text-decoration-style: wavy;
            text-decoration-color: #d4af37;
        }
        
        .project-title {
            font-size: 24px;
            color: #667eea;
            font-weight: bold;
            margin: 20px 0;
        }
        
        .highlights {
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
            padding: 20px;
            border-left: 5px solid #667eea;
            margin: 25px 0;
            text-align: left;
            border-radius: 5px;
        }
        
        .highlights h3 {
            color: #667eea;
            margin-bottom: 15px;
            font-size: 18px;
        }
        
        .highlights ul {
            list-style: none;
            margin-left: 20px;
        }
        
        .highlights li {
            color: #333;
            margin: 10px 0;
            font-size: 14px;
        }
        
        .highlights li:before {
            content: "✓ ";
            color: #667eea;
            font-weight: bold;
            margin-right: 10px;
        }
        
        .signature-section {
            display: flex;
            justify-content: space-around;
            margin-top: 60px;
            padding-top: 40px;
            border-top: 2px solid #d4af37;
        }
        
        .signature-box {
            text-align: center;
            flex: 1;
        }
        
        .signature-line {
            border-top: 2px solid #333;
            width: 150px;
            margin: 0 auto 10px;
        }
        
        .signature-name {
            font-weight: bold;
            color: #333;
            font-size: 14px;
        }
        
        .signature-title {
            color: #666;
            font-size: 12px;
            margin-top: 5px;
        }
        
        .date {
            color: #666;
            font-size: 12px;
            margin-top: 5px;
        }
        
        .seal {
            font-size: 60px;
            margin: 20px 0;
            opacity: 0.3;
        }
        
        .footer {
            margin-top: 30px;
            font-size: 12px;
            color: #999;
        }
        
        @media print {
            body {
                background: white;
            }
            .certificate {
                box-shadow: none;
                max-width: 100%;
            }
        }
    </style>
</head>
<body>
    <div class="certificate">
        <div class="header">
            <h1>Certificate of Achievement</h1>
            <p>In Recognition of Exceptional Work</p>
        </div>
        
        <div class="divider"></div>
        
        <div class="content">
            <p>This is to certify that</p>
            
            <div class="recipient">Al Ameen</div>
            
            <p>has successfully completed and delivered</p>
            
            <div class="project-title">🎓 AI Career Success Predictor</div>
            
            <p>A comprehensive Machine Learning project demonstrating expertise in predictive analytics, data science, and full-stack application development.</p>
            
            <div class="highlights">
                <h3>Project Achievements:</h3>
                <ul>
                    <li>Developed an advanced ML model using Random Forest Classifier</li>
                    <li>Engineered placement prediction system with 15+ input parameters</li>
                    <li>Created interactive Streamlit dashboard for data visualization</li>
                    <li>Implemented Placement Readiness Score & Skill Gap Analysis</li>
                    <li>Provided actionable Career Recommendations for students</li>
                    <li>Integrated comprehensive data processing with Pandas & NumPy</li>
                    <li>Demonstrated proficiency in Python, Scikit-Learn, and ML workflows</li>
                </ul>
            </div>
            
            <p><strong>Technologies & Tools:</strong></p>
            <p>Python • Pandas • NumPy • Scikit-Learn • Streamlit • Joblib • Random Forest Algorithm</p>
            
            <p style="margin-top: 40px; font-weight: bold;">This certificate recognizes exceptional dedication to Machine Learning, Data Science, and Software Development.</p>
        </div>
        
        <div class="seal">⭐</div>
        
        <div class="signature-section">
            <div class="signature-box">
                <div class="signature-line"></div>
                <div class="signature-name">Project Owner</div>
                <div class="signature-title">Al Ameen</div>
                <div class="date">July 6, 2026</div>
            </div>
            <div class="signature-box">
                <div class="signature-line"></div>
                <div class="signature-name">Verified By</div>
                <div class="signature-title">GitHub Community</div>
                <div class="date">Certificate ID: ACSP-2026-001</div>
            </div>
        </div>
        
        <div class="footer">
            <p>This certificate is a formal recognition of the completion and quality of the AI Career Success Predictor project.</p>
            <p>🔗 GitHub: https://github.com/Alameen444/AI-Career-Success-Predictor</p>
        </div>
    </div>
</body>
</html>
````
