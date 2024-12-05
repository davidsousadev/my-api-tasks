# items_controller.py
from flask import jsonify, request
from models import Item
from database import db

def init_app(app):
    @app.route('/items', methods=['GET'])
    def get_items():
        """
        Retorna todos os itens.
        ---
        responses:
          200:
            description: Lista de itens
            schema:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                    description: O ID do item
                  item:
                    type: string
                    description: O nome do item
        """
        items = Item.query.all()
        return jsonify([item.to_dict() for item in items])

    @app.route('/items/<int:item_id>', methods=['GET'])
    def get_items_by_id(item_id):
        """
        Retorna um item pelo seu ID.
        ---
        parameters:
          - name: item_id
            in: path
            type: integer
            required: true
            description: O ID do item
        responses:
          200:
            description: Item encontrado
            schema:
              type: object
              properties:
                id:
                  type: integer
                  description: O ID do item
                item:
                  type: string
                  description: O nome do item
          404:
            description: Item não encontrado
        """
        item = Item.query.get_or_404(item_id)
        return jsonify(item.to_dict())

    @app.route('/items/<string:item>', methods=['GET'])
    def get_items_by_item(item):
        """
        Retorna um item pelo nome.
        ---
        parameters:
          - name: item
            in: path
            type: string
            required: true
            description: O nome do item
        responses:
          200:
            description: Item encontrado
            schema:
              type: object
              properties:
                id:
                  type: integer
                  description: O ID do item
                item:
                  type: string
                  description: O nome do item
          404:
            description: Item não encontrado
        """
        item = Item.query.filter_by(item=item).first_or_404()
        return jsonify(item.to_dict())

    @app.route('/items', methods=['POST'])
    def create_item():
        """
        Cria um novo item.
        ---
        parameters:
          - name: item
            in: body
            required: true
            schema:
              type: object
              properties:
                item:
                  type: string
                  description: O nome do item
        responses:
          201:
            description: Item criado com sucesso
            schema:
              type: object
              properties:
                id:
                  type: integer
                item:
                  type: string
        """
        data = request.get_json()
        new_item = Item(item=data['item'])
        db.session.add(new_item)
        db.session.commit()
        return jsonify(new_item.to_dict()), 201

    @app.route('/items/<int:item_id>', methods=['PUT'])
    def update_item(item_id):
        """
        Atualiza um item existente.
        ---
        parameters:
          - name: item_id
            in: path
            type: integer
            required: true
            description: O ID do item
          - name: item
            in: body
            required: true
            schema:
              type: object
              properties:
                item:
                  type: string
                  description: O nome do item
        responses:
          200:
            description: Item atualizado com sucesso
            schema:
              type: object
              properties:
                id:
                  type: integer
                item:
                  type: string
        """
        data = request.get_json()
        item = Item.query.get_or_404(item_id)
        item.item = data.get('item', item.item)
        db.session.commit()
        return jsonify(item.to_dict())

    @app.route('/items/<int:item_id>', methods=['DELETE'])
    def delete_item(item_id):
        """
        Deleta um item pelo seu ID.
        ---
        parameters:
          - name: item_id
            in: path
            type: integer
            required: true
            description: O ID do item
        responses:
          204:
            description: Item deletado com sucesso
        """
        item = Item.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return '', 204
