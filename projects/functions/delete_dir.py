import os
import shutil
from projects import UPLOAD_FOLDER
from flask_login import current_user

def delete_dir():
    codes = "projects/codes/"+current_user.NIM
    decodes = "projects/decodes/"+current_user.NIM
    result = "projects/results/"+current_user.NIM
    if os.path.exists(codes) == True:
        shutil.rmtree(codes)
    
    if os.path.exists(decodes) == True:
        shutil.rmtree(decodes)
    
    if os.path.exists(result) == True:
        shutil.rmtree(result)
    
def del_user_dir():
    user_dir = UPLOAD_FOLDER+'/'+current_user.NIM

    if os.path.exists(user_dir) == True:
        shutil.rmtree(user_dir)
