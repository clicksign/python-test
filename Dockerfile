FROM python:3.10
LABEL maintainer="martinslabs@gmail.com"

ENV PYTHONUNBUFFERED=1

# Create the app user and group.
RUN addgroup --system django && adduser --system --group django

ENV HOME=/home/django

WORKDIR $HOME

# Install dependencies
RUN pip install --upgrade pip
COPY requirements.txt $HOME/requirements.txt
RUN pip install -r requirements.txt

# Copy project
COPY . $HOME

# Chown all the files to the app user.
RUN chown -R django:django $HOME

# Change to the app user.
USER django

EXPOSE 8000

# # Run migrations
# RUN python manage.py makemigrations
# RUN python manage.py migrate

# # Load initial data (optional)
# RUN python manage.py loaddata initial_data

# # Create superuser
# RUN python manage.py initadmin

# # Create other users (optional)
# RUN python manage.py initusers

# # Run tests
# RUN python manage.py test


# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "core.wsgi:application"]