from flask import Flask, request, jsonify
import mysql.connector
from autoNXT.database.queries import LIST_CONNECTORS, INSERT_CONNECTOR
from autoNXT.database.dbConnection import get_db_connection
autoNxtApp = Flask(__name__)



# LIST_CONNECTORS = 'SELECT * FROM Connectors;'

@autoNxtApp.route('/list_connectors', methods=['GET'])
def get_connectors():
    con = get_db_connection()
    cursor = con.cursor()
    cursor.execute(LIST_CONNECTORS)
    tables = cursor.fetchall()
    cursor.close()
    con.close()
    table_names = [table[1] for table in tables]
    return jsonify(table_names), 200


@autoNxtApp.route('/add_connector', methods=['POST'])
def add_connector():
    try:
        data = request.get_json()
        connector_name = data.get('connector_name')
        print(connector_name)
        con = get_db_connection()
        cursor = con.cursor()
        cursor.execute(INSERT_CONNECTOR, (connector_name,))
        con.commit()
        cursor.close()
        con.close()
        return jsonify({"message": "Connector added successfully", "data": data}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500


if __name__ == '__main__':
    autoNxtApp.run(debug=True)