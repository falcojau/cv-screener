from fastapi import APIRouter, Form, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse
import resend
import os
import base64

router = APIRouter(prefix="/upload", tags=["upload"])

@router.post("")
async def upload_cv(
  name: str = Form(...),
  last_name: str = Form(...),
  email: str = Form(...),
  phone: str = Form(...),
  cv: UploadFile = File(...)
):
    # Validating the PDF
    if cv.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="The CV must be on PDF format!")
    
    # Reading the content of the CV
    cv_bytes = await cv.read()

    # Checking the size of the file
    if len(cv_bytes) > 5*1024*1024:
        raise HTTPException(status_code=400, detail="The size cannot be bigger than 5MB")
    
    # Resend settings:
    resend.api_key = os.getenv("RESEND_API_KEY")
    hr_email = os.getenv("HR_EMAIL")

    try:
        # 5. Email de confirmación al candidato
        resend.Emails.send({
            "from": "CV Screener <onboarding@resend.dev>",
            "to": hr_email,
            "subject": f"We have received your CV",
            "html": f"""
                <h2>Hi {name}, have received your CV 👋</h2>
                <p>Thanks for sending your resume.</p>
                <p>Our team will review your resume carefully and, if your profile is of interest of any of our vacancies, we will contact you shortly.</p>
                <br>
                <p>Best regards</p>
            """
        })

        # 6.Email to HR:
        resend.Emails.send({
            "from": "CV Screener <onboarding@resend.dev>",
            "to": hr_email,
            "subject": f"New CV received",
            "html": f"""
                <h2>New CV received</h2>
                <ul>
                    <li><strong>Full name:</strong> {name} {last_name}</li>
                    <li><strong>Email:</strong> {email}</li>
                    <li><strong>Phone:</strong> {phone}</li>
                </ul>
                <p>CV attached.</p>
            """,
            "attachments": [
                {
                    "filename": cv.filename,
                    "content": list(cv_bytes)
                }
            ]
        })
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error sending emails: {str(e)}")

    return JSONResponse(content={
        "message": "CV received correctly",
        "candidato": name,
    })
