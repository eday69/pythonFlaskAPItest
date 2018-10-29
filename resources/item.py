from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be blank!"
                        )
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Every Item needs a store id."
                        )

    @jwt_required()
    def get(self, name):
        # item = next(filter(lambda x: x['name'] == name, items), None)
        # # return {'item': None}, 404 # not found
        # return {'item': item}, 200 if item else 404
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {"message": "An item with name '{}' already exists".format(name)}, 400 #bad request

        data = Item.parser.parse_args()

        item = ItemModel(name, **data)
        try:
            item.save_to_db()
        except:
            return {"message": "An error ocurred inserting the item."}, 500 # internal server error

        return item.json(), 201   # created


    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if (item):
            item.delete_from_db()

        return {'message': 'Item deleted'}

        # # global items
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        #
        # query = "DELETE FROM items WHERE name=?"
        # result = cursor.execute(query, (name,))
        # connection.commit()
        # connection.close()
        # # items = list(filter(lambda x: x['name'] != name, items))
        # return {'message': 'Item deleted'}

    def put(self, name):

        # data = request.get_json()
        data = Item.parser.parse_args()

        # item = next(filter(lambda x: x['name'] == name, items), None)
        item = ItemModel.find_by_name(name)
        # updated_item = ItemModel(name, data['price'])
        if item is None:
            # item = {'name': name, 'price': data['price']}
            # items.append(item)
            item = ItemModel(name, **data)
            # try:
            #     updated_item.insert()
            # except:
            #     return {"message","An error ocurred inserting the item."}, 500
        else:
            item.price = data['price']
            # item.update(data)
            # try:
            #     updated_item.update()
            # except:
            #     return {"message", "An error ocurred updating the item."}, 500
        item.save_to_db()
        return item.json()
        # return updated_item.json()


class ItemList(Resource):
    def get(self):
        # return {'items': [item.json() for item in ItemModel.query.all()}
        return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}

        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        #
        # query = "SELECT * FROM items"
        # result = cursor.execute(query)
        #
        # items=[];
        # for row in result:
        #     items.append({'name': row[0], 'price': row[1]});
        #
        # connection.commit()
        # connection.close()

        return {'items': items}
