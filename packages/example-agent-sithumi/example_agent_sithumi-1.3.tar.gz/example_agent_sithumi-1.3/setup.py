from setuptools import setup

setup(
    name="example_agent_sithumi",
    version="1.3",
    description="This will return Sithumi's info.",
    packages=["example_agent_sithumi"],
    zip_safe=False,
    long_description_content_type="text/x-rst",
    install_requires=["pandas", "numpy"]
)