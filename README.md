# obmovieassignment
# Solution to the assignment problem

*******************************************************************************************

## **Phase 1: Creating basic infrastructure**

1. Created Amazon EKS cluster for deployment testing and automation

2. Create nodegroup with 3 nodes

3. Updated local kubectl with the cluster kubeconfig using the command

  aws eks --region us-east-2 update-kubeconfig --name eksclusterassignment

4. Connected to the cluster and verified

```
 kubectl get nodes
NAME                                          STATUS   ROLES    AGE     VERSION
ip-172-31-23-9.us-east-2.compute.internal     Ready    <none>   4m15s   v1.21.2-eks-55daa9d
ip-172-31-3-94.us-east-2.compute.internal     Ready    <none>   4m6s    v1.21.2-eks-55daa9d
ip-172-31-35-214.us-east-2.compute.internal   Ready    <none>   4m14s   v1.21.2-eks-55daa9d
```

5. Installed all basic softwares on my centralized EC2 instance like git, docker, kubectl and also configured AWS CLI using credentials.

************************************************************************************************


## **Phase 2: Testing the Python code locally**

1. Created mongoDb atlas account and imported sample schema 

2. Modified .ini file with url 
```
# Ticket: Connection
# Rename this file to .ini after filling in your MOVIES_DB_URI and your SECRET_KEY
# Do not surround the URI with quotes

[PROD]
SECRET_KEY = super_secret_key_you_should_change
MOVIES_DB_URI = mongodb+srv://dbuser:dbuser@cluster0.e2r2m.mongodb.net/Cluster0?retryWrites=true&w=majority
MOVIES_NS = sample_mflix

[TEST]
SECRET_KEY = super_secret_testing_key
MOVIES_DB_URI = mongodb+srv://dbuser:dbuser@cluster0.e2r2m.mongodb.net/Cluster0?retryWrites=true&w=majority
MOVIES_NS = sample_mflix

```
2. Opened Port 5000 on security group to access the application directly

3. Added the entry for opening connection from all sources i.e 0.0.0.0, following code changes were done 

```
from obmovies.factory import create_app

import os
import configparser


config = configparser.ConfigParser()
config.read(os.path.abspath(os.path.join(".ini")))

if __name__ == "__main__":
    app = create_app()
    app.config['DEBUG'] = True
    app.config['MOVIES_DB_URI'] = config['PROD']['MOVIES_DB_URI']
    app.config['MOVIES_NS'] = config['PROD']['MOVIES_NS']
    app.config['SECRET_KEY'] = config['PROD']['SECRET_KEY']
    app.run(host='0.0.0.0')

```
4. Testing the application from browser on url  http://3.15.230.94:5000/status 


************************************************************************************************

## **Phase 3: Containerizing the application and creating local image**

1. Created the Dockerfile code for containerizing

```
[root@ip-172-31-21-28 pythonwebserver]# cat Dockerfile
FROM python:3
COPY obmovies /obmovies
WORKDIR /obmovies
RUN pip3 install -r requirements.txt
EXPOSE 5000
CMD [ "python3", "run.py" ]
```

2. docker build -t obmovieimage .

```
docker build -t obmovieimage .
Sending build context to Docker daemon  158.2MB
Step 1/6 : FROM python:3
3: Pulling from library/python
955615a668ce: Pull complete
2756ef5f69a5: Pull complete
911ea9f2bd51: Pull complete
27b0a22ee906: Pull complete
8584d51a9262: Pull complete
524774b7d363: Pull complete
af193b9b3d11: Pull complete
aacb0e56e8f3: Pull complete
46cd7abc9e93: Pull complete
Digest: sha256:6abb8dd5517c43615841ec2d0b71cffec4eb5b5f7098ffb97f9fb2129912eafe
Status: Downloaded newer image for python:3
 ---> a5210955ee89
Step 2/6 : COPY obmovies /obmovies
 ---> c3fa20e993b1
Step 3/6 : WORKDIR /obmovies
 ---> Running in cba4fe05d800
Removing intermediate container cba4fe05d800
 ---> 2db0b05b2e47
Step 4/6 : RUN pip3 install -r requirements.txt
 ---> Running in 4376d2d2b4b5
Collecting appnope==0.1.0
  Downloading appnope-0.1.0-py2.py3-none-any.whl (4.0 kB)
Collecting attrs==19.1.0
  Downloading attrs-19.1.0-py2.py3-none-any.whl (35 kB)
Collecting backcall==0.1.0
  Downloading backcall-0.1.0.zip (11 kB)
Collecting bcrypt==3.1.7
  Downloading bcrypt-3.1.7-cp34-abi3-manylinux1_x86_64.whl (56 kB)
Collecting bleach>=3.1.0
  Downloading bleach-4.1.0-py2.py3-none-any.whl (157 kB)
Collecting cffi==1.13.1
  Downloading cffi-1.13.1.tar.gz (460 kB)
Collecting Click==7.0
  Downloading Click-7.0-py2.py3-none-any.whl (81 kB)
Collecting decorator==4.4.0
  Downloading decorator-4.4.0-py2.py3-none-any.whl (8.3 kB)
Collecting defusedxml==0.6.0
  Downloading defusedxml-0.6.0-py2.py3-none-any.whl (23 kB)
Collecting dnspython==1.15.0
  Downloading dnspython-1.15.0-py2.py3-none-any.whl (177 kB)
Collecting entrypoints==0.3
  Downloading entrypoints-0.3-py2.py3-none-any.whl (11 kB)
Collecting Faker==0.8.13
  Downloading Faker-0.8.13-py2.py3-none-any.whl (741 kB)
Collecting flake8==3.7.8
  Downloading flake8-3.7.8-py2.py3-none-any.whl (70 kB)
Collecting Flask>=0.12.4
  Downloading Flask-2.0.1-py3-none-any.whl (94 kB)
Collecting Flask-Bcrypt==0.7.1
  Downloading Flask-Bcrypt-0.7.1.tar.gz (5.1 kB)
Collecting Flask-Cors==3.0.3
  Downloading Flask_Cors-3.0.3-py2.py3-none-any.whl (15 kB)
Collecting Flask-JWT-Extended==3.7.0
  Downloading Flask-JWT-Extended-3.7.0.tar.gz (14 kB)
Collecting Flask-Login==0.4.0
  Downloading Flask_Login-0.4.0-py2.py3-none-any.whl (15 kB)
Collecting importlib-metadata==0.23
  Downloading importlib_metadata-0.23-py2.py3-none-any.whl (28 kB)
Collecting ipykernel==5.1.3
  Downloading ipykernel-5.1.3-py3-none-any.whl (116 kB)
Collecting ipython==7.8.0
  Downloading ipython-7.8.0-py3-none-any.whl (775 kB)
Collecting ipython-genutils==0.2.0
  Downloading ipython_genutils-0.2.0-py2.py3-none-any.whl (26 kB)
Collecting ipywidgets==7.5.1
  Downloading ipywidgets-7.5.1-py2.py3-none-any.whl (121 kB)
Collecting itsdangerous==1.1.0
  Downloading itsdangerous-1.1.0-py2.py3-none-any.whl (16 kB)
Collecting jedi==0.15.1
  Downloading jedi-0.15.1-py2.py3-none-any.whl (1.0 MB)
Collecting Jinja2==2.10.3
  Downloading Jinja2-2.10.3-py2.py3-none-any.whl (125 kB)
Collecting jsonschema==3.1.1
  Downloading jsonschema-3.1.1-py2.py3-none-any.whl (56 kB)
Collecting jupyter==1.0.0
  Downloading jupyter-1.0.0-py2.py3-none-any.whl (2.7 kB)
Collecting jupyter-client==5.3.1
  Downloading jupyter_client-5.3.1-py2.py3-none-any.whl (91 kB)
Collecting jupyter-console==6.0.0
  Downloading jupyter_console-6.0.0-py2.py3-none-any.whl (21 kB)
Collecting jupyter-core==4.4.0
  Downloading jupyter_core-4.4.0-py2.py3-none-any.whl (126 kB)
Collecting MarkupSafe==1.1.1
  Downloading MarkupSafe-1.1.1-cp39-cp39-manylinux2010_x86_64.whl (32 kB)
Collecting mccabe==0.6.1
  Downloading mccabe-0.6.1-py2.py3-none-any.whl (8.6 kB)
Collecting mistune==0.8.4
  Downloading mistune-0.8.4-py2.py3-none-any.whl (16 kB)
Collecting more-itertools==7.2.0
  Downloading more_itertools-7.2.0-py3-none-any.whl (57 kB)
Collecting nbconvert==5.6.0
  Downloading nbconvert-5.6.0-py2.py3-none-any.whl (453 kB)
Collecting nbformat==4.4.0
  Downloading nbformat-4.4.0-py2.py3-none-any.whl (155 kB)
Collecting notebook==6.0.1
  Downloading notebook-6.0.1-py3-none-any.whl (9.0 MB)
Collecting pandocfilters==1.4.2
  Downloading pandocfilters-1.4.2.tar.gz (14 kB)
Collecting parso==0.5.1
  Downloading parso-0.5.1-py2.py3-none-any.whl (95 kB)
Collecting pexpect==4.7.0
  Downloading pexpect-4.7.0-py2.py3-none-any.whl (58 kB)
Collecting pickleshare==0.7.5
  Downloading pickleshare-0.7.5-py2.py3-none-any.whl (6.9 kB)
Collecting pluggy==0.6.0
  Downloading pluggy-0.6.0-py3-none-any.whl (13 kB)
Collecting prometheus-client==0.7.1
  Downloading prometheus_client-0.7.1.tar.gz (38 kB)
Collecting prompt-toolkit==2.0.10
  Downloading prompt_toolkit-2.0.10-py3-none-any.whl (340 kB)
Collecting ptyprocess==0.6.0
  Downloading ptyprocess-0.6.0-py2.py3-none-any.whl (39 kB)
Collecting py==1.8.0
  Downloading py-1.8.0-py2.py3-none-any.whl (83 kB)
Collecting pycodestyle==2.5.0
  Downloading pycodestyle-2.5.0-py2.py3-none-any.whl (51 kB)
Collecting pycparser==2.19
  Downloading pycparser-2.19.tar.gz (158 kB)
Collecting pyflakes==2.1.1
  Downloading pyflakes-2.1.1-py2.py3-none-any.whl (59 kB)
Collecting Pygments==2.4.2
  Downloading Pygments-2.4.2-py2.py3-none-any.whl (883 kB)
Collecting PyJWT==1.7.1
  Downloading PyJWT-1.7.1-py2.py3-none-any.whl (18 kB)
Collecting pymongo==3.7.2
  Downloading pymongo-3.7.2.tar.gz (628 kB)
Collecting pyrsistent==0.15.4
  Downloading pyrsistent-0.15.4.tar.gz (107 kB)
Collecting pytest==3.3.0
  Downloading pytest-3.3.0-py2.py3-none-any.whl (184 kB)
Collecting pytest-flask==0.11.0
  Downloading pytest_flask-0.11.0-py2.py3-none-any.whl (7.2 kB)
Collecting python-dateutil==2.8.0
  Downloading python_dateutil-2.8.0-py2.py3-none-any.whl (226 kB)
Collecting pyzmq==18.1.0
  Downloading pyzmq-18.1.0.tar.gz (1.2 MB)
Collecting qtconsole==4.5.5
  Downloading qtconsole-4.5.5-py2.py3-none-any.whl (121 kB)
Collecting Send2Trash==1.5.0
  Downloading Send2Trash-1.5.0-py3-none-any.whl (12 kB)
Collecting six==1.12.0
  Downloading six-1.12.0-py2.py3-none-any.whl (10 kB)
Collecting terminado==0.8.2
  Downloading terminado-0.8.2-py2.py3-none-any.whl (33 kB)
Collecting testpath==0.4.2
  Downloading testpath-0.4.2-py2.py3-none-any.whl (163 kB)
Collecting text-unidecode==1.2
  Downloading text_unidecode-1.2-py2.py3-none-any.whl (77 kB)
Collecting tornado==6.0.3
  Downloading tornado-6.0.3.tar.gz (482 kB)
Collecting traitlets==4.3.3
  Downloading traitlets-4.3.3-py2.py3-none-any.whl (75 kB)
Collecting wcwidth==0.1.7
  Downloading wcwidth-0.1.7-py2.py3-none-any.whl (21 kB)
Collecting webencodings==0.5.1
  Downloading webencodings-0.5.1-py2.py3-none-any.whl (11 kB)
Collecting Werkzeug==0.16.0
  Downloading Werkzeug-0.16.0-py2.py3-none-any.whl (327 kB)
Collecting widgetsnbextension==3.5.1
  Downloading widgetsnbextension-3.5.1-py2.py3-none-any.whl (2.2 MB)
Collecting zipp==0.6.0
  Downloading zipp-0.6.0-py2.py3-none-any.whl (4.1 kB)
Requirement already satisfied: setuptools>=18.5 in /usr/local/lib/python3.9/site-packages (from ipython==7.8.0->-r requirements.txt (line 21)) (57.5.0)
Collecting packaging
  Downloading packaging-21.0-py3-none-any.whl (40 kB)
Collecting Flask>=0.12.4
  Downloading Flask-2.0.0-py3-none-any.whl (93 kB)
  Downloading Flask-1.1.4-py2.py3-none-any.whl (94 kB)
Collecting pyparsing>=2.0.2
  Downloading pyparsing-2.4.7-py2.py3-none-any.whl (67 kB)
Building wheels for collected packages: backcall, cffi, Flask-Bcrypt, Flask-JWT-Extended, pandocfilters, prometheus-client, pycparser, pymongo, pyrsistent, pyzmq, tornado
  Building wheel for backcall (setup.py): started
  Building wheel for backcall (setup.py): finished with status 'done'
  Created wheel for backcall: filename=backcall-0.1.0-py3-none-any.whl size=10413 sha256=b4835a817ffdf7ed773dc9babaa9ed4974e0d46ca0cd5319e09ee4d630f38e6d
  Stored in directory: /root/.cache/pip/wheels/60/7f/64/5dfcb954945e78249c8b21cfce3e6174070243ae486f952e61
  Building wheel for cffi (setup.py): started
  Building wheel for cffi (setup.py): finished with status 'done'
  Created wheel for cffi: filename=cffi-1.13.1-cp39-cp39-linux_x86_64.whl size=413000 sha256=44aa8f43ae6254846fe8ce4d5cc57943347b512ead75f274fc55c12f61cd9480
  Stored in directory: /root/.cache/pip/wheels/1c/d4/cf/5ff21a378f5f301e2180f726e75d28d06fea815b7b9fdc19a9
  Building wheel for Flask-Bcrypt (setup.py): started
  Building wheel for Flask-Bcrypt (setup.py): finished with status 'done'
  Created wheel for Flask-Bcrypt: filename=Flask_Bcrypt-0.7.1-py3-none-any.whl size=5030 sha256=9c797bf6c88a06e81c117440741d3d162ae9416b5f75a9931f412259e9e8047a
  Stored in directory: /root/.cache/pip/wheels/46/c7/4d/b94ab085c8bb76ffcb87b41efbe5919f59292134b018fa0d57
  Building wheel for Flask-JWT-Extended (setup.py): started
  Building wheel for Flask-JWT-Extended (setup.py): finished with status 'done'
  Created wheel for Flask-JWT-Extended: filename=Flask_JWT_Extended-3.7.0-py2.py3-none-any.whl size=16843 sha256=324112b25f5e70ffe7324e8e74cee266f4d195c29b979de79977064e9323993c
  Stored in directory: /root/.cache/pip/wheels/41/19/e2/d7e86ddfd14151afa8938ca244d41e15ebcdcfce8198f56704
  Building wheel for pandocfilters (setup.py): started
  Building wheel for pandocfilters (setup.py): finished with status 'done'
  Created wheel for pandocfilters: filename=pandocfilters-1.4.2-py3-none-any.whl size=7871 sha256=9e58cb083ff593d570c7c266d937f5952ad71200ee77d12edcdd31835e55876d
  Stored in directory: /root/.cache/pip/wheels/ae/2a/6b/187c1f3132b28c9c67c1fd451c4a597696fcb95fdd5d70cfdf
  Building wheel for prometheus-client (setup.py): started
  Building wheel for prometheus-client (setup.py): finished with status 'done'
  Created wheel for prometheus-client: filename=prometheus_client-0.7.1-py3-none-any.whl size=41404 sha256=031ff37cd296f6a0a0400867d0f2963a451e740b96c03717906ac9326d81af90
  Stored in directory: /root/.cache/pip/wheels/fc/9b/86/f1eb31f154b2db5de1c46d38e367c7178f6f9715beb3e82479
  Building wheel for pycparser (setup.py): started
  Building wheel for pycparser (setup.py): finished with status 'done'
  Created wheel for pycparser: filename=pycparser-2.19-py2.py3-none-any.whl size=111051 sha256=ed6e7cded9f5ababa2b57bbe12ef91732c09d672c273ce21991c841c5b1fb9d0
  Stored in directory: /root/.cache/pip/wheels/4c/33/cc/4f98d7defeaadac79c493a4343d33e2317f68f52b33115569b
  Building wheel for pymongo (setup.py): started
  Building wheel for pymongo (setup.py): finished with status 'done'
  Created wheel for pymongo: filename=pymongo-3.7.2-cp39-cp39-linux_x86_64.whl size=427681 sha256=a74623b2dc99a62e868a506eff1c5365015ce7ed1e399cc0a48a192fa64b725a
  Stored in directory: /root/.cache/pip/wheels/f5/09/ef/63aed9051effc647dde06bf22a2ff0c8537a0bdae2dde72121
  Building wheel for pyrsistent (setup.py): started
  Building wheel for pyrsistent (setup.py): finished with status 'done'
  Created wheel for pyrsistent: filename=pyrsistent-0.15.4-cp39-cp39-linux_x86_64.whl size=115449 sha256=f1a9f09371a1b055c76028243121d1e7355e69e93901cbdf19906eb056dc0231
  Stored in directory: /root/.cache/pip/wheels/00/e0/f2/9f5f7789cda866d85293301a6c5fc83feb5efbdb903bd33b37
  Building wheel for pyzmq (setup.py): started
  Building wheel for pyzmq (setup.py): still running...
  Building wheel for pyzmq (setup.py): finished with status 'done'
  Created wheel for pyzmq: filename=pyzmq-18.1.0-cp39-cp39-linux_x86_64.whl size=6959816 sha256=0467a6662affd890db94e1b0612818371709669aa6b5b89b52b19a8191572db8
  Stored in directory: /root/.cache/pip/wheels/e6/5c/1f/d47eefd7a774d0f1b8d38a9cc2101e1d79534bc9291279dc62
  Building wheel for tornado (setup.py): started
  Building wheel for tornado (setup.py): finished with status 'done'
  Created wheel for tornado: filename=tornado-6.0.3-cp39-cp39-linux_x86_64.whl size=417867 sha256=5dbaea8a6aad6fe4564a8b0e648c80c34e5e89d02506790f425b601d7a5a2198
  Stored in directory: /root/.cache/pip/wheels/09/6a/bf/43222f8768d509dcbd092c4a6ae0b71904bcece141a59715f3
Successfully built backcall cffi Flask-Bcrypt Flask-JWT-Extended pandocfilters prometheus-client pycparser pymongo pyrsistent pyzmq tornado
Installing collected packages: more-itertools, zipp, six, ipython-genutils, decorator, wcwidth, traitlets, pyrsistent, pyparsing, ptyprocess, parso, importlib-metadata, attrs, webencodings, tornado, pyzmq, python-dateutil, Pygments, prompt-toolkit, pickleshare, pexpect, packaging, MarkupSafe, jupyter-core, jsonschema, jedi, backcall, testpath, pandocfilters, nbformat, mistune, jupyter-client, Jinja2, ipython, entrypoints, defusedxml, bleach, terminado, Send2Trash, prometheus-client, nbconvert, ipykernel, pycparser, notebook, widgetsnbextension, Werkzeug, py, pluggy, itsdangerous, Click, cffi, text-unidecode, qtconsole, pytest, PyJWT, pyflakes, pycodestyle, mccabe, jupyter-console, ipywidgets, Flask, bcrypt, pytest-flask, pymongo, jupyter, Flask-Login, Flask-JWT-Extended, Flask-Cors, Flask-Bcrypt, flake8, Faker, dnspython, appnope
Successfully installed Click-7.0 Faker-0.8.13 Flask-1.1.4 Flask-Bcrypt-0.7.1 Flask-Cors-3.0.3 Flask-JWT-Extended-3.7.0 Flask-Login-0.4.0 Jinja2-2.10.3 MarkupSafe-1.1.1 PyJWT-1.7.1 Pygments-2.4.2 Send2Trash-1.5.0 Werkzeug-0.16.0 appnope-0.1.0 attrs-19.1.0 backcall-0.1.0 bcrypt-3.1.7 bleach-4.1.0 cffi-1.13.1 decorator-4.4.0 defusedxml-0.6.0 dnspython-1.15.0 entrypoints-0.3 flake8-3.7.8 importlib-metadata-0.23 ipykernel-5.1.3 ipython-7.8.0 ipython-genutils-0.2.0 ipywidgets-7.5.1 itsdangerous-1.1.0 jedi-0.15.1 jsonschema-3.1.1 jupyter-1.0.0 jupyter-client-5.3.1 jupyter-console-6.0.0 jupyter-core-4.4.0 mccabe-0.6.1 mistune-0.8.4 more-itertools-7.2.0 nbconvert-5.6.0 nbformat-4.4.0 notebook-6.0.1 packaging-21.0 pandocfilters-1.4.2 parso-0.5.1 pexpect-4.7.0 pickleshare-0.7.5 pluggy-0.6.0 prometheus-client-0.7.1 prompt-toolkit-2.0.10 ptyprocess-0.6.0 py-1.8.0 pycodestyle-2.5.0 pycparser-2.19 pyflakes-2.1.1 pymongo-3.7.2 pyparsing-2.4.7 pyrsistent-0.15.4 pytest-3.3.0 pytest-flask-0.11.0 python-dateutil-2.8.0 pyzmq-18.1.0 qtconsole-4.5.5 six-1.12.0 terminado-0.8.2 testpath-0.4.2 text-unidecode-1.2 tornado-6.0.3 traitlets-4.3.3 wcwidth-0.1.7 webencodings-0.5.1 widgetsnbextension-3.5.1 zipp-0.6.0
WARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv
Removing intermediate container 4376d2d2b4b5
 ---> 0b85be451ae0
Step 5/6 : EXPOSE 5000
 ---> Running in ffe29bcd20ad
Removing intermediate container ffe29bcd20ad
 ---> 61963271bd51
Step 6/6 : CMD [ "python3", "run.py" ]
 ---> Running in 66b0a5e87c49
Removing intermediate container 66b0a5e87c49
 ---> 5f99f47aff66
Successfully built 5f99f47aff66
Successfully tagged obmovieimage:latest

```


3. Verified if the images are created correctly
```
docker images
REPOSITORY     TAG       IMAGE ID       CREATED          SIZE
obmovieimage   latest    5f99f47aff66   14 seconds ago   1.17GB
python         3         a5210955ee89   2 weeks ago      911MB

```

4. Executed the image to verify its running correctly

```
docker run -t -i -d -p 5000:5000 obmovieimage
969715082c2f59ca84bb9f41291adffaba5112b119db6c11f2e19a540a0638e7
[root@ip-172-31-20-248 obmovieassignment]# docker ps
CONTAINER ID   IMAGE          COMMAND            CREATED         STATUS         PORTS                                       NAMES
969715082c2f   obmovieimage   "python3 run.py"   3 seconds ago   Up 2 seconds   0.0.0.0:5000->5000/tcp, :::5000->5000/tcp   happy_williamson
[root@ip-172-31-20-248 obmovieassignment]# docker logs -f 969715082c2f
 * Serving Flask app "obmovies.factory" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 135-341-489
103.208.71.106 - - [28/Sep/2021 10:36:22] "GET /status HTTP/1.1" 200 -
103.208.71.106 - - [28/Sep/2021 10:36:22] "GET /favicon.ico HTTP/1.1" 200 -
103.208.71.106 - - [28/Sep/2021 10:36:28] "GET /api/v1/movies/ HTTP/1.1" 200 -
103.208.71.106 - - [28/Sep/2021 10:36:30] "GET /api/v1/movies/countries?countries=Australia HTTP/1.1" 200 -
103.208.71.106 - - [28/Sep/2021 10:36:33] "GET /api/v1/movies/facet-search?cast=Denzel%20Washington&page=0 HTTP/1.1" 200 -
103.208.71.106 - - [28/Sep/2021 10:36:34] "POST /api/v1/user/register HTTP/1.1" 400 -
103.208.71.106 - - [28/Sep/2021 10:36:37] "GET /api/v1/movies/id/573a13a7f29313caabd1aa1f HTTP/1.1" 200 -

```

5. Access the application from outside, used port forwarding to connect to container and verified logs


***************************************************************************************************

## **Phase 4: Creating the repository and push images, create helm charts**

1. Created the AWS ECR repository using command below
```
aws ecr create-repository --repository-name devopsec-assignment-ecr --image-scanning-configuration scanOnPush=true --region us-east-2
{
    "repository": {
        "repositoryUri": "929644394706.dkr.ecr.us-east-2.amazonaws.com/devopsec-assignment-ecr",
        "imageScanningConfiguration": {
            "scanOnPush": true
        },
        "encryptionConfiguration": {
            "encryptionType": "AES256"
        },
        "registryId": "929644394706",
        "imageTagMutability": "MUTABLE",
        "repositoryArn": "arn:aws:ecr:us-east-2:929644394706:repository/devopsec-assignment-ecr",
        "repositoryName": "devopsec-assignment-ecr",
        "createdAt": 1632826592.0
    }
}

```
2. Tag the image and push it to the repo
```
docker tag obmovieimage:latest 929644394706.dkr.ecr.us-east-2.amazonaws.com/devopsec-assignment-ecr:obmovie
```

3. Perform the docker login

```
aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin 929644394706.dkr.ecr.us-east-2.amazonaws.com
WARNING! Your password will be stored unencrypted in /root/.docker/config.json.
Configure a credential helper to remove this warning. See
https://docs.docker.com/engine/reference/commandline/login/#credentials-store

Login Succeeded
```

4. Pushing  the image to repo

```
docker push 929644394706.dkr.ecr.us-east-2.amazonaws.com/devopsec-assignment-ecr:obmovie
The push refers to repository [929644394706.dkr.ecr.us-east-2.amazonaws.com/devopsec-assignment-ecr]
2d6b3f412323: Pushed
0913ad2bbaf2: Pushed
d1d5915c84e4: Pushed
45b0de752fd9: Pushed
78744c48c9d3: Pushed
6cb051b7bcc1: Pushed
7cf0f434f498: Pushed
8555e663f65b: Pushed
d00da3cd7763: Pushed
4e61e63529c2: Pushed
799760671c38: Pushed
obmovie: digest: sha256:dba73db3e9d37fc17ea746171020446de87fe42ad663358e52941282b16a6d80 size: 2643
```

***************************************************************************************************
## **Phase 5: Creating the Kubernetes object for the deployment, using helm charts**

1. Create helm templates

```
helm create obmovie
WARNING: Kubernetes configuration file is group-readable. This is insecure. Location: /root/.kube/config
WARNING: Kubernetes configuration file is world-readable. This is insecure. Location: /root/.kube/config
Creating obmovie

```

2. Modify the values.yaml and Chart.yaml for the Imagepath, Pull Policy, Ingress details and tag (Templates are uploaded under helmcart folder)

3. Installation of helm charts on EKS cluster

```

helm install obmovie obmovie/ --values obmovie/values.yaml
WARNING: Kubernetes configuration file is group-readable. This is insecure. Location: /root/.kube/config
WARNING: Kubernetes configuration file is world-readable. This is insecure. Location: /root/.kube/config
NAME: obmovie
LAST DEPLOYED: Tue Sep 28 17:14:06 2021
NAMESPACE: default
STATUS: deployed
REVISION: 1
NOTES:
1. Get the application URL by running these commands:
  export POD_NAME=$(kubectl get pods --namespace default -l "app.kubernetes.io/name=obmovie,app.kubernetes.io/instance=obmovie" -o jsonpath="{.items[0].metadata.name}")
  export CONTAINER_PORT=$(kubectl get pod --namespace default $POD_NAME -o jsonpath="{.spec.containers[0].ports[0].containerPort}")
  echo "Visit http://127.0.0.1:8080 to use your application"
  kubectl --namespace default port-forward $POD_NAME 8080:$CONTAINER_PORT

```

4. Validation of PODS using helm charts

```
kubectl get pods -n default
NAME                       READY   STATUS    RESTARTS   AGE
obmovie-58cb7d9d6b-rtjjl   0/1     Running   1          75s
[root@ip-172-31-20-248 obmovieassignment]# kubeclt logs -f obmovie-58cb7d9d6b-rtjjl -n default
-bash: kubeclt: command not found
[root@ip-172-31-20-248 obmovieassignment]# kubectl logs -f  obmovie-58cb7d9d6b-rtjjl -n default
 * Serving Flask app "obmovies.factory" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 320-245-633

```

5. Contents of values.yaml

```
cat values.yaml
# Default values for obmovie.
# This is a YAML-formatted file.
# Declare variables to be passed into your templates.

replicaCount: 1

image:
  repository: 929644394706.dkr.ecr.us-east-2.amazonaws.com/devopsec-assignment-ecr
  pullPolicy: IfNotPresent
  # Overrides the image tag whose default is the chart appVersion.
  tag: "obmovie"

imagePullSecrets: []
nameOverride: ""
fullnameOverride: ""

serviceAccount:
  # Specifies whether a service account should be created
  create: true
  # Annotations to add to the service account
  annotations: {}
  # The name of the service account to use.
  # If not set and create is true, a name is generated using the fullname template
  name: ""

podAnnotations: {}

podSecurityContext: {}
  # fsGroup: 2000

securityContext: {}
  # capabilities:
  #   drop:
  #   - ALL
  # readOnlyRootFilesystem: true
  # runAsNonRoot: true
  # runAsUser: 1000

service:
  type: ClusterIP
  port: 80

ingress:
  enabled: false
  className: ""
  annotations: {}
    # kubernetes.io/ingress.class: nginx
    # kubernetes.io/tls-acme: "true"
  hosts:
    - host: chart-example.local
      paths:
        - path: /
          pathType: ImplementationSpecific
  tls: []
  #  - secretName: chart-example-tls
  #    hosts:
  #      - chart-example.local

resources: {}
  # We usually recommend not to specify default resources and to leave this as a conscious
  # choice for the user. This also increases chances charts run on environments with little
  # resources, such as Minikube. If you do want to specify resources, uncomment the following
  # lines, adjust them as necessary, and remove the curly braces after 'resources:'.
  # limits:
  #   cpu: 100m
  #   memory: 128Mi
  # requests:
  #   cpu: 100m
  #   memory: 128Mi

autoscaling:
  enabled: false
  minReplicas: 1
  maxReplicas: 100
  targetCPUUtilizationPercentage: 80
  # targetMemoryUtilizationPercentage: 80

nodeSelector: {}

tolerations: []

affinity: {}

```

