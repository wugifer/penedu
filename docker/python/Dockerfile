FROM wg/centos
ADD python/pkg /pkg
ADD python/egg /egg
ADD python/nginx.conf /
RUN rpm -i /pkg/*.rpm \
    && rm -rf /pkg \
    && easy_install /egg/pip-9.0.1.tar.gz \
    && pip install --no-index --find-links=/egg \
        Django \
        Flask \
        gevent \
        pytest \
        pytest_cov \
        pytest_flask \
        sphinx \
    && rm -rf /egg \
    && mv /nginx.conf /etc/nginx/nginx.conf
EXPOSE 5000

# patch
RUN sed -i -e '/issame...self/s/issame.*/issame = True/' /usr/lib/python2.7/site-packages/py/_path/local.py

# CMD ["nginx", "-g", "daemon off;"]
CMD ["python", "/src/penedu/server/app.py"]

