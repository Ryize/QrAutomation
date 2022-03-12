from datetime import datetime

from main import db


class User(db.Model):
    """
    Модель представления пользователя.
    Пользователь может отмечать уборку в кабинете(class: ScheduleCleaning)
    """
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True)
    login = db.Column(db.String(64), unique=True)
    name = db.Column(db.String(64), nullable=False)
    surname = db.Column(db.String(64), nullable=False)
    patronymic = db.Column(db.String(64))
    password = db.Column(db.String(128), nullable=False)
    user_sc = db.relationship('ScheduleCleaning', backref='user')
    created_on = db.Column(db.DateTime, default=datetime.utcnow)

    __translate_dict = {'ь': '', 'ъ': '', 'а': 'a', 'б': 'b', 'в': 'v',
                        'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh',
                        'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l',
                        'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r',
                        'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h',
                        'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch', 'ы': 'yi',
                        'э': 'e', 'ю': 'yu', 'я': 'ya'}

    def create_login(self) -> str:
        """
        Установить пользователю логин по имени и фамилии с помощью транслитерации
        :example: имя=Матвей, фамилия=Чекашов -- будет установлен логин MatveyChekashov
        :return: строка с логином(str)
        """
        self.login = self._translate(f'{self.name} {self.surname}')
        return self.login

    def _translate(self, string: str) -> str:
        """
        Транслитерация строки с русских символов в английские
        :example: Матвей чекашов -> MatveyChekashov
        """
        if not string or not isinstance(string, str):
            raise ValueError('Для транслитерации необходима исходная строка(str)!')
        string = string.lower()
        translate_string = ''
        tr_dict = self.__translate_dict
        for i in string:
            translate_string += tr_dict.get(i.lower(), i.lower()).upper() if i.isupper() else tr_dict.get(i, i)
        translate_string = ''.join(
            translate_string.title().split())  # Удаляем пробелы/табы из строки. Первая буква слова будет большой
        return translate_string

    def __repr__(self):
        return f'<User: {self.id}, {self.name}-{self.surname}>'


class Cabinet(db.Model):
    """
    Класс описывает помещение, которое убирают.
    При уборке(class: ScheduleCleaning) передаётся ссылка на конкретный кабинет
    """
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(48), nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    sc = db.relationship('ScheduleCleaning', backref='cabinet')

    def __repr__(self):
        return f'<Cabinet: {self.id}, {self.number}>'


class ScheduleCleaning(db.Model):
    """
    Чтобы убрать кабинет, пользователь создаёт экземпляр данного класса.
    Данный класс ссылается на помещение(class: Cabinet) и на пользователя(class: User), которой это помещение убрал
    """
    id = db.Column(db.Integer, primary_key=True)
    cabinet_id = db.Column(db.Integer, db.ForeignKey('cabinet.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    updated_on = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<ScheduleCleaning: {self.id}, {self.created_on}>'


db.create_all()
