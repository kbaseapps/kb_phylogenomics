# -*- coding: utf-8 -*-
#BEGIN_HEADER
from __future__ import print_function
from __future__ import division

import os
import sys
import shutil
import hashlib
import subprocess
import requests
requests.packages.urllib3.disable_warnings()
import re
import traceback
import uuid
from datetime import datetime
from pprint import pprint, pformat

import numpy as np
import math
from Bio import SeqIO

from biokbase.workspace.client import Workspace as workspaceService
from DataFileUtil.DataFileUtilClient import DataFileUtil as DFUClient
from KBaseReport.KBaseReportClient import KBaseReport

from DomainAnnotation.DomainAnnotationClient import DomainAnnotation

import ete3
import matplotlib.pyplot as pyplot  # use this instead
from matplotlib.patches import Arc

#END_HEADER


class kb_phylogenomics:
    '''
    Module Name:
    kb_phylogenomics

    Module Description:
    A KBase module: kb_phylogenomics

This module contains methods for running and visualizing results of phylogenomics and comparative genomics analyses
    '''

    ######## WARNING FOR GEVENT USERS ####### noqa
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    ######################################### noqa
    VERSION = "0.0.1"
    GIT_URL = "https://github.com/kbaseapps/kb_phylogenomics.git"
    GIT_COMMIT_HASH = "f7b44b9ffa99f06e66ecc5be3f5298088c56974b"

    #BEGIN_CLASS_HEADER

    def log(self, target, message):
        if target is not None:
            target.append(message)
        print(message)
        sys.stdout.flush()

    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.workspaceURL = config['workspace-url']
        self.shockURL = config['shock-url']
        self.handleURL = config['handle-service-url']
        self.serviceWizardURL = config['service-wizard-url']
        self.callbackURL = os.environ['SDK_CALLBACK_URL']
        self.scratch = os.path.abspath(config['scratch'])

        pprint(config)

        if not os.path.exists(self.scratch):
            os.makedirs(self.scratch)

        #END_CONSTRUCTOR
        pass


    def run_DomainAnnotation_Sets(self, ctx, params):
        """
        :param params: instance of type "run_DomainAnnotation_Sets_Input"
           (run_DomainAnnotation_Sets() ** ** run the DomainAnnotation App
           against a GenomeSet) -> structure: parameter "workspace_name" of
           type "workspace_name" (** Common types), parameter
           "input_genomeSet_ref" of type "data_obj_ref", parameter
           "override_annot" of type "bool"
        :returns: instance of type "run_DomainAnnotation_Sets_Output" ->
           structure: parameter "report_name" of String, parameter
           "report_ref" of String
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN run_DomainAnnotation_Sets
        console = []
        self.log(console, 'Running run_DomainAnnotation_Sets() with params=')
        self.log(console, "\n"+pformat(params))

        token = ctx['token']
        wsClient = workspaceService(self.workspaceURL, token=token)
        headers = {'Authorization': 'OAuth '+token}
        env = os.environ.copy()
        env['KB_AUTH_TOKEN'] = token

        #SERVICE_VER = 'dev'  # DEBUG
        SERVICE_VER = 'release'


        ### STEP 1: basic parameter checks + parsing
        required_params = ['workspace_name',
                           'input_genomeSet_ref'
                          ]
        for arg in required_params:
            if arg not in params or params[arg] == None or params[arg] == '':
                raise ValueError ("Must define required param: '"+required_param+"'")


        ### STEP 2: build a list of genomes to iterate through

        # get genome set
        input_ref = params['input_genomeSet_ref']
        try:
            [OBJID_I, NAME_I, TYPE_I, SAVE_DATE_I, VERSION_I, SAVED_BY_I, WSID_I, WORKSPACE_I, CHSUM_I, SIZE_I, META_I] = range(11)  # object_info tuple
            input_obj_info = wsClient.get_object_info_new ({'objects':[{'ref':input_ref}]})[0]
            input_obj_type = re.sub ('-[0-9]+\.[0-9]+$', "", input_obj_info[TYPE_I])  # remove trailing version
        except Exception as e:
            raise ValueError('Unable to get object from workspace: (' + input_ref +')' + str(e))
        accepted_input_types = ["KBaseSearch.GenomeSet" ]
        if input_obj_type not in accepted_input_types:
            raise ValueError ("Input object of type '"+input_obj_type+"' not accepted.  Must be one of "+", ".join(accepted_input_types))

        # get set obj
        try:
            genomeSet_obj =  wsClient.get_objects([{'ref':input_ref}])[0]['data']
        except:
            raise ValueError ("unable to fetch genomeSet: "+input_ref)

        # get genome refs and object names
        genome_ids = genomeSet_obj['elements'].keys()  # note: genome_id may be meaningless
        genome_refs = []
        for genome_id in genome_ids:
            genome_refs.append (genomeSet_obj['elements'][genome_id]['ref'])

        genome_obj_name_by_ref = dict()
        uniq_genome_ws_ids = dict()
        ws_name_by_genome_ref = dict()

        for genome_ref in genome_refs:

            # get genome object name
            input_ref = genome_ref
            try:
                [OBJID_I, NAME_I, TYPE_I, SAVE_DATE_I, VERSION_I, SAVED_BY_I, WSID_I, WORKSPACE_I, CHSUM_I, SIZE_I, META_I] = range(11)  # object_info tuple
                input_obj_info = wsClient.get_object_info_new ({'objects':[{'ref':input_ref}]})[0]
                input_obj_type = re.sub ('-[0-9]+\.[0-9]+$', "", input_obj_info[TYPE_I])  # remove trailing version
                input_name = input_obj_info[NAME_I]
                uniq_genome_ws_ids[input_obj_info[WSID_I]] = True
                ws_name_by_genome_ref[input_ref] = input_obj_info[WORKSPACE_I]

            except Exception as e:
                raise ValueError('Unable to get object from workspace: (' + input_ref +')' + str(e))
            accepted_input_types = ["KBaseGenomes.Genome" ]
            if input_obj_type not in accepted_input_types:
                raise ValueError ("Input object of type '"+input_obj_type+"' not accepted.  Must be one of "+", ".join(accepted_input_types))

            genome_obj_name_by_ref[input_ref] = input_name


        ### STEP 3: Determine which genomes have already got domain annotations
        domain_annot_done = dict()
        for ws_id in uniq_genome_ws_ids.keys():
            try:
                dom_annot_obj_info_list = wsClient.list_objects({'ids':[ws_id],'type':"KBaseGeneFamilies.DomainAnnotation"})
            except Exception as e:
                raise ValueError ("Unable to list DomainAnnotation objects from workspace: "+str(ws_id)+" "+str(e))

            for info in dom_annot_obj_info_list:
                [OBJID_I, NAME_I, TYPE_I, SAVE_DATE_I, VERSION_I, SAVED_BY_I, WSID_I, WORKSPACE_I, CHSUM_I, SIZE_I, META_I] = range(11)  # object_info tuple
                
                dom_annot_ref = str(info[WSID_I])+'/'+str(info[OBJID_I])+'/'+str(info[VERSION_I])
                try:
                    domain_data = wsClient.get_objects([{'ref':dom_annot_ref}])[0]['data']
                except:
                    raise ValueError ("unable to fetch domain annotation: "+dom_annot_ref)

                # read domain data object
                genome_ref = domain_data['genome_ref']
                if genome_ref not in genome_refs:
                    continue
                domain_annot_done[genome_ref] = True


        ### STEP 4: run DomainAnnotation on each genome in set
        try:
            SERVICE_VER = 'dev'  # DEBUG
            daClient = DomainAnnotation (url=self.callbackURL, token=ctx['token'], service_ver=SERVICE_VER)  # SDK Local
            #daClient = DomainAnnotation (url=self.serviceWizardURL, token=ctx['token'], service_ver=SERVICE_VER)  # Dynamic service
        except:
            raise ValueError ("unable to instantiate DomainAnnotationClient")

        # RUN DomainAnnotations
        report_text = ''
        for genome_i,genome_ref in enumerate(genome_refs):

            if 'override_annot' not in params or params['override_annot'] != '1':
                if genome_ref in domain_annot_done:
                    self.log (console, "SKIPPING repeat domain annotation for genome: "+genome_obj_name_by_ref[genome_ref])

                    continue

            genome_obj_name = genome_obj_name_by_ref[genome_ref]
            domains_obj_name = re.sub ('[\.\-\_\:]GenomeAnnotation$', '', genome_obj_name)
            domains_obj_name = re.sub ('[\.\-\_\:]Genome$', '', domains_obj_name)
            domains_obj_name += '.DomainAnnotation'
            domains_obj_name = 'domains_'+domains_obj_name  # DEBUG
            DomainAnnotation_Params = { 'genome_ref': genome_ref,
                                        'dms_ref': 'KBasePublicGeneDomains/All',
                                        'ws': params['workspace_name'],
                                        #'ws': ws_name_by_genome_ref[genome_ref],
                                        'output_result_id': domains_obj_name
                                      }
            self.log (console, "RUNNING domain annotation for genome: "+genome_obj_name_by_ref[genome_ref])
            self.log(console, "\n"+pformat(DomainAnnotation_Params))
            self.log(console, str(datetime.now()))

            da_retVal = daClient.search_domains (DomainAnnotation_Params)[0]
            this_output_ref  = da_retVal['output_result_id']
            this_report_name = da_retVal['report_name']
            this_report_ref  = da_retVal['report_ref']

            try:
                this_report_obj =  wsClient.get_objects([{'ref':this_report_ref}])[0]['data']
            except:
                raise ValueError ("unable to fetch report: "+this_report_ref)
            report_text += this_report_obj['text_message']
            report_text += "\n\n"


        ### STEP 5: build and save the report
        reportObj = {
            'objects_created': [],
            'text_message': report_text
        }
        reportClient = KBaseReport(self.callbackURL, token=ctx['token'], service_ver=SERVICE_VER)
        report_info = reportClient.create({'report':reportObj, 'workspace_name':params['workspace_name']})


        ### STEP 6: construct the output to send back
        output = { 'report_name': report_info['name'], 'report_ref': report_info['ref'] }

        #END run_DomainAnnotation_Sets

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method run_DomainAnnotation_Sets return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]

    def view_fxn_profile(self, ctx, params):
        """
        :param params: instance of type "view_fxn_profile_Input"
           (view_fxn_profile() ** ** show a table/heatmap of general
           categories or custom gene families for a set of Genomes) ->
           structure: parameter "workspace_name" of type "workspace_name" (**
           Common types), parameter "input_genomeSet_ref" of type
           "data_obj_ref", parameter "namespace" of String, parameter
           "custom_target_fams" of type "CustomTargetFams" (parameter groups)
           -> structure: parameter "target_fams" of list of String, parameter
           "extra_target_fam_groups_COG" of list of String, parameter
           "extra_target_fam_groups_PFAM" of list of String, parameter
           "extra_target_fam_groups_TIGR" of list of String, parameter
           "extra_target_fam_groups_SEED" of list of String, parameter
           "count_category" of String, parameter "heatmap" of type "bool",
           parameter "vertical" of type "bool", parameter "top_hit" of type
           "bool", parameter "e_value" of Double, parameter "log_base" of
           Double, parameter "show_blanks" of type "bool"
        :returns: instance of type "view_fxn_profile_Output" -> structure:
           parameter "report_name" of String, parameter "report_ref" of String
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN view_fxn_profile

        ### STEP 0: basic init
        console = []
        self.log(console, 'Running view_fxn_profile(): ')
        self.log(console, "\n"+pformat(params))

        token = ctx['token']
        wsClient = workspaceService(self.workspaceURL, token=token)
        headers = {'Authorization': 'OAuth '+token}
        env = os.environ.copy()
        env['KB_AUTH_TOKEN'] = token

        #SERVICE_VER = 'dev'  # DEBUG
        SERVICE_VER = 'release'

        # param checks
        required_params = ['input_genomeSet_ref',
                           'namespace'
                          ]
        for arg in required_params:
            if arg not in params or params[arg] == None or params[arg] == '':
                raise ValueError ("Must define required param: '"+arg+"'")

        if params['namespace'] == 'custom':
            if ('custom_target_fams' not in params or not params['custom_target_fams']) \
                    or ( \
                ('target_fams' not in params['custom_target_fams'] or not params['custom_target_fams']['target_fams']) \
                    and ('extra_target_fam_groups_COG' not in params['custom_target_fams'] or not params['custom_target_fams']['extra_target_fam_groups_COG']) \
                    and ('extra_target_fam_groups_PFAM' not in params['custom_target_fams'] or not params['custom_target_fams']['extra_target_fam_groups_PFAM']) \
                    and ('extra_target_fam_groups_TIGR' not in params['custom_target_fams'] or not params['custom_target_fams']['extra_target_fam_groups_TIGR']) \
                    and ('extra_target_fam_groups_SEED' not in params['custom_target_fams'] or not params['custom_target_fams']['extra_target_fam_groups_SEED'])
                ):
                    
                raise ValueError ("Must define either param: 'target_fams' or 'extra_target_fam_groups' if using CUSTOM targets")

        # base config
        namespace_classes = ['COG', 'PF', 'TIGR', 'SEED']
        show_blanks = False
        if 'show_blanks' in params and params['show_blanks'] == '1':
            show_blanks = True
        e_value_thresh = None
        if 'e_value' in params and params['e_value'] != None and params['e_value'] != '':
            e_value_thresh = float (params['e_value'])
        top_hit_flag = False
        if 'top_hit' in params and params['top_hit'] != None and params['top_hit'] != '' and params['top_hit'] != 0:
            top_hit_flag = True

        domain_desc_basepath           = os.path.abspath('/kb/module/data/domain_desc')
        domain_to_cat_map_path         = dict()
        domain_cat_names_path          = dict()
        domain_fam_names_path          = dict()
        domain_to_cat_map_path['COG']  = os.path.join(domain_desc_basepath, 'COG_2014.tsv')
        domain_cat_names_path['COG']   = os.path.join(domain_desc_basepath, 'COG_2014_funcat.tsv')
        domain_fam_names_path['COG']   = os.path.join(domain_desc_basepath, 'COG_2014.tsv')
        domain_to_cat_map_path['PF']   = os.path.join(domain_desc_basepath, 'Pfam-A.clans.tsv')
        domain_cat_names_path['PF']    = os.path.join(domain_desc_basepath, 'Pfam-A.clans_names.tsv')
        domain_fam_names_path['PF']    = os.path.join(domain_desc_basepath, 'Pfam-A.clans.tsv')
        domain_to_cat_map_path['TIGR'] = os.path.join(domain_desc_basepath, 'TIGRInfo.tsv')
        domain_cat_names_path['TIGR']  = os.path.join(domain_desc_basepath, 'tigrrole2go.txt')
        #domain_fam_names_path['TIGR']  = os.path.join(domain_desc_basepath, 'tigrfams2go.txt')
        domain_fam_names_path['TIGR']  = os.path.join(domain_desc_basepath, 'TIGRInfo.tsv')
        domain_to_cat_map_path['SEED'] = os.path.join(domain_desc_basepath, 'SEED_subsys.txt')
        domain_cat_names_path['SEED']  = os.path.join(domain_desc_basepath, 'SEED_funcat.txt')
        #domain_cat_names_path['SEED']  = os.path.join(domain_desc_basepath, 'SEED_subsys.txt')
        domain_fam_names_path['SEED']  = os.path.join(domain_desc_basepath, 'SEED_subsys.txt')


        # load provenance
        provenance = [{}]
        if 'provenance' in ctx:
            provenance = ctx['provenance']
        provenance[0]['input_ws_objects']=[str(params['input_genomeSet_ref'])]


        # set the output path
        timestamp = int((datetime.utcnow() - datetime.utcfromtimestamp(0)).total_seconds()*1000)
        output_dir = os.path.join(self.scratch,'output.'+str(timestamp))
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)


        # configure categories
        #
        cats = []
        cat2name = dict()
        cat2group = dict()
        domfam2cat = dict()
        cat2domfams = dict()
        namespaces_reading = dict()

        # categories are high-level summations
        if params['namespace'] != 'custom':
            for namespace in ['COG','PF','TIGR','SEED']:
                if params['namespace'] == namespace:
                    namespaces_reading[namespace] = True

        # read all mappings between groups and domfams
        for namespace in ['COG','PF','TIGR','SEED']:

            cat2name[namespace] = dict()
            cat2group[namespace] = dict()
            domfam2cat[namespace] = dict()
            cat2domfams[namespace] = dict()

            # get high-level cats
            tigrrole_id2cat = dict()
            with open (domain_cat_names_path[namespace], 'r', 0) as dom_cat_handle:
                for line in dom_cat_handle.readlines():
                    line = line.strip()
                    
                    if namespace == 'COG':
                        [cat, cat_group, cat_name] = line.split("\t")[0:3]
                        if namespace == params['namespace'] and cat not in cats:
                            cats.append(cat)
                        cat2name[namespace][cat] = cat_name
                        cat2group[namespace][cat] = cat_group

                    elif namespace == 'PF':
                        [cat, cat_name] = line.split("\t")[0:2]
                        if namespace == params['namespace'] and cat not in cats:
                            cats.append(cat)
                        cat2name[namespace][cat] = cat_name
                        cat2group[namespace][cat] = None

                    elif namespace == 'TIGR':
                        if line.startswith('!'):
                            continue
                        [cat, cat_id, cat_group, cat_name_plus_go_terms] = line.split("\t")[0:4]
                        tigrrole_id2cat[cat_id] = cat
                        if namespace == params['namespace'] and cat not in cats:
                            cats.append(cat)
                        cat_name = re.sub (' *\> GO:.*$', '', cat_name_plus_go_terms)
                        cat2name[namespace][cat] = cat_name
                        cat2group[namespace][cat] = cat_group

                    elif namespace == 'SEED':
                        #[cat_group, cat_subgroup, cat, domfam] = line.split("\t")[0:4]
                        [cat_group, cat] = line.split("\t")[0:2]
                        if namespace == params['namespace'] and cat not in cats:
                            cats.append(cat)
                        cat_disp = re.sub ('_', ' ', cat)
                        cat2name[namespace][cat] = cat_disp
                        cat2group[namespace][cat] = cat_group

            # get domfam to cat map, and vice versa
            with open (domain_to_cat_map_path[namespace], 'r', 0) as dom2cat_map_handle:
                for line in dom2cat_map_handle.readlines():
                    line = line.strip()

                    if namespace == 'COG':
                        [domfam, cat_str, cat_name] = line.split("\t")[0:3]
                        cat = cat_str[0]  # only use first cat

                    elif namespace == 'PF':
                        [domfam, cat, cat_name, dom_id, dom_name] = line.split("\t")[0:5]

                    elif namespace == 'TIGR':
                        if line.startswith('!'):
                            continue
                        [domfam_id, domfam, cat_group, cat_id, domfam_name, ec_id, domfam_desc] = line.split("\t")[0:7]
                        if cat_id != '' and int(cat_id) != 0 and cat_id in tigrrole_id2cat:
                            cat = tigrrole_id2cat[cat_id]
                        else:
                            continue

                    elif namespace == 'SEED':
                        [cat_group, cat_subgroup, cat, domfam] = line.split("\t")[0:4]
                        domfam = domfam.strip()
                        domfam = re.sub (' *\#.*$', '', domfam)
                        domfam = re.sub (' *\(EC [\d\.\-\w]*\) *$', '', domfam)
                        domfam = re.sub (' *\(TC [\d\.\-\w]*\) *$', '', domfam)
                        domfam = re.sub (' ', '_', domfam)
                        domfam = 'SEED'+domfam

                    domfam2cat[namespace][domfam] = cat
                    if cat not in cat2domfams[namespace]:
                        cat2domfams[namespace][cat] = []
                    cat2domfams[namespace][cat].append(domfam)

        # custom domains
        if params['namespace'] == 'custom':

            # add target fams
            target_fams = []
            if 'target_fams' in params['custom_target_fams'] and params['custom_target_fams']['target_fams']:
                for target_fam in params['custom_target_fams']['target_fams']:
                    target_fam = target_fam.strip()
                    if target_fam == '':
                        continue

                    target_fam = re.sub ("^cog", "COG", target_fam, flags=re.IGNORECASE)
                    target_fam = re.sub ("^pf", "PF", target_fam, flags=re.IGNORECASE)
                    target_fam = re.sub ("^tigr", "TIGR", target_fam, flags=re.IGNORECASE)
                    target_fam = re.sub ("^seed", "SEED", target_fam, flags=re.IGNORECASE)
                    target_fam = re.sub ("^PFAM", "PF", target_fam, flags=re.IGNORECASE)
                    target_fam = re.sub ("^P-FAM", "PF", target_fam, flags=re.IGNORECASE)
                    target_fam = re.sub ("^P_FAM", "PF", target_fam, flags=re.IGNORECASE)
                    target_fam = re.sub ("^TIGRFAM", "TIGR", target_fam, flags=re.IGNORECASE)
                    target_fam = re.sub ("^TIGR-FAM", "TIGR", target_fam, flags=re.IGNORECASE)
                    target_fam = re.sub ("^TIGR_FAM", "TIGR", target_fam, flags=re.IGNORECASE)

                    target_fam = re.sub ("^COG:", "COG", target_fam, flags=re.IGNORECASE)
                    target_fam = re.sub ("^COG-", "COG", target_fam, flags=re.IGNORECASE)
                    target_fam = re.sub ("^COG_", "COG", target_fam, flags=re.IGNORECASE)
                    target_fam = re.sub ("^COG *", "COG", target_fam, flags=re.IGNORECASE)
                    target_fam = re.sub ("^PF:", "PF", target_fam, flags=re.IGNORECASE)
                    target_fam = re.sub ("^PF-", "PF", target_fam, flags=re.IGNORECASE)
                    target_fam = re.sub ("^PF_", "PF", target_fam, flags=re.IGNORECASE)
                    target_fam = re.sub ("^PF *", "PF", target_fam, flags=re.IGNORECASE)
                    target_fam = re.sub ("^TIGR:", "TIGR", target_fam, flags=re.IGNORECASE)
                    target_fam = re.sub ("^TIGR-", "TIGR", target_fam, flags=re.IGNORECASE)
                    target_fam = re.sub ("^TIGR_", "TIGR", target_fam, flags=re.IGNORECASE)
                    target_fam = re.sub ("^TIGR *", "TIGR", target_fam, flags=re.IGNORECASE)
                    target_fam = re.sub ("^SEED:", "SEED", target_fam, flags=re.IGNORECASE)
                    target_fam = re.sub ("^SEED-", "SEED", target_fam, flags=re.IGNORECASE)
                    target_fam = re.sub ("^SEED_", "SEED", target_fam, flags=re.IGNORECASE)
                    target_fam = re.sub ("^SEED *", "SEED", target_fam, flags=re.IGNORECASE)

                    num_id_len = dict()
                    num_id_len['COG'] = 4
                    num_id_len['PF'] = 5
                    num_id_len['TIGR'] = 5

                    #self.log (console, "TARGET_FAM A: '"+target_fam+"'")  # DEBUG
                    
                    if target_fam.startswith('SEED'):
                        namespaces_reading['SEED'] = True
                        target_fam = target_fam.strip()
                        target_fam = re.sub (' *\(EC [\d\.\-\w]*\) *$', '', target_fam)
                        target_fam = re.sub (' *\(TC [\d\.\-\w]*\) *$', '', target_fam)
                        target_fam = re.sub (' ', '_', target_fam)
                    else:
                        namespace_found = False
                        for namespace_iter in ['COG','PF','TIGR']:
                            if target_fam.startswith(namespace_iter):
                                this_namespace = namespace_iter
                                namespaces_reading[this_namespace] = True
                                target_fam = re.sub(this_namespace, "", target_fam)
                                namespace_found = True
                                break
                        if not namespace_found:
                            raise ValueError ("unrecognized custom domain family: '"+str(target_fam)+"'")
                        leading_zeros = ''
                        for c_i in range(num_id_len[this_namespace] - len(str(target_fam))):
                            leading_zeros += '0'
                        target_fam = this_namespace + leading_zeros + target_fam

                    #self.log (console, "TARGET_FAM B: '"+target_fam+"'")  # DEBUG

                    target_fams.append(target_fam)

            # add extra target fams
            extra_target_fams = []
            extra_target_fam_groups = []
            domfam2group = dict()
            for target_set in ['extra_target_fam_groups_COG', 'extra_target_fam_groups_PFAM', 'extra_target_fam_groups_TIGR', 'extra_target_fam_groups_SEED']:
                if target_set in params['custom_target_fams'] and params['custom_target_fams'][target_set]:
                    extra_target_fam_groups.extend (params['custom_target_fams'][target_set])

            if extra_target_fam_groups:
                for target_group in extra_target_fam_groups:
                    target_group = target_group.strip()
                    if target_group == '':
                        continue

                    namespace = re.sub (":.*$", "", target_group)
                    namespaces_reading[namespace] = True

                    if namespace == 'COG':
                        this_group = re.sub ("COG: ", "", target_group)
                        this_group = re.sub (":.*$", "", this_group)
                    elif namespace == 'PF':
                        this_group = re.sub ("PF: Clan ", "", target_group)
                        this_group = re.sub (":.*$", "", this_group)
                    elif namespace == 'TIGR':
                        this_group = re.sub ("TIGR: role:", "", target_group)
                        this_group = re.sub (":.*$", "", this_group)
                        this_group = 'TIGR_role:'+this_group
                    elif namespace == 'SEED':
                        this_group = re.sub ("SEED: ", "", target_group)

                    for domfam in cat2domfams[namespace][this_group]:
                        extra_target_fams.append(domfam)
                        domfam2group[domfam] = target_group

            # we have our targets
            cats = target_fams + extra_target_fams

            # store names of targets
            domfam2name = dict()
            for namespace in namespaces_reading.keys():
                domfam2name[namespace] = dict()

                if namespace == 'COG':
                    with open (domain_fam_names_path[namespace], 'r', 0) as dom_fam_handle:
                        for line in dom_fam_handle.readlines():
                            line = line.strip()
                            [domfam, cat_class, domfam_name] = line.split("\t")[0:3]
                            domfam2name[namespace][domfam] = domfam_name

                elif namespace == 'PF':
                    with open (domain_fam_names_path[namespace], 'r', 0) as dom_fam_handle:
                        for line in dom_fam_handle.readlines():
                            line = line.strip()
                            [domfam, class_id, class_name, domfam_id, domfam_name] = line.split("\t")[0:5]
                            if domfam_name.startswith(domfam_id):
                                combo_name = domfam_name
                            else:
                                combo_name = domfam_id+': '+domfam_name
                            domfam2name[namespace][domfam] = combo_name

                elif namespace == 'TIGR':
                    with open (domain_fam_names_path[namespace], 'r', 0) as dom_fam_handle:
                        for line in dom_fam_handle.readlines():
                            line = line.strip()
                            if line.startswith('!'):
                                continue
                            [domfam_id, domfam, cat_group, cat_id, domfam_name, ec_id, domfam_desc] = line.split("\t")[0:7]
                            if domfam_name != '':
                                if domfam_desc.startswith(domfam_name):
                                    combo_name = domfam_desc
                                else:
                                    combo_name = domfam_name+': '+domfam_desc
                            else:
                                if domfam_desc.startswith(domfam_id):
                                    combo_name = domfam_desc
                                else:
                                    combo_name = domfam_id+': '+domfam_desc
                            if ec_id != '':
                                combo_name += ' (EC '+ec_id+')'
                                    
                            domfam2name[namespace][domfam] = combo_name

                elif namespace == 'SEED':
                    with open (domain_fam_names_path[namespace], 'r', 0) as dom_fam_handle:
                        for line in dom_fam_handle.readlines():
                            line = line.strip()
                            [level1, level2, level3, domfam] = line.split("\t")[0:4]

                            domfam_desc = domfam
                            domfam = domfam.strip()
                            domfam = re.sub (' *\#.*$', '', domfam)
                            domfam = re.sub (' *\(EC [\d\.\-\w]*\) *$', '', domfam)
                            domfam = re.sub (' *\(TC [\d\.\-\w]*\) *$', '', domfam)
                            domfam = re.sub (' ', '_', domfam)
                            domfam = 'SEED'+domfam
                            if domfam in domfam2name[namespace]:
                                if len(domfam_desc) > len(domfam2name[namespace][domfam]):
                                    domfam2name[namespace][domfam] = domfam_desc
                            else:
                                domfam2name[namespace][domfam] = domfam_desc

        # just in case
        elif params['namespace'] != 'COG' \
                and params['namespace'] != 'PF' \
                and params['namespace'] != 'TIGR' \
                and params['namespace'] != 'SEED':
            raise ValueError ("Unknown namespace: '"+str(params['namespace'])+"'")


        # get genome set
        #
        input_ref = params['input_genomeSet_ref']
        try:
            [OBJID_I, NAME_I, TYPE_I, SAVE_DATE_I, VERSION_I, SAVED_BY_I, WSID_I, WORKSPACE_I, CHSUM_I, SIZE_I, META_I] = range(11)  # object_info tuple
            input_obj_info = wsClient.get_object_info_new ({'objects':[{'ref':input_ref}]})[0]
            input_obj_type = re.sub ('-[0-9]+\.[0-9]+$', "", input_obj_info[TYPE_I])  # remove trailing version
        except Exception as e:
            raise ValueError('Unable to get object from workspace: (' + input_ref +')' + str(e))
        accepted_input_types = ["KBaseSearch.GenomeSet" ]
        if input_obj_type not in accepted_input_types:
            raise ValueError ("Input object of type '"+input_obj_type+"' not accepted.  Must be one of "+", ".join(accepted_input_types))

        # get set obj
        try:
            genomeSet_obj = wsClient.get_objects([{'ref':input_ref}])[0]['data']
        except:
            raise ValueError ("unable to fetch genomeSet: "+input_ref)


        # get genome refs, object names, sci names, protein-coding gene counts, and SEED annot
        #
        genome_ids = genomeSet_obj['elements'].keys()  # note: genome_id may be meaningless
        genome_refs = []
        for genome_id in genome_ids:
            genome_refs.append (genomeSet_obj['elements'][genome_id]['ref'])

        genome_obj_name_by_ref = dict()
        genome_sci_name_by_ref = dict()
        genome_CDS_count_by_ref = dict()
        uniq_genome_ws_ids = dict()

        dom_hits = dict()  # initialize dom_hits here because reading SEED within genome
        genes_with_hits_cnt = dict()

        for genome_ref in genome_refs:

            dom_hits[genome_ref] = dict()
            genes_with_hits_cnt[genome_ref] = dict()

            # get genome object name
            input_ref = genome_ref
            try:
                [OBJID_I, NAME_I, TYPE_I, SAVE_DATE_I, VERSION_I, SAVED_BY_I, WSID_I, WORKSPACE_I, CHSUM_I, SIZE_I, META_I] = range(11)  # object_info tuple
                input_obj_info = wsClient.get_object_info_new ({'objects':[{'ref':input_ref}]})[0]
                input_obj_type = re.sub ('-[0-9]+\.[0-9]+$', "", input_obj_info[TYPE_I])  # remove trailing version
                input_name = input_obj_info[NAME_I]
                uniq_genome_ws_ids[input_obj_info[WSID_I]] = True

            except Exception as e:
                raise ValueError('Unable to get object from workspace: (' + input_ref +')' + str(e))
            accepted_input_types = ["KBaseGenomes.Genome" ]
            if input_obj_type not in accepted_input_types:
                raise ValueError ("Input object of type '"+input_obj_type+"' not accepted.  Must be one of "+", ".join(accepted_input_types))

            genome_obj_name_by_ref[genome_ref] = input_name

            try:
                genome_obj = wsClient.get_objects([{'ref':input_ref}])[0]['data']
            except:
                raise ValueError ("unable to fetch genome: "+input_ref)

            # sci name
            genome_sci_name_by_ref[genome_ref] = genome_obj['scientific_name']
            
            # CDS cnt
            cds_cnt = 0
            for feature in genome_obj['features']:
                if 'protein_translation' in feature and feature['protein_translation'] != None and feature['protein_translation'] != '':
                    cds_cnt += 1
            genome_CDS_count_by_ref[genome_ref] = cds_cnt

            # SEED annotations
            #
            #f_cnt = 0  # DEBUG
            if 'SEED' in namespaces_reading:
                for feature in genome_obj['features']:
                    #if f_cnt % 100 == 0:
                    #    self.log (console, "iterating features: "+str(f_cnt))  # DEBUG

                    if 'protein_translation' in feature and feature['protein_translation'] != None and feature['protein_translation'] != '':
                        #if f_cnt % 100 == 0:
                        #    self.log (console, "prot: "+str(feature['protein_translation']))  # DEBUG

                        if 'function' in feature and feature['function'] != None and feature['function'] != '':
                            gene_name = feature['id']
                            
                            #if f_cnt % 100 == 0:
                            #    self.log (console, "fxn: '"+str(feature['function'])+"'")  # DEBUG

                            # store assignments for gene
                            for namespace in ['SEED']:
                                if namespace not in genes_with_hits_cnt[genome_ref]:
                                    genes_with_hits_cnt[genome_ref][namespace] = 0
                                genes_with_hits_cnt[genome_ref][namespace] += 1

                                if gene_name not in dom_hits[genome_ref]:
                                    dom_hits[genome_ref][gene_name] = dict()
                                    dom_hits[genome_ref][gene_name][namespace] = dict()

                                domfam_list = []
                                annot_set = feature['function'].strip().split(';')
                                for annot in annot_set:
                                    annot_set_2 = annot.strip().split('@')
                                    for annot2 in annot_set_2:
                                        domfam = annot2.strip()
                                        domfam = re.sub (' *\#.*$', '', domfam)
                                        domfam = re.sub (' *\(EC [\d\.\-\w]*\) *$', '', domfam)
                                        domfam = re.sub (' *\(TC [\d\.\-\w]*\) *$', '', domfam)
                                        domfam = re.sub (' ', '_', domfam)
                                        domfam = 'SEED'+domfam
                                        domfam_list.append(domfam)
                                        #if f_cnt % 100 == 0:
                                        #    self.log (console, "domfam: '"+str(domfam)+"'")  # DEBUG

                                if top_hit_flag:  # does SEED give more than one function?
                                    dom_hits[genome_ref][gene_name][namespace][domfam_list[0]] = True
                                else:
                                    for domfam in domfam_list:
                                        dom_hits[genome_ref][gene_name][namespace][domfam] = True

                    #f_cnt += 1  # DEBUG


        # capture domain hits to genes within each namespace
        #
        if params['namespace'] != 'SEED':
            dom_annot_found = dict()

            KBASE_DOMAINHIT_GENE_ID_I        = 0
            KBASE_DOMAINHIT_GENE_BEG_I       = 1  # not used
            KBASE_DOMAINHIT_GENE_END_I       = 2  # not used
            KBASE_DOMAINHIT_GENE_STRAND_I    = 3  # not used
            KBASE_DOMAINHIT_GENE_HITS_DICT_I = 4
            KBASE_DOMAINHIT_GENE_HITS_DICT_BEG_J      = 0
            KBASE_DOMAINHIT_GENE_HITS_DICT_END_J      = 1
            KBASE_DOMAINHIT_GENE_HITS_DICT_EVALUE_J   = 2
            KBASE_DOMAINHIT_GENE_HITS_DICT_BITSCORE_J = 3
            KBASE_DOMAINHIT_GENE_HITS_DICT_ALNPERC_J  = 4

            # DEBUG
            #for genome_ref in genome_refs:
            #    self.log (console, "SEED ANNOT CNT A: '"+str(genes_with_hits_cnt[genome_ref]['SEED'])+"'")

            for ws_id in uniq_genome_ws_ids.keys():
                try:
                    dom_annot_obj_info_list = wsClient.list_objects({'ids':[ws_id],'type':"KBaseGeneFamilies.DomainAnnotation"})
                except Exception as e:
                    raise ValueError ("Unable to list DomainAnnotation objects from workspace: "+str(ws_id)+" "+str(e))

                for info in dom_annot_obj_info_list:
                    [OBJID_I, NAME_I, TYPE_I, SAVE_DATE_I, VERSION_I, SAVED_BY_I, WSID_I, WORKSPACE_I, CHSUM_I, SIZE_I, META_I] = range(11)  # object_info tuple
            
                    dom_annot_ref = str(info[WSID_I])+'/'+str(info[OBJID_I])+'/'+str(info[VERSION_I])
                    try:
                        domain_data = wsClient.get_objects([{'ref':dom_annot_ref}])[0]['data']
                    except:
                        raise ValueError ("unable to fetch domain annotation: "+dom_annot_ref)

                    # read domain data object
                    genome_ref = domain_data['genome_ref']
                    if genome_ref not in genome_refs:
                        continue
                    dom_annot_found[genome_ref] = True

                    if genome_ref not in dom_hits:
                        dom_hits[genome_ref] = dict()

                    if genome_ref not in genes_with_hits_cnt:
                        genes_with_hits_cnt[genome_ref] = dict()

                    for scaffold_id_iter in domain_data['data'].keys():
                        for CDS_domain_list in domain_data['data'][scaffold_id_iter]:
                            gene_ID   = CDS_domain_list[KBASE_DOMAINHIT_GENE_ID_I]
                            #gene_name = re.sub ('^'+genome_object_name+'.', '', gene_ID) 
                            gene_name = gene_ID
                            #(contig_name, gene_name) = (gene_ID[0:gene_ID.index(".")], gene_ID[gene_ID.index(".")+1:])
                            #print ("DOMAIN_HIT: "+contig_name+" "+gene_name)  # DEBUG
                            #print ("DOMAIN_HIT for gene: "+gene_name)  # DEBUG
                            #gene_beg       = CDS_domain_list[KBASE_DOMAINHIT_GENE_BEG_I]
                            #gene_end       = CDS_domain_list[KBASE_DOMAINHIT_GENE_END_I]
                            #gene_strand    = CDS_domain_list[KBASE_DOMAINHIT_GENE_STRAND_I]
                            gene_hits_dict = CDS_domain_list[KBASE_DOMAINHIT_GENE_HITS_DICT_I]

                            dom_hits_by_namespace       = dict()
                            top_hit_evalue_by_namespace = dict()
                            top_hit_dom_by_namespace    = dict()

                            for namespace in namespace_classes:
                                dom_hits_by_namespace[namespace] = dict()
                                top_hit_evalue_by_namespace[namespace] = 100
                                top_hit_dom_by_namespace[namespace] = None

                            for domfam in gene_hits_dict.keys():
                                if domfam.startswith('PF'):
                                    domfam_clean = re.sub('\.[^\.]*$','',domfam)
                                else:
                                    domfam_clean = domfam
                                known_namespace = False
                                for this_namespace in namespace_classes:
                                    if domfam.startswith(this_namespace):
                                        namespace = this_namespace
                                        known_namespace = True
                                if not known_namespace:
                                    continue

                                for hit in gene_hits_dict[domfam]:
                                    beg       = int(hit[KBASE_DOMAINHIT_GENE_HITS_DICT_BEG_J])
                                    end       = int(hit[KBASE_DOMAINHIT_GENE_HITS_DICT_END_J])
                                    e_value   = float(hit[KBASE_DOMAINHIT_GENE_HITS_DICT_EVALUE_J])
                                    bit_score = float(hit[KBASE_DOMAINHIT_GENE_HITS_DICT_BITSCORE_J])
                                    aln_perc  = float(hit[KBASE_DOMAINHIT_GENE_HITS_DICT_ALNPERC_J])

                                    if e_value_thresh != None and e_value > e_value_thresh:
                                        continue
                                    if top_hit_flag:
                                        if top_hit_dom_by_namespace[namespace] == None \
                                                or top_hit_evalue_by_namespace[namespace] > e_value:
                                            top_hit_dom_by_namespace[namespace] = domfam_clean
                                            top_hit_evalue_by_namespace[namespace] = e_value
                                        
                                    dom_hits_by_namespace[namespace][domfam_clean] = True

                            # store assignments for gene
                            for namespace in namespace_classes:
                                if namespace == 'SEED':
                                    continue
                                if namespace not in genes_with_hits_cnt[genome_ref]:
                                    genes_with_hits_cnt[genome_ref][namespace] = 0
                                if dom_hits_by_namespace[namespace]:
                                    genes_with_hits_cnt[genome_ref][namespace] += 1

                                    if gene_name not in dom_hits[genome_ref]:
                                        dom_hits[genome_ref][gene_name] = dict()
                                
                                    if top_hit_flag:
                                        dom_hits[genome_ref][gene_name][namespace] = { top_hit_dom_by_namespace[namespace]: True }
                                    else:
                                        dom_hits[genome_ref][gene_name][namespace] = dom_hits_by_namespace[namespace]

            # make sure we have domain annotations for all genomes
            missing_annot = []
            for genome_ref in genome_refs:
                if genome_ref not in dom_annot_found:
                    missing_annot.append('MISSING DOMAIN ANNOTATION FOR: '+genome_ref)
            if missing_annot:
                raise ValueError ("\n".join(missing_annot))
                                
        # DEBUG
        #for genome_ref in genome_refs:
        #    self.log (console, "SEED ANNOT CNT B: '"+str(genes_with_hits_cnt[genome_ref]['SEED'])+"'")

                                    
        # calculate table
        #
        table_data = dict()
        INSANE_VALUE = 10000000000000000
        overall_low_val  =  INSANE_VALUE
        overall_high_val = -INSANE_VALUE

        # count raw
        for genome_ref in genome_refs:
            if genome_ref not in table_data:
                table_data[genome_ref] = dict()
                for cat in cats:
                    table_data[genome_ref][cat] = 0

            # custom
            if params['namespace'] == 'custom':
                for cat in cats:
                    if cat.startswith('SEED'):
                        namespace = 'SEED'
                    else:
                        namespace = re.sub ('\d*$', '', cat)
                    for gene_name in dom_hits[genome_ref].keys():
                        if namespace in dom_hits[genome_ref][gene_name]:
                            if cat in dom_hits[genome_ref][gene_name][namespace]:
                                table_data[genome_ref][cat] += 1

            # high level summation
            else:
                namespace = params['namespace']
                for gene_name in dom_hits[genome_ref].keys():
                    if namespace in dom_hits[genome_ref][gene_name]:
                        for domfam in dom_hits[genome_ref][gene_name][namespace].keys():
                            #self.log(console, "DOMFAM: '"+str(domfam)+"'")  # DEBUG

                            if domfam in domfam2cat[namespace]:
                                cat = domfam2cat[namespace][domfam]
                                #self.log(console, "CAT: '"+str(cat)+"'")  # DEBUG
                                if cat in cats:
                                    #self.log(console, "CAT_FOUND: '"+str(cat)+"'")  # DEBUG
                                    table_data[genome_ref][cat] += 1
                
        # adjust to percs
        if params['count_category'].startswith('perc'):
            for genome_ref in genome_refs:
                for cat in cats:
                    if params['count_category'] == 'perc_annot':
                        if params['namespace'] == 'custom':
                            if cat.startswith('SEED'):
                                namespace = 'SEED'
                            else:
                                namespace = re.sub ('\d*$', '', cat)
                        else:
                            namespace = params['namespace']
                        total_genes = genes_with_hits_cnt[genome_ref][namespace]
                    else:
                        total_genes = genome_CDS_count_by_ref[genome_ref]

                    table_data[genome_ref][cat] /= float(total_genes)
                    table_data[genome_ref][cat] *= 100.0

        # determine high and low val
        for genome_ref in genome_refs:
            for cat in cats:
                val = table_data[genome_ref][cat]
                if val == 0:  continue
                #self.log (console, "HIGH VAL SCAN CAT: '"+cat+"' VAL: '"+str(val)+"'")  # DEBUG
                if 'log_base' in params and params['log_base'] != None and params['log_base'] != '':
                    log_base = float(params['log_base'])
                    if log_base <= 1.0:
                        raise ValueError ("log base must be > 1.0")
                    val = math.log(val, log_base)
                if val > overall_high_val:
                    overall_high_val = val
                if val < overall_low_val:
                    overall_low_val = val
        if overall_high_val == -INSANE_VALUE:
            raise ValueError ("unable to find any counts")


        # determine cats with a value and build group
        #
        cat_seen = dict()
        group_size = dict()
        group_size_with_blanks = dict()
        group_order = []
        group_order_with_blanks = []
        for cat in cats:
            cat_seen[cat] = False
        if params['namespace'] == 'custom':
            # get cats seen and group size
            for cat in cats:
                for genome_ref in genome_refs:
                    if cat in table_data[genome_ref] and table_data[genome_ref][cat] != 0:
                        cat_seen[cat] = True
                        cat_group = None
                        if extra_target_fam_groups:
                            if cat in domfam2group:
                                cat_group = domfam2group[cat]
                            else:
                                cat_group = 'N/A'
                        if cat_group != None:
                            if cat_group not in group_size:
                                group_order.append(cat_group)
                                group_size[cat_group] = 0
                            group_size[cat_group] += 1
                        break
            # get group size including blanks
            for cat in cats:
                cat_group = None
                if extra_target_fam_groups:
                    if cat in domfam2group:
                        cat_group = domfam2group[cat]
                    else:
                        cat_group = 'N/A'
                if cat_group != None:
                    if cat_group not in group_size_with_blanks:
                        group_order_with_blanks.append(cat_group)
                        group_size_with_blanks[cat_group] = 0
                    group_size_with_blanks[cat_group] += 1
        else:
            namespace = params['namespace']
            # get group size
            for cat in cats:
                for genome_ref in genome_refs:
                    if cat in table_data[genome_ref] and table_data[genome_ref][cat] != None and table_data[genome_ref][cat] != 0:
                        cat_seen[cat] = True
                        cat_group = cat2group[namespace][cat]
                        if cat_group != None:
                            if cat_group not in group_size:
                                group_order.append(cat_group)
                                group_size[cat_group] = 0
                            group_size[cat_group] += 1
                        break
            # get group size including blanks
            for cat in cats:
                cat_group = cat2group[namespace][cat]
                if cat_group != None:
                    if cat_group not in group_size_with_blanks:
                        group_order_with_blanks.append(cat_group)
                        group_size_with_blanks[cat_group] = 0
                    group_size_with_blanks[cat_group] += 1


        # build report
        #
        reportName = 'kb_phylogenomics_report_'+str(uuid.uuid4())
        reportObj = {'objects_created': [],
                     #'text_message': '',  # or is it 'message'?
                     'message': '',  # or is it 'text_message'?
                     'direct_html': '',
                     'direct_html_link_index': 0,
                     'file_links': [],
                     'html_links': [],
                     'workspace_name': params['workspace_name'],
                     'report_object_name': reportName
                     }


        # build html report
        sp = '&nbsp;'
        text_color   = "#606060"
        text_color_2 = "#606060"
        head_color_1 = "#eeeeee"
        head_color_2 = "#eeeeee"
        border_color = "#cccccc"
        border_cat_color = "#ffccff"
        #graph_color = "lightblue"
        #graph_width = 100
        #graph_char = "."
        graph_char = sp
        color_list = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e']
        max_color = len(color_list)-1
        cat_disp_trunc_len = 40
        cell_width = '10px'
        if len(genome_refs) > 20:
            graph_gen_fontsize = "1"
        elif len(genome_refs) > 10:
            graph_gen_fontsize = "2"
        else:
            graph_gen_fontsize = "3"
        if len(cats) > 20:
            graph_cat_fontsize = "1"
        elif len(cats) > 5:
            graph_cat_fontsize = "2"
        else:
            graph_cat_fontsize = "3"
        if int(graph_cat_fontsize) < int(graph_gen_fontsize):
            cell_fontsize = graph_gen_fontsize = graph_cat_fontsize
        else:
            cell_fontsize = graph_cat_fontsize = graph_gen_fontsize
        graph_padding = "5"
        graph_spacing = "3"
        #border = "1"
        border = "0"
        #row_spacing = "-2"
        num_rows = len(genome_refs)
        show_groups = False
        if len(group_order) > 0:  show_groups = True

        html_report_lines = []
        html_report_lines += ['<html>']
        html_report_lines += ['<head>']
        html_report_lines += ['<title>KBase Functional Domain Profile</title>']
        html_report_lines += ['<style>']
        html_report_lines += [".vertical-text {\ndisplay: inline-block;\noverflow: hidden;\nwidth: 0.65em;\n}\n.vertical-text__inner {\ndisplay: inline-block;\nwhite-space: nowrap;\nline-height: 1.1;\ntransform: translate(0,100%) rotate(-90deg);\ntransform-origin: 0 0;\n}\n.vertical-text__inner:after {\ncontent: \"\";\ndisplay: block;\nmargin: 0.0em 0 100%;\n}"]
        html_report_lines += [".vertical-text_title {\ndisplay: inline-block;\noverflow: hidden;\nwidth: 1.0em;\n}\n.vertical-text__inner_title {\ndisplay: inline-block;\nwhite-space: nowrap;\nline-height: 1.0;\ntransform: translate(0,100%) rotate(-90deg);\ntransform-origin: 0 0;\n}\n.vertical-text__inner_title:after {\ncontent: \"\";\ndisplay: block;\nmargin: 0.0em 0 100%;\n}"]
        html_report_lines += ['</style>']
        html_report_lines += ['</head>']
        html_report_lines += ['<body bgcolor="white">']

        # genomes as rows
        if 'vertical' in params and params['vertical'] == "1":
            # table header
            html_report_lines += ['<table cellpadding='+graph_padding+' cellspacing='+graph_spacing+' border='+border+'>']
            corner_rowspan = "1"
            if show_groups:  corner_rowspan = "2"
            label = ''
            if params['namespace'] != 'custom':
                label = params['namespace']
                if label == 'PF':
                    label = 'PFAM'
                elif label == 'TIGR':
                    label = 'TIGRFAM'
            html_report_lines += ['<tr><td valign=bottom align=right rowspan='+corner_rowspan+'><div class="vertical-text_title"><div class="vertical-text__inner_title"><font color="'+text_color+'">'+label+'</font></div></div></td>']
        
            # group headers
            if show_groups:
                for cat_group in group_order:
                    if cat_group.startswith('SEED'):
                        cat_group_disp = re.sub ('_',' ',cat_group)
                    else:
                        cat_group_disp = cat_group
                    cat_group_words = cat_group_disp.split()
                    max_group_width = 3*group_size[cat_group]
                    if len(cat_group) > max_group_width:
                        new_cat_group_words = []
                        sentence_len = 0
                        for w_i,word in enumerate(cat_group_words):
                            new_cat_group_words.append(word)
                            sentence_len += len(word)
                            if w_i < len(cat_group_words)-1:
                                if sentence_len + 1 + len(cat_group_words[w_i+1]) > max_group_width:
                                    new_cat_group_words[w_i] += '<br>'
                                    sentence_len = 0
                        cat_group_words = new_cat_group_words
                    if cat_group_words[0] == 'N/A':
                        cat_group_disp = ''
                    else:
                        cat_group_disp = " ".join(cat_group_words)

                    # DEBUG
                    #if cat_group not in group_size:
                    #    self.log(console, "CAT_GROUP: '"+str(cat_group)+"'")  # DEBUG
                    #    self.log(console, "CAT_GROUP_DISP: '"+str(cat_group_disp)+"'")  # DEBUG
                    #    for cg in group_size:
                    #        self.log(console, "CG: '"+str(cg)+"'")  # DEBUG

                    if cat_group_disp == '':
                        html_report_lines += ['<td bgcolor=white colspan='+str(group_size[cat_group])+'></td>']
                    else:
                        html_report_lines += ['<td style="border-right:solid 2px '+border_cat_color+'; border-bottom:solid 2px '+border_cat_color+'" bgcolor="'+head_color_1+'"valign=middle align=center colspan='+str(group_size[cat_group])+'><font color="'+text_color+'" size='+str(graph_cat_fontsize)+'><b>'+cat_group_disp+'</b></font></td>']

                html_report_lines += ['</tr><tr>']

            # column headers
            for cat in cats:
                if not cat_seen[cat] and not show_blanks:
                    continue
                if params['namespace'] == 'custom':
                    if cat.startswith('SEED'):
                        namespace = 'SEED'
                    else:
                        namespace = re.sub ("\d*$", "", cat)
                    cell_title = domfam2name[namespace][cat].strip()
                    cat_disp = cat
                    cat_disp = re.sub ('^SEED', 'SEED:', cat_disp)
                else:
                    cell_title = cat2name[params['namespace']][cat].strip()
                    cat_disp = cat
                    cat_disp = re.sub ("TIGR_", "", cat_disp)
                if len(cat_disp) > cat_disp_trunc_len+1:
                    cat_disp = cat_disp[0:cat_disp_trunc_len]+'*'
                html_report_lines += ['<td style="border-right:solid 2px '+border_cat_color+'; border-bottom:solid 2px '+border_cat_color+'" bgcolor="'+head_color_2+'"title="'+cell_title+'" valign=bottom align=center>']
                if params['namespace'] != 'COG':
                    html_report_lines += ['<div class="vertical-text"><div class="vertical-text__inner">']
                html_report_lines += ['<font color="'+text_color_2+'" size='+graph_cat_fontsize+'><b>']
                #for c_i,c in enumerate(cat_disp):
                #    if c_i < len(cat_disp)-1:
                #        html_report_lines += [c+'<br>']
                #    else:
                #        html_report_lines += [c]
                html_report_lines += [cat_disp]
                html_report_lines += ['</b></font>']
                if params['namespace'] != 'COG':
                    html_report_lines += ['</div></div>']
                html_report_lines += ['</td>']
            html_report_lines += ['</tr>']
            
            # rest of rows
            for genome_ref in genome_refs:
                genome_sci_name = genome_sci_name_by_ref[genome_ref]
                html_report_lines += ['<tr>']
                html_report_lines += ['<td align=right><font color="'+text_color+'" size='+graph_gen_fontsize+'><b><nobr>'+genome_sci_name+'</nobr></b></font></td>']
                for cat in cats:
                    if not cat_seen[cat] and not show_blanks:
                        continue
                    val = table_data[genome_ref][cat]
                    if val == 0:
                        cell_color = 'white'
                    else:                    
                        if 'log_base' in params and params['log_base'] != None and params['log_base'] != '':
                            log_base = float(params['log_base'])
                            if log_base <= 1.0:
                                raise ValueError ("log base must be > 1.0")
                            val = math.log(val, log_base)
                        cell_color_i = max_color - int(round(max_color * (val-overall_low_val) / float(overall_high_val-overall_low_val)))
                        c = color_list[cell_color_i]
                        cell_color = '#'+c+c+c+c+'FF'

                    if params['count_category'].startswith('perc'):
                        cell_val = str("%.3f"%table_data[genome_ref][cat])
                        cell_val += '%'
                    else:
                        cell_val = str(table_data[genome_ref][cat])

                    if 'heatmap' in params and params['heatmap'] == '1':
                        if table_data[genome_ref][cat] == 0:
                            this_text_color = text_color
                            #this_graph_char = "0"
                            this_graph_char = sp
                        else:
                            this_text_color = cell_color
                            this_graph_char = graph_char
                        html_report_lines += ['<td align=center valign=middle title="'+cell_val+'" style="width:'+cell_width+'" bgcolor="'+cell_color+'"><font color="'+this_text_color+'" size='+cell_fontsize+'>'+this_graph_char+'</font></td>']
                    else:
                        html_report_lines += ['<td align=center valign=middle style="'+cell_width+'; border-right:solid 2px '+border_color+'; border-bottom:solid 2px '+border_color+'"><font color="'+text_color+'" size='+cell_fontsize+'>'+cell_val+'</font></td>']

                html_report_lines += ['</tr>']
            html_report_lines += ['</table>']

        # genomes as columns
        else:
            raise ValueError ("Do not yet support Genomes as columns")


        # key table
        html_report_lines += ['<p>']
        html_report_lines += ['<table cellpadding=3 cellspacing=2 border='+border+'>']
        html_report_lines += ['<tr><td valign=middle align=left colspan=3 style="border-bottom:solid 4px '+border_color+'"><font color="'+text_color+'"><b>KEY</b></font></td></tr>']

        if show_groups:
            group_cat_i = 0
            for cat_group in group_order_with_blanks:
                if cat_group.startswith('SEED'):
                    cat_group_disp = re.sub ('_',' ',cat_group)
                else:
                    cat_group_disp = cat_group
                cat_group_words = cat_group_disp.split()
                if cat_group_words[0] == 'N/A':
                    cat_group_disp = ''
                else:
                    cat_group_disp = "&nbsp;<br>".join(cat_group_words)
                    cat_group_disp += sp

                html_report_lines += ['<tr>']
                if cat_group_disp == '':
                    html_report_lines += ['<td bgcolor=white rowspan='+str(group_size_with_blanks[cat_group])+' style="border-right:solid 4px '+border_color+'"></td>']
                else:
                    html_report_lines += ['<td style="border-right:solid 4px '+border_color+'" valign=top align=right rowspan='+str(group_size_with_blanks[cat_group])+'><font color="'+text_color+'" size='+str(graph_cat_fontsize)+'><b>'+cat_group_disp+'</b></font></td>']

                # add first cat for group
                first_cat = cats[group_cat_i]
                cell_color = 'white'
                #if not cat_seen[first_cat] and not show_blanks:
                if not cat_seen[first_cat]:
                    cell_color = "#eeeeee"
                if params['namespace'] == 'custom':
                    domfam = first_cat
                    if first_cat.startswith('SEED'):
                        namespace = 'SEED'
                    else:
                        namespace = re.sub ('\d*$', '', first_cat)
                    cat_disp = re.sub ('^SEED', 'SEED:', first_cat)
                    desc = domfam2name[namespace][domfam]
                else:
                    namespace = params['namespace']
                    cat_disp = first_cat
                    desc = cat2name[namespace][first_cat]
                if len(cat_disp) > cat_disp_trunc_len+1:
                    cat_disp = cat_disp[0:cat_disp_trunc_len]+'*'
                cat_disp = sp+cat_disp

                html_report_lines += ['<td valign=middle align=left bgcolor="'+cell_color+'" style="border-right:solid 4px '+border_color+'"><font color="'+text_color+'" size='+graph_cat_fontsize+'>'+cat_disp+'</font></td>']
                html_report_lines += ['<td valign=middle align=left bgcolor="'+cell_color+'"><font color="'+text_color+'" size='+graph_cat_fontsize+'>'+sp+desc+'</font></td>']
                html_report_lines += ['</tr>']

                group_cat_i += 1

                # add rest of cats in group
                for c_i in range(group_cat_i, group_cat_i+group_size_with_blanks[cat_group]-1):
                    cat = cats[c_i]
                    cell_color = 'white'
                    #if not cat_seen[cat] and not show_blanks:
                    if not cat_seen[cat]:
                        cell_color = "#eeeeee"
                    if params['namespace'] == 'custom':
                        domfam = cat
                        if cat.startswith('SEED'):
                            namespace = 'SEED'
                        else:
                            namespace = re.sub ('\d*$', '', cat)
                        cat_disp = re.sub ('^SEED', 'SEED:', cat)
                        desc = domfam2name[namespace][domfam]
                    else:
                        namespace = params['namespace']
                        cat_disp = cat
                        desc = cat2name[namespace][cat]
                    if len(cat_disp) > cat_disp_trunc_len+1:
                        cat_disp = cat_disp[0:cat_disp_trunc_len]+'*'
                    cat_disp = sp+cat_disp
                        
                    html_report_lines += ['<tr>']
                    html_report_lines += ['<td valign=middle align=left bgcolor="'+cell_color+'" style="border-right:solid 4px '+border_color+'"><font color="'+text_color+'" size='+graph_cat_fontsize+'>'+cat_disp+'</font></td>']
                    html_report_lines += ['<td valign=middle align=left bgcolor="'+cell_color+'"><font color="'+text_color+'" size='+graph_cat_fontsize+'>'+sp+desc+'</font></td>']
                    html_report_lines += ['</tr>']

                    group_cat_i += 1

        else:
            for cat in cats:
                cell_color = 'white'
                if not cat_seen[cat] and not show_blanks:
                    cell_color = "#eeeeee"
                if params['namespace'] == 'custom':
                    domfam = cat
                    if cat.startswith('SEED'):
                        namespace = 'SEED'
                    else:
                        namespace = re.sub ('\d*$', '', domfam)
                    cat_disp = re.sub ('^SEED', 'SEED:', cat)
                    desc = domfam2name[namespace][domfam]
                else:
                    namespace = params['namespace']
                    cat_disp = cat
                    desc = cat2name[namespace][cat]
                if len(cat_disp) > cat_disp_trunc_len+1:
                    cat_disp = cat_disp[0:cat_disp_trunc_len]+'*'
                html_report_lines += ['<tr>']
                html_report_lines += ['<td valign=middle align=left bgcolor="'+cell_color+'" style="border-right:solid 4px '+border_color+'><font color="'+text_color+'" size='+graph_cat_fontsize+'>'+cat_disp+'</font></td>']
                html_report_lines += ['<td valign=middle align=left bgcolor="'+cell_color+'"><font color="'+text_color+'" size='+graph_cat_fontsize+'>'+desc+'</font></td>']
                html_report_lines += ['</tr>']


        html_report_lines += ['</table>']

        # close
        html_report_lines += ['</body>']
        html_report_lines += ['</html>']
        
        html_report_str = "\n".join(html_report_lines)
        reportObj['direct_html'] = html_report_str


        # write html to file and upload
        html_file = os.path.join (output_dir, 'domain_profile_report.html')
        with open (html_file, 'w', 0) as html_handle:
            html_handle.write(html_report_str)
        dfu = DFUClient(self.callbackURL)
        try:
            upload_ret = dfu.file_to_shock({'file_path': html_file,
                                            'make_handle': 0,
                                            'pack': 'zip'})
        except:
            raise ValueError ('Logging exception loading html_report to shock')

        reportObj['html_links'] = [{'shock_id': upload_ret['shock_id'],
                                    'name': 'domain_profile_report.html',
                                    'label': 'Functional Domain Profile report'}
                                   ]


        # save report object
        #
        reportClient = KBaseReport(self.callbackURL, token=ctx['token'], service_ver=SERVICE_VER)
        #report_info = report.create({'report':reportObj, 'workspace_name':params['workspace_name']})
        report_info = reportClient.create_extended_report(reportObj)

        output = { 'report_name': report_info['name'], 'report_ref': report_info['ref'] }

        #END view_fxn_profile

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method view_fxn_profile return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]

    def view_fxn_profile_phylo(self, ctx, params):
        """
        :param params: instance of type "view_fxn_profile_phylo_Input"
           (view_fxn_profile_phylo() ** ** show a table/heatmap of general
           categories or custom gene families for a set of Genomes using the
           species tree) -> structure: parameter "workspace_name" of type
           "workspace_name" (** Common types), parameter
           "input_speciesTree_ref" of type "data_obj_ref", parameter
           "namespace" of String, parameter "custom_target_fams" of type
           "CustomTargetFams" (parameter groups) -> structure: parameter
           "target_fams" of list of String, parameter
           "extra_target_fam_groups_COG" of list of String, parameter
           "extra_target_fam_groups_PFAM" of list of String, parameter
           "extra_target_fam_groups_TIGR" of list of String, parameter
           "extra_target_fam_groups_SEED" of list of String, parameter
           "count_category" of String, parameter "heatmap" of type "bool",
           parameter "vertical" of type "bool", parameter "top_hit" of type
           "bool", parameter "e_value" of Double, parameter "log_base" of
           Double, parameter "show_blanks" of type "bool"
        :returns: instance of type "view_fxn_profile_phylo_Output" ->
           structure: parameter "report_name" of String, parameter
           "report_ref" of String
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN view_fxn_profile_phylo

        ### STEP 0: basic init
        console = []
        self.log(console, 'Running view_fxn_profile_phylo(): ')
        self.log(console, "\n"+pformat(params))

        token = ctx['token']
        wsClient = workspaceService(self.workspaceURL, token=token)
        headers = {'Authorization': 'OAuth '+token}
        env = os.environ.copy()
        env['KB_AUTH_TOKEN'] = token

        #SERVICE_VER = 'dev'  # DEBUG
        SERVICE_VER = 'release'

        # param checks
        required_params = ['input_speciesTree_ref',
                           'namespace'
                          ]
        for arg in required_params:
            if arg not in params or params[arg] == None or params[arg] == '':
                raise ValueError ("Must define required param: '"+arg+"'")

        if params['namespace'] == 'custom':
            if ('custom_target_fams' not in params or not params['custom_target_fams']) \
                    or ( \
                ('target_fams' not in params['custom_target_fams'] or not params['custom_target_fams']['target_fams']) \
                    and ('extra_target_fam_groups_COG' not in params['custom_target_fams'] or not params['custom_target_fams']['extra_target_fam_groups_COG']) \
                    and ('extra_target_fam_groups_PFAM' not in params['custom_target_fams'] or not params['custom_target_fams']['extra_target_fam_groups_PFAM']) \
                    and ('extra_target_fam_groups_TIGR' not in params['custom_target_fams'] or not params['custom_target_fams']['extra_target_fam_groups_TIGR']) \
                    and ('extra_target_fam_groups_SEED' not in params['custom_target_fams'] or not params['custom_target_fams']['extra_target_fam_groups_SEED'])
                ):
                    
                raise ValueError ("Must define either param: 'target_fams' or 'extra_target_fam_groups' if using CUSTOM targets")

        # base config
        namespace_classes = ['COG', 'PF', 'TIGR', 'SEED']
        show_blanks = False
        if 'show_blanks' in params and params['show_blanks'] == '1':
            show_blanks = True
        e_value_thresh = None
        if 'e_value' in params and params['e_value'] != None and params['e_value'] != '':
            e_value_thresh = float (params['e_value'])
        top_hit_flag = False
        if 'top_hit' in params and params['top_hit'] != None and params['top_hit'] != '' and params['top_hit'] != 0:
            top_hit_flag = True

        domain_desc_basepath           = os.path.abspath('/kb/module/data/domain_desc')
        domain_to_cat_map_path         = dict()
        domain_cat_names_path          = dict()
        domain_fam_names_path          = dict()
        domain_to_cat_map_path['COG']  = os.path.join(domain_desc_basepath, 'COG_2014.tsv')
        domain_cat_names_path['COG']   = os.path.join(domain_desc_basepath, 'COG_2014_funcat.tsv')
        domain_fam_names_path['COG']   = os.path.join(domain_desc_basepath, 'COG_2014.tsv')
        domain_to_cat_map_path['PF']   = os.path.join(domain_desc_basepath, 'Pfam-A.clans.tsv')
        domain_cat_names_path['PF']    = os.path.join(domain_desc_basepath, 'Pfam-A.clans_names.tsv')
        domain_fam_names_path['PF']    = os.path.join(domain_desc_basepath, 'Pfam-A.clans.tsv')
        domain_to_cat_map_path['TIGR'] = os.path.join(domain_desc_basepath, 'TIGRInfo.tsv')
        domain_cat_names_path['TIGR']  = os.path.join(domain_desc_basepath, 'tigrrole2go.txt')
        #domain_fam_names_path['TIGR']  = os.path.join(domain_desc_basepath, 'tigrfams2go.txt')
        domain_fam_names_path['TIGR']  = os.path.join(domain_desc_basepath, 'TIGRInfo.tsv')
        domain_to_cat_map_path['SEED'] = os.path.join(domain_desc_basepath, 'SEED_subsys.txt')
        domain_cat_names_path['SEED']  = os.path.join(domain_desc_basepath, 'SEED_funcat.txt')
        #domain_cat_names_path['SEED']  = os.path.join(domain_desc_basepath, 'SEED_subsys.txt')
        domain_fam_names_path['SEED']  = os.path.join(domain_desc_basepath, 'SEED_subsys.txt')


        # load provenance
        provenance = [{}]
        if 'provenance' in ctx:
            provenance = ctx['provenance']
        provenance[0]['input_ws_objects']=[str(params['input_speciesTree_ref'])]


        # set the output paths
        timestamp = int((datetime.utcnow() - datetime.utcfromtimestamp(0)).total_seconds()*1000)
        output_dir = os.path.join(self.scratch,'output.'+str(timestamp))
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        html_output_dir = os.path.join(output_dir,'html_output')
        if not os.path.exists(html_output_dir):
            os.makedirs(html_output_dir)


        # configure categories
        #
        cats = []
        cat2name = dict()
        cat2group = dict()
        domfam2cat = dict()
        cat2domfams = dict()
        namespaces_reading = dict()

        # categories are high-level summations
        if params['namespace'] != 'custom':
            for namespace in ['COG','PF','TIGR','SEED']:
                if params['namespace'] == namespace:
                    namespaces_reading[namespace] = True

        # read all mappings between groups and domfams
        for namespace in ['COG','PF','TIGR','SEED']:

            cat2name[namespace] = dict()
            cat2group[namespace] = dict()
            domfam2cat[namespace] = dict()
            cat2domfams[namespace] = dict()

            # get high-level cats
            tigrrole_id2cat = dict()
            with open (domain_cat_names_path[namespace], 'r', 0) as dom_cat_handle:
                for line in dom_cat_handle.readlines():
                    line = line.strip()
                    
                    if namespace == 'COG':
                        [cat, cat_group, cat_name] = line.split("\t")[0:3]
                        if namespace == params['namespace'] and cat not in cats:
                            cats.append(cat)
                        cat2name[namespace][cat] = cat_name
                        cat2group[namespace][cat] = cat_group

                    elif namespace == 'PF':
                        [cat, cat_name] = line.split("\t")[0:2]
                        if namespace == params['namespace'] and cat not in cats:
                            cats.append(cat)
                        cat2name[namespace][cat] = cat_name
                        cat2group[namespace][cat] = None

                    elif namespace == 'TIGR':
                        if line.startswith('!'):
                            continue
                        [cat, cat_id, cat_group, cat_name_plus_go_terms] = line.split("\t")[0:4]
                        tigrrole_id2cat[cat_id] = cat
                        if namespace == params['namespace'] and cat not in cats:
                            cats.append(cat)
                        cat_name = re.sub (' *\> GO:.*$', '', cat_name_plus_go_terms)
                        cat2name[namespace][cat] = cat_name
                        cat2group[namespace][cat] = cat_group

                        # DEBUG
                        #self.log(console, "CAT: '"+str(cat)+"' NAME: '"+str(cat_name)+"' GROUP: '"+str(cat_group)+"'")

                    elif namespace == 'SEED':
                        #[cat_group, cat_subgroup, cat, domfam] = line.split("\t")[0:4]
                        [cat_group, cat] = line.split("\t")[0:2]
                        if namespace == params['namespace'] and cat not in cats:
                            cats.append(cat)
                        cat_disp = re.sub ('_', ' ', cat)
                        cat2name[namespace][cat] = cat_disp
                        cat2group[namespace][cat] = cat_group

            # get domfam to cat map, and vice versa
            with open (domain_to_cat_map_path[namespace], 'r', 0) as dom2cat_map_handle:
                for line in dom2cat_map_handle.readlines():
                    line = line.strip()

                    if namespace == 'COG':
                        [domfam, cat_str, cat_name] = line.split("\t")[0:3]
                        cat = cat_str[0]  # only use first cat

                    elif namespace == 'PF':
                        [domfam, cat, cat_name, dom_id, dom_name] = line.split("\t")[0:5]

                    elif namespace == 'TIGR':
                        if line.startswith('!'):
                            continue
                        [domfam_id, domfam, cat_group, cat_id, domfam_name, ec_id, domfam_desc] = line.split("\t")[0:7]
                        if cat_id != '' and int(cat_id) != 0 and cat_id in tigrrole_id2cat:
                            cat = tigrrole_id2cat[cat_id]
                        else:
                            continue

                    elif namespace == 'SEED':
                        [cat_group, cat_subgroup, cat, domfam] = line.split("\t")[0:4]
                        domfam = domfam.strip()
                        domfam = re.sub (' *\#.*$', '', domfam)
                        domfam = re.sub (' *\(EC [\d\.\-\w]*\) *$', '', domfam)
                        domfam = re.sub (' *\(TC [\d\.\-\w]*\) *$', '', domfam)
                        domfam = re.sub (' ', '_', domfam)
                        domfam = 'SEED'+domfam

                    domfam2cat[namespace][domfam] = cat
                    if cat not in cat2domfams[namespace]:
                        cat2domfams[namespace][cat] = []
                    cat2domfams[namespace][cat].append(domfam)

        # custom domains
        if params['namespace'] == 'custom':

            # add target fams
            target_fams = []
            if 'target_fams' in params['custom_target_fams'] and params['custom_target_fams']['target_fams']:
                for target_fam in params['custom_target_fams']['target_fams']:
                    target_fam = target_fam.strip()
                    if target_fam == '':
                        continue

                    target_fam = re.sub ("^cog", "COG", target_fam, flags=re.IGNORECASE)
                    target_fam = re.sub ("^pf", "PF", target_fam, flags=re.IGNORECASE)
                    target_fam = re.sub ("^tigr", "TIGR", target_fam, flags=re.IGNORECASE)
                    target_fam = re.sub ("^seed", "SEED", target_fam, flags=re.IGNORECASE)
                    target_fam = re.sub ("^PFAM", "PF", target_fam, flags=re.IGNORECASE)
                    target_fam = re.sub ("^P-FAM", "PF", target_fam, flags=re.IGNORECASE)
                    target_fam = re.sub ("^P_FAM", "PF", target_fam, flags=re.IGNORECASE)
                    target_fam = re.sub ("^TIGRFAM", "TIGR", target_fam, flags=re.IGNORECASE)
                    target_fam = re.sub ("^TIGR-FAM", "TIGR", target_fam, flags=re.IGNORECASE)
                    target_fam = re.sub ("^TIGR_FAM", "TIGR", target_fam, flags=re.IGNORECASE)

                    target_fam = re.sub ("^COG:", "COG", target_fam, flags=re.IGNORECASE)
                    target_fam = re.sub ("^COG-", "COG", target_fam, flags=re.IGNORECASE)
                    target_fam = re.sub ("^COG_", "COG", target_fam, flags=re.IGNORECASE)
                    target_fam = re.sub ("^COG *", "COG", target_fam, flags=re.IGNORECASE)
                    target_fam = re.sub ("^PF:", "PF", target_fam, flags=re.IGNORECASE)
                    target_fam = re.sub ("^PF-", "PF", target_fam, flags=re.IGNORECASE)
                    target_fam = re.sub ("^PF_", "PF", target_fam, flags=re.IGNORECASE)
                    target_fam = re.sub ("^PF *", "PF", target_fam, flags=re.IGNORECASE)
                    target_fam = re.sub ("^TIGR:", "TIGR", target_fam, flags=re.IGNORECASE)
                    target_fam = re.sub ("^TIGR-", "TIGR", target_fam, flags=re.IGNORECASE)
                    target_fam = re.sub ("^TIGR_", "TIGR", target_fam, flags=re.IGNORECASE)
                    target_fam = re.sub ("^TIGR *", "TIGR", target_fam, flags=re.IGNORECASE)
                    target_fam = re.sub ("^SEED:", "SEED", target_fam, flags=re.IGNORECASE)
                    target_fam = re.sub ("^SEED-", "SEED", target_fam, flags=re.IGNORECASE)
                    target_fam = re.sub ("^SEED_", "SEED", target_fam, flags=re.IGNORECASE)
                    target_fam = re.sub ("^SEED *", "SEED", target_fam, flags=re.IGNORECASE)

                    num_id_len = dict()
                    num_id_len['COG'] = 4
                    num_id_len['PF'] = 5
                    num_id_len['TIGR'] = 5

                    #self.log (console, "TARGET_FAM A: '"+target_fam+"'")  # DEBUG
                    
                    if target_fam.startswith('SEED'):
                        namespaces_reading['SEED'] = True
                        target_fam = target_fam.strip()
                        target_fam = re.sub (' *\(EC [\d\.\-\w]*\) *$', '', target_fam)
                        target_fam = re.sub (' *\(TC [\d\.\-\w]*\) *$', '', target_fam)
                        target_fam = re.sub (' ', '_', target_fam)
                    else:
                        namespace_found = False
                        for namespace_iter in ['COG','PF','TIGR']:
                            if target_fam.startswith(namespace_iter):
                                this_namespace = namespace_iter
                                namespaces_reading[this_namespace] = True
                                target_fam = re.sub(this_namespace, "", target_fam)
                                namespace_found = True
                                break
                        if not namespace_found:
                            raise ValueError ("unrecognized custom domain family: '"+str(target_fam)+"'")
                        leading_zeros = ''
                        for c_i in range(num_id_len[this_namespace] - len(str(target_fam))):
                            leading_zeros += '0'
                        target_fam = this_namespace + leading_zeros + target_fam

                    #self.log (console, "TARGET_FAM B: '"+target_fam+"'")  # DEBUG

                    target_fams.append(target_fam)

            # add extra target fams
            extra_target_fams = []
            extra_target_fam_groups = []
            domfam2group = dict()
            for target_set in ['extra_target_fam_groups_COG', 'extra_target_fam_groups_PFAM', 'extra_target_fam_groups_TIGR', 'extra_target_fam_groups_SEED']:
                if target_set in params['custom_target_fams'] and params['custom_target_fams'][target_set]:
                    extra_target_fam_groups.extend (params['custom_target_fams'][target_set])

            if extra_target_fam_groups:
                for target_group in extra_target_fam_groups:
                    target_group = target_group.strip()
                    if target_group == '':
                        continue

                    namespace = re.sub (":.*$", "", target_group)
                    namespaces_reading[namespace] = True

                    if namespace == 'COG':
                        this_group = re.sub ("COG: ", "", target_group)
                        this_group = re.sub (":.*$", "", this_group)
                    elif namespace == 'PF':
                        this_group = re.sub ("PF: Clan ", "", target_group)
                        this_group = re.sub (":.*$", "", this_group)
                    elif namespace == 'TIGR':
                        this_group = re.sub ("TIGR: role:", "", target_group)
                        this_group = re.sub (":.*$", "", this_group)
                        this_group = 'TIGR_role:'+this_group
                    elif namespace == 'SEED':
                        this_group = re.sub ("SEED: ", "", target_group)

                    for domfam in cat2domfams[namespace][this_group]:
                        extra_target_fams.append(domfam)
                        domfam2group[domfam] = target_group

            # we have our targets
            cats = target_fams + extra_target_fams

            # store names of targets
            domfam2name = dict()
            for namespace in namespaces_reading.keys():
                domfam2name[namespace] = dict()

                if namespace == 'COG':
                    with open (domain_fam_names_path[namespace], 'r', 0) as dom_fam_handle:
                        for line in dom_fam_handle.readlines():
                            line = line.strip()
                            [domfam, cat_class, domfam_name] = line.split("\t")[0:3]
                            domfam2name[namespace][domfam] = domfam_name

                elif namespace == 'PF':
                    with open (domain_fam_names_path[namespace], 'r', 0) as dom_fam_handle:
                        for line in dom_fam_handle.readlines():
                            line = line.strip()
                            [domfam, class_id, class_name, domfam_id, domfam_name] = line.split("\t")[0:5]
                            if domfam_name.startswith(domfam_id):
                                combo_name = domfam_name
                            else:
                                combo_name = domfam_id+': '+domfam_name
                            domfam2name[namespace][domfam] = combo_name

                elif namespace == 'TIGR':
                    with open (domain_fam_names_path[namespace], 'r', 0) as dom_fam_handle:
                        for line in dom_fam_handle.readlines():
                            line = line.strip()
                            if line.startswith('!'):
                                continue
                            [domfam_id, domfam, cat_group, cat_id, domfam_name, ec_id, domfam_desc] = line.split("\t")[0:7]
                            if domfam_name != '':
                                if domfam_desc.startswith(domfam_name):
                                    combo_name = domfam_desc
                                else:
                                    combo_name = domfam_name+': '+domfam_desc
                            else:
                                if domfam_desc.startswith(domfam_id):
                                    combo_name = domfam_desc
                                else:
                                    combo_name = domfam_id+': '+domfam_desc
                            if ec_id != '':
                                combo_name += ' (EC '+ec_id+')'
                                    
                            domfam2name[namespace][domfam] = combo_name

                elif namespace == 'SEED':
                    with open (domain_fam_names_path[namespace], 'r', 0) as dom_fam_handle:
                        for line in dom_fam_handle.readlines():
                            line = line.strip()
                            [level1, level2, level3, domfam] = line.split("\t")[0:4]

                            domfam_desc = domfam
                            domfam = domfam.strip()
                            domfam = re.sub (' *\#.*$', '', domfam)
                            domfam = re.sub (' *\(EC [\d\.\-\w]*\) *$', '', domfam)
                            domfam = re.sub (' *\(TC [\d\.\-\w]*\) *$', '', domfam)
                            domfam = re.sub (' ', '_', domfam)
                            domfam = 'SEED'+domfam
                            if domfam in domfam2name[namespace]:
                                if len(domfam_desc) > len(domfam2name[namespace][domfam]):
                                    domfam2name[namespace][domfam] = domfam_desc
                            else:
                                domfam2name[namespace][domfam] = domfam_desc

        # just in case
        elif params['namespace'] != 'COG' \
                and params['namespace'] != 'PF' \
                and params['namespace'] != 'TIGR' \
                and params['namespace'] != 'SEED':
            raise ValueError ("Unknown namespace: '"+str(params['namespace'])+"'")


        # get speciesTree
        #
        input_ref = params['input_speciesTree_ref']
        speciesTree_name = None
        try:
            [OBJID_I, NAME_I, TYPE_I, SAVE_DATE_I, VERSION_I, SAVED_BY_I, WSID_I, WORKSPACE_I, CHSUM_I, SIZE_I, META_I] = range(11)  # object_info tuple
            input_obj_info = wsClient.get_object_info_new ({'objects':[{'ref':input_ref}]})[0]
            input_obj_type = re.sub ('-[0-9]+\.[0-9]+$', "", input_obj_info[TYPE_I])  # remove trailing version
            speciesTree_name = input_obj_info[NAME_I]
        except Exception as e:
            raise ValueError('Unable to get object from workspace: (' + input_ref +')' + str(e))
        accepted_input_types = ["KBaseTrees.Tree" ]
        if input_obj_type not in accepted_input_types:
            raise ValueError ("Input object of type '"+input_obj_type+"' not accepted.  Must be one of "+", ".join(accepted_input_types))

        # get set obj
        try:
            speciesTree_obj = wsClient.get_objects([{'ref':input_ref}])[0]['data']
        except:
            raise ValueError ("unable to fetch speciesTree: "+input_ref)


        # get genome_refs from speciesTree and instantiate ETE3 tree and order
        #
        genome_refs = []
        genome_id_by_ref = dict()
        genome_ref_by_id = dict()
        for genome_id in speciesTree_obj['default_node_labels'].keys():
            genome_ref = speciesTree_obj['ws_refs'][genome_id]['g'][0]
            genome_id_by_ref[genome_ref] = genome_id
            genome_ref_by_id[genome_id] = genome_ref

        species_tree = ete3.Tree(speciesTree_obj['tree'])
        species_tree.ladderize()
        for genome_id in species_tree.get_leaf_names():
            genome_refs.append(genome_ref_by_id[genome_id])


        # get object names, sci names, protein-coding gene counts, and SEED annot
        #
        genome_obj_name_by_ref = dict()
        genome_sci_name_by_ref = dict()
        genome_sci_name_by_id  = dict()
        genome_CDS_count_by_ref = dict()
        uniq_genome_ws_ids = dict()

        dom_hits = dict()  # initialize dom_hits here because reading SEED within genome
        genes_with_hits_cnt = dict()

        for genome_ref in genome_refs:

            dom_hits[genome_ref] = dict()
            genes_with_hits_cnt[genome_ref] = dict()

            # get genome object name
            input_ref = genome_ref
            try:
                [OBJID_I, NAME_I, TYPE_I, SAVE_DATE_I, VERSION_I, SAVED_BY_I, WSID_I, WORKSPACE_I, CHSUM_I, SIZE_I, META_I] = range(11)  # object_info tuple
                input_obj_info = wsClient.get_object_info_new ({'objects':[{'ref':input_ref}]})[0]
                input_obj_type = re.sub ('-[0-9]+\.[0-9]+$', "", input_obj_info[TYPE_I])  # remove trailing version
                input_name = input_obj_info[NAME_I]
                uniq_genome_ws_ids[input_obj_info[WSID_I]] = True

            except Exception as e:
                raise ValueError('Unable to get object from workspace: (' + input_ref +')' + str(e))
            accepted_input_types = ["KBaseGenomes.Genome" ]
            if input_obj_type not in accepted_input_types:
                raise ValueError ("Input object of type '"+input_obj_type+"' not accepted.  Must be one of "+", ".join(accepted_input_types))

            genome_obj_name_by_ref[genome_ref] = input_name

            try:
                genome_obj = wsClient.get_objects([{'ref':input_ref}])[0]['data']
            except:
                raise ValueError ("unable to fetch genome: "+input_ref)

            # sci name
            genome_sci_name_by_ref[genome_ref] = genome_obj['scientific_name']
            genome_sci_name_by_id[genome_id_by_ref[genome_ref]] = genome_obj['scientific_name']
            
            # CDS cnt
            cds_cnt = 0
            for feature in genome_obj['features']:
                if 'protein_translation' in feature and feature['protein_translation'] != None and feature['protein_translation'] != '':
                    cds_cnt += 1
            genome_CDS_count_by_ref[genome_ref] = cds_cnt

            # SEED annotations
            #
            #f_cnt = 0  # DEBUG
            if 'SEED' in namespaces_reading:
                for feature in genome_obj['features']:
                    #if f_cnt % 100 == 0:
                    #    self.log (console, "iterating features: "+str(f_cnt))  # DEBUG

                    if 'protein_translation' in feature and feature['protein_translation'] != None and feature['protein_translation'] != '':
                        #if f_cnt % 100 == 0:
                        #    self.log (console, "prot: "+str(feature['protein_translation']))  # DEBUG

                        if 'function' in feature and feature['function'] != None and feature['function'] != '':
                            gene_name = feature['id']
                            
                            #if f_cnt % 100 == 0:
                            #    self.log (console, "fxn: '"+str(feature['function'])+"'")  # DEBUG

                            # store assignments for gene
                            for namespace in ['SEED']:
                                if namespace not in genes_with_hits_cnt[genome_ref]:
                                    genes_with_hits_cnt[genome_ref][namespace] = 0
                                genes_with_hits_cnt[genome_ref][namespace] += 1

                                if gene_name not in dom_hits[genome_ref]:
                                    dom_hits[genome_ref][gene_name] = dict()
                                    dom_hits[genome_ref][gene_name][namespace] = dict()

                                domfam_list = []
                                annot_set = feature['function'].strip().split(';')
                                for annot in annot_set:
                                    annot_set_2 = annot.strip().split('@')
                                    for annot2 in annot_set_2:
                                        domfam = annot2.strip()
                                        domfam = re.sub (' *\#.*$', '', domfam)
                                        domfam = re.sub (' *\(EC [\d\.\-\w]*\) *$', '', domfam)
                                        domfam = re.sub (' *\(TC [\d\.\-\w]*\) *$', '', domfam)
                                        domfam = re.sub (' ', '_', domfam)
                                        domfam = 'SEED'+domfam
                                        domfam_list.append(domfam)
                                        #if f_cnt % 100 == 0:
                                        #    self.log (console, "domfam: '"+str(domfam)+"'")  # DEBUG

                                if top_hit_flag:  # does SEED give more than one function?
                                    dom_hits[genome_ref][gene_name][namespace][domfam_list[0]] = True
                                else:
                                    for domfam in domfam_list:
                                        dom_hits[genome_ref][gene_name][namespace][domfam] = True

                    #f_cnt += 1  # DEBUG


        # capture domain hits to genes within each namespace
        #
        if params['namespace'] != 'SEED':
            dom_annot_found = dict()

            KBASE_DOMAINHIT_GENE_ID_I        = 0
            KBASE_DOMAINHIT_GENE_BEG_I       = 1  # not used
            KBASE_DOMAINHIT_GENE_END_I       = 2  # not used
            KBASE_DOMAINHIT_GENE_STRAND_I    = 3  # not used
            KBASE_DOMAINHIT_GENE_HITS_DICT_I = 4
            KBASE_DOMAINHIT_GENE_HITS_DICT_BEG_J      = 0
            KBASE_DOMAINHIT_GENE_HITS_DICT_END_J      = 1
            KBASE_DOMAINHIT_GENE_HITS_DICT_EVALUE_J   = 2
            KBASE_DOMAINHIT_GENE_HITS_DICT_BITSCORE_J = 3
            KBASE_DOMAINHIT_GENE_HITS_DICT_ALNPERC_J  = 4

            # DEBUG
            #for genome_ref in genome_refs:
            #    self.log (console, "SEED ANNOT CNT A: '"+str(genes_with_hits_cnt[genome_ref]['SEED'])+"'")

            for ws_id in uniq_genome_ws_ids.keys():
                try:
                    dom_annot_obj_info_list = wsClient.list_objects({'ids':[ws_id],'type':"KBaseGeneFamilies.DomainAnnotation"})
                except Exception as e:
                    raise ValueError ("Unable to list DomainAnnotation objects from workspace: "+str(ws_id)+" "+str(e))

                for info in dom_annot_obj_info_list:
                    [OBJID_I, NAME_I, TYPE_I, SAVE_DATE_I, VERSION_I, SAVED_BY_I, WSID_I, WORKSPACE_I, CHSUM_I, SIZE_I, META_I] = range(11)  # object_info tuple
            
                    dom_annot_ref = str(info[WSID_I])+'/'+str(info[OBJID_I])+'/'+str(info[VERSION_I])
                    try:
                        domain_data = wsClient.get_objects([{'ref':dom_annot_ref}])[0]['data']
                    except:
                        raise ValueError ("unable to fetch domain annotation: "+dom_annot_ref)

                    # read domain data object
                    genome_ref = domain_data['genome_ref']
                    if genome_ref not in genome_refs:
                        continue
                    dom_annot_found[genome_ref] = True

                    if genome_ref not in dom_hits:
                        dom_hits[genome_ref] = dict()

                    if genome_ref not in genes_with_hits_cnt:
                        genes_with_hits_cnt[genome_ref] = dict()

                    for scaffold_id_iter in domain_data['data'].keys():
                        for CDS_domain_list in domain_data['data'][scaffold_id_iter]:
                            gene_ID   = CDS_domain_list[KBASE_DOMAINHIT_GENE_ID_I]
                            #gene_name = re.sub ('^'+genome_object_name+'.', '', gene_ID) 
                            gene_name = gene_ID
                            #(contig_name, gene_name) = (gene_ID[0:gene_ID.index(".")], gene_ID[gene_ID.index(".")+1:])
                            #print ("DOMAIN_HIT: "+contig_name+" "+gene_name)  # DEBUG
                            #print ("DOMAIN_HIT for gene: "+gene_name)  # DEBUG
                            #gene_beg       = CDS_domain_list[KBASE_DOMAINHIT_GENE_BEG_I]
                            #gene_end       = CDS_domain_list[KBASE_DOMAINHIT_GENE_END_I]
                            #gene_strand    = CDS_domain_list[KBASE_DOMAINHIT_GENE_STRAND_I]
                            gene_hits_dict = CDS_domain_list[KBASE_DOMAINHIT_GENE_HITS_DICT_I]

                            dom_hits_by_namespace       = dict()
                            top_hit_evalue_by_namespace = dict()
                            top_hit_dom_by_namespace    = dict()

                            for namespace in namespace_classes:
                                dom_hits_by_namespace[namespace] = dict()
                                top_hit_evalue_by_namespace[namespace] = 100
                                top_hit_dom_by_namespace[namespace] = None

                            for domfam in gene_hits_dict.keys():
                                if domfam.startswith('PF'):
                                    domfam_clean = re.sub('\.[^\.]*$','',domfam)
                                else:
                                    domfam_clean = domfam
                                known_namespace = False
                                for this_namespace in namespace_classes:
                                    if domfam.startswith(this_namespace):
                                        namespace = this_namespace
                                        known_namespace = True
                                if not known_namespace:
                                    continue

                                for hit in gene_hits_dict[domfam]:
                                    beg       = int(hit[KBASE_DOMAINHIT_GENE_HITS_DICT_BEG_J])
                                    end       = int(hit[KBASE_DOMAINHIT_GENE_HITS_DICT_END_J])
                                    e_value   = float(hit[KBASE_DOMAINHIT_GENE_HITS_DICT_EVALUE_J])
                                    bit_score = float(hit[KBASE_DOMAINHIT_GENE_HITS_DICT_BITSCORE_J])
                                    aln_perc  = float(hit[KBASE_DOMAINHIT_GENE_HITS_DICT_ALNPERC_J])

                                    if e_value_thresh != None and e_value > e_value_thresh:
                                        continue
                                    if top_hit_flag:
                                        if top_hit_dom_by_namespace[namespace] == None \
                                                or top_hit_evalue_by_namespace[namespace] > e_value:
                                            top_hit_dom_by_namespace[namespace] = domfam_clean
                                            top_hit_evalue_by_namespace[namespace] = e_value
                                        
                                    dom_hits_by_namespace[namespace][domfam_clean] = True

                            # store assignments for gene
                            for namespace in namespace_classes:
                                if namespace == 'SEED':
                                    continue
                                if namespace not in genes_with_hits_cnt[genome_ref]:
                                    genes_with_hits_cnt[genome_ref][namespace] = 0
                                if dom_hits_by_namespace[namespace]:
                                    genes_with_hits_cnt[genome_ref][namespace] += 1

                                    if gene_name not in dom_hits[genome_ref]:
                                        dom_hits[genome_ref][gene_name] = dict()
                                
                                    if top_hit_flag:
                                        dom_hits[genome_ref][gene_name][namespace] = { top_hit_dom_by_namespace[namespace]: True }
                                    else:
                                        dom_hits[genome_ref][gene_name][namespace] = dom_hits_by_namespace[namespace]
                                
            # make sure we have domain annotations for all genomes
            missing_annot = []
            for genome_ref in genome_refs:
                if genome_ref not in dom_annot_found:
                    missing_annot.append('MISSING DOMAIN ANNOTATION FOR: '+genome_ref)
            if missing_annot:
                raise ValueError ("\n".join(missing_annot))
                                
        # DEBUG
        #for genome_ref in genome_refs:
        #    self.log (console, "SEED ANNOT CNT B: '"+str(genes_with_hits_cnt[genome_ref]['SEED'])+"'")

                                    
        # calculate table
        #
        table_data = dict()
        INSANE_VALUE = 10000000000000000
        overall_low_val  =  INSANE_VALUE
        overall_high_val = -INSANE_VALUE

        # count raw
        for genome_ref in genome_refs:
            if genome_ref not in table_data:
                table_data[genome_ref] = dict()
                for cat in cats:
                    table_data[genome_ref][cat] = 0

            # custom
            if params['namespace'] == 'custom':
                for cat in cats:
                    if cat.startswith('SEED'):
                        namespace = 'SEED'
                    else:
                        namespace = re.sub ('\d*$', '', cat)
                    for gene_name in dom_hits[genome_ref].keys():
                        if namespace in dom_hits[genome_ref][gene_name]:
                            if cat in dom_hits[genome_ref][gene_name][namespace]:
                                table_data[genome_ref][cat] += 1

            # high level summation
            else:
                namespace = params['namespace']
                for gene_name in dom_hits[genome_ref].keys():
                    if namespace in dom_hits[genome_ref][gene_name]:
                        for domfam in dom_hits[genome_ref][gene_name][namespace].keys():
                            #self.log(console, "DOMFAM: '"+str(domfam)+"'")  # DEBUG

                            if domfam in domfam2cat[namespace]:
                                cat = domfam2cat[namespace][domfam]
                                #self.log(console, "CAT: '"+str(cat)+"'")  # DEBUG
                                if cat in cats:
                                    #self.log(console, "CAT_FOUND: '"+str(cat)+"'")  # DEBUG
                                    table_data[genome_ref][cat] += 1
                
        # adjust to percs
        if params['count_category'].startswith('perc'):
            for genome_ref in genome_refs:

                # DEBUG
                #sci_name = genome_sci_name_by_ref[genome_ref]
                #try:
                #    total_genes = genes_with_hits_cnt[genome_ref]['COG']
                #    print (sci_name +" ("+genome_ref+"): COG OK")
                #except:
                #    print (sci_name +" ("+genome_ref+"): COG MISSING")

                for cat in cats:
                    if params['count_category'] == 'perc_annot':
                        if params['namespace'] == 'custom':
                            if cat.startswith('SEED'):
                                namespace = 'SEED'
                            else:
                                namespace = re.sub ('\d*$', '', cat)
                        else:
                            namespace = params['namespace']
                        total_genes = genes_with_hits_cnt[genome_ref][namespace]
                    else:
                        total_genes = genome_CDS_count_by_ref[genome_ref]

                    table_data[genome_ref][cat] /= float(total_genes)
                    table_data[genome_ref][cat] *= 100.0

        # determine high and low val
        for genome_ref in genome_refs:
            for cat in cats:
                val = table_data[genome_ref][cat]
                if val == 0:  continue
                #self.log (console, "HIGH VAL SCAN CAT: '"+cat+"' VAL: '"+str(val)+"'")  # DEBUG
                if 'log_base' in params and params['log_base'] != None and params['log_base'] != '':
                    log_base = float(params['log_base'])
                    if log_base <= 1.0:
                        raise ValueError ("log base must be > 1.0")
                    val = math.log(val, log_base)
                if val > overall_high_val:
                    overall_high_val = val
                if val < overall_low_val:
                    overall_low_val = val
        if overall_high_val == -INSANE_VALUE:
            raise ValueError ("unable to find any counts")


        # determine cats with a value and build group
        #
        cat_seen = dict()
        group_size = dict()
        group_size_with_blanks = dict()
        group_order = []
        group_order_with_blanks = []
        for cat in cats:
            cat_seen[cat] = False
        if params['namespace'] == 'custom':
            # get group size
            for cat in cats:
                for genome_ref in genome_refs:
                    if cat in table_data[genome_ref] and table_data[genome_ref][cat] != 0:
                        cat_seen[cat] = True
                        cat_group = None
                        if extra_target_fam_groups:
                            if cat in domfam2group:
                                cat_group = domfam2group[cat]
                            else:
                                cat_group = 'N/A'
                        if cat_group != None:
                            if cat_group not in group_size:
                                group_order.append(cat_group)
                                group_size[cat_group] = 0
                            group_size[cat_group] += 1
                        break
            # get group size including blanks
            for cat in cats:
                cat_group = None
                if extra_target_fam_groups:
                    if cat in domfam2group:
                        cat_group = domfam2group[cat]
                    else:
                        cat_group = 'N/A'
                if cat_group != None:
                    if cat_group not in group_size_with_blanks:
                        group_order_with_blanks.append(cat_group)
                        group_size_with_blanks[cat_group] = 0
                    group_size_with_blanks[cat_group] += 1
        else:
            namespace = params['namespace']
            # get group size
            for cat in cats:
                for genome_ref in genome_refs:
                    if cat in table_data[genome_ref] and table_data[genome_ref][cat] != None and table_data[genome_ref][cat] != 0:
                        cat_seen[cat] = True
                        cat_group = cat2group[namespace][cat]
                        if cat_group != None:
                            if cat_group not in group_size:
                                group_order.append(cat_group)
                                group_size[cat_group] = 0
                            group_size[cat_group] += 1
                        break
            # get group size including blanks
            for cat in cats:
                cat_group = cat2group[namespace][cat]
                if cat_group != None:
                    if cat_group not in group_size_with_blanks:
                        group_order_with_blanks.append(cat_group)
                        group_size_with_blanks[cat_group] = 0
                    group_size_with_blanks[cat_group] += 1


        # Draw tree (we already instantiated Tree above)
        #
        png_file = speciesTree_name+'.png'
        pdf_file = speciesTree_name+'.pdf'
        output_png_file_path = os.path.join(html_output_dir, png_file);
        output_pdf_file_path = os.path.join(html_output_dir, pdf_file);

        # init ETE3 accessory objects
        ts = ete3.TreeStyle()

        # customize
        ts.show_leaf_name = True
        ts.show_branch_length = False
        ts.show_branch_support = True
        #ts.scale = 50 # 50 pixels per branch length unit
        ts.branch_vertical_margin = 5 # pixels between adjacent branches
        #ts.title.add_face(ete3.TextFace(params['output_name']+": "+params['desc'], fsize=10), column=0)

        node_style = ete3.NodeStyle()
        node_style["fgcolor"] = "#606060"  # for node balls
        node_style["size"] = 10  # for node balls (gets reset based on support)
        node_style["vt_line_color"] = "#606060"
        node_style["hz_line_color"] = "#606060"
        node_style["vt_line_width"] = 2
        node_style["hz_line_width"] = 2
        node_style["vt_line_type"] = 0 # 0 solid, 1 dashed, 2 dotted
        node_style["hz_line_type"] = 0

        leaf_style = ete3.NodeStyle()
        leaf_style["fgcolor"] = "#ffffff"  # for node balls
        leaf_style["size"] = 2  # for node balls (we're using it to add space)
        leaf_style["vt_line_color"] = "#606060"  # unecessary
        leaf_style["hz_line_color"] = "#606060"
        leaf_style["vt_line_width"] = 2
        leaf_style["hz_line_width"] = 2
        leaf_style["vt_line_type"] = 0 # 0 solid, 1 dashed, 2 dotted
        leaf_style["hz_line_type"] = 0

        for n in species_tree.traverse():
            if n.is_leaf():
                style = leaf_style
                genome_id = n.name
                #n.name = genome_sci_name_by_id[genome_id]
                n.name = None
                leaf_name_disp = genome_sci_name_by_id[genome_id]
                n.add_face(ete3.TextFace(leaf_name_disp, fsize=10), column=0, position="branch-right")
            else:
                style = ete3.NodeStyle()
                for k in node_style.keys():
                    style[k] = node_style[k]

                if n.support > 0.95:
                    style["size"] = 6
                elif n.support > 0.90:
                    style["size"] = 5
                elif n.support > 0.80:
                    style["size"] = 4
                else:
                    style["size"] = 2

            n.set_style(style)

        # save images
        dpi = 300
        img_units = "in"
        img_pix_width = 1200
        img_in_width = round(float(img_pix_width)/float(dpi), 1)
        img_html_width = img_pix_width // 2
        species_tree.render(output_png_file_path, w=img_in_width, units=img_units, dpi=dpi, tree_style=ts)
        species_tree.render(output_pdf_file_path, w=img_in_width, units=img_units, tree_style=ts)  # dpi irrelevant


        # build report
        #
        reportName = 'kb_phylogenomics_report_'+str(uuid.uuid4())
        reportObj = {'objects_created': [],
                     #'text_message': '',  # or is it 'message'?
                     'message': '',  # or is it 'text_message'?
                     'direct_html': '',
                     'direct_html_link_index': 0,
                     'file_links': [],
                     'html_links': [],
                     'workspace_name': params['workspace_name'],
                     'report_object_name': reportName
                     }


        # build html report
        sp = '&nbsp;'
        text_color   = "#606060"
        text_color_2 = "#606060"
        head_color_1 = "#eeeeee"
        head_color_2 = "#eeeeee"
        border_color = "#cccccc"
        border_cat_color = "#ffccff"
        #graph_color = "lightblue"
        #graph_width = 100
        #graph_char = "."
        graph_char = sp
        color_list = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e']
        max_color = len(color_list)-1
        cat_disp_trunc_len = 40
        cell_width = '10px'
        tree_scale_factor = 22.625
        tree_img_height = int(tree_scale_factor*len(genome_refs))
        extra_tree_rows = 3
        if len(genome_refs) > 20:
            graph_gen_fontsize = "1"
        elif len(genome_refs) > 10:
            graph_gen_fontsize = "2"
        else:
            graph_gen_fontsize = "3"
        if len(cats) > 20:
            graph_cat_fontsize = "1"
        elif len(cats) > 5:
            graph_cat_fontsize = "2"
        else:
            graph_cat_fontsize = "3"
        if int(graph_cat_fontsize) < int(graph_gen_fontsize):
            cell_fontsize = graph_gen_fontsize = graph_cat_fontsize
        else:
            cell_fontsize = graph_cat_fontsize = graph_gen_fontsize
        #graph_padding = "5"
        graph_padding = "2"
        graph_spacing = "3"
        #border = "1"
        border = "0"
        #row_spacing = "-2"
        num_rows = len(genome_refs)
        show_groups = False
        if len(group_order) > 0:  show_groups = True

        html_report_lines = []
        html_report_lines += ['<html>']
        html_report_lines += ['<head>']
        html_report_lines += ['<title>KBase Functional Domain Profile with Species Tree</title>']
        html_report_lines += ['<style>']
        html_report_lines += [".vertical-text {\ndisplay: inline-block;\noverflow: hidden;\nwidth: 0.65em;\n}\n.vertical-text__inner {\ndisplay: inline-block;\nwhite-space: nowrap;\nline-height: 1.1;\ntransform: translate(0,100%) rotate(-90deg);\ntransform-origin: 0 0;\n}\n.vertical-text__inner:after {\ncontent: \"\";\ndisplay: block;\nmargin: 0.0em 0 100%;\n}"]
        html_report_lines += [".vertical-text_title {\ndisplay: inline-block;\noverflow: hidden;\nwidth: 1.0em;\n}\n.vertical-text__inner_title {\ndisplay: inline-block;\nwhite-space: nowrap;\nline-height: 1.0;\ntransform: translate(0,100%) rotate(-90deg);\ntransform-origin: 0 0;\n}\n.vertical-text__inner_title:after {\ncontent: \"\";\ndisplay: block;\nmargin: 0.0em 0 100%;\n}"]
        html_report_lines += ['</style>']
        html_report_lines += ['</head>']
        html_report_lines += ['<body bgcolor="white">']

        # genomes as rows
        if 'vertical' in params and params['vertical'] == "1":
            # table header
            html_report_lines += ['<table cellpadding='+graph_padding+' cellspacing='+graph_spacing+' border='+border+'>']
            corner_rowspan = "1"
            if show_groups:  corner_rowspan = "2"
            label = ''
            if params['namespace'] != 'custom':
                label = params['namespace']
                if label == 'PF':
                    label = 'PFAM'
                elif label == 'TIGR':
                    label = 'TIGRFAM'
            html_report_lines += ['<tr><td valign=bottom align=right rowspan='+corner_rowspan+'><div class="vertical-text_title"><div class="vertical-text__inner_title"><font color="'+text_color+'">'+label+'</font></div></div></td>']
        
            # group headers
            if show_groups:
                for cat_group in group_order:
                    if cat_group.startswith('SEED'):
                        cat_group_disp = re.sub ('_',' ',cat_group)
                    else:
                        cat_group_disp = cat_group
                    cat_group_words = cat_group_disp.split()
                    max_group_width = 3*group_size[cat_group]
                    if len(cat_group) > max_group_width:
                        new_cat_group_words = []
                        sentence_len = 0
                        for w_i,word in enumerate(cat_group_words):
                            new_cat_group_words.append(word)
                            sentence_len += len(word)
                            if w_i < len(cat_group_words)-1:
                                if sentence_len + 1 + len(cat_group_words[w_i+1]) > max_group_width:
                                    new_cat_group_words[w_i] += '<br>'
                                    sentence_len = 0
                        cat_group_words = new_cat_group_words
                    if cat_group_words[0] == 'N/A':
                        cat_group_disp = ''
                    else:
                        cat_group_disp = " ".join(cat_group_words)

                    # DEBUG
                    #if cat_group not in group_size:
                    #    self.log(console, "CAT_GROUP: '"+str(cat_group)+"'")  # DEBUG
                    #    self.log(console, "CAT_GROUP_DISP: '"+str(cat_group_disp)+"'")  # DEBUG
                    #    for cg in group_size:
                    #        self.log(console, "CG: '"+str(cg)+"'")  # DEBUG

                    if cat_group_disp == '':
                        html_report_lines += ['<td bgcolor=white colspan='+str(group_size[cat_group])+'></td>']
                    else:
                        html_report_lines += ['<td style="border-right:solid 2px '+border_cat_color+'; border-bottom:solid 2px '+border_cat_color+'" bgcolor="'+head_color_1+'"valign=middle align=center colspan='+str(group_size[cat_group])+'><font color="'+text_color+'" size='+str(graph_cat_fontsize)+'><b>'+cat_group_disp+'</b></font></td>']

                html_report_lines += ['</tr><tr>']

            # column headers
            for cat in cats:
                if not cat_seen[cat] and not show_blanks:
                    continue
                if params['namespace'] == 'custom':
                    if cat.startswith('SEED'):
                        namespace = 'SEED'
                    else:
                        namespace = re.sub ("\d*$", "", cat)
                    cell_title = domfam2name[namespace][cat].strip()
                    cat_disp = cat
                    cat_disp = re.sub ('^SEED', 'SEED:', cat_disp)
                else:
                    cell_title = cat2name[params['namespace']][cat].strip()
                    cat_disp = cat
                    cat_disp = re.sub ("TIGR_", "", cat_disp)
                if len(cat_disp) > cat_disp_trunc_len+1:
                    cat_disp = cat_disp[0:cat_disp_trunc_len]+'*'
                html_report_lines += ['<td style="border-right:solid 2px '+border_cat_color+'; border-bottom:solid 2px '+border_cat_color+'" bgcolor="'+head_color_2+'"title="'+cell_title+'" valign=bottom align=center>']
                if params['namespace'] != 'COG':
                    html_report_lines += ['<div class="vertical-text"><div class="vertical-text__inner">']
                html_report_lines += ['<font color="'+text_color_2+'" size='+graph_cat_fontsize+'><b>']
                #for c_i,c in enumerate(cat_disp):
                #    if c_i < len(cat_disp)-1:
                #        html_report_lines += [c+'<br>']
                #    else:
                #        html_report_lines += [c]
                html_report_lines += [cat_disp]
                html_report_lines += ['</b></font>']
                if params['namespace'] != 'COG':
                    html_report_lines += ['</div></div>']
                html_report_lines += ['</td>']
            html_report_lines += ['</tr>']
            
            # add tree image
            html_report_lines += ['<tr><td align="left" valign="top" rowspan='+str(len(genome_refs)+extra_tree_rows)+'><img src="'+png_file+'" height='+str(tree_img_height)+'></td>']

            # rest of rows
            for row_i,genome_ref in enumerate(genome_refs):
                genome_sci_name = genome_sci_name_by_ref[genome_ref]
                if row_i > 0:
                    html_report_lines += ['<tr>']
                #html_report_lines += ['<td align=right><font color="'+text_color+'" size='+graph_gen_fontsize+'><b><nobr>'+genome_sci_name+'</nobr></b></font></td>']
                for cat in cats:
                    if not cat_seen[cat] and not show_blanks:
                        continue
                    val = table_data[genome_ref][cat]
                    if val == 0:
                        cell_color = 'white'
                    else:                    
                        if 'log_base' in params and params['log_base'] != None and params['log_base'] != '':
                            log_base = float(params['log_base'])
                            if log_base <= 1.0:
                                raise ValueError ("log base must be > 1.0")
                            val = math.log(val, log_base)
                        cell_color_i = max_color - int(round(max_color * (val-overall_low_val) / float(overall_high_val-overall_low_val)))
                        c = color_list[cell_color_i]
                        cell_color = '#'+c+c+c+c+'FF'

                    if params['count_category'].startswith('perc'):
                        cell_val = str("%.3f"%table_data[genome_ref][cat])
                        cell_val += '%'
                    else:
                        cell_val = str(table_data[genome_ref][cat])

                    if 'heatmap' in params and params['heatmap'] == '1':
                        if table_data[genome_ref][cat] == 0:
                            this_text_color = text_color
                            #this_graph_char = "0"
                            this_graph_char = sp
                        else:
                            this_text_color = cell_color
                            this_graph_char = graph_char
                        html_report_lines += ['<td align=center valign=middle title="'+cell_val+'" style="width:'+cell_width+'" bgcolor="'+cell_color+'"><font color="'+this_text_color+'" size='+cell_fontsize+'>'+this_graph_char+'</font></td>']
                    else:
                        html_report_lines += ['<td align=center valign=middle style="'+cell_width+'; border-right:solid 2px '+border_color+'; border-bottom:solid 2px '+border_color+'"><font color="'+text_color+'" size='+cell_fontsize+'>'+cell_val+'</font></td>']

                html_report_lines += ['</tr>']
            # add extra blank rows to extend tree rule below grid
            for row_i in range(extra_tree_rows):
                html_report_lines += ['<tr><td bgcolor="white" style="width:10px"><font color="white" size='+cell_fontsize+'>'+sp+'</font></td></tr>']

            html_report_lines += ['</table>']

        # genomes as columns
        else:
            raise ValueError ("Do not yet support Genomes as columns")


        # key table
        html_report_lines += ['<p>']
        html_report_lines += ['<table cellpadding=3 cellspacing=2 border='+border+'>']
        html_report_lines += ['<tr><td valign=middle align=left colspan=3 style="border-bottom:solid 4px '+border_color+'"><font color="'+text_color+'"><b>KEY</b></font></td></tr>']

        if show_groups:
            group_cat_i = 0
            for cat_group in group_order_with_blanks:
                if cat_group.startswith('SEED'):
                    cat_group_disp = re.sub ('_',' ',cat_group)
                else:
                    cat_group_disp = cat_group
                cat_group_words = cat_group_disp.split()
                if cat_group_words[0] == 'N/A':
                    cat_group_disp = ''
                else:
                    cat_group_disp = "&nbsp;<br>".join(cat_group_words)
                    cat_group_disp += sp

                html_report_lines += ['<tr>']
                if cat_group_disp == '':
                    html_report_lines += ['<td bgcolor=white rowspan='+str(group_size_with_blanks[cat_group])+' style="border-right:solid 4px '+border_color+'"></td>']
                else:
                    html_report_lines += ['<td style="border-right:solid 4px '+border_color+'" valign=top align=right rowspan='+str(group_size_with_blanks[cat_group])+'><font color="'+text_color+'" size='+str(graph_cat_fontsize)+'><b>'+cat_group_disp+'</b></font></td>']


                # DEBUG
                #self.log (console, "CAT GROUP: '"+cat_group+"' SIZE: '"+str(group_size_with_blanks[cat_group])+"'")

                # add first cat for group
                first_cat = cats[group_cat_i]
                cell_color = 'white'
                #if not cat_seen[first_cat] and not show_blanks:
                if not cat_seen[first_cat]:
                    cell_color = "#eeeeee"
                if params['namespace'] == 'custom':
                    domfam = first_cat
                    if first_cat.startswith('SEED'):
                        namespace = 'SEED'
                    else:
                        namespace = re.sub ('\d*$', '', first_cat)
                    cat_disp = re.sub ('^SEED', 'SEED:', first_cat)
                    desc = domfam2name[namespace][domfam]
                else:
                    namespace = params['namespace']
                    cat_disp = first_cat
                    desc = cat2name[namespace][first_cat]
                if len(cat_disp) > cat_disp_trunc_len+1:
                    cat_disp = cat_disp[0:cat_disp_trunc_len]+'*'
                cat_disp = sp+cat_disp

                html_report_lines += ['<td valign=middle align=left bgcolor="'+cell_color+'" style="border-right:solid 4px '+border_color+'"><font color="'+text_color+'" size='+graph_cat_fontsize+'>'+cat_disp+'</font></td>']
                html_report_lines += ['<td valign=middle align=left bgcolor="'+cell_color+'"><font color="'+text_color+'" size='+graph_cat_fontsize+'>'+sp+desc+'</font></td>']
                html_report_lines += ['</tr>']

                group_cat_i += 1

                # add rest of cats in group
                for c_i in range(group_cat_i, group_cat_i+group_size_with_blanks[cat_group]-1):
                    cat = cats[c_i]
                    cell_color = 'white'
                    #if not cat_seen[cat] and not show_blanks:
                    if not cat_seen[cat]:
                        cell_color = "#eeeeee"
                    if params['namespace'] == 'custom':
                        domfam = cat
                        if cat.startswith('SEED'):
                            namespace = 'SEED'
                        else:
                            namespace = re.sub ('\d*$', '', cat)
                        cat_disp = re.sub ('^SEED', 'SEED:', cat)
                        desc = domfam2name[namespace][domfam]
                    else:
                        namespace = params['namespace']
                        cat_disp = cat
                        desc = cat2name[namespace][cat]
                    if len(cat_disp) > cat_disp_trunc_len+1:
                        cat_disp = cat_disp[0:cat_disp_trunc_len]+'*'
                    cat_disp = sp+cat_disp
                        
                    html_report_lines += ['<tr>']
                    html_report_lines += ['<td valign=middle align=left bgcolor="'+cell_color+'" style="border-right:solid 4px '+border_color+'"><font color="'+text_color+'" size='+graph_cat_fontsize+'>'+cat_disp+'</font></td>']
                    html_report_lines += ['<td valign=middle align=left bgcolor="'+cell_color+'"><font color="'+text_color+'" size='+graph_cat_fontsize+'>'+sp+desc+'</font></td>']
                    html_report_lines += ['</tr>']

                    group_cat_i += 1

        else:
            for cat in cats:
                cell_color = 'white'
                if not cat_seen[cat] and not show_blanks:
                    cell_color = "#eeeeee"
                if params['namespace'] == 'custom':
                    domfam = cat
                    if cat.startswith('SEED'):
                        namespace = 'SEED'
                    else:
                        namespace = re.sub ('\d*$', '', domfam)
                    cat_disp = re.sub ('^SEED', 'SEED:', cat)
                    desc = domfam2name[namespace][domfam]
                else:
                    namespace = params['namespace']
                    cat_disp = cat
                    desc = cat2name[namespace][cat]
                if len(cat_disp) > cat_disp_trunc_len+1:
                    cat_disp = cat_disp[0:cat_disp_trunc_len]+'*'
                html_report_lines += ['<tr>']
                html_report_lines += ['<td valign=middle align=left bgcolor="'+cell_color+'" style="border-right:solid 4px '+border_color+'><font color="'+text_color+'" size='+graph_cat_fontsize+'>'+cat_disp+'</font></td>']
                html_report_lines += ['<td valign=middle align=left bgcolor="'+cell_color+'"><font color="'+text_color+'" size='+graph_cat_fontsize+'>'+desc+'</font></td>']
                html_report_lines += ['</tr>']


        html_report_lines += ['</table>']

        # close
        html_report_lines += ['</body>']
        html_report_lines += ['</html>']
        
        html_report_str = "\n".join(html_report_lines)
        #reportObj['direct_html'] = html_report_str


        # write html to file and upload
        html_file = os.path.join (html_output_dir, 'domain_profile_report.html')
        with open (html_file, 'w', 0) as html_handle:
            html_handle.write(html_report_str)
        dfu = DFUClient(self.callbackURL)
        try:
            #upload_ret = dfu.file_to_shock({'file_path': html_file,
            upload_ret = dfu.file_to_shock({'file_path': html_output_dir,
                                            'make_handle': 0,
                                            'pack': 'zip'})
        except:
            raise ValueError ('Logging exception loading html_report to shock')

        reportObj['html_links'] = [{'shock_id': upload_ret['shock_id'],
                                    'name': 'domain_profile_report.html',
                                    'label': 'Functional Domain Profile report'}
                                   ]
        reportObj['direct_html_link_index'] = 0


        # save report object
        #
        reportClient = KBaseReport(self.callbackURL, token=ctx['token'], service_ver=SERVICE_VER)
        #report_info = report.create({'report':reportObj, 'workspace_name':params['workspace_name']})
        report_info = reportClient.create_extended_report(reportObj)

        output = { 'report_name': report_info['name'], 'report_ref': report_info['ref'] }

        #END view_fxn_profile_phylo

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method view_fxn_profile_phylo return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]

    def view_genome_circle_plot(self, ctx, params):
        """
        :param params: instance of type "view_genome_circle_plot_Input"
           (view_genome_circle_plot() ** ** build a circle plot of a
           microbial genome) -> structure: parameter "workspace_name" of type
           "workspace_name" (** Common types), parameter "input_genome_ref"
           of type "data_obj_ref"
        :returns: instance of type "view_genome_circle_plot_Output" ->
           structure: parameter "report_name" of String, parameter
           "report_ref" of String
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN view_genome_circle_plot
        #END view_genome_circle_plot

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method view_genome_circle_plot return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]

    def view_pan_circle_plot(self, ctx, params):
        """
        :param params: instance of type "view_pan_circle_plot_Input"
           (view_pan_circle_plot() ** ** build a circle plot of a microbial
           genome with its pangenome members) -> structure: parameter
           "workspace_name" of type "workspace_name" (** Common types),
           parameter "input_genome_ref" of type "data_obj_ref", parameter
           "input_pangenome_ref" of type "data_obj_ref", parameter
           "input_compare_genome_refs" of type "data_obj_ref"
        :returns: instance of type "view_pan_circle_plot_Output" ->
           structure: parameter "report_name" of String, parameter
           "report_ref" of String
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN view_pan_circle_plot

        ### STEP 0: basic init
        console = []
        self.log(console, 'Running view_pan_circle_plot(): ')
        self.log(console, "\n"+pformat(params))

        token = ctx['token']
        wsClient = workspaceService(self.workspaceURL, token=token)
        headers = {'Authorization': 'OAuth '+token}
        env = os.environ.copy()
        env['KB_AUTH_TOKEN'] = token

        #SERVICE_VER = 'dev'  # DEBUG
        SERVICE_VER = 'release'

        # param checks
        required_params = ['input_genome_ref',
                           'input_pangenome_ref'
                          ]
        for arg in required_params:
            if arg not in params or params[arg] == None or params[arg] == '':
                raise ValueError ("Must define required param: '"+arg+"'")


        # load provenance
        provenance = [{}]
        if 'provenance' in ctx:
            provenance = ctx['provenance']
        provenance[0]['input_ws_objects']=[str(params['input_genome_ref']),
                                           str(params['input_pangenome_ref'])
                                           ]


        # set the output paths
        timestamp = int((datetime.utcnow() - datetime.utcfromtimestamp(0)).total_seconds()*1000)
        output_dir = os.path.join(self.scratch,'output.'+str(timestamp))
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        html_output_dir = os.path.join(output_dir,'html_output')
        if not os.path.exists(html_output_dir):
            os.makedirs(html_output_dir)


        # get base genome
        #
        base_genome_ref = input_ref = params['input_genome_ref']
        base_genome_obj_name = None
        try:
            [OBJID_I, NAME_I, TYPE_I, SAVE_DATE_I, VERSION_I, SAVED_BY_I, WSID_I, WORKSPACE_I, CHSUM_I, SIZE_I, META_I] = range(11)  # object_info tuple
            input_obj_info = wsClient.get_object_info_new ({'objects':[{'ref':input_ref}]})[0]
            input_obj_type = re.sub ('-[0-9]+\.[0-9]+$', "", input_obj_info[TYPE_I])  # remove trailing version
            base_genome_obj_name = input_obj_info[NAME_I]
        except Exception as e:
            raise ValueError('Unable to get object from workspace: (' + input_ref +')' + str(e))
        accepted_input_types = ["KBaseGenomes.Genome" ]
        if input_obj_type not in accepted_input_types:
            raise ValueError ("Input object of type '"+input_obj_type+"' not accepted.  Must be one of "+", ".join(accepted_input_types))

        try:
            base_genome_obj =  wsClient.get_objects([{'ref':input_ref}])[0]['data']
        except:
            raise ValueError ("unable to fetch genome: "+input_ref)


        # get pangenome
        #
        input_ref = params['input_pangenome_ref']
        try:
            [OBJID_I, NAME_I, TYPE_I, SAVE_DATE_I, VERSION_I, SAVED_BY_I, WSID_I, WORKSPACE_I, CHSUM_I, SIZE_I, META_I] = range(11)  # object_info tuple
            input_obj_info = wsClient.get_object_info_new ({'objects':[{'ref':input_ref}]})[0]
            input_obj_type = re.sub ('-[0-9]+\.[0-9]+$', "", input_obj_info[TYPE_I])  # remove trailing version
        except Exception as e:
            raise ValueError('Unable to get object from workspace: (' + input_ref +')' + str(e))
        accepted_input_types = ["KBaseGenomes.Pangenome" ]
        if input_obj_type not in accepted_input_types:
            raise ValueError ("Input object of type '"+input_obj_type+"' not accepted.  Must be one of "+", ".join(accepted_input_types))

        try:
            pg_obj =  wsClient.get_objects([{'ref':input_ref}])[0]['data']
        except:
            raise ValueError ("unable to fetch genome: "+input_ref)


        # get genome_refs from pangenome and make sure requested genomes are found
        #
        pg_genome_refs = pg_obj['genome_refs']
        compare_genome_refs = []
        if 'input_compare_genome_refs' not in params or not params['input_compare_genome_refs']:
            for g_ref in pg_genome_refs:
                if g_ref == base_genome_ref:
                    continue
                compare_genome_refs.append(g_ref)
        else:
            for genome_ref in params['input_compare_genome_refs']:
                compare_genome_refs.append(genome_ref)

        missing_genomes = []
        for genome_ref in [base_genome_ref]+compare_genome_refs:
            if genome_ref not in pg_genome_refs:
                missing_genomes.append(genome_ref)
        if missing_genomes:
            msg = ''
            for genome_ref in missing_genomes:
                msg += "genome "+genome_ref+" not found in pangenome\n"
            raise ValueError (msg)


        # Get positions of genes in base genome
        #
        sorted_base_contig_ids = []
        sorted_base_contig_lens = []
        unsorted_contig_lens = dict()
        sorted_contig_order = dict()
        feature_contig_id = dict()
        feature_pos_in_contig = dict()
        feature_order = []
        sum_contig_lens = 0

        for contig_i,contig_id in enumerate(base_genome_obj['contig_ids']):
            unsorted_contig_lens[contig_id] = base_genome_obj['contig_lengths'][contig_i]
            sum_contig_lens += base_genome_obj['contig_lengths'][contig_i]

        for order_i,contig_id in enumerate(sorted(unsorted_contig_lens, key=unsorted_contig_lens.__getitem__, reverse=True)):
            sorted_contig_order[contig_id] = order_i
            sorted_base_contig_ids.append(contig_id)
            sorted_base_contig_lens.append(unsorted_contig_lens[contig_id])
            feature_order.append([])

        for feature in base_genome_obj['features']:
            if 'protein_translation' in feature and feature['protein_translation'] != None and feature['protein_translation'] != '':

                fid = feature['id']
                feature_contig_id[fid] = feature['location'][0][0]
                beg                    = feature['location'][0][1]
                strand                 = feature['location'][0][2]
                len                    = feature['location'][0][3]
                if strand == '-':
                    feature_pos_in_contig[fid] = beg - int(len/2)
                else:
                    feature_pos_in_contig[fid] = beg + int(len/2)
                contig_i = sorted_contig_order[feature_contig_id[fid]]
                feature_order[contig_i].append(fid)


        # Draw circle plot
        #
        png_file = base_genome_obj_name+'-pangenome_circle.png'
        pdf_file = base_genome_obj_name+'-pangenome_circle.pdf'
        output_png_file_path = os.path.join(html_output_dir, png_file);
        output_pdf_file_path = os.path.join(html_output_dir, pdf_file);

        # Init matplotlib
        img_dpi = 300
        img_units = "in"
        img_pix_width = 1200
        img_in_width = round(float(img_pix_width) / float(img_dpi), 2)
        img_html_width = img_pix_width // 4

        mark_width = 0.25
        ellipse_to_circle_scaling = 1.0
        ellipse_center_x = 0.50
        ellipse_center_y = 0.50
        ellipse_center = (ellipse_center_x, ellipse_center_y)
        base_diameter = 0.25
        gene_bar_lw = 10
        lw_to_coord_scale = 0.01

        # Build image
        fig = pyplot.figure()
        fig.set_size_inches(5, 5)
        ax = pyplot.subplot2grid( (1,1), (0,0), rowspan=1, colspan=1 )

        # Let's turn off visibility of all tic labels and boxes here
        for ax in fig.axes:
            ax.xaxis.set_visible(False)  # remove axis labels and tics
            ax.yaxis.set_visible(False)
            for t in ax.get_xticklabels()+ax.get_yticklabels():  # remove tics
                t.set_visible(False)
            ax.spines['top'].set_visible(False)     # Get rid of top axis line
            ax.spines['bottom'].set_visible(False)  # bottom axis line
            ax.spines['left'].set_visible(False)    # left axis line
            ax.spines['right'].set_visible(False)   # right axis line

        # Add marks for base genome
        ax = fig.axes[0]
        base_contig_pos = 0
        for contig_i,contig_feature_order in enumerate(feature_order):
            if contig_i > 0:
                base_contig_pos += sorted_base_contig_lens[contig_i-1]

            for fid in contig_feature_order:
                gene_color = "blue"
                gene_pos = base_contig_pos + feature_pos_in_contig[fid]
                
                arc_beg = 90 - 360 * (float(gene_pos) / float(sum_contig_lens)) - mark_width
                arc_end = 90 - 360 * (float(gene_pos) / float(sum_contig_lens)) + mark_width
                gene_bar_diameter = base_diameter + 0.5*gene_bar_lw*lw_to_coord_scale
                gene_x_diameter = 1.0 * gene_bar_diameter
                gene_y_diameter = ellipse_to_circle_scaling * gene_bar_diameter
                gene_arc = Arc (ellipse_center, gene_x_diameter, gene_y_diameter, \
                                    theta1=arc_beg, theta2=arc_end, \
                                    edgecolor=gene_color, lw=gene_bar_lw, alpha=1.0, zorder=1)  # facecolor does nothing (no fill for Arc)
                ax.add_patch (gene_arc)        

        # save
        fig.savefig(output_png_file_path, dpi=img_dpi)
        fig.savefig(output_pdf_file_path, format='pdf')

        # END HERE


        # build report object
        #
        reportName = 'kb_phylogenomics_report_'+str(uuid.uuid4())
        reportObj = {'objects_created': [],
                     #'text_message': '',  # or is it 'message'?
                     'message': '',  # or is it 'text_message'?
                     'direct_html': '',
                     'direct_html_link_index': 0,
                     'file_links': [],
                     'html_links': [],
                     'workspace_name': params['workspace_name'],
                     'report_object_name': reportName
                     }


        # build html report
        #
        circle_img_height = 1000
        cell_padding = 0
        #cell_spacing = 5
        cell_spacing = 0
        cell_border = 0
        sp = '&nbsp;'
        text_color = "#606060"
        font_size = '2'
        space_fontsize = '1'
        bar_char = '.'
        bar_fontsize = '1'
        bar_width = 50
        num_bars_per_node = 2 + 1
        
        html_report_lines = []
        html_report_lines += ['<html>']
        html_report_lines += ['<head>']
        html_report_lines += ['<title>KBase Homolog Circle Plot</title>']
        html_report_lines += ['</head>']
        html_report_lines += ['<body bgcolor="white">']
        html_report_lines += ['<table cellpadding="'+str(cell_padding)+'" cellspacing="'+str(cell_spacing)+'" border="'+str(cell_border)+'">']

        # add circle image
        circle_rowspan = 10  # DEBUG
        html_report_lines += ['<tr>']
        html_report_lines += ['<td valign="top" align="left" rowspan="'+str(circle_rowspan)+'">']
        html_report_lines += ['<img src="'+png_file+'" height='+str(circle_img_height)+'>']
        html_report_lines += ['</td>']
        html_report_lines += ['</tr>']

        # ADD KEY HERE
            
        # close
        html_report_lines += ['</table>']
        html_report_lines += ['</body>']
        html_report_lines += ['</html>']
        
        html_report_str = "\n".join(html_report_lines)
        #reportObj['direct_html'] = html_report_str


        # write html to file and upload
        html_file = os.path.join (html_output_dir, 'pan_circle_plot_report.html')
        with open (html_file, 'w', 0) as html_handle:
            html_handle.write(html_report_str)
        dfu = DFUClient(self.callbackURL)
        try:
            png_upload_ret = dfu.file_to_shock({'file_path': output_png_file_path,
                                                'make_handle': 0})
                                            #'pack': 'zip'})
        except:
            raise ValueError ('Logging exception loading png_file to shock')

        try:
            pdf_upload_ret = dfu.file_to_shock({'file_path': output_pdf_file_path,
                                                'make_handle': 0})
                                            #'pack': 'zip'})
        except:
            raise ValueError ('Logging exception loading pdf_file to shock')

        try:
            #upload_ret = dfu.file_to_shock({'file_path': html_file,
            upload_ret = dfu.file_to_shock({'file_path': html_output_dir,
                                            'make_handle': 0,
                                            'pack': 'zip'})
        except:
            raise ValueError ('Logging exception loading html_report to shock')

        reportObj['file_links'] = [{'shock_id': png_upload_ret['shock_id'],
                                    'name': 'pan_circle_plot.png',
                                    'label': 'Pangenome Circle Plot PNG'},
                                   {'shock_id': pdf_upload_ret['shock_id'],
                                    'name': 'pan_circle_plot.pdf',
                                    'label': 'Pangenome Circle Plot PDF'}
                                   ]
        reportObj['html_links'] = [{'shock_id': upload_ret['shock_id'],
                                    'name': 'pan_circle_plot_report.html',
                                    'label': 'Pangenome Circle Plot Report'}
                                   ]
        reportObj['direct_html_link_index'] = 0


        # save report object
        #
        reportClient = KBaseReport(self.callbackURL, token=ctx['token'], service_ver=SERVICE_VER)
        #report_info = report.create({'report':reportObj, 'workspace_name':params['workspace_name']})
        report_info = reportClient.create_extended_report(reportObj)

        output = { 'report_name': report_info['name'], 'report_ref': report_info['ref'] }

        #END view_pan_circle_plot

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method view_pan_circle_plot return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]

    def view_pan_accumulation_plot(self, ctx, params):
        """
        :param params: instance of type "view_pan_accumulation_plot_Input"
           (view_pan_accumulation_plot() ** ** build an accumulation plot of
           a pangenome) -> structure: parameter "workspace_name" of type
           "workspace_name" (** Common types), parameter "input_genome_ref"
           of type "data_obj_ref", parameter "input_pangenome_ref" of type
           "data_obj_ref"
        :returns: instance of type "view_pan_accumulation_plot_Output" ->
           structure: parameter "report_name" of String, parameter
           "report_ref" of String
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN view_pan_accumulation_plot
        #END view_pan_accumulation_plot

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method view_pan_accumulation_plot return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]

    def view_pan_flower_venn(self, ctx, params):
        """
        :param params: instance of type "view_pan_flower_venn_Input"
           (view_pan_flower_venn() ** ** build a multi-member pangenome
           flower venn diagram) -> structure: parameter "workspace_name" of
           type "workspace_name" (** Common types), parameter
           "input_genome_ref" of type "data_obj_ref", parameter
           "input_pangenome_ref" of type "data_obj_ref"
        :returns: instance of type "view_pan_flower_venn_Output" ->
           structure: parameter "report_name" of String, parameter
           "report_ref" of String
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN view_pan_flower_venn
        #END view_pan_flower_venn

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method view_pan_flower_venn return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]

    def view_pan_pairwise_overlap(self, ctx, params):
        """
        :param params: instance of type "view_pan_pairwise_overlap_Input"
           (view_pan_pairwise_overlap() ** ** build a multi-member pangenome
           pairwise overlap plot) -> structure: parameter "workspace_name" of
           type "workspace_name" (** Common types), parameter
           "input_genome_ref" of type "data_obj_ref", parameter
           "input_pangenome_ref" of type "data_obj_ref"
        :returns: instance of type "view_pan_pairwise_overlap_Output" ->
           structure: parameter "report_name" of String, parameter
           "report_ref" of String
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN view_pan_pairwise_overlap
        #END view_pan_pairwise_overlap

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method view_pan_pairwise_overlap return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]

    def view_pan_phylo(self, ctx, params):
        """
        :param params: instance of type "view_pan_phylo_Input"
           (view_pan_phylo() ** ** show the pangenome accumulation using a
           tree) -> structure: parameter "workspace_name" of type
           "workspace_name" (** Common types), parameter
           "input_pangenome_ref" of type "data_obj_ref", parameter
           "input_speciesTree_ref" of type "data_obj_ref"
        :returns: instance of type "view_pan_phylo_Output" -> structure:
           parameter "report_name" of String, parameter "report_ref" of String
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN view_pan_phylo

        ### STEP 0: basic init
        console = []
        self.log(console, 'Running view_pan_phylo(): ')
        self.log(console, "\n"+pformat(params))

        token = ctx['token']
        wsClient = workspaceService(self.workspaceURL, token=token)
        headers = {'Authorization': 'OAuth '+token}
        env = os.environ.copy()
        env['KB_AUTH_TOKEN'] = token

        #SERVICE_VER = 'dev'  # DEBUG
        SERVICE_VER = 'release'

        # param checks
        required_params = ['input_speciesTree_ref',
                           'input_pangenome_ref'
                          ]
        for arg in required_params:
            if arg not in params or params[arg] == None or params[arg] == '':
                raise ValueError ("Must define required param: '"+arg+"'")


        # load provenance
        provenance = [{}]
        if 'provenance' in ctx:
            provenance = ctx['provenance']
        provenance[0]['input_ws_objects']=[str(params['input_speciesTree_ref']),
                                           str(params['input_pangenome_ref'])
                                          ]


        # set the output paths
        timestamp = int((datetime.utcnow() - datetime.utcfromtimestamp(0)).total_seconds()*1000)
        output_dir = os.path.join(self.scratch,'output.'+str(timestamp))
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        html_output_dir = os.path.join(output_dir,'html_output')
        if not os.path.exists(html_output_dir):
            os.makedirs(html_output_dir)


        # get speciesTree
        #
        input_ref = params['input_speciesTree_ref']
        speciesTree_name = None
        try:
            [OBJID_I, NAME_I, TYPE_I, SAVE_DATE_I, VERSION_I, SAVED_BY_I, WSID_I, WORKSPACE_I, CHSUM_I, SIZE_I, META_I] = range(11)  # object_info tuple
            input_obj_info = wsClient.get_object_info_new ({'objects':[{'ref':input_ref}]})[0]
            input_obj_type = re.sub ('-[0-9]+\.[0-9]+$', "", input_obj_info[TYPE_I])  # remove trailing version
            speciesTree_name = input_obj_info[NAME_I]
        except Exception as e:
            raise ValueError('Unable to get object from workspace: (' + input_ref +')' + str(e))
        accepted_input_types = ["KBaseTrees.Tree" ]
        if input_obj_type not in accepted_input_types:
            raise ValueError ("Input object of type '"+input_obj_type+"' not accepted.  Must be one of "+", ".join(accepted_input_types))

        # get set obj
        try:
            speciesTree_obj = wsClient.get_objects([{'ref':input_ref}])[0]['data']
        except:
            raise ValueError ("unable to fetch speciesTree: "+input_ref)


        # get genome_refs from speciesTree and instantiate ETE3 tree and order
        #
        genome_refs = []
        genome_id_by_ref = dict()
        genome_ref_by_id = dict()
        for genome_id in speciesTree_obj['default_node_labels'].keys():
            genome_ref = speciesTree_obj['ws_refs'][genome_id]['g'][0]
            genome_id_by_ref[genome_ref] = genome_id
            genome_ref_by_id[genome_id] = genome_ref

        species_tree = ete3.Tree(speciesTree_obj['tree'])  # instantiate ETE3 tree
        species_tree.ladderize()
        for genome_id in species_tree.get_leaf_names():
            genome_refs.append(genome_ref_by_id[genome_id])


        # get internal node ids based on sorted genome_refs of children
        #
        node_ref_ids = dict()
        genome_ref_to_node_ref_ids = dict()
        node_size = dict()
        node_order_by_ref = []
        node_num_id = -1
        for n in species_tree.traverse("preorder"):
            if n.is_leaf():
                continue

            node_num_id += 1
            leaf_refs = []
            for genome_id in n.get_leaf_names():
                leaf_refs.append(genome_ref_by_id[genome_id])
            node_ref_id = "+".join(sorted(leaf_refs))
            node_size[node_ref_id] = len(leaf_refs)
            node_order_by_ref.append(node_ref_id)
            node_ref_ids[node_ref_id] = node_num_id

            # point each genome at its nodes
            for genome_ref in leaf_refs:
                if genome_ref not in genome_ref_to_node_ref_ids:
                    genome_ref_to_node_ref_ids[genome_ref] = []
                genome_ref_to_node_ref_ids[genome_ref].append(node_ref_id)
            

        # get object names, sci names, protein-coding gene counts, and SEED annot
        #
        genome_obj_name_by_ref = dict()
        genome_sci_name_by_ref = dict()
        genome_sci_name_by_id  = dict()
        genome_CDS_count_by_ref = dict()
        uniq_genome_ws_ids = dict()

        dom_hits = dict()  # initialize dom_hits here because reading SEED within genome
        genes_with_hits_cnt = dict()

        for genome_ref in genome_refs:

            dom_hits[genome_ref] = dict()
            genes_with_hits_cnt[genome_ref] = dict()

            # get genome object name
            input_ref = genome_ref
            try:
                [OBJID_I, NAME_I, TYPE_I, SAVE_DATE_I, VERSION_I, SAVED_BY_I, WSID_I, WORKSPACE_I, CHSUM_I, SIZE_I, META_I] = range(11)  # object_info tuple
                input_obj_info = wsClient.get_object_info_new ({'objects':[{'ref':input_ref}]})[0]
                input_obj_type = re.sub ('-[0-9]+\.[0-9]+$', "", input_obj_info[TYPE_I])  # remove trailing version
                input_name = input_obj_info[NAME_I]
                uniq_genome_ws_ids[input_obj_info[WSID_I]] = True

            except Exception as e:
                raise ValueError('Unable to get object from workspace: (' + input_ref +')' + str(e))
            accepted_input_types = ["KBaseGenomes.Genome" ]
            if input_obj_type not in accepted_input_types:
                raise ValueError ("Input object of type '"+input_obj_type+"' not accepted.  Must be one of "+", ".join(accepted_input_types))

            genome_obj_name_by_ref[genome_ref] = input_name

            try:
                genome_obj = wsClient.get_objects([{'ref':input_ref}])[0]['data']
            except:
                raise ValueError ("unable to fetch genome: "+input_ref)

            # sci name
            genome_sci_name_by_ref[genome_ref] = genome_obj['scientific_name']
            genome_sci_name_by_id[genome_id_by_ref[genome_ref]] = genome_obj['scientific_name']
            
            # CDS cnt
            cds_cnt = 0
            for feature in genome_obj['features']:
                if 'protein_translation' in feature and feature['protein_translation'] != None and feature['protein_translation'] != '':
                    cds_cnt += 1
            genome_CDS_count_by_ref[genome_ref] = cds_cnt


        # get pangenome
        #
        input_ref = params['input_pangenome_ref']
        pangenome_name = None
        try:
            [OBJID_I, NAME_I, TYPE_I, SAVE_DATE_I, VERSION_I, SAVED_BY_I, WSID_I, WORKSPACE_I, CHSUM_I, SIZE_I, META_I] = range(11)  # object_info tuple
            input_obj_info = wsClient.get_object_info_new ({'objects':[{'ref':input_ref}]})[0]
            input_obj_type = re.sub ('-[0-9]+\.[0-9]+$', "", input_obj_info[TYPE_I])  # remove trailing version
            pangenome_name = input_obj_info[NAME_I]
        except Exception as e:
            raise ValueError('Unable to get object from workspace: (' + input_ref +')' + str(e))
        accepted_input_types = ["KBaseGenomes.Pangenome" ]
        if input_obj_type not in accepted_input_types:
            raise ValueError ("Input object of type '"+input_obj_type+"' not accepted.  Must be one of "+", ".join(accepted_input_types))

        # get obj
        try:
            pg_obj = wsClient.get_objects([{'ref':input_ref}])[0]['data']
        except:
            raise ValueError ("unable to fetch pangenome: "+input_ref)


        # make sure species tree genomes are found in pangenome (reverse not required)
        for genome_ref in genome_refs:
            if genome_ref not in pg_obj['genome_refs']:
                raise ValueError ("genome: '"+str(genome_ref)+"' from SpeciesTree not present in Pangenome object")


        # determine pangenome accumulations of core, partial, and singleton
        #
        cluster_hits = dict()
        for node_ref_id in node_ref_ids.keys():
            cluster_hits[node_ref_id] = []

        cluster_num = -1  # cluster ids themselves start from 1
        for homolog_cluster in pg_obj['orthologs']:
            cluster_num += 1
            for node_ref_id in node_ref_ids.keys():
                cluster_hits[node_ref_id].append(0)

            nodes_hit = dict()
            for gene in homolog_cluster['orthologs']:
                gene_id                     = gene[0]
                probably_gene_len_dont_need = gene[1]
                genome_ref                  = gene[2]

                if genome_ref not in genome_ref_to_node_ref_ids:
                    continue
                for node_ref_id in genome_ref_to_node_ref_ids[genome_ref]:
                    if node_ref_id not in nodes_hit:
                        nodes_hit[node_ref_id] = dict()
                    nodes_hit[node_ref_id][genome_ref] = True
            
            for node_ref_id in nodes_hit.keys():
                for genome_ref in nodes_hit[node_ref_id].keys():
                    cluster_hits[node_ref_id][cluster_num] += 1

        # calc accumulations
        clusters_total = dict()
        clusters_singletons = dict()
        clusters_core = dict()
        for node_ref_id in node_ref_ids.keys():
            clusters_total[node_ref_id] = 0
            clusters_singletons[node_ref_id] = 0
            clusters_core[node_ref_id] = 0

            for cluster_num,hit_cnt in enumerate(cluster_hits[node_ref_id]):
                if hit_cnt > 0:
                    clusters_total[node_ref_id] += 1
                    if hit_cnt == 1:
                        clusters_singletons[node_ref_id] += 1
                    elif hit_cnt == node_size[node_ref_id]:
                        clusters_core[node_ref_id] += 1

        # get min and max cluster cnts
        INSANE_VALUE = 10000000000000000
        max_clusters_cnt = -INSANE_VALUE
        min_clusters_cnt =  INSANE_VALUE
        for node_ref_id in node_ref_ids.keys():
            if clusters_total[node_ref_id] > max_clusters_cnt:
                max_clusters_cnt = clusters_total[node_ref_id]
            if clusters_total[node_ref_id] < min_clusters_cnt:
                min_clusters_cnt = clusters_total[node_ref_id]

            self.log(console, "NODE: "+node_ref_id+" MIN: "+str(min_clusters_cnt)+" MAX: "+str(max_clusters_cnt))  # DEBUg


        # Draw tree (we already instantiated Tree above)
        #
        png_file = speciesTree_name+'-pangenome.png'
        pdf_file = speciesTree_name+'-pangenome.pdf'
        output_png_file_path = os.path.join(html_output_dir, png_file);
        output_pdf_file_path = os.path.join(html_output_dir, pdf_file);

        # init ETE3 accessory objects
        ts = ete3.TreeStyle()

        # customize
        min_pie_size = 1000
        max_pie_size = 2000
        leaf_fontsize = 500  # scale of everything is goofy in circle tree mode, and pie size affects type size and line thickness.  ugh.
        node_fontsize = 500
        ts.mode = "c"  # circular tree graph
        #ts.arc_start = -180 # 0 degrees = 3 o'clock
        #ts.arc_span = 180
        ts.show_leaf_name = True
        ts.show_branch_length = False
        ts.show_branch_support = True
        #ts.scale = 50 # 50 pixels per branch length unit
        ts.branch_vertical_margin = 5 # pixels between adjacent branches
        #ts.title.add_face(ete3.TextFace(params['output_name']+": "+params['desc'], fsize=10), column=0)

        node_style = ete3.NodeStyle()
        node_style["fgcolor"] = "#606060"  # for node balls
        node_style["size"] = 10  # for node balls (gets reset based on support)
        node_style["vt_line_color"] = "#606060"
        node_style["hz_line_color"] = "#606060"
        node_style["vt_line_width"] = 100  # 2
        node_style["hz_line_width"] = 100  # 2
        node_style["vt_line_type"] = 0 # 0 solid, 1 dashed, 2 dotted
        node_style["hz_line_type"] = 0

        leaf_style = ete3.NodeStyle()
        leaf_style["fgcolor"] = "#ffffff"  # for node balls
        leaf_style["size"] = 100  # for node balls (we're using it to add space)
        leaf_style["vt_line_color"] = "#606060"  # unecessary
        leaf_style["hz_line_color"] = "#606060"
        leaf_style["vt_line_width"] = 100  # 2
        leaf_style["hz_line_width"] = 100  # 2
        leaf_style["vt_line_type"] = 0 # 0 solid, 1 dashed, 2 dotted
        leaf_style["hz_line_type"] = 0

        for n in species_tree.traverse("preorder"):
            if n.is_leaf():
                style = leaf_style
                genome_id = n.name
                #n.name = genome_sci_name_by_id[genome_id]
                n.name = None
                leaf_name_disp = genome_sci_name_by_id[genome_id]
                n.add_face (ete3.TextFace(leaf_name_disp, fsize=leaf_fontsize), column=0, position="branch-right")

            else:
                leaf_refs = []
                for genome_id in n.get_leaf_names():
                    leaf_refs.append(genome_ref_by_id[genome_id])
                node_ref_id = "+".join(sorted (leaf_refs))
                node_num_id = node_ref_ids[node_ref_id]
                node_name_disp = str(node_num_id)
                #n.add_face (ete3.TextFace(node_name_disp, fsize=node_fontsize),column=0, position="branch-right")
                n.add_face (ete3.TextFace(' '+node_name_disp+' ', fsize=node_fontsize),column=0)

                style = ete3.NodeStyle()
                for k in node_style.keys():
                    style[k] = node_style[k]

                if n.support > 0.95:
                    style["size"] = 6
                elif n.support > 0.90:
                    style["size"] = 5
                elif n.support > 0.80:
                    style["size"] = 4
                else:
                    style["size"] = 2

                # yum! pie!
                pie_size = int(min_pie_size + float(max_pie_size-min_pie_size) * float(clusters_total[node_ref_id]-min_clusters_cnt) / float(max_clusters_cnt-min_clusters_cnt))
                singleton_perc = round(100.0*float(clusters_singletons[node_ref_id]) / float(clusters_total[node_ref_id]), 1)
                core_perc = round(100.0*float(clusters_core[node_ref_id]) / float(clusters_total[node_ref_id]), 1)
                partial_perc = round (100.0 - core_perc - singleton_perc, 1)

                pie_w = pie_h = pie_size
                pie_percs = [singleton_perc, partial_perc, core_perc]
                pie_colors = ["IndianRed", "Orchid", "DodgerBlue"]
                pie_line_color = "White"

                this_pieFace = ete3.PieChartFace(pie_percs, pie_w, pie_h, pie_colors, pie_line_color)
                n.add_face (this_pieFace, column=1)

            n.set_style(style)

        # save images
        dpi = 300
        img_units = "in"
        img_pix_width = 1200
        img_in_width = round(float(img_pix_width)/float(dpi), 1)
        img_html_width = img_pix_width // 2
        species_tree.render(output_png_file_path, w=img_in_width, units=img_units, dpi=dpi, tree_style=ts)
        species_tree.render(output_pdf_file_path, w=img_in_width, units=img_units, tree_style=ts)  # dpi irrelevant


        # build report object
        #
        reportName = 'kb_phylogenomics_report_'+str(uuid.uuid4())
        reportObj = {'objects_created': [],
                     #'text_message': '',  # or is it 'message'?
                     'message': '',  # or is it 'text_message'?
                     'direct_html': '',
                     'direct_html_link_index': 0,
                     'file_links': [],
                     'html_links': [],
                     'workspace_name': params['workspace_name'],
                     'report_object_name': reportName
                     }


        # build html report
        #
        tree_img_height = 1000
        cell_padding = 0
        #cell_spacing = 5
        cell_spacing = 0
        cell_border = 0
        sp = '&nbsp;'
        horiz_sp = sp+sp+sp+sp
        text_color = "#606060"
        font_size = '2'
        space_fontsize = '1'
        bar_char = '.'
        bar_fontsize = '1'
        bar_width = 50
        cat_order = ['TOTAL', 'singleton', 'partial', 'perfect core']
        cat_colors = [text_color] + pie_colors
        #num_bars_per_node = 2*len(cat_order) + 1
        num_bars_per_node = len(cat_order) + 1
        
        html_report_lines = []
        html_report_lines += ['<html>']
        html_report_lines += ['<head>']
        html_report_lines += ['<title>KBase Pangenome Phylogenetic Context</title>']
        html_report_lines += ['</head>']
        html_report_lines += ['<body bgcolor="white">']
        html_report_lines += ['<table cellpadding="'+str(cell_padding)+'" cellspacing="'+str(cell_spacing)+'" border="'+str(cell_border)+'">']

        # add tree image
        html_report_lines += ['<tr>']
        html_report_lines += ['<td valign="top" align="left" rowspan="'+str(num_bars_per_node*len(node_ref_ids))+'">']
        html_report_lines += ['<img src="'+png_file+'" height='+str(tree_img_height)+'>']
        html_report_lines += ['</td>']

        # add key and bar graph
        max_cnt = 0
        for node_ref_id in node_order_by_ref:
            if clusters_total[node_ref_id] > max_cnt:
                max_cnt = clusters_total[node_ref_id]

        for node_i,node_ref_id in enumerate(node_order_by_ref):
            node_id = node_ref_ids[node_ref_id]
            if node_i > 0:
                html_report_lines += ['<tr>']

            # vals
            cat_cnts  = dict()
            cat_percs = dict()
            cat_cnts['TOTAL']        = clusters_total[node_ref_id]
            cat_cnts['singleton']    = clusters_singletons[node_ref_id]
            cat_cnts['perfect core'] = clusters_core[node_ref_id]
            cat_cnts['partial']      = clusters_total[node_ref_id] - clusters_singletons[node_ref_id] - clusters_core[node_ref_id]
            cat_percs['TOTAL'] = '100'
            cat_percs['singleton']    = round (100.0*float(clusters_singletons[node_ref_id]) / float(clusters_total[node_ref_id]), 1)
            cat_percs['perfect core'] = round (100.0*float(clusters_core[node_ref_id]) / float(clusters_total[node_ref_id]), 1)
            if cat_cnts['partial'] == 0:
                cat_percs['partial'] = 0.0
            else:
                cat_percs['partial'] = round (100.0 - cat_percs['perfect core'] - cat_percs['singleton'], 1)

            # node id
            node_label = 'NODE '+str(node_id)
            html_report_lines += ['<td rowspan="'+str(num_bars_per_node)+'" valign="top" align="right"><font color="'+str(text_color)+'" size="'+str(font_size)+'"><b><nobr>'+str(node_label)+'</nobr></b></font></td>']
            html_report_lines += ['<td rowspan="'+str(num_bars_per_node)+'"><font size="'+str(space_fontsize)+'">'+horiz_sp+'</font></td>']

            for cat_i,cat in enumerate(cat_order):
                if cat_i > 0:
                    html_report_lines += ['<tr>']
                # cat name
                html_report_lines += ['<td valign="top" align="right"><font color="'+str(text_color)+'" size="'+str(font_size)+'"><nobr>'+cat+'</nobr></font></td>']
                html_report_lines += ['<td><font size="'+str(space_fontsize)+'">'+horiz_sp+'</font></td>']
            
                # cnt
                html_report_lines += ['<td valign="top" align="right"><font color="'+str(text_color)+'" size="'+str(font_size)+'">'+str(cat_cnts[cat])+'</font></td>']
                html_report_lines += ['<td><font size="'+str(space_fontsize)+'">'+horiz_sp+'</font></td>']

                #perc
                html_report_lines += ['<td valign="top" align="right"><font color="'+str(text_color)+'" size="'+str(font_size)+'">'+str(cat_percs[cat])+'%'+'</font></td>']
                html_report_lines += ['<td><font size="'+str(space_fontsize)+'">'+horiz_sp+'</font></td>']

                # bar
                this_width = int(round(float(bar_width) * (float(cat_cnts[cat])/float(max_cnt)), 0))
                for cell_i in range(this_width):
                    html_report_lines += ['<td bgcolor="'+str(cat_colors[cat_i])+'"><font size="'+str(bar_fontsize)+'" color="'+str(cat_colors[cat_i])+'">'+bar_char+'</font></td>']

                html_report_lines += ['</tr>']
                #html_report_lines += ['<tr><td><font size="'+str(space_fontsize)+'">'+sp+'</font></td></tr>']  # space for blank row
            html_report_lines += ['<tr><td><font size="'+str(space_fontsize)+'">'+sp+'</font></td></tr>']  # space for blank row
            

        # close
        html_report_lines += ['</table>']
        html_report_lines += ['</body>']
        html_report_lines += ['</html>']
        
        html_report_str = "\n".join(html_report_lines)
        #reportObj['direct_html'] = html_report_str


        # write html to file and upload
        html_file = os.path.join (html_output_dir, 'pan_phylo_report.html')
        with open (html_file, 'w', 0) as html_handle:
            html_handle.write(html_report_str)
        dfu = DFUClient(self.callbackURL)
        try:
            png_upload_ret = dfu.file_to_shock({'file_path': output_png_file_path,
                                                'make_handle': 0})
                                            #'pack': 'zip'})
        except:
            raise ValueError ('Logging exception loading png_file to shock')

        try:
            pdf_upload_ret = dfu.file_to_shock({'file_path': output_pdf_file_path,
                                                'make_handle': 0})
                                            #'pack': 'zip'})
        except:
            raise ValueError ('Logging exception loading pdf_file to shock')

        try:
            #upload_ret = dfu.file_to_shock({'file_path': html_file,
            upload_ret = dfu.file_to_shock({'file_path': html_output_dir,
                                            'make_handle': 0,
                                            'pack': 'zip'})
        except:
            raise ValueError ('Logging exception loading html_report to shock')

        reportObj['file_links'] = [{'shock_id': png_upload_ret['shock_id'],
                                    'name': 'phylogenetic_pangenome.png',
                                    'label': 'Phylogenetic Pangenome PNG'},
                                   {'shock_id': pdf_upload_ret['shock_id'],
                                    'name': 'phylogenetic_pangenome.pdf',
                                    'label': 'Phylogenetic Pangenome PDF'}
                                   ]
        reportObj['html_links'] = [{'shock_id': upload_ret['shock_id'],
                                    'name': 'pan_phylo_report.html',
                                    'label': 'Phylogenetic Pangenome report'}
                                   ]
        reportObj['direct_html_link_index'] = 0


        # save report object
        #
        reportClient = KBaseReport(self.callbackURL, token=ctx['token'], service_ver=SERVICE_VER)
        #report_info = report.create({'report':reportObj, 'workspace_name':params['workspace_name']})
        report_info = reportClient.create_extended_report(reportObj)

        output = { 'report_name': report_info['name'], 'report_ref': report_info['ref'] }

        #END view_pan_phylo

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method view_pan_phylo return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]
    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK",
                     'message': "",
                     'version': self.VERSION,
                     'git_url': self.GIT_URL,
                     'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]
