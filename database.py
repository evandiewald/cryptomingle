from sqlalchemy import Table, Column, String, Integer, MetaData, func


def users_table(db):
    table = Table('users', MetaData(db),
                  Column('id', Integer, primary_key=True, nullable=False),
                  Column('name', String, nullable=False),
                  Column('email', String, nullable=False),
                  Column('address', String, nullable=False),
                  Column('age', Integer),
                  Column('height', Integer),
                  Column('imageurl', String),
                  Column('bio', String),
                  Column('transaction', String))
    return table


def add_user(session, users_table, height, address, name, email, age, bio, imageurl, transaction):
    id = get_next_id(session, users_table)
    users_table.insert().values(id=id, height=height, address=address, name=name, email=email,
                                age=age, bio=bio, imageurl=imageurl, transaction=transaction).execute()



def get_next_id(session, users_table):
    next_id = session.query(func.max(users_table.columns.id)).scalar()
    if not next_id:
        next_id = 1
    return next_id


def list_users(users_table):
    select_statement = users_table.select().execute()
    result_set = select_statement.fetchall()
    users_list = []
    for r in result_set:
        users_list.append(r)
        print(r)
    return users_list