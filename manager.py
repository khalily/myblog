#!/usr/bin/env python
# encoding: utf-8

from flask.ext.script import Manager, Shell

from app import create_app
from app.models import db, User, Role

app = create_app('default')

manager = Manager(app)

def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)

manager.add_command("shell", Shell(make_context=make_shell_context))

@manager.command
def test():
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

if __name__ == "__main__":
    manager.run()

