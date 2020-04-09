import unittest

from modelbuilder.model import Model, Attribute

class TestSimpleModel(unittest.TestCase):
    def test_model_creation(self):
        class Primitive(Model):
            string = Attribute(obj_name="string", obj_type=str)
            _float = Attribute(obj_name="float", obj_type=float)
            integer = Attribute(obj_name="integer", obj_type=int)
            boolean = Attribute(obj_name="boolean", obj_type=bool)
        
        test_class = Primitive()
        self.assertIsNone(test_class.string)
        self.assertIsNone(test_class._float)
        self.assertIsNone(test_class.integer)
        self.assertIsNone(test_class.boolean)

