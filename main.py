import psycopg2
from tqdm import tqdm
import time

class DataBase:
    def __init__(self, connection):
        self.connection = connection

    def create_database(self):
        with self.connection.cursor() as cur:
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
            self.connection.commit()

class Client:
    def __init__(self, conn):
        self.conn = conn

    def add_new_client(self, records):
        with self.conn.cursor() as cur:
            postgre_insert = """
                    insert into clients(client_id, first_name, last_name, email) values (%s, %s, %s, %s);
                    """
            result = cur.execute(postgre_insert, records)
            self.conn.commit()

    def add_phone(self, phone):
        with self.conn.cursor() as cur:
            postgre_insert = """
        insert into client_phones(link_id, client_id, phone_number) values (%s, %s, %s);
        """
            result = cur.execute(postgre_insert, phone)
            self.conn.commit()

    def change_client_data(self):
        with self.conn.cursor() as cur:
            postgre = ['update clients set ']
            query_update = input('Обновить информацию по клиентам?: ')
            condition = ' where '
            if query_update.lower() == 'да':
                i = 0
                while i < 6:
                    query = input('Введите по-одному параметры для обновления(first_name = , last_name = , email = ): ')
                    query_condition = input('Введите условие для обновления строки(например: client_id = 1): ')
                    if query.lower() != 'нет':
                        postgre.append(query)
                        postgre.append(condition)
                        postgre.append(query_condition)
                    else:
                        postgre.append(';')
                        break
                        i = i + 1
                postgre_update = ''.join(postgre)
                cur.execute(postgre_update)
                self.conn.commit()

    def update_phone(self, phone):
        with self.conn.cursor() as cur:
            postgre_insert = """
        update client_phones set phone = %s where client_id = %s;
        """
            result = cur.execute(postgre_insert, phone)
            self.conn.commit()

    def delete_data_phone(self, record):
        with self.conn.cursor() as cur:
            postgre_delete = ("""
        delete from client_phones where client_id = %s;
        """)
            result = cur.execute(postgre_delete, record)
            self.conn.commit()

    def delete_client(self, record):
        with self.conn.cursor() as cur:
            postgre_delete = ("""
        delete from clients where client_id = %s;  
        """)
            result = cur.execute(postgre_delete, (record,))
            self.conn.commit()

    def find_client(self):
        with self.conn.cursor() as cur:
            postgre = ['select * from clients full join client_phones using(client_id) where ']
            query_select = input('Вывести информацию по клиентам?: ')
            condition = ' or '
            if query_select.lower() == 'да':
                i = 0
                while i < 6:
                    query = input('Введите по-одному параметры для поиска(client_id = , first_name = '', last_name = '', email = '', phone_number = ''): ')
                    if query.lower() != 'нет':
                        postgre.append(query)
                        postgre.append(condition)
                    else:
                        postgre.pop(-1)
                        postgre.append(';')
                        break
                    i = i + 1

            postgre_find = ''.join(postgre)

            cur.execute(postgre_find)
            print(cur.fetchall())

print('Программа для управления клиентами в базе данных')
time.sleep(1)
print('Чтобы подключиться к базе данных, введите данные:')
time.sleep(1)

user_name = input('Имя пользователя: ')
user_password = input('Пароль: ')
if __name__ == '__main__':
    try:
        connection = psycopg2.connect(database='netology_db', user=user_name, password=user_password)

        data_base = DataBase(connection)
        create = data_base.create_database()
        clients = Client(connection)

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
                add_client = clients.add_new_client(records_to_insert)
                print('')
                print('Клиент успешно внесен в базу данных')
                print('')
            else:
                break

        for m in range(10):
            query_phone = input('Добавить номер телефона клиенту?: ')
            if query_phone.lower() == 'да':
                print('')
                query_client = input(f'Клиенту с каким порядковым номером добавить телефон?(не больше {client_id_db}): ')
                if query_client <= client_id_db:
                    print('Добавление телефона(формат 123-456)')
                    print('')
                    link_id = input('Введите порядковый номер записи: ')
                    phone_number = input('Введите телефон клиента: ')
                    records_to_insert = (link_id, query_client, phone_number)
                    add_phone = clients.add_phone(records_to_insert)
                    print('')
                    print(f'Номер телефона успешно добавлен клиенту {query_client}')
                    print('')
                else:
                    print('Клиента с таким номером не существует')
            else:
                break

        clients.change_client_data()

        for m in range(10):
            query_change = input('Клиенту с каким id удалить номер телефона?: ')
            if query_change.lower() != 'не удалять':
                print('')
                print(f'Удаление телефона клиента с номером {query_change}')
                print('')
                records_to_delete = (query_change)
                clients.delete_data_phone(records_to_delete)
                print(f'Данные клиента {query_change} успешно обновлены')
                print('')
            else:
                break

        for m in range(10):
            query_change = input('Удалить устаревшие данные?: ')
            print('')
            if query_change.lower() == 'да':
                client = input(f'Для клиента с каким порядковым номером удалить данные?(не больше {client_id_db}): ')
                if client <= client_id_db:
                    print('')
                    print(f'Удаление данных клиента с номером {client}')
                    print('')
                    records_to_delete = (client)
                    clients.delete_client(records_to_delete)
                    print('')
                    print(f'Данные клиента {client} удалены')
            else:
                break

        clients.find_client()

        connection.close()

    except psycopg2.OperationalError:
        print(f'Произошла ошибка. Проверьте правильность логина и пароля')
    except psycopg2.errors.UniqueViolation:
        print(f'Клиент с введенными данными уже записан в базу данных')
    except psycopg2.errors.CheckViolation:
        print(f'Пожалуйста, проверьте формат введенных данных')
    except psycopg2.errors.ForeignKeyViolation:
        print(f'Клиента с указанным id не существует, проверьте корректность данных')