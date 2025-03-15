from zeep import Client

def get_url() -> str:
    print("Доступные категории для запроса:")
    print("+ Temperature")
    category = input("Введите категорию запроса или оствьте поле не заполненым для выхода: ")

    match category:
        case 'Temperature':
            url = 'https://www.w3schools.com/xml/tempconvert.asmx?WSDL'
        case _:
            url = None
            print('Выбран неподдерживаемая категория!')

    return url

def get_data_on_method():
    url = get_url()

    if url:
        client = Client(url)
        services = client.service
        methods = services.__dir__()
        filtered_methods = [method for method in methods if not method.startswith('__')]
        
        print("Доступные методы для выбранной категории:")
        for method in filtered_methods:
            print(f"+ {method}")

        method = input("Введите метод: ")
        if method in filtered_methods:
            num = input("Введите число: ")
            result = getattr(services, method)(num)
            return result
        else: print('Выбран неподдерживаемый метод!')


if __name__ == '__main__':
    while True:
        result = get_data_on_method()
        if result:
            print("Результат:", result)
        else: break 


