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
6. For OAuth to work, SSL/TLS is required. For the purposes of development, one way this was achieved was by using a reverse proxy. This is reflected in the code as the gateway tries to redirect to itself, but corrections were made to redirect to the proxy. The reverse proxy was achieved by setting up an Apache HTTPd server with a self-signed certificate.  