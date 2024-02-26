import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="ego-tea",
  version="0.0.2",
  author="ego",
  author_email="1224632377@qq.com",
  description="ego-tea package",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/ego520/ego-tea.git",
  packages=setuptools.find_packages(),
  classifiers=[
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: MIT License",
  "Operating System :: OS Independent",
  ],
)