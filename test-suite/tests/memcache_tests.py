import json
from time import sleep
import uuid
from hawkeye_utils import HawkeyeTestCase, HawkeyeTestSuite

__author__ = 'hiranya'

class MemcacheAddTest(HawkeyeTestCase):
  def runTest(self):
    key = str(uuid.uuid1())
    value = str(uuid.uuid1())
    status, headers, payload = self.http_post('/memcache',
      'key={0}&value={1}'.format(key, value))
    self.assertEquals(status, 200)
    entry_info = json.loads(payload)
    self.assertTrue(entry_info['success'])

    status, headers, payload = self.http_get('/memcache?key={0}'.format(key))
    self.assertEquals(status, 200)
    entry_info = json.loads(payload)
    self.assertEquals(entry_info['value'], value)

    status, headers, payload = self.http_post('/memcache',
      'key={0}&value=foo'.format(key))
    self.assertEquals(status, 200)
    entry_info = json.loads(payload)
    self.assertFalse(entry_info['success'])

    status, headers, payload = self.http_get('/memcache?key={0}'.format(key))
    self.assertEquals(status, 200)
    entry_info = json.loads(payload)
    self.assertEquals(entry_info['value'], value)

class MemcacheSetTest(HawkeyeTestCase):
  def runTest(self):
    key = str(uuid.uuid1())
    value = str(uuid.uuid1())
    status, headers, payload = self.http_post('/memcache',
      'key={0}&value={1}&update=true'.format(key, value))
    self.assertEquals(status, 200)
    entry_info = json.loads(payload)
    self.assertTrue(entry_info['success'])

    status, headers, payload = self.http_get('/memcache?key={0}'.format(key))
    self.assertEquals(status, 200)
    entry_info = json.loads(payload)
    self.assertEquals(entry_info['value'], value)

    status, headers, payload = self.http_post('/memcache',
      'key={0}&value=foo&update=true'.format(key))
    self.assertEquals(status, 200)
    entry_info = json.loads(payload)
    self.assertTrue(entry_info['success'])

    status, headers, payload = self.http_get('/memcache?key={0}'.format(key))
    self.assertEquals(status, 200)
    entry_info = json.loads(payload)
    self.assertEquals(entry_info['value'], 'foo')

class MemcacheKeyExpiryTest(HawkeyeTestCase):
  def runTest(self):
    key = str(uuid.uuid1())
    value = str(uuid.uuid1())
    status, headers, payload = self.http_post('/memcache',
      'key={0}&value={1}&timeout=6'.format(key, value))
    self.assertEquals(status, 200)
    entry_info = json.loads(payload)
    self.assertTrue(entry_info['success'])

    status, headers, payload = self.http_get('/memcache?key={0}'.format(key))
    self.assertEquals(status, 200)
    entry_info = json.loads(payload)
    self.assertEquals(entry_info['value'], value)

    sleep(8)
    status, headers, payload = self.http_get('/memcache?key={0}'.format(key))
    self.assertEquals(status, 404)

class MemcacheDeleteTest(HawkeyeTestCase):
  def runTest(self):
    key = str(uuid.uuid1())
    value = str(uuid.uuid1())
    status, headers, payload = self.http_post('/memcache',
      'key={0}&value={1}'.format(key, value))
    self.assertEquals(status, 200)
    entry_info = json.loads(payload)
    self.assertTrue(entry_info['success'])

    status, headers, payload = self.http_get('/memcache?key={0}'.format(key))
    self.assertEquals(status, 200)
    entry_info = json.loads(payload)
    self.assertEquals(entry_info['value'], value)

    status, headers, payload = self.http_delete('/memcache?key={0}'.format(key))
    self.assertEquals(status, 200)
    entry_info = json.loads(payload)
    self.assertTrue(entry_info['success'])

    status, headers, payload = self.http_get('/memcache?key={0}'.format(key))
    self.assertEquals(status, 404)

class MemcacheMultiAddTest(HawkeyeTestCase):
  def runTest(self):
    key1 = str(uuid.uuid1())
    key2 = str(uuid.uuid1())
    value1 = str(uuid.uuid1())
    value2 = str(uuid.uuid1())
    status, headers, payload = self.http_post('/memcache/multi',
      'keys={0},{1}&values={2},{3}'.format(key1, key2, value1, value2))
    self.assertEquals(status, 200)
    entry_info = json.loads(payload)
    self.assertTrue(entry_info['success'])

    status, headers, payload = self.http_get('/memcache/multi?keys={0},{1}'.
      format(key1, key2))
    self.assertEquals(status, 200)
    entry_info = json.loads(payload)
    self.assertEquals(entry_info[key1], value1)
    self.assertEquals(entry_info[key2], value2)

    status, headers, payload = self.http_post('/memcache/multi',
      'keys={0},{1}&values={2},{3}'.format(key1, key2, 'foo', 'bar'))
    self.assertEquals(status, 200)
    entry_info = json.loads(payload)
    self.assertFalse(entry_info['success'])

    status, headers, payload = self.http_get('/memcache/multi?keys={0},{1}'.
      format(key1, key2))
    self.assertEquals(status, 200)
    entry_info = json.loads(payload)
    self.assertEquals(entry_info[key1], value1)
    self.assertEquals(entry_info[key2], value2)

class MemcacheMultiSetTest(HawkeyeTestCase):
  def runTest(self):
    key1 = str(uuid.uuid1())
    key2 = str(uuid.uuid1())
    value1 = str(uuid.uuid1())
    value2 = str(uuid.uuid1())
    status, headers, payload = self.http_post('/memcache/multi',
      'keys={0},{1}&values={2},{3}&update=true'.format(key1, key2,
        value1, value2))
    self.assertEquals(status, 200)
    entry_info = json.loads(payload)
    self.assertTrue(entry_info['success'])

    status, headers, payload = self.http_get('/memcache/multi?keys={0},{1}'.
      format(key1, key2))
    self.assertEquals(status, 200)
    entry_info = json.loads(payload)
    self.assertEquals(entry_info[key1], value1)
    self.assertEquals(entry_info[key2], value2)

    status, headers, payload = self.http_post('/memcache/multi',
      'keys={0},{1}&values={2},{3}&update=true'.format(key1, key2, 'foo', 'bar'))
    self.assertEquals(status, 200)
    entry_info = json.loads(payload)
    self.assertTrue(entry_info['success'])

    status, headers, payload = self.http_get('/memcache/multi?keys={0},{1}'.
      format(key1, key2))
    self.assertEquals(status, 200)
    entry_info = json.loads(payload)
    self.assertEquals(entry_info[key1], 'foo')
    self.assertEquals(entry_info[key2], 'bar')

class MemcacheMultiDeleteTest(HawkeyeTestCase):
  def runTest(self):
    key1 = str(uuid.uuid1())
    key2 = str(uuid.uuid1())
    value1 = str(uuid.uuid1())
    value2 = str(uuid.uuid1())
    status, headers, payload = self.http_post('/memcache/multi',
      'keys={0},{1}&values={2},{3}'.format(key1, key2, value1, value2))
    self.assertEquals(status, 200)
    entry_info = json.loads(payload)
    self.assertTrue(entry_info['success'])

    status, headers, payload = self.http_get('/memcache/multi?keys={0},{1}'.
      format(key1, key2))
    self.assertEquals(status, 200)
    entry_info = json.loads(payload)
    self.assertEquals(entry_info[key1], value1)
    self.assertEquals(entry_info[key2], value2)

    status, headers, payload = self.http_delete('/memcache/multi?keys={0},{1}'.
      format(key1, key2))
    self.assertEquals(status, 200)
    entry_info = json.loads(payload)
    self.assertTrue(entry_info['success'])

    status, headers, payload = self.http_get('/memcache/multi?keys={0},{1}'.
      format(key1, key2))
    self.assertEquals(status, 200)
    entry_info = json.loads(payload)
    self.assertEquals(len(entry_info), 0)

def suite():
  suite = HawkeyeTestSuite('Memcache Test Suite', 'memcache')
  suite.addTest(MemcacheAddTest())
  suite.addTest(MemcacheSetTest())
  suite.addTest(MemcacheKeyExpiryTest())
  suite.addTest(MemcacheDeleteTest())
  suite.addTest(MemcacheMultiAddTest())
  suite.addTest(MemcacheMultiSetTest())
  suite.addTest(MemcacheMultiDeleteTest())
  return suite