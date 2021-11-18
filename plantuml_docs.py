import hashlib
import logging
import os
import re

logger = logging.getLogger(__name__)

try:
    import plantuml
except ImportError:
    plantuml = None

_PLANTUML_RE = re.compile("(@startuml.*?@enduml)", re.MULTILINE|re.DOTALL)
FLASK_SWAGGER_PLANTUML_SERVER = 'FLASK_SWAGGER_PLANTUML_SERVER'
FLASK_SWAGGER_PLANTUML_FOLDER = 'FLASK_SWAGGER_PLANTUML_FOLDER'

def sub(string, match, replacement):
    return string[:match.start()] + replacement + string[match.end():]

def generate_plantuml(docstring, app):
    """
    Generate PlantUML diagrams from the given docstring.

    If the plantuml Python package is not installed, the docstring is returned
    unaltered.  Otherwise, it performs the following steps:
    * Looks for any `@startuml...@enduml` pairs.
    * When it finds one, extracts the diagram text and sends it to a PlantUML
      server.  The default is the public server, but this can be configured by
      setting the `FLASK_SWAGGER_PLANTUML_SERVER` in the flask app config.
    * The image returned from the server is placed into the application's static
      files folder.  The location of the static folder is determined from the
      `app` object.  The subfolder defaults to `uml` but can be configured by
      setting the `FLASK_SWAGGER_PLANTUML_FOLDER` in the flask app config.
    * The original diagram text is replaced with a markdown link to the generated
      image.
    """
    if not plantuml:
        logger.info("PlantUML not installed; not generating diagrams")
        return docstring

    url=app.config.get(FLASK_SWAGGER_PLANTUML_SERVER, 'http://www.plantuml.com/plantuml/img/')
    logger.info("User PlantUML server %s", url)
    server = plantuml.PlantUML(url=url)

    subfolder = app.config.get(FLASK_SWAGGER_PLANTUML_FOLDER, 'uml')
    folder = os.path.join(app.static_folder, subfolder)
    if not os.path.exists(folder):
        os.mkdir(folder)
    logger.info("Outputting diagrams to %s", folder)

    while True:
        match = _PLANTUML_RE.search(docstring)
        if not match:
            break
        uml = match.group(1)
        # The same UML data will produce the same filename
        filename = hashlib.sha256(uml.encode('utf-8')).hexdigest() + '.png'
        output_file = os.path.join(folder, filename)
        try:
            image_data = server.processes(uml)
            with open(output_file, 'wb') as file:
                file.write(image_data)
            docstring = sub(docstring, match, f'![{filename}]({app.static_url_path}/{subfolder}/{filename})')
        except plantuml.PlantUMLConnectionError as e:
            docstring = sub(docstring, match, f"Failed to connect to the PlantUML server: {e}")
        except plantuml.PlantUMLHTTPError as e:
            docstring = sub(docstring, match, f"HTTP error while connection to the PlantUML server: {e}")
        except plantuml.PlantUMLError as e:
            docstring = sub(docstring, match, f"PlantUML error: {e}")

    return docstring


