# Custom UI Tutorial App

## Getting Started

1. Follow the instructions for installing the
   [Airavata Django Portal](https://github.com/apache/airavata-django-portal)
2. With the Airavata Django Portal virtual environment activated, clone this
   repo and install it into the portal's virtual environment

   ```
   cd custom_ui_tutorial_app
   pip install -e .
   ```

3. Start (or restart) the Django Portal server.
4. Create an Application on Zenodo.
5. Set `ZENODO_CLIENT_ID` and `ZENODO_SECRET` environment variables. (`.env` is also supported)
