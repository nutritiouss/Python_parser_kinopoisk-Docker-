FROM python:3.9
MAINTAINER VladimirTikhonov
WORKDIR /usr/project
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8050
CMD ["python", "/usr/project/dask.py"]
