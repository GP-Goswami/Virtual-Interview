# # ====== Linux Ubuntu base (Render Compatible) ======
# FROM ubuntu:22.04

# # Avoid interactive prompts
# ENV DEBIAN_FRONTEND=noninteractive

# # ====== Update Linux + Install Python 3.13 ======
# RUN apt-get update && \
#     apt-get upgrade -y && \
#     apt-get install -y wget build-essential libssl-dev zlib1g-dev \
#     libncurses5-dev libbz2-dev libreadline-dev libsqlite3-dev \
#     libffi-dev curl

# # ----- Install Python 3.13 from source -----
# RUN wget https://www.python.org/ftp/python/3.13.0/Python-3.13.0.tgz && \
#     tar -xvf Python-3.13.0.tgz && \
#     cd Python-3.13.0 && \
#     ./configure --enable-optimizations && \
#     make -j 4 && \
#     make altinstall && \
#     ln -s /usr/local/bin/python3.13 /usr/bin/python3 && \
#     ln -s /usr/local/bin/pip3.13 /usr/bin/pip3

# # ====== Set working directory ======
# WORKDIR /app

# # ====== Copy all project files ======
# COPY . .

# # ====== Install requirements ======
# RUN pip3 install --upgrade pip
# RUN pip3 install -r requirements.txt

# # ====== Expose ports ======
# EXPOSE 8501      
# EXPOSE 8000      

# # ====== Start both FRONTEND + BACKEND ======
# CMD ["bash", "-c", "uvicorn main:app --host 0.0.0.0 --port 8000 & streamlit run app.py --server.port 8501 --server.address 0.0.0.0"]

FROM python:3.13-slim

# Install system dependencies for audio (optional)
RUN apt-get update && apt-get install -y \
    portaudio19-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Frontend (Streamlit) will run at port 8501
# Backend (FastAPI) at port 8000
EXPOSE 8000
EXPOSE 8501

# Run FastAPI + Streamlit together
CMD uvicorn main:app --host 0.0.0.0 --port 8000 & streamlit run app.py --server.address 0.0.0.0
