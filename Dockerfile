FROM python:3.9
MAINTAINER wufan2019@126.com
WORKDIR /myApp/jenkins_home/workspace/flaskProject
COPY . /myApp/jenkins_home/workspace/flaskProject
RUN pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/ || echo "Error installing requirements"
EXPOSE 9091
CMD ["python3","app.py"]

