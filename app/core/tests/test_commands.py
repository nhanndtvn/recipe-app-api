#Test custome commang

from unittest.mock import patch

from psycopg2 import OperationalError as Psycopg2Error

from django.core.management import call_command

from django.db.utils import OperationalError
from django.test import SimpleTestCase

"""
Vì chúng ta muốn test_wait_for_db_ready(self) chỉ chạy cho DB command và database sẳn sàng
Chúng ta không muốn nó làm thêm việc gì khác
Chúng ta chỉ muốn nó tiếp tục và cho phép chúng ta thực thi ứng dụng

Để làm điều này - chúng ta cần mock behavior của database - bằng @patch

"""
#core.management.commands -> là thự mục core/management/commands,  
#wait_for_db - là file waitfordb.py
#Command - class Commandt trong file
@patch('core.management.commands.wait_for_db.Command.check')

class CommandTests(SimpleTestCase):    
    
    #patched_check object, the magic mock object that is replaced or that replaces check by patch
    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for DB ready """
        patched_check.return_value=True
        
        call_command('wait_for_db')
        
        patched_check.assert_called_once_with(database=['default'])
    
    @patch('time.sleep')    
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        patched_check.side_effect = [Psycopg2Error] * 2 + \
            [OperationalError] * 3 + [True]
        
        call_command('wait_for_db')
        
        self.assertEqual(patched_check.call_count,6)
        
        patched_check.assert_called_with(database=['default'])
        