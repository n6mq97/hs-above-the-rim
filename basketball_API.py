import sys
from above_the_rim.app_factory import create_app
from above_the_rim.configs.prod import ProdConfig

# don't change the following way to run flask:
if __name__ == '__main__':
    app = create_app(ProdConfig())

    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run(debug=True)