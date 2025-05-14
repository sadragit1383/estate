import logging
logger = logging.getLogger(__name__)
from django.utils import timezone
from django.http import HttpResponseForbidden
from datetime import timedelta
import random
import web.settings as settings
import os
from uuid import uuid4




def create_random_code(num):
    import random
    num-=1
    return random.randint(10**num,10**(num+1)-1)





from sms_ir import SmsIr
def send_sms(number,code):

    pass
    sms_ir = SmsIr('he4QV5RJiXYsfgjHBpgjpJ2GMFtemy28GSEcDlCpEweK9q0ahroGcmgT5kexuJUR')

    result = sms_ir.send_verify_code(
        number=str(number),
        template_id=172582,
        parameters=[
            {

                "name" : "CODE",
                "value": str(code)

            }
        ],
    )



class FileUpload:


    def __init__(self,dir,prefix):
        self.dir = dir
        self.prefix = prefix



    def upload_to(self,instance,filename):
        filename,ext=os.path.splitext(filename)
        return f'{self.dir}/{self.prefix}/{uuid4()}{filename}{ext}'



