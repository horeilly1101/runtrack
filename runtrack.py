from runtrack_app import app, db

# import db in shell
@app.shell_context_processor
def make_shell_context():
	return {'db': db}

import runtrack_app.functions as func

print(func)