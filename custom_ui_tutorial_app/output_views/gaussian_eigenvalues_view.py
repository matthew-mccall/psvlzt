from airavata_django_portal_sdk import user_storage
from django.conf import settings

import io
import os
import hashlib
import json

import requests

import numpy as np
from cclib.parser import ccopen
from django.conf import settings
from matplotlib.figure import Figure


class GaussianEigenvaluesViewProvider:
    display_type = "link"
    # As a performance optimization, the output view provider can be invoked
    # immediately instead of only after being selected by the user in the
    # portal.  Set to True to invoke immediately. Only use this with simple
    # output view providers that return quickly
    immediate = False
    name = "Gaussian Eigenvalues Upload Output"

    def generate_data(self, request, experiment_output, experiment, output_file=None, **kwargs):

        output_text = io.TextIOWrapper(output_file)
        gaussian = ccopen(output_text)
        data = gaussian.parse()
        data.listify()
        homo_eigenvalues = None
        lumo_eigenvalues = None
        if hasattr(data, 'homos') and hasattr(data, 'moenergies'):
            homos = data.homos[0] + 1
            moenergies = data.moenergies[0]
            if homos > 9 and len(moenergies) >= homos:
                homo_eigenvalues = [data.moenergies[0]
                                    [homos - 1 - i] for i in range(1, 10)]
            if homos + 9 <= len(moenergies):
                lumo_eigenvalues = [data.moenergies[0][homos + i]
                                    for i in range(1, 10)]

        # Create plot
        fig = Figure()
        if homo_eigenvalues and lumo_eigenvalues:
            fig.suptitle("Eigenvalues")
            ax = fig.subplots(2, 1)
            ax[0].plot(range(1, 10), homo_eigenvalues, label='Homo')
            ax[0].set_ylabel('eV')
            ax[0].legend()
            ax[1].plot(range(1, 10), lumo_eigenvalues, label='Lumo')
            ax[1].set_ylabel('eV')
            ax[1].legend()
        else:
            ax = fig.subplots()
            ax.text(0.5, 0.5, "No applicable data", horizontalalignment='center',
                    verticalalignment='center', transform=ax.transAxes)

        # Typical thing is to write an image to an in-memory BytesIO object and
        # then return its bytes
        buffer = io.BytesIO()
        # Example: say you have a figure object, which is an instance of
        # matplotlib's Figure. Then you can write it to the BytesIO object
        fig.savefig(buffer, format='png')
        image_bytes = buffer.getvalue()
        buffer.close()

        m = hashlib.sha256()
        m.update(image_bytes)

        filename = "gaussian_output-{}.png".format(m.hexdigest())
        upload_name = "gateway_{}".format(m.hexdigest())

        ZENODO_PAT = "<insert your access token here>"

        res = requests.get('https://zenodo.org/api/deposit/depositions',
                           params={'q': upload_name,
                                   'access_token': ZENODO_PAT})

        if len(res.json()):
            depID = res.json()[0]['id']
            fileLink = res.json()[0]['links']['files']
            htmlLink = res.json()[0]['links']['html']

            res = requests.get(fileLink,
                               params={'access_token': ZENODO_PAT})

            return {
                'url': htmlLink,
                'label': 'Uploaded Zenodo Ouput'
            }

        headers = {"Content-Type": "application/json"}
        params = {'access_token': ZENODO_PAT}

        print("new upload!")

        res = requests.post('https://zenodo.org/api/deposit/depositions',
                            params=params,
                            json={
                                "metadata": {
                                    "upload_type": "image",
                                    "image_type": "figure",
                                    "title": upload_name,
                                    "creators": [
                                        {
                                            "name": "John Doe"
                                        }
                                    ],
                                    "description": "Automatically uploaded data from the Space Science Virtual Laboratory",
                                    "access_right": "closed"
                                }
                            },
                            # Headers are not necessary here since "requests" automatically
                            # adds "Content-Type: application/json", because we're using
                            # the "json=" keyword argument
                            # headers=headers,
                            headers=headers)

        bucket_url = res.json()["links"]["bucket"]

        res = requests.put(
            "%s/%s" % (bucket_url, filename),
            data=image_bytes,
            params=params,
        )

        return {
            'url': res.json()["links"]["self"],
            'label': 'Uploaded Zenodo Ouput'
        }
