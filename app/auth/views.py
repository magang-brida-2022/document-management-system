from . import auth

@auth.get('/signin')
def login():
  return 'Login page'

@auth.get('/signup')
def register():
  return 'Register page'