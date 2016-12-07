import re,os

class Field(object):
    '''字段类，只关心当前字段是否通过验证、正确值、错误信息'''
    def __init__(self,error_msg_dic,required):
        self.is_valid = False
        self.value = None
        self.error = None
        self.name = None
        self.error_msg = error_msg_dic
        self.required = required

    def match(self,name,value):
        '''所有字段类型的公共验证方法
        传入字段名和字段值'''
        self.name = name
        if not self.required:
            self.is_valid = True
            self.value = value
        else:
            if not value:
                if self.error_msg.get('required',None):
                    self.error = self.error_msg['required']
                else:
                    self.error = '%s is required' % name
            else:
                ret = re.match(self.REGULAR,value)
                if ret:
                    self.is_valid = True
                    self.value = ret.group()
                else:
                    if self.error_msg.get('valid',None):
                        self.error = self.error_msg('valid')
                    else:
                        self.error = '%s is invalid' % name

class IPField(Field):
    REGULAR = "^(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}$"

    def __init__(self, error_msg_dict=None, required=True):

        error_msg = {}  # {'required': 'IP不能为空', 'valid': 'IP格式错误'}
        if error_msg_dict:
            error_msg.update(error_msg_dict)

        super(IPField, self).__init__(error_msg_dic=error_msg, required=required)


class IntegerField(Field):
    REGULAR = "^\d+$"

    def __init__(self, error_msg_dict=None, required=True):
        error_msg = {'required': '数字不能为空', 'valid': '数字格式错误'}
        if error_msg_dict:
            error_msg.update(error_msg_dict)

        super(IntegerField, self).__init__(error_msg_dic=error_msg, required=required)

class CheckBoxField(Field):
    '''多选框仅仅验证值是否是列表类型'''
    def __init__(self,error_msg_dic=None,required=True):
        error_msg = {}
        if error_msg_dic:
            error_msg.update(error_msg_dic)
        super(CheckBoxField, self).__init__(error_msg_dic=error_msg,required=required)

    def match(self,name,value):
        self.name = name
        if not self.required:
            self.is_valid = True
            self.value = value
        else:
            if not value:
                if self.error_msg.get('required',None):
                    self.error = self.error_msg['required']
                else:
                    self.error = '%s is required' % name
            else:
                if isinstance(name,list):
                    self.is_valid = True
                    self.value = value
                else:
                    if self.error_msg.get('valid',None):
                        self.error = self.error_msg['valid']
                    else:
                        self.error = '%s is invalid' % name

class FileField(Field):
    REGULAR = "^(\w+\.pdf)|(\w+\.mp3)|(\w+\.py)$"
    def __init__(self,error_msg_dic=None,required=True):
        error_msg = {}
        if error_msg_dic:
            error_msg.update(error_msg_dic)
        super(CheckBoxField, self).__init__(error_msg_dic=error_msg,required=required)

    def match(self,name,value):
        self.name = name
        self.value = []
        if not self.required:
            self.is_valid = True
            self.value = value
        else:
            if not value:
                if self.error_msg.get('required',None):
                    self.error = self.error_msg['required']
                else:
                    self.error = '%s is required' % name
            else:
                m = re.compile(self.REGULAR)
                if isinstance(value,list):
                    for file_name in value:
                        r = m.match(file_name)
                        if r:
                            self.value.append(r.group())
                            self.is_valid = True
                        else:
                            self.is_valid = False
                            if self.error_msg.get('valid',None):
                                self.error = self.error_msg['valid']
                            else:
                                self.error = '%s is invalid' % name
                            break
                else:
                    if self.error_msg.get('valid', None):
                        self.error = self.error_msg['valid']
                    else:
                        self.error = '%s is invalid' % name

    def save(self,request,upload_path=''):
        file_metas = request.files[self.name]
        for meta in file_metas:
            file_name = os.path.join(upload_path,meta['filename'])
            with open(file_name) as up:
                up.write(meta['body'])