import re
import semantic_version

X_RANGE = re.compile(r'(\.[*xX])+$')
BAD_TILDE = re.compile(r'^~\d+$')
EXPR = re.compile(r'^(v)?(\d+)\.(\d+)\.(\d+)$')

def is_valid(tag):
  return EXPR.match(tag) is not None

def compare(version1, version2):
  version1 = EXPR.match(version1)
  version2 = EXPR.match(version2)
  result = cmp(int(version1.group(2)), int(version2.group(2)))
  if result != 0:
    return result
  result = cmp(int(version1.group(3)), int(version2.group(3)))
  if result != 0:
    return result
  result = cmp(int(version1.group(4)), int(version2.group(4)))
  if result != 0:
    return result
  return cmp(version1.group(1), version2.group(1))

def match(version, spec):
  if spec == '*' or spec == 'master':
    return True
  if X_RANGE.search(spec):
    spec = '~' + X_RANGE.sub('', spec)
  # semantic_version fails with '~1'...
  if BAD_TILDE.search(spec):
    main = spec[1:]
    spec = '>=%s,<%d' % (main, int(main) + 1)
  if version[0] == 'v':
    version = version[1:]
  try:
    return semantic_version.match(spec, version)
  except ValueError:
    # If the spec is malformed or we don't support it.
    return False
