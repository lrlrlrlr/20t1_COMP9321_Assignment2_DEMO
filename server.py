import flask
from flask_restplus import Resource, Api
from main import * # import all the functions from main.py, you may need to fix this line

# 1. init
app = flask.Flask(__name__)
api = Api(app)
data = Data()


# 2. start:
@api.route("/collections")
class Q1nQ3(Resource):
    def post(self):
        # 1. get the user query
        indicator_id = flask.request.args.get('indicator_id')

        # 2. import the data to our database
        result = data.import_data_from_worldbank(indicator_id)

        # todo if the error occurs?
        return result, 201

    def get(self):
        # Q3
        # get the query arg
        order_by = flask.request.args.get("order_by")
        if order_by:
            result = data.sorted(order_by)
            # todo if error
            return result, 200

        return data.all_tables, 200


@api.route("/collections/<int:id>")
class Q2nQ4(Resource):
    def delete(self, id):
        '''
        Q2 delete a collection by id
        :param id:
        :return:
        '''
        # todo if the table exist

        data.drop(id)

        return {"message": f"The collection {id} was removed from the database"}, 200

    def get(self, id):
        '''
        Q4 get a collection by id
        :param id:
        :return:
        '''

        # build the result
        result = data.get(id)

        # todo if error
        return result, 200

@api.route("/collections/<int:id>/<int:year>/<string:country>")
class Q5(Resource):
    def get(self, id, year, country):
        '''
        Q5 get spec data from db according to the condition
        :param id: int
        :param year: int
        :param country: str
        :return: response
        '''
        # todo if error
        return data.get_by_id_year_country(id,year,country), 200

@api.route("/collections/<int:id>/<int:year>")
class Q6(Resource):
    def get(self, id, year):
        '''
        Q6 get a list according to the condition
        :param id:
        :param year:
        :return:
        '''
        # top n or bot n
        q = flask.request.args.get('q') # todo make sure it's q or query

        result = data.get_n_country_by_year(id, year, q)
        return result,200

# 3. run
app.run(port=5890)
