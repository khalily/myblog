#!/usr/bin/env python
# encoding: utf-8

from flask.ext.script import Manager

from app import create_app

app = create_app('default')

manager = Manager(app)

@manager.command
def test():
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

if __name__ == "__main__":
    manager.run()

