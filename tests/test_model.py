import unittest

from modelbuilder.model import Model, Attribute


class TestPrimitiveModel(unittest.TestCase):
    def setUp(self):
        class Primitive(Model):
            string = Attribute(obj_name="string", obj_type=str)
            _float = Attribute(obj_name="float", obj_type=float)
            integer = Attribute(obj_name="integer", obj_type=int)
            boolean = Attribute(obj_name="boolean", obj_type=bool)

        self.Primitive = Primitive

    def test_model_init_none(self):
        test_class = self.Primitive()

        self.assertIsNone(test_class.string)
        self.assertIsNone(test_class._float)
        self.assertIsNone(test_class.integer)
        self.assertIsNone(test_class.boolean)

    def test_model_init(self):
        test_string = "Hello"
        test_float = 1.0
        test_integer = 5
        test_boolean = True

        test_class = self.Primitive(
            string=test_string,
            _float=test_float,
            integer=test_integer,
            boolean=test_boolean
        )

        self.assertEqual(test_class.string, test_string)
        self.assertEqual(test_class._float, test_float)
        self.assertEqual(test_class.integer, test_integer)
        self.assertEqual(test_class.boolean, test_boolean)


if __name__ == '__main__':
    unittest.main()
