FROM python:3.9

# ติดตั้งไลบรารีระบบพื้นฐานที่ AI สแกนภาพต้องใช้
RUN apt-get update && apt-get install -y libgl1 libglib2.0-0

# สร้าง User สำหรับรันใน Hugging Face
RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"

WORKDIR /app

# ติดตั้งไลบรารี
COPY --chown=user ./requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# นำโค้ด main.py เข้ามา
COPY --chown=user . /app

# คำสั่งเปิด API บนพอร์ต 7860
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
