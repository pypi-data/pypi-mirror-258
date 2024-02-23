from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    description = fh.read()

setup(
    name="selenium_web_browser",
    version="v0.0.1",
    author="Eren Mustafa Özdal",
    author_email="eren.060737@gmail.com",
    packages=find_packages(),
    description="Module covering Selenium browser",
    long_description=description,
    long_description_content_type="text/markdown",
    url="https://github.com/erenmustafaozdal/selenium-browser",
    license='MIT',
    python_requires='>=3.11',
    install_requires=["selenium>=4.18.1", "webdriver-manager>=4.0.1"],
)
