FROM kbase/kbase:sdkbase.latest
MAINTAINER KBase Developer
# -----------------------------------------

# RUN apt-get update
RUN pip install coverage

# -----------------------------------------

COPY ./ /kb/module
RUN mkdir -p /kb/module/work
RUN chmod 777 /kb/module

WORKDIR /kb/module

RUN make all

# Install Minconda  (you can ignore this step if you already have Anaconda/Miniconda)
#
##wget http://repo.continuum.io/miniconda/Miniconda-latest-Linux-x86_64.sh -O Miniconda-latest-Linux-x86_64.sh
RUN curl https://repo.continuum.io/miniconda/Miniconda2-latest-Linux-x86_64.sh -o Miniconda2-latest-Linux-x86_64.sh && \
    bash Miniconda2-latest-Linux-x86_64.sh -b -p /kb/module/anaconda_ete/
RUN export PATH=/kb/module/anaconda_ete/bin:$PATH
#RUN echo "export PATH=/kb/module/anaconda_ete/bin:$PATH" >> ~/.profile  # DOESN'T WORK
RUN echo "export PATH=/kb/module/anaconda_ete/bin:$PATH" >> ~/.bashrc  # WORKS

# Install X11 (for ETE)
RUN sudo apt-get -y --fix-missing install xorg openbox
RUN echo "/etc/init.d/x11-common start" >> ~/.bashrc

# Install ETE
RUN /kb/module/anaconda_ete/bin/conda install -c etetoolkit ete3 ete3_external_apps
RUN /kb/module/anaconda_ete/bin/ete3 version
#RUN /kb/module/anaconda_ete/bin/ete3 build check  # breaks without path, which I haven't fixed yet




ENTRYPOINT [ "./scripts/entrypoint.sh" ]

CMD [ ]
