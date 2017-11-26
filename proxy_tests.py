import unittest
from app import configure_proxy_settings

IP = '127.0.0.1'
PORT = '8000'
USERNAME = 'user'
PASSWORD = 'password'


class ProxyConfigTestCase(unittest.TestCase):
    def test_proxies_without_credentials(self):
        actual = configure_proxy_settings(IP, PORT)
        expected = {'http': 'http://127.0.0.1:8000',
                    'https': 'https://127.0.0.1:8000'
                    }
        self.assertEqual(actual, expected,
                         'Proxy is not configured properly, showing {}'.format(actual))

    def test_proxies_with_credentials(self):
        actual = configure_proxy_settings(IP, PORT, username=USERNAME, password=PASSWORD)
        expected = {'http': 'http://user:password@127.0.0.1:8000',
                    'https': 'https://user:password@127.0.0.1:8000'
                    }
        self.assertEqual(actual, expected,
                         'Proxy is not configured properly, showing {}'.format(actual))

    def test_proxies_with_empty_parameters(self):
        actual = configure_proxy_settings(None, None)
        self.assertEqual(actual, None,'Proxy is not configured properly, this should return None')


if __name__ == '__main__':
    unittest.main()
