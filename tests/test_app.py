import os
import tempfile
import unittest
import app as todo


class TodoTests(unittest.TestCase):
    def setUp(self):
        fd, self.path = tempfile.mkstemp()
        os.close(fd)
        todo.DB_PATH = self.path
        todo.init_db()
        self.client = todo.app.test_client()

    def tearDown(self):
        os.unlink(self.path)

    def test_health(self):
        self.assertEqual(self.client.get('/health').json, {'status': 'ok'})

    def test_add_toggle_delete(self):
        self.client.post('/add', data={'title': 'Study DevOps'})
        self.assertIn(b'Study DevOps', self.client.get('/').data)
        self.client.post('/toggle/1')
        self.assertIn(b'Completed', self.client.get('/').data)
        with todo.get_db() as conn:
            self.assertEqual(conn.execute('SELECT completed FROM tasks WHERE id = 1').fetchone()[0], 1)
        self.client.post('/delete/1')
        self.assertNotIn(b'Study DevOps', self.client.get('/').data)

    def test_blank_task_not_added(self):
        self.client.post('/add', data={'title': '   '})
        with todo.get_db() as conn:
            self.assertEqual(conn.execute('SELECT COUNT(*) FROM tasks').fetchone()[0], 0)


if __name__ == '__main__':
    unittest.main()
