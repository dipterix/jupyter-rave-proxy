import setuptools

setuptools.setup(
    name="jupyter-rave-proxy",
    version='0.0.1',
    url="https://github.com/dipterix/jupyter-rave-proxy",
    author="Zhengjia Wang",
    description="Jupyter extension to proxy RAVE",
    packages=setuptools.find_packages(),
	keywords=['RAVE', 'RAVE-iEEG'],
	classifiers=['Framework :: Jupyter'],
    install_requires=[
        'jupyter-server-proxy>=3.2.2'
    ],
    entry_points={
        'jupyter_serverproxy_servers': [
            'rstudio = jupyter_rave_proxy:setup_rave'
        ]
    },
    package_data={
        'jupyter_rave_proxy': ['icons/rstudio.svg'],
    },
)
