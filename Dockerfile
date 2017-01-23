FROM kbase/kbase:sdkbase.latest
MAINTAINER KBase Developer
# -----------------------------------------

# Install Minconda  (you can ignore this step if you already have Anaconda/Miniconda)
##wget http://repo.continuum.io/miniconda/Miniconda-latest-Linux-x86_64.sh -O Miniconda-latest-Linux-x86_64.sh
RUN curl https://repo.continuum.io/miniconda/Miniconda2-latest-Linux-x86_64.sh -o Miniconda2-latest-Linux-x86_64.sh && \
    bash Miniconda2-latest-Linux-x86_64.sh -b -p ~/anaconda_ete/ && \
    export PATH=~/anaconda_ete/bin:$PATH

# Install ETE
RUN ~/anaconda_ete/bin/conda install -c etetoolkit ete3 ete3_external_apps && \
    ~/anaconda_ete/bin/ete3 version && \
    ~/anaconda_ete/bin/ete3 build check && \
    export PATH=~/anaconda_ete/bin:$PATH


# RUN apt-get update
RUN pip install coverage

# -----------------------------------------

COPY ./ /kb/module
RUN mkdir -p /kb/module/work
RUN chmod 777 /kb/module

WORKDIR /kb/module

RUN make all

ENTRYPOINT [ "./scripts/entrypoint.sh" ]

CMD [ ]
