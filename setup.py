import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name="pyNeFrauds",
	version="0.0.5",
	author="Deepam Rai",
	# author_email="",
	description="Python library that integrates with neo4j facilitating in fraud detection using deep learning techniques.",

	# long_description=long_description,
	long_description=long_description,
	long_description_content_type="text/markdown",

	# url="https://github.",
	packages=setuptools.find_packages(),

		 install_requires=["matplotlib","neo4j","numpy","scikit_learn","torch","torch_geometric","pandas"],


	license="MIT",

	# classifiers like program is suitable for python3, just leave as it is.
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
)
