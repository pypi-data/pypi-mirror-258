# https://packaging.python.org/en/latest/guides/distributing-packages-using-setuptools/
# https://packaging.python.org/en/latest/tutorials/packaging-projects/
#
# https://pypi.org/classifiers/
#
# build : python -m build
# upload :
# twine check dist/*



from src.og_log import LOG,LEVEL

LOG.start()
LOG.level(LEVEL.info)
LOG.debug("test")
LOG.info("test")
LOG.warning("test")
LOG.error("test")
LOG.fatal("test")
LOG.temp("test")
