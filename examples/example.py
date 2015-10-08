from flask import Flask, jsonify
from flask.views import MethodView
from flask_swagger import swagger

app = Flask(__name__)

class UserAPI(MethodView):

    def get(self, team_id):
        """
        Get a list of users
        First line is the summary
        All following lines until the hyphens is added to description
        ---
        tags:
          - users
        responses:
          200:
            description: Returns a list of users
        """
        return []

    def post(self, team_id):
        """
        Create a new user
        ---
        tags:
          - users
        parameters:
          - in: body
            name: body
            schema:
              id: User
              required:
                - email
                - name
              properties:
                email:
                  type: string
                  description: email for user
                name:
                  type: string
                  description: name for user
        responses:
          201:
            description: User created
        """
        return {}


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin','*')
    response.headers.add('Access-Control-Allow-Headers', "Authorization, Content-Type")
    response.headers.add('Access-Control-Expose-Headers', "Authorization")
    response.headers.add('Access-Control-Allow-Methods', "GET, POST, PUT, DELETE, OPTIONS")
    response.headers.add('Access-Control-Allow-Credentials', "true")
    response.headers.add('Access-Control-Max-Age', 60 * 60 * 24 * 20)
    return response

view = UserAPI.as_view('users')
app.add_url_rule('/users/<int:team_id>', view_func=view, methods=["GET"])
app.add_url_rule('/testing/<int:team_id>', view_func=view)

@app.route("/hacky")
def bla():
    """
    An endpoint that isn't using method view
    ---
    tags:
    - hacks
    responses:
      200:
        description: Hacked some hacks
        schema:
          id: Hack
          properties:
            hack:
              type: string
              description: it's a hack
            subitems:
              type: array
              items:
                schema:
                  id: SubItem
                  properties:
                    bla:
                      type: string
                      description: Bla
                    blu:
                      type: integer
                      description: Blu

    """
    return jsonify(['hacky'])

class PetAPI(MethodView):

    def get(self, pet_id):
        """
        Get a pet.

        This is an example of how to use references and factored out definitions
        ---
        tags:
          - pets
        parameters:
          - in: path
            name: pet_id
        definitions:
          - schema:
              id: Pet
              required:
                - name
                - owner
              properties:
                name:
                  type: string
                  description: the pet's name
                owner:
                  $ref: '#/definitions/Owner'
          - schema:
              id: Owner
              required:
                - name
              properties:
                name:
                  type: string
                  description: the owner's name
        responses:
          200:
            description: Returns the specified pet
            $ref: '#/definitions/Pet'
        """
        return {}

pet_view = PetAPI.as_view('pets')
app.add_url_rule('/pets/<int:pet_id>', view_func=pet_view, methods=["GET"])


@app.route("/")
def hello():
    return "Hello World!"

@app.route("/spec")
def spec():
    return jsonify(swagger(app))

if __name__ == "__main__":
    app.run(debug=True)
