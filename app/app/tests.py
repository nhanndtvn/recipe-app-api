# 1. Import test
from django.test import SimpleTestCase

# 2. Import object
from app import calc


# 3. Define Test class
class CalcTest(SimpleTestCase):
    """Test Calc models"""
    # 4. Add test method
    def test_add_number(self):
        """Test adding number"""
        # 5. Setup input + 6. Execute
        res = calc.add(5, 6)
        # 7. Check output
        self.assertEqual(res, 11)

    # USING TDD
    def test_substract_number(self):
        res = calc.subtract(10, 15)  # subtract function is not defined
        self.assertEqual(res, 5)
