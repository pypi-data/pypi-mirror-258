import pyximport
# pyximport.install()
pyximport.install(setup_args={"script_args" : ["--verbose"]})
from rolling_cy import rolling_cy