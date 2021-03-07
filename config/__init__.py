import hiyapyco

import os

env = os.environ.get('APP_ENV', default="local")

config = hiyapyco.load('{}/config/_base.yaml'.format(os.getcwd()), '{}/config/{}.yaml'.format(os.getcwd(), env))

print(hiyapyco.dump(config))
