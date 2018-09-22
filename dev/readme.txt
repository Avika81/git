docker run -it --rm --name my-running-script -v "$PWD":/usr/src/myapp -w /usr/src/myapp python:3 bash
> pip install virtualenv
> virtualenv venv
> venv/bin/pip install -r installation_requirements
> exit

#run
docker run -p 8888:8000 -it --rm -v "$PWD":/usr/src/myapp -w /usr/src/myapp python:3 venv/bin/python run.py


curl -v --header "Content-Type: application/json" \
  --request POST \
  --data '{"username":"xyz","password":"xyz"}' \
  http://localhost:8888/
