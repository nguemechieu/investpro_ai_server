from setuptools import setup, find_packages

setup(
    name="investpro-ai-server",
    version="1.0.0",
    description="FastAPI + TensorFlow server for InvestPro AI predictions",
    author="NOEL NGUEMECHIEU",
    author_email="nguemechieu@live.com",
    url="https://www.github.com/nguemechieu/investpro/ai_server/investpro-ai-server",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
       "requirements.txt"
    ],
    entry_points={
        "console_scripts": [
            "investpro-ai-server=investpro_ai_server:run"
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
