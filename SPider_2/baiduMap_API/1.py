'''
crtl + r
'''


def update(self, table_name, data, restrication_str):
    data_str = ''
    for item in data.items():
        data_str += '{}="{}",'.format(item[0], item[1])
    values = data_str[:-1]

dicts = {
    'name':'Tuling',
    'age':18,
    'sex':'W'
}
data_str = ''
for item in dicts.items():
    # print(item)
    data_str += '{}="{}",'.format(item[0], item[1])
    # print(data_str)
    # print(type(data_str))
values = data_str[:-1]
print(values)


'''
{.........}
{
    {
        
    },
    {
        
    }
}'''

a = dicts.keys()
print(a)
print(type(a))

a = [11,22,33,22,33,44,55]
b = tuple(a)
print(b)
