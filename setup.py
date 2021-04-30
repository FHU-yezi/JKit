import setuptools

with open("README.md","r",encoding = "utf-8") as file:
    long_description = file.read()

setuptools.setup(
    name="JianshuResearchTools",
    version="0.4.0",
    author="FHU-yezi",
    author_email="yehaowei20060411@qq.com",
    description="科技赋能创作星辰",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/FHU-yezi/JianshuResearchTools",
    packages=["JianshuResearchTools"],
    install_requires=["beautifulsoup4>=4.9.3","requests>=2.25.1"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.0"
)