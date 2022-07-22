import json
from db_connection import connect_to_db

def lambda_handler(event, context):
    # TODO implement
    conn, cursor = connect_to_db()
    cursor.execute("select * from Notice")

    rows = cursor.fetchall()

    for row in rows:
        print("{0} {1}".format(row[0], row[1]))

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!'),
    }
