import base64

def get_image(name):
	return str(base64.b64encode(open('images/'+name, 'rb').read()))[2:-1]