from mysql_client import MysqlClient

class Field:
    def __init__(self,name,column_type,primary_key,default):
        self.name = name
        self.column_type = column_type
        self.primary_key = primary_key
        self.default = default

class IntegerField(Field):
    def __init__(self,name,column_type=int,primary_key=False,default=0):
        super().__init__(name,column_type,primary_key,default)

class StringField(Field):
    def __init__(self,name,column_type=str,primary_key=False,default=0):
        super().__init__(name,column_type,primary_key,default)

class OrmMetaclass(type):
    def __new__(cls,class_name,class_base,class_dic):
        if class_name == 'Models':
            return type.__new__(cls,class_name,class_base,class_dic)
        primary_key = None
        mappings = {}
        table_name = class_dic.get('table_name',class_name)
        for key,value in class_dic.items():
            if isinstance(value,Field):
                mappings[key] = value
                if value.primary_key:
                    if primary_key:
                        raise TypeError('只能有一个主键')
                    primary_key = value.primary_key
        if not primary_key:
            raise TypeError('必须有一个主键')
        for key in mappings.keys():
            class_dic.pop(key)
        class_dic['primary_key'] = primary_key
        class_dic['table_name'] = table_name
        class_dic['mappings'] = mappings
        return type.__new__(cls,class_name,class_base,class_dic)

class Models(dict,OrmMetaclass):
    def __getattr__(self, item):
        return self.get(item)

    def __setattr__(self, key, value):
        self[key] = value


    @classmethod
    def orm_select(cls,**kwargs):
        mysql = MysqlClient()
        if not kwargs:
            sql = 'select * from %s'%cls.table_name
            res = mysql.my_select(sql)
        else:
            key = list(kwargs.keys())[0]
            value = kwargs.get(key)
            sql = 'select * from %s where %s = ?'%(cls.table_name,key)
            sql = sql.replace('?','%s')
            res = mysql.my_select(sql,value)
        return [cls(**d) for d in res ]



    def orm_insert(self):
        mysql = MysqlClient()
        keys = []
        values = []
        args = []
        for k,v in self.mappings.items():
            if not v.primary_key:
                keys.append(v.name)
                values.append(getattr(self,v.name))
                args.append('?')
        sql = 'insert into %s(%s) values(%s)'%(self.table_name,
                                               ','.join(keys),
                                               ','.join(args))
        sql = sql.replace('?','%s')
        mysql.my_execute(sql,values)

    def orm_update(self):
        mysql = MysqlClient()
        keys = []
        values = []
        primary_key = None
        for k,v in self.mappings.items():
            if v.primary_key:
                primary_key = v.name + '= %s'%(getattr(self,v.name))
            else:
                keys.append(v.name + '= ?')
                values.append(getattr(self,v.name))
        sql = 'update %s set %s where %s'%(self.table_name,
                                           ','.join(keys),
                                           primary_key)
        sql = sql.replace('?','%s')
        mysql.my_execute(sql,values)


