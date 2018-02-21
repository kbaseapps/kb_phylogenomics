FROM kbase/kbase:sdkbase.latest
MAINTAINER KBase Developer
# -----------------------------------------
# In this section, you can install any system dependencies required
# to run your App.  For instance, you could place an apt-get update or
# install line here, a git checkout to download code, or run any other
# installation scripts.

# Update certs
RUN apt-get update
RUN apt-get install ca-certificates

# Fix Python SSL warnings for python < 2.7.9 (system python on Trusty is 2.7.6)
# https://github.com/pypa/pip/issues/4098
RUN pip install pip==8.1.2
RUN pip install --disable-pip-version-check requests requests_toolbelt pyopenssl --upgrade


## update security libraries in the base image (deprecated approach)
#RUN pip install cffi --upgrade \
#    && pip install pyopenssl --upgrade \
#    && pip install ndg-httpsclient --upgrade \
#    && pip install pyasn1 --upgrade \
#    && pip install requests --upgrade \
#    && pip install 'requests[security]' --upgrade


# Here we install a python coverage tool and an
# https library that is out of date in the base image.
RUN pip install coverage


# Install ETE3
RUN apt-get update && \
    apt-get -y install xvfb python-qt4 && \
    pip install ete3==3.0.0b35

# -----------------------------------------

COPY ./ /kb/module
RUN mkdir -p /kb/module/work
RUN chmod -R a+rw /kb/module

WORKDIR /kb/module

RUN make all

ENTRYPOINT [ "./scripts/entrypoint.sh" ]

CMD [ ]
