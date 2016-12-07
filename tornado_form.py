from tornado_form_field import *

class Form(object):
    '''表单类是字段对象的集合，关心的是整个表单是否验证成功、哪些成功了，哪些是失败了'''
    def __init__(self):
        self.value_dic = {}
        self.error_dic = {}
        self.valid_status = True

    def validate(self,request,depth=10,pre_key=''):
        '''处理多级表单的迭代，调用表单中字段对象的match方法完成验证，并搜集正确的值和错误信息'''
        self.initialize()#留作扩展功能
        self.__valid(self,request,depth,pre_key)

    def initialize(self):
        pass

    def __valid(self,form_obj,request,depth,pre_key):
        '''form_obj可能是一级或二级表单对象'''
        depth -= 1
        if depth < 0:
            return None

        form_field_dic = form_obj.__dict__
        for key,field_obj in form_field_dic.items():
            if isinstance(field_obj,Form) or isinstance(field_obj,Field):
                if isinstance(field_obj,Form):
                    self.__valid(field_obj,request,depth,key)
                    continue
                if pre_key:#如果当前进入到了递归，修正字段名
                    key = '%s.%s' % (pre_key,key)

                if isinstance(field_obj,CheckBoxField):
                    #获取多选框的值用get_arguments
                    post_value = request.get_arguments(key,None)
                elif isinstance(field_obj,FileField):
                    #获取文件
                    post_value = []
                    file_list = request.request.files.get(key,None)
                    for file_item in file_list:
                        post_value.append(file_item['filename'])
                else:
                    #获取其他用get_argument
                    post_value = request.get_argument(key,None)

                print(post_value)
                #调用自定义方法做正则匹配
                field_obj.match(key,post_value)
                if field_obj.is_valid:
                    self.value_dic[key] = field_obj.value
                else:
                    self.error_dic[key] = field_obj.error
                    self.valid_status = False

class MainForm(Form):
    '''用于处理单行数据提交'''
    def __init__(self):
        # 先定义字段
        self.ip = IPField(required=True)
        self.port = IntegerField(required=True)
        self.new_ip = IPField(required=True)
        self.second = SecondForm()#有二级表单
        # self.image = FileField(required=True)
        super(MainForm,self).__init__()

class SecondForm(Form):
    def __init__(self):
        self.ip = IPField(required=True)
        self.port = IntegerField(required=True)
        super(SecondForm, self).__init__()

class ListForm(object):
    '''用于处理连续、多行批量数据提交'''
    def __init__(self,form_type):
        self.form_type = form_type
        self.valid_status = True
        self.valid_dic = {}
        self.error_dic = {}

    def validate(self,request):
        '''仅能处理序号从0开始且不间断的批量数据,如字段名分别为：
            [0].ip,[0].port, ...
            [1].ip,[1].port, ...
            [2].ip,[2].port, ...
        '''
        name_list = list(request.request.arguments.keys()) + list(request.request.files.keys())
        index = 0
        flag = False
        while True:
            pre_key = '[%d]' % index
            for name in name_list:
                if name.startswith(pre_key):
                    flag = True
                    break
            if flag:
                form_obj = self.form_type()
                form_obj.validate(request,depth=10,pre_key=pre_key)
                if form_obj.valid_status:
                    self.value_dic[index] = form_obj.value_dic
                else:
                    self.error_dic[index] = form_obj.error_dic
                    self.valid_status = False
            else:
                break
            index += 1
            flag = False