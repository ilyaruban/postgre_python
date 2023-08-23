import psycopg2
from tqdm import tqdm
import time

def create_database(conn):
    with conn.cursor() as cur:
        cur.execute("""
        create table if not exists clients(
            client_id  serial      primary key,
            first_name varchar(20) not null,
            last_name  varchar(20) not null,
            email      varchar(20) not null unique);
        
        create table if not exists client_phones(
            link_id      serial       primary key,
            client_id    integer      references clients(client_id),
            phone_number varchar(20)  check(phone_number like '%_-_%')
        );  
        """)
        conn.commit()

def add_new_client(conn, records):
    with conn.cursor() as cur:
        postgre_insert = """
        insert into clients(client_id, first_name, last_name, email) values (%s, %s, %s, %s);
        """
        result = cur.execute(postgre_insert, records)
        conn.commit()

def add_phone(conn, phone):
    with conn.cursor() as cur:
        postgre_insert = """
        insert into client_phones(link_id, client_id, phone_number) values (%s, %s, %s);
        """
        result = cur.execute(postgre_insert, phone)
        conn.commit()

def change_client_data(conn, new_data):
    with conn.cursor() as cur:
        postgre_insert = """
        update clients set last_name = %s where client_id = %s;
        """
        result = cur.execute(postgre_insert, new_data)
        conn.commit()

def delete_data_phone(conn, record):
    with conn.cursor() as cur:
        postgre_delete = ("""
        delete from client_phones where client_id = %s;
        """)
        result = cur.execute(postgre_delete, record)
        conn.commit()

def delete_client(conn, record):
    with conn.cursor() as cur:
        postgre_delete = ("""
        delete from clients where client_id = %s;  
        """)
        result = cur.execute(postgre_delete, (record,))
        conn.commit()

def find_client(conn):
    with conn.cursor() as cur:
        cur.execute("""
        select * from clients
        full join client_phones using(client_id);  
        """)
        print(cur.fetchall())

print('Программа для управления клиентами в базе данных')
time.sleep(1)
print('Чтобы подключиться к базе данных, введите данные:')
time.sleep(1)

user_name = input('Имя пользователя: ')
user_password = input('Пароль: ')

try:
    connection = psycopg2.connect(database='netology_db', user=user_name, password=user_password)
    create_database(connection)
    for i in tqdm(range(100), desc = f'Создание таблиц "clients" и "client_phones"'):
        time.sleep(0.1)
        pass
    print('Таблицы успешно созданы')

    for i in range(10):
        query = input('Добавить клиента в базу данных?: ')
        if query.lower() == 'да':
            print('')
            print('Добавление нового клиента')
            print('')
            client_id_db = input('Введите порядковый номер клиента: ')
            first_name = input('Введите имя клиента: ')
            last_name = input('Введите фамилию клиента: ')
            email = input('Введите email клиента: ')
            records_to_insert = (client_id_db, first_name, last_name, email)
            add_new_client(connection, records_to_insert)
            print('')
            print('Клиент успешно внесен в базу данных')
            print('')
        else:
            break

    for m in range(10):
        query_phone = input('Добавить номер телефона клиенту?: ')
        if query_phone.lower() == 'да':
            print('')
            print('Добавление телефона(формат 123-456)')
            print('')
            link_id = input('Введите порядковый номер: ')
            client_id = input(f'Введите порядковый номер клиента(не больше {client_id_db}): ')
            phone_number = input('Введите телефон клиента: ')
            records_to_insert = (link_id, client_id, phone_number)
            add_phone(connection, records_to_insert)
            print('')
            print(f'Номер телефона успешно добавлен клиенту {client_id}')
            print('')
        else:
            break

    for m in range(10):
        query_change = input('Обновить данные в базе?: ')
        print('')
        if query_change.lower() == 'да':
            client = input(f'Для клиента с каким порядковым номером обновить данные?(не больше {client_id_db}): ')
            print('')
            print(f'Обновление фамилии клиента с номером {client}')
            print('')
            last_name = input('Введите новую фамилию клиента: ')
            records_to_update = (last_name, client)
            change_client_data(connection, records_to_update)
            print('')
            print(f'Данные клиента {client} успешно обновлены')
        else:
            break

    for m in range(10):
        query_change = input(f'Клиенту с id {client_id} был добавлен новый номер телефона, удалить старый номер?: ')
        if query_change.lower() == 'да':
            print('')
            print(f'Обновление информации по клиенту с номером {client_id}')
            print('')
            records_to_delete = (client_id)
            delete_data_phone(connection, records_to_delete)
            print(f'Данные клиента {client_id} успешно обновлены')
            print('')
        else:
            break

    for m in range(10):
        query_change = input(f'Договор клиента с id {client_id} завершен, удалить данные?: ')
        print('')
        if query_change.lower() == 'да':
            print(f'Обновление информации по клиенту с номером {client_id}')
            records_to_delete = (client_id)
            delete_client(connection, records_to_delete)
            print('')
            print(f'Данные клиента {client_id} успешно обновлены')
        else:
            break

    for m in range(10):
        query_select = input(f'Вывести всю информацию по клиентам?: ')
        if query_select.lower() == 'да':
            find_client(connection)
        else:
            break

    connection.close()
except psycopg2.OperationalError:
    print(f'Произошла ошибка. Проверьте правильность логина и пароля')
except psycopg2.errors.UniqueViolation:
    print(f'Клиент с введенными данными уже записан в базу данных')
except psycopg2.errors.CheckViolation:
    print(f'Пожалуйста, проверьте формат введенных данных')
except psycopg2.errors.ForeignKeyViolation:
    print(f'Клиента с указанным id не существует, проверьте корректность данных')