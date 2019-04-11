import pymysql


db = pymysql.connect(host='127.0.0.1',
                             user='root',
                             password='S233kaas17102001',
                             db='pultickbot',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


def get_balance(id):

    with db.cursor() as cursor:
        query = "select balance from clients where id_clients = %s"
        cursor.execute(query, str(id))
        result = cursor.fetchone()
        if result.get(query) == 0:
            return 0
        return result.get('balance')


def write_task (id_person1, task, message_id, id_person2=0, cost=-1, status = 0):
    with db.cursor() as cursor:

        query = """o INSERT INTO `posts`
                          (`id_person1`, `id_person2`, `cost`, `task`, `message_id`, `status`) VALUES (%s,%s,%s,%s,%s,%s)"""
        tuple = (id_person1, id_person2, cost, task, message_id, status)
        cursor.execute(query, tuple)
        db.commit()


def get_task_id_zakazchik (id):
    with db.cursor() as cursor:

        query = "select message_id from posts where id_person1 = %s and status = 0"
        cursor.execute(query, str(id))
        result = cursor.fetchall()
        if len(result) == 0:
            return 0
        return result


def get_task_id_ispolnitel(id):
    with db.cursor() as cursor:

        query = "select message_id from posts where id_person2 = %s and status = 0"
        cursor.execute(query, str(id))
        result = cursor.fetchall()
        if len(result) == 0:
            return 0
        return result
