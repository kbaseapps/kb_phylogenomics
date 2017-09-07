# -*- coding: utf-8 -*-
import unittest
import os  # noqa: F401
import json  # noqa: F401
import time
import shutil
import requests

from os import environ
try:
    from ConfigParser import ConfigParser  # py2
except:
    from configparser import ConfigParser  # py3

from pprint import pprint  # noqa: F401

#from biokbase.workspace.client import Workspace as workspaceService
from Workspace.WorkspaceClient import Workspace as workspaceService
from GenomeFileUtil.GenomeFileUtilClient import GenomeFileUtil
from kb_phylogenomics.kb_phylogenomicsImpl import kb_phylogenomics
from kb_phylogenomics.kb_phylogenomicsServer import MethodContext
from kb_phylogenomics.authclient import KBaseAuth as _KBaseAuth


class kb_phylogenomicsTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        token = environ.get('KB_AUTH_TOKEN', None)
        config_file = environ.get('KB_DEPLOYMENT_CONFIG', None)
        cls.cfg = {}
        config = ConfigParser()
        config.read(config_file)
        for nameval in config.items('kb_phylogenomics'):
            cls.cfg[nameval[0]] = nameval[1]
        authServiceUrl = cls.cfg.get('auth-service-url',
                "https://kbase.us/services/authorization/Sessions/Login")
        auth_client = _KBaseAuth(authServiceUrl)
        user_id = auth_client.get_user(token)
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

    # call this method to get the WS object info of a Genome
    #   (will upload the example data if this is the first time the method is called during tests)
    def getGenomeInfo(self, genome_basename, lib_i=0):
        if hasattr(self.__class__, 'genomeInfo_list'):
            try:
                info = self.__class__.genomeInfo_list[lib_i]
                name = self.__class__.genomeName_list[lib_i]
                if info != None:
                    if name != genome_basename:
                        self.__class__.genomeInfo_list[lib_i] = None
                        self.__class__.genomeName_list[lib_i] = None
                    else:
                        return info
            except:
                pass

        # 1) transform genbank to kbase genome object and upload to ws
        shared_dir = "/kb/module/work/tmp"
        genome_data_file = 'data/genomes/'+genome_basename+'.gbff'
        genome_file = os.path.join(shared_dir, os.path.basename(genome_data_file))
        shutil.copy(genome_data_file, genome_file)

        SERVICE_VER = 'release'
        #SERVICE_VER = 'dev'
        GFU = GenomeFileUtil(os.environ['SDK_CALLBACK_URL'],
                             token=self.getContext()['token'],
                             service_ver=SERVICE_VER
                         )
        print ("UPLOADING genome: "+genome_basename+" to WORKSPACE "+self.getWsName()+" ...")
        genome_upload_result = GFU.genbank_to_genome({'file': {'path': genome_file },
                                                      'workspace_name': self.getWsName(),
                                                      'genome_name': genome_basename
                                                  })
#                                                  })[0]
        pprint(genome_upload_result)
        genome_ref = genome_upload_result['genome_ref']
        new_obj_info = self.getWsClient().get_object_info_new({'objects': [{'ref': genome_ref}]})[0]

        # 2) store it
        if not hasattr(self.__class__, 'genomeInfo_list'):
            self.__class__.genomeInfo_list = []
            self.__class__.genomeName_list = []
        for i in range(lib_i+1):
            try:
                assigned = self.__class__.genomeInfo_list[i]
            except:
                self.__class__.genomeInfo_list.append(None)
                self.__class__.genomeName_list.append(None)

        self.__class__.genomeInfo_list[lib_i] = new_obj_info
        self.__class__.genomeName_list[lib_i] = genome_basename
        return new_obj_info


    ##############
    # UNIT TESTS #
    ##############



    ### Annotate domains in a GenomeSet
    def test_run_DomainAnnotation_Sets_01(self):
        method = 'run_DomainAnnotation_Sets'

        print ("\n\nRUNNING: test_"+method+"_01()")
        print ("==================================================\n\n")

        # input_data
        genomeInfo_0 = self.getGenomeInfo('GCF_000287295.1_ASM28729v1_genomic', 0)  # Candidatus Carsonella ruddii HT isolate Thao2000
        genomeInfo_1 = self.getGenomeInfo('GCF_000306885.1_ASM30688v1_genomic', 1)  # Wolbachia endosymbiont of Onchocerca ochengi
        genomeInfo_2 = self.getGenomeInfo('GCF_001439985.1_wTPRE_1.0_genomic',  2)  # Wolbachia endosymbiont of Trichogramma pretiosum
        genomeInfo_3 = self.getGenomeInfo('GCF_000022285.1_ASM2228v1_genomic',  3)  # Wolbachia sp. wRi

        genome_ref_0 = self.getWsName() + '/' + str(genomeInfo_0[0]) + '/' + str(genomeInfo_0[4])
        genome_ref_1 = self.getWsName() + '/' + str(genomeInfo_1[0]) + '/' + str(genomeInfo_1[4])
        genome_ref_2 = self.getWsName() + '/' + str(genomeInfo_2[0]) + '/' + str(genomeInfo_2[4])
        genome_ref_3 = self.getWsName() + '/' + str(genomeInfo_3[0]) + '/' + str(genomeInfo_3[4])

        #feature_id_0 = 'A355_RS00030'   # F0F1 ATP Synthase subunit B
        #feature_id_1 = 'WOO_RS00195'    # F0 ATP Synthase subunit B
        #feature_id_2 = 'AOR14_RS04755'  # F0 ATP Synthase subunit B
        #feature_id_3 = 'WRI_RS01560'    # F0 ATP Synthase subunit B

        genome_ref_list = [genome_ref_0, genome_ref_1]
        genome_scinames = dict()
        genome_objnames = dict()
        genome_refs_by_objname = dict()
        genome_scinames[genome_ref_0] = 'Candidatus Carsonella ruddii HT isolate Thao2000'
        genome_scinames[genome_ref_1] = 'Wolbachia endosymbiont of Onchocerca ochengi'
        for genome_ref in genome_ref_list: 
            try:
                [OBJID_I, NAME_I, TYPE_I, SAVE_DATE_I, VERSION_I, SAVED_BY_I, WSID_I, WORKSPACE_I, CHSUM_I, SIZE_I, META_I] = range(11)  # object_info tuple
                obj_info = self.getWsClient().get_object_info_new ({'objects':[{'ref':genome_ref}]})[0]
                obj_name = obj_info[NAME_I]
                genome_objnames[genome_ref] = obj_name
                genome_refs_by_objname[obj_name] = genome_ref
            except Exception as e:
                raise ValueError('Unable to get object from workspace: (' + genome_ref +')' + str(e))

        # build GenomeSet obj
        testGS = {
            'description': 'two genomes',
            'elements': dict()
        }
        for genome_ref in genome_ref_list: 
            testGS['elements'][genome_scinames[genome_ref]] = { 'ref': genome_ref }

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
                                                })[0]

        pprint(obj_info)

        # run annotateDomains
        params = {
            'workspace_name': self.getWsName(),
            'input_genomeSet_ref': str(obj_info[6])+'/'+str(obj_info[0]),
            'override_annot': 0
        }

        result = self.getImpl().run_DomainAnnotation_Sets(self.getContext(),params)
        print('RESULT:')
        pprint(result)

        # check the output DomainAnnotation objects to make sure all domain annotations are done
        domain_annot_done = dict()
        for ws_id in self.getWsName():
            try:
                dom_annot_obj_info_list = self.getWsClient().list_objects({'ids':[ws_id],'type':"KBaseGeneFamilies.DomainAnnotation"})
            except Exception as e:
                raise ValueError ("Unable to list DomainAnnotation objects from workspace: "+str(ws_id)+" "+str(e))

            for info in dom_annot_obj_info_list:
                [OBJID_I, NAME_I, TYPE_I, SAVE_DATE_I, VERSION_I, SAVED_BY_I, WSID_I, WORKSPACE_I, CHSUM_I, SIZE_I, META_I] = range(11)  # object_info tuple
                
                dom_annot_ref = str(info[WSID_I])+'/'+str(info[OBJID_I])+'/'+str(info[VERSION_I])
                try:
                    domain_data = self.getWsClient().get_objects2({'objects':[{'ref':dom_annot_ref}]})['data'][0]['data']
                except:
                    raise ValueError ("unable to fetch domain annotation: "+dom_annot_ref)

                # read domain data object
                this_genome_ref = domain_data['genome_ref']
                if this_genome_ref not in genome_ref_list:
                    continue
                domain_annot_done[this_genome_ref] = True

        self.assertEqual(len(domain_annot_done.keys()), genome_ref_list)
