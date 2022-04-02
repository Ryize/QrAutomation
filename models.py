from abc import abstractmethod, ABC
from datetime import datetime
from flask_login import UserMixin, login_user
from werkzeug.security import check_password_hash, generate_password_hash

from app import db, login_manager


class IUser(ABC):
    @abstractmethod
    def register(self, **kwargs):
        pass

    @abstractmethod
    def login_user(self, **kwargs):
        pass


class User(db.Model, UserMixin):
    """
    Модель представления пользователя.
    Пользователь может отмечать уборку в кабинете(class: ScheduleCleaning)
    """
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64))
    login = db.Column(db.String(64), unique=True)
    name = db.Column(db.String(64), nullable=False)
    surname = db.Column(db.String(64), nullable=False)
    patronymic = db.Column(db.String(64))
    admin_status = db.Column(db.Boolean, default=False)
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

    @staticmethod
    def login_user(username: str, password: str) -> bool:
        """
        Метод аутентификации и авторизации пользователя с помощью Flask-Login
        :return: bool(True - пользователь успешно авторизован, False - что-то пошло не так (Неверный пароль и т.п.))
        """
        user = User.query.filter_by(login=username).first()
        if not user:
            user = User.query.filter_by(email=username).first()
        if not user:
            user = User.query.filter_by(id=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return True
        return False

    @staticmethod
    def register(username: str, surname: str, patronymic: str, email: str, password: str,
                 auto_login: bool = True) -> IUser:
        """
        Метод регистрации пользователя
        :param password: str(метод шифрует пароль с помощью werkzeug.security.generate_password_hash)
        :return: Готовый экземпляр класса User(Конкретный пользователь).
                 Если при регистрации возникла ошибка, кидается исключение ValueError
        """
        if not (len(username) < 2 or len(surname) < 2 or len(password) < 4 or password == '1234'):
            password = generate_password_hash(password)
            user = User(name=username, surname=surname, patronymic=patronymic, password=password, email=email)
            if auto_login:
                user.create_login()
            db.session.add(user)
            db.session.commit()
            return user
        raise ValueError('Данные для регистрации не корректны!')

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

    def login(self):
        pass

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


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
