import setuptools
setuptools.setup(
     name='blackbox_mpc2',
     version='0.3.0.1',
     author="Ossama Ahmed, Jonas Rothfuss, Ibrahim Ahmed",
     author_email="ibr_alameen@hotmail.com",
     description="Fork of BlackBox MPC - Model Predictive Control with"
                  "sampling based optimizers",
     url="https://github.com/Malborne/blackbox_mpc2.git",
     packages=setuptools.find_packages(),
     install_requires=[
        'tensorflow',
        'tensorflow-probability',
        'gym',
        'numpy',
        'sphinx',
        'matplotlib',
        'sphinx_rtd_theme',
        'sphinxcontrib-bibtex',
      ],
    zip_safe=False
    )