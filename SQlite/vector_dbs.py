import os
folder_path = 'Vector_dbs'
def create_user_folder(username):
    if not os.path.exists(f'{folder_path}/{username}'):
        os.mkdir(f'{folder_path}/{username}')

def get_all_user_vec_db(username):
    try:
        folders = [f for f in os.listdir(f'{folder_path}/{username}') if os.path.isdir(os.path.join(f'{folder_path}/{username}', f))]
        return folders
    except:
        raise Exception('folder is not exist')


