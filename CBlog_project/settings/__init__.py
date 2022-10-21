#SETTINGS INIT

from .base import *
# you need to set "project_settings = 'prod'" as an environment variable
# in your OS (on which your website is hosted)
if os.environ['project_settings'] == 'prod':
   from .prod import *
else:
   from .dev import *