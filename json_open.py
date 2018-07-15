import json

#загрузить из json
def open_conf(class_name):
    with open(class_name+'_base_config.json', 'r', encoding='utf-8') as conf: #открываем файл на чтение
        data = json.load(conf) #загружаем из файла данные в словарь data
    return(data)
