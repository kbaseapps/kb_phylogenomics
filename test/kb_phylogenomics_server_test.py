# -*- coding: utf-8 -*-
import unittest
import os  # noqa: F401
import json  # noqa: F401
import time
import requests

from os import environ
try:
    from ConfigParser import ConfigParser  # py2
except:
    from configparser import ConfigParser  # py3

from pprint import pprint  # noqa: F401

from biokbase.workspace.client import Workspace as workspaceService
from kb_phylogenomics.kb_phylogenomicsImpl import kb_phylogenomics
from kb_phylogenomics.kb_phylogenomicsServer import MethodContext


class kb_phylogenomicsTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        token = environ.get('KB_AUTH_TOKEN', None)
        user_id = requests.post(
            'https://kbase.us/services/authorization/Sessions/Login',
            data='token={}&fields=user_id'.format(token)).json()['user_id']
        # WARNING: don't call any logging methods on the context object,
        # it'll result in a NoneType error
        cls.ctx = MethodContext(None)
        cls.ctx.update({'token': token,
                        'user_id': user_id,
                        'provenance': [
                            {'service': 'kb_phylogenomics',
                             'method': 'please_never_use_it_in_production',
                             'method_params': []
                             }],
                        'authenticated': 1})
        config_file = environ.get('KB_DEPLOYMENT_CONFIG', None)
        cls.cfg = {}
        config = ConfigParser()
        config.read(config_file)
        for nameval in config.items('kb_phylogenomics'):
            cls.cfg[nameval[0]] = nameval[1]
        cls.wsURL = cls.cfg['workspace-url']
        cls.wsClient = workspaceService(cls.wsURL, token=token)
        cls.serviceImpl = kb_phylogenomics(cls.cfg)

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'wsName'):
            cls.wsClient.delete_workspace({'workspace': cls.wsName})
            print('Test workspace was deleted')

    def getWsClient(self):
        return self.__class__.wsClient

    def getWsName(self):
        if hasattr(self.__class__, 'wsName'):
            return self.__class__.wsName
        suffix = int(time.time() * 1000)
        wsName = "test_kb_phylogenomics_" + str(suffix)
        ret = self.getWsClient().create_workspace({'workspace': wsName})  # noqa
        self.__class__.wsName = wsName
        return wsName

    def getImpl(self):
        return self.__class__.serviceImpl

    def getContext(self):
        return self.__class__.ctx

    # NOTE: According to Python unittest naming rules test method names should start from 'test'. # noqa
    def test_your_method(self):
        # Prepare test objects in workspace if needed using
        # self.getWsClient().save_objects({'workspace': self.getWsName(),
        #                                  'objects': []})
        #
        # Run your method by
        # ret = self.getImpl().your_method(self.getContext(), parameters...)
        #
        # Check returned data with
        # self.assertEqual(ret[...], ...) or other unittest methods
        pass


    ### Annotate domains in a GenomeSet
    def test_annotateDomains(self):

        # make a simple GenomeSet that refers to two public Genomes
        # kb|g.371 is Shewanella MR-1
        # kb|g.3562 is DvH
        testGS = {
            'description': 'two genomes',
            'elements': {
                'so': {
                    'ref': '4258/35060/1'
                },
                'dvh': {
                    'ref': '4258/34734/1'
                }
            }
        }

        obj_info = self.getWsClient().save_objects({'workspace': self.getWsName(),       
                                                    'objects': [
                                                        {
                                                            'type':'KBaseSearch.GenomeSet',
                                                            'data':testGS,
                                                            'name':'test_genomeset',
                                                            'meta':{},
                                                            'provenance':[
                                                                {
                                                                    'service':'kb_phylogenomics',
                                                                    'method':'test_annotateDomains'
                                                                }
                                                            ]
                                                        }]
                                                })

        pprint(obj_info)

        # run annotateDomains
        params = {
            'workspace_name': self.getWsName(),
            'input_genomeSet_ref': str(obj_info[0][6])+'/'+str(obj_info[0][0]),
            'override_annot': 0
        }

        result = self.getImpl().run_DomainAnnotation_Sets(self.getContext(),params)
        print('RESULT:')
        pprint(result)

