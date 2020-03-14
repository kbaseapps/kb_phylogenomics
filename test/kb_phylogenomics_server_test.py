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

from installed_clients.WorkspaceClient import Workspace as workspaceService
from installed_clients.GenomeFileUtilClient import GenomeFileUtil
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


    # call this method to get the WS object info of a DomainAnnotation
    #   (will upload the example data if this is the first time the method is called during tests)
    def getDomainInfo(self, domain_basename, lib_i=0, genome_ref=None):
        if hasattr(self.__class__, 'domainInfo_list'):
            try:
                info = self.__class__.domainInfo_list[lib_i]
                name = self.__class__.domainName_list[lib_i]
                if info != None:
                    if name != domain_basename:
                        self.__class__.domainInfo_list[lib_i] = None
                        self.__class__.domainName_list[lib_i] = None
                    else:
                        return info
            except:
                pass

        # 1) transform json to kbase DomainAnnotation object and upload to ws
        shared_dir = "/kb/module/work/tmp"
        domain_data_file = 'data/domains/'+domain_basename+'.json'
        domain_file = os.path.join(shared_dir, os.path.basename(domain_data_file))
        shutil.copy(domain_data_file, domain_file)

        # create object
        with open (domain_file, 'r', 0) as domain_fh:
            domain_obj = json.load(domain_fh)

        domain_obj['used_dms_ref'] = 'KBasePublicGeneDomains/All'
        if genome_ref != None:
            domain_obj['genome_ref'] = genome_ref

        provenance = [{}]
        new_obj_info = self.getWsClient().save_objects({
            'workspace': self.getWsName(), 
            'objects': [
                {
                    'type': 'KBaseGeneFamilies.DomainAnnotation',
                    'data': domain_obj,
                    'name': domain_basename+'.test_DOMAINS',
                    'meta': {},
                    'provenance': provenance
                }
            ]})[0]

        # 2) store it
        if not hasattr(self.__class__, 'domainInfo_list'):
            self.__class__.domainInfo_list = []
            self.__class__.domainName_list = []
        for i in range(lib_i+1):
            try:
                assigned = self.__class__.domainInfo_list[i]
            except:
                self.__class__.domainInfo_list.append(None)
                self.__class__.domainName_list.append(None)

        self.__class__.domainInfo_list[lib_i] = new_obj_info
        self.__class__.domainName_list[lib_i] = domain_basename
        return new_obj_info


    # call this method to get the WS object info of a Tree
    #   (will upload the example data if this is the first time the method is called during tests)
    def getTreeInfo(self, tree_basename, lib_i=0, genome_ref_map=None):
        if hasattr(self.__class__, 'treeInfo_list'):
            try:
                info = self.__class__.treeInfo_list[lib_i]
                name = self.__class__.treeName_list[lib_i]
                if info != None:
                    if name != tree_basename:
                        self.__class__.treeInfo_list[lib_i] = None
                        self.__class__.treeName_list[lib_i] = None
                    else:
                        return info
            except:
                pass

        # 1) transform json to kbase Tree object and upload to ws
        shared_dir = "/kb/module/work/tmp"
        tree_data_file = 'data/trees/'+tree_basename+'.json'
        tree_file = os.path.join(shared_dir, os.path.basename(tree_data_file))
        shutil.copy(tree_data_file, tree_file)

        # create object
        with open (tree_file, 'r', 0) as tree_fh:
            tree_obj = json.load(tree_fh)

        # update genome_refs
        if genome_ref_map != None:
            for label_id in tree_obj['default_node_labels']:
                for old_genome_ref in genome_ref_map.keys():
                    tree_obj['default_node_labels'][label_id] = tree_obj['default_node_labels'][label_id].replace(old_genome_ref, genome_ref_map[old_genome_ref])
            for label_id in tree_obj['ws_refs'].keys():
                new_genome_refs = []
                for old_genome_ref in tree_obj['ws_refs'][label_id]['g']:
                    new_genome_refs.append(genome_ref_map[old_genome_ref])
                tree_obj['ws_refs'][label_id]['g'] = new_genome_refs

        provenance = [{}]
        new_obj_info = self.getWsClient().save_objects({
            'workspace': self.getWsName(), 
            'objects': [
                {
                    'type': 'KBaseTrees.Tree',
                    'data': tree_obj,
                    'name': tree_basename+'.test_TREE',
                    'meta': {},
                    'provenance': provenance
                }
            ]})[0]

        # 2) store it
        if not hasattr(self.__class__, 'treeInfo_list'):
            self.__class__.treeInfo_list = []
            self.__class__.treeName_list = []
        for i in range(lib_i+1):
            try:
                assigned = self.__class__.treeInfo_list[i]
            except:
                self.__class__.treeInfo_list.append(None)
                self.__class__.treeName_list.append(None)

        self.__class__.treeInfo_list[lib_i] = new_obj_info
        self.__class__.treeName_list[lib_i] = tree_basename
        return new_obj_info


    # call this method to get the WS object info of a Pangenome obj
    #   (will upload the example data if this is the first time the method is called during tests)
    def getPangenomeInfo(self, pan_basename, lib_i=0, genome_ref_map=None):
        if hasattr(self.__class__, 'panInfo_list'):
            try:
                info = self.__class__.panInfo_list[lib_i]
                name = self.__class__.panName_list[lib_i]
                if info != None:
                    if name != pan_basename:
                        self.__class__.panInfo_list[lib_i] = None
                        self.__class__.panName_list[lib_i] = None
                    else:
                        return info
            except:
                pass

        # 1) transform json to kbase Pangenome object and upload to ws
        shared_dir = "/kb/module/work/tmp"
        pan_data_file = 'data/pangenomes/'+pan_basename+'.json'
        pan_file = os.path.join(shared_dir, os.path.basename(pan_data_file))
        shutil.copy(pan_data_file, pan_file)

        # create object
        with open (pan_file, 'r', 0) as pan_fh:
            pan_obj = json.load(pan_fh)

        # update genome_refs
        if genome_ref_map != None:
            # basic list of genome_refs
            new_genome_refs = []
            for old_genome_ref in pan_obj['genome_refs']:
                new_genome_refs.append(genome_ref_map[old_genome_ref])
            pan_obj['genome_refs'] = new_genome_refs

            # fix genome refs embedded in ortholog clusters
            GENOME_REF_I = 2
            for clust_i, clust in enumerate(pan_obj['orthologs']):
                for ortholog_i,ortholog in enumerate(pan_obj['orthologs'][clust_i]['orthologs']):
                    old_genome_ref = pan_obj['orthologs'][clust_i]['orthologs'][ortholog_i][GENOME_REF_I]
                    pan_obj['orthologs'][clust_i]['orthologs'][ortholog_i][GENOME_REF_I] = genome_ref_map[old_genome_ref]

        provenance = [{}]
        new_obj_info = self.getWsClient().save_objects({
            'workspace': self.getWsName(), 
            'objects': [
                {
                    'type': 'KBaseGenomes.Pangenome',
                    'data': pan_obj,
                    'name': pan_basename+'.test_PANGENOME',
                    'meta': {},
                    'provenance': provenance
                }
            ]})[0]

        # 2) store it
        if not hasattr(self.__class__, 'panInfo_list'):
            self.__class__.panInfo_list = []
            self.__class__.panName_list = []
        for i in range(lib_i+1):
            try:
                assigned = self.__class__.panInfo_list[i]
            except:
                self.__class__.panInfo_list.append(None)
                self.__class__.panName_list.append(None)

        self.__class__.panInfo_list[lib_i] = new_obj_info
        self.__class__.panName_list[lib_i] = pan_basename
        return new_obj_info


    ##############
    # UNIT TESTS #
    ##############

    #### Annotate domains in a GenomeSet
    ##
    # HIDE @unittest.skip("skipped test_run_DomainAnnotation_Sets_01()")  # uncomment to skip
    def test_run_DomainAnnotation_Sets_01_GenomeSet(self):
        method = 'run_DomainAnnotation_Sets'

        print ("\n\nRUNNING: test_"+method+"_01_GenomeSet()")
        print ("==================================================\n\n")

        # input_data
        genomeInfo_0 = self.getGenomeInfo('GCF_000287295.1_ASM28729v1_genomic', 0)  # Candidatus Carsonella ruddii HT isolate Thao2000
        genomeInfo_1 = self.getGenomeInfo('GCF_000306885.1_ASM30688v1_genomic', 1)  # Wolbachia endosymbiont of Onchocerca ochengi
#        genomeInfo_2 = self.getGenomeInfo('GCF_001439985.1_wTPRE_1.0_genomic',  2)  # Wolbachia endosymbiont of Trichogramma pretiosum
#        genomeInfo_3 = self.getGenomeInfo('GCF_000022285.1_ASM2228v1_genomic',  3)  # Wolbachia sp. wRi

        genome_ref_0 = self.getWsName() + '/' + str(genomeInfo_0[0]) + '/' + str(genomeInfo_0[4])
        genome_ref_1 = self.getWsName() + '/' + str(genomeInfo_1[0]) + '/' + str(genomeInfo_1[4])
#        genome_ref_2 = self.getWsName() + '/' + str(genomeInfo_2[0]) + '/' + str(genomeInfo_2[4])
#        genome_ref_3 = self.getWsName() + '/' + str(genomeInfo_3[0]) + '/' + str(genomeInfo_3[4])

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
        for ws_id in [self.getWsName()]:
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


    #### Annotate domains in a GenomeSet
    ##
    # HIDE @unittest.skip("skipped test_run_DomainAnnotation_Sets_02_SpeciesTree()")  # uncomment to skip
    def test_run_DomainAnnotation_Sets_02_SpeciesTree(self):
        method = 'run_DomainAnnotation_Sets'

        print ("\n\nRUNNING: test_"+method+"_02_SpeciesTree()")
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

        # upload Tree
        genome_refs_map = { '23880/3/1': genome_ref_0,
                            '23880/4/1': genome_ref_1,
                            '23880/5/1': genome_ref_2,
                            '23880/6/1': genome_ref_3
                        }
        obj_info = self.getTreeInfo('Tiny_things.SpeciesTree', 0, genome_refs_map)
        [OBJID_I, NAME_I, TYPE_I, SAVE_DATE_I, VERSION_I, SAVED_BY_I, WSID_I, WORKSPACE_I, CHSUM_I, SIZE_I, META_I] = range(11)  # object_info tuple
        tree_ref = str(obj_info[WSID_I])+'/'+str(obj_info[OBJID_I])+'/'+str(obj_info[VERSION_I])

        #feature_id_0 = 'A355_RS00030'   # F0F1 ATP Synthase subunit B
        #feature_id_1 = 'WOO_RS00195'    # F0 ATP Synthase subunit B
        #feature_id_2 = 'AOR14_RS04755'  # F0 ATP Synthase subunit B
        #feature_id_3 = 'WRI_RS01560'    # F0 ATP Synthase subunit B

        # run annotateDomains
        params = {
            'workspace_name': self.getWsName(),
            'input_genomeSet_ref': tree_ref,
            'override_annot': 0
        }

        result = self.getImpl().run_DomainAnnotation_Sets(self.getContext(),params)
        print('RESULT:')
        pprint(result)

        # check the output DomainAnnotation objects to make sure all domain annotations are done
        domain_annot_done = dict()
        for ws_id in [self.getWsName()]:
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


    #### View Fxn Profile for GenomeSet
    ##
    # HIDE @unittest.skip("skipped test_view_fxn_profile_01()")  # uncomment to skip
    def test_view_fxn_profile_01(self):
        method = 'view_fxn_profile'

        print ("\n\nRUNNING: test_"+method+"_01()")
        print ("==================================================\n\n")

        # input_data
        genomeInfo_0 = self.getGenomeInfo('GCF_000287295.1_ASM28729v1_genomic', 0)  # Candidatus Carsonella ruddii HT isolate Thao2000
        genomeInfo_1 = self.getGenomeInfo('GCF_000306885.1_ASM30688v1_genomic', 1)  # Wolbachia endosymbiont of Onchocerca ochengi
#        genomeInfo_2 = self.getGenomeInfo('GCF_001439985.1_wTPRE_1.0_genomic',  2)  # Wolbachia endosymbiont of Trichogramma pretiosum
#        genomeInfo_3 = self.getGenomeInfo('GCF_000022285.1_ASM2228v1_genomic',  3)  # Wolbachia sp. wRi

        genome_ref_0 = self.getWsName() + '/' + str(genomeInfo_0[0]) + '/' + str(genomeInfo_0[4])
        genome_ref_1 = self.getWsName() + '/' + str(genomeInfo_1[0]) + '/' + str(genomeInfo_1[4])
#        genome_ref_2 = self.getWsName() + '/' + str(genomeInfo_2[0]) + '/' + str(genomeInfo_2[4])
#        genome_ref_3 = self.getWsName() + '/' + str(genomeInfo_3[0]) + '/' + str(genomeInfo_3[4])

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
                                                            'name':method+'.test_genomeset',
                                                            'meta':{},
                                                            'provenance':[
                                                                {
                                                                    'service':'kb_phylogenomics',
                                                                    'method':'test_view_fxn_profile'
                                                                }
                                                            ]
                                                        }]
                                                })[0]

        pprint(obj_info)
        [OBJID_I, NAME_I, TYPE_I, SAVE_DATE_I, VERSION_I, SAVED_BY_I, WSID_I, WORKSPACE_I, CHSUM_I, SIZE_I, META_I] = range(11)  # object_info tuple
        genomeSet_ref = str(obj_info[WSID_I])+'/'+str(obj_info[OBJID_I])+'/'+str(obj_info[VERSION_I])

        # get annotated domains
        domain_info_0 = self.getDomainInfo('Carsonella.Domains', 0, genome_ref_0)
        domain_info_1 = self.getDomainInfo('Wolbachia_ochengi.Domains', 1, genome_ref_1)
#        domain_info_2 = self.getDomainInfo('Wolbachia_pretiosum.Domains', 2, genome_ref_2)
#        domain_info_3 = self.getDomainInfo('Wolbachia_sp.wRi.Domains', 3, genome_ref_3)


        # run that sucker
        params = { 'workspace_name': self.getWsName(),
                   'custom_target_fams': { 'target_fams': ['COG0001','COG0002'],
                                           'extra_target_fam_groups_COG':  ["COG: N: Cell motility"],
                                           'extra_target_fam_groups_PFAM': ["PF: Clan CL0003: SAM"],
                                           'extra_target_fam_groups_TIGR': ["TIGR: role:11010: Aromatic amino acid family "],
                                           #'extra_target_fam_groups_SEED': ["SEED: Alanine_biosynthesis"]
                                           'extra_target_fam_groups_SEED': []
                                       },
                   'input_genomeSet_ref': genomeSet_ref,
                   'namespace': 'custom',
                   'genome_disp_name_config': "obj_name_ver_sci_name",
                   'count_category': "perc_annot",
                   'heatmap': "1",
                   'vertical': "1",
                   'top_hit': "1",
                   'e_value': "0.001",
                   'log_base': "",
                   'required_COG_annot_perc': "10",
                   'required_TIGR_annot_perc': "10",
                   'required_PFAM_annot_perc': "10",
                   'required_SEED_annot_perc': "33",
                   'count_hypothetical': "0",
                   'show_blanks': "0",
                   'skip_missing_genomes': "0",
                   'enforce_genome_version_match': "0"
               }
        ret = self.getImpl().view_fxn_profile(self.getContext(),params)[0]
        self.assertIsNotNone(ret['report_ref'])

        # check created obj
        #report_obj = self.getWsClient().get_objects2({'objects':[{'ref':ret['report_ref']}]})['data'][0]['data']
        #report_obj = self.getWsClient().get_objects([{'ref':ret['report_ref']}])[0]['data']
        #self.assertIsNotNone(report_obj['objects_created'][0]['ref'])

        #created_obj_0_info = self.getWsClient().get_object_info_new({'objects':[{'ref':report_obj['objects_created'][0]['ref']}]})[0]
        #self.assertEqual(created_obj_0_info[NAME_I], obj_out_name)
        #self.assertEqual(created_obj_0_info[TYPE_I].split('-')[0], obj_out_type)


    #### View Fxn Profile for FeatureSet
    ##
    # HIDE @unittest.skip("skipped test_view_fxn_profile_featureSet_01()")  # uncomment to skip
    def test_view_fxn_profile_featureSet_01(self):
        method = 'view_fxn_profile_featureSet'

        print ("\n\nRUNNING: test_"+method+"_01()")
        print ("==================================================\n\n")

        # input_data
        genomeInfo_0 = self.getGenomeInfo('GCF_000287295.1_ASM28729v1_genomic', 0)  # Candidatus Carsonella ruddii HT isolate Thao2000
        genomeInfo_1 = self.getGenomeInfo('GCF_000306885.1_ASM30688v1_genomic', 1)  # Wolbachia endosymbiont of Onchocerca ochengi
#        genomeInfo_2 = self.getGenomeInfo('GCF_001439985.1_wTPRE_1.0_genomic',  2)  # Wolbachia endosymbiont of Trichogramma pretiosum
#        genomeInfo_3 = self.getGenomeInfo('GCF_000022285.1_ASM2228v1_genomic',  3)  # Wolbachia sp. wRi

        genome_ref_0 = self.getWsName() + '/' + str(genomeInfo_0[0]) + '/' + str(genomeInfo_0[4])
        genome_ref_1 = self.getWsName() + '/' + str(genomeInfo_1[0]) + '/' + str(genomeInfo_1[4])
#        genome_ref_2 = self.getWsName() + '/' + str(genomeInfo_2[0]) + '/' + str(genomeInfo_2[4])
#        genome_ref_3 = self.getWsName() + '/' + str(genomeInfo_3[0]) + '/' + str(genomeInfo_3[4])

        feature_id_0_0 = 'A355_RS00030'   # F0F1 ATP Synthase subunit B
        feature_id_0_1 = 'A355_RS00035'
        feature_id_0_2 = 'A355_RS00040'
        feature_id_0_3 = 'A355_RS00125'
        feature_id_0_4 = 'A355_RS00130'
        feature_id_1_0 = 'WOO_RS00195'    # F0 ATP Synthase subunit B
        feature_id_1_1 = 'WOO_RS00200'
        feature_id_1_2 = 'WOO_RS03660'
        feature_id_1_3 = 'WOO_RS03665'
        feature_id_1_4 = 'WOO_RS00250'
        #feature_id_2 = 'AOR14_RS04755'  # F0 ATP Synthase subunit B
        #feature_id_3 = 'WRI_RS01560'    # F0 ATP Synthase subunit B

        # build FeatureSet obj
        testFS = {
            'description': 'a few features',
            'elements': { feature_id_0_0: [genome_ref_0],
                          feature_id_0_1: [genome_ref_0],
                          feature_id_0_2: [genome_ref_0],
                          feature_id_0_3: [genome_ref_0],
                          feature_id_0_4: [genome_ref_0],
                          feature_id_1_0: [genome_ref_1],
                          feature_id_1_1: [genome_ref_1],
                          feature_id_1_2: [genome_ref_1],
                          feature_id_1_3: [genome_ref_1],
                          feature_id_1_4: [genome_ref_1]
                      }
        }
        
        obj_info = self.getWsClient().save_objects({'workspace': self.getWsName(),       
                                                    'objects': [
                                                        {
                                                            'type':'KBaseCollections.FeatureSet',
                                                            'data':testFS,
                                                            'name':method+'.test_FeatureSet',
                                                            'meta':{},
                                                            'provenance':[
                                                                {
                                                                    'service':'kb_phylogenomics',
                                                                    'method':'test_view_fxn_profile_featureSet'
                                                                }
                                                            ]
                                                        }]
                                                })[0]

        pprint(obj_info)
        [OBJID_I, NAME_I, TYPE_I, SAVE_DATE_I, VERSION_I, SAVED_BY_I, WSID_I, WORKSPACE_I, CHSUM_I, SIZE_I, META_I] = range(11)  # object_info tuple
        featureSet_ref = str(obj_info[WSID_I])+'/'+str(obj_info[OBJID_I])+'/'+str(obj_info[VERSION_I])

        # get annotated domains
        domain_info_0 = self.getDomainInfo('Carsonella.Domains', 0, genome_ref_0)
        domain_info_1 = self.getDomainInfo('Wolbachia_ochengi.Domains', 1, genome_ref_1)
#        domain_info_2 = self.getDomainInfo('Wolbachia_pretiosum.Domains', 2, genome_ref_2)
#        domain_info_3 = self.getDomainInfo('Wolbachia_sp.wRi.Domains', 3, genome_ref_3)


        # run that sucker
        params = { 'workspace_name': self.getWsName(),
                   'custom_target_fams': { 'target_fams': [],
                                           'extra_target_fam_groups_COG':  [],
                                           'extra_target_fam_groups_PFAM': [],
                                           'extra_target_fam_groups_TIGR': [],
                                           'extra_target_fam_groups_SEED': []
                                       },
                   'input_featureSet_ref': featureSet_ref,
                   'namespace': 'COG',
                   'genome_disp_name_config': "obj_name",
                   #'count_category': "perc_annot",
                   'count_category': "raw_count",
                   'heatmap': "1",
                   'vertical': "1",
                   'top_hit': "1",
                   'e_value': "0.001",
                   'log_base': "",
                   'required_COG_annot_perc': "10",
                   'required_TIGR_annot_perc': "10",
                   'required_PFAM_annot_perc': "10",
                   'required_SEED_annot_perc': "33",
                   'count_hypothetical': "0",
                   'show_blanks': "0",
                   'skip_missing_genomes': "0",
                   'enforce_genome_version_match': "0"
               }
        ret = self.getImpl().view_fxn_profile_featureSet(self.getContext(),params)[0]
        self.assertIsNotNone(ret['report_ref'])

        # check created obj
        #report_obj = self.getWsClient().get_objects2({'objects':[{'ref':ret['report_ref']}]})['data'][0]['data']
        #report_obj = self.getWsClient().get_objects([{'ref':ret['report_ref']}])[0]['data']
        #self.assertIsNotNone(report_obj['objects_created'][0]['ref'])

        #created_obj_0_info = self.getWsClient().get_object_info_new({'objects':[{'ref':report_obj['objects_created'][0]['ref']}]})[0]
        #self.assertEqual(created_obj_0_info[NAME_I], obj_out_name)
        #self.assertEqual(created_obj_0_info[TYPE_I].split('-')[0], obj_out_type)


    #### View Fxn Profile for Tree
    ##
    # HIDE @unittest.skip("skipped test_view_fxn_profile_phylo_01()")  # uncomment to skip
    def test_view_fxn_profile_phylo_01(self):
        method = 'view_fxn_profile_phylo'

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

        # upload Tree
        genome_refs_map = { '23880/3/1': genome_ref_0,
                            '23880/4/1': genome_ref_1,
                            '23880/5/1': genome_ref_2,
                            '23880/6/1': genome_ref_3
                        }
        obj_info = self.getTreeInfo('Tiny_things.SpeciesTree', 0, genome_refs_map)
        [OBJID_I, NAME_I, TYPE_I, SAVE_DATE_I, VERSION_I, SAVED_BY_I, WSID_I, WORKSPACE_I, CHSUM_I, SIZE_I, META_I] = range(11)  # object_info tuple
        tree_ref = str(obj_info[WSID_I])+'/'+str(obj_info[OBJID_I])+'/'+str(obj_info[VERSION_I])

        # get annotated domains
        domain_info_0 = self.getDomainInfo('Carsonella.Domains', 0, genome_ref_0)
        domain_info_1 = self.getDomainInfo('Wolbachia_ochengi.Domains', 1, genome_ref_1)
        domain_info_2 = self.getDomainInfo('Wolbachia_pretiosum.Domains', 2, genome_ref_2)
        domain_info_3 = self.getDomainInfo('Wolbachia_sp.wRi.Domains', 3, genome_ref_3)


        # run that sucker
        params = { 'workspace_name': self.getWsName(),
                   'custom_target_fams': { 'target_fams': ['COG0001','COG0002'],
                                           'extra_target_fam_groups_COG':  ["COG: N: Cell motility"],
                                           'extra_target_fam_groups_PFAM': ["PF: Clan CL0003: SAM"],
                                           'extra_target_fam_groups_TIGR': ["TIGR: role:11010: Aromatic amino acid family "],
                                           #'extra_target_fam_groups_SEED': ["SEED: Alanine_biosynthesis"]
                                           'extra_target_fam_groups_SEED': []
                                       },
                   'input_speciesTree_ref': tree_ref,
                   'namespace': 'custom',
                   'genome_disp_name_config': "sci_name",
                   'count_category': "perc_annot",
                   'heatmap': "1",
                   'vertical': "1",
                   'top_hit': "1",
                   'e_value': "0.001",
                   'log_base': "",
                   'required_COG_annot_perc': "10",
                   'required_TIGR_annot_perc': "10",
                   'required_PFAM_annot_perc': "10",
                   'required_SEED_annot_perc': "33",
                   'count_hypothetical': "0",
                   'show_blanks': "0",
                   'skip_missing_genomes': "0",
                   'enforce_genome_version_match': "0"
               }
        ret = self.getImpl().view_fxn_profile_phylo(self.getContext(),params)[0]
        self.assertIsNotNone(ret['report_ref'])

        # check created obj
        #report_obj = self.getWsClient().get_objects2({'objects':[{'ref':ret['report_ref']}]})['data'][0]['data']
        #report_obj = self.getWsClient().get_objects([{'ref':ret['report_ref']}])[0]['data']
        #self.assertIsNotNone(report_obj['objects_created'][0]['ref'])

        #created_obj_0_info = self.getWsClient().get_object_info_new({'objects':[{'ref':report_obj['objects_created'][0]['ref']}]})[0]
        #self.assertEqual(created_obj_0_info[NAME_I], obj_out_name)
        #self.assertEqual(created_obj_0_info[TYPE_I].split('-')[0], obj_out_type)


    #### View Pangenome Circle Plot
    ##
    # HIDE @unittest.skip("skipped test_view_pan_circle_plot_01()")  # uncomment to skip
    def test_view_pan_circle_plot_01(self):
        method = 'view_pan_circle_plot'

        print ("\n\nRUNNING: test_"+method+"_01()")
        print ("==================================================\n\n")

        # input_data
        genomeInfo_0 = self.getGenomeInfo('GCF_000287295.1_ASM28729v1_genomic', 0)  # Candidatus Carsonella ruddii HT isolate Thao2000
        genomeInfo_1 = self.getGenomeInfo('GCF_000306885.1_ASM30688v1_genomic', 1)  # Wolbachia endosymbiont of Onchocerca ochengi
        genomeInfo_2 = self.getGenomeInfo('GCF_001439985.1_wTPRE_1.0_genomic',  2)  # Wolbachia endosymbiont of Trichogramma pretiosum
        genomeInfo_3 = self.getGenomeInfo('GCF_000022285.1_ASM2228v1_genomic',  3)  # Wolbachia sp. wRi

        [OBJID_I, NAME_I, TYPE_I, SAVE_DATE_I, VERSION_I, SAVED_BY_I, WSID_I, WORKSPACE_I, CHSUM_I, SIZE_I, META_I] = range(11)  # object_info tuple
        genome_ref_0 = str(genomeInfo_0[WSID_I]) + '/' + str(genomeInfo_0[OBJID_I]) + '/' + str(genomeInfo_0[VERSION_I])
        genome_ref_1 = str(genomeInfo_1[WSID_I]) + '/' + str(genomeInfo_1[OBJID_I]) + '/' + str(genomeInfo_1[VERSION_I])
        genome_ref_2 = str(genomeInfo_2[WSID_I]) + '/' + str(genomeInfo_2[OBJID_I]) + '/' + str(genomeInfo_2[VERSION_I])
        genome_ref_3 = str(genomeInfo_3[WSID_I]) + '/' + str(genomeInfo_3[OBJID_I]) + '/' + str(genomeInfo_3[VERSION_I])

        #feature_id_0 = 'A355_RS00030'   # F0F1 ATP Synthase subunit B
        #feature_id_1 = 'WOO_RS00195'    # F0 ATP Synthase subunit B
        #feature_id_2 = 'AOR14_RS04755'  # F0 ATP Synthase subunit B
        #feature_id_3 = 'WRI_RS01560'    # F0 ATP Synthase subunit B

        # upload Pangenome
        genome_refs_map = { '23880/3/1': genome_ref_0,
                            '23880/4/1': genome_ref_1,
                            '23880/5/1': genome_ref_2,
                            '23880/6/1': genome_ref_3
                        }
        obj_info = self.getPangenomeInfo('Tiny_things.OrthoMCL_pangenome', 0, genome_refs_map)
        [OBJID_I, NAME_I, TYPE_I, SAVE_DATE_I, VERSION_I, SAVED_BY_I, WSID_I, WORKSPACE_I, CHSUM_I, SIZE_I, META_I] = range(11)  # object_info tuple
        pangenome_ref = str(obj_info[WSID_I])+'/'+str(obj_info[OBJID_I])+'/'+str(obj_info[VERSION_I])

        # run that sucker
        base_genome_ref = genome_ref_1
        compare_genome_refs = [genome_ref_1, genome_ref_2, genome_ref_3]  # Wolbachia
        outgroup_genome_refs = [genome_ref_0]  # Carsonella
        params = { 'workspace_name':             self.getWsName(),
                   'input_genome_ref':           base_genome_ref,
                   'input_pangenome_ref':        pangenome_ref,
                   'input_compare_genome_refs':  compare_genome_refs,
                   'input_outgroup_genome_refs': outgroup_genome_refs,
                   'save_featuresets':           1

               }
        ret = self.getImpl().view_pan_circle_plot(self.getContext(),params)[0]
        self.assertIsNotNone(ret['report_ref'])

        # check created obj
        #report_obj = self.getWsClient().get_objects2({'objects':[{'ref':ret['report_ref']}]})['data'][0]['data']
        #report_obj = self.getWsClient().get_objects([{'ref':ret['report_ref']}])[0]['data']
        #self.assertIsNotNone(report_obj['objects_created'][0]['ref'])

        #created_obj_0_info = self.getWsClient().get_object_info_new({'objects':[{'ref':report_obj['objects_created'][0]['ref']}]})[0]
        #self.assertEqual(created_obj_0_info[NAME_I], obj_out_name)
        #self.assertEqual(created_obj_0_info[TYPE_I].split('-')[0], obj_out_type)


    #### View Pangenome on Tree
    ##
    # HIDE @unittest.skip("skipped test_view_pan_phylo_01()")  # uncomment to skip
    def test_view_pan_phylo_01(self):
        method = 'view_pan_phylo'

        print ("\n\nRUNNING: test_"+method+"_01()")
        print ("==================================================\n\n")

        # input_data
        genomeInfo_0 = self.getGenomeInfo('GCF_000287295.1_ASM28729v1_genomic', 0)  # Candidatus Carsonella ruddii HT isolate Thao2000
        genomeInfo_1 = self.getGenomeInfo('GCF_000306885.1_ASM30688v1_genomic', 1)  # Wolbachia endosymbiont of Onchocerca ochengi
        genomeInfo_2 = self.getGenomeInfo('GCF_001439985.1_wTPRE_1.0_genomic',  2)  # Wolbachia endosymbiont of Trichogramma pretiosum
        genomeInfo_3 = self.getGenomeInfo('GCF_000022285.1_ASM2228v1_genomic',  3)  # Wolbachia sp. wRi

        [OBJID_I, NAME_I, TYPE_I, SAVE_DATE_I, VERSION_I, SAVED_BY_I, WSID_I, WORKSPACE_I, CHSUM_I, SIZE_I, META_I] = range(11)  # object_info tuple
        genome_ref_0 = str(genomeInfo_0[WSID_I]) + '/' + str(genomeInfo_0[OBJID_I]) + '/' + str(genomeInfo_0[VERSION_I])
        genome_ref_1 = str(genomeInfo_1[WSID_I]) + '/' + str(genomeInfo_1[OBJID_I]) + '/' + str(genomeInfo_1[VERSION_I])
        genome_ref_2 = str(genomeInfo_2[WSID_I]) + '/' + str(genomeInfo_2[OBJID_I]) + '/' + str(genomeInfo_2[VERSION_I])
        genome_ref_3 = str(genomeInfo_3[WSID_I]) + '/' + str(genomeInfo_3[OBJID_I]) + '/' + str(genomeInfo_3[VERSION_I])

        #feature_id_0 = 'A355_RS00030'   # F0F1 ATP Synthase subunit B
        #feature_id_1 = 'WOO_RS00195'    # F0 ATP Synthase subunit B
        #feature_id_2 = 'AOR14_RS04755'  # F0 ATP Synthase subunit B
        #feature_id_3 = 'WRI_RS01560'    # F0 ATP Synthase subunit B

        # upload Pangenome
        genome_refs_map = { '23880/3/1': genome_ref_0,
                            '23880/4/1': genome_ref_1,
                            '23880/5/1': genome_ref_2,
                            '23880/6/1': genome_ref_3
                        }
        obj_info = self.getPangenomeInfo('Tiny_things.OrthoMCL_pangenome', 0, genome_refs_map)
        [OBJID_I, NAME_I, TYPE_I, SAVE_DATE_I, VERSION_I, SAVED_BY_I, WSID_I, WORKSPACE_I, CHSUM_I, SIZE_I, META_I] = range(11)  # object_info tuple
        pangenome_ref = str(obj_info[WSID_I])+'/'+str(obj_info[OBJID_I])+'/'+str(obj_info[VERSION_I])

        # upload Species Tree
        obj_info = self.getTreeInfo('Tiny_things.SpeciesTree', 0, genome_refs_map)
        [OBJID_I, NAME_I, TYPE_I, SAVE_DATE_I, VERSION_I, SAVED_BY_I, WSID_I, WORKSPACE_I, CHSUM_I, SIZE_I, META_I] = range(11)  # object_info tuple
        tree_ref = str(obj_info[WSID_I])+'/'+str(obj_info[OBJID_I])+'/'+str(obj_info[VERSION_I])

        # run that sucker
        params = { 'workspace_name':        self.getWsName(),
                   'input_pangenome_ref':   pangenome_ref,
                   'input_speciesTree_ref': tree_ref,
                   'save_featuresets':      1,
                   'skip_missing_genomes': "0",
                   'enforce_genome_version_match': "0"
               }
        ret = self.getImpl().view_pan_phylo(self.getContext(),params)[0]
        self.assertIsNotNone(ret['report_ref'])

        # check created obj
        #report_obj = self.getWsClient().get_objects2({'objects':[{'ref':ret['report_ref']}]})['data'][0]['data']
        #report_obj = self.getWsClient().get_objects([{'ref':ret['report_ref']}])[0]['data']
        #self.assertIsNotNone(report_obj['objects_created'][0]['ref'])

        #created_obj_0_info = self.getWsClient().get_object_info_new({'objects':[{'ref':report_obj['objects_created'][0]['ref']}]})[0]
        #self.assertEqual(created_obj_0_info[NAME_I], obj_out_name)
        #self.assertEqual(created_obj_0_info[TYPE_I].split('-')[0], obj_out_type)


    #### View Tree
    ##
    # HIDE @unittest.skip("skipped test_view_tree_01()")  # uncomment to skip
    def test_view_tree_01(self):
        method = 'view_tree'

        print ("\n\nRUNNING: test_"+method+"_01()")
        print ("=============================\n\n")

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

        # upload Tree
        genome_refs_map = { '23880/3/1': genome_ref_0,
                            '23880/4/1': genome_ref_1,
                            '23880/5/1': genome_ref_2,
                            '23880/6/1': genome_ref_3
                        }
        obj_info = self.getTreeInfo('Tiny_things.SpeciesTree', 0, genome_refs_map)
        [OBJID_I, NAME_I, TYPE_I, SAVE_DATE_I, VERSION_I, SAVED_BY_I, WSID_I, WORKSPACE_I, CHSUM_I, SIZE_I, META_I] = range(11)  # object_info tuple
        tree_ref = str(obj_info[WSID_I])+'/'+str(obj_info[OBJID_I])+'/'+str(obj_info[VERSION_I])

        # run that sucker
        params = { 'workspace_name': self.getWsName(),
                   'input_tree_ref': tree_ref,
                   'desc':           'test tree'
               }
        ret = self.getImpl().view_tree(self.getContext(),params)[0]
        self.assertIsNotNone(ret['report_ref'])

        # check created obj
        #report_obj = self.getWsClient().get_objects2({'objects':[{'ref':ret['report_ref']}]})['data'][0]['data']
        #report_obj = self.getWsClient().get_objects([{'ref':ret['report_ref']}])[0]['data']
        #self.assertIsNotNone(report_obj['objects_created'][0]['ref'])

        #created_obj_0_info = self.getWsClient().get_object_info_new({'objects':[{'ref':report_obj['objects_created'][0]['ref']}]})[0]
        #self.assertEqual(created_obj_0_info[NAME_I], obj_out_name)
        #self.assertEqual(created_obj_0_info[TYPE_I].split('-')[0], obj_out_type)


    #### Trim SpeciesTree to GenomeSet
    ##
    # HIDE @unittest.skip("skipped test_trim_speciestree_to_genomeset_01()")  # uncomment to skip
    def test_trim_speciestree_to_genomeset_01(self):
        method = 'trim_speciestree_to_genomeset'

        print ("\n\nRUNNING: test_"+method+"_01()")
        print ("=============================\n\n")

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

        # upload Tree
        genome_refs_map = { '23880/3/1': genome_ref_0,
                            '23880/4/1': genome_ref_1,
                            '23880/5/1': genome_ref_2,
                            '23880/6/1': genome_ref_3
                        }
        obj_info = self.getTreeInfo('Tiny_things.SpeciesTree', 0, genome_refs_map)
        [OBJID_I, NAME_I, TYPE_I, SAVE_DATE_I, VERSION_I, SAVED_BY_I, WSID_I, WORKSPACE_I, CHSUM_I, SIZE_I, META_I] = range(11)  # object_info tuple
        tree_ref = str(obj_info[WSID_I])+'/'+str(obj_info[OBJID_I])+'/'+str(obj_info[VERSION_I])


        # upload genomeSet
        genome_ref_list = [genome_ref_0, genome_ref_1, genome_ref_3]
        genome_scinames = dict()
        genome_objnames = dict()
        genome_refs_by_objname = dict()
        genome_scinames[genome_ref_0] = 'Candidatus Carsonella ruddii HT isolate Thao2000'
        genome_scinames[genome_ref_1] = 'Wolbachia endosymbiont of Onchocerca ochengi'
        genome_scinames[genome_ref_3] = 'Wolbachia sp. wRi'
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
            'description': 'three genomes',
            'elements': dict()
        }
        for genome_ref in genome_ref_list: 
            testGS['elements'][genome_scinames[genome_ref]] = { 'ref': genome_ref }

        obj_info = self.getWsClient().save_objects({'workspace': self.getWsName(),       
                                                    'objects': [
                                                        {
                                                            'type':'KBaseSearch.GenomeSet',
                                                            'data':testGS,
                                                            'name':method+'.test_genomeset',
                                                            'meta':{},
                                                            'provenance':[
                                                                {
                                                                    'service':'kb_phylogenomics',
                                                                    'method':'test_view_fxn_profile'
                                                                }
                                                            ]
                                                        }]
                                                })[0]
        pprint(obj_info)
        [OBJID_I, NAME_I, TYPE_I, SAVE_DATE_I, VERSION_I, SAVED_BY_I, WSID_I, WORKSPACE_I, CHSUM_I, SIZE_I, META_I] = range(11)  # object_info tuple
        genomeSet_ref = str(obj_info[WSID_I])+'/'+str(obj_info[OBJID_I])+'/'+str(obj_info[VERSION_I])


        # run that sucker
        obj_out_name = 'Trimmed.SpeciesTree'
        obj_out_type = 'KBaseTrees.Tree'
        params = { 'workspace_name':               self.getWsName(),
                   'input_tree_ref':               tree_ref,
                   'input_genomeSet_ref':          genomeSet_ref,
                   'output_tree_name':             obj_out_name,
                   'enforce_genome_version_match': "1",
                   'desc':                         'test tree'
               }
        ret = self.getImpl().trim_speciestree_to_genomeset(self.getContext(),params)[0]
        self.assertIsNotNone(ret['report_ref'])

        # check created obj
        #report_obj = self.getWsClient().get_objects([{'ref':ret['report_ref']}])[0]['data']
        report_obj = self.getWsClient().get_objects2({'objects':[{'ref':ret['report_ref']}]})['data'][0]['data']
        self.assertIsNotNone(report_obj['objects_created'][0]['ref'])

        created_obj_0_info = self.getWsClient().get_object_info_new({'objects':[{'ref':report_obj['objects_created'][0]['ref']}]})[0]
        self.assertEqual(created_obj_0_info[NAME_I], obj_out_name)
        self.assertEqual(created_obj_0_info[TYPE_I].split('-')[0], obj_out_type)


    #### Build Microbial SpeciesTree
    ##
    # HIDE @unittest.skip("skipped test_build_microbial_speciestree_01()")  # uncomment to skip
    def test_build_microbial_speciestree_01(self):
        method = 'build_microbial_speciestree'

        print ("\n\nRUNNING: test_"+method+"_01()")
        print ("=============================\n\n")

        [OBJID_I, NAME_I, TYPE_I, SAVE_DATE_I, VERSION_I, SAVED_BY_I, WSID_I, WORKSPACE_I, CHSUM_I, SIZE_I, META_I] = range(11)  # object_info tuple

        # input_data
        genomeInfo_0 = self.getGenomeInfo('GCF_000287295.1_ASM28729v1_genomic', 0)  # Candidatus Carsonella ruddii HT isolate Thao2000
        #genomeInfo_1 = self.getGenomeInfo('GCF_000306885.1_ASM30688v1_genomic', 1)  # Wolbachia endosymbiont of Onchocerca ochengi
        #genomeInfo_2 = self.getGenomeInfo('GCF_001439985.1_wTPRE_1.0_genomic',  2)  # Wolbachia endosymbiont of Trichogramma pretiosum
        #genomeInfo_3 = self.getGenomeInfo('GCF_000022285.1_ASM2228v1_genomic',  3)  # Wolbachia sp. wRi

        genome_ref_0 = self.getWsName() + '/' + str(genomeInfo_0[0]) + '/' + str(genomeInfo_0[4])
        #genome_ref_1 = self.getWsName() + '/' + str(genomeInfo_1[0]) + '/' + str(genomeInfo_1[4])
        #genome_ref_2 = self.getWsName() + '/' + str(genomeInfo_2[0]) + '/' + str(genomeInfo_2[4])
        #genome_ref_3 = self.getWsName() + '/' + str(genomeInfo_3[0]) + '/' + str(genomeInfo_3[4])

        #feature_id_0 = 'A355_RS00030'   # F0F1 ATP Synthase subunit B
        #feature_id_1 = 'WOO_RS00195'    # F0 ATP Synthase subunit B
        #feature_id_2 = 'AOR14_RS04755'  # F0 ATP Synthase subunit B
        #feature_id_3 = 'WRI_RS01560'    # F0 ATP Synthase subunit B

        # upload genomeSet
        #genome_ref_list = [genome_ref_0, genome_ref_1, genome_ref_2, genome_ref_3]
        genome_ref_list = [genome_ref_0]
        genome_scinames = dict()
        genome_objnames = dict()
        genome_refs_by_objname = dict()
        genome_scinames[genome_ref_0] = 'Candidatus Carsonella ruddii HT isolate Thao2000'
        #genome_scinames[genome_ref_1] = 'Wolbachia endosymbiont of Onchocerca ochengi'
        #genome_scinames[genome_ref_2] = 'Wolbachia endosymbiont of Trichogramma pretiosum'
        #genome_scinames[genome_ref_3] = 'Wolbachia sp. wRi'
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
            'description': 'one genome',
            'elements': dict()
        }
        for genome_ref in genome_ref_list: 
            testGS['elements'][genome_scinames[genome_ref]] = { 'ref': genome_ref }

        obj_info = self.getWsClient().save_objects({'workspace': self.getWsName(),       
                                                    'objects': [
                                                        {
                                                            'type':'KBaseSearch.GenomeSet',
                                                            'data':testGS,
                                                            'name':method+'.test_genomeset',
                                                            'meta':{},
                                                            'provenance':[
                                                                {
                                                                    'service':'kb_phylogenomics',
                                                                    'method':'build_microbial_speciestree'
                                                                }
                                                            ]
                                                        }]
                                                })[0]
        pprint(obj_info)
        genomeSet_ref = str(obj_info[WSID_I])+'/'+str(obj_info[OBJID_I])+'/'+str(obj_info[VERSION_I])


        # run that sucker
        obj_out_name = 'Microbial_Tree_with_Skeleton.SpeciesTree'
        obj_out_type = 'KBaseTrees.Tree'
        skeleton_set = 'RefSeq-Isolates'
        params = { 'workspace_name':               self.getWsName(),
                   'input_genome_refs':            [genomeSet_ref],
                   'output_tree_name':             obj_out_name,
                   'desc':                         'test tree',
                   'skeleton_set':                 skeleton_set
               }
        ret = self.getImpl().build_microbial_speciestree(self.getContext(),params)[0]
        self.assertIsNotNone(ret['report_ref'])

        # check created obj
        #report_obj = self.getWsClient().get_objects([{'ref':ret['report_ref']}])[0]['data']
        report_obj = self.getWsClient().get_objects2({'objects':[{'ref':ret['report_ref']}]})['data'][0]['data']
        self.assertIsNotNone(report_obj['objects_created'][0]['ref'])

        created_obj_0_info = self.getWsClient().get_object_info_new({'objects':[{'ref':report_obj['objects_created'][0]['ref']}]})[0]
        self.assertEqual(created_obj_0_info[NAME_I], obj_out_name)
        self.assertEqual(created_obj_0_info[TYPE_I].split('-')[0], obj_out_type)


    #### Find Homologs with Genome Context
    ##
    # HIDE @unittest.skip("skipped test_find_homologs_with_genome_context_01()")  # uncomment to skip
    def test_find_homologs_with_genome_context_01(self):
        method = 'find_homologs_with_genome_context'

        print ("\n\nRUNNING: test_"+method+"_01()")
        print ("=============================\n\n")

        # input_data
        genomeInfo_0 = self.getGenomeInfo('GCF_000287295.1_ASM28729v1_genomic', 0)  # Candidatus Carsonella ruddii HT isolate Thao2000
        genomeInfo_1 = self.getGenomeInfo('GCF_000306885.1_ASM30688v1_genomic', 1)  # Wolbachia endosymbiont of Onchocerca ochengi
        genomeInfo_2 = self.getGenomeInfo('GCF_001439985.1_wTPRE_1.0_genomic',  2)  # Wolbachia endosymbiont of Trichogramma pretiosum
        genomeInfo_3 = self.getGenomeInfo('GCF_000022285.1_ASM2228v1_genomic',  3)  # Wolbachia sp. wRi

        genome_ref_0 = self.getWsName() + '/' + str(genomeInfo_0[0]) + '/' + str(genomeInfo_0[4])
        genome_ref_1 = self.getWsName() + '/' + str(genomeInfo_1[0]) + '/' + str(genomeInfo_1[4])
        genome_ref_2 = self.getWsName() + '/' + str(genomeInfo_2[0]) + '/' + str(genomeInfo_2[4])
        genome_ref_3 = self.getWsName() + '/' + str(genomeInfo_3[0]) + '/' + str(genomeInfo_3[4])

        feature_id_0_0 = 'A355_RS00030'   # F0F1 ATP Synthase subunit B
        feature_id_0_1 = 'A355_RS00035'
        feature_id_0_2 = 'A355_RS00040'
        feature_id_0_3 = 'A355_RS00125'
        feature_id_0_4 = 'A355_RS00130'
        feature_id_1_0 = 'WOO_RS00195'    # F0 ATP Synthase subunit B
        feature_id_1_1 = 'WOO_RS00200'
        feature_id_1_2 = 'WOO_RS03660'
        feature_id_1_3 = 'WOO_RS03665'
        feature_id_1_4 = 'WOO_RS00250'
        #feature_id_2 = 'AOR14_RS04755'  # F0 ATP Synthase subunit B
        #feature_id_3 = 'WRI_RS01560'    # F0 ATP Synthase subunit B

        # upload Tree
        genome_refs_map = { '23880/3/1': genome_ref_0,
                            '23880/4/1': genome_ref_1,
                            '23880/5/1': genome_ref_2,
                            '23880/6/1': genome_ref_3
                        }
        obj_info = self.getTreeInfo('Tiny_things.SpeciesTree', 0, genome_refs_map)
        [OBJID_I, NAME_I, TYPE_I, SAVE_DATE_I, VERSION_I, SAVED_BY_I, WSID_I, WORKSPACE_I, CHSUM_I, SIZE_I, META_I] = range(11)  # object_info tuple
        tree_ref = str(obj_info[WSID_I])+'/'+str(obj_info[OBJID_I])+'/'+str(obj_info[VERSION_I])

        # build FeatureSet obj
        testFS = {
            'description': 'a few features',
            'elements': { feature_id_0_0: [genome_ref_0],
                          feature_id_0_1: [genome_ref_0],
                          feature_id_0_2: [genome_ref_0],
                          feature_id_0_3: [genome_ref_0],
                          feature_id_0_4: [genome_ref_0],
                          feature_id_1_0: [genome_ref_1],
                          feature_id_1_1: [genome_ref_1],
                          feature_id_1_2: [genome_ref_1]
                          #feature_id_1_3: [genome_ref_1],
                          #feature_id_1_4: [genome_ref_1]
                      }
        }
        
        obj_info = self.getWsClient().save_objects({'workspace': self.getWsName(),       
                                                    'objects': [
                                                        {
                                                            'type':'KBaseCollections.FeatureSet',
                                                            'data':testFS,
                                                            'name':method+'.test_FeatureSet',
                                                            'meta':{},
                                                            'provenance':[
                                                                {
                                                                    'service':'kb_phylogenomics',
                                                                    'method':'test_find_homologs_with_genome_context_featureSet'
                                                                }
                                                            ]
                                                        }]
                                                })[0]

        pprint(obj_info)
        [OBJID_I, NAME_I, TYPE_I, SAVE_DATE_I, VERSION_I, SAVED_BY_I, WSID_I, WORKSPACE_I, CHSUM_I, SIZE_I, META_I] = range(11)  # object_info tuple
        query_featureSet_ref = str(obj_info[WSID_I])+'/'+str(obj_info[OBJID_I])+'/'+str(obj_info[VERSION_I])

        # run that sucker
        params = { 'workspace_name': self.getWsName(),
                   'input_speciesTree_ref': tree_ref,
                   'input_featureSet_ref': query_featureSet_ref,
                   'save_per_genome_featureSets': 0,
                   'neighbor_thresh': 10,
                   'ident_thresh': 40.0,
                   'e_value': .001,
                   'bitscore': 50,
                   'overlap_fraction': 50.0,
                   'color_seed': 1
               }
        ret = self.getImpl().find_homologs_with_genome_context(self.getContext(),params)[0]
        self.assertIsNotNone(ret['report_ref'])

        # check created obj
        #report_obj = self.getWsClient().get_objects2({'objects':[{'ref':ret['report_ref']}]})['data'][0]['data']
        #report_obj = self.getWsClient().get_objects([{'ref':ret['report_ref']}])[0]['data']
        #self.assertIsNotNone(report_obj['objects_created'][0]['ref'])

        #created_obj_0_info = self.getWsClient().get_object_info_new({'objects':[{'ref':report_obj['objects_created'][0]['ref']}]})[0]
        #self.assertEqual(created_obj_0_info[NAME_I], obj_out_name)
        #self.assertEqual(created_obj_0_info[TYPE_I].split('-')[0], obj_out_type)


    #### Find Homologs with Genome Context (with queries with no matches)
    ##
    # HIDE @unittest.skip("skipped test_find_homologs_with_genome_context_02()")  # uncomment to skip
    def test_find_homologs_with_genome_context_02(self):
        method = 'find_homologs_with_genome_context'

        print ("\n\nRUNNING: test_"+method+"_01()")
        print ("=============================\n\n")

        # input_data
        genomeInfo_0 = self.getGenomeInfo('GCF_000287295.1_ASM28729v1_genomic', 0)  # Candidatus Carsonella ruddii HT isolate Thao2000
        genomeInfo_1 = self.getGenomeInfo('GCF_000306885.1_ASM30688v1_genomic', 1)  # Wolbachia endosymbiont of Onchocerca ochengi
        genomeInfo_2 = self.getGenomeInfo('GCF_001439985.1_wTPRE_1.0_genomic',  2)  # Wolbachia endosymbiont of Trichogramma pretiosum
        genomeInfo_3 = self.getGenomeInfo('GCF_000022285.1_ASM2228v1_genomic',  3)  # Wolbachia sp. wRi

        genome_ref_0 = self.getWsName() + '/' + str(genomeInfo_0[0]) + '/' + str(genomeInfo_0[4])
        genome_ref_1 = self.getWsName() + '/' + str(genomeInfo_1[0]) + '/' + str(genomeInfo_1[4])
        genome_ref_2 = self.getWsName() + '/' + str(genomeInfo_2[0]) + '/' + str(genomeInfo_2[4])
        genome_ref_3 = self.getWsName() + '/' + str(genomeInfo_3[0]) + '/' + str(genomeInfo_3[4])

        feature_id_0_0 = 'A355_RS00030'   # F0F1 ATP Synthase subunit B
        feature_id_0_1 = 'A355_RS00035'
        feature_id_0_2 = 'A355_RS00040'
        feature_id_0_3 = 'A355_RS00125'
        feature_id_0_4 = 'A355_RS00130'
        feature_id_1_0 = 'WOO_RS00195'    # F0 ATP Synthase subunit B
        feature_id_1_1 = 'WOO_RS00200'
        feature_id_1_2 = 'WOO_RS03660'
        feature_id_1_3 = 'WOO_RS03665'
        feature_id_1_4 = 'WOO_RS00250'
        #feature_id_2 = 'AOR14_RS04755'  # F0 ATP Synthase subunit B
        #feature_id_3 = 'WRI_RS01560'    # F0 ATP Synthase subunit B

        # upload Tree
        genome_refs_map = { '23880/3/1': genome_ref_0,
                            '23880/4/1': genome_ref_1,
                            '23880/5/1': genome_ref_2,
                            '23880/6/1': genome_ref_3
                        }
        obj_info = self.getTreeInfo('Tiny_things.SpeciesTree', 0, genome_refs_map)
        [OBJID_I, NAME_I, TYPE_I, SAVE_DATE_I, VERSION_I, SAVED_BY_I, WSID_I, WORKSPACE_I, CHSUM_I, SIZE_I, META_I] = range(11)  # object_info tuple
        tree_ref = str(obj_info[WSID_I])+'/'+str(obj_info[OBJID_I])+'/'+str(obj_info[VERSION_I])

        # build FeatureSet obj
        testFS = {
            'description': 'a few features',
            'elements': { feature_id_0_0: [genome_ref_0],
                          feature_id_0_1: [genome_ref_0],
#                          feature_id_0_2: [genome_ref_0],
#                          feature_id_0_3: [genome_ref_0],
#                          feature_id_0_4: [genome_ref_0],
#                          feature_id_1_0: [genome_ref_1],
#                          feature_id_1_1: [genome_ref_1],
#                          feature_id_1_2: [genome_ref_1]
                          #feature_id_1_3: [genome_ref_1],
                          #feature_id_1_4: [genome_ref_1]
                      }
        }
        
        obj_info = self.getWsClient().save_objects({'workspace': self.getWsName(),       
                                                    'objects': [
                                                        {
                                                            'type':'KBaseCollections.FeatureSet',
                                                            'data':testFS,
                                                            'name':method+'.test_2_FeatureSet',
                                                            'meta':{},
                                                            'provenance':[
                                                                {
                                                                    'service':'kb_phylogenomics',
                                                                    'method':'test_find_homologs_with_genome_context_featureSet'
                                                                }
                                                            ]
                                                        }]
                                                })[0]

        pprint(obj_info)
        [OBJID_I, NAME_I, TYPE_I, SAVE_DATE_I, VERSION_I, SAVED_BY_I, WSID_I, WORKSPACE_I, CHSUM_I, SIZE_I, META_I] = range(11)  # object_info tuple
        query_featureSet_ref = str(obj_info[WSID_I])+'/'+str(obj_info[OBJID_I])+'/'+str(obj_info[VERSION_I])

        # run that sucker
        params = { 'workspace_name': self.getWsName(),
                   'input_speciesTree_ref': tree_ref,
                   'input_featureSet_ref': query_featureSet_ref,
                   'save_per_genome_featureSets': 0,
                   'neighbor_thresh': 10,
                   'ident_thresh': 40.0,
                   'e_value': .001,
                   'bitscore': 10000000000000000000000000,  # this should do it
                   'overlap_fraction': 50.0,
                   'color_seed': 1
               }
        ret = self.getImpl().find_homologs_with_genome_context(self.getContext(),params)[0]
        self.assertIsNotNone(ret['report_ref'])

        # check created obj
        #report_obj = self.getWsClient().get_objects2({'objects':[{'ref':ret['report_ref']}]})['data'][0]['data']
        #report_obj = self.getWsClient().get_objects([{'ref':ret['report_ref']}])[0]['data']
        #self.assertIsNotNone(report_obj['objects_created'][0]['ref'])

        #created_obj_0_info = self.getWsClient().get_object_info_new({'objects':[{'ref':report_obj['objects_created'][0]['ref']}]})[0]
        #self.assertEqual(created_obj_0_info[NAME_I], obj_out_name)
        #self.assertEqual(created_obj_0_info[TYPE_I].split('-')[0], obj_out_type)
        

    #### Build Gene Tree
    ##
    # HIDE @unittest.skip("skipped test_build_gene_tree_01()")  # uncomment to skip
    def test_build_gene_tree_01(self):
        method = 'build_gene_tree'

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

        feature_id_0 = 'A355_RS00030'   # F0F1 ATP Synthase subunit B
        feature_id_1 = 'WOO_RS00195'    # F0 ATP Synthase subunit B
        feature_id_2 = 'AOR14_RS04755'  # F0 ATP Synthase subunit B
        feature_id_3 = 'WRI_RS01560'    # F0 ATP Synthase subunit B

        # build FeatureSet obj
        testFS = {
            'description': 'F0 ATP Synthase subunit B',
            'elements': { feature_id_0: [genome_ref_0],
                          feature_id_1: [genome_ref_1],
                          feature_id_2: [genome_ref_2],
                          feature_id_3: [genome_ref_3]
                      }
        }
        
        obj_info = self.getWsClient().save_objects({'workspace': self.getWsName(),       
                                                    'objects': [
                                                        {
                                                            'type':'KBaseCollections.FeatureSet',
                                                            'data':testFS,
                                                            'name':method+'.test_FeatureSet',
                                                            'meta':{},
                                                            'provenance':[
                                                                {
                                                                    'service':'kb_phylogenomics',
                                                                    'method':'test_build_gene_tree'
                                                                }
                                                            ]
                                                        }]
                                                })[0]

        pprint(obj_info)
        [OBJID_I, NAME_I, TYPE_I, SAVE_DATE_I, VERSION_I, SAVED_BY_I, WSID_I, WORKSPACE_I, CHSUM_I, SIZE_I, META_I] = range(11)  # object_info tuple
        featureSet_ref = str(obj_info[WSID_I])+'/'+str(obj_info[OBJID_I])+'/'+str(obj_info[VERSION_I])


        # run that sucker
        obj_out_name = method+'.geneTree'
        obj_out_type = 'KBaseTrees.Tree'
        params = { 'workspace_name': self.getWsName(),
                   'desc': 'gene tree for '+testFS['description'],
                   'input_featureSet_ref': featureSet_ref,
                   'output_tree_name': obj_out_name,
                   'muscle_maxiters': '16',
                   'muscle_maxours': '0.5',
                   'gblocks_trim_level': '1',
                   'gblocks_min_seqs_for_conserved': '0',
                   'gblocks_min_seqs_for_flank': '0',
                   'gblocks_max_pos_contig_nonconserved': '8',
                   'gblocks_min_block_len': '10',
                   'gblocks_remove_mask_positions_flag': '0',
                   'fasttree_fastest': '0',
                   'fasttree_pseudo': '0',
                   'fasttree_gtr': '0',
                   'fasttree_wag': '0',
                   'fasttree_noml': '0',
                   'fasttree_nome': '0',
                   'fasttree_cat': '20',
                   'fasttree_nocat': '0',
                   'fasttree_gamma': '0'
               }
        ret = self.getImpl().build_gene_tree(self.getContext(),params)[0]
        self.assertIsNotNone(ret['report_ref'])

        # check created obj
        report_obj = self.getWsClient().get_objects2({'objects':[{'ref':ret['report_ref']}]})['data'][0]['data']
        report_obj = self.getWsClient().get_objects([{'ref':ret['report_ref']}])[0]['data']
        self.assertIsNotNone(report_obj['objects_created'][0]['ref'])

        created_obj_0_info = self.getWsClient().get_object_info_new({'objects':[{'ref':report_obj['objects_created'][0]['ref']}]})[0]
        self.assertEqual(created_obj_0_info[NAME_I], obj_out_name)
        self.assertEqual(created_obj_0_info[TYPE_I].split('-')[0], obj_out_type)


    #### Get Categories auto-configure method
    ##
    # HIDE @unittest.skip("skipped test_get_categoreis()")  # uncomment to skip
    def test_get_categories(self):
        method = 'get_configure_categories'

        print ("\n\nRUNNING: test_"+method+"_01()")
        print ("=============================\n\n")
        
        # run that sucker
        params = { 'workspace_name': self.getWsName()
               }        
        ret = self.getImpl().get_configure_categories(self.getContext(),params)[0]
        self.assertIn('SEED', ret['cat2name'])
        
