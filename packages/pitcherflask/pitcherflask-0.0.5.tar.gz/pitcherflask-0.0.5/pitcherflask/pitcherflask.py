import argparse
import os

def create_project(args):
    project_name = args.project_name
    os.mkdir(project_name)
    os.mkdir(f'{project_name}/templates')
    os.mkdir(f'{project_name}/static')
    os.mkdir(f'{project_name}/static/img')
    with open(f"{project_name}/templates/index.html",'w') as f:
        f.write("""
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <p>Hello, World!</p>
</body>
</html>
""")
    with open(f"{project_name}/main.py",'w') as f:
        f.write("""from flask import Flask, render_template
app = Flask(__name__)
                
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run()""")
    with open(f"{project_name}/requirements.txt",'w') as f:
        f.write("flask")
    with open(f"{project_name}/README.md",'w') as f:
        f.write("# A really cool project!")

def main():
    parser = argparse.ArgumentParser(description='pitcherflask - start developing flask applications without wasting time on setup.', formatter_class=argparse.RawTextHelpFormatter, add_help=False)
    subparsers = parser.add_subparsers()

    create_parser = subparsers.add_parser('create', help='Create a new Flask project')
    create_parser.add_argument('project_name', type=str, help='Name of the project')
    create_parser.set_defaults(func=create_project)

    parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS, help='show this help message and exit')

    args = parser.parse_args()
    if not vars(args):
        parser.print_help()
        parser.exit()
    args.func(args)

if __name__ == '__main__':
    main()