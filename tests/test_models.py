import unittest

from models import User


class TestUser(unittest.TestCase):
    def test_translate_standart(self):
        user = User.query.get(1)
        self.assertEqual(user._translate('Матвей чекашов'), 'MatveyChekashov')
        self.assertEqual(user._translate('Matvey chekashov'), 'MatveyChekashov')

    def test_translate_nothing(self):
        user = User.query.get(1)
        self.assertRaises(ValueError, user._translate, '')

    def test_translate_data_type(self):
        user = User.query.get(1)
        self.assertRaises(ValueError, user._translate, None)
        self.assertRaises(ValueError, user._translate, 1)
        self.assertRaises(ValueError, user._translate, 1.1)
        self.assertRaises(ValueError, user._translate, ['1.1'])
        self.assertRaises(ValueError, user._translate, ('1.1',))
        self.assertRaises(ValueError, user._translate, {'1.1'})
        self.assertRaises(ValueError, user._translate, {'1.1': 1.1})
        self.assertRaises(ValueError, user._translate, [])

if __name__ == '__main__':
    unittest.main()