import argparse
import json
import pkg_resources
from flask_swagger import swagger

parser = argparse.ArgumentParser()
parser.add_argument('app', help='the flask app to swaggerify')
#parser.add_argument('--definitions', help='json definitions file')
parser.add_argument('--template', help='template spec to start with')
parser.add_argument('--out-dir', default=None, help='the directory to output to')
args = parser.parse_args()

def run():
    template = args.template
    app = pkg_resources.EntryPoint.parse("x=%s" % args.app).load(False)
    if template is not None:
        with open(template, 'r') as f:
            spec = swagger(app, template=json.loads(f.read()))
    else:
        spec = swagger(app)
    if args.out_dir is None:
        print json.dumps(spec, indent=4)
    else:
        with open("%s/swagger.json" % args.out_dir, 'w') as f:
            f.write(json.dumps(spec, indent=4))
            f.close()

run()

