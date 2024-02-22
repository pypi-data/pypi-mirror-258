from ast import literal_eval
from tqdm import tqdm as tq
import sqlalchemy as sa


#env파일 read
def get_env_keyvalue(key):
    """
    Create folders and files in that path
    path = './env/env.txt'
    
    sample 
    {'pg_dbname': '','pg_passwd': '','pg_userid': '','pg_host':'','pg_port':''}
    """
    try:
        path = './env/env.txt'
        f = open(path, 'r', encoding='utf-8-sig')
        line = f.readline()
        f.close()

        env_dict = literal_eval(line)

        return env_dict[key]

    # ----------------------------------------
    # 모든 함수의 공통 부분(Exception 처리)
    # ----------------------------------------
    except Exception:
        raise

# db연결후 data insert
def create_table(df,name,exists):
    engine=sa.create_engine(f'postgresql://{get_env_keyvalue("pg_userid")}:{get_env_keyvalue("pg_passwd")}@{get_env_keyvalue("pg_host")}/{get_env_keyvalue("pg_dbname")}', client_encoding='utf8')

    with tq(total=len(df)) as pbar:
        def update_progress(*args, **kwargs):
            pbar.update(1)

        df.apply(update_progress,axis=1)

    if exists == 'append':
        df.to_sql(name=name, con=engine, if_exists='append', schema='public', index=False, chunksize=100)
    elif exists == 'fail':
        df.to_sql(name=name, con=engine, if_exists='fail', schema='public', index=False, chunksize=100)
    elif exists == 'replace':
        df.to_sql(name=name, con=engine, if_exists='replace', schema='public', index=False, chunksize=100)
    else:
        raise Exception("Please enter one of the following: 'append' or 'fail' or 'replace'")