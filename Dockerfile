# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.5

EXPOSE 9091

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

# Install pip requirements
ADD requirements.txt .
RUN pip install -r requirements.txt
RUN mkdir /ffhs_nmt2
WORKDIR /ffhs_nmt2
ADD ./ffhs_nmt2 /ffhs_nmt2
RUN python manage.py makemigrations
RUN python manage.py collectstatic --no-input

# During debugging, this entry point will be overridden. For more information, refer to https://aka.ms/vscode-docker-python-debug
# File wsgi.py was not found in subfolder:ffhs-nmt2.0. Please enter the Python path to wsgi file.
CMD ["gunicorn", "--bind", "0.0.0.0:9091", "ffhs_nmt2.wsgi:application"]
