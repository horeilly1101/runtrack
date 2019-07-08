
if __name__ == '__main__':
	from runtrack import create_app
	app = create_app()

	# development
	app.run(debug=True)
