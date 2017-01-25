# -*- coding: utf-8 -*-
#BEGIN_HEADER

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
from Bio import SeqIO

from biokbase.workspace.client import Workspace as workspaceService
from KBaseReport.KBaseReportClient import KBaseReport

from DomainAnnotation.DomainAnnotationClient import DomainAnnotation
#from kb_phylogenomics.PhyloPlotUtil import PhyloPlotUtil

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
    GIT_COMMIT_HASH = "f781cac5982d643350d79f32d31b51c8735f157a"

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
           "input_genomeSet_ref" of type "data_obj_ref"
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
        for genome_ref in genome_refs:

            # get genome object name
            input_ref = genome_ref
            try:
                [OBJID_I, NAME_I, TYPE_I, SAVE_DATE_I, VERSION_I, SAVED_BY_I, WSID_I, WORKSPACE_I, CHSUM_I, SIZE_I, META_I] = range(11)  # object_info tuple
                input_obj_info = wsClient.get_object_info_new ({'objects':[{'ref':input_ref}]})[0]
                input_obj_type = re.sub ('-[0-9]+\.[0-9]+$', "", input_obj_info[TYPE_I])  # remove trailing version
                input_name = input_obj_info[NAME_I]

            except Exception as e:
                raise ValueError('Unable to get object from workspace: (' + input_ref +')' + str(e))
            accepted_input_types = ["KBaseGenomes.Genome" ]
            if input_obj_type not in accepted_input_types:
                raise ValueError ("Input object of type '"+input_obj_type+"' not accepted.  Must be one of "+", ".join(accepted_input_types))

            genome_obj_name_by_ref[input_ref] = input_name


        ### STEP 3: run DomainAnnotation on each genome in set
        try:
#            daClient = DomainAnnotation (url=self.callbackURL, token=ctx['token'], service_ver=SERVICE_VER)  # SDK Local
            TEMP_SERVICE_VER='beta'
            daClient = DomainAnnotation (url=self.callbackURL, token=ctx['token'], service_ver=TEMP_SERVICE_VER)  # SDK Local
            #daClient = DomainAnnotation (url=self.serviceWizardURL, token=ctx['token'], service_ver=SERVICE_VER)  # Dynamic service
        except:
            raise ValueError ("unable to instantiate DomainAnnotationClient")

        # RUN DomainAnnotations
        report_text = ''
        for genome_i,genome_ref in enumerate(genome_refs):
            genome_obj_name = genome_obj_name_by_ref[genome_ref]
            domains_obj_name = genome_obj_name+'.DomainAnnotation'
            DomainAnnotation_Params = { 'genome_ref': genome_ref,
                                        'dms_ref': 'KBasePublicGeneDomains/All',
                                        #'ws': params['workspace_name'],
                                        'output_result_id': domains_obj_name
                                      }
            da_retVal = daClient.search_domains (ctx, DomainAnnotation_Params)[0]
            this_output_ref  = da_retVal['output_result_id']
            this_report_name = da_retVal['report_name']
            this_report_ref  = da_retVal['report_ref']

            try:
                this_report_obj =  wsClient.get_objects([{'ref':this_report_ref}])[0]['data']
            except:
                raise ValueError ("unable to fetch report: "+this_report_ref)
            report_text += this_report_obj['text_message']
            report_text += "\n\n"


        ### STEP 4: build and save the report
        reportObj = {
            'objects_created': [],
            'text_message': report_text
        }
        reportClient = KBaseReport(self.callbackURL, token=ctx['token'], service_ver=SERVICE_VER)
        report_info = reportClient.create({'report':reportObj, 'workspace_name':params['workspace_name']})


        ### STEP 5: construct the output to send back
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
           "data_obj_ref", parameter "target_fams" of list of String,
           parameter "heatmap" of type "bool"
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
        required_params = ['input_genomeSet_ref'
                          ]

        for arg in required_params:
            if arg not in params or params[arg] == None or params[arg] == '':
                raise ValueError ("Must define required param: '"+arg+"'")

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


        # DEBUG
        self.log(console, "GOT HERE A")


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
            genomeSet_obj = wsClient.get_objects([{'ref':input_ref}])[0]['data']
        except:
            raise ValueError ("unable to fetch genomeSet: "+input_ref)


        # get genome refs and object names
        genome_ids = genomeSet_obj['elements'].keys()  # note: genome_id may be meaningless
        genome_refs = []
        for genome_id in genome_ids:
            genome_refs.append (genomeSet_obj['elements'][genome_id]['ref'])

        genome_obj_name_by_ref = dict()
        genome_sci_name_by_ref = dict()
        for genome_ref in genome_refs:

            # get genome object name
            input_ref = genome_ref
            try:
                [OBJID_I, NAME_I, TYPE_I, SAVE_DATE_I, VERSION_I, SAVED_BY_I, WSID_I, WORKSPACE_I, CHSUM_I, SIZE_I, META_I] = range(11)  # object_info tuple
                input_obj_info = wsClient.get_object_info_new ({'objects':[{'ref':input_ref}]})[0]
                input_obj_type = re.sub ('-[0-9]+\.[0-9]+$', "", input_obj_info[TYPE_I])  # remove trailing version
                input_name = input_obj_info[NAME_I]

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

            genome_sci_name_by_ref[genome_ref] = genome_obj['scientific_name']


        # DEBUG
        self.log(console, "GOT HERE B")

# HERE

        # configure fams
        fams = ['A', 'B', 'C', 'PF00007']

        
        # build report
        #
        reportName = 'kb_phylogenomics_report_'+str(uuid.uuid4())
        reportObj = {'objects_created': [],
                     #'text_message': '',  # or is it 'message'?
                     'message': '',  # or is it 'text_message'?
                     'direct_html': '',
                     'direct_html_index': 0,
                     'file_links': [],
                     'html_links': [],
                     'workspace_name': params['workspace_name'],
                     'report_object_name': reportName
                     }

        # DEBUG
        self.log(console, "GOT HERE C")


        # build html report
        sp = '&nbsp;'
        text_color = "#606060"
        graph_color = "lightblue"
        #graph_width = 100
        graph_char = "."
        graph_fontsize = "-2"
        #row_spacing = "-2"
        num_rows = len(genome_refs)

        html_report_lines = []
        html_report_lines += ['<html>']
        html_report_lines += ['<body bgcolor="white">']

        # DEBUG
        self.log(console, "GOT HERE D")

        # header
        html_report_lines += ['<table cellpadding=10 cellspacing=10 border=1>']
        html_report_lines += ['<tr><td valign=bottom align=right><font color="'+text_color+'"><b>Genomes</b></font></td>']
        for fam in fams:
            html_report_lines += ['<td valign=bottom><font color="'+text_color+'"><b>']
            for c_i,c in enumerate(fam):
                if c_i < len(fam)-1:
                    html_report_lines += [c+'<br>']
                else:
                    html_report_lines += [c]
            html_report_lines += ['</b></font></td>']
        html_report_lines += ['</tr>']

        # DEBUG
        self.log(console, "GOT HERE E")

        # rest of rows
        for genome_ref in genome_refs:
            genome_sci_name = genome_sci_name_by_ref[genome_ref]
            html_report_lines += ['<tr>']
            html_report_lines += ['<td align=right><font color="'+text_color+'">'+genome_sci_name+'</font></td>']
            for fam in fams:
                cell_color = graph_color
                cell_val = "88%"
                html_report_lines += ['<td title="'+cell_val+'" bgcolor="'+cell_color+'"><font color="'+cell_color+'" size='+graph_fontsize+'>'+graph_char+'</font></td>']
            html_report_lines += ['</tr>']
        
        html_report_lines += ['</table>']
        html_report_lines += ['</body>']
        html_report_lines += ['</html>']

        # DEBUG
        self.log(console, "GOT HERE F")

        reportObj['direct_html'] = "\n".join(html_report_lines)


        # DEBUG
        self.log(console, "GOT HERE G")


        # save report object
        #
        report = KBaseReport(self.callbackURL, token=ctx['token'], service_ver=SERVICE_VER)
        #report_info = report.create({'report':reportObj, 'workspace_name':params['workspace_name']})
        report_info = report.create_extended_report(reportObj)

        # DEBUG
        self.log(console, "GOT HERE H")


        output = { 'report_name': report_info['name'], 'report_ref': report_info['ref'] }

        # DEBUG
        self.log(console, "GOT HERE I")

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
           "target_fams" of list of String, parameter "heatmap" of type "bool"
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
        required_params = ['input_speciesTree_ref'
                          ]
# DEBUG 
#        for arg in required_params:
#            if arg not in params or params[arg] == None or params[arg] == '':
#                raise ValueError ("Must define required param: '"+arg+"'")

        # load provenance
        provenance = [{}]
        if 'provenance' in ctx:
            provenance = ctx['provenance']
        provenance[0]['input_ws_objects']=[str(params['input_speciesTree_ref'])]


        # set the output path
        timestamp = int((datetime.utcnow() - datetime.utcfromtimestamp(0)).total_seconds()*1000)
        output_dir = os.path.join(self.scratch,'output.'+str(timestamp))
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        format = 'png'
        output_tree_img_file_path = os.path.join(output_dir, 'tree.'+format);


        # configure fams
        fams = ['A', 'B', 'C', 'PF00007']
        genome_ids = ['spree', 'smarties', 'skittles', 'rolos', 'butterfinger', 'milky way', 'snickers', 'skor', 'heath bar', 'starburst']

        # create figures
        newick_str = "(A:1,(B:1,(E:1,D:1):0.5):0.5);"


        phyloplot = PhyloPlotUtil (self.config)
        phyloplot.write_tree_to_file (newick_str, output_tree_img_file_path, 200, format)

        
        # build report
        #
        reportName = 'kb_phylogenomics_report_'+str(uuid.uuid4())
        reportObj = {'objects_created': [],
                     #'text_message': '',  # or is it 'message'?
                     'message': '',  # or is it 'text_message'?
                     'direct_html': '',
                     'direct_html_index': 0,
                     'file_links': [],
                     'html_links': [],
                     'workspace_name': params['workspace_name'],
                     'report_object_name': reportName
                     }


        # build html report
        sp = '&nbsp;'
        text_color = "#606060"
        graph_color = "lightblue"
        #graph_width = 100
        graph_char = "."
        graph_fontsize = "-2"
        #row_spacing = "-2"
        num_rows = len(genome_ids)

        html_report_lines = []
        html_report_lines += ['<html>']
        html_report_lines += ['<body bgcolor="white">']

        # header
        html_report_lines += ['<table cellpadding=10 cellspacing=10 border=1>']
        html_report_lines += ['<tr><td valign=bottom><font color="'+text_color+'"><b>Species Tree</b></font></td>']
        for fam in fams:
            html_report_lines += ['<td valign=bottom><font color="'+text_color+'"><b>']
            for c_i,c in enumerate(fam):
                if c_i < len(fam)-1:
                    html_report_lines += [c+'<br>']
                else:
                    html_report_lines += [c]
            html_report_lines += ['</b></font></td>']
        html_report_lines += ['</tr>']

        # first row
        html_report_lines += ['<tr>']
        html_report_lines += ['<td rowspan='+str(num_rows)+'><img src="'+output_tree_img_file_path+'"></td>']
        genome_id = genome_ids[0]
        for fam in fams:
            cell_color = graph_color
            html_report_lines += ['<td bgcolor="'+cell_color+'"><font color="'+cell_color+'" size='+graph_fontsize+'>'+graph_char+'</font></td>']
        html_report_lines += ['</tr>']

        # rest of rows
        for genome_i,genome_id in enumerate(genome_ids):
            if genome_i == 0:
                continue
            html_report_lines += ['<tr>']
            for fam in fams:
                cell_color = graph_color
                html_report_lines += ['<td bgcolor="'+cell_color+'"><font color="'+cell_color+'" size='+graph_fontsize+'>'+graph_char+'</font></td>']
            html_report_lines += ['</tr>']
        
        html_report_lines += ['</table>']
        html_report_lines += ['</body>']
        html_report_lines += ['</html>']

        reportObj['direct_html'] = "\n".join(html_report_lines)


        # save report object
        #
        report = KBaseReport(self.callbackURL, token=ctx['token'], service_ver=SERVICE_VER)
        #report_info = report.create({'report':reportObj, 'workspace_name':params['workspace_name']})
        report_info = report.create_extended_report(reportObj)

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
           "input_pangenome_ref" of type "data_obj_ref"
        :returns: instance of type "view_pan_circle_plot_Output" ->
           structure: parameter "report_name" of String, parameter
           "report_ref" of String
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN view_pan_circle_plot
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
           "workspace_name" (** Common types), parameter "input_genome_ref"
           of type "data_obj_ref", parameter "input_pangenome_ref" of type
           "data_obj_ref", parameter "input_speciesTree_ref" of type
           "data_obj_ref"
        :returns: instance of type "view_pan_phylo_Output" -> structure:
           parameter "report_name" of String, parameter "report_ref" of String
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN view_pan_phylo
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
