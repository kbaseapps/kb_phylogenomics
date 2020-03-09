# -*- coding: utf-8 -*-
#BEGIN_HEADER
from __future__ import division
from __future__ import print_function

import copy
import math
import os
import re
import sys
import uuid
import random
from datetime import datetime
from pprint import pformat,pprint

import ete3
import matplotlib.pyplot as pyplot  # use this instead
from matplotlib.patches import Arc
from matplotlib.patches import Rectangle

from installed_clients.SpeciesTreeBuilderClient import SpeciesTreeBuilder
from installed_clients.KBaseReportClient import KBaseReport
from installed_clients.DataFileUtilClient import DataFileUtil as DFUClient
from installed_clients.DomainAnnotationClient import DomainAnnotation
from installed_clients.kb_blastClient import kb_blast
from installed_clients.WorkspaceClient import Workspace as workspaceService
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
    VERSION = "1.5.1"
    GIT_URL = "https://github.com/dcchivian/kb_phylogenomics"
    GIT_COMMIT_HASH = "9a15480a5f41f7eaf71235012ff0c0bd37d5893a"

    #BEGIN_CLASS_HEADER

    def now_ISO(self):
#        now_timestamp = datetime.datetime.now()
#        now_secs_from_epoch = (end_timestamp - datetime.datetime(1970,1,1)).total_seconds()
#        now_timestamp_in_iso = datetime.datetime.fromtimestamp(int(now_secs_from_epoch)).strftime('%Y-%m-%d_%T')
        now_timestamp = datetime.now()
        now_secs_from_epoch = (now_timestamp - datetime(1970,1,1)).total_seconds()
        now_timestamp_in_iso = datetime.fromtimestamp(int(now_secs_from_epoch)).strftime('%Y-%m-%d_%T')
        return now_timestamp_in_iso

    def log(self, target, message):
        message = '['+self.now_ISO()+'] '+message
        if target is not None:
            target.append(message)
        print(message)
        sys.stdout.flush()

    def _get_dark_pretty_html_color(self, index, seed):

        # colors from https://www.w3schools.com/colors/colors_names.asp

        dark_pretty_html_colors = [
            #"AliceBlue",
            #"AntiqueWhite",
            #"Aqua",
            #"Aquamarine",
            #"Azure",
            #"Beige",
            #"Bisque",
            #"Black",
            #"BlanchedAlmond",
            "Blue",
            "BlueViolet",
            "Brown",
            #"BurlyWood",
            "CadetBlue",
            #"Chartreuse",
            "Chocolate",
            "Coral",
            "CornflowerBlue",
            #"Cornsilk",
            "Crimson",
            #"Cyan",
            "DarkBlue",
            "DarkCyan",
            "DarkGoldenRod",
            #"DarkGray",
            #"DarkGrey",
            "DarkGreen",
            #"DarkKhaki",
            "DarkMagenta",
            #"DarkOliveGreen",
            "DarkOrange",
            "DarkOrchid",
            "DarkRed",
            "DarkSalmon",
            #"DarkSeaGreen",
            "DarkSlateBlue",
            #"DarkSlateGray",
            #"DarkSlateGrey",
            "DarkTurquoise",
            "DarkViolet",
            "DeepPink",
            "DeepSkyBlue",
            #"DimGray",
            #"DimGrey",
            "DodgerBlue",
            "FireBrick",
            #"FloralWhite",
            "ForestGreen",
            "Fuchsia",
            #"Gainsboro",
            #"GhostWhite",
            "Gold",
            "GoldenRod",
            #"Gray",
            #"Grey",
            "Green",
            #"GreenYellow",
            #"HoneyDew",
            "HotPink",
            "IndianRed",
            "Indigo",
            #"Ivory",
            #"Khaki",
            #"Lavender",
            #"LavenderBlush",
            #"LawnGreen",
            #"LemonChiffon",
            "LightBlue",
            "LightCoral",
            #"LightCyan",
            #"LightGoldenRodYellow",
            #"LightGray",
            #"LightGrey",
            "LightGreen",
            "LightPink",
            "LightSalmon",
            "LightSeaGreen",
            "LightSkyBlue",
            #"LightSlateGray",
            #"LightSlateGrey",
            #"LightSteelBlue",
            #"LightYellow",
            #"Lime",
            "LimeGreen",
            #"Linen",
            "Magenta",
            "Maroon",
            "MediumAquaMarine",
            "MediumBlue",
            "MediumOrchid",
            "MediumPurple",
            "MediumSeaGreen",
            "MediumSlateBlue",
            "MediumSpringGreen",
            "MediumTurquoise",
            "MediumVioletRed",
            "MidnightBlue",
            #"MintCream",
            #"MistyRose",
            #"Moccasin",
            #"NavajoWhite",
            "Navy",
            #"OldLace",
            #"Olive",
            #"OliveDrab",
            "Orange",
            "OrangeRed",
            "Orchid",
            #"PaleGoldenRod",
            #"PaleGreen",
            #"PaleTurquoise",
            "PaleVioletRed",
            #"PapayaWhip",
            #"PeachPuff",
            "Peru",
            #"Pink",
            "Plum",
            #"PowderBlue",
            "Purple",
            "RebeccaPurple",
            "Red",
            #"RosyBrown",
            "RoyalBlue",
            #"SaddleBrown",
            "Salmon",
            "SandyBrown",
            "SeaGreen",
            #"SeaShell",
            "Sienna",
            #"Silver",
            "SkyBlue",
            "SlateBlue",
            #"SlateGray",
            #"SlateGrey",
            #"Snow",
            #"SpringGreen",
            "SteelBlue",
            #"Tan",
            "Teal",
            #"Thistle",
            "Tomato",
            "Turquoise",
            "Violet",
            #"Wheat",
            #"White",
            #"WhiteSmoke",
            #"Yellow",
            "YellowGreen"
        ]

        if seed != None:
            random.seed(index * seed)
            index = random.randint (0,len(dark_pretty_html_colors)-1)
        else:
            index = index % len(dark_pretty_html_colors)

        return dark_pretty_html_colors[index]

    def _check_SEED_function_defined_in_feature(self, feature):
        if feature.get('function') or feature.get('functions'):
            return True
        else:
            return False

    def _get_SEED_annotations(self, feature):
        annot_set = []
        if feature.get('function'):
            annot_set = feature['function'].strip().split(';')
        elif feature.get('functions'):
            annot_set = feature['functions']
        return annot_set

    def _standardize_SEED_subsys_ID (self, domfam_orig):
        domfam = domfam_orig.strip()
        domfam = re.sub(' *\#.*$', '', domfam)
        domfam = re.sub(' *\(EC [\d\.\-\w]*\) *$', '', domfam)
        domfam = re.sub(' *\(TC [\d\.\-\w]*\) *$', '', domfam)
        domfam = re.sub(' ', '_', domfam)
        domfam = domfam.lower()
        domfam = 'SEED' + domfam
        return domfam

    def _configure_categories(self, params):

        domain_desc_basepath = os.path.abspath('/kb/module/data/domain_desc')
        domain_to_cat_map_path = dict()
        domain_cat_names_path = dict()
        domain_fam_names_path = dict()
        domain_to_cat_map_path['COG'] = os.path.join(domain_desc_basepath, 'COG_2014.tsv')
        domain_cat_names_path['COG'] = os.path.join(domain_desc_basepath, 'COG_2014_funcat.tsv')
        domain_fam_names_path['COG'] = os.path.join(domain_desc_basepath, 'COG_2014.tsv')
        domain_to_cat_map_path['PF'] = os.path.join(domain_desc_basepath, 'Pfam-A.clans.tsv')
        domain_cat_names_path['PF'] = os.path.join(domain_desc_basepath, 'Pfam-A.clans_names.tsv')
        domain_fam_names_path['PF'] = os.path.join(domain_desc_basepath, 'Pfam-A.clans.tsv')
        domain_to_cat_map_path['TIGR'] = os.path.join(domain_desc_basepath, 'TIGRInfo.tsv')
        domain_cat_names_path['TIGR'] = os.path.join(domain_desc_basepath, 'tigrrole2go.txt')
        #domain_fam_names_path['TIGR']  = os.path.join(domain_desc_basepath, 'tigrfams2go.txt')
        domain_fam_names_path['TIGR'] = os.path.join(domain_desc_basepath, 'TIGRInfo.tsv')
        domain_to_cat_map_path['SEED'] = os.path.join(domain_desc_basepath, 'SEED_subsys.txt')
        domain_cat_names_path['SEED'] = os.path.join(domain_desc_basepath, 'SEED_funcat.txt')
        #domain_cat_names_path['SEED']  = os.path.join(domain_desc_basepath, 'SEED_subsys.txt')
        domain_fam_names_path['SEED'] = os.path.join(domain_desc_basepath, 'SEED_subsys.txt')

        cats = []
        cat2name = dict()
        cat2group = dict()
        domfam2cat = dict()
        cat2domfams = dict()
        namespaces_reading = dict()

        # categories are high-level summations
        if params['namespace'] != 'custom':
            for namespace in ['COG', 'PF', 'TIGR', 'SEED']:
                if params['namespace'] == namespace:
                    namespaces_reading[namespace] = True

        # read all mappings between groups and domfams
        tigrrole_id2cat = dict()
        for namespace in ['COG', 'PF', 'TIGR', 'SEED']:

            cat2name[namespace] = dict()
            cat2group[namespace] = dict()
            domfam2cat[namespace] = dict()
            cat2domfams[namespace] = dict()

            # get high-level cats
            with open(domain_cat_names_path[namespace], 'r', 0) as dom_cat_handle:
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
                        cat_name = re.sub(' *\> GO:.*$', '', cat_name_plus_go_terms)
                        cat2name[namespace][cat] = cat_name
                        cat2group[namespace][cat] = cat_group

                    elif namespace == 'SEED':
                        #[cat_group, cat_subgroup, cat, domfam] = line.split("\t")[0:4]
                        [cat_group, cat] = line.split("\t")[0:2]
                        if namespace == params['namespace'] and cat not in cats:
                            cats.append(cat)
                        cat_disp = re.sub('_', ' ', cat)
                        cat2name[namespace][cat] = cat_disp
                        cat2group[namespace][cat] = cat_group

            # get domfam to cat map, and vice versa
            with open(domain_to_cat_map_path[namespace], 'r', 0) as dom2cat_map_handle:
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
                        domfam = self._standardize_SEED_subsys_ID(domfam)

                    domfam2cat[namespace][domfam] = cat
                    if cat not in cat2domfams[namespace]:
                        cat2domfams[namespace][cat] = []
                    cat2domfams[namespace][cat].append(domfam)

        # add extra target fams
        target_fams = []
        extra_target_fams = []
        extra_target_fam_groups = []
        domfam2group = dict()
        domfam2name = dict()

        # custom domains
        if params['namespace'] == 'custom':

            # add target fams
            if 'target_fams' in params['custom_target_fams'] and params['custom_target_fams']['target_fams']:
                for target_fam in params['custom_target_fams']['target_fams']:
                    target_fam = target_fam.strip()
                    if target_fam == '':
                        continue

                    target_fam = re.sub("^cog", "COG", target_fam, flags=re.IGNORECASE)
                    target_fam = re.sub("^pf", "PF", target_fam, flags=re.IGNORECASE)
                    target_fam = re.sub("^tigr", "TIGR", target_fam, flags=re.IGNORECASE)
                    target_fam = re.sub("^seed", "SEED", target_fam, flags=re.IGNORECASE)
                    target_fam = re.sub("^PFAM", "PF", target_fam, flags=re.IGNORECASE)
                    target_fam = re.sub("^P-FAM", "PF", target_fam, flags=re.IGNORECASE)
                    target_fam = re.sub("^P_FAM", "PF", target_fam, flags=re.IGNORECASE)
                    target_fam = re.sub("^TIGRFAM", "TIGR", target_fam, flags=re.IGNORECASE)
                    target_fam = re.sub("^TIGR-FAM", "TIGR", target_fam, flags=re.IGNORECASE)
                    target_fam = re.sub("^TIGR_FAM", "TIGR", target_fam, flags=re.IGNORECASE)

                    target_fam = re.sub("^COG:", "COG", target_fam, flags=re.IGNORECASE)
                    target_fam = re.sub("^COG-", "COG", target_fam, flags=re.IGNORECASE)
                    target_fam = re.sub("^COG_", "COG", target_fam, flags=re.IGNORECASE)
                    target_fam = re.sub("^COG *", "COG", target_fam, flags=re.IGNORECASE)
                    target_fam = re.sub("^PF:", "PF", target_fam, flags=re.IGNORECASE)
                    target_fam = re.sub("^PF-", "PF", target_fam, flags=re.IGNORECASE)
                    target_fam = re.sub("^PF_", "PF", target_fam, flags=re.IGNORECASE)
                    target_fam = re.sub("^PF *", "PF", target_fam, flags=re.IGNORECASE)
                    target_fam = re.sub("^TIGR:", "TIGR", target_fam, flags=re.IGNORECASE)
                    target_fam = re.sub("^TIGR-", "TIGR", target_fam, flags=re.IGNORECASE)
                    target_fam = re.sub("^TIGR_", "TIGR", target_fam, flags=re.IGNORECASE)
                    target_fam = re.sub("^TIGR *", "TIGR", target_fam, flags=re.IGNORECASE)
                    target_fam = re.sub("^SEED:", "SEED", target_fam, flags=re.IGNORECASE)
                    target_fam = re.sub("^SEED-", "SEED", target_fam, flags=re.IGNORECASE)
                    target_fam = re.sub("^SEED_", "SEED", target_fam, flags=re.IGNORECASE)
                    target_fam = re.sub("^SEED *", "SEED", target_fam, flags=re.IGNORECASE)

                    num_id_len = dict()
                    num_id_len['COG'] = 4
                    num_id_len['PF'] = 5
                    num_id_len['TIGR'] = 5

                    #self.log (console, "TARGET_FAM A: '"+target_fam+"'")  # DEBUG

                    if target_fam.startswith('SEED'):
                        namespaces_reading['SEED'] = True
                        target_fam = target_fam.strip()
                        target_fam = re.sub(' *\(EC [\d\.\-\w]*\) *$', '', target_fam)
                        target_fam = re.sub(' *\(TC [\d\.\-\w]*\) *$', '', target_fam)
                        target_fam = re.sub(' ', '_', target_fam)
                    else:
                        namespace_found = False
                        for namespace_iter in ['COG', 'PF', 'TIGR']:
                            if target_fam.startswith(namespace_iter):
                                this_namespace = namespace_iter
                                namespaces_reading[this_namespace] = True
                                target_fam = re.sub(this_namespace, "", target_fam)
                                namespace_found = True
                                break
                        if not namespace_found:
                            raise ValueError("unrecognized custom domain family: '" + str(target_fam) + "'")
                        leading_zeros = ''
                        for c_i in range(num_id_len[this_namespace] - len(str(target_fam))):
                            leading_zeros += '0'
                        target_fam = this_namespace + leading_zeros + target_fam

                    #self.log (console, "TARGET_FAM B: '"+target_fam+"'")  # DEBUG

                    target_fams.append(target_fam)


            for target_set in ['extra_target_fam_groups_COG', 'extra_target_fam_groups_PFAM', 'extra_target_fam_groups_TIGR', 'extra_target_fam_groups_SEED']:
                if target_set in params['custom_target_fams'] and params['custom_target_fams'][target_set]:
                    extra_target_fam_groups.extend(params['custom_target_fams'][target_set])

            if extra_target_fam_groups:
                for target_group in extra_target_fam_groups:
                    target_group = target_group.strip()
                    if target_group == '':
                        continue

                    namespace = re.sub(":.*$", "", target_group)
                    namespaces_reading[namespace] = True

                    if namespace == 'COG':
                        this_group = re.sub("COG: ", "", target_group)
                        this_group = re.sub(":.*$", "", this_group)
                    elif namespace == 'PF':
                        this_group = re.sub("PF: Clan ", "", target_group)
                        this_group = re.sub(":.*$", "", this_group)
                    elif namespace == 'TIGR':
                        this_group = re.sub("TIGR: role:", "", target_group)
                        this_group = re.sub(":.*$", "", this_group)
                        this_group = 'TIGR_role:' + this_group
                    elif namespace == 'SEED':
                        this_group = re.sub("SEED: ", "", target_group)

                    for domfam in cat2domfams[namespace][this_group]:
                        extra_target_fams.append(domfam)
                        domfam2group[domfam] = target_group

            # we have our targets
            cats = target_fams + extra_target_fams

            # store names of targets
            for namespace in namespaces_reading.keys():
                domfam2name[namespace] = dict()

                if namespace == 'COG':
                    with open(domain_fam_names_path[namespace], 'r', 0) as dom_fam_handle:
                        for line in dom_fam_handle.readlines():
                            line = line.strip()
                            [domfam, cat_class, domfam_name] = line.split("\t")[0:3]
                            domfam2name[namespace][domfam] = domfam_name

                elif namespace == 'PF':
                    with open(domain_fam_names_path[namespace], 'r', 0) as dom_fam_handle:
                        for line in dom_fam_handle.readlines():
                            line = line.strip()
                            [domfam, class_id, class_name, domfam_id, domfam_name] = line.split("\t")[0:5]
                            if domfam_name.startswith(domfam_id):
                                combo_name = domfam_name
                            else:
                                combo_name = domfam_id + ': ' + domfam_name
                            domfam2name[namespace][domfam] = combo_name

                elif namespace == 'TIGR':
                    with open(domain_fam_names_path[namespace], 'r', 0) as dom_fam_handle:
                        for line in dom_fam_handle.readlines():
                            line = line.strip()
                            if line.startswith('!'):
                                continue
                            [domfam_id, domfam, cat_group, cat_id, domfam_name, ec_id, domfam_desc] = line.split("\t")[
                                0:7]
                            if domfam_name != '':
                                if domfam_desc.startswith(domfam_name):
                                    combo_name = domfam_desc
                                else:
                                    combo_name = domfam_name + ': ' + domfam_desc
                            else:
                                if domfam_desc.startswith(domfam_id):
                                    combo_name = domfam_desc
                                else:
                                    combo_name = domfam_id + ': ' + domfam_desc
                            if ec_id != '':
                                combo_name += ' (EC ' + ec_id + ')'

                            domfam2name[namespace][domfam] = combo_name

                elif namespace == 'SEED':
                    with open(domain_fam_names_path[namespace], 'r', 0) as dom_fam_handle:
                        for line in dom_fam_handle.readlines():
                            line = line.strip()
                            [level1, level2, level3, domfam] = line.split("\t")[0:4]

                            domfam_desc = domfam
                            domfam = self._standardize_SEED_subsys_ID(domfam)
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
            raise ValueError("Unknown namespace: '" + str(params['namespace']) + "'")

        return(cats, cat2name, cat2group, domfam2cat, cat2domfams, namespaces_reading, target_fams,
               extra_target_fams, extra_target_fam_groups, domfam2group, domfam2name)

    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.workspaceURL = config['workspace-url']
        self.shockURL = config['shock-url']
        #self.handleURL = config['handle-service-url']
        self.serviceWizardURL = config['service-wizard-url']
        self.callbackURL = os.environ['SDK_CALLBACK_URL']
        self.scratch = os.path.abspath(config['scratch'])

        #pprint(config)

        if not os.path.exists(self.scratch):
            os.makedirs(self.scratch)

        #self.genome_feature_id_delim = '.f:'

        #END_CONSTRUCTOR
        pass


    def view_tree(self, ctx, params):
        """
        :param params: instance of type "view_tree_Input" (view_tree() ** **
           show a KBase Tree and make newick and images downloadable) ->
           structure: parameter "workspace_name" of type "workspace_name" (**
           Common types), parameter "input_tree_ref" of type "data_obj_ref",
           parameter "desc" of String, parameter "genome_disp_name_config" of
           String, parameter "show_skeleton_genome_sci_name" of type "bool",
           parameter "reference_genome_disp" of mapping from type
           "data_obj_ref" to mapping from String to String, parameter
           "skeleton_genome_disp" of mapping from type "data_obj_ref" to
           mapping from String to String, parameter "user_genome_disp" of
           mapping from type "data_obj_ref" to mapping from String to String,
           parameter "user2_genome_disp" of mapping from type "data_obj_ref"
           to mapping from String to String, parameter
           "color_for_reference_genomes" of String, parameter
           "color_for_skeleton_genomes" of String, parameter
           "color_for_user_genomes" of String, parameter
           "color_for_user2_genomes" of String, parameter "tree_shape" of
           String
        :returns: instance of type "view_tree_Output" -> structure: parameter
           "report_name" of String, parameter "report_ref" of String
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN view_tree

        #### STEP 0: init
        ##
        dfu = DFUClient(self.callbackURL)
        console = []
        invalid_msgs = []
        self.log(console, 'Running view_tree() with params=')
        self.log(console, "\n" + pformat(params))
        report = ''
        timestamp = int((datetime.utcnow() - datetime.utcfromtimestamp(0)).total_seconds() * 1000)
        output_dir = os.path.join(self.scratch, 'output_' + str(timestamp))
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        #SERVICE_VER = 'dev'  # DEBUG
        SERVICE_VER = 'release'
        token = ctx['token']
        try:
            wsClient = workspaceService(self.workspaceURL, token=token)
        except:
            raise ValueError("unable to instantiate wsClient")

        #### STEP 1: do some basic checks
        ##
        required_params = ['workspace_name',
                           'input_tree_ref'
                           ]
        for arg in required_params:
            if arg not in params or params[arg] == None or params[arg] == '':
                raise ValueError("Must define required param: '" + arg + "'")

        #### STEP 2: load the method provenance from the context object
        ##
        self.log(console, "SETTING PROVENANCE")  # DEBUG
        provenance = [{}]
        if 'provenance' in ctx:
            provenance = ctx['provenance']
        # add additional info to provenance here, in this case the input data object reference
        provenance[0]['input_ws_objects'] = []
        provenance[0]['input_ws_objects'].append(params['input_tree_ref'])
        provenance[0]['service'] = 'kb_phylogenomics'
        provenance[0]['method'] = 'view_tree'

        #### STEP 3: Get tree and save as newick file
        ##
        try:
            objects = wsClient.get_objects([{'ref': params['input_tree_ref']}])
            data = objects[0]['data']
            info = objects[0]['info']
            intree_name = info[1]
            intree_type_name = info[2].split('.')[1].split('-')[0]

        except Exception as e:
            raise ValueError('Unable to fetch input_tree_ref object from workspace: ' + str(e))
            #to get the full stack trace: traceback.format_exc()

        if intree_type_name == 'Tree':
            tree_in = data
        else:
            raise ValueError('Cannot yet handle input_tree type of: ' + intree_type_name)

        intree_newick_file_path = os.path.join(output_dir, intree_name + ".newick")
        self.log(console, 'writing intree file: ' + intree_newick_file_path)
        with open(intree_newick_file_path, 'w', 0) as intree_newick_file_handle:
            intree_newick_file_handle.write(tree_in['tree'])

        # upload
        try:
            newick_upload_ret = dfu.file_to_shock({'file_path': intree_newick_file_path,
                                                   #'pack': 'zip'})
                                                   'make_handle': 0})
        except:
            raise ValueError('error uploading newick file to shock')


        #### STEP 4: change disp labels if provided as input
        ##
        genome_ref_to_label_disp = dict()
        if tree_in.get('default_node_labels') and tree_in.get('ws_refs'):
            genome_ref_to_node_id = dict()
            genome_node_id_to_ref = dict()
            for genome_node_id in tree_in['default_node_labels'].keys():
                genome_label = tree_in['default_node_labels'][genome_node_id]
                genome_ref   = tree_in['ws_refs'][genome_node_id]['g'][0]
                if genome_ref_to_node_id.get(genome_ref):
                    raise ValueError ("FAILURE: repeat genome_ref "+genome_ref+" in tree")
                if genome_node_id_to_ref.get(genome_node_id):
                    raise ValueError ("FAILURE: repeat genome_node_id "+genome_node_id+" in tree")
                genome_ref_to_node_id[genome_ref] = genome_node_id
                genome_node_id_to_ref[genome_node_id] = genome_ref
                genome_ref_to_label_disp[genome_ref] = genome_label

        if params.get('reference_genome_disp'):
            for genome_ref in params['reference_genome_disp'].keys():
                if params['reference_genome_disp'][genome_ref].get('label'):
                    genome_ref_to_label_disp[genome_ref] = params['reference_genome_disp'][genome_ref]['label']
        if params.get('skeleton_genome_disp'):
            for genome_ref in params['skeleton_genome_disp'].keys():
                if params['skeleton_genome_disp'][genome_ref].get('label'):
                    genome_ref_to_label_disp[genome_ref] = params['skeleton_genome_disp'][genome_ref]['label']
        if params.get('user_genome_disp'):
            for genome_ref in params['user_genome_disp'].keys():
                if params['user_genome_disp'][genome_ref].get('label'):
                    genome_ref_to_label_disp[genome_ref] = params['user_genome_disp'][genome_ref]['label']


        #### STEP 4: if labels defined, make separate newick-labels file
        ##     (NOTE: adjust IDs so ETE3 parse doesn't choke on conflicting chars)
        ##
        if 'default_node_labels' in tree_in:
            newick_labels_file = intree_name + '-labels.newick'
            output_newick_labels_file_path = os.path.join(output_dir, newick_labels_file)
            #default_row_ids = tree_in['default_row_labels']
            #new_ids = dict()
            #for row_id in default_row_ids.keys():
            #    new_ids[row_id] = default_row_ids[row_id]

            mod_newick_buf = tree_in['tree']
            mod_newick_buf = re.sub('\|', '%' + '|'.encode("hex"), mod_newick_buf)
            #for row_id in new_ids.keys():
            for node_id in tree_in['default_node_labels'].keys():
                label = None
                if node_id in genome_node_id_to_ref:
                    genome_ref = genome_node_id_to_ref[node_id]
                    if genome_ref in genome_ref_to_label_disp:
                        label = genome_ref_to_label_disp[genome_ref]
                if not label:
                    label = tree_in['default_node_labels'][node_id]
                #self.log (console, "node "+node_id+" label B4: '"+label+"'")  # DEBUG
                label = re.sub(' \(kb[^\)]*\)', '', label)  # just get rid of problematic (kb|g.1234)
                label = re.sub('\s', '_', label)
                #label = re.sub('\/','%'+'/'.encode("hex"), label)
                #label = re.sub(r'\\','%'+'\\'.encode("hex"), label)
                #label = re.sub('\[','%'+'['.encode("hex"), label)
                #label = re.sub('\]','%'+']'.encode("hex"), label)
                label = re.sub('\(', '[', label)
                label = re.sub('\)', ']', label)
                label = re.sub('\:', '%' + ':'.encode("hex"), label)
                label = re.sub('\;', '%' + ';'.encode("hex"), label)
                label = re.sub('\|', '%' + '|'.encode("hex"), label)
                #self.log (console, "node "+node_id+" label AF: '"+label+"'")  # DEBUG
                #self.log (console, "NEWICK B4: '"+mod_newick_buf+"'")  # DEBUG
                mod_node_id = re.sub('\|', '%' + '|'.encode("hex"), node_id)
                mod_newick_buf = re.sub('\(' + mod_node_id + '\:', '(' + label + ':', mod_newick_buf)
                mod_newick_buf = re.sub('\,' + mod_node_id + '\:', ',' + label + ':', mod_newick_buf)
                #self.log (console, "NEWICK AF: '"+mod_newick_buf+"'")  # DEBUG

                #self.log(console, "new_id: '"+new_id+"' label: '"+label+"'")  # DEBUG

            mod_newick_buf = re.sub('_', ' ', mod_newick_buf)
            with open(output_newick_labels_file_path, 'w', 0) as output_newick_labels_file_handle:
                output_newick_labels_file_handle.write(mod_newick_buf)

            # upload
            try:
                newick_labels_upload_ret = dfu.file_to_shock({'file_path': output_newick_labels_file_path,
                                                              #'pack': 'zip'})
                                                              'make_handle': 0})
            except:
                raise ValueError('error uploading newick labels file to shock')


        #### STEP 5: Create html with tree image
        ##
        html_output_dir = os.path.join(output_dir, 'output_html.' + str(timestamp))
        if not os.path.exists(html_output_dir):
            os.makedirs(html_output_dir)
        html_file = intree_name + '.html'
        png_file = intree_name + '.png'
        pdf_file = intree_name + '.pdf'
        output_html_file_path = os.path.join(html_output_dir, html_file)
        output_png_file_path = os.path.join(html_output_dir, png_file)
        output_pdf_file_path = os.path.join(output_dir, pdf_file)
        newick_buf = tree_in['tree']
        #if 'default_node_labels' in tree_in:
        #    newick_buf = mod_newick_buf
        self.log(console, "NEWICK_BUF: '" + newick_buf + "'")

        # init ETE3 objects
        t = ete3.Tree(newick_buf)
        t.ladderize()
        ts = ete3.TreeStyle()

        # determine if there are more user or non-user genomes in tree to color fewer
        #user_genome_color      = "#fafcc2"   # too light yellow
        leaf_colors = dict()
        leaf_colors['white']     = "#FFFFFF"
        leaf_colors['mustard']   = "#FEE787"
        leaf_colors['violet']    = "#DFCFFC"
        leaf_colors['lightblue'] = "#A8EAFC"
        leaf_colors['darkblue']  = "#A8C1FC"
        default_user_genome_color = leaf_colors['mustard']
        default_reference_genome_color = leaf_colors['lightblue']
        color_by_user_genome = False
        color_by_reference_genome = False
        genome_total = 0
        user_genome_cnt = 0
        for n in t.traverse():
            if n.is_leaf():
                genome_total += 1
                #if "User Genome" in n.name:
                #    user_genome_cnt += 1
                node_id = n.name
                if node_id in genome_node_id_to_ref:
                    genome_ref = genome_node_id_to_ref[node_id]
                    if genome_ref in genome_ref_to_label_disp:
                        if "User Genome" in genome_ref_to_label_disp[genome_ref]:
                            user_genome_cnt += 1
        if float(user_genome_cnt) / float(genome_total) < 0.5:
            color_by_user_genome = True
        else:
            color_by_reference_genome = True

        # check for user, skeleton, and/or reference color override
        if tree_in.get('ws_refs'):
            genome_ref_to_color = dict()

            for genome_node_id in tree_in['ws_refs'].keys():
                genome_ref = tree_in['ws_refs'][genome_node_id]['g'][0]

                # reference genome colors
                if params.get('reference_genome_disp'):
                    color_by_user_genome = False
                    color_by_reference_genome = False
                    for genome_ref in params['reference_genome_disp'].keys():
                        genome_ref_to_color[genome_ref] = leaf_colors['white']
                        if params['reference_genome_disp'][genome_ref]['color'] == 'default':
                            if params.get('color_for_reference_genomes') and \
                               params['color_for_reference_genomes'] != 'no_color':
                                genome_ref_to_color[genome_ref] = leaf_colors[params['color_for_reference_genomes']]
                        else:
                            genome_ref_to_color[genome_ref] = params['reference_genome_disp'][genome_ref]['color']

                # skeleton genome colors
                if params.get('skeleton_genome_disp'):
                    color_by_user_genome = False
                    color_by_reference_genome = False
                    for genome_ref in params['skeleton_genome_disp'].keys():
                        genome_ref_to_color[genome_ref] = leaf_colors['white']
                        if params['skeleton_genome_disp'][genome_ref]['color'] == 'default':
                            if params.get('color_for_skeleton_genomes') and \
                               params['color_for_skeleton_genomes'] != 'no_color':
                                genome_ref_to_color[genome_ref] = leaf_colors[params['color_for_skeleton_genomes']]
                        else:
                            genome_ref_to_color[genome_ref] = params['skeleton_genome_disp'][genome_ref]['color']

                # user genome colors
                if params.get('user_genome_disp'):
                    color_by_user_genome = False
                    color_by_reference_genome = False
                    for genome_ref in params['user_genome_disp'].keys():
                        genome_ref_to_color[genome_ref] = leaf_colors['white']
                        if params['user_genome_disp'][genome_ref]['color'] == 'default':
                            if params.get('color_for_user_genomes') and \
                               params['color_for_user_genomes'] != 'no_color':
                                genome_ref_to_color[genome_ref] = leaf_colors[params['color_for_user_genomes']]
                        else:
                            genome_ref_to_color[genome_ref] = params['user_genome_disp'][genome_ref]['color']

                # user2 genome colors
                if params.get('user2_genome_disp'):
                    color_by_user_genome = False
                    color_by_reference_genome = False
                    for genome_ref in params['user2_genome_disp'].keys():
                        genome_ref_to_color[genome_ref] = leaf_colors['white']
                        if params['user2_genome_disp'][genome_ref]['color'] == 'default':
                            if params.get('color_for_user2_genomes') and \
                               params['color_for_user2_genomes'] != 'no_color':
                                genome_ref_to_color[genome_ref] = leaf_colors[params['color_for_user2_genomes']]
                        else:
                            genome_ref_to_color[genome_ref] = params['user2_genome_disp'][genome_ref]['color']


        # customize
        ts.show_leaf_name = True
        ts.show_branch_length = False
        ts.show_branch_support = True
        #ts.scale = 50 # 50 pixels per branch length unit
        ts.branch_vertical_margin = 5  # pixels between adjacent branches
        title_disp = intree_name
        if 'desc' in params and params['desc'] != None and params['desc'] != '':
            title_disp += ': ' + params['desc']
        ts.title.add_face(ete3.TextFace(title_disp, fsize=10), column=0)

        node_style = ete3.NodeStyle()
        node_style["fgcolor"] = "#606060"  # for node balls
        node_style["size"] = 10  # for node balls (gets reset based on support)
        node_style["vt_line_color"] = "#606060"
        node_style["hz_line_color"] = "#606060"
        node_style["vt_line_width"] = 2
        node_style["hz_line_width"] = 2
        node_style["vt_line_type"] = 0  # 0 solid, 1 dashed, 2 dotted
        node_style["hz_line_type"] = 0

        leaf_style = ete3.NodeStyle()
        leaf_style["fgcolor"] = "#ffffff"  # for node balls
        leaf_style["size"] = 2  # for node balls (we're using it to add space)
        leaf_style["vt_line_color"] = "#606060"  # unecessary
        leaf_style["hz_line_color"] = "#606060"
        leaf_style["vt_line_width"] = 2
        leaf_style["hz_line_width"] = 2
        leaf_style["vt_line_type"] = 0  # 0 solid, 1 dashed, 2 dotted
        leaf_style["hz_line_type"] = 0

        for n in t.traverse():
            if n.is_leaf():
                style = copy.copy(leaf_style)

                node_id = n.name
                if node_id in genome_node_id_to_ref:
                    genome_ref = genome_node_id_to_ref[node_id]
                    if genome_ref in genome_ref_to_label_disp:
                        label = genome_ref_to_label_disp[genome_ref]
                    else:
                        label = n.name

                n.name = label

                if color_by_user_genome and "User Genome" in n.name:
                    style["bgcolor"] = default_user_genome_color
                elif color_by_reference_genome and "User Genome" not in n.name:
                    style["bgcolor"] = default_reference_genome_color
                else:
                    if genome_ref in genome_ref_to_color:
                        #style["bgcolor"] = genome_ref_to_color[genome_ref]
                        style["hz_line_color"] = genome_ref_to_color[genome_ref]
                        style["hz_line_width"] = 5 * leaf_style["hz_line_width"]

            else:
                style = copy.copy(node_style)

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
        img_in_width = round(float(img_pix_width) / float(dpi), 1)
        img_html_width = img_pix_width // 2
        t.render(output_png_file_path, w=img_in_width, units=img_units, dpi=dpi, tree_style=ts)
        t.render(output_pdf_file_path, w=img_in_width, units=img_units, tree_style=ts)  # dpi irrelevant

        # make html
        html_report_lines = []
        html_report_lines += ['<html>']
        html_report_lines += ['<head><title>KBase Tree: ' + intree_name + '</title></head>']
        html_report_lines += ['<body bgcolor="white">']
        html_report_lines += ['<img width=' + str(img_html_width) + ' src="' + png_file + '">']
        html_report_lines += ['</body>']
        html_report_lines += ['</html>']

        html_report_str = "\n".join(html_report_lines)
        with open(output_html_file_path, 'w', 0) as html_handle:
            html_handle.write(html_report_str)

        # upload images and html
        try:
            png_upload_ret = dfu.file_to_shock({'file_path': output_png_file_path,
                                                #'pack': 'zip'})
                                                'make_handle': 0})
        except:
            raise ValueError('error uploading png file to shock')
        try:
            pdf_upload_ret = dfu.file_to_shock({'file_path': output_pdf_file_path,
                                                #'pack': 'zip'})
                                                'make_handle': 0})
        except:
            raise ValueError('error uploading pdf file to shock')
        try:
            html_upload_ret = dfu.file_to_shock({'file_path': html_output_dir,
                                                 'make_handle': 0,
                                                 'pack': 'zip'})
        except:
            raise ValueError('error uploading png file to shock')


        # Create report obj
        #
        reportName = 'view_tree_report_' + str(uuid.uuid4())
        #report += output_newick_buf+"\n"
        reportObj = {'objects_created': [],
                     'direct_html_link_index': 0,
                     'file_links': [],
                     'html_links': [],
                     'workspace_name': params['workspace_name'],
                     'report_object_name': reportName
                     }
        #reportObj['objects_created'].append({'ref': str(params['workspace_name'])+'/'+str(params['output_name']),'description': params['output_name']+' Tree'})
        reportObj['html_links'] = [{'shock_id': html_upload_ret['shock_id'],
                                    'name': html_file,
                                    'label': intree_name + ' HTML'
                                    }
                                   ]
        reportObj['file_links'] = [{'shock_id': newick_upload_ret['shock_id'],
                                    'name': intree_name + '.newick',
                                    'label': intree_name + ' NEWICK'
                                    }
                                   ]
        if 'default_node_labels' in tree_in:
            reportObj['file_links'].append({'shock_id': newick_labels_upload_ret['shock_id'],
                                            'name': intree_name + '-labels.newick',
                                            'label': intree_name + ' NEWICK (with labels)'
                                            })

        reportObj['file_links'].extend([{'shock_id': png_upload_ret['shock_id'],
                                         'name': intree_name + '.png',
                                         'label': intree_name + ' PNG'
                                         },
                                        {'shock_id': pdf_upload_ret['shock_id'],
                                         'name': intree_name + '.pdf',
                                         'label': intree_name + ' PDF'
                                         }])

        reportClient = KBaseReport(self.callbackURL, token=ctx['token'], service_ver=SERVICE_VER)
        report_info = reportClient.create_extended_report(reportObj)

        # Done
        #
        self.log(console, "BUILDING RETURN OBJECT")
        output = {'report_name': report_info['name'],
                  'report_ref': report_info['ref']
                  }

        self.log(console, "view_tree() DONE")
        #END view_tree

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method view_tree return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]

    def trim_speciestree_to_genomeset(self, ctx, params):
        """
        :param params: instance of type "trim_speciestree_to_genomeset_Input"
           (trim_speciestree_to_genomeset() ** ** reduce tree to match
           genomes found in genomeset) -> structure: parameter
           "workspace_name" of type "workspace_name" (** Common types),
           parameter "input_genomeSet_ref" of type "data_obj_ref", parameter
           "input_tree_ref" of type "data_obj_ref", parameter
           "output_tree_name" of type "data_obj_name", parameter "desc" of
           String, parameter "genome_disp_name_config" of String, parameter
           "show_skeleton_genome_sci_name" of type "bool", parameter
           "enforce_genome_version_match" of type "bool", parameter
           "reference_genome_disp" of mapping from type "data_obj_ref" to
           mapping from String to String, parameter "skeleton_genome_disp" of
           mapping from type "data_obj_ref" to mapping from String to String,
           parameter "user_genome_disp" of mapping from type "data_obj_ref"
           to mapping from String to String, parameter "user2_genome_disp" of
           mapping from type "data_obj_ref" to mapping from String to String,
           parameter "color_for_reference_genomes" of String, parameter
           "color_for_skeleton_genomes" of String, parameter
           "color_for_user_genomes" of String, parameter
           "color_for_user2_genomes" of String, parameter "tree_shape" of
           String
        :returns: instance of type "trim_speciestree_to_genomeset_Output" ->
           structure: parameter "report_name" of String, parameter
           "report_ref" of String
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN trim_speciestree_to_genomeset

        #### STEP 0: init
        ##
        dfu = DFUClient(self.callbackURL)
        console = []
        invalid_msgs = []
        self.log(console, 'Running trim_speciestree_to_genomeset() with params=')
        self.log(console, "\n" + pformat(params))
        report = ''
        timestamp = int((datetime.utcnow() - datetime.utcfromtimestamp(0)).total_seconds() * 1000)
        output_dir = os.path.join(self.scratch, 'output_' + str(timestamp))
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # ws obj info indices
        [OBJID_I, NAME_I, TYPE_I, SAVE_DATE_I, VERSION_I, SAVED_BY_I, WSID_I,
         WORKSPACE_I, CHSUM_I, SIZE_I, META_I] = range(11)  # object_info tuple

        #SERVICE_VER = 'dev'  # DEBUG
        SERVICE_VER = 'release'
        token = ctx['token']
        try:
            wsClient = workspaceService(self.workspaceURL, token=token)
        except:
            raise ValueError("unable to instantiate wsClient")


        #### STEP 1: do some basic checks
        ##
        required_params = ['workspace_name',
                           'input_tree_ref',
                           'input_genomeSet_ref',
                           'output_tree_name'
                           ]
        for arg in required_params:
            if arg not in params or params[arg] == None or params[arg] == '':
                raise ValueError("Must define required param: '" + arg + "'")


        #### STEP 2: load the method provenance from the context object
        ##
        self.log(console, "SETTING PROVENANCE")  # DEBUG
        provenance = [{}]
        if 'provenance' in ctx:
            provenance = ctx['provenance']
        # add additional info to provenance here, in this case the input data object reference
        provenance[0]['input_ws_objects'] = []
        provenance[0]['input_ws_objects'].append(params['input_tree_ref'])
        provenance[0]['input_ws_objects'].append(params['input_genomeSet_ref'])
        provenance[0]['service'] = 'kb_phylogenomics'
        provenance[0]['method'] = 'trim_speciestree_to_genomeset'


        #### STEP 3: Get tree object and store genome id and ref relationship
        ##
        try:
            objects = wsClient.get_objects([{'ref': params['input_tree_ref']}])
            data = objects[0]['data']
            info = objects[0]['info']
            intree_name = info[1]
            intree_type_name = info[2].split('.')[1].split('-')[0]

        except Exception as e:
            raise ValueError('Unable to fetch input_tree_ref object from workspace: ' + str(e))
            #to get the full stack trace: traceback.format_exc()

        if intree_type_name == 'Tree':
            tree_in = data
        else:
            raise ValueError('Cannot yet handle input_tree type of: ' + intree_type_name)

        genome_id_by_ref = dict()
        genome_ref_by_id = dict()
        for genome_id in tree_in['default_node_labels'].keys():
            genome_ref = tree_in['ws_refs'][genome_id]['g'][0]
            genome_id_by_ref[genome_ref] = genome_id
            genome_ref_by_id[genome_id] = genome_ref


        #### STEP 4: Get GenomeSet object
        #
        input_ref = params['input_genomeSet_ref']
        try:
            input_obj_info = wsClient.get_object_info_new({'objects': [{'ref': input_ref}]})[0]
            input_obj_name = input_obj_info[NAME_I]
            input_obj_type = re.sub('-[0-9]+\.[0-9]+$', "", input_obj_info[TYPE_I])  # remove trailing version
        except Exception as e:
            raise ValueError('Unable to get object from workspace: (' + input_ref + ')' + str(e))
        accepted_input_types = ["KBaseSearch.GenomeSet"]
        if input_obj_type not in accepted_input_types:
            raise ValueError("Input object of type '" + input_obj_type +
                             "' not accepted.  Must be one of " + ", ".join(accepted_input_types))
        input_genomeSet_name = input_obj_name


        # get set obj
        try:
            genomeSet_obj = wsClient.get_objects([{'ref': input_ref}])[0]['data']
        except:
            raise ValueError("unable to fetch genomeSet: " + input_ref)

        # get genome refs from GenomeSet and determine whether to wobble version
        #
        wobble_version = True
        retained_genome_refs = dict()
        retained_genome_refs_versionless = dict()
        for genome_id in genomeSet_obj['elements'].keys():
            genome_ref = genomeSet_obj['elements'][genome_id]['ref']
            (ws_id, obj_id, version) = genome_ref.split('/')
            genome_ref_versionless = str(ws_id)+'/'+str(obj_id)
            retained_genome_refs[genome_ref] = True
            retained_genome_refs_versionless[genome_ref_versionless] = True
        if params.get('enforce_genome_version_match') and int(params.get('enforce_genome_version_match')) == 1:
            wobble_version = False


        # STEP 5 - Prune tree if any leaf genomes not found in GenomeSet
        #
        newick_buf = tree_in['tree']
        self.log(console, "NEWICK_BUF: '" + newick_buf + "'")

        # init ETE3 objects
        species_tree = ete3.Tree(newick_buf)
        prune_retain_list = []  # prune() method takes list of leaves to keep
        prune_remove_list = []
        leaves_trimmed = False
        for n in species_tree.traverse():
            if n.is_leaf():
                genome_id = n.name
                genome_ref = genome_ref_by_id[genome_id]
                (ws_id, obj_id, version) = genome_ref.split('/')
                genome_ref_versionless = str(ws_id)+'/'+str(obj_id)
                if wobble_version and genome_ref_versionless in retained_genome_refs_versionless:
                    prune_retain_list.append(n.name)
                    self.log(console, "Retaining "+n.name) # DEBUG
                elif genome_ref in retained_genome_refs:
                    prune_retain_list.append(n.name)
                    self.log(console, "Retaining "+n.name) # DEBUG
                else:
                    prune_remove_list.append(n.name)

        if len(prune_retain_list) < 3:
            raise ValueError ("ABORT: less than 3 leaves left so output tree not meaningful")
        if len(prune_remove_list) > 0:
            leaves_trimmed = True
            self.log(console, "Pruning following genomes from SpeciesTree")
            for genome_id in prune_remove_list:
                self.log(console, "\t"+"Removing from SpeciesTree "+genome_id+" ref: "+genome_ref_by_id[genome_id])
            # prune() takes keep list, not remove list
            species_tree.prune (prune_retain_list)
        else:
            self.log(console, "No genomes found to remove from SpeciesTree")


        #### STEP 6: upload trimmed tree
        ##
        if leaves_trimmed:
            self.log(console,"UPLOADING RESULTS")  # DEBUG

            tree_name = params['output_tree_name']
            if params.get('desc'):
                tree_description = params['desc']
            else:
                if tree_in.get('desc'):
                    tree_description = tree_in['desc']+" TRIMMED "
                else:
                    tree_description = "Tree TRIMMED "
                for genome_id in prune_remove_list:
                    tree_description += " "+genome_id+"("+genome_ref_by_id[genome_id]+")"
            tree_type = 'SpeciesTree'
            species_tree.ladderize()
            output_newick_buf = species_tree.write()
            if not output_newick_buf.endswith(';'):
                output_newick_buf += ';'
            self.log(console,"\nNEWICK:\n"+output_newick_buf+"\n")

            # Extract info from input tree
            #
            tree_attributes = None
            default_node_labels = None
            ws_refs = None
            kb_refs = None
            leaf_list = None
            if 'default_node_labels' in tree_in:
                default_node_labels = dict()
                leaf_list = []
                for node_id in tree_in['default_node_labels'].keys():
                    genome_id = node_id
                    if genome_id in prune_retain_list:
                        default_node_labels[node_id] = tree_in['default_node_labels'][node_id]
                        leaf_list.append(node_id)
            if 'ws_refs' in tree_in.keys() and tree_in['ws_refs'] != None:
                ws_refs = dict()
                for node_id in tree_in['ws_refs'].keys():
                    genome_id = node_id
                    if genome_id in prune_retain_list:
                        ws_refs[node_id] = tree_in['ws_refs'][node_id]
            if 'kb_refs' in tree_in.keys() and tree_in['kb_refs'] != None:
                kb_refs = dict()
                for node_id in tree_in['kb_refs'].keys():
                    genome_id = node_id
                    if genome_id in prune_retain_list:
                        kb_refs[node_id] = tree_in['kb_refs'][node_id]

            # Build output_Tree structure
            #
            output_Tree = {
                      'name': tree_name,
                      'description': tree_description,
                      'type': tree_type,
                      'tree': output_newick_buf
                     }
            if tree_attributes != None:
                output_Tree['tree_attributes'] = tree_attributes
            if default_node_labels != None:
                output_Tree['default_node_labels'] = default_node_labels
            if ws_refs != None:
                output_Tree['ws_refs'] = ws_refs
            if kb_refs != None:
                output_Tree['kb_refs'] = kb_refs
            if leaf_list != None:
                output_Tree['leaf_list'] = leaf_list

            # Store output_Tree
            #
            try:
                tree_out_obj_info = wsClient.save_objects({
                    'workspace': params['workspace_name'],
                    'objects':[{
                        'type': 'KBaseTrees.Tree',
                        'data': output_Tree,
                        'name': params['output_tree_name'],
                        'meta': {},
                        'provenance': provenance
                    }]
                })[0]
            except Exception as e:
                raise ValueError('Unable to save tree '+params['output_tree_name']+' object to workspace '+str(params['workspace_name'])+': ' + str(e))
                #to get the full stack trace: traceback.format_exc()

            output_tree_ref = '/'.join([str(tree_out_obj_info[WSID_I]),
                                        str(tree_out_obj_info[OBJID_I]),
                                        str(tree_out_obj_info[VERSION_I])])


        #### STEP 7: call view_tree() to make report (if trimmed)
        ##
        report_info = dict()
        reportName = 'trim_speciestree_to_genomeset_report_' + str(uuid.uuid4())
        #report += output_newick_buf+"\n"
        reportObj = {'objects_created': [],
                     'direct_html_link_index': 0,
                     'file_links': [],
                     'html_links': [],
                     'workspace_name': params['workspace_name'],
                     'report_object_name': reportName
        }
        if not leaves_trimmed:
            # Create report obj
            report_text = "No genomes found in GenomeSet "+input_genomeSet_name+" to remove from SpeciesTree "+intree_name
            reportObj['text_message'] = report_text
        else:
            # RUN view_tree() and forward report object through
            view_tree_Params = {'workspace_name': params['workspace_name'],
                                'input_tree_ref': output_tree_ref,
                                'desc': tree_description,
                                'genome_disp_name_config': params['genome_disp_name_config'],
                                'show_skeleton_genome_sci_name': params['show_skeleton_genome_sci_name'],
                                'reference_genome_disp':    params['reference_genome_disp'],
                                'skeleton_genome_disp':     params['skeleton_genome_disp'],
                                'user_genome_disp':         params['user_genome_disp'],
                                'user2_genome_disp':        params['user2_genome_disp'],
                                'color_for_reference_genomes':  params['color_for_reference_genomes'],
                                'color_for_skeleton_genomes':   params['color_for_skeleton_genomes'],
                                'color_for_user_genomes':       params['color_for_user_genomes'],
                                'color_for_user2_genomes':      params['color_for_user2_genomes'],
                                'tree_shape':                   params['tree_shape']

                            }
            self.log(console, "RUNNING view_tree() for tree: " + output_tree_ref)
            view_tree_retVal = self.view_tree(ctx, view_tree_Params)[0]

            # can't just pass forward report because we created objects we need to add
            try:
                view_tree_reportObj = wsClient.get_objects([{'ref': view_tree_retVal['report_ref']}])[0]['data']
            except Exception as e:
                raise ValueError('Unable to fetch view_tree() report from workspace: ' + str(e))
                #to get the full stack trace: traceback.format_exc()

            # can't just copy substructures because format of those fields in report object different from the format needed to pass to create_extended_report() method
            #for field in ('direct_html_link_index', 'file_links', 'html_links'):
            #    reportObj[field] = view_tree_reportObj[field]
            #    self.log<(console, "REPORT "+field+": "+pformat(view_tree_reportObj[field]))  # DEBUG
            #
            reportObj['direct_html_link_index'] = view_tree_reportObj['direct_html_link_index']
            for html_link_item in view_tree_reportObj['html_links']:
                #this_shock_id = html_link_item['URL']
                this_shock_id = re.sub('^.*/', '', html_link_item['URL'])
                new_html_link_item = {'shock_id': this_shock_id,
                                      'name': html_link_item['name'],
                                      'label': html_link_item['label']
                                    }
                reportObj['html_links'].append(new_html_link_item)
            for file_link_item in view_tree_reportObj['file_links']:
                #this_shock_id = file_link_item['URL']
                this_shock_id = re.sub('^.*/', '', file_link_item['URL'])
                new_file_link_item = {'shock_id': this_shock_id,
                                      'name': file_link_item['name'],
                                      'label': file_link_item['label']
                                    }
                reportObj['file_links'].append(new_file_link_item)

            reportObj['objects_created'].append({'ref': output_tree_ref,
                                                 'description': params['output_tree_name']+' Trimmed Tree'})


        # save report object
        reportClient = KBaseReport(self.callbackURL, token=ctx['token'], service_ver=SERVICE_VER)
        report_info = reportClient.create_extended_report(reportObj)


        # Done
        #
        self.log(console, "BUILDING RETURN OBJECT")
        output = {'report_name': report_info['name'],
                  'report_ref': report_info['ref']
                  }

        self.log(console, "trim_speciestree_to_genomeset() DONE")
        #END trim_speciestree_to_genomeset

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method trim_speciestree_to_genomeset return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]

    def build_microbial_speciestree(self, ctx, params):
        """
        :param params: instance of type "build_microbial_speciestree_Input"
           (build_microbial_speciestree() ** ** run Insert Set of Genomes
           into Species Tree with extra features) -> structure: parameter
           "workspace_name" of type "workspace_name" (** Common types),
           parameter "input_genome_refs" of type "data_obj_ref", parameter
           "output_tree_name" of type "data_obj_name", parameter "desc" of
           String, parameter "genome_disp_name_config" of String, parameter
           "show_skeleton_genome_sci_name" of type "bool", parameter
           "skeleton_set" of String, parameter "num_proximal_sisters" of
           Long, parameter "proximal_sisters_ANI_spacing" of Double,
           parameter "color_for_reference_genomes" of String, parameter
           "color_for_skeleton_genomes" of String, parameter
           "color_for_user_genomes" of String, parameter
           "color_for_user2_genomes" of String, parameter "tree_shape" of
           String
        :returns: instance of type "build_microbial_speciestree_Output" ->
           structure: parameter "report_name" of String, parameter
           "report_ref" of String
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN build_microbial_speciestree

        #### STEP 0: init
        ##
        dfu = DFUClient(self.callbackURL)
        console = []
        invalid_msgs = []
        self.log(console, 'Running build_microbial_speciestree() with params=')
        self.log(console, "\n" + pformat(params))
        report = ''
        timestamp = int((datetime.utcnow() - datetime.utcfromtimestamp(0)).total_seconds() * 1000)
        output_dir = os.path.join(self.scratch, 'output_' + str(timestamp))
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # ws obj info indices
        [OBJID_I, NAME_I, TYPE_I, SAVE_DATE_I, VERSION_I, SAVED_BY_I, WSID_I,
         WORKSPACE_I, CHSUM_I, SIZE_I, META_I] = range(11)  # object_info tuple

        #SERVICE_VER = 'dev'  # DEBUG
        SERVICE_VER = 'release'
        token = ctx['token']
        try:
            wsClient = workspaceService(self.workspaceURL, token=token)
        except:
            raise ValueError("unable to instantiate wsClient")


        #### STEP 1: Configure Skeleton Genome info
        ##
        skeleton_file = 'Phylogenetic_Skeleton.tsv'
        config_dir = os.path.join (os.path.sep, 'kb', 'module', 'data', 'skeleton_genomes')
        skeleton_path = os.path.join (config_dir, skeleton_file)
        skeleton_genome_config = dict()
        headers = []
        with open (skeleton_path, 'r') as skeleton_handle:
            for skeleton_line in skeleton_handle.readlines():
                skeleton_line = skeleton_line.rstrip()
                skeleton_row = skeleton_line.split("\t")
                if skeleton_row[0] == 'KBase Phylo Ref':
                    headers = skeleton_row
                elif skeleton_row[0] != None and skeleton_row[0] != '':
                    genome_ref = skeleton_row[0]
                    skeleton_genome_config[genome_ref] = dict()
                    for col_i,datum in enumerate(skeleton_row):
                        skeleton_genome_config[genome_ref][headers[col_i]] = datum
                        # DEBUG
                        self.log(console, "Skeleton Genome DB info: "+genome_ref+" "+headers[col_i]+": "+datum)


        #### STEP 2: do some basic checks
        ##
        required_params = ['workspace_name',
                           'input_genome_refs',
                           'skeleton_set',
                           'output_tree_name'
                           ]
        for arg in required_params:
            if arg not in params or params[arg] == None or params[arg] == '':
                raise ValueError("Must define required param: '" + arg + "'")


        #### STEP 3: load the method provenance from the context object
        ##
        self.log(console, "SETTING PROVENANCE")  # DEBUG
        provenance = [{}]
        if 'provenance' in ctx:
            provenance = ctx['provenance']
        # add additional info to provenance here, in this case the input data object reference
        provenance[0]['input_ws_objects'] = []
        provenance[0]['input_ws_objects'].extend(params['input_genome_refs'])
        provenance[0]['service'] = 'kb_phylogenomics'
        provenance[0]['method'] = 'build_microbial_speciestree'


        #### STEP 4: Get Query Genomes
        ##
        query_genome_ref_order = []
        query_genome_disp = dict()
        genomeSet_obj_types = ["KBaseSearch.GenomeSet", "KBaseSets.GenomeSet"]
        genome_obj_types    = ["KBaseGenomes.Genome", "KBaseGenomeAnnotations.Genome"]
        tree_obj_types      = ["KBaseTrees.Tree"]
        for input_ref in params['input_genome_refs']:
            try:
                query_genome_obj = wsClient.get_objects2({'objects':[{'ref': input_ref}]})['data'][0]
                query_genome_obj_data = query_genome_obj['data']
                query_genome_obj_info = query_genome_obj['info']
                query_genome_obj_type = query_genome_obj_info[TYPE_I].split('-')[0]
            except:
                raise ValueError("unable to fetch input genome object: " + input_ref)

            # just a genome
            if query_genome_obj_type in genome_obj_types:
                if input_ref not in query_genome_disp:
                    query_genome_disp[input_ref] = dict()
                    query_genome_disp[input_ref]['color'] = 'default'
                    query_genome_ref_order.append(input_ref)

            # handle genomeSet
            elif query_genome_obj_type in genomeSet_obj_types:
                for genome_id in sorted(query_genome_obj_data['elements'].keys()):
                    genome_ref = query_genome_obj_data['elements'][genome_id]['ref']
                    if genome_ref not in query_genome_disp:
                        query_genome_disp[genome_ref] = dict()
                        query_genome_disp[genome_ref]['color'] = 'default'
                        query_genome_ref_order.append(genome_ref)

            # handle tree type
            elif query_genome_obj_type in tree_obj_types:
                for genome_id in sorted(query_genome_obj_data['ws_refs'].keys()):
                    genome_ref = query_genome_obj_data['ws_refs'][genome_id]['g'][0]
                    if genome_ref not in query_genome_disp:
                        query_genome_disp[genome_ref] = dict()
                        query_genome_disp[genome_ref]['color'] = 'default'
                        query_genome_ref_order.append(genome_ref)
            else:
                raise ValueError ("bad type for input_genome_refs")


        #### STEP 4.b: Get Additional User Genomes
        ##
        query2_genome_ref_order = []
        query2_genome_disp = dict()
        genomeSet_obj_types = ["KBaseSearch.GenomeSet", "KBaseSets.GenomeSet"]
        genome_obj_types    = ["KBaseGenomes.Genome", "KBaseGenomeAnnotations.Genome"]
        tree_obj_types      = ["KBaseTrees.Tree"]
        for input_ref in params['input_genome2_refs']:
            try:
                query_genome_obj = wsClient.get_objects2({'objects':[{'ref': input_ref}]})['data'][0]
                query_genome_obj_data = query_genome_obj['data']
                query_genome_obj_info = query_genome_obj['info']
                query_genome_obj_type = query_genome_obj_info[TYPE_I].split('-')[0]
            except:
                raise ValueError("unable to fetch input genome object: " + input_ref)

            # just a genome
            if query_genome_obj_type in genome_obj_types:
                if input_ref not in query2_genome_disp:
                    query2_genome_disp[input_ref] = dict()
                    query2_genome_disp[input_ref]['color'] = 'default'
                    query2_genome_ref_order.append(input_ref)

            # handle genomeSet
            elif query_genome_obj_type in genomeSet_obj_types:
                for genome_id in sorted(query_genome_obj_data['elements'].keys()):
                    genome_ref = query_genome_obj_data['elements'][genome_id]['ref']
                    if genome_ref not in query2_genome_disp:
                        query2_genome_disp[genome_ref] = dict()
                        query2_genome_disp[genome_ref]['color'] = 'default'
                        query2_genome_ref_order.append(genome_ref)

            # handle tree type
            elif query_genome_obj_type in tree_obj_types:
                for genome_id in sorted(query_genome_obj_data['ws_refs'].keys()):
                    genome_ref = query_genome_obj_data['ws_refs'][genome_id]['g'][0]
                    if genome_ref not in query2_genome_disp:
                        query2_genome_disp[genome_ref] = dict()
                        query2_genome_disp[genome_ref]['color'] = 'default'
                        query2_genome_ref_order.append(genome_ref)
            else:
                raise ValueError ("bad type for input_genome2_refs")


        #### STEP 5: Get proximal sisters for user genomes
        ##
        reference_genome_ref_order = []
        reference_genome_disp = dict()


        #### STEP 6: Get Skeleton genomes
        ##
        skeleton_genome_ref_order = []
        skeleton_genome_disp = dict()
        if params.get('skeleton_set'):
            #skeleton_ws_id = 45087;  # CI
            skeleton_ws_id = 50737;  # PROD
            skeleton_genomeSet_obj_name = 'Phylogenetic_Skeleton-'+params['skeleton_set']+".GenomeSet"

            # get set obj
            try:
                skeleton_genomeSet_obj = wsClient.get_objects2({'objects':[{'wsid': skeleton_ws_id,'name':skeleton_genomeSet_obj_name}]})['data'][0]
            except:
                raise ValueError("unable to fetch skeleton genomeSet: " + skeleton_genomeSet_obj_name + " from ws "+str(skeleton_ws_id))
            skeleton_genomeSet_obj_data = skeleton_genomeSet_obj['data']

            for genome_id in skeleton_genomeSet_obj_data['elements'].keys():
                genome_ref = skeleton_genomeSet_obj_data['elements'][genome_id]['ref']
                skeleton_genome_disp[genome_ref] = dict()
                skeleton_genome_disp[genome_ref]['color'] = 'default'
                skeleton_genome_ref_order.append(genome_ref)

                # add skeleton genome extra disp info
                lineage_info = []
                lineage_info.append(skeleton_genome_config[genome_ref]['Phylum'])
                if skeleton_genome_config[genome_ref].get('Class'):
                    lineage_info.append(skeleton_genome_config[genome_ref]['Class'])
                if skeleton_genome_config[genome_ref].get('Order'):
                    lineage_info.append(skeleton_genome_config[genome_ref]['Order'])
                skeleton_genome_disp[genome_ref]['label'] = "["+" > ".join(lineage_info)+"]"
                if params.get('show_skeleton_genome_sci_name'):
                    skeleton_genome_disp[genome_ref]['label'] += " "+skeleton_genome_config[genome_ref]['Species Name']
                    skeleton_genome_disp[genome_ref]['label'] += " ["+skeleton_genome_config[genome_ref]['Isolate / MAG / SAG']+"]"


        #### STEP 7: merge genome sets
        ##
        combined_genome_ref_order = []
        for genome_ref in query_genome_ref_order:
            combined_genome_ref_order.append(genome_ref)
        for genome_ref in query2_genome_ref_order:
            combined_genome_ref_order.append(genome_ref)
        for genome_ref in skeleton_genome_ref_order:
            combined_genome_ref_order.append(genome_ref)
        for genome_ref in reference_genome_ref_order:
            combined_genome_ref_order.append(genome_ref)
        if len(skeleton_genome_ref_order) > 0:
            provenance[0]['input_ws_objects'].extend(skeleton_genome_ref_order)
        if len(reference_genome_ref_order) > 0:
            provenance[0]['input_ws_objects'].extend(reference_genome_ref_order)

        # DEBUG
        #self.log (console, "GENOME REFS: "+"\t".join(combined_genome_ref_order))


        #### STEP 8: prep for untrimmed tree and tree GenomeSet
        ##
        trimmed_tree_name = params['output_tree_name']
        untrimmed_tree_name = trimmed_tree_name+'-UNTRIMMED'
        trimmed_genomeSet_name = trimmed_tree_name+'.GenomeSet'
        untrimmed_genomeSet_name = untrimmed_tree_name+'.GenomeSet'
        trimmedGS = {
            'description': 'trimmed species tree genomes',
            'elements': dict()
        }
        for genome_i,genome_ref in enumerate(combined_genome_ref_order):
            trimmedGS['elements'][str(genome_i)] = { 'ref': genome_ref }

        # save trimmed genomeset
        gs_obj_info = wsClient.save_objects({'workspace': params['workspace_name'],
                                             'objects': [
                                                 {
                                                     'type':'KBaseSearch.GenomeSet',
                                                     'data':trimmedGS,
                                                     'name':trimmed_genomeSet_name,
                                                     'meta':{},
                                                     'provenance':[
                                                         {
                                                             'service':'kb_phylogenomics',
                                                             'method':'build_microbial_speciestree'
                                                         }
                                                     ]
                                                 }]})[0]
        #pprint(gs_obj_info)
        trimmed_genomeSet_ref = '/'.join([str(gs_obj_info[WSID_I]),
                                          str(gs_obj_info[OBJID_I]),
                                          str(gs_obj_info[VERSION_I])])

        # save untrimmed genomeset (really just a target for SpeciesTreeBuilder)
        gs_obj_info = wsClient.save_objects({'workspace': params['workspace_name'],
                                             'objects': [
                                                 {
                                                     'type':'KBaseSearch.GenomeSet',
                                                     'data':trimmedGS,
                                                     'name':untrimmed_genomeSet_name,
                                                     'meta':{},
                                                     'provenance':[
                                                         {
                                                             'service':'kb_phylogenomics',
                                                             'method':'build_microbial_speciestree'
                                                         }
                                                     ]
                                                 }]})[0]
        #pprint(gs_obj_info)
        untrimmed_genomeSet_ref = '/'.join([params['workspace_name'],
                                            untrimmed_genomeSet_name])
                                            #str(gs_obj_info[OBJID_I])])
                                            #str(gs_obj_info[VERSION_I])])


        #### STEP 9: call species tree app and get back created object
        ##
        #"SpeciesTreeBuilder/insert_genomeset_into_species_tree"
        nearest_genome_count = 1
        if len(combined_genome_ref_order) < 3:
            nearest_genome_count = 3 - len(combined_genome_ref_order)
        species_tree_app_params = {
            "out_workspace": params['workspace_name'],
            "new_genomes": combined_genome_ref_order,
            #"new_genomes": query_genome_ref_order,
            "nearest_genome_count": nearest_genome_count,
            "copy_genomes": 0,
            "out_tree_id": untrimmed_tree_name,
            # out_genomeset_ref format must be "workspace_name/obj_name"
            "out_genomeset_ref": untrimmed_genomeSet_ref,
            "use_ribosomal_s9_only": 0
        }
        # DEBUG
        self.log(console, "SPECIES_TREE_PARAMS: ")
        self.log(console, str(species_tree_app_params))

        try:
            #SERVICE_VER = 'dev'  # DEBUG
            SERVICE_VER = 'release'
            speciesTreeClient = SpeciesTreeBuilder(url=self.callbackURL, token=ctx['token'], service_ver=SERVICE_VER)  # SDK Local
            #speciesTreeClient = SpeciesTreeBuilder(url=self.serviceWizardURL, token=ctx['token'], service_ver=SERVICE_VER)  # Dynamic service
        except:
            raise ValueError("unable to instantiate SpeciesTreeBuilder Client")
        # run
        #speciesTree_retVal = speciesTreeClient.construct_species_tree(species_tree_app_params)[0]
        speciesTree_retVal = speciesTreeClient.construct_species_tree(species_tree_app_params)
        untrimmed_speciesTree_obj = wsClient.get_objects2({'objects':[{'workspace':params['workspace_name'],'name':untrimmed_tree_name}]})['data'][0]
        untrimmed_speciesTree_obj_info = untrimmed_speciesTree_obj['info']
        untrimmed_speciesTree_obj_data = untrimmed_speciesTree_obj['data']

        untrimmed_speciesTree_obj_ref = '/'.join([str(untrimmed_speciesTree_obj_info[WSID_I]),
                                                  str(untrimmed_speciesTree_obj_info[OBJID_I]),
                                                  str(untrimmed_speciesTree_obj_info[VERSION_I])])


        #### STEP 10: call trim_speciestree_to_genomeset() to make report
        ##
        report_info = dict()
        reportName = 'build_microbial_speciestree_report_' + str(uuid.uuid4())
        #report += output_newick_buf+"\n"
        reportObj = {'objects_created': [],
                     'direct_html_link_index': 0,
                     'file_links': [],
                     'html_links': [],
                     'workspace_name': params['workspace_name'],
                     'report_object_name': reportName
        }
        # RUN trim_speciestree_to_genomeset() and forward report object through
        trim_tree_Params = {'workspace_name':          params['workspace_name'],
                            'input_genomeSet_ref':     trimmed_genomeSet_ref,
                            'input_tree_ref':          untrimmed_speciesTree_obj_ref,
                            'output_tree_name':        params['output_tree_name'],
                            'desc':                    params['desc'],
                            'genome_disp_name_config': params['genome_disp_name_config'],
                            'show_skeleton_genome_sci_name': params['show_skeleton_genome_sci_name'],
                            'enforce_genome_version_match': 1,
                            'reference_genome_disp':        reference_genome_disp,
                            'skeleton_genome_disp':         skeleton_genome_disp,
                            'user_genome_disp':             query_genome_disp,
                            'user2_genome_disp':            query2_genome_disp,
                            'color_for_reference_genomes':  params['color_for_reference_genomes'],
                            'color_for_skeleton_genomes':   params['color_for_skeleton_genomes'],
                            'color_for_user_genomes':       params['color_for_user_genomes'],
                            'color_for_user2_genomes':      params['color_for_user2_genomes'],
                            'tree_shape':                   params['tree_shape']
        }
        self.log(console, "RUNNING trim_speciestree_to_genomeset() for tree: " + untrimmed_tree_name+" genomeSet: "+trimmed_genomeSet_name)
        trim_tree_retVal = self.trim_speciestree_to_genomeset(ctx, trim_tree_Params)[0]

        # can't just pass forward report because we created objects we need to add
        try:
            trim_tree_reportObj = wsClient.get_objects([{'ref': trim_tree_retVal['report_ref']}])[0]['data']
        except Exception as e:
            raise ValueError('Unable to fetch trim_speciestree_to_genomeset() report from workspace: ' + str(e))
            #to get the full stack trace: traceback.format_exc()

        # can't just copy substructures because format of those fields in report object different from the format needed to pass to create_extended_report() method
        #for field in ('direct_html_link_index', 'file_links', 'html_links'):
        #    reportObj[field] = view_tree_reportObj[field]
        #    self.log<(console, "REPORT "+field+": "+pformat(view_tree_reportObj[field]))  # DEBUG
        #
        reportObj['direct_html_link_index'] = trim_tree_reportObj['direct_html_link_index']
        for html_link_item in trim_tree_reportObj['html_links']:
            #this_shock_id = html_link_item['URL']
            this_shock_id = re.sub('^.*/', '', html_link_item['URL'])
            new_html_link_item = {'shock_id': this_shock_id,
                                  'name': html_link_item['name'],
                                  'label': html_link_item['label']
            }
            reportObj['html_links'].append(new_html_link_item)
        for file_link_item in trim_tree_reportObj['file_links']:
            #this_shock_id = file_link_item['URL']
            this_shock_id = re.sub('^.*/', '', file_link_item['URL'])
            new_file_link_item = {'shock_id': this_shock_id,
                                  'name': file_link_item['name'],
                                  'label': file_link_item['label']
            }
            reportObj['file_links'].append(new_file_link_item)

        reportObj['objects_created'].append({'ref': trim_tree_reportObj['objects_created'][0]['ref'],
                                             'description': params['desc']})

        reportClient = KBaseReport(self.callbackURL, token=ctx['token'], service_ver=SERVICE_VER)
        report_info = reportClient.create_extended_report(reportObj)


        # Done
        #
        self.log(console, "BUILDING RETURN OBJECT")
        output = {'report_name': report_info['name'],
                  'report_ref': report_info['ref']
                  }

        self.log(console, "build_microbial_speciestree() DONE")
        #END build_microbial_speciestree

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method build_microbial_speciestree return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]

    def localize_DomainAnnotations(self, ctx, params):
        """
        :param params: instance of type "localize_DomainAnnotations_Input"
           (localize_DomainAnnotations() ** ** point all DomainAnnotations at
           local copies of Genome Objects) -> structure: parameter
           "workspace_name" of type "workspace_name" (** Common types),
           parameter "input_DomainAnnotation_refs" of type "data_obj_ref"
        :returns: instance of type "localize_DomainAnnotations_Output" ->
           structure: parameter "report_name" of String, parameter
           "report_ref" of String
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN localize_DomainAnnotations
        console = []
        self.log(console, 'Running localize_DomainAnnotations() with params=')
        self.log(console, "\n" + pformat(params))

        # ws obj info indices
        [OBJID_I, NAME_I, TYPE_I, SAVE_DATE_I, VERSION_I, SAVED_BY_I, WSID_I,
         WORKSPACE_I, CHSUM_I, SIZE_I, META_I] = range(11)  # object_info tuple

        #SERVICE_VER = 'dev'  # DEBUG
        SERVICE_VER = 'release'
        token = ctx['token']
        try:
            wsClient = workspaceService(self.workspaceURL, token=token)
        except:
            raise ValueError("unable to instantiate wsClient")
        try:
            dfuClient = DFUClient(self.callbackURL)
        except:
            raise ValueError("unable to instantiate dfuClient")
        headers = {'Authorization': 'OAuth ' + token}
        env = os.environ.copy()
        env['KB_AUTH_TOKEN'] = token


        ### STEP 1: basic parameter checks + parsing
        required_params = ['workspace_name']
        for arg in required_params:
            if arg not in params or params[arg] == None or params[arg] == '':
                raise ValueError("Must define required param: '" + arg + "'")


        ### STEP 2: read the local genomes names and refs
        local_genome_name_by_ref = dict()
        local_genome_ref_by_name = dict()
        local_genome_obj_info_list = []
        try:
            local_genome_obj_info_list.extend(wsClient.list_objects(
                {'workspaces': [params['workspace_name']], 'type': "KBaseGenomes.Genome"}))
        except Exception as e:
            raise ValueError("Unable to list Genome objects from workspace: " + str(workspace_name) + " " + str(e))

        for info in local_genome_obj_info_list:
            local_genome_ref = str(info[WSID_I]) + '/' + str(info[OBJID_I]) + '/' + str(info[VERSION_I])
            local_genome_name = info[NAME_I]
            local_genome_name_by_ref[local_genome_ref]  = local_genome_name
            local_genome_ref_by_name[local_genome_name] = local_genome_ref


        ### STEP 3: Read local DomainAnnotation objects, find remote genome name, replace with local ref, and save DomainAnnotation
        report_text = []
        objects_created = []
        local_DomainAnnotation_refs = []
        WsID = None
        if params.get('input_DomainAnnotation_refs'):
            local_DomainAnnotation_refs = params['input_DomainAnnotation_refs']
        else:
            dom_annot_obj_info_list = []
            # read local workspace first
            try:
                dom_annot_obj_info_list.extend(wsClient.list_objects(
                    {'workspaces': [params['workspace_name']], 'type': "KBaseGeneFamilies.DomainAnnotation"}))
            except Exception as e:
                raise ValueError("Unable to list DomainAnnotation objects from workspace: " + str(workspace_name) + " " + str(e))

            for info in dom_annot_obj_info_list:
                WsID = info[WSID_I]
                dom_annot_ref = str(info[WSID_I]) + '/' + str(info[OBJID_I]) + '/' + str(info[VERSION_I])
                local_DomainAnnotation_refs.append(dom_annot_ref)

        # go through each DomainAnnotation object and replace the genome_ref
        for dom_annot_ref in local_DomainAnnotation_refs:
            try:
                domain_obj = wsClient.get_objects([{'ref': dom_annot_ref}])[0]
            except:
                raise ValueError("unable to fetch domain annotation: " + dom_annot_ref)
            domain_data = domain_obj['data']
            domain_info = domain_obj['info']
            domain_obj_name = domain_info[NAME_I]

            # read remote genome ref from domain data object
            remote_genome_ref = domain_data['genome_ref']
            remote_genome_obj_info = wsClient.get_object_info_new({'objects': [{'ref': remote_genome_ref}]})[0]
            remote_genome_name = remote_genome_obj_info[NAME_I]

            # we already got one
            if local_genome_ref_by_name.get(remote_genome_name) \
               and local_genome_ref_by_name[remote_genome_name] == remote_genome_ref:
                msg = "Local Genome Object of name "+remote_genome_name+" is already pointed to by DomainAnnotation "+domain_obj_name+"."
                msg += "\n"
                self.log(console, msg)
                report_text.append(msg)
                continue

            # let's get one
            elif not local_genome_ref_by_name.get(remote_genome_name):
                msg = "No local Genome Object of name "+remote_genome_name+" found for DomainAnnotation "+domain_obj_name+".  Making local copy,"
                msg += "\n"
                self.log(console, msg)
                report_text.append(msg)

                # get Genome obj, copy Assembly obj, set assembly pointer in Genome, and save
                try:
                    genome_obj_data = wsClient.get_objects([{'ref':remote_genome_ref}])[0]['data']
                except:
                    raise ValueError("unable to fetch genome: " + remote_genome_ref)

# HERE
                genome_assembly_type = None
                if not genome_obj_data.get('contig_set_ref') and not genome_obj_data.get('assembly_ref'):
                    msg = "Genome " + remote_genome_name + \
                          " (ref:" + remote_genome_ref + ") " + \
                          " MISSING BOTH contigset_ref AND assembly_ref.  Cannot process.  Exiting."
                    self.log(console, msg)
                    #self.log(invalid_msgs, msg)
                    #continue
                    raise ValueError(msg)
                elif genome_obj_data.get('assembly_ref'):
                    msg = "Genome " + remote_genome_name + \
                          " (ref:" + remote_genome_ref + ") " + \
                          " USING assembly_ref: " + str(genome_obj_data['assembly_ref'])
                    self.log(console, msg)
                    genome_assembly_ref = genome_obj_data['assembly_ref']
                    genome_assembly_type = 'assembly'
                elif genome_obj_data.get('contigset_ref'):
                    msg = "Genome " + remote_genome_name + \
                          " (ref:" + remote_genome_ref + ") " + \
                          " USING contigset_ref: " + str(genome_obj_data['contigset_ref'])
                    self.log(console, msg)
                    genome_assembly_ref = genome_obj_data['contigset_ref']
                    genome_assembly_type = 'contigset'

                try:
                    ass_obj = wsClient.get_objects([{'ref': genome_assembly_ref}])[0]
                    ass_data = ass_obj['data']
                    ass_info = ass_obj['info']
                    ass_name = ass_info[NAME_I]
                except:
                    raise ValueError("unable to fetch assembly: " + genome_assembly_ref)

                # save assembly to local workspace
                provenance = [{}]
                if 'provenance' in ctx:
                    provenance = ctx['provenance']
                provenance[0]['input_ws_objects'] = [str(genome_assembly_ref)]

                ass_obj_type = "KBaseGenomeAnnotations.Assembly"
                if genome_assembly_type == 'contigset':
                    ass_obj_type = "KBaseGenomes.ContigSet"
                #new_obj_info = wsClient.save_objects({
                #    'workspace': params['workspace_name'],
                new_obj_info = dfuClient.save_objects({
                    'id': WsID,
                    'objects': [
                        {'type': ass_obj_type,
                         'data': ass_data,
                         'name': ass_name
                         #'meta': {},
                         #'provenance': provenance
                     }]
                })[0]
                local_assembly_ref = '{}/{}/{}'.format(new_obj_info[WSID_I],
                                                       new_obj_info[OBJID_I],
                                                       new_obj_info[VERSION_I])
                #objects_created.append(
                #    {'ref': local_assembly_ref, 'description': 'localized Assembly for '+remote_genome_name})

                # reset ref for assembly in Genome obj
                if genome_assembly_type == 'assembly':
                    genome_obj_data['assembly_ref'] = local_assembly_ref
                else:  # contigset obj
                    genome_obj_data['contig_set_ref'] = local_assembly_ref

                # save genome to local workspace
                provenance = [{}]
                if 'provenance' in ctx:
                    provenance = ctx['provenance']
                provenance[0]['input_ws_objects'] = [str(remote_genome_ref)]

                genome_obj_type = "KBaseGenomes.Genome"
                #new_obj_info = wsClient.save_objects({
                #    'workspace': params['workspace_name'],
                new_obj_info = dfuClient.save_objects({
                    'id': WsID,
                    'objects': [
                        {'type': genome_obj_type,
                         'data': genome_obj_data,
                         'name': remote_genome_name
                         #'meta': {},
                         #'provenance': provenance
                     }]
                })[0]
                local_genome_ref = '{}/{}/{}'.format(new_obj_info[WSID_I],
                                                     new_obj_info[OBJID_I],
                                                     new_obj_info[VERSION_I])
                #objects_created.append(
                #    {'ref': local_genome_ref, 'description': 'localized Genome for '+remote_genome_name})
                local_genome_ref_by_name[remote_genome_name] = local_genome_ref


            # change genome ref to local copy
            local_genome_ref = local_genome_ref_by_name[remote_genome_name]
            domain_data['genome_ref'] = local_genome_ref
            msg = "Setting DomainAnnotation object "+domain_obj_name+" to local copy of Genome "+remote_genome_name+" with local ref "+local_genome_ref
            msg += "\n"
            self.log(console, msg)
            report_text.append(msg)

            # save DomainAnnotation object
            provenance = [{}]
            if 'provenance' in ctx:
                provenance = ctx['provenance']
            provenance[0]['input_ws_objects'] = [str(remote_genome_ref), str(local_genome_ref)]

            #new_obj_info = wsClient.save_objects({
            #    'workspace': params['workspace_name'],
            new_obj_info = dfuClient.save_objects({
                'id': WsID,
                'objects': [
                    {'type': 'KBaseGeneFamilies.DomainAnnotation',
                     'data': domain_data,
                     'name': domain_obj_name
                     #'meta': {},
                     #'provenance': provenance
                 }]
            })[0]
            objects_created.append(
                {'ref': str(new_obj_info[WSID_I]) + '/' + str(new_obj_info[OBJID_I]) + '/' + str(new_obj_info[VERSION_I]), 'description': 'localized DomainAnnotation for '+remote_genome_name})


        ### STEP 4: build and save the report
        reportObj = {
            'objects_created': objects_created,
            'text_message': "\n".join(report_text)
        }
        SERVICE_VER = 'release'
        reportClient = KBaseReport(self.callbackURL, token=ctx['token'], service_ver=SERVICE_VER)
        report_info = reportClient.create({'report': reportObj, 'workspace_name': params['workspace_name']})

        ### STEP 6: construct the output to send back
        output = {'report_name': report_info['name'], 'report_ref': report_info['ref']}

        #END localize_DomainAnnotations

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method localize_DomainAnnotations return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]

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
        self.log(console, "\n" + pformat(params))

        # ws obj info indices
        [OBJID_I, NAME_I, TYPE_I, SAVE_DATE_I, VERSION_I, SAVED_BY_I, WSID_I,
         WORKSPACE_I, CHSUM_I, SIZE_I, META_I] = range(11)  # object_info tuple

        #SERVICE_VER = 'dev'  # DEBUG
        SERVICE_VER = 'release'
        token = ctx['token']
        try:
            wsClient = workspaceService(self.workspaceURL, token=token)
        except:
            raise ValueError("unable to instantiate wsClient")
        headers = {'Authorization': 'OAuth ' + token}
        env = os.environ.copy()
        env['KB_AUTH_TOKEN'] = token


        ### STEP 1: basic parameter checks + parsing
        required_params = ['workspace_name',
                           'input_genomeSet_ref'
                           ]
        for arg in required_params:
            if arg not in params or params[arg] == None or params[arg] == '':
                raise ValueError("Must define required param: '" + arg + "'")

        ### STEP 2: build a list of genomes to iterate through

        # get input obj
        genomeSet_types =  ["KBaseSearch.GenomeSet","KBaseSets.GenomeSet"]
        tree_types = ["KBaseTrees.Tree"]
        input_ref = params['input_genomeSet_ref']
        try:
            input_obj_info = wsClient.get_object_info_new({'objects': [{'ref': input_ref}]})[0]
            input_obj_type = re.sub('-[0-9]+\.[0-9]+$', "", input_obj_info[TYPE_I])  # remove trailing version
        except Exception as e:
            raise ValueError('Unable to get object from workspace: (' + input_ref + ')' + str(e))
        accepted_input_types = genomeSet_types + tree_types
        if input_obj_type not in accepted_input_types:
            raise ValueError("Input object of type '" + input_obj_type +
                             "' not accepted.  Must be one of " + ", ".join(accepted_input_types))

        # get list of genomes
        genome_refs = []
        if input_obj_type in genomeSet_types:
            # get set obj
            try:
                genomeSet_obj = wsClient.get_objects([{'ref': input_ref}])[0]['data']
            except:
                raise ValueError("unable to fetch genomeSet: " + input_ref)

            # get genome refs and object names
            genome_ids = genomeSet_obj['elements'].keys()  # note: genome_id may be meaningless
            for genome_id in genome_ids:
                genome_refs.append(genomeSet_obj['elements'][genome_id]['ref'])

        elif input_obj_type in tree_types:

            # get speciesTree
            #
            input_ref = params['input_genomeSet_ref']
            speciesTree_name = None
            try:
                input_obj_info = wsClient.get_object_info_new({'objects': [{'ref': input_ref}]})[0]
                input_obj_name = input_obj_info[NAME_I]
                input_obj_type = re.sub('-[0-9]+\.[0-9]+$', "", input_obj_info[TYPE_I])  # remove trailing version
                speciesTree_name = input_obj_info[NAME_I]
            except Exception as e:
                raise ValueError('Unable to get object from workspace: (' + input_ref + ')' + str(e))
            accepted_input_types = ["KBaseTrees.Tree"]
            if input_obj_type not in accepted_input_types:
                raise ValueError("Input object of type '" + input_obj_type +
                                 "' not accepted.  Must be one of " + ", ".join(accepted_input_types))

            # get set obj
            try:
                speciesTree_obj = wsClient.get_objects([{'ref': input_ref}])[0]['data']
            except:
                raise ValueError("unable to fetch speciesTree: " + input_ref)

            # get genome_refs from speciesTree and instantiate ETE3 tree and order
            #
            for genome_id in speciesTree_obj['default_node_labels'].keys():
                genome_refs.append(speciesTree_obj['ws_refs'][genome_id]['g'][0])

        else:
            raise ValueError ("Bad type for input object")


        # get additional info for genomes
        genome_obj_name_by_ref = dict()
        uniq_genome_ws_ids = dict()
        ws_name_by_genome_ref = dict()

        for genome_ref in genome_refs:

            # get genome object name
            input_ref = genome_ref
            try:
                input_obj_info = wsClient.get_object_info_new({'objects': [{'ref': input_ref}]})[0]
                input_obj_type = re.sub('-[0-9]+\.[0-9]+$', "", input_obj_info[TYPE_I])  # remove trailing version
                input_name = input_obj_info[NAME_I]
                if input_obj_info[WORKSPACE_I] != params['workspace_name']:
                    uniq_genome_ws_ids[input_obj_info[WSID_I]] = True
                ws_name_by_genome_ref[input_ref] = input_obj_info[WORKSPACE_I]

            except Exception as e:
                raise ValueError('Unable to get object from workspace: (' + input_ref + ')' + str(e))
            accepted_input_types = ["KBaseGenomes.Genome"]
            if input_obj_type not in accepted_input_types:
                raise ValueError("Input object of type '" + input_obj_type +
                                 "' not accepted.  Must be one of " + ", ".join(accepted_input_types))

            genome_obj_name_by_ref[input_ref] = input_name


        ### STEP 3: Determine which genomes have already got domain annotations
        domain_annot_done = dict()
        dom_annot_obj_info_list = []
        # read local workspace first
        try:
            dom_annot_obj_info_list.extend(wsClient.list_objects(
                {'workspaces': [params['workspace_name']], 'type': "KBaseGeneFamilies.DomainAnnotation"}))
        except Exception as e:
            raise ValueError("Unable to list DomainAnnotation objects from workspace: " + str(workspace_name) + " " + str(e))
        # read any remote workspaces
        for ws_id in uniq_genome_ws_ids.keys():
            try:
                dom_annot_obj_info_list.extend(wsClient.list_objects(
                    {'ids': [ws_id], 'type': "KBaseGeneFamilies.DomainAnnotation"}))
            except Exception as e:
                raise ValueError("Unable to list DomainAnnotation objects from workspace: " + str(ws_id) + " " + str(e))

        for info in dom_annot_obj_info_list:
            dom_annot_ref = str(info[WSID_I]) + '/' + str(info[OBJID_I]) + '/' + str(info[VERSION_I])
            try:
                domain_data = wsClient.get_objects([{'ref': dom_annot_ref}])[0]['data']
            except:
                raise ValueError("unable to fetch domain annotation: " + dom_annot_ref)

            # read domain data object
            genome_ref = domain_data['genome_ref']
            if genome_ref not in genome_refs:
                continue
            domain_annot_done[genome_ref] = True


        ### STEP 4: run DomainAnnotation on each genome in set
        try:
            #SERVICE_VER = 'dev'  # DEBUG
            #SERVICE_VER = 'release'
            SERVICE_VER = 'beta'  # has Pfam32
            daClient = DomainAnnotation(url=self.callbackURL, token=ctx['token'], service_ver=SERVICE_VER)  # SDK Local
            #daClient = DomainAnnotation (url=self.serviceWizardURL, token=ctx['token'], service_ver=SERVICE_VER)  # Dynamic service
        except:
            raise ValueError("unable to instantiate DomainAnnotationClient")

        # RUN DomainAnnotations
        report_text = ''
        for genome_i, genome_ref in enumerate(genome_refs):

            if 'override_annot' not in params or params['override_annot'] != '1':
                if genome_ref in domain_annot_done:
                    self.log(console, "SKIPPING repeat domain annotation for genome: " +
                             genome_obj_name_by_ref[genome_ref])

                    continue

            genome_obj_name = genome_obj_name_by_ref[genome_ref]
            domains_obj_name = re.sub('[\.\-\_\:]GenomeAnnotation$', '', genome_obj_name)
            domains_obj_name = re.sub('[\.\-\_\:]Genome$', '', domains_obj_name)
            domains_obj_name += '.DomainAnnotation'
            domains_obj_name = 'domains_' + domains_obj_name  # DEBUG
            DomainAnnotation_Params = {'genome_ref': genome_ref,
                                       'dms_ref': 'KBasePublicGeneDomains/All',
                                       'ws': params['workspace_name'],
                                       #'ws': ws_name_by_genome_ref[genome_ref],
                                       'output_result_id': domains_obj_name
                                       }
            self.log(console, "RUNNING domain annotation for genome: " + genome_obj_name_by_ref[genome_ref])
            self.log(console, "\n" + pformat(DomainAnnotation_Params))
            self.log(console, str(datetime.now()))

            #da_retVal = daClient.search_domains (DomainAnnotation_Params)[0]
            da_retVal = daClient.search_domains(DomainAnnotation_Params)
            this_output_ref = da_retVal['output_result_id']
            this_report_name = da_retVal['report_name']
            this_report_ref = da_retVal['report_ref']

            try:
                this_report_obj = wsClient.get_objects([{'ref': this_report_ref}])[0]['data']
            except:
                raise ValueError("unable to fetch report: " + this_report_ref)
            report_text += this_report_obj['text_message']
            report_text += "\n\n"

        ### STEP 5: build and save the report
        reportObj = {
            'objects_created': [],
            'text_message': report_text
        }
        SERVICE_VER = 'release'
        reportClient = KBaseReport(self.callbackURL, token=ctx['token'], service_ver=SERVICE_VER)
        report_info = reportClient.create({'report': reportObj, 'workspace_name': params['workspace_name']})

        ### STEP 6: construct the output to send back
        output = {'report_name': report_info['name'], 'report_ref': report_info['ref']}

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
           "genome_disp_name_config" of String, parameter "count_category" of
           String, parameter "heatmap" of type "bool", parameter "vertical"
           of type "bool", parameter "top_hit" of type "bool", parameter
           "e_value" of Double, parameter "log_base" of Double, parameter
           "required_COG_annot_perc" of Double, parameter
           "required_PFAM_annot_perc" of Double, parameter
           "required_TIGR_annot_perc" of Double, parameter
           "required_SEED_annot_perc" of Double, parameter
           "count_hypothetical" of type "bool", parameter "show_blanks" of
           type "bool", parameter "skip_missing_genomes" of type "bool",
           parameter "enforce_genome_version_match" of type "bool"
        :returns: instance of type "view_fxn_profile_Output" -> structure:
           parameter "report_name" of String, parameter "report_ref" of String
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN view_fxn_profile

        ### STEP 0: basic init
        console = []
        self.log(console, 'Running view_fxn_profile(): ')
        self.log(console, "\n" + pformat(params))

        # ws obj info indices
        [OBJID_I, NAME_I, TYPE_I, SAVE_DATE_I, VERSION_I, SAVED_BY_I, WSID_I,
         WORKSPACE_I, CHSUM_I, SIZE_I, META_I] = range(11)  # object_info tuple

        #SERVICE_VER = 'dev'  # DEBUG
        SERVICE_VER = 'release'
        token = ctx['token']
        try:
            wsClient = workspaceService(self.workspaceURL, token=token)
        except:
            raise ValueError("unable to instantiate wsClient")
        headers = {'Authorization': 'OAuth ' + token}
        env = os.environ.copy()
        env['KB_AUTH_TOKEN'] = token

        # param checks
        required_params = ['workspace_name',
                           'input_genomeSet_ref',
                           'genome_disp_name_config',
                           'namespace'
                           ]
        for arg in required_params:
            if arg not in params or params[arg] == None or params[arg] == '':
                raise ValueError("Must define required param: '" + arg + "'")

        if params['namespace'] != 'custom':
            if params.get('custom_target_fams') \
               and (params['custom_target_fams'].get('target_fams') \
                    or params['custom_target_fams'].get('extra_target_fam_groups_COG') \
                    or params['custom_target_fams'].get('extra_target_fam_groups_PFAM') \
                    or params['custom_target_fams'].get('extra_target_fam_groups_TIGR') \
                    or params['custom_target_fams'].get('extra_target_fam_groups_SEED')):

                self.log(console, "CUSTOM_TARGET_FAMS found.  Resetting NAMESPACE param to 'custom'")
                params['namespace'] = 'custom'
        else:
            if ('custom_target_fams' not in params or not params['custom_target_fams']) \
                or (
                    ('target_fams' not in params['custom_target_fams']
                     or not params['custom_target_fams']['target_fams'])
                and ('extra_target_fam_groups_COG' not in params['custom_target_fams'] or not params['custom_target_fams']['extra_target_fam_groups_COG'])
                and ('extra_target_fam_groups_PFAM' not in params['custom_target_fams'] or not params['custom_target_fams']['extra_target_fam_groups_PFAM'])
                and ('extra_target_fam_groups_TIGR' not in params['custom_target_fams'] or not params['custom_target_fams']['extra_target_fam_groups_TIGR'])
                and ('extra_target_fam_groups_SEED' not in params['custom_target_fams'] or not params['custom_target_fams']['extra_target_fam_groups_SEED'])
            ):
                error_msg = "If you select 'Custom' Domain Namespace, you must also Enable some Custom Domains or Custom Domain Groups"
                self.log (console, "ABORT: "+error_msg)
                raise ValueError("ABORT: "+error_msg)


        # base config
        namespace_classes = ['COG', 'PF', 'TIGR', 'SEED']
        show_blanks = False
        if 'show_blanks' in params and params['show_blanks'] == '1':
            show_blanks = True
        e_value_thresh = None
        if 'e_value' in params and params['e_value'] != None and params['e_value'] != '':
            e_value_thresh = float(params['e_value'])
        top_hit_flag = False
        if 'top_hit' in params and params['top_hit'] != None and params['top_hit'] != '' and params['top_hit'] != 0:
            top_hit_flag = True

        # set percentage required for annotated genes by each namespace
        required_annot_perc = dict()
        for namespace in namespace_classes:
            required_annot_perc[namespace] = 0.0
            if params.get('required_'+namespace+'_annot_perc'):
                required_annot_perc[namespace] = float(params.get('required_'+namespace+'_annot_perc'))


        # load provenance
        provenance = [{}]
        if 'provenance' in ctx:
            provenance = ctx['provenance']
        provenance[0]['input_ws_objects'] = [str(params['input_genomeSet_ref'])]

        # set the output path
        timestamp = int((datetime.utcnow() - datetime.utcfromtimestamp(0)).total_seconds() * 1000)
        output_dir = os.path.join(self.scratch, 'output.' + str(timestamp))
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # configure categories
        #
        (cats, cat2name, cat2group, domfam2cat, cat2domfams, namespaces_reading, target_fams,
         extra_target_fams, extra_target_fam_groups, domfam2group, domfam2name) = self._configure_categories(params)

        # instantiate custom FeatureSets
        #
        features_by_custom_target_fam = dict()
        custom_target_fam_features_hit = False


        # STEP 1 - Get the Data
        # get genome set
        #
        input_ref = params['input_genomeSet_ref']
        try:
            input_obj_info = wsClient.get_object_info_new({'objects': [{'ref': input_ref}]})[0]
            input_obj_name = input_obj_info[NAME_I]
            input_obj_type = re.sub('-[0-9]+\.[0-9]+$', "", input_obj_info[TYPE_I])  # remove trailing version
        except Exception as e:
            raise ValueError('Unable to get object from workspace: (' + input_ref + ')' + str(e))
        accepted_input_types = ["KBaseSearch.GenomeSet"]
        if input_obj_type not in accepted_input_types:
            raise ValueError("Input object of type '" + input_obj_type +
                             "' not accepted.  Must be one of " + ", ".join(accepted_input_types))

        # get set obj
        try:
            genomeSet_obj = wsClient.get_objects([{'ref': input_ref}])[0]['data']
        except:
            raise ValueError("unable to fetch genomeSet: " + input_ref)

        # get genome refs, object names, sci names, protein-coding gene counts, and SEED annot
        #
        genome_ids = genomeSet_obj['elements'].keys()  # note: genome_id may be meaningless
        genome_refs = []
        for genome_id in genome_ids:
            genome_refs.append(genomeSet_obj['elements'][genome_id]['ref'])

        genome_ref_by_versionless = dict()
        for genome_ref in genome_refs:
            (ws_id, obj_id, version) = genome_ref.split('/')
            genome_ref_by_versionless[ws_id+'/'+obj_id] = genome_ref

        genome_obj_name_by_ref = dict()
        genome_sci_name_by_ref = dict()
        genome_CDS_count_by_ref = dict()
        uniq_genome_ws_ids = dict()
        domain_annot_obj_by_genome_ref = dict()

        dom_hits = dict()  # initialize dom_hits here because reading SEED within genome
        genes_with_hits_cnt = dict()
        genes_with_validated_vocab_hits_cnt = dict()  # only used for SEED at this time

        for genome_ref in genome_refs:

            dom_hits[genome_ref] = dict()
            genes_with_hits_cnt[genome_ref] = dict()
            genes_with_validated_vocab_hits_cnt[genome_ref] = dict()

            # get genome object name
            input_ref = genome_ref
            try:
                input_obj_info = wsClient.get_object_info_new({'objects': [{'ref': input_ref}]})[0]
                input_obj_type = re.sub('-[0-9]+\.[0-9]+$', "", input_obj_info[TYPE_I])  # remove trailing version
                input_name = input_obj_info[NAME_I]
                if input_obj_info[WORKSPACE_I] != params['workspace_name']:
                    uniq_genome_ws_ids[input_obj_info[WSID_I]] = True

            except Exception as e:
                raise ValueError('Unable to get object from workspace: (' + input_ref + ')' + str(e))
            accepted_input_types = ["KBaseGenomes.Genome"]
            if input_obj_type not in accepted_input_types:
                raise ValueError("Input object of type '" + input_obj_type +
                                 "' not accepted.  Must be one of " + ", ".join(accepted_input_types))

            genome_obj_name_by_ref[genome_ref] = input_name

            try:
                genome_obj = wsClient.get_objects([{'ref': input_ref}])[0]['data']
            except:
                raise ValueError("unable to fetch genome: " + input_ref)

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

                        if self._check_SEED_function_defined_in_feature(feature):
                            gene_name = feature['id']

                            #if f_cnt % 100 == 0:
                            #    self.log (console, "fxn: '"+str(feature['function'])+"'")  # DEBUG

                            # store assignments for gene
                            for namespace in ['SEED']:
                                if namespace not in genes_with_hits_cnt[genome_ref]:
                                    genes_with_hits_cnt[genome_ref][namespace] = 0
                                if namespace not in genes_with_validated_vocab_hits_cnt[genome_ref]:
                                    genes_with_validated_vocab_hits_cnt[genome_ref][namespace] = 0

                                if gene_name not in dom_hits[genome_ref]:
                                    dom_hits[genome_ref][gene_name] = dict()
                                    dom_hits[genome_ref][gene_name][namespace] = dict()

                                non_hypothetical_hit = False
                                validated_vocab = False
                                domfam_list = []
                                for annot in self._get_SEED_annotations(feature):
                                    for annot2 in annot.strip().split('@'):
                                        domfam = self._standardize_SEED_subsys_ID(annot2)
                                        domfam_list.append(domfam)
                                        if not 'hypothetical' in domfam:
                                            non_hypothetical_hit = True
                                        else:
                                            continue
                                        if domfam in domfam2cat[namespace]:
                                            validated_vocab = True
                                        #if f_cnt % 100 == 0:
                                        #    self.log (console, "domfam: '"+str(domfam)+"'")  # DEBUG

                                if params.get('count_hypothetical') and int(params.get('count_hypothetical')) == 1:
                                    genes_with_hits_cnt[genome_ref][namespace] += 1
                                elif non_hypothetical_hit:
                                    genes_with_hits_cnt[genome_ref][namespace] += 1
                                if validated_vocab:
                                    genes_with_validated_vocab_hits_cnt[genome_ref][namespace] += 1

                                if top_hit_flag:  # does SEED give more than one function?
                                    domfam_list = [domfam_list[0]]
                                for domfam in domfam_list:
                                    dom_hits[genome_ref][gene_name][namespace][domfam] = True
                                    if domfam in target_fams:
                                        custom_target_fam_features_hit = True
                                        if domfam not in features_by_custom_target_fam:
                                            features_by_custom_target_fam[domfam] = dict()
                                        if genome_ref not in features_by_custom_target_fam[domfam]:
                                            features_by_custom_target_fam[domfam][genome_ref] = []
                                        features_by_custom_target_fam[domfam][genome_ref].append(gene_name)
                    #f_cnt += 1  # DEBUG


        # Make sure we have CDSs
        #
        missing_genes = []
        for genome_ref in genome_refs:
            if genome_CDS_count_by_ref[genome_ref] == 0:
                missing_genes.append("\t" + 'MISSING GENES FOR: ' + 'ref: '+genome_ref + ', obj_name: '+genome_obj_name_by_ref[genome_ref]+', sci_name: '+genome_sci_name_by_ref[genome_ref])
                missing_genes_by_genome_ref[genome_ref] = True
        if missing_genes:
            error_msg = "ABORT: Some of the Genomes are missing gene calls.  Please run RAST or Prokka App to get Genome objects with Gene calls for the following Genomes\n"
            error_msg += "\n".join(missing_genes)
            self.log(console, error_msg)
            raise ValueError(error_msg)


        # check for validated vocab if reading SEED
        #
        missing_SEED_annot_by_genome_ref = dict()
        missing_SEED_annot = []
        if 'SEED' in namespaces_reading:
            namespace = 'SEED'
            fraction_required_valid = required_annot_perc[namespace] / 100.0
            for genome_ref in genome_refs:
                self.log(console, "genome:"+genome_ref+" gene cnt with validated annot:"+str(genes_with_validated_vocab_hits_cnt[genome_ref][namespace])+" gene cnt with annot:"+str(genes_with_hits_cnt[genome_ref][namespace]))  # DEBUG

                valid_fraction = genes_with_validated_vocab_hits_cnt[genome_ref][namespace] / float(genes_with_hits_cnt[genome_ref][namespace])
                if valid_fraction < fraction_required_valid:
                    missing_SEED_annot.append("\t" + 'MISSING RAST SEED ANNOTATION FOR: ' + 'ref: '+genome_ref + ', obj_name: '+genome_obj_name_by_ref[genome_ref]+', sci_name: '+genome_sci_name_by_ref[genome_ref]+".  You can drop the threshold required in advanced parameters.")
                    missing_SEED_annot_by_genome_ref[genome_ref] = True

            if missing_SEED_annot:
                if len(missing_SEED_annot) == len(genome_refs):
                    error_msg = "ABORT: ALL genomes are missing RAST SEED Annotation.  You must run the RAST SEED Annotation App first\n"
                    error_msg += "\n".join(missing_SEED_annot)
                    self.log(console, error_msg)
                    raise ValueError(error_msg)

                # if strict, then abort
                if not params.get('skip_missing_genomes') or int(params.get('skip_missing_genomes')) != 1:
                    error_msg = "ABORT: You must run the RAST SEED Annotation App or use SKIP option on below genomes first\n"
                    error_msg += "\n".join(missing_SEED_annot)
                    self.log(console, error_msg)
                    raise ValueError(error_msg)
                # if skipping, then remove genomes with missing annotations
                else:
                    new_genome_refs = []
                    for genome_ref in genome_refs:
                        if genome_ref in missing_SEED_annot_by_genome_ref:
                            continue
                        new_genome_refs.append(genome_ref)
                    genome_refs = new_genome_refs
                    self.log(console, "SKIP option selected. If you wish to include the below Genomes, you must run the RAST SEED Annotation App first")
                    self.log(console, "\n".join(missing_SEED_annot))


        # determine if custom domains are not just SEED
        #
        search_domains_just_SEED = True
        for namespace in namespaces_reading.keys():
            if namespace != 'SEED':
                search_domains_just_SEED = False

        # read DomainAnnotation object to capture domain hits to genes within each namespace
        #
        if search_domains_just_SEED:
            self.log(console, "Search Domains just SEED.  Not looking for Domain Annotations")
        else:
            self.log(console, "Search Domains other than SEED.  Looking for Domain Annotations")
            dom_annot_found = dict()

            KBASE_DOMAINHIT_GENE_ID_I = 0
            KBASE_DOMAINHIT_GENE_BEG_I = 1  # not used
            KBASE_DOMAINHIT_GENE_END_I = 2  # not used
            KBASE_DOMAINHIT_GENE_STRAND_I = 3  # not used
            KBASE_DOMAINHIT_GENE_HITS_DICT_I = 4
            KBASE_DOMAINHIT_GENE_HITS_DICT_BEG_J = 0
            KBASE_DOMAINHIT_GENE_HITS_DICT_END_J = 1
            KBASE_DOMAINHIT_GENE_HITS_DICT_EVALUE_J = 2
            KBASE_DOMAINHIT_GENE_HITS_DICT_BITSCORE_J = 3
            KBASE_DOMAINHIT_GENE_HITS_DICT_ALNPERC_J = 4

            # DEBUG
            #for genome_ref in genome_refs:
            #    self.log (console, "SEED ANNOT CNT A: '"+str(genes_with_hits_cnt[genome_ref]['SEED'])+"'")

            dom_annot_obj_info_list = []
            # read local workspace first
            try:
                dom_annot_obj_info_list.extend(wsClient.list_objects(
                    {'workspaces': [params['workspace_name']], 'type': "KBaseGeneFamilies.DomainAnnotation"}))
            except Exception as e:
                raise ValueError("Unable to list DomainAnnotation objects from workspace: " +
                                 str(ws_id) + " " + str(e))
            # read any remaining remote workspaces
            for ws_id in uniq_genome_ws_ids.keys():
                try:
                    dom_annot_obj_info_list.extend(wsClient.list_objects(
                        {'ids': [ws_id], 'type': "KBaseGeneFamilies.DomainAnnotation"}))
                except Exception as e:
                    raise ValueError("Unable to list DomainAnnotation objects from workspace: " +
                                     str(ws_id) + " " + str(e))

            for info in dom_annot_obj_info_list:
                dom_annot_ref = str(info[WSID_I]) + '/' + str(info[OBJID_I]) + '/' + str(info[VERSION_I])
                try:
                    domain_data = wsClient.get_objects([{'ref': dom_annot_ref}])[0]['data']
                except:
                    raise ValueError("unable to fetch domain annotation: " + dom_annot_ref)

                # read domain data object
                genome_ref = domain_data['genome_ref']
                if params.get('enforce_genome_version_match') and int(params.get('enforce_genome_version_match')) == 1:
                    # skip extra domainannots
                    if genome_ref not in genome_refs:
                        continue
                else:
                    (ws_id, obj_id, version) = genome_ref.split('/')
                    genome_ref_versionless = ws_id+'/'+obj_id
                    # skip extra domainannots
                    if genome_ref_versionless not in genome_ref_by_versionless:
                        continue

                    # report any change in obj version
                    source_obj_type = 'GenomeSet'
                    source_genome_ref = genome_ref_by_versionless[ws_id+'/'+obj_id]
                    if genome_ref != source_genome_ref:
                        self.log(console, "DomainAnnotation object generated from different version of genome found in "+source_obj_type+".  DomainAnnotation for ref: "+genome_ref+" obj_name: "+genome_obj_name_by_ref[source_genome_ref]+" sci_name: "+genome_sci_name_by_ref[source_genome_ref]+" but using genome version from "+source_obj_type+" instead: "+source_genome_ref)
                    else:
                        self.log(console, "DomainAnnotation object generated from same version of genome ref: "+genome_ref+" obj_name: "+genome_obj_name_by_ref[genome_ref]+" sci_name: "+genome_sci_name_by_ref[genome_ref]+" as in "+source_obj_type)

                    genome_ref = source_genome_ref

                # avoid duplicate domain annotations
                dom_annot_found[genome_ref] = True
                if genome_ref not in domain_annot_obj_by_genome_ref:
                    domain_annot_obj_by_genome_ref[genome_ref] = dom_annot_ref
                    self.log(console, "DomainAnnotation object "+str(domain_annot_obj_by_genome_ref[genome_ref])+" being used for Genome obj_name: "+genome_obj_name_by_ref[genome_ref]+" sci_name: "+genome_sci_name_by_ref[genome_ref])
                else:
                    self.log(console, "DomainAnnotation object "+str(domain_annot_obj_by_genome_ref[genome_ref])+" already found for Genome obj_name: "+genome_obj_name_by_ref[genome_ref]+" sci_name: "+genome_sci_name_by_ref[genome_ref]+". Ignoring DomainAnnotation "+dom_annot_ref)
                    continue

                if genome_ref not in dom_hits:
                    dom_hits[genome_ref] = dict()

                if genome_ref not in genes_with_hits_cnt:
                    genes_with_hits_cnt[genome_ref] = dict()
                    #self.log (console, "ADDING "+genome_ref+" to genes_with_hits_cnt")  # DEBUG

                for scaffold_id_iter in domain_data['data'].keys():
                    for CDS_domain_list in domain_data['data'][scaffold_id_iter]:
                        gene_ID = CDS_domain_list[KBASE_DOMAINHIT_GENE_ID_I]
                        #gene_name = re.sub ('^'+genome_object_name+'.', '', gene_ID)
                        gene_name = gene_ID
                        #(contig_name, gene_name) = (gene_ID[0:gene_ID.index(".")], gene_ID[gene_ID.index(".")+1:])
                        #print ("DOMAIN_HIT: "+contig_name+" "+gene_name)  # DEBUG
                        #print ("DOMAIN_HIT for gene: "+gene_name)  # DEBUG
                        #gene_beg       = CDS_domain_list[KBASE_DOMAINHIT_GENE_BEG_I]
                        #gene_end       = CDS_domain_list[KBASE_DOMAINHIT_GENE_END_I]
                        #gene_strand    = CDS_domain_list[KBASE_DOMAINHIT_GENE_STRAND_I]
                        gene_hits_dict = CDS_domain_list[KBASE_DOMAINHIT_GENE_HITS_DICT_I]

                        dom_hits_by_namespace = dict()
                        top_hit_evalue_by_namespace = dict()
                        top_hit_dom_by_namespace = dict()

                        for namespace in namespace_classes:
                            dom_hits_by_namespace[namespace] = dict()
                            top_hit_evalue_by_namespace[namespace] = 100
                            top_hit_dom_by_namespace[namespace] = None

                        for domfam in gene_hits_dict.keys():
                            if domfam.startswith('PF'):
                                domfam_clean = re.sub('\.[^\.]*$', '', domfam)
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
                                beg = int(hit[KBASE_DOMAINHIT_GENE_HITS_DICT_BEG_J])
                                end = int(hit[KBASE_DOMAINHIT_GENE_HITS_DICT_END_J])
                                e_value = float(hit[KBASE_DOMAINHIT_GENE_HITS_DICT_EVALUE_J])
                                bit_score = float(hit[KBASE_DOMAINHIT_GENE_HITS_DICT_BITSCORE_J])
                                aln_perc = float(hit[KBASE_DOMAINHIT_GENE_HITS_DICT_ALNPERC_J])

                                if e_value_thresh != None and e_value > e_value_thresh:
                                    continue
                                if top_hit_flag:
                                    if top_hit_dom_by_namespace[namespace] == None \
                                       or top_hit_evalue_by_namespace[namespace] > e_value:
                                        top_hit_dom_by_namespace[namespace] = domfam_clean
                                        top_hit_evalue_by_namespace[namespace] = e_value

                                dom_hits_by_namespace[namespace][domfam_clean] = True
                                #if namespace == 'COG':
                                #   self.log(console,"STORING "+genome_ref+" "+namespace+" "+domfam_clean)  # DEBUG

                        # store assignments for gene
                        for namespace in namespace_classes:
                            if namespace == 'SEED':
                                continue
                            if namespace not in genes_with_hits_cnt[genome_ref]:
                                genes_with_hits_cnt[genome_ref][namespace] = 0

                                #self.log(console,"GENOME "+genome_ref+" HIT NAMESPACE "+namespace)  # DEBUG

                            if dom_hits_by_namespace[namespace]:
                                genes_with_hits_cnt[genome_ref][namespace] += 1
                                #self.log(console,"GENOME "+genome_ref+" HIT NAMESPACE "+namespace+ " count "+str(genes_with_hits_cnt[genome_ref][namespace])) # DEBUG

                                if gene_name not in dom_hits[genome_ref]:
                                    dom_hits[genome_ref][gene_name] = dict()

                                if top_hit_flag:
                                    dom_hits[genome_ref][gene_name][namespace] = {
                                        top_hit_dom_by_namespace[namespace]: True}
                                else:
                                    dom_hits[genome_ref][gene_name][namespace] = dom_hits_by_namespace[namespace]

                                # store for featureset
                                for domfam in dom_hits[genome_ref][gene_name][namespace].keys():
                                    if domfam in target_fams:
                                        custom_target_fam_features_hit = True
                                        if domfam not in features_by_custom_target_fam:
                                            features_by_custom_target_fam[domfam] = dict()
                                        if genome_ref not in features_by_custom_target_fam[domfam]:
                                            features_by_custom_target_fam[domfam][genome_ref] = []
                                        features_by_custom_target_fam[domfam][genome_ref].append(gene_name)


            # make sure we have domain annotations for all genomes
            missing_annot = []
            missing_dom_annot_by_genome_ref = dict()
            for genome_ref in genome_refs:
                if genome_ref not in dom_annot_found:
                    missing_annot.append("\t" + 'MISSING DOMAIN ANNOTATION FOR: ' + 'ref: '+genome_ref + ', obj_name: '+genome_obj_name_by_ref[genome_ref]+', sci_name: '+genome_sci_name_by_ref[genome_ref])
                    missing_dom_annot_by_genome_ref[genome_ref] = True

            if missing_annot:
                if len(missing_annot) == len(genome_refs):
                    error_msg = "ABORT: ALL genomes have no matching Domain Annotation.  You must run the 'Domain Annotation' App first\n"
                    error_msg += "\n".join(missing_annot)
                    self.log(console, error_msg)
                    raise ValueError(error_msg)

                # if strict, then abort
                if not params.get('skip_missing_genomes') or int(params.get('skip_missing_genomes')) != 1:
                    error_msg = "ABORT: You must run the 'Domain Annotation' App or use SKIP option on below genomes first\n"
                    error_msg += "\n".join(missing_annot)
                    self.log(console, error_msg)
                    raise ValueError(error_msg)
                # if skipping, then remove genomes with missing annotations
                else:
                    new_genome_refs = []
                    for genome_ref in genome_refs:
                        if genome_ref in missing_dom_annot_by_genome_ref:
                            continue
                        new_genome_refs.append(genome_ref)
                    genome_refs = new_genome_refs
                    self.log(console, "SKIP option selected. If you wish to include the below Genomes, you must run the 'Domain Annotation' App first")
                    self.log(console, "\n".join(missing_annot))

        # DEBUG
        #for genome_ref in genome_refs:
        #    self.log (console, "SEED ANNOT CNT B: '"+str(genes_with_hits_cnt[genome_ref]['SEED'])+"'")


        # Alert user for any genomes that are missing annotations in a requested namespace
        #   this can happen even with a DomainAnnotation object if the namespace was skipped
        #
        inadequate_annot = []
        inadequate_annot_by_genome_ref = dict()
        for genome_ref in genome_refs:
            total_genes = genome_CDS_count_by_ref[genome_ref]

            for namespace in sorted(namespaces_reading.keys()):
                fraction_requiring_annotation = required_annot_perc[namespace] / 100.0
                if namespace == 'SEED':
                    annotation_tool = 'RAST Genome Annotation App'
                else:
                    annotation_tool = 'Domain Annotation App'
                if genes_with_hits_cnt[genome_ref][namespace] < fraction_requiring_annotation * total_genes:
                    inadequate_annot.append("\t" + 'INADEQUATE DOMAIN ANNOTATION FOR: ' + 'ref: '+genome_ref + ', obj_name: '+genome_obj_name_by_ref[genome_ref]+', sci_name: '+genome_sci_name_by_ref[genome_ref]+".  Namespace: "+namespace+" found in "+str(genes_with_hits_cnt[genome_ref][namespace])+" of a total of "+str(total_genes)+".  "+str(required_annot_perc[namespace])+"% were configured in advanced parameter input required to be annotated by "+namespace+".  Something may have gone wrong with "+annotation_tool+".  Try rerunning or dropping the threshold required in advanced parameters.")
                    inadequate_annot_by_genome_ref[genome_ref] = True

            if inadequate_annot:
                if len(inadequate_annot) == len(genome_refs):
                    error_msg = "ABORT: ALL genomes have poor Domain Annotation.  You must run the 'Domain Annotation' App first\n"
                    error_msg += "\n".join(inadequate_annot)
                    self.log(console, error_msg)
                    raise ValueError(error_msg)

                # if strict, then abort
                if not params.get('skip_missing_genomes') or int(params.get('skip_missing_genomes')) != 1:
                    error_msg = "ABORT: You must run the 'Domain Annotation' App or use SKIP option on below genomes first\n"
                    error_msg += "\n".join(inadequate_annot)
                    self.log(console, error_msg)
                    raise ValueError(error_msg)
                # if skipping, then remove genomes with missing annotations
                else:
                    new_genome_refs = []
                    for genome_ref in genome_refs:
                        if genome_ref in inadequate_annot_by_genome_ref:
                            continue
                        new_genome_refs.append(genome_ref)
                    genome_refs = new_genome_refs
                    self.log(console, "SKIP option selected. If you wish to include the below Genomes, you must run the 'Domain Annotation' App first")
                    self.log(console, "\n".join(inadequate_annot))


        # STEP 2 - Analysis
        # calculate table
        #
        table_data = dict()
        INSANE_VALUE = 10000000000000000
        overall_low_val = INSANE_VALUE
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
                        namespace = re.sub('\d*$', '', cat)
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
                                namespace = re.sub('\d*$', '', cat)
                        else:
                            namespace = params['namespace']
                        total_genes = genes_with_hits_cnt[genome_ref][namespace]
                    else:
                        total_genes = genome_CDS_count_by_ref[genome_ref]

                    if total_genes > 0:
                        table_data[genome_ref][cat] /= float(total_genes)
                        table_data[genome_ref][cat] *= 100.0
                    else:
                        table_data[genome_ref][cat] = 0

        # determine high and low val
        for genome_ref in genome_refs:
            for cat in cats:
                val = table_data[genome_ref][cat]
                if val == 0:
                    continue
                #self.log (console, "HIGH VAL SCAN CAT: '"+cat+"' VAL: '"+str(val)+"'")  # DEBUG
                if 'log_base' in params and params['log_base'] != None and params['log_base'] != '':
                    log_base = float(params['log_base'])
                    if log_base <= 1.0:
                        raise ValueError("log base must be > 1.0")
                    val = math.log(val, log_base)
                if val > overall_high_val:
                    overall_high_val = val
                if val < overall_low_val:
                    overall_low_val = val
        if overall_high_val == -INSANE_VALUE:
            raise ValueError("unable to find any counts")

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


        # STEP 3 - Create and save featureSets
        #
        objects_created = []
        if custom_target_fam_features_hit:
            featureSet_by_custom_target_fam = dict()
            for target_fam in sorted(features_by_custom_target_fam.keys()):
                featureSet_by_custom_target_fam[target_fam] = dict()
                for genome_ref in sorted(features_by_custom_target_fam[target_fam].keys()):
                    for fid in sorted(features_by_custom_target_fam[target_fam][genome_ref]):
                        if fid in featureSet_by_custom_target_fam[target_fam]:
                            featureSet_by_custom_target_fam[target_fam][fid].append(genome_ref)
                        else:
                            featureSet_by_custom_target_fam[target_fam][fid] = [genome_ref]

                fs_name = target_fam+'-'+input_obj_name+'.FeatureSet'
                fs_desc = 'Hits by '+target_fam+' to '+input_obj_name
                fs_obj = {'description': fs_desc,
                          'elements': featureSet_by_custom_target_fam[target_fam]
                         }
                new_obj_info = wsClient.save_objects({
                    'workspace': params['workspace_name'],
                    'objects': [
                        {'type': 'KBaseCollections.FeatureSet',
                         'data': fs_obj,
                         'name': fs_name,
                         'meta': {},
                         'provenance': provenance
                         }]
                })[0]
                objects_created.append(
                    {'ref': str(new_obj_info[6]) + '/' + str(new_obj_info[0]) + '/' + str(new_obj_info[4]), 'description': fs_desc})
                featureSet_by_custom_target_fam[target_fam] = {}  # free memory
                fs_obj = {}  # free memory


        # STEP 4 - build report
        #
        reportName = 'kb_phylogenomics_report_' + str(uuid.uuid4())
        reportObj = {'objects_created': objects_created,
                     'direct_html_link_index': 0,
                     'file_links': [],
                     'html_links': [],
                     'workspace_name': params['workspace_name'],
                     'report_object_name': reportName
                     }

        # build html report
        sp = '&nbsp;'
        text_color = "#606060"
        text_color_2 = "#606060"
        head_color_1 = "#eeeeee"
        head_color_2 = "#eeeeee"
        border_color = "#cccccc"
        border_cat_color = "#ffccff"
        #graph_color = "lightblue"
        #graph_width = 100
        #graph_char = "."
        graph_char = sp
        color_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e']
        max_color = len(color_list) - 1
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
        if len(group_order) > 0:
            show_groups = True

        # sort genomes by display name
        genome_ref_by_disp_name = dict()
        for genome_ref in genome_refs:
            genome_obj_name = genome_obj_name_by_ref[genome_ref]
            genome_sci_name = genome_sci_name_by_ref[genome_ref]
            [ws_id, obj_id, genome_obj_version] = genome_ref.split('/')
            genome_disp_name = ''
            if 'obj_name' in params.get('genome_disp_name_config'):
                genome_disp_name += genome_obj_name
                if 'ver' in params.get('genome_disp_name_config'):
                    genome_disp_name += '.v'+str(genome_obj_version)

                if 'sci_name' in params.get('genome_disp_name_config'):
                    genome_disp_name += ': '+genome_sci_name
            else:
                genome_disp_name = genome_sci_name

            if genome_disp_name in genome_ref_by_disp_name:
                error_msg = "duplicate genome display names.  Can be fixed by adding genome object name to report"
                self.log (console, "ABORT: "+error_msg)
                raise ValueError ("ABORT: "+error_msg)

            genome_ref_by_disp_name[genome_disp_name] = genome_ref

        # html report buffer
        html_report_lines = []
        html_report_lines += ['<html>']
        html_report_lines += ['<head>']
        html_report_lines += ['<title>KBase Functional Domain Profile</title>']
        html_report_lines += ['<style>']
        html_report_lines += [
            ".vertical-text {\ndisplay: inline-block;\noverflow: hidden;\nwidth: 0.65em;\n}\n.vertical-text__inner {\ndisplay: inline-block;\nwhite-space: nowrap;\nline-height: 1.1;\ntransform: translate(0,100%) rotate(-90deg);\ntransform-origin: 0 0;\n}\n.vertical-text__inner:after {\ncontent: \"\";\ndisplay: block;\nmargin: 0.0em 0 100%;\n}"]
        html_report_lines += [
            ".vertical-text_title {\ndisplay: inline-block;\noverflow: hidden;\nwidth: 1.0em;\n}\n.vertical-text__inner_title {\ndisplay: inline-block;\nwhite-space: nowrap;\nline-height: 1.0;\ntransform: translate(0,100%) rotate(-90deg);\ntransform-origin: 0 0;\n}\n.vertical-text__inner_title:after {\ncontent: \"\";\ndisplay: block;\nmargin: 0.0em 0 100%;\n}"]
        html_report_lines += ['</style>']
        html_report_lines += ['</head>']
        html_report_lines += ['<body bgcolor="white">']

        # genomes as rows
        if 'vertical' in params and params['vertical'] == "1":
            # table header
            html_report_lines += ['<table cellpadding=' + graph_padding +
                                  ' cellspacing=' + graph_spacing + ' border=' + border + '>']
            corner_rowspan = "1"
            if show_groups:
                corner_rowspan = "2"
            label = ''
            if params['namespace'] != 'custom':
                label = params['namespace']
                if label == 'PF':
                    label = 'PFAM'
                elif label == 'TIGR':
                    label = 'TIGRFAM'
            html_report_lines += ['<tr><td valign=bottom align=right rowspan=' + corner_rowspan +
                                  '><div class="vertical-text_title"><div class="vertical-text__inner_title"><font color="' + text_color + '">' + label + '</font></div></div></td>']

            # group headers
            if show_groups:
                for cat_group in group_order:
                    if cat_group.startswith('SEED'):
                        cat_group_disp = re.sub('_', ' ', cat_group)
                    else:
                        cat_group_disp = cat_group
                    cat_group_words = cat_group_disp.split()
                    max_group_width = 3 * group_size[cat_group]
                    if len(cat_group) > max_group_width:
                        new_cat_group_words = []
                        sentence_len = 0
                        for w_i, word in enumerate(cat_group_words):
                            new_cat_group_words.append(word)
                            sentence_len += len(word)
                            if w_i < len(cat_group_words) - 1:
                                if sentence_len + 1 + len(cat_group_words[w_i + 1]) > max_group_width:
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
                        html_report_lines += ['<td bgcolor=white colspan=' + str(group_size[cat_group]) + '></td>']
                    else:
                        html_report_lines += ['<td style="border-right:solid 2px ' + border_cat_color + '; border-bottom:solid 2px ' + border_cat_color + '" bgcolor="' + head_color_1 +
                                              '"valign=middle align=center colspan=' + str(group_size[cat_group]) + '><font color="' + text_color + '" size=' + str(graph_cat_fontsize) + '><b>' + cat_group_disp + '</b></font></td>']

                html_report_lines += ['</tr><tr>']

            # column headers
            for cat in cats:
                if not cat_seen[cat] and not show_blanks:
                    continue
                if params['namespace'] == 'custom':
                    if cat.startswith('SEED'):
                        namespace = 'SEED'
                    else:
                        namespace = re.sub("\d*$", "", cat)
                    cell_title = domfam2name[namespace][cat].strip()
                    cat_disp = cat
                    cat_disp = re.sub('^SEED', 'SEED:', cat_disp)
                else:
                    cell_title = cat2name[params['namespace']][cat].strip()
                    cat_disp = cat
                    cat_disp = re.sub("TIGR_", "", cat_disp)
                if len(cat_disp) > cat_disp_trunc_len + 1:
                    cat_disp = cat_disp[0:cat_disp_trunc_len] + '*'
                html_report_lines += ['<td style="border-right:solid 2px ' + border_cat_color + '; border-bottom:solid 2px ' +
                                      border_cat_color + '" bgcolor="' + head_color_2 + '"title="' + cell_title + '" valign=bottom align=center>']
                if params['namespace'] != 'COG':
                    html_report_lines += ['<div class="vertical-text"><div class="vertical-text__inner">']
                html_report_lines += ['<font color="' + text_color_2 + '" size=' + graph_cat_fontsize + '><b>']
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
            for genome_disp_name in sorted(genome_ref_by_disp_name.keys()):
                genome_ref = genome_ref_by_disp_name[genome_disp_name]

                html_report_lines += ['<tr>']
                html_report_lines += ['<td align=right><font color="' + text_color + '" size=' +
                                      graph_gen_fontsize + '><b><nobr>' + genome_disp_name + '</nobr></b></font></td>']
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
                                raise ValueError("log base must be > 1.0")
                            val = math.log(val, log_base)
                        if overall_high_val == overall_low_val:
                            denom = 1.0
                        else:
                            denom = float(overall_high_val - overall_low_val)
                        cell_color_i = max_color - \
                            int(round(max_color * (val - overall_low_val) / denom))
                        c = color_list[cell_color_i]
                        cell_color = '#' + c + c + c + c + 'FF'

                    if params['count_category'].startswith('perc'):
                        cell_val = str("%.3f" % table_data[genome_ref][cat])
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
                        html_report_lines += ['<td align=center valign=middle title="' + cell_val + '" style="width:' + cell_width + '" bgcolor="' +
                                              cell_color + '"><font color="' + this_text_color + '" size=' + cell_fontsize + '>' + this_graph_char + '</font></td>']
                    else:
                        html_report_lines += ['<td align=center valign=middle style="' + cell_width + '; border-right:solid 2px ' + border_color +
                                              '; border-bottom:solid 2px ' + border_color + '"><font color="' + text_color + '" size=' + cell_fontsize + '>' + cell_val + '</font></td>']

                html_report_lines += ['</tr>']
            html_report_lines += ['</table>']

        # genomes as columns
        else:
            raise ValueError("Do not yet support Genomes as columns")

        # key table
        html_report_lines += ['<p>']
        html_report_lines += ['<table cellpadding=3 cellspacing=2 border=' + border + '>']
        html_report_lines += ['<tr><td valign=middle align=left colspan=3 style="border-bottom:solid 4px ' +
                              border_color + '"><font color="' + text_color + '"><b>KEY</b></font></td></tr>']

        if show_groups:
            group_cat_i = 0
            for cat_group in group_order_with_blanks:
                if cat_group.startswith('SEED'):
                    cat_group_disp = re.sub('_', ' ', cat_group)
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
                    html_report_lines += ['<td bgcolor=white rowspan=' + str(
                        group_size_with_blanks[cat_group]) + ' style="border-right:solid 4px ' + border_color + '"></td>']
                else:
                    html_report_lines += ['<td style="border-right:solid 4px ' + border_color + '" valign=top align=right rowspan=' + str(
                        group_size_with_blanks[cat_group]) + '><font color="' + text_color + '" size=' + str(graph_cat_fontsize) + '><b>' + cat_group_disp + '</b></font></td>']

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
                        namespace = re.sub('\d*$', '', first_cat)
                    cat_disp = re.sub('^SEED', 'SEED:', first_cat)
                    desc = domfam2name[namespace][domfam]
                else:
                    namespace = params['namespace']
                    cat_disp = first_cat
                    desc = cat2name[namespace][first_cat]
                if len(cat_disp) > cat_disp_trunc_len + 1:
                    cat_disp = cat_disp[0:cat_disp_trunc_len] + '*'
                cat_disp = sp + cat_disp

                html_report_lines += ['<td valign=middle align=left bgcolor="' + cell_color + '" style="border-right:solid 4px ' +
                                      border_color + '"><font color="' + text_color + '" size=' + graph_cat_fontsize + '>' + cat_disp + '</font></td>']
                html_report_lines += ['<td valign=middle align=left bgcolor="' + cell_color + '"><font color="' +
                                      text_color + '" size=' + graph_cat_fontsize + '>' + sp + desc + '</font></td>']
                html_report_lines += ['</tr>']

                group_cat_i += 1

                # add rest of cats in group
                for c_i in range(group_cat_i, group_cat_i + group_size_with_blanks[cat_group] - 1):
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
                            namespace = re.sub('\d*$', '', cat)
                        cat_disp = re.sub('^SEED', 'SEED:', cat)
                        desc = domfam2name[namespace][domfam]
                    else:
                        namespace = params['namespace']
                        cat_disp = cat
                        desc = cat2name[namespace][cat]
                    if len(cat_disp) > cat_disp_trunc_len + 1:
                        cat_disp = cat_disp[0:cat_disp_trunc_len] + '*'
                    cat_disp = sp + cat_disp

                    html_report_lines += ['<tr>']
                    html_report_lines += ['<td valign=middle align=left bgcolor="' + cell_color + '" style="border-right:solid 4px ' +
                                          border_color + '"><font color="' + text_color + '" size=' + graph_cat_fontsize + '>' + cat_disp + '</font></td>']
                    html_report_lines += ['<td valign=middle align=left bgcolor="' + cell_color + '"><font color="' +
                                          text_color + '" size=' + graph_cat_fontsize + '>' + sp + desc + '</font></td>']
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
                        namespace = re.sub('\d*$', '', domfam)
                    cat_disp = re.sub('^SEED', 'SEED:', cat)
                    desc = domfam2name[namespace][domfam]
                else:
                    namespace = params['namespace']
                    cat_disp = cat
                    desc = cat2name[namespace][cat]
                if len(cat_disp) > cat_disp_trunc_len + 1:
                    cat_disp = cat_disp[0:cat_disp_trunc_len] + '*'
                html_report_lines += ['<tr>']
                html_report_lines += ['<td valign=middle align=left bgcolor="' + cell_color + '" style="border-right:solid 4px ' +
                                      border_color + '><font color="' + text_color + '" size=' + graph_cat_fontsize + '>' + cat_disp + '</font></td>']
                html_report_lines += ['<td valign=middle align=left bgcolor="' + cell_color +
                                      '"><font color="' + text_color + '" size=' + graph_cat_fontsize + '>' + desc + '</font></td>']
                html_report_lines += ['</tr>']

        html_report_lines += ['</table>']

        # close
        html_report_lines += ['</body>']
        html_report_lines += ['</html>']

        html_report_str = "\n".join(html_report_lines)
        #reportObj['direct_html'] = html_report_str

        # write html to file and upload
        html_file = os.path.join(output_dir, 'domain_profile_report.html')
        with open(html_file, 'w', 0) as html_handle:
            html_handle.write(html_report_str)
        dfu = DFUClient(self.callbackURL)
        try:
            upload_ret = dfu.file_to_shock({'file_path': html_file,
                                            'make_handle': 0,
                                            'pack': 'zip'})
        except:
            raise ValueError('Logging exception loading html_report to shock')

        reportObj['html_links'] = [{'shock_id': upload_ret['shock_id'],
                                    'name': 'domain_profile_report.html',
                                    'label': 'Functional Domain Profile report'}
                                   ]

        # save report object
        #
        reportClient = KBaseReport(self.callbackURL, token=ctx['token'], service_ver=SERVICE_VER)
        #report_info = report.create({'report':reportObj, 'workspace_name':params['workspace_name']})
        report_info = reportClient.create_extended_report(reportObj)

        output = {'report_name': report_info['name'], 'report_ref': report_info['ref']}

        #END view_fxn_profile

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method view_fxn_profile return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]

    def view_fxn_profile_featureSet(self, ctx, params):
        """
        :param params: instance of type "view_fxn_profile_featureSet_Input"
           (view_fxn_profile_featureSet() ** ** show a table/heatmap of
           general categories or custom gene families for a set of Genomes)
           -> structure: parameter "workspace_name" of type "workspace_name"
           (** Common types), parameter "input_featureSet_ref" of type
           "data_obj_ref", parameter "namespace" of String, parameter
           "custom_target_fams" of type "CustomTargetFams" (parameter groups)
           -> structure: parameter "target_fams" of list of String, parameter
           "extra_target_fam_groups_COG" of list of String, parameter
           "extra_target_fam_groups_PFAM" of list of String, parameter
           "extra_target_fam_groups_TIGR" of list of String, parameter
           "extra_target_fam_groups_SEED" of list of String, parameter
           "genome_disp_name_config" of String, parameter "count_category" of
           String, parameter "heatmap" of type "bool", parameter "vertical"
           of type "bool", parameter "top_hit" of type "bool", parameter
           "e_value" of Double, parameter "log_base" of Double, parameter
           "required_COG_annot_perc" of Double, parameter
           "required_PFAM_annot_perc" of Double, parameter
           "required_TIGR_annot_perc" of Double, parameter
           "required_SEED_annot_perc" of Double, parameter
           "count_hypothetical" of type "bool", parameter "show_blanks" of
           type "bool", parameter "skip_missing_genomes" of type "bool",
           parameter "enforce_genome_version_match" of type "bool"
        :returns: instance of type "view_fxn_profile_featureSet_Output" ->
           structure: parameter "report_name" of String, parameter
           "report_ref" of String
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN view_fxn_profile_featureSet

        ### STEP 0: basic init
        console = []
        self.log(console, 'Running view_fxn_profile_featureSet(): ')
        self.log(console, "\n" + pformat(params))

        # ws obj info indices
        [OBJID_I, NAME_I, TYPE_I, SAVE_DATE_I, VERSION_I, SAVED_BY_I, WSID_I,
         WORKSPACE_I, CHSUM_I, SIZE_I, META_I] = range(11)  # object_info tuple

        #SERVICE_VER = 'dev'  # DEBUG
        SERVICE_VER = 'release'
        token = ctx['token']
        try:
            wsClient = workspaceService(self.workspaceURL, token=token)
        except:
            raise ValueError("unable to instantiate wsClient")
        headers = {'Authorization': 'OAuth ' + token}
        env = os.environ.copy()
        env['KB_AUTH_TOKEN'] = token

        # param checks
        required_params = ['workspace_name',
                           'input_featureSet_ref',
                           'genome_disp_name_config',
                           'namespace'
                           ]
        for arg in required_params:
            if arg not in params or params[arg] == None or params[arg] == '':
                raise ValueError("Must define required param: '" + arg + "'")

        if params['namespace'] != 'custom':
            if params.get('custom_target_fams') \
               and (params['custom_target_fams'].get('target_fams') \
                    or params['custom_target_fams'].get('extra_target_fam_groups_COG') \
                    or params['custom_target_fams'].get('extra_target_fam_groups_PFAM') \
                    or params['custom_target_fams'].get('extra_target_fam_groups_TIGR') \
                    or params['custom_target_fams'].get('extra_target_fam_groups_SEED')):

                self.log(console, "CUSTOM_TARGET_FAMS found.  Resetting NAMESPACE param to 'custom'")
                params['namespace'] = 'custom'
        else:
            if ('custom_target_fams' not in params or not params['custom_target_fams']) \
                or (
                    ('target_fams' not in params['custom_target_fams']
                     or not params['custom_target_fams']['target_fams'])
                and ('extra_target_fam_groups_COG' not in params['custom_target_fams'] or not params['custom_target_fams']['extra_target_fam_groups_COG'])
                and ('extra_target_fam_groups_PFAM' not in params['custom_target_fams'] or not params['custom_target_fams']['extra_target_fam_groups_PFAM'])
                and ('extra_target_fam_groups_TIGR' not in params['custom_target_fams'] or not params['custom_target_fams']['extra_target_fam_groups_TIGR'])
                and ('extra_target_fam_groups_SEED' not in params['custom_target_fams'] or not params['custom_target_fams']['extra_target_fam_groups_SEED'])
            ):
                error_msg = "If you select 'Custom' Domain Namespace, you must also Enable some Custom Domains or Custom Domain Groups"
                self.log (console, "ABORT: "+error_msg)
                raise ValueError("ABORT: "+error_msg)


        # base config
        namespace_classes = ['COG', 'PF', 'TIGR', 'SEED']
        show_blanks = False
        if 'show_blanks' in params and params['show_blanks'] == '1':
            show_blanks = True
        e_value_thresh = None
        if 'e_value' in params and params['e_value'] != None and params['e_value'] != '':
            e_value_thresh = float(params['e_value'])
        top_hit_flag = False
        if 'top_hit' in params and params['top_hit'] != None and params['top_hit'] != '' and params['top_hit'] != 0:
            top_hit_flag = True

        # set percentage required for annotated genes by each namespace
        required_annot_perc = dict()
        for namespace in namespace_classes:
            required_annot_perc[namespace] = 0.0
            if params.get('required_'+namespace+'_annot_perc'):
                required_annot_perc[namespace] = float(params.get('required_'+namespace+'_annot_perc'))


        # load provenance
        provenance = [{}]
        if 'provenance' in ctx:
            provenance = ctx['provenance']
        provenance[0]['input_ws_objects'] = [str(params['input_featureSet_ref'])]

        # set the output path
        timestamp = int((datetime.utcnow() - datetime.utcfromtimestamp(0)).total_seconds() * 1000)
        output_dir = os.path.join(self.scratch, 'output.' + str(timestamp))
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # configure categories
        #
        (cats, cat2name, cat2group, domfam2cat, cat2domfams, namespaces_reading, target_fams,
         extra_target_fams, extra_target_fam_groups, domfam2group, domfam2name) = self._configure_categories(params)

        # instantiate custom FeatureSets
        #
        features_by_custom_target_fam = dict()
        custom_target_fam_features_hit = False


        # STEP 1 - Get the Data
        # get genome set from featureSet
        #
        input_ref = params['input_featureSet_ref']
        try:
            input_obj_info = wsClient.get_object_info_new({'objects': [{'ref': input_ref}]})[0]
            input_obj_name = input_obj_info[NAME_I]
            input_obj_type = re.sub('-[0-9]+\.[0-9]+$', "", input_obj_info[TYPE_I])  # remove trailing version
        except Exception as e:
            raise ValueError('Unable to get object from workspace: (' + input_ref + ')' + str(e))
        accepted_input_types = ["KBaseCollections.FeatureSet"]
        if input_obj_type not in accepted_input_types:
            raise ValueError("Input object of type '" + input_obj_type +
                             "' not accepted.  Must be one of " + ", ".join(accepted_input_types))

        # get set obj
        try:
            featureSet_obj = wsClient.get_objects([{'ref': input_ref}])[0]['data']
        except:
            raise ValueError("unable to fetch featureSet: " + input_ref)

        # get genome refs, object names, sci names, protein-coding gene counts, and SEED annot
        #
        #genome_ids = genomeSet_obj['elements'].keys()  # note: genome_id may be meaningless
        genome_refs = []
        genome_ref_seen = dict()
        #for genome_id in genome_ids:
        #    genome_refs.append (genomeSet_obj['elements'][genome_id]['ref'])
        for element_id in featureSet_obj['elements'].keys():
            genome_ref = featureSet_obj['elements'][element_id][0]
            if genome_ref not in genome_ref_seen:
                genome_ref_seen[genome_ref] = True
                genome_refs.append(genome_ref)

        genome_ref_by_versionless = dict()
        for genome_ref in genome_refs:
            (ws_id, obj_id, version) = genome_ref.split('/')
            genome_ref_by_versionless[ws_id+'/'+obj_id] = genome_ref

        genome_obj_name_by_ref = dict()
        genome_sci_name_by_ref = dict()
        genome_CDS_count_by_ref = dict()
        uniq_genome_ws_ids = dict()
        domain_annot_obj_by_genome_ref = dict()

        dom_hits = dict()  # initialize dom_hits here because reading SEED within genome
        genes_with_hits_cnt = dict()
        genes_with_validated_vocab_hits_cnt = dict()

        for genome_ref in genome_refs:

            dom_hits[genome_ref] = dict()
            genes_with_hits_cnt[genome_ref] = dict()
            genes_with_validated_vocab_hits_cnt[genome_ref] = dict()

            # get genome object name
            input_ref = genome_ref
            try:
                input_obj_info = wsClient.get_object_info_new({'objects': [{'ref': input_ref}]})[0]
                input_obj_type = re.sub('-[0-9]+\.[0-9]+$', "", input_obj_info[TYPE_I])  # remove trailing version
                input_name = input_obj_info[NAME_I]
                if input_obj_info[WORKSPACE_I] != params['workspace_name']:
                    uniq_genome_ws_ids[input_obj_info[WSID_I]] = True

            except Exception as e:
                raise ValueError('Unable to get object from workspace: (' + input_ref + ')' + str(e))
            accepted_input_types = ["KBaseGenomes.Genome"]
            if input_obj_type not in accepted_input_types:
                raise ValueError("Input object of type '" + input_obj_type +
                                 "' not accepted.  Must be one of " + ", ".join(accepted_input_types))

            genome_obj_name_by_ref[genome_ref] = input_name

            try:
                genome_obj = wsClient.get_objects([{'ref': input_ref}])[0]['data']
            except:
                raise ValueError("unable to fetch genome: " + input_ref)

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

                    # filter out genes that aren't in featureSet
                    target_feature = False
                    #featureSet_element_id = genome_ref+self.genome_feature_id_delim+feature['id']
                    featureSet_element_id = feature['id']
                    gene_name = feature['id']
                    if featureSet_element_id in featureSet_obj['elements']:
                        target_feature = True

                    #if f_cnt % 100 == 0:
                    #    self.log (console, "iterating features: "+str(f_cnt))  # DEBUG

                    if 'protein_translation' in feature and feature['protein_translation'] != None and feature['protein_translation'] != '':
                        #if f_cnt % 100 == 0:
                        #    self.log (console, "prot: "+str(feature['protein_translation']))  # DEBUG

                        if self._check_SEED_function_defined_in_feature(feature):
                            #if f_cnt % 100 == 0:
                            #    self.log (console, "fxn: '"+str(feature['function'])+"'")  # DEBUG

                            # store assignments for gene
                            for namespace in ['SEED']:
                                if namespace not in genes_with_hits_cnt[genome_ref]:
                                    genes_with_hits_cnt[genome_ref][namespace] = 0
                                if namespace not in genes_with_validated_vocab_hits_cnt[genome_ref]:
                                    genes_with_validated_vocab_hits_cnt[genome_ref][namespace] = 0

                                if gene_name not in dom_hits[genome_ref]:
                                    dom_hits[genome_ref][gene_name] = dict()
                                    dom_hits[genome_ref][gene_name][namespace] = dict()

                                non_hypothetical_hit = False
                                validated_vocab = False
                                domfam_list = []
                                for annot in self._get_SEED_annotations(feature):
                                    for annot2 in annot.strip().split('@'):
                                        domfam = self._standardize_SEED_subsys_ID(annot2)
                                        domfam_list.append(domfam)
                                        if not 'hypothetical' in domfam:
                                            non_hypothetical_hit = True
                                        else:
                                            continue
                                        if domfam in domfam2cat[namespace]:
                                            validated_vocab = True
                                        #if f_cnt % 100 == 0:
                                        #    self.log (console, "domfam: '"+str(domfam)+"'")  # DEBUG

                                if params.get('count_hypothetical') and int(params.get('count_hypothetical')) == 1:
                                    genes_with_hits_cnt[genome_ref][namespace] += 1
                                elif non_hypothetical_hit:
                                    genes_with_hits_cnt[genome_ref][namespace] += 1
                                if validated_vocab:
                                    genes_with_validated_vocab_hits_cnt[genome_ref][namespace] += 1

                                """ OLD CODE
                                genes_with_hits_cnt[genome_ref][namespace] += 1

                                # THIS IS DIFFERENT
                                if not target_feature:
                                    continue

                                if gene_name not in dom_hits[genome_ref]:
                                    dom_hits[genome_ref][gene_name] = dict()
                                    dom_hits[genome_ref][gene_name][namespace] = dict()

                                domfam_list = []
                                for annot in self._get_SEED_annotations(feature):
                                    for annot2 in annot.strip().split('@'):
                                        domfam = self._standardize_SEED_subsys_ID(annot2)
                                        domfam_list.append(domfam)
                                        #if f_cnt % 100 == 0:
                                        #    self.log (console, "domfam: '"+str(domfam)+"'")  # DEBUG

                                """
                                if top_hit_flag:  # does SEED give more than one function?
                                    domfam_list = [domfam_list[0]]
                                for domfam in domfam_list:
                                    dom_hits[genome_ref][gene_name][namespace][domfam] = True
                                    if target_feature and domfam in target_fams:
                                        custom_target_fam_features_hit = True
                                        if domfam not in features_by_custom_target_fam:
                                            features_by_custom_target_fam[domfam] = dict()
                                        if genome_ref not in features_by_custom_target_fam[domfam]:
                                            features_by_custom_target_fam[domfam][genome_ref] = []
                                        features_by_custom_target_fam[domfam][genome_ref].append(gene_name)
                    #f_cnt += 1  # DEBUG


        # Make sure we have CDSs
        #
        missing_genes = []
        for genome_ref in genome_refs:
            if genome_CDS_count_by_ref[genome_ref] == 0:
                missing_genes.append("\t" + 'MISSING GENES FOR: ' + 'ref: '+genome_ref + ', obj_name: '+genome_obj_name_by_ref[genome_ref]+', sci_name: '+genome_sci_name_by_ref[genome_ref])
                missing_genes_by_genome_ref[genome_ref] = True
        if missing_genes:
            error_msg = "ABORT: Some of the Genomes are missing gene calls.  Please run RAST or Prokka App to get Genome objects with Gene calls for the following Genomes\n"
            error_msg += "\n".join(missing_genes)
            self.log(console, error_msg)
            raise ValueError(error_msg)


        # check for validated vocab if reading SEED
        #
        missing_SEED_annot_by_genome_ref = dict()
        missing_SEED_annot = []
        if 'SEED' in namespaces_reading:
            namespace = 'SEED'
            fraction_required_valid = required_annot_perc[namespace] / 100.0
            for genome_ref in genome_refs:
                self.log(console, "genome:"+genome_ref+" gene cnt with validated annot:"+str(genes_with_validated_vocab_hits_cnt[genome_ref][namespace])+" gene cnt with annot:"+str(genes_with_hits_cnt[genome_ref][namespace]))  # DEBUG

                valid_fraction = genes_with_validated_vocab_hits_cnt[genome_ref][namespace] / float(genes_with_hits_cnt[genome_ref][namespace])
                if valid_fraction < fraction_required_valid:
                    missing_SEED_annot.append("\t" + 'MISSING RAST SEED ANNOTATION FOR: ' + 'ref: '+genome_ref + ', obj_name: '+genome_obj_name_by_ref[genome_ref]+', sci_name: '+genome_sci_name_by_ref[genome_ref]+".  You can drop the threshold required in advanced parameters.")
                    missing_SEED_annot_by_genome_ref[genome_ref] = True

            if missing_SEED_annot:
                if len(missing_SEED_annot) == len(genome_refs):
                    error_msg = "ABORT: ALL genomes are missing RAST SEED Annotation.  You must run the RAST SEED Annotation App first\n"
                    error_msg += "\n".join(missing_SEED_annot)
                    self.log(console, error_msg)
                    raise ValueError(error_msg)

                # if strict, then abort
                if not params.get('skip_missing_genomes') or int(params.get('skip_missing_genomes')) != 1:
                    error_msg = "ABORT: You must run the RAST SEED Annotation App or use SKIP option on below genomes first\n"
                    error_msg += "\n".join(missing_SEED_annot)
                    self.log(console, error_msg)
                    raise ValueError(error_msg)
                # if skipping, then remove genomes with missing annotations
                else:
                    new_genome_refs = []
                    for genome_ref in genome_refs:
                        if genome_ref in missing_SEED_annot_by_genome_ref:
                            continue
                        new_genome_refs.append(genome_ref)
                    genome_refs = new_genome_refs
                    self.log(console, "SKIP option selected. If you wish to include the below Genomes, you must run the RAST SEED Annotation App first")
                    self.log(console, "\n".join(missing_SEED_annot))


        # determine if custom domains are not just SEED
        #
        search_domains_just_SEED = True
        for namespace in namespaces_reading.keys():
            if namespace != 'SEED':
                search_domains_just_SEED = False

        # read DomainAnnotation object to capture domain hits to genes within each namespace
        #
        if search_domains_just_SEED:
            self.log(console, "Search Domains just SEED.  Not looking for Domain Annotations")
        else:
            self.log(console, "Search Domains other than SEED.  Looking for Domain Annotations")
            dom_annot_found = dict()

            KBASE_DOMAINHIT_GENE_ID_I = 0
            KBASE_DOMAINHIT_GENE_BEG_I = 1  # not used
            KBASE_DOMAINHIT_GENE_END_I = 2  # not used
            KBASE_DOMAINHIT_GENE_STRAND_I = 3  # not used
            KBASE_DOMAINHIT_GENE_HITS_DICT_I = 4
            KBASE_DOMAINHIT_GENE_HITS_DICT_BEG_J = 0
            KBASE_DOMAINHIT_GENE_HITS_DICT_END_J = 1
            KBASE_DOMAINHIT_GENE_HITS_DICT_EVALUE_J = 2
            KBASE_DOMAINHIT_GENE_HITS_DICT_BITSCORE_J = 3
            KBASE_DOMAINHIT_GENE_HITS_DICT_ALNPERC_J = 4

            # DEBUG
            #for genome_ref in genome_refs:
            #    self.log (console, "SEED ANNOT CNT A: '"+str(genes_with_hits_cnt[genome_ref]['SEED'])+"'")

            dom_annot_obj_info_list = []
            # read local workspace first
            try:
                dom_annot_obj_info_list.extend(wsClient.list_objects(
                    {'workspaces': [params['workspace_name']], 'type': "KBaseGeneFamilies.DomainAnnotation"}))
            except Exception as e:
                raise ValueError("Unable to list DomainAnnotation objects from workspace: " +
                                 str(ws_id) + " " + str(e))
            # read any remaining remote workspaces
            for ws_id in uniq_genome_ws_ids.keys():
                try:
                    dom_annot_obj_info_list.extend(wsClient.list_objects(
                        {'ids': [ws_id], 'type': "KBaseGeneFamilies.DomainAnnotation"}))
                except Exception as e:
                    raise ValueError("Unable to list DomainAnnotation objects from workspace: " +
                                     str(ws_id) + " " + str(e))

            for info in dom_annot_obj_info_list:
                dom_annot_ref = str(info[WSID_I]) + '/' + str(info[OBJID_I]) + '/' + str(info[VERSION_I])
                try:
                    domain_data = wsClient.get_objects([{'ref': dom_annot_ref}])[0]['data']
                except:
                    raise ValueError("unable to fetch domain annotation: " + dom_annot_ref)

                # read domain data object
                genome_ref = domain_data['genome_ref']
                if params.get('enforce_genome_version_match') and int(params.get('enforce_genome_version_match')) == 1:
                    # skip extra domainannots
                    if genome_ref not in genome_refs:
                        continue
                else:
                    (ws_id, obj_id, version) = genome_ref.split('/')
                    genome_ref_versionless = ws_id+'/'+obj_id
                    # skip extra domainannots
                    if genome_ref_versionless not in genome_ref_by_versionless:
                        continue

                    # report any change in obj version
                    source_obj_type = 'FeatureSet'
                    source_genome_ref = genome_ref_by_versionless[ws_id+'/'+obj_id]
                    if genome_ref != source_genome_ref:
                        self.log(console, "DomainAnnotation object generated from different version of genome found in "+source_obj_type+".  DomainAnnotation for ref: "+genome_ref+" obj_name: "+genome_obj_name_by_ref[source_genome_ref]+" sci_name: "+genome_sci_name_by_ref[source_genome_ref]+" but using genome version from "+source_obj_type+" instead: "+source_genome_ref)
                    else:
                        self.log(console, "DomainAnnotation object generated from same version of genome ref: "+genome_ref+" obj_name: "+genome_obj_name_by_ref[genome_ref]+" sci_name: "+genome_sci_name_by_ref[genome_ref]+" as in "+source_obj_type)

                    genome_ref = source_genome_ref

                # avoid duplicate domain annotations
                dom_annot_found[genome_ref] = True
                if genome_ref not in domain_annot_obj_by_genome_ref:
                    domain_annot_obj_by_genome_ref[genome_ref] = dom_annot_ref
                    self.log(console, "DomainAnnotation object "+str(domain_annot_obj_by_genome_ref[genome_ref])+" being used for Genome obj_name: "+genome_obj_name_by_ref[genome_ref]+" sci_name: "+genome_sci_name_by_ref[genome_ref])
                else:
                    self.log(console, "DomainAnnotation object "+str(domain_annot_obj_by_genome_ref[genome_ref])+" already found for Genome obj_name: "+genome_obj_name_by_ref[genome_ref]+" sci_name: "+genome_sci_name_by_ref[genome_ref]+". Ignoring DomainAnnotation "+dom_annot_ref)
                    continue

                if genome_ref not in dom_hits:
                    dom_hits[genome_ref] = dict()

                if genome_ref not in genes_with_hits_cnt:
                    genes_with_hits_cnt[genome_ref] = dict()

                for scaffold_id_iter in domain_data['data'].keys():
                    for CDS_domain_list in domain_data['data'][scaffold_id_iter]:
                        gene_ID = CDS_domain_list[KBASE_DOMAINHIT_GENE_ID_I]
                        #gene_name = re.sub ('^'+genome_object_name+'.', '', gene_ID)
                        gene_name = gene_ID
                        #(contig_name, gene_name) = (gene_ID[0:gene_ID.index(".")], gene_ID[gene_ID.index(".")+1:])
                        #print ("DOMAIN_HIT: "+contig_name+" "+gene_name)  # DEBUG
                        #print ("DOMAIN_HIT for gene: "+gene_name)  # DEBUG
                        #gene_beg       = CDS_domain_list[KBASE_DOMAINHIT_GENE_BEG_I]
                        #gene_end       = CDS_domain_list[KBASE_DOMAINHIT_GENE_END_I]
                        #gene_strand    = CDS_domain_list[KBASE_DOMAINHIT_GENE_STRAND_I]
                        gene_hits_dict = CDS_domain_list[KBASE_DOMAINHIT_GENE_HITS_DICT_I]

                        # filter out genes that aren't in featureSet
                        target_feature = False
                        #featureSet_element_id = genome_ref+self.genome_feature_id_delim+feature['id']
                        featureSet_element_id = gene_ID
                        if featureSet_element_id in featureSet_obj['elements']:
                            target_feature = True

                        # init dom hits storage
                        dom_hits_by_namespace = dict()
                        top_hit_evalue_by_namespace = dict()
                        top_hit_dom_by_namespace = dict()

                        for namespace in namespace_classes:
                            dom_hits_by_namespace[namespace] = dict()
                            top_hit_evalue_by_namespace[namespace] = 100
                            top_hit_dom_by_namespace[namespace] = None

                        for domfam in gene_hits_dict.keys():
                            if domfam.startswith('PF'):
                                domfam_clean = re.sub('\.[^\.]*$', '', domfam)
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
                                beg = int(hit[KBASE_DOMAINHIT_GENE_HITS_DICT_BEG_J])
                                end = int(hit[KBASE_DOMAINHIT_GENE_HITS_DICT_END_J])
                                e_value = float(hit[KBASE_DOMAINHIT_GENE_HITS_DICT_EVALUE_J])
                                bit_score = float(hit[KBASE_DOMAINHIT_GENE_HITS_DICT_BITSCORE_J])
                                aln_perc = float(hit[KBASE_DOMAINHIT_GENE_HITS_DICT_ALNPERC_J])

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

                                # filter out genes that aren't in featureSet
                                #featureSet_element_id = genome_ref+self.genome_feature_id_delim+gene_ID
                                featureSet_element_id = gene_ID
                                if featureSet_element_id not in featureSet_obj['elements']:
                                    continue

                                if gene_name not in dom_hits[genome_ref]:
                                    dom_hits[genome_ref][gene_name] = dict()

                                if top_hit_flag:
                                    dom_hits[genome_ref][gene_name][namespace] = {
                                        top_hit_dom_by_namespace[namespace]: True}
                                else:
                                    dom_hits[genome_ref][gene_name][namespace] = dom_hits_by_namespace[namespace]

                                # store for featureset
                                for domfam in dom_hits[genome_ref][gene_name][namespace].keys():
                                    if target_feature and domfam in target_fams:
                                        custom_target_fam_features_hit = True
                                        if domfam not in features_by_custom_target_fam:
                                            features_by_custom_target_fam[domfam] = dict()
                                        if genome_ref not in features_by_custom_target_fam[domfam]:
                                            features_by_custom_target_fam[domfam][genome_ref] = []
                                        features_by_custom_target_fam[domfam][genome_ref].append(gene_name)


            # make sure we have domain annotations for all genomes
            missing_annot = []
            missing_dom_annot_by_genome_ref = dict()
            for genome_ref in genome_refs:
                if genome_ref not in dom_annot_found:
                    missing_annot.append("\t" + 'MISSING DOMAIN ANNOTATION FOR: ' + 'ref: '+genome_ref + ', obj_name: '+genome_obj_name_by_ref[genome_ref]+', sci_name: '+genome_sci_name_by_ref[genome_ref])
                    missing_dom_annot_by_genome_ref[genome_ref] = True

            if missing_annot:
                if len(missing_annot) == len(genome_refs):
                    error_msg = "ABORT: ALL genomes have no matching Domain Annotation.  You must run the 'Domain Annotation' App first\n"
                    error_msg += "\n".join(missing_annot)
                    self.log(console, error_msg)
                    raise ValueError(error_msg)

                # if strict, then abort
                if not params.get('skip_missing_genomes') or int(params.get('skip_missing_genomes')) != 1:
                    error_msg = "ABORT: You must run the 'Domain Annotation' App or use SKIP option on below genomes first\n"
                    error_msg += "\n".join(missing_annot)
                    self.log(console, error_msg)
                    raise ValueError(error_msg)
                # if skipping, then remove genomes with missing annotations
                else:
                    new_genome_refs = []
                    for genome_ref in genome_refs:
                        if genome_ref in missing_dom_annot_by_genome_ref:
                            continue
                        new_genome_refs.append(genome_ref)
                    genome_refs = new_genome_refs
                    self.log(console, "SKIP option selected. If you wish to include the below Genomes, you must run the 'Domain Annotation' App first")
                    self.log(console, "\n".join(missing_annot))

        # DEBUG
        #for genome_ref in genome_refs:
        #    self.log (console, "SEED ANNOT CNT B: '"+str(genes_with_hits_cnt[genome_ref]['SEED'])+"'")

        # Alert user for any genomes that are missing annotations in a requested namespace
        #   this can happen even with a DomainAnnotation object if the namespace was skipped
        #
        inadequate_annot = []
        inadequate_annot_by_genome_ref = dict()
        for genome_ref in genome_refs:
            total_genes = genome_CDS_count_by_ref[genome_ref]

            for namespace in sorted(namespaces_reading.keys()):
                fraction_requiring_annotation = required_annot_perc[namespace] / 100.0
                if namespace == 'SEED':
                    annotation_tool = 'RAST Genome Annotation App'
                else:
                    annotation_tool = 'Domain Annotation App'
                if genes_with_hits_cnt[genome_ref][namespace] < fraction_requiring_annotation * total_genes:
                    inadequate_annot.append("\t" + 'INADEQUATE DOMAIN ANNOTATION FOR: ' + 'ref: '+genome_ref + ', obj_name: '+genome_obj_name_by_ref[genome_ref]+', sci_name: '+genome_sci_name_by_ref[genome_ref]+".  Namespace: "+namespace+" found in "+str(genes_with_hits_cnt[genome_ref][namespace])+" of a total of "+str(total_genes)+".  "+str(required_annot_perc[namespace])+"% were configured in advanced parameter input required to be annotated by "+namespace+".  Something may have gone wrong with "+annotation_tool+".  Try rerunning or dropping the threshold required in advanced parameters.")
                    inadequate_annot_by_genome_ref[genome_ref] = True

            if inadequate_annot:
                if len(inadequate_annot) == len(genome_refs):
                    error_msg = "ABORT: ALL genomes have poor Domain Annotation.  You must run the 'Domain Annotation' App first\n"
                    error_msg += "\n".join(inadequate_annot)
                    self.log(console, error_msg)
                    raise ValueError(error_msg)

                # if strict, then abort
                if not params.get('skip_missing_genomes') or int(params.get('skip_missing_genomes')) != 1:
                    error_msg = "ABORT: You must run the 'Domain Annotation' App or use SKIP option on below genomes first\n"
                    error_msg += "\n".join(inadequate_annot)
                    self.log(console, error_msg)
                    raise ValueError(error_msg)
                # if skipping, then remove genomes with missing annotations
                else:
                    new_genome_refs = []
                    for genome_ref in genome_refs:
                        if genome_ref in inadequate_annot_by_genome_ref:
                            continue
                        new_genome_refs.append(genome_ref)
                    genome_refs = new_genome_refs
                    self.log(console, "SKIP option selected. If you wish to include the below Genomes, you must run the 'Domain Annotation' App first")
                    self.log(console, "\n".join(inadequate_annot))


        # STEP 2 - Analysis
        # calculate table
        #
        table_data = dict()
        INSANE_VALUE = 10000000000000000
        overall_low_val = INSANE_VALUE
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
                        namespace = re.sub('\d*$', '', cat)
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
                                namespace = re.sub('\d*$', '', cat)
                        else:
                            namespace = params['namespace']
                        total_genes = genes_with_hits_cnt[genome_ref][namespace]
                    else:
                        total_genes = genome_CDS_count_by_ref[genome_ref]

                    if total_genes > 0:
                        table_data[genome_ref][cat] /= float(total_genes)
                        table_data[genome_ref][cat] *= 100.0
                    else:
                        table_data[genome_ref][cat] = 0

        # determine high and low val
        for genome_ref in genome_refs:
            for cat in cats:
                val = table_data[genome_ref][cat]
                if val == 0:
                    continue
                #self.log (console, "HIGH VAL SCAN CAT: '"+cat+"' VAL: '"+str(val)+"'")  # DEBUG
                if 'log_base' in params and params['log_base'] != None and params['log_base'] != '':
                    log_base = float(params['log_base'])
                    if log_base <= 1.0:
                        raise ValueError("log base must be > 1.0")
                    val = math.log(val, log_base)
                if val > overall_high_val:
                    overall_high_val = val
                if val < overall_low_val:
                    overall_low_val = val
        if overall_high_val == -INSANE_VALUE:
            raise ValueError("unable to find any counts")

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


        # STEP 3 - Create and save featureSets
        #
        objects_created = []
        if custom_target_fam_features_hit:
            featureSet_by_custom_target_fam = dict()
            for target_fam in sorted(features_by_custom_target_fam.keys()):
                featureSet_by_custom_target_fam[target_fam] = dict()
                for genome_ref in sorted(features_by_custom_target_fam[target_fam].keys()):
                    for fid in sorted(features_by_custom_target_fam[target_fam][genome_ref]):
                        if fid in featureSet_by_custom_target_fam[target_fam]:
                            featureSet_by_custom_target_fam[target_fam][fid].append(genome_ref)
                        else:
                            featureSet_by_custom_target_fam[target_fam][fid] = [genome_ref]

                fs_name = target_fam+'-'+input_obj_name+'.FeatureSet'
                fs_desc = 'Hits by '+target_fam+' to '+input_obj_name
                fs_obj = {'description': fs_desc,
                          'elements': featureSet_by_custom_target_fam[target_fam]
                         }
                new_obj_info = wsClient.save_objects({
                    'workspace': params['workspace_name'],
                    'objects': [
                        {'type': 'KBaseCollections.FeatureSet',
                         'data': fs_obj,
                         'name': fs_name,
                         'meta': {},
                         'provenance': provenance
                         }]
                })[0]
                objects_created.append(
                    {'ref': str(new_obj_info[6]) + '/' + str(new_obj_info[0]) + '/' + str(new_obj_info[4]), 'description': fs_desc})
                featureSet_by_custom_target_fam[target_fam] = {}  # free memory
                fs_obj = {}  # free memory


        # STEP 4 - build report
        #
        reportName = 'kb_phylogenomics_report_' + str(uuid.uuid4())
        reportObj = {'objects_created': objects_created,
                     'direct_html_link_index': 0,
                     'file_links': [],
                     'html_links': [],
                     'workspace_name': params['workspace_name'],
                     'report_object_name': reportName
                     }

        # build html report
        sp = '&nbsp;'
        text_color = "#606060"
        text_color_2 = "#606060"
        head_color_1 = "#eeeeee"
        head_color_2 = "#eeeeee"
        border_color = "#cccccc"
        border_cat_color = "#ffccff"
        #graph_color = "lightblue"
        #graph_width = 100
        #graph_char = "."
        graph_char = sp
        color_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e']
        max_color = len(color_list) - 1
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
        if len(group_order) > 0:
            show_groups = True

        # sort genomes by display name
        genome_ref_by_disp_name = dict()
        for genome_ref in genome_refs:
            genome_obj_name = genome_obj_name_by_ref[genome_ref]
            genome_sci_name = genome_sci_name_by_ref[genome_ref]
            [ws_id, obj_id, genome_obj_version] = genome_ref.split('/')
            genome_disp_name = ''
            if 'obj_name' in params.get('genome_disp_name_config'):
                genome_disp_name += genome_obj_name
                if 'ver' in params.get('genome_disp_name_config'):
                    genome_disp_name += '.v'+str(genome_obj_version)

                if 'sci_name' in params.get('genome_disp_name_config'):
                    genome_disp_name += ': '+genome_sci_name
            else:
                genome_disp_name = genome_sci_name

            if genome_disp_name in genome_ref_by_disp_name:
                error_msg = "duplicate genome display names.  Can be fixed by adding genome object name to report"
                self.log (console, "ABORT: "+error_msg)
                raise ValueError ("ABORT: "+error_msg)

            genome_ref_by_disp_name[genome_disp_name] = genome_ref

        # html report buffer
        html_report_lines = []
        html_report_lines += ['<html>']
        html_report_lines += ['<head>']
        html_report_lines += ['<title>KBase Functional Domain Profile</title>']
        html_report_lines += ['<style>']
        html_report_lines += [
            ".vertical-text {\ndisplay: inline-block;\noverflow: hidden;\nwidth: 0.65em;\n}\n.vertical-text__inner {\ndisplay: inline-block;\nwhite-space: nowrap;\nline-height: 1.1;\ntransform: translate(0,100%) rotate(-90deg);\ntransform-origin: 0 0;\n}\n.vertical-text__inner:after {\ncontent: \"\";\ndisplay: block;\nmargin: 0.0em 0 100%;\n}"]
        html_report_lines += [
            ".vertical-text_title {\ndisplay: inline-block;\noverflow: hidden;\nwidth: 1.0em;\n}\n.vertical-text__inner_title {\ndisplay: inline-block;\nwhite-space: nowrap;\nline-height: 1.0;\ntransform: translate(0,100%) rotate(-90deg);\ntransform-origin: 0 0;\n}\n.vertical-text__inner_title:after {\ncontent: \"\";\ndisplay: block;\nmargin: 0.0em 0 100%;\n}"]
        html_report_lines += ['</style>']
        html_report_lines += ['</head>']
        html_report_lines += ['<body bgcolor="white">']

        # genomes as rows
        if 'vertical' in params and params['vertical'] == "1":
            # table header
            html_report_lines += ['<table cellpadding=' + graph_padding +
                                  ' cellspacing=' + graph_spacing + ' border=' + border + '>']
            corner_rowspan = "1"
            if show_groups:
                corner_rowspan = "2"
            label = ''
            if params['namespace'] != 'custom':
                label = params['namespace']
                if label == 'PF':
                    label = 'PFAM'
                elif label == 'TIGR':
                    label = 'TIGRFAM'
            html_report_lines += ['<tr><td valign=bottom align=right rowspan=' + corner_rowspan +
                                  '><div class="vertical-text_title"><div class="vertical-text__inner_title"><font color="' + text_color + '">' + label + '</font></div></div></td>']

            # group headers
            if show_groups:
                for cat_group in group_order:
                    if cat_group.startswith('SEED'):
                        cat_group_disp = re.sub('_', ' ', cat_group)
                    else:
                        cat_group_disp = cat_group
                    cat_group_words = cat_group_disp.split()
                    max_group_width = 3 * group_size[cat_group]
                    if len(cat_group) > max_group_width:
                        new_cat_group_words = []
                        sentence_len = 0
                        for w_i, word in enumerate(cat_group_words):
                            new_cat_group_words.append(word)
                            sentence_len += len(word)
                            if w_i < len(cat_group_words) - 1:
                                if sentence_len + 1 + len(cat_group_words[w_i + 1]) > max_group_width:
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
                        html_report_lines += ['<td bgcolor=white colspan=' + str(group_size[cat_group]) + '></td>']
                    else:
                        html_report_lines += ['<td style="border-right:solid 2px ' + border_cat_color + '; border-bottom:solid 2px ' + border_cat_color + '" bgcolor="' + head_color_1 +
                                              '"valign=middle align=center colspan=' + str(group_size[cat_group]) + '><font color="' + text_color + '" size=' + str(graph_cat_fontsize) + '><b>' + cat_group_disp + '</b></font></td>']

                html_report_lines += ['</tr><tr>']

            # column headers
            for cat in cats:
                if not cat_seen[cat] and not show_blanks:
                    continue
                if params['namespace'] == 'custom':
                    if cat.startswith('SEED'):
                        namespace = 'SEED'
                    else:
                        namespace = re.sub("\d*$", "", cat)
                    cell_title = domfam2name[namespace][cat].strip()
                    cat_disp = cat
                    cat_disp = re.sub('^SEED', 'SEED:', cat_disp)
                else:
                    cell_title = cat2name[params['namespace']][cat].strip()
                    cat_disp = cat
                    cat_disp = re.sub("TIGR_", "", cat_disp)
                if len(cat_disp) > cat_disp_trunc_len + 1:
                    cat_disp = cat_disp[0:cat_disp_trunc_len] + '*'
                html_report_lines += ['<td style="border-right:solid 2px ' + border_cat_color + '; border-bottom:solid 2px ' +
                                      border_cat_color + '" bgcolor="' + head_color_2 + '"title="' + cell_title + '" valign=bottom align=center>']
                if params['namespace'] != 'COG':
                    html_report_lines += ['<div class="vertical-text"><div class="vertical-text__inner">']
                html_report_lines += ['<font color="' + text_color_2 + '" size=' + graph_cat_fontsize + '><b>']
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
            for genome_disp_name in sorted(genome_ref_by_disp_name.keys()):
                genome_ref = genome_ref_by_disp_name[genome_disp_name]

                html_report_lines += ['<tr>']
                html_report_lines += ['<td align=right><font color="' + text_color + '" size=' +
                                      graph_gen_fontsize + '><b><nobr>' + genome_disp_name + '</nobr></b></font></td>']
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
                                raise ValueError("log base must be > 1.0")
                            val = math.log(val, log_base)
                        if overall_high_val == overall_low_val:
                            denom = 1.0
                        else:
                            denom = float(overall_high_val - overall_low_val)
                        cell_color_i = max_color - \
                                      int(round(max_color * (val - overall_low_val) / denom))
                        c = color_list[cell_color_i]
                        cell_color = '#' + c + c + c + c + 'FF'

                    if params['count_category'].startswith('perc'):
                        cell_val = str("%.3f" % table_data[genome_ref][cat])
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
                        html_report_lines += ['<td align=center valign=middle title="' + cell_val + '" style="width:' + cell_width + '" bgcolor="' +
                                              cell_color + '"><font color="' + this_text_color + '" size=' + cell_fontsize + '>' + this_graph_char + '</font></td>']
                    else:
                        html_report_lines += ['<td align=center valign=middle style="' + cell_width + '; border-right:solid 2px ' + border_color +
                                              '; border-bottom:solid 2px ' + border_color + '"><font color="' + text_color + '" size=' + cell_fontsize + '>' + cell_val + '</font></td>']

                html_report_lines += ['</tr>']
            html_report_lines += ['</table>']

        # genomes as columns
        else:
            raise ValueError("Do not yet support Genomes as columns")

        # key table
        html_report_lines += ['<p>']
        html_report_lines += ['<table cellpadding=3 cellspacing=2 border=' + border + '>']
        html_report_lines += ['<tr><td valign=middle align=left colspan=3 style="border-bottom:solid 4px ' +
                              border_color + '"><font color="' + text_color + '"><b>KEY</b></font></td></tr>']

        if show_groups:
            group_cat_i = 0
            for cat_group in group_order_with_blanks:
                if cat_group.startswith('SEED'):
                    cat_group_disp = re.sub('_', ' ', cat_group)
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
                    html_report_lines += ['<td bgcolor=white rowspan=' + str(
                        group_size_with_blanks[cat_group]) + ' style="border-right:solid 4px ' + border_color + '"></td>']
                else:
                    html_report_lines += ['<td style="border-right:solid 4px ' + border_color + '" valign=top align=right rowspan=' + str(
                        group_size_with_blanks[cat_group]) + '><font color="' + text_color + '" size=' + str(graph_cat_fontsize) + '><b>' + cat_group_disp + '</b></font></td>']

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
                        namespace = re.sub('\d*$', '', first_cat)
                    cat_disp = re.sub('^SEED', 'SEED:', first_cat)
                    desc = domfam2name[namespace][domfam]
                else:
                    namespace = params['namespace']
                    cat_disp = first_cat
                    desc = cat2name[namespace][first_cat]
                if len(cat_disp) > cat_disp_trunc_len + 1:
                    cat_disp = cat_disp[0:cat_disp_trunc_len] + '*'
                cat_disp = sp + cat_disp

                html_report_lines += ['<td valign=middle align=left bgcolor="' + cell_color + '" style="border-right:solid 4px ' +
                                      border_color + '"><font color="' + text_color + '" size=' + graph_cat_fontsize + '>' + cat_disp + '</font></td>']
                html_report_lines += ['<td valign=middle align=left bgcolor="' + cell_color + '"><font color="' +
                                      text_color + '" size=' + graph_cat_fontsize + '>' + sp + desc + '</font></td>']
                html_report_lines += ['</tr>']

                group_cat_i += 1

                # add rest of cats in group
                for c_i in range(group_cat_i, group_cat_i + group_size_with_blanks[cat_group] - 1):
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
                            namespace = re.sub('\d*$', '', cat)
                        cat_disp = re.sub('^SEED', 'SEED:', cat)
                        desc = domfam2name[namespace][domfam]
                    else:
                        namespace = params['namespace']
                        cat_disp = cat
                        desc = cat2name[namespace][cat]
                    if len(cat_disp) > cat_disp_trunc_len + 1:
                        cat_disp = cat_disp[0:cat_disp_trunc_len] + '*'
                    cat_disp = sp + cat_disp

                    html_report_lines += ['<tr>']
                    html_report_lines += ['<td valign=middle align=left bgcolor="' + cell_color + '" style="border-right:solid 4px ' +
                                          border_color + '"><font color="' + text_color + '" size=' + graph_cat_fontsize + '>' + cat_disp + '</font></td>']
                    html_report_lines += ['<td valign=middle align=left bgcolor="' + cell_color + '"><font color="' +
                                          text_color + '" size=' + graph_cat_fontsize + '>' + sp + desc + '</font></td>']
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
                        namespace = re.sub('\d*$', '', domfam)
                    cat_disp = re.sub('^SEED', 'SEED:', cat)
                    desc = domfam2name[namespace][domfam]
                else:
                    namespace = params['namespace']
                    cat_disp = cat
                    desc = cat2name[namespace][cat]
                if len(cat_disp) > cat_disp_trunc_len + 1:
                    cat_disp = cat_disp[0:cat_disp_trunc_len] + '*'
                html_report_lines += ['<tr>']
                html_report_lines += ['<td valign=middle align=left bgcolor="' + cell_color + '" style="border-right:solid 4px ' +
                                      border_color + '><font color="' + text_color + '" size=' + graph_cat_fontsize + '>' + cat_disp + '</font></td>']
                html_report_lines += ['<td valign=middle align=left bgcolor="' + cell_color +
                                      '"><font color="' + text_color + '" size=' + graph_cat_fontsize + '>' + desc + '</font></td>']
                html_report_lines += ['</tr>']

        html_report_lines += ['</table>']

        # close
        html_report_lines += ['</body>']
        html_report_lines += ['</html>']

        html_report_str = "\n".join(html_report_lines)
        #reportObj['direct_html'] = html_report_str

        # write html to file and upload
        html_file = os.path.join(output_dir, 'domain_profile_report.html')
        with open(html_file, 'w', 0) as html_handle:
            html_handle.write(html_report_str)
        dfu = DFUClient(self.callbackURL)
        try:
            upload_ret = dfu.file_to_shock({'file_path': html_file,
                                            'make_handle': 0,
                                            'pack': 'zip'})
        except:
            raise ValueError('Logging exception loading html_report to shock')

        reportObj['html_links'] = [{'shock_id': upload_ret['shock_id'],
                                    'name': 'domain_profile_report.html',
                                    'label': 'Functional Domain Profile report'}
                                   ]

        # save report object
        #
        reportClient = KBaseReport(self.callbackURL, token=ctx['token'], service_ver=SERVICE_VER)
        #report_info = report.create({'report':reportObj, 'workspace_name':params['workspace_name']})
        report_info = reportClient.create_extended_report(reportObj)

        output = {'report_name': report_info['name'], 'report_ref': report_info['ref']}

        #END view_fxn_profile_featureSet

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method view_fxn_profile_featureSet return value ' +
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
           "genome_disp_name_config" of String, parameter "count_category" of
           String, parameter "heatmap" of type "bool", parameter "vertical"
           of type "bool", parameter "top_hit" of type "bool", parameter
           "e_value" of Double, parameter "log_base" of Double, parameter
           "required_COG_annot_perc" of Double, parameter
           "required_PFAM_annot_perc" of Double, parameter
           "required_TIGR_annot_perc" of Double, parameter
           "required_SEED_annot_perc" of Double, parameter
           "count_hypothetical" of type "bool", parameter "show_blanks" of
           type "bool", parameter "skip_missing_genomes" of type "bool",
           parameter "enforce_genome_version_match" of type "bool"
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
        self.log(console, "\n" + pformat(params))

        # ws obj info indices
        [OBJID_I, NAME_I, TYPE_I, SAVE_DATE_I, VERSION_I, SAVED_BY_I, WSID_I,
         WORKSPACE_I, CHSUM_I, SIZE_I, META_I] = range(11)  # object_info tuple

        #SERVICE_VER = 'dev'  # DEBUG
        SERVICE_VER = 'release'
        token = ctx['token']
        try:
            wsClient = workspaceService(self.workspaceURL, token=token)
        except:
            raise ValueError("unable to instantiate wsClient")
        headers = {'Authorization': 'OAuth ' + token}
        env = os.environ.copy()
        env['KB_AUTH_TOKEN'] = token

        # param checks
        required_params = ['workspace_name',
                           'input_speciesTree_ref',
                           'genome_disp_name_config',
                           'namespace'
                           ]
        for arg in required_params:
            if arg not in params or params[arg] == None or params[arg] == '':
                raise ValueError("Must define required param: '" + arg + "'")

        if params['namespace'] != 'custom':
            if params.get('custom_target_fams') \
               and (params['custom_target_fams'].get('target_fams') \
                    or params['custom_target_fams'].get('extra_target_fam_groups_COG') \
                    or params['custom_target_fams'].get('extra_target_fam_groups_PFAM') \
                    or params['custom_target_fams'].get('extra_target_fam_groups_TIGR') \
                    or params['custom_target_fams'].get('extra_target_fam_groups_SEED')):

                self.log(console, "CUSTOM_TARGET_FAMS found.  Resetting NAMESPACE param to 'custom'")
                params['namespace'] = 'custom'
        else:
            if ('custom_target_fams' not in params or not params['custom_target_fams']) \
                or (
                    ('target_fams' not in params['custom_target_fams']
                     or not params['custom_target_fams']['target_fams'])
                and ('extra_target_fam_groups_COG' not in params['custom_target_fams'] or not params['custom_target_fams']['extra_target_fam_groups_COG'])
                and ('extra_target_fam_groups_PFAM' not in params['custom_target_fams'] or not params['custom_target_fams']['extra_target_fam_groups_PFAM'])
                and ('extra_target_fam_groups_TIGR' not in params['custom_target_fams'] or not params['custom_target_fams']['extra_target_fam_groups_TIGR'])
                and ('extra_target_fam_groups_SEED' not in params['custom_target_fams'] or not params['custom_target_fams']['extra_target_fam_groups_SEED'])
            ):
                error_msg = "If you select 'Custom' Domain Namespace, you must also Enable some Custom Domains or Custom Domain Groups"
                self.log (console, "ABORT: "+error_msg)
                raise ValueError("ABORT: "+error_msg)


        # base config
        namespace_classes = ['COG', 'PF', 'TIGR', 'SEED']
        show_blanks = False
        if 'show_blanks' in params and params['show_blanks'] == '1':
            show_blanks = True
        e_value_thresh = None
        if 'e_value' in params and params['e_value'] != None and params['e_value'] != '':
            e_value_thresh = float(params['e_value'])
        top_hit_flag = False
        if 'top_hit' in params and params['top_hit'] != None and params['top_hit'] != '' and params['top_hit'] != 0:
            top_hit_flag = True

        # set percentage required for annotated genes by each namespace
        required_annot_perc = dict()
        for namespace in namespace_classes:
            required_annot_perc[namespace] = 0.0
            if params.get('required_'+namespace+'_annot_perc'):
                required_annot_perc[namespace] = float(params.get('required_'+namespace+'_annot_perc'))


        # load provenance
        provenance = [{}]
        if 'provenance' in ctx:
            provenance = ctx['provenance']
        provenance[0]['input_ws_objects'] = [str(params['input_speciesTree_ref'])]

        # set the output paths
        timestamp = int((datetime.utcnow() - datetime.utcfromtimestamp(0)).total_seconds() * 1000)
        output_dir = os.path.join(self.scratch, 'output.' + str(timestamp))
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        html_output_dir = os.path.join(output_dir, 'html_output')
        if not os.path.exists(html_output_dir):
            os.makedirs(html_output_dir)

        # configure categories
        #
        (cats, cat2name, cat2group, domfam2cat, cat2domfams, namespaces_reading, target_fams,
         extra_target_fams, extra_target_fam_groups, domfam2group, domfam2name) = self._configure_categories(params)

        # instantiate custom FeatureSets
        #
        features_by_custom_target_fam = dict()
        custom_target_fam_features_hit = False


        # STEP 1 - Get the Data
        # get speciesTree
        #
        input_ref = params['input_speciesTree_ref']
        speciesTree_name = None
        try:
            input_obj_info = wsClient.get_object_info_new({'objects': [{'ref': input_ref}]})[0]
            input_obj_name = input_obj_info[NAME_I]
            input_obj_type = re.sub('-[0-9]+\.[0-9]+$', "", input_obj_info[TYPE_I])  # remove trailing version
            speciesTree_name = input_obj_info[NAME_I]
        except Exception as e:
            raise ValueError('Unable to get object from workspace: (' + input_ref + ')' + str(e))
        accepted_input_types = ["KBaseTrees.Tree"]
        if input_obj_type not in accepted_input_types:
            raise ValueError("Input object of type '" + input_obj_type +
                             "' not accepted.  Must be one of " + ", ".join(accepted_input_types))

        # get set obj
        try:
            speciesTree_obj = wsClient.get_objects([{'ref': input_ref}])[0]['data']
        except:
            raise ValueError("unable to fetch speciesTree: " + input_ref)

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

        genome_ref_by_versionless = dict()
        for genome_ref in genome_refs:
            (ws_id, obj_id, version) = genome_ref.split('/')
            genome_ref_by_versionless[ws_id+'/'+obj_id] = genome_ref

        # get object names, sci names, protein-coding gene counts, and SEED annot
        #
        genome_obj_name_by_ref = dict()
        genome_obj_name_by_id = dict()
        genome_sci_name_by_ref = dict()
        genome_sci_name_by_id = dict()
        genome_CDS_count_by_ref = dict()
        uniq_genome_ws_ids = dict()
        domain_annot_obj_by_genome_ref = dict()

        dom_hits = dict()  # initialize dom_hits here because reading SEED within genome
        genes_with_hits_cnt = dict()
        genes_with_validated_vocab_hits_cnt = dict()  # only used for SEED at this time

        for genome_ref in genome_refs:

            dom_hits[genome_ref] = dict()
            genes_with_hits_cnt[genome_ref] = dict()
            genes_with_validated_vocab_hits_cnt[genome_ref] = dict()

            # get genome object name
            input_ref = genome_ref
            try:
                input_obj_info = wsClient.get_object_info_new({'objects': [{'ref': input_ref}]})[0]
                input_obj_type = re.sub('-[0-9]+\.[0-9]+$', "", input_obj_info[TYPE_I])  # remove trailing version
                input_name = input_obj_info[NAME_I]
                if input_obj_info[WORKSPACE_I] != params['workspace_name']:
                    uniq_genome_ws_ids[input_obj_info[WSID_I]] = True

            except Exception as e:
                raise ValueError('Unable to get object from workspace: (' + input_ref + ')' + str(e))
            accepted_input_types = ["KBaseGenomes.Genome"]
            if input_obj_type not in accepted_input_types:
                raise ValueError("Input object of type '" + input_obj_type +
                                 "' not accepted.  Must be one of " + ", ".join(accepted_input_types))

            genome_obj_name_by_ref[genome_ref] = input_name
            genome_obj_name_by_id[genome_id_by_ref[genome_ref]] = input_name

            try:
                genome_obj = wsClient.get_objects([{'ref': input_ref}])[0]['data']
            except:
                raise ValueError("unable to fetch genome: " + input_ref)

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

                        if self._check_SEED_function_defined_in_feature(feature):
                            gene_name = feature['id']

                            #if f_cnt % 100 == 0:
                            #    self.log (console, "fxn: '"+str(feature['function'])+"'")  # DEBUG

                            # store assignments for gene
                            for namespace in ['SEED']:
                                if namespace not in genes_with_hits_cnt[genome_ref]:
                                    genes_with_hits_cnt[genome_ref][namespace] = 0
                                if namespace not in genes_with_validated_vocab_hits_cnt[genome_ref]:
                                    genes_with_validated_vocab_hits_cnt[genome_ref][namespace] = 0

                                if gene_name not in dom_hits[genome_ref]:
                                    dom_hits[genome_ref][gene_name] = dict()
                                    dom_hits[genome_ref][gene_name][namespace] = dict()

                                non_hypothetical_hit = False
                                validated_vocab = False
                                domfam_list = []
                                for annot in self._get_SEED_annotations(feature):
                                    for annot2 in annot.strip().split('@'):
                                        domfam = self._standardize_SEED_subsys_ID(annot2)
                                        domfam_list.append(domfam)
                                        if not 'hypothetical' in domfam:
                                            non_hypothetical_hit = True
                                        else:
                                            continue
                                        if domfam in domfam2cat[namespace]:
                                            validated_vocab = True
                                        # DEBUG
                                        #else:
                                        #    self.log(console, "genome:"+genome_ref+" not recognizing function: "+domfam)

                                        #if f_cnt % 100 == 0:
                                        #    self.log (console, "domfam: '"+str(domfam)+"'")  # DEBUG
                                if params.get('count_hypothetical') and int(params.get('count_hypothetical')) == 1:
                                    genes_with_hits_cnt[genome_ref][namespace] += 1
                                elif non_hypothetical_hit:
                                    genes_with_hits_cnt[genome_ref][namespace] += 1
                                if validated_vocab:
                                    genes_with_validated_vocab_hits_cnt[genome_ref][namespace] += 1

                                if top_hit_flag:  # does SEED give more than one function?
                                    domfam_list = [domfam_list[0]]
                                for domfam in domfam_list:
                                    dom_hits[genome_ref][gene_name][namespace][domfam] = True
                                    if domfam in target_fams:
                                        custom_target_fam_features_hit = True
                                        if domfam not in features_by_custom_target_fam:
                                            features_by_custom_target_fam[domfam] = dict()
                                        if genome_ref not in features_by_custom_target_fam[domfam]:
                                            features_by_custom_target_fam[domfam][genome_ref] = []
                                        features_by_custom_target_fam[domfam][genome_ref].append(gene_name)
                    #f_cnt += 1  # DEBUG


        # Make sure we have CDSs
        #
        missing_genes = []
        for genome_ref in genome_refs:
            if genome_CDS_count_by_ref[genome_ref] == 0:
                missing_genes.append("\t" + 'MISSING GENES FOR: ' + 'ref: '+genome_ref + ', obj_name: '+genome_obj_name_by_ref[genome_ref]+', sci_name: '+genome_sci_name_by_ref[genome_ref])
                missing_genes_by_genome_ref[genome_ref] = True
        if missing_genes:
            error_msg = "ABORT: Some of the Genomes are missing gene calls.  Please run RAST or Prokka App to get Genome objects with Gene calls for the following Genomes\n"
            error_msg += "\n".join(missing_genes)
            self.log(console, error_msg)
            raise ValueError(error_msg)


        # check for validated vocab if reading SEED
        #
        missing_SEED_annot_by_genome_ref = dict()
        missing_SEED_annot = []
        if 'SEED' in namespaces_reading:
            namespace = 'SEED'
            fraction_required_valid = required_annot_perc[namespace] / 100.0
            for genome_ref in genome_refs:
                self.log(console, "genome:"+genome_ref+" gene cnt with validated annot:"+str(genes_with_validated_vocab_hits_cnt[genome_ref][namespace])+" gene cnt with annot:"+str(genes_with_hits_cnt[genome_ref][namespace]))  # DEBUG

                valid_fraction = genes_with_validated_vocab_hits_cnt[genome_ref][namespace] / float(genes_with_hits_cnt[genome_ref][namespace])
                if valid_fraction < fraction_required_valid:
                    missing_SEED_annot.append("\t" + 'MISSING RAST SEED ANNOTATION FOR: ' + 'ref: '+genome_ref + ', obj_name: '+genome_obj_name_by_ref[genome_ref]+', sci_name: '+genome_sci_name_by_ref[genome_ref]+".  You can drop the threshold required in advanced parameters.")
                    missing_SEED_annot_by_genome_ref[genome_ref] = True

            if missing_SEED_annot:
                if len(missing_SEED_annot) == len(genome_refs):
                    error_msg = "ABORT: ALL genomes are missing RAST SEED Annotation.  You must run the RAST SEED Annotation App first\n"
                    error_msg += "\n".join(missing_SEED_annot)
                    self.log(console, error_msg)
                    raise ValueError(error_msg)

                # if strict, then abort
                if not params.get('skip_missing_genomes') or int(params.get('skip_missing_genomes')) != 1:
                    error_msg = "ABORT: You must run the RAST SEED Annotation App or use SKIP option on below genomes first\n"
                    error_msg += "\n".join(missing_SEED_annot)
                    self.log(console, error_msg)
                    raise ValueError(error_msg)
                # if skipping, then remove genomes with missing annotations
                else:
                    new_genome_refs = []
                    for genome_ref in genome_refs:
                        if genome_ref in missing_SEED_annot_by_genome_ref:
                            continue
                        new_genome_refs.append(genome_ref)
                    genome_refs = new_genome_refs
                    self.log(console, "SKIP option selected. If you wish to include the below Genomes, you must run the RAST SEED Annotation App first")
                    self.log(console, "\n".join(missing_SEED_annot))


        # determine if custom domains are not just SEED
        #
        search_domains_just_SEED = True
        for namespace in namespaces_reading.keys():
            if namespace != 'SEED':
                search_domains_just_SEED = False

        # read DomainAnnotation object to capture domain hits to genes within each namespace
        #
        if search_domains_just_SEED:
            self.log(console, "Search Domains just SEED.  Not looking for Domain Annotations")
        else:
            self.log(console, "Search Domains other than SEED.  Looking for Domain Annotations")
            dom_annot_found = dict()

            KBASE_DOMAINHIT_GENE_ID_I = 0
            KBASE_DOMAINHIT_GENE_BEG_I = 1  # not used
            KBASE_DOMAINHIT_GENE_END_I = 2  # not used
            KBASE_DOMAINHIT_GENE_STRAND_I = 3  # not used
            KBASE_DOMAINHIT_GENE_HITS_DICT_I = 4
            KBASE_DOMAINHIT_GENE_HITS_DICT_BEG_J = 0
            KBASE_DOMAINHIT_GENE_HITS_DICT_END_J = 1
            KBASE_DOMAINHIT_GENE_HITS_DICT_EVALUE_J = 2
            KBASE_DOMAINHIT_GENE_HITS_DICT_BITSCORE_J = 3
            KBASE_DOMAINHIT_GENE_HITS_DICT_ALNPERC_J = 4

            # DEBUG
            #for genome_ref in genome_refs:
            #    self.log (console, "SEED ANNOT CNT A: '"+str(genes_with_hits_cnt[genome_ref]['SEED'])+"'")

            dom_annot_obj_info_list = []
            # read local workspace first
            try:
                dom_annot_obj_info_list.extend(wsClient.list_objects(
                    {'workspaces': [params['workspace_name']], 'type': "KBaseGeneFamilies.DomainAnnotation"}))
            except Exception as e:
                raise ValueError("Unable to list DomainAnnotation objects from workspace: " +
                                 str(ws_id) + " " + str(e))
            # read any remaining remote workspaces
            for ws_id in uniq_genome_ws_ids.keys():
                try:
                    dom_annot_obj_info_list.extend(wsClient.list_objects(
                        {'ids': [ws_id], 'type': "KBaseGeneFamilies.DomainAnnotation"}))
                except Exception as e:
                    raise ValueError("Unable to list DomainAnnotation objects from workspace: " +
                                     str(ws_id) + " " + str(e))

            for info in dom_annot_obj_info_list:
                dom_annot_ref = str(info[WSID_I]) + '/' + str(info[OBJID_I]) + '/' + str(info[VERSION_I])
                try:
                    domain_data = wsClient.get_objects([{'ref': dom_annot_ref}])[0]['data']
                except:
                    raise ValueError("unable to fetch domain annotation: " + dom_annot_ref)

                # read domain data object
                genome_ref = domain_data['genome_ref']
                if params.get('enforce_genome_version_match') and int(params.get('enforce_genome_version_match')) == 1:
                    # skip extra domainannots
                    if genome_ref not in genome_refs:
                        continue
                else:
                    (ws_id, obj_id, version) = genome_ref.split('/')
                    genome_ref_versionless = ws_id+'/'+obj_id
                    # skip extra domainannots
                    if genome_ref_versionless not in genome_ref_by_versionless:
                        continue

                    # report any change in obj version
                    source_obj_type = 'SpeciesTree'
                    source_genome_ref = genome_ref_by_versionless[ws_id+'/'+obj_id]
                    if genome_ref != source_genome_ref:
                        self.log(console, "DomainAnnotation object generated from different version of genome found in "+source_obj_type+".  DomainAnnotation for ref: "+genome_ref+" obj_name: "+genome_obj_name_by_ref[source_genome_ref]+" sci_name: "+genome_sci_name_by_ref[source_genome_ref]+" but using genome version from "+source_obj_type+" instead: "+source_genome_ref)
                    else:
                        self.log(console, "DomainAnnotation object generated from same version of genome ref: "+genome_ref+" obj_name: "+genome_obj_name_by_ref[genome_ref]+" sci_name: "+genome_sci_name_by_ref[genome_ref]+" as in "+source_obj_type)

                    genome_ref = source_genome_ref

                # avoid duplicate domain annotations
                dom_annot_found[genome_ref] = True
                if genome_ref not in domain_annot_obj_by_genome_ref:
                    domain_annot_obj_by_genome_ref[genome_ref] = dom_annot_ref
                    self.log(console, "DomainAnnotation object "+str(domain_annot_obj_by_genome_ref[genome_ref])+" being used for Genome obj_name: "+genome_obj_name_by_ref[genome_ref]+" sci_name: "+genome_sci_name_by_ref[genome_ref])
                else:
                    self.log(console, "DomainAnnotation object "+str(domain_annot_obj_by_genome_ref[genome_ref])+" already found for Genome obj_name: "+genome_obj_name_by_ref[genome_ref]+" sci_name: "+genome_sci_name_by_ref[genome_ref]+". Ignoring DomainAnnotation "+dom_annot_ref)
                    continue

                if genome_ref not in dom_hits:
                    dom_hits[genome_ref] = dict()

                if genome_ref not in genes_with_hits_cnt:
                    genes_with_hits_cnt[genome_ref] = dict()

                for scaffold_id_iter in domain_data['data'].keys():
                    for CDS_domain_list in domain_data['data'][scaffold_id_iter]:
                        gene_ID = CDS_domain_list[KBASE_DOMAINHIT_GENE_ID_I]
                        #gene_name = re.sub ('^'+genome_object_name+'.', '', gene_ID)
                        gene_name = gene_ID
                        #(contig_name, gene_name) = (gene_ID[0:gene_ID.index(".")], gene_ID[gene_ID.index(".")+1:])
                        #print ("DOMAIN_HIT: "+contig_name+" "+gene_name)  # DEBUG
                        #print ("DOMAIN_HIT for gene: "+gene_name)  # DEBUG
                        #gene_beg       = CDS_domain_list[KBASE_DOMAINHIT_GENE_BEG_I]
                        #gene_end       = CDS_domain_list[KBASE_DOMAINHIT_GENE_END_I]
                        #gene_strand    = CDS_domain_list[KBASE_DOMAINHIT_GENE_STRAND_I]
                        gene_hits_dict = CDS_domain_list[KBASE_DOMAINHIT_GENE_HITS_DICT_I]

                        dom_hits_by_namespace = dict()
                        top_hit_evalue_by_namespace = dict()
                        top_hit_dom_by_namespace = dict()

                        for namespace in namespace_classes:
                            dom_hits_by_namespace[namespace] = dict()
                            top_hit_evalue_by_namespace[namespace] = 100
                            top_hit_dom_by_namespace[namespace] = None

                        for domfam in gene_hits_dict.keys():
                            if domfam.startswith('PF'):
                                domfam_clean = re.sub('\.[^\.]*$', '', domfam)
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
                                beg = int(hit[KBASE_DOMAINHIT_GENE_HITS_DICT_BEG_J])
                                end = int(hit[KBASE_DOMAINHIT_GENE_HITS_DICT_END_J])
                                e_value = float(hit[KBASE_DOMAINHIT_GENE_HITS_DICT_EVALUE_J])
                                bit_score = float(hit[KBASE_DOMAINHIT_GENE_HITS_DICT_BITSCORE_J])
                                aln_perc = float(hit[KBASE_DOMAINHIT_GENE_HITS_DICT_ALNPERC_J])

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
                                    dom_hits[genome_ref][gene_name][namespace] = {
                                        top_hit_dom_by_namespace[namespace]: True}
                                else:
                                    dom_hits[genome_ref][gene_name][namespace] = dom_hits_by_namespace[namespace]

                                # store for featureset
                                for domfam in dom_hits[genome_ref][gene_name][namespace].keys():
                                    if domfam in target_fams:
                                        custom_target_fam_features_hit = True
                                        if domfam not in features_by_custom_target_fam:
                                            features_by_custom_target_fam[domfam] = dict()
                                        if genome_ref not in features_by_custom_target_fam[domfam]:
                                            features_by_custom_target_fam[domfam][genome_ref] = []
                                        features_by_custom_target_fam[domfam][genome_ref].append(gene_name)


            # make sure we have domain annotations for all genomes
            missing_annot = []
            missing_dom_annot_by_genome_ref = dict()
            for genome_ref in genome_refs:
                if genome_ref not in dom_annot_found:
                    missing_annot.append("\t" + 'MISSING DOMAIN ANNOTATION FOR: ' + 'ref: '+genome_ref + ', obj_name: '+genome_obj_name_by_ref[genome_ref]+', sci_name: '+genome_sci_name_by_ref[genome_ref])
                    missing_dom_annot_by_genome_ref[genome_ref] = True

            if missing_annot:
                if len(missing_annot) == len(genome_refs):
                    error_msg = "ABORT: ALL genomes have no matching Domain Annotation.  You must run the 'Domain Annotation' App first\n"
                    error_msg += "\n".join(missing_annot)
                    self.log(console, error_msg)
                    raise ValueError(error_msg)

                # if strict, then abort
                if not params.get('skip_missing_genomes') or int(params.get('skip_missing_genomes')) != 1:
                    error_msg = "ABORT: You must run the 'Domain Annotation' App or use SKIP option on below genomes first\n"
                    error_msg += "\n".join(missing_annot)
                    self.log(console, error_msg)
                    raise ValueError(error_msg)
                # if skipping, then remove genomes with missing annotations
                else:
                    new_genome_refs = []
                    for genome_ref in genome_refs:
                        if genome_ref in missing_dom_annot_by_genome_ref:
                            continue
                        new_genome_refs.append(genome_ref)
                    genome_refs = new_genome_refs
                    self.log(console, "SKIP option selected. If you wish to include the below Genomes, you must run the 'Domain Annotation' App first")
                    self.log(console, "\n".join(missing_annot))


        # DEBUG
        #for genome_ref in genome_refs:
        #    self.log (console, "SEED ANNOT CNT B: '"+str(genes_with_hits_cnt[genome_ref]['SEED'])+"'")

        # Alert user for any genomes that are missing annotations in a requested namespace
        #   this can happen even with a DomainAnnotation object if the namespace was skipped
        #
        inadequate_annot = []
        inadequate_annot_by_genome_ref = dict()
        for genome_ref in genome_refs:
            total_genes = genome_CDS_count_by_ref[genome_ref]

            for namespace in sorted(namespaces_reading.keys()):
                fraction_requiring_annotation = required_annot_perc[namespace] / 100.0
                if namespace == 'SEED':
                    annotation_tool = 'RAST Genome Annotation App'
                else:
                    annotation_tool = 'Domain Annotation App'
                if genes_with_hits_cnt[genome_ref][namespace] < fraction_requiring_annotation * total_genes:
                    inadequate_annot.append("\t" + 'INADEQUATE DOMAIN ANNOTATION FOR: ' + 'ref: '+genome_ref + ', obj_name: '+genome_obj_name_by_ref[genome_ref]+', sci_name: '+genome_sci_name_by_ref[genome_ref]+".  Namespace: "+namespace+" found in "+str(genes_with_hits_cnt[genome_ref][namespace])+" of a total of "+str(total_genes)+".  "+str(required_annot_perc[namespace])+"% were configured in advanced parameter input required to be annotated by "+namespace+".  Something may have gone wrong with "+annotation_tool+".  Try rerunning or dropping the threshold required in advanced parameters.")
                    inadequate_annot_by_genome_ref[genome_ref] = True

            if inadequate_annot:
                if len(inadequate_annot) == len(genome_refs):
                    error_msg = "ABORT: ALL genomes have poor Domain Annotation.  You must run the 'Domain Annotation' App first\n"
                    error_msg += "\n".join(inadequate_annot)
                    self.log(console, error_msg)
                    raise ValueError(error_msg)

                # if strict, then abort
                if not params.get('skip_missing_genomes') or int(params.get('skip_missing_genomes')) != 1:
                    error_msg = "ABORT: You must run the 'Domain Annotation' App or use SKIP option on below genomes first\n"
                    error_msg += "\n".join(inadequate_annot)
                    self.log(console, error_msg)
                    raise ValueError(error_msg)
                # if skipping, then remove genomes with missing annotations
                else:
                    new_genome_refs = []
                    for genome_ref in genome_refs:
                        if genome_ref in inadequate_annot_by_genome_ref:
                            continue
                        new_genome_refs.append(genome_ref)
                    genome_refs = new_genome_refs
                    self.log(console, "SKIP option selected. If you wish to include the below Genomes, you must run the 'Domain Annotation' App first")
                    self.log(console, "\n".join(inadequate_annot))


        # shouldn't draw tree with less than 3 leaves
        #
        if len(genome_refs) < 3:
            error_msg = "Too few remaining genomes ("+str(len(genome_refs))+") to draw meaningful tree.  Need at least 3.  Please use 'View Function Profile for Genomes' App instead"
            self.log(console, error_msg)
            raise ValueError ("ABORT: "+error_msg)


        # STEP 2 - Analysis
        # calculate table
        #
        table_data = dict()
        INSANE_VALUE = 10000000000000000
        overall_low_val = INSANE_VALUE
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
                        namespace = re.sub('\d*$', '', cat)
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
                                namespace = re.sub('\d*$', '', cat)
                        else:
                            namespace = params['namespace']
                        total_genes = genes_with_hits_cnt[genome_ref][namespace]
                    else:
                        total_genes = genome_CDS_count_by_ref[genome_ref]

                    if total_genes > 0:
                        table_data[genome_ref][cat] /= float(total_genes)
                        table_data[genome_ref][cat] *= 100.0
                    else:
                        table_data[genome_ref][cat] = 0

        # determine high and low val
        for genome_ref in genome_refs:
            for cat in cats:
                val = table_data[genome_ref][cat]
                if val == 0:
                    continue
                #self.log (console, "HIGH VAL SCAN CAT: '"+cat+"' VAL: '"+str(val)+"'")  # DEBUG
                if 'log_base' in params and params['log_base'] != None and params['log_base'] != '':
                    log_base = float(params['log_base'])
                    if log_base <= 1.0:
                        raise ValueError("log base must be > 1.0")
                    val = math.log(val, log_base)
                if val > overall_high_val:
                    overall_high_val = val
                if val < overall_low_val:
                    overall_low_val = val
        if overall_high_val == -INSANE_VALUE:
            raise ValueError("unable to find any counts")

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


        # STEP 3 - Create and save featureSets
        #
        objects_created = []
        if custom_target_fam_features_hit:
            featureSet_by_custom_target_fam = dict()
            for target_fam in sorted(features_by_custom_target_fam.keys()):
                featureSet_by_custom_target_fam[target_fam] = dict()
                for genome_ref in sorted(features_by_custom_target_fam[target_fam].keys()):
                    for fid in sorted(features_by_custom_target_fam[target_fam][genome_ref]):
                        if fid in featureSet_by_custom_target_fam[target_fam]:
                            featureSet_by_custom_target_fam[target_fam][fid].append(genome_ref)
                        else:
                            featureSet_by_custom_target_fam[target_fam][fid] = [genome_ref]

                fs_name = target_fam+'-'+input_obj_name+'.FeatureSet'
                fs_desc = 'Hits by '+target_fam+' to '+input_obj_name
                fs_obj = {'description': fs_desc,
                          'elements': featureSet_by_custom_target_fam[target_fam]
                         }
                new_obj_info = wsClient.save_objects({
                    'workspace': params['workspace_name'],
                    'objects': [
                        {'type': 'KBaseCollections.FeatureSet',
                         'data': fs_obj,
                         'name': fs_name,
                         'meta': {},
                         'provenance': provenance
                         }]
                })[0]
                objects_created.append(
                    {'ref': str(new_obj_info[6]) + '/' + str(new_obj_info[0]) + '/' + str(new_obj_info[4]), 'description': fs_desc})
                featureSet_by_custom_target_fam[target_fam] = {}  # free memory
                fs_obj = {}  # free memory


        # STEP 4 - Prune tree if any leaf genomes missing domain annotation
        #
        if not search_domains_just_SEED:
            prune_retain_list = []  # prune() method takes list of leaves to keep
            prune_remove_list = []
            for n in species_tree.traverse():
                if n.is_leaf():
                    genome_id = n.name
                    if genome_ref_by_id[genome_id] not in missing_dom_annot_by_genome_ref:
                        prune_retain_list.append(n.name)
                        self.log(console, "Retaining "+n.name) # DEBUG
                    else:
                        prune_remove_list.append(n.name)
            if len(prune_remove_list) > 0:
                self.log(console, "Pruning genomes from SpeciesTree that have no corresponding DomainAnnotation object")
                for genome_id in prune_remove_list:
                    self.log(console, "\t"+"Removing from SpeciesTree "+genome_id+" ref: "+genome_ref_by_id[genome_id]+" obj_name: "+genome_obj_name_by_ref[genome_ref_by_id[genome_id]]+" sci_name: "+genome_sci_name_by_ref[genome_ref_by_id[genome_id]])

                # prune() takes keep list, not remove list
                species_tree.prune (prune_retain_list)


        # STEP 5 - Draw tree (we already instantiated Tree above)
        #
        png_file = speciesTree_name + '.png'
        pdf_file = speciesTree_name + '.pdf'
        output_png_file_path = os.path.join(html_output_dir, png_file)
        output_pdf_file_path = os.path.join(html_output_dir, pdf_file)

        # init ETE3 accessory objects
        ts = ete3.TreeStyle()

        # customize
        ts.show_leaf_name = True
        ts.show_branch_length = False
        ts.show_branch_support = True
        #ts.scale = 50 # 50 pixels per branch length unit
        ts.branch_vertical_margin = 5  # pixels between adjacent branches
        #ts.title.add_face(ete3.TextFace(params['output_name']+": "+params['desc'], fsize=10), column=0)

        node_style = ete3.NodeStyle()
        node_style["fgcolor"] = "#606060"  # for node balls
        node_style["size"] = 10  # for node balls (gets reset based on support)
        node_style["vt_line_color"] = "#606060"
        node_style["hz_line_color"] = "#606060"
        node_style["vt_line_width"] = 2
        node_style["hz_line_width"] = 2
        node_style["vt_line_type"] = 0  # 0 solid, 1 dashed, 2 dotted
        node_style["hz_line_type"] = 0

        leaf_style = ete3.NodeStyle()
        leaf_style["fgcolor"] = "#ffffff"  # for node balls
        leaf_style["size"] = 2  # for node balls (we're using it to add space)
        leaf_style["vt_line_color"] = "#606060"  # unecessary
        leaf_style["hz_line_color"] = "#606060"
        leaf_style["vt_line_width"] = 2
        leaf_style["hz_line_width"] = 2
        leaf_style["vt_line_type"] = 0  # 0 solid, 1 dashed, 2 dotted
        leaf_style["hz_line_type"] = 0

        # make tree display ready
        for n in species_tree.traverse():
            if n.is_leaf():
                style = leaf_style
                genome_id = n.name
                #n.name = genome_sci_name_by_id[genome_id]
                n.name = None
                genome_obj_name = genome_obj_name_by_id[genome_id]
                genome_sci_name = genome_sci_name_by_id[genome_id]
                [ws_id, obj_id, genome_obj_version] = genome_ref_by_id[genome_id].split('/')
                genome_disp_name = ''
                if 'obj_name' in params.get('genome_disp_name_config'):
                    genome_disp_name += genome_obj_name
                    if 'ver' in params.get('genome_disp_name_config'):
                        genome_disp_name += '.v'+str(genome_obj_version)

                    if 'sci_name' in params.get('genome_disp_name_config'):
                        genome_disp_name += ': '+genome_sci_name
                else:
                    genome_disp_name = genome_sci_name

                leaf_name_disp = genome_disp_name
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
        img_in_width = round(float(img_pix_width) / float(dpi), 1)
        img_html_width = img_pix_width // 2
        species_tree.render(output_png_file_path, w=img_in_width, units=img_units, dpi=dpi, tree_style=ts)
        species_tree.render(output_pdf_file_path, w=img_in_width, units=img_units, tree_style=ts)  # dpi irrelevant


        # STEP 6 - build report
        #
        reportName = 'kb_phylogenomics_report_' + str(uuid.uuid4())
        reportObj = {'objects_created': objects_created,
                     'direct_html_link_index': 0,
                     'file_links': [],
                     'html_links': [],
                     'workspace_name': params['workspace_name'],
                     'report_object_name': reportName
                     }

        # build html report
        sp = '&nbsp;'
        text_color = "#606060"
        text_color_2 = "#606060"
        head_color_1 = "#eeeeee"
        head_color_2 = "#eeeeee"
        border_color = "#cccccc"
        border_cat_color = "#ffccff"
        #graph_color = "lightblue"
        #graph_width = 100
        #graph_char = "."
        graph_char = sp
        color_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e']
        max_color = len(color_list) - 1
        cat_disp_trunc_len = 40
        cell_width = '10px'
        tree_scale_factor = 22.625
        tree_img_height = int(tree_scale_factor * len(genome_refs))
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
        if len(group_order) > 0:
            show_groups = True

        html_report_lines = []
        html_report_lines += ['<html>']
        html_report_lines += ['<head>']
        html_report_lines += ['<title>KBase Functional Domain Profile with Species Tree</title>']
        html_report_lines += ['<style>']
        html_report_lines += [
            ".vertical-text {\ndisplay: inline-block;\noverflow: hidden;\nwidth: 0.65em;\n}\n.vertical-text__inner {\ndisplay: inline-block;\nwhite-space: nowrap;\nline-height: 1.1;\ntransform: translate(0,100%) rotate(-90deg);\ntransform-origin: 0 0;\n}\n.vertical-text__inner:after {\ncontent: \"\";\ndisplay: block;\nmargin: 0.0em 0 100%;\n}"]
        html_report_lines += [
            ".vertical-text_title {\ndisplay: inline-block;\noverflow: hidden;\nwidth: 1.0em;\n}\n.vertical-text__inner_title {\ndisplay: inline-block;\nwhite-space: nowrap;\nline-height: 1.0;\ntransform: translate(0,100%) rotate(-90deg);\ntransform-origin: 0 0;\n}\n.vertical-text__inner_title:after {\ncontent: \"\";\ndisplay: block;\nmargin: 0.0em 0 100%;\n}"]
        html_report_lines += ['</style>']
        html_report_lines += ['</head>']
        html_report_lines += ['<body bgcolor="white">']

        # genomes as rows
        if 'vertical' in params and params['vertical'] == "1":
            # table header
            html_report_lines += ['<table cellpadding=' + graph_padding +
                                  ' cellspacing=' + graph_spacing + ' border=' + border + '>']
            corner_rowspan = "1"
            if show_groups:
                corner_rowspan = "2"
            label = ''
            if params['namespace'] != 'custom':
                label = params['namespace']
                if label == 'PF':
                    label = 'PFAM'
                elif label == 'TIGR':
                    label = 'TIGRFAM'
            html_report_lines += ['<tr><td valign=bottom align=right rowspan=' + corner_rowspan +
                                  '><div class="vertical-text_title"><div class="vertical-text__inner_title"><font color="' + text_color + '">' + label + '</font></div></div></td>']

            # group headers
            if show_groups:
                for cat_group in group_order:
                    if cat_group.startswith('SEED'):
                        cat_group_disp = re.sub('_', ' ', cat_group)
                    else:
                        cat_group_disp = cat_group
                    cat_group_words = cat_group_disp.split()
                    max_group_width = 3 * group_size[cat_group]
                    if len(cat_group) > max_group_width:
                        new_cat_group_words = []
                        sentence_len = 0
                        for w_i, word in enumerate(cat_group_words):
                            new_cat_group_words.append(word)
                            sentence_len += len(word)
                            if w_i < len(cat_group_words) - 1:
                                if sentence_len + 1 + len(cat_group_words[w_i + 1]) > max_group_width:
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
                        html_report_lines += ['<td bgcolor=white colspan=' + str(group_size[cat_group]) + '></td>']
                    else:
                        html_report_lines += ['<td style="border-right:solid 2px ' + border_cat_color + '; border-bottom:solid 2px ' + border_cat_color + '" bgcolor="' + head_color_1 +
                                              '"valign=middle align=center colspan=' + str(group_size[cat_group]) + '><font color="' + text_color + '" size=' + str(graph_cat_fontsize) + '><b>' + cat_group_disp + '</b></font></td>']

                html_report_lines += ['</tr><tr>']

            # column headers
            for cat in cats:
                if not cat_seen[cat] and not show_blanks:
                    continue
                if params['namespace'] == 'custom':
                    if cat.startswith('SEED'):
                        namespace = 'SEED'
                    else:
                        namespace = re.sub("\d*$", "", cat)
                    cell_title = domfam2name[namespace][cat].strip()
                    cat_disp = cat
                    cat_disp = re.sub('^SEED', 'SEED:', cat_disp)
                else:
                    cell_title = cat2name[params['namespace']][cat].strip()
                    cat_disp = cat
                    cat_disp = re.sub("TIGR_", "", cat_disp)
                if len(cat_disp) > cat_disp_trunc_len + 1:
                    cat_disp = cat_disp[0:cat_disp_trunc_len] + '*'
                html_report_lines += ['<td style="border-right:solid 2px ' + border_cat_color + '; border-bottom:solid 2px ' +
                                      border_cat_color + '" bgcolor="' + head_color_2 + '"title="' + cell_title + '" valign=bottom align=center>']
                if params['namespace'] != 'COG':
                    html_report_lines += ['<div class="vertical-text"><div class="vertical-text__inner">']
                html_report_lines += ['<font color="' + text_color_2 + '" size=' + graph_cat_fontsize + '><b>']
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
            html_report_lines += ['<tr><td align="left" valign="top" rowspan=' + str(
                len(genome_refs) + extra_tree_rows) + '><img src="' + png_file + '" height=' + str(tree_img_height) + '></td>']

            # rest of rows
            for row_i, genome_ref in enumerate(genome_refs):
                #genome_obj_name = genome_obj_name_by_ref[genome_ref]
                #genome_sci_name = genome_sci_name_by_ref[genome_ref]
                #if params.get('display_genome_object_name') \
                #   and int(params.get('display_genome_object_name')) == 1:
                #    genome_disp_name = genome_obj_name + ': ' + genome_sci_name
                #else:
                #    genome_disp_name = genome_sci_name
                if row_i > 0:
                    html_report_lines += ['<tr>']
                #html_report_lines += ['<td align=right><font color="'+text_color+'" size='+graph_gen_fontsize+'><b><nobr>'+genome_disp_name+'</nobr></b></font></td>']
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
                                raise ValueError("log base must be > 1.0")
                            val = math.log(val, log_base)
                        if overall_high_val == overall_low_val:
                            denom = 1.0
                        else:
                            denom = float(overall_high_val - overall_low_val)
                        cell_color_i = max_color - \
                                      int(round(max_color * (val - overall_low_val) / denom))
                        c = color_list[cell_color_i]
                        cell_color = '#' + c + c + c + c + 'FF'

                    if params['count_category'].startswith('perc'):
                        cell_val = str("%.3f" % table_data[genome_ref][cat])
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
                        html_report_lines += ['<td align=center valign=middle title="' + cell_val + '" style="width:' + cell_width + '" bgcolor="' +
                                              cell_color + '"><font color="' + this_text_color + '" size=' + cell_fontsize + '>' + this_graph_char + '</font></td>']
                    else:
                        html_report_lines += ['<td align=center valign=middle style="' + cell_width + '; border-right:solid 2px ' + border_color +
                                              '; border-bottom:solid 2px ' + border_color + '"><font color="' + text_color + '" size=' + cell_fontsize + '>' + cell_val + '</font></td>']

                html_report_lines += ['</tr>']
            # add extra blank rows to extend tree rule below grid
            for row_i in range(extra_tree_rows):
                html_report_lines += ['<tr><td bgcolor="white" style="width:10px"><font color="white" size=' +
                                      cell_fontsize + '>' + sp + '</font></td></tr>']

            html_report_lines += ['</table>']

        # genomes as columns
        else:
            raise ValueError("Do not yet support Genomes as columns")

        # key table
        html_report_lines += ['<p>']
        html_report_lines += ['<table cellpadding=3 cellspacing=2 border=' + border + '>']
        html_report_lines += ['<tr><td valign=middle align=left colspan=3 style="border-bottom:solid 4px ' +
                              border_color + '"><font color="' + text_color + '"><b>KEY</b></font></td></tr>']

        if show_groups:
            group_cat_i = 0
            for cat_group in group_order_with_blanks:
                if cat_group.startswith('SEED'):
                    cat_group_disp = re.sub('_', ' ', cat_group)
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
                    html_report_lines += ['<td bgcolor=white rowspan=' + str(
                        group_size_with_blanks[cat_group]) + ' style="border-right:solid 4px ' + border_color + '"></td>']
                else:
                    html_report_lines += ['<td style="border-right:solid 4px ' + border_color + '" valign=top align=right rowspan=' + str(
                        group_size_with_blanks[cat_group]) + '><font color="' + text_color + '" size=' + str(graph_cat_fontsize) + '><b>' + cat_group_disp + '</b></font></td>']

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
                        namespace = re.sub('\d*$', '', first_cat)
                    cat_disp = re.sub('^SEED', 'SEED:', first_cat)
                    desc = domfam2name[namespace][domfam]
                else:
                    namespace = params['namespace']
                    cat_disp = first_cat
                    desc = cat2name[namespace][first_cat]
                if len(cat_disp) > cat_disp_trunc_len + 1:
                    cat_disp = cat_disp[0:cat_disp_trunc_len] + '*'
                cat_disp = sp + cat_disp

                html_report_lines += ['<td valign=middle align=left bgcolor="' + cell_color + '" style="border-right:solid 4px ' +
                                      border_color + '"><font color="' + text_color + '" size=' + graph_cat_fontsize + '>' + cat_disp + '</font></td>']
                html_report_lines += ['<td valign=middle align=left bgcolor="' + cell_color + '"><font color="' +
                                      text_color + '" size=' + graph_cat_fontsize + '>' + sp + desc + '</font></td>']
                html_report_lines += ['</tr>']

                group_cat_i += 1

                # add rest of cats in group
                for c_i in range(group_cat_i, group_cat_i + group_size_with_blanks[cat_group] - 1):
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
                            namespace = re.sub('\d*$', '', cat)
                        cat_disp = re.sub('^SEED', 'SEED:', cat)
                        desc = domfam2name[namespace][domfam]
                    else:
                        namespace = params['namespace']
                        cat_disp = cat
                        desc = cat2name[namespace][cat]
                    if len(cat_disp) > cat_disp_trunc_len + 1:
                        cat_disp = cat_disp[0:cat_disp_trunc_len] + '*'
                    cat_disp = sp + cat_disp

                    html_report_lines += ['<tr>']
                    html_report_lines += ['<td valign=middle align=left bgcolor="' + cell_color + '" style="border-right:solid 4px ' +
                                          border_color + '"><font color="' + text_color + '" size=' + graph_cat_fontsize + '>' + cat_disp + '</font></td>']
                    html_report_lines += ['<td valign=middle align=left bgcolor="' + cell_color + '"><font color="' +
                                          text_color + '" size=' + graph_cat_fontsize + '>' + sp + desc + '</font></td>']
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
                        namespace = re.sub('\d*$', '', domfam)
                    cat_disp = re.sub('^SEED', 'SEED:', cat)
                    desc = domfam2name[namespace][domfam]
                else:
                    namespace = params['namespace']
                    cat_disp = cat
                    desc = cat2name[namespace][cat]
                if len(cat_disp) > cat_disp_trunc_len + 1:
                    cat_disp = cat_disp[0:cat_disp_trunc_len] + '*'
                html_report_lines += ['<tr>']
                html_report_lines += ['<td valign=middle align=left bgcolor="' + cell_color + '" style="border-right:solid 4px ' +
                                      border_color + '><font color="' + text_color + '" size=' + graph_cat_fontsize + '>' + cat_disp + '</font></td>']
                html_report_lines += ['<td valign=middle align=left bgcolor="' + cell_color +
                                      '"><font color="' + text_color + '" size=' + graph_cat_fontsize + '>' + desc + '</font></td>']
                html_report_lines += ['</tr>']

        html_report_lines += ['</table>']

        # close
        html_report_lines += ['</body>']
        html_report_lines += ['</html>']

        html_report_str = "\n".join(html_report_lines)
        #reportObj['direct_html'] = html_report_str

        # write html to file and upload
        html_file = os.path.join(html_output_dir, 'domain_profile_report.html')
        with open(html_file, 'w', 0) as html_handle:
            html_handle.write(html_report_str)
        dfu = DFUClient(self.callbackURL)
        try:
            #upload_ret = dfu.file_to_shock({'file_path': html_file,
            upload_ret = dfu.file_to_shock({'file_path': html_output_dir,
                                            'make_handle': 0,
                                            'pack': 'zip'})
        except:
            raise ValueError('Logging exception loading html_report to shock')

        reportObj['html_links'] = [{'shock_id': upload_ret['shock_id'],
                                    'name': 'domain_profile_report.html',
                                    'label': 'Functional Domain Profile report'}
                                   ]

        # save report object
        #
        reportClient = KBaseReport(self.callbackURL, token=ctx['token'], service_ver=SERVICE_VER)
        #report_info = report.create({'report':reportObj, 'workspace_name':params['workspace_name']})
        report_info = reportClient.create_extended_report(reportObj)

        output = {'report_name': report_info['name'], 'report_ref': report_info['ref']}

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
        output = {}
        raise NotImplementedError
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
           "input_compare_genome_refs" of type "data_obj_ref", parameter
           "input_outgroup_genome_refs" of type "data_obj_ref", parameter
           "save_featuresets" of type "bool"
        :returns: instance of type "view_pan_circle_plot_Output" ->
           structure: parameter "report_name" of String, parameter
           "report_ref" of String
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN view_pan_circle_plot

        ### STEP 0: basic init
        console = []
        invalid_msgs = []
        self.log(console, 'Running view_pan_circle_plot(): ')
        self.log(console, "\n" + pformat(params))

        # ws obj info indices
        [OBJID_I, NAME_I, TYPE_I, SAVE_DATE_I, VERSION_I, SAVED_BY_I, WSID_I,
         WORKSPACE_I, CHSUM_I, SIZE_I, META_I] = range(11)  # object_info tuple

        #SERVICE_VER = 'dev'  # DEBUG
        SERVICE_VER = 'release'
        token = ctx['token']
        try:
            wsClient = workspaceService(self.workspaceURL, token=token)
        except:
            raise ValueError("unable to instantiate wsClient")
        headers = {'Authorization': 'OAuth ' + token}
        env = os.environ.copy()
        env['KB_AUTH_TOKEN'] = token

        # param checks
        required_params = ['input_genome_ref',
                           'input_pangenome_ref'
                           ]
        for arg in required_params:
            if arg not in params or params[arg] == None or params[arg] == '':
                raise ValueError("Must define required param: '" + arg + "'")

        # load provenance
        provenance = [{}]
        if 'provenance' in ctx:
            provenance = ctx['provenance']
        provenance[0]['input_ws_objects'] = [str(params['input_genome_ref']),
                                             str(params['input_pangenome_ref'])
                                             ]

        # set the output paths
        timestamp = int((datetime.utcnow() - datetime.utcfromtimestamp(0)).total_seconds() * 1000)
        output_dir = os.path.join(self.scratch, 'output.' + str(timestamp))
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        html_output_dir = os.path.join(output_dir, 'html_output')
        if not os.path.exists(html_output_dir):
            os.makedirs(html_output_dir)

        # get base genome
        #
        self.log(console, "GETTING BASE GENOME OBJECT")
        genome_sci_name_by_ref = dict()
        base_genome_ref = input_ref = params['input_genome_ref']
        base_genome_obj_name = None
        try:
            input_obj_info = wsClient.get_object_info_new({'objects': [{'ref': input_ref}]})[0]
            input_obj_type = re.sub('-[0-9]+\.[0-9]+$', "", input_obj_info[TYPE_I])  # remove trailing version
            base_genome_obj_name = input_obj_info[NAME_I]
            base_genome_obj_name = base_genome_obj_name.replace(" ", "_")
        except Exception as e:
            raise ValueError('Unable to get object from workspace: (' + input_ref + ')' + str(e))
        accepted_input_types = ["KBaseGenomes.Genome"]
        if input_obj_type not in accepted_input_types:
            raise ValueError("Input object of type '" + input_obj_type +
                             "' not accepted.  Must be one of " + ", ".join(accepted_input_types))

        try:
            base_genome_obj = wsClient.get_objects([{'ref': input_ref}])[0]['data']
            genome_sci_name_by_ref[base_genome_ref] = base_genome_obj['scientific_name']
        except:
            raise ValueError("unable to fetch genome: " + input_ref)

        # get pangenome
        #
        self.log(console, "GETTING PANGENOME OBJECT")
        input_ref = params['input_pangenome_ref']
        try:
            input_obj_info = wsClient.get_object_info_new({'objects': [{'ref': input_ref}]})[0]
            input_obj_type = re.sub('-[0-9]+\.[0-9]+$', "", input_obj_info[TYPE_I])  # remove trailing version
            pg_obj_name = input_obj_info[NAME_I]
            pg_obj_name = pg_obj_name.replace(" ", "_")
        except Exception as e:
            raise ValueError('Unable to get object from workspace: (' + input_ref + ')' + str(e))
        accepted_input_types = ["KBaseGenomes.Pangenome"]
        if input_obj_type not in accepted_input_types:
            raise ValueError("Input object of type '" + input_obj_type +
                             "' not accepted.  Must be one of " + ", ".join(accepted_input_types))

        try:
            pg_obj = wsClient.get_objects([{'ref': input_ref}])[0]['data']
        except:
            raise ValueError("unable to fetch genome: " + input_ref)

        # get genome_refs from pangenome and make sure requested genomes are found
        #
        self.log(console, "READING GENOME REFS IN PANGENOME")
        pg_genome_refs = pg_obj['genome_refs']
        compare_genome_refs = []
        compare_genomes_cnt = 0
        if 'input_compare_genome_refs' not in params or not params['input_compare_genome_refs']:
            for g_ref in pg_genome_refs:
                if g_ref == base_genome_ref:
                    continue
                compare_genome_refs.append(g_ref)
                compare_genomes_cnt += 1
        else:
            for g_ref in params['input_compare_genome_refs']:
                if g_ref == base_genome_ref:
                    continue
                compare_genome_refs.append(g_ref)
                compare_genomes_cnt += 1

        # get outgroup genomes and remove from compare_genomes
        #
        self.log(console, "REMOVING OUTGROUP GENOME(s) FROM TARGETS")
        outgroup_genome_refs = []
        outgroup_genome_refs_cnt = 0
        if 'input_outgroup_genome_refs' in params and params['input_outgroup_genome_refs']:
            for genome_ref in params['input_outgroup_genome_refs']:
                outgroup_genome_refs.append(genome_ref)
                outgroup_genome_refs_cnt += 1
            new_compare_genome_refs = []
            compare_genomes_cnt = 0
            for genome_ref in compare_genome_refs:
                if genome_ref not in outgroup_genome_refs:
                    new_compare_genome_refs.append(genome_ref)
                    compare_genomes_cnt += 1
            compare_genome_refs = new_compare_genome_refs

        # Make sure all requested genomes are in pangenome
        #
        self.log(console, "CHECKING FOR REQUESTED GENOMES IN PANGENOME")
        missing_genomes = []
        for genome_ref in [base_genome_ref] + compare_genome_refs + outgroup_genome_refs:
            if genome_ref not in pg_genome_refs:
                missing_genomes.append(genome_ref)
        if missing_genomes:
            msg = ''
            for genome_ref in missing_genomes:
                msg += "genome " + genome_ref + " not found in pangenome\n"
            raise ValueError(msg)

        # Reorder compare genomes by fractional overlap to base by pangenome
        #
        self.log(console, "ORDERING TARGET GENOMES BY OVERLAP WITH BASE")
        compare_genome_cluster_overlap_cnt = dict()
        for genome_ref in compare_genome_refs:
            compare_genome_cluster_overlap_cnt[genome_ref] = 0

        for cluster in pg_obj['orthologs']:
            genomes_seen = dict()
            for cluster_member in cluster['orthologs']:
                feature_id = cluster_member[0]
                feature_len_maybe = cluster_member[1]
                genome_ref = cluster_member[2]
                genomes_seen[genome_ref] = True
            if base_genome_ref in genomes_seen:
                for genome_ref in compare_genome_refs:
                    if genome_ref in genomes_seen:
                        compare_genome_cluster_overlap_cnt[genome_ref] += 1

        sorted_compare_genome_refs = sorted(compare_genome_cluster_overlap_cnt,
                                            key=compare_genome_cluster_overlap_cnt.__getitem__, reverse=True)
        compare_genome_refs = sorted_compare_genome_refs

        # Get genome sci names
        #
        self.log(console, "GETTING GENOME SCIENTIFIC NAMES")
        for genome_ref in compare_genome_refs + outgroup_genome_refs:
            try:
                genome_obj = wsClient.get_objects([{'ref': genome_ref}])[0]['data']
                genome_sci_name_by_ref[genome_ref] = genome_obj['scientific_name']
            except:
                raise ValueError("unable to fetch genome: " + genome_ref)

        # Determine singleton, clade-core, universal, and partial pangenome
        #   feature sets for base+compare genome set
        #   (but not including outgroup genome features)
        #
        self.log(console, "DETERMINING PANGENOME CATEGORIES OF FEATURES")
        singleton_featureSet_elements = dict()
        partial_featureSet_elements = dict()
        core_featureSet_elements = dict()
        univ_featureSet_elements = dict()
        for cluster in pg_obj['orthologs']:
            genomes_seen = dict()
            fids_by_genome_ref = dict()
            for cluster_member in cluster['orthologs']:
                feature_id = cluster_member[0]
                feature_len_maybe = cluster_member[1]
                genome_ref = cluster_member[2]
                genomes_seen[genome_ref] = True
                try:
                    fid_list = fids_by_genome_ref[genome_ref]
                except:
                    fids_by_genome_ref[genome_ref] = []
                fids_by_genome_ref[genome_ref].append(feature_id)

            # determine categorization
            hit_cnt = 0
            for genome_ref in [base_genome_ref] + compare_genome_refs:
                if genome_ref in genomes_seen:
                    hit_cnt += 1
            if hit_cnt == 0:  # nothing within requested genome set
                continue
            elif hit_cnt == 1:  # singleton
                for genome_ref in [base_genome_ref] + compare_genome_refs:
                    if genome_ref in genomes_seen:
                        for fid in fids_by_genome_ref[genome_ref]:
                            #featureSet_element_id = genome_ref + self.genome_feature_id_delim + fid
                            #singleton_featureSet_elements[featureSet_element_id] = [genome_ref]
                            if fid in singleton_featureSet_elements:
                                singleton_featureSet_elements[fid].append(genome_ref)
                            else:
                                singleton_featureSet_elements[fid] = [genome_ref]
            elif hit_cnt < compare_genomes_cnt + 1:  # +1: include base genome
                for genome_ref in [base_genome_ref] + compare_genome_refs:
                    if genome_ref in genomes_seen:
                        for fid in fids_by_genome_ref[genome_ref]:
                            #featureSet_element_id = genome_ref + self.genome_feature_id_delim + fid
                            #partial_featureSet_elements[featureSet_element_id] = [genome_ref]
                            if fid in partial_featureSet_elements:
                                partial_featureSet_elements[fid].append(genome_ref)
                            else:
                                partial_featureSet_elements[fid] = [genome_ref]
            else:  # core
                outgroup_hit = False
                for genome_ref in outgroup_genome_refs:
                    if genome_ref in genomes_seen:
                        outgroup_hit = True
                        break
                if outgroup_hit:  # universal core
                    for genome_ref in [base_genome_ref] + compare_genome_refs:
                        #if genome_ref in genomes_seen:  # implicit
                        for fid in fids_by_genome_ref[genome_ref]:
                            #featureSet_element_id = genome_ref + self.genome_feature_id_delim + fid
                            #univ_featureSet_elements[featureSet_element_id] = [genome_ref]
                            if fid in univ_featureSet_elements:
                                univ_featureSet_elements[fid].append(genome_ref)
                            else:
                                univ_featureSet_elements[fid] = [genome_ref]
                else:  # clade-specific core
                    for genome_ref in [base_genome_ref] + compare_genome_refs:
                        #if genome_ref in genomes_seen:  # implicit
                        for fid in fids_by_genome_ref[genome_ref]:
                            #featureSet_element_id = genome_ref + self.genome_feature_id_delim + fid
                            #core_featureSet_elements[featureSet_element_id] = [genome_ref]
                            if fid in core_featureSet_elements:
                                core_featureSet_elements[fid].append(genome_ref)
                            else:
                                core_featureSet_elements[fid] = [genome_ref]

        # Create and save featureSets
        #
        objects_created = []
        if 'save_featuresets' not in params or params['save_featuresets'] == None or params['save_featuresets'] == '' or int(params['save_featuresets']) != 1:
            self.log(console, "SKIPPING FEATURESETS")
        else:
            self.log(console, "SAVING FEATURESETS")

            if singleton_featureSet_elements:
                fs_name = pg_obj_name + ".base_genome-" + base_genome_obj_name + ".singleton_pangenome.FeatureSet"
                fs_desc = pg_obj_name + ".base_genome-" + base_genome_obj_name + " singleton pangenome features"
                singleton_obj = {'description': fs_desc,
                                 'elements': singleton_featureSet_elements
                                 }
                new_obj_info = wsClient.save_objects({
                    'workspace': params['workspace_name'],
                    'objects': [
                        {'type': 'KBaseCollections.FeatureSet',
                         'data': singleton_obj,
                         'name': fs_name,
                         'meta': {},
                         'provenance': provenance
                         }]
                })[0]
                objects_created.append(
                    {'ref': str(new_obj_info[6]) + '/' + str(new_obj_info[0]) + '/' + str(new_obj_info[4]), 'description': fs_desc})
                singleton_featureSet_elements = {}  # free memory
                singleton_obj = {}  # free memory

            if partial_featureSet_elements:
                fs_name = pg_obj_name + ".base_genome-" + base_genome_obj_name + ".non-core_pangenome.FeatureSet"
                fs_desc = pg_obj_name + ".base_genome-" + base_genome_obj_name + " non-core pangenome features"
                partial_obj = {'description': fs_desc,
                               'elements': partial_featureSet_elements
                               }
                new_obj_info = wsClient.save_objects({
                    'workspace': params['workspace_name'],
                    'objects': [
                        {'type': 'KBaseCollections.FeatureSet',
                         'data': partial_obj,
                         'name': fs_name,
                         'meta': {},
                         'provenance': provenance
                         }]
                })[0]
                objects_created.append(
                    {'ref': str(new_obj_info[6]) + '/' + str(new_obj_info[0]) + '/' + str(new_obj_info[4]), 'description': fs_desc})
                partial_featureSet_elements = {}  # free memory
                partial_obj = {}  # free memory

            if core_featureSet_elements:
                if outgroup_genome_refs_cnt == 0:
                    fs_name = pg_obj_name + ".base_genome-" + base_genome_obj_name + ".core_pangenome.FeatureSet"
                    fs_desc = pg_obj_name + ".base_genome-" + base_genome_obj_name + " core pangenome features"
                else:
                    fs_name = pg_obj_name + ".base_genome-" + base_genome_obj_name + ".clade-specific_core_pangenome.FeatureSet"
                    fs_desc = pg_obj_name + ".base_genome-" + base_genome_obj_name + " clade-specific core pangenome features"
                core_obj = {'description': fs_desc,
                            'elements': core_featureSet_elements
                            }
                new_obj_info = wsClient.save_objects({
                    'workspace': params['workspace_name'],
                    'objects': [
                        {'type': 'KBaseCollections.FeatureSet',
                         'data': core_obj,
                         'name': fs_name,
                         'meta': {},
                         'provenance': provenance
                         }]
                })[0]
                objects_created.append(
                    {'ref': str(new_obj_info[6]) + '/' + str(new_obj_info[0]) + '/' + str(new_obj_info[4]), 'description': fs_desc})
                core_featureSet_elements = {}  # free memory
                core_obj = {}  # free memory

            if univ_featureSet_elements:
                fs_name = pg_obj_name + ".base_genome-" + base_genome_obj_name + ".non-specific_core_pangenome.FeatureSet"
                fs_desc = pg_obj_name + ".base_genome-" + base_genome_obj_name + " non-specific core pangenome features"
                univ_obj = {'description': fs_desc,
                            'elements': univ_featureSet_elements
                            }
                new_obj_info = wsClient.save_objects({
                    'workspace': params['workspace_name'],
                    'objects': [
                        {'type': 'KBaseCollections.FeatureSet',
                         'data': univ_obj,
                         'name': fs_name,
                         'meta': {},
                         'provenance': provenance
                         }]
                })[0]
                objects_created.append(
                    {'ref': str(new_obj_info[6]) + '/' + str(new_obj_info[0]) + '/' + str(new_obj_info[4]), 'description': fs_desc})
                univ_featureSet_elements = {}  # free memory
                univ_obj = {}  # free memory

        # Get mapping of base genes to pangenome
        #
        self.log(console, "DETERMINING MAPPING OF BASE GENES TO PANGENOME")
        base_to_compare_redundant_map = dict()
        base_singletons = dict()
        base_cores = dict()
        base_universals = dict()
        for cluster in pg_obj['orthologs']:
            genomes_seen = dict()
            base_fids = []
            compare_genomes_seen = []
            outgroup_genomes_seen = []
            for cluster_member in cluster['orthologs']:
                feature_id = cluster_member[0]
                feature_len_maybe = cluster_member[1]
                genome_ref = cluster_member[2]
                genomes_seen[genome_ref] = True
                if genome_ref == base_genome_ref:
                    base_fids.append(feature_id)
            if base_genome_ref in genomes_seen:
                universal = True
                core = True
                singleton = True
                for genome_ref in compare_genome_refs:
                    if genome_ref in genomes_seen:
                        singleton = False
                        compare_genomes_seen.append(True)
                    else:
                        universal = False
                        core = False
                        compare_genomes_seen.append(False)
                for genome_ref in outgroup_genome_refs:
                    if genome_ref in genomes_seen:
                        singleton = False
                        core = False
                    else:
                        universal = False
                for base_fid in base_fids:
                    base_to_compare_redundant_map[base_fid] = compare_genomes_seen
                    if universal:
                        base_universals[base_fid] = True
                    elif core:
                        base_cores[base_fid] = True
                    elif singleton:
                        base_singletons[base_fid] = True

        # Get positions of genes in base genome
        #
        self.log(console, "READING BASE GENOME COORDS")
        sorted_base_contig_ids = []
        sorted_base_contig_lens = []
        unsorted_contig_lens = dict()
        sorted_contig_order = dict()
        feature_contig_id = dict()
        feature_pos_in_contig = dict()
        feature_order = []
        sum_contig_lens = 0

        # hopefully info sitting in Genome obj
        if 'contig_ids' in base_genome_obj and base_genome_obj['contig_ids'] != None:
            for contig_i, contig_id in enumerate(base_genome_obj['contig_ids']):
                contig_len = base_genome_obj['contig_lengths'][contig_i]
                unsorted_contig_lens[contig_id] = contig_len
                sum_contig_lens += contig_len

        # otherwise have to get contig ids from Assembly or ContigSet obj
        else:
            # Get genome_assembly_refs
            base_genome_assemby_ref = None
            base_genome_assembly_type = None
            if ('contigset_ref' not in base_genome_obj or base_genome_obj['contigset_ref'] == None) \
               and ('assembly_ref' not in base_genome_obj or base_genome_obj['assembly_ref'] == None):
                msg = "Genome " + base_genome_obj_name + \
                    " (ref:" + base_genome_ref + ") " + genome_sci_name_by_ref[base_genome_ref] + \
                    " MISSING BOTH contigset_ref AND assembly_ref.  Cannot process.  Exiting."
                self.log(console, msg)
                #self.log(invalid_msgs, msg)
                #continue
                raise ValueError(msg)
            elif 'assembly_ref' in base_genome_obj and base_genome_obj['assembly_ref'] != None:
                msg = "Genome " + base_genome_obj_name + \
                    " (ref:" + base_genome_ref + ") " + \
                    genome_sci_name_by_ref[base_genome_ref] + \
                    " USING assembly_ref: " + str(base_genome_obj['assembly_ref'])
                self.log(console, msg)
                base_genome_assembly_ref = base_genome_obj['assembly_ref']
                base_genome_assembly_type = 'assembly'
            elif 'contigset_ref' in base_genome_obj and base_genome_obj['contigset_ref'] != None:
                msg = "Genome " + base_genome_obj_name + \
                    " (ref:" + base_genome_ref + ") " + \
                    genome_sci_name_by_ref[base_genome_ref] + \
                    " USING contigset_ref: " + str(base_genome_obj['contigset_ref'])
                self.log(console, msg)
                base_genome_assembly_ref = base_genome_obj['contigset_ref']
                base_genome_assembly_type = 'contigset'

            # get assembly obj and read contig ids and lengths (both contigset obj and assembly obj have list of contigs that
            try:
                #objects_list = wsClient.get_objects2({'objects':[{'ref':input_ref}]})['data']
                ass_obj = wsClient.get_objects([{'ref': base_genome_assembly_ref}])[0]['data']
            except:
                raise ValueError("unable to fetch assembly: " + base_genome_assembly_ref)

            if base_genome_assembly_type == 'assembly':
                for contig_key in ass_obj['contigs'].keys():
                    contig_id = ass_obj['contigs'][contig_key]['contig_id']
                    contig_len = ass_obj['contigs'][contig_key]['length']
                    #print ("CONTIG_ID: '"+str(contig_id)+"' CONTIG_LEN: '"+str(contig_len)+"'\n")  # DEBUG
                    unsorted_contig_lens[contig_id] = contig_len
                    sum_contig_lens += contig_len
            else:  # contigset obj
                for contig in ass_obj['contigs']:
                    contig_id = contig['id']
                    contig_len = contig['length']
                    unsorted_contig_lens[contig_id] = contig_len
                    sum_contig_lens += contig_len

        # order contigs by length and store by contig_id
        for order_i, contig_id in enumerate(sorted(unsorted_contig_lens, key=unsorted_contig_lens.__getitem__, reverse=True)):
            #print ("STORING CONTIG ORDER: '"+str(order_i)+"' for CONTIG_ID: '"+str(contig_id)+"'\n")  # DEBUG
            sorted_contig_order[contig_id] = order_i
            sorted_base_contig_ids.append(contig_id)
            sorted_base_contig_lens.append(unsorted_contig_lens[contig_id])
            feature_order.append([])

        for feature in base_genome_obj['features']:
            if 'protein_translation' in feature and feature['protein_translation'] != None and feature['protein_translation'] != '':
                fid = feature['id']
                #print ("FEATURE_ID: '"+str(fid)+"'\n")  # DEBUG
                feature_contig_id[fid] = feature['location'][0][0]
                beg = feature['location'][0][1]
                strand = feature['location'][0][2]
                len = feature['location'][0][3]
                if strand == '-':
                    feature_pos_in_contig[fid] = beg - int(len / 2)
                else:
                    feature_pos_in_contig[fid] = beg + int(len / 2)
                contig_i = sorted_contig_order[feature_contig_id[fid]]
                feature_order[contig_i].append(fid)

        # Draw Circle Plot with matplotlib
        #
        self.log(console, "CREATING CIRCLE PLOT")
        img_dpi = 200
        img_units = "in"
        img_pix_width = 2000
        img_in_width = round(float(img_pix_width) / float(img_dpi), 2)
        img_html_width = img_pix_width // 4

        #genome_ring_scale_factor = 0.8
        genome_ring_scale_factor = 1.0 / compare_genomes_cnt
        #img_pix_width = img_dpi * compare_genomes_cnt * genome_ring_scale_factor

        origin_gap_angle = 20
        mark_width = 0.1
        ellipse_to_circle_scaling = 1.0
        ellipse_center_x = 0.50
        ellipse_center_y = 0.50
        ellipse_center = (ellipse_center_x, ellipse_center_y)
        lw_to_coord_scale = 0.005
        max_unscaled_rings = 4
        unscaled_ring_lw = 30
        outer_ring_radius = 0.8
        min_inner_radius = 0.3

        if compare_genomes_cnt <= max_unscaled_rings:
            gene_bar_lw = unscaled_ring_lw
            inner_radius = outer_ring_radius - lw_to_coord_scale * compare_genomes_cnt * gene_bar_lw
        else:
            inner_radius = min_inner_radius
            gene_bar_lw = genome_ring_scale_factor * (outer_ring_radius - min_inner_radius) / lw_to_coord_scale
        #genome_ring_spacing = 0.05 * gene_bar_lw
        genome_ring_spacing = 0.0
        gene_bar_lw -= genome_ring_spacing
        #self.log(console, "gene_bar_lw: "+str(gene_bar_lw))  # DEBUG
        #self.log(console, "genome_ring_spacing: "+str(genome_ring_spacing))  # DEBUG
        #self.log(console, "inner_radius: "+str(inner_radius))  # DEBUG
        #genome_ring_spacing = 0.05 * gene_bar_lw
        #genome_ring_spacing = 0.3 * gene_bar_lw
        #lw_to_coord_scale = 0.1
        base_singleton_color = "red"
        base_core_color = "magenta"
        #hit_core_color = "darkmagenta"
        hit_core_color = "magenta"
        #base_univ_color = "blue"
        base_univ_color = "darkblue"
        hit_univ_color = "darkblue"
        #base_nonspecific_core_color = "purple"
        #hit_nonspecific_core_color = "purple"
        base_nonspecific_core_color = "darkblue"
        hit_nonspecific_core_color = "darkblue"
        #base_partial_color = "cyan"
        #hit_partial_color = "deepskyblue"
        base_partial_color = "deepskyblue"
        #hit_partial_color = "gray"  # too dark
        hit_partial_color = "lightgray"

        # Build image
        fig = pyplot.figure()
        fig.set_size_inches(img_in_width, img_in_width)
        ax = pyplot.subplot2grid((1, 1), (0, 0), rowspan=1, colspan=1)

        # Let's turn off visibility of all tic labels and boxes here
        for ax in fig.axes:
            ax.xaxis.set_visible(False)  # remove axis labels and tics
            ax.yaxis.set_visible(False)
            for t in ax.get_xticklabels() + ax.get_yticklabels():  # remove tics
                t.set_visible(False)
            ax.spines['top'].set_visible(False)     # Get rid of top axis line
            ax.spines['bottom'].set_visible(False)  # bottom axis line
            ax.spines['left'].set_visible(False)    # left axis line
            ax.spines['right'].set_visible(False)   # right axis line

        # Add marks for genomes
        ax = fig.axes[0]
        base_contig_pos = 0
        for contig_i, contig_feature_order in enumerate(feature_order):
            if contig_i > 0:
                base_contig_pos += sorted_base_contig_lens[contig_i - 1]

            # use base genome for angle
            #
            for fid in contig_feature_order:

                # base genome ring color
                if fid in base_singletons:
                    gene_color = base_singleton_color
                    this_mark_width = 2 * mark_width
                    z_level = 4
                elif fid in base_cores:
                    gene_color = base_core_color
                    hit_gene_color = hit_core_color
                    this_mark_width = mark_width
                    z_level = 3
                elif fid in base_universals:
                    if outgroup_genome_refs_cnt == 0:
                        gene_color = base_nonspecific_core_color
                        hit_gene_color = hit_nonspecific_core_color
                    else:
                        gene_color = base_univ_color
                        hit_gene_color = hit_univ_color
                    this_mark_width = mark_width
                    z_level = 2
                else:
                    gene_color = base_partial_color
                    hit_gene_color = hit_partial_color
                    this_mark_width = mark_width
                    z_level = 1
                gene_pos = base_contig_pos + feature_pos_in_contig[fid]

                arc_beg = 90 - origin_gap_angle / 2.0 - \
                    (360 - origin_gap_angle) * (float(gene_pos) / float(sum_contig_lens)) - this_mark_width
                arc_end = 90 - origin_gap_angle / 2.0 - \
                    (360 - origin_gap_angle) * (float(gene_pos) / float(sum_contig_lens)) + this_mark_width

                # draw base genome gene
                #gene_bar_radius = inner_radius + 0.5*gene_bar_lw*lw_to_coord_scale

                # old (with base in center)
                #gene_bar_radius = inner_radius
                # new (with base on outside)
                #gene_bar_radius = inner_radius + 0.5*(compare_genomes_cnt)*(gene_bar_lw+genome_ring_spacing)*lw_to_coord_scale
                #gene_bar_radius = inner_radius + lw_to_coord_scale * (compare_genomes_cnt + 0.5) * (gene_bar_lw+genome_ring_spacing)
                #gene_bar_radius = inner_radius + lw_to_coord_scale * (compare_genomes_cnt-1) * (gene_bar_lw+genome_ring_spacing) + lw_to_coord_scale * (this_gene_bar_lw+genome_ring_spacing)
                this_gene_bar_lw = unscaled_ring_lw
                if gene_bar_lw == unscaled_ring_lw:
                    gene_bar_radius = inner_radius + lw_to_coord_scale * \
                        (compare_genomes_cnt) * (gene_bar_lw + genome_ring_spacing)
                else:
                    gene_bar_radius = inner_radius + lw_to_coord_scale * (compare_genomes_cnt - 1) * (
                        gene_bar_lw + genome_ring_spacing) + 0.5 * lw_to_coord_scale * (this_gene_bar_lw + genome_ring_spacing)

                #self.log(console, str('BASE')+" gene_bar_radius: "+str(gene_bar_radius))  # DEBUG
                gene_x_radius = 1.0 * gene_bar_radius
                gene_y_radius = ellipse_to_circle_scaling * gene_bar_radius

                gene_arc = Arc(ellipse_center, gene_x_radius, gene_y_radius,
                               theta1=arc_beg, theta2=arc_end,
                               edgecolor=gene_color, lw=this_gene_bar_lw, alpha=1.0, zorder=z_level)  # facecolor does nothing (no fill for Arc)
                ax.add_patch(gene_arc)

                # add homolog rings
                for genome_i, hit_flag in enumerate(base_to_compare_redundant_map[fid]):
                    if not hit_flag:
                        continue
#                    if fid in base_cores:
#                        #gene_color = "darkmagenta"
#                        gene_color = "magenta"
#                        z_level = 3
#                    elif fid in base_universals:
#                        gene_color = "darkblue"
#                        z_level = 2
#                    else:
#                        gene_color = "deepskyblue"
#                        z_level = 1
                    #gene_bar_radius = inner_radius + 0.5*(compare_genomes_cnt-(genome_i+1))*(gene_bar_lw+genome_ring_spacing)*lw_to_coord_scale
                    #gene_bar_radius = inner_radius + lw_to_coord_scale * (compare_genomes_cnt - (genome_i+1) + 0.5) * (gene_bar_lw+genome_ring_spacing)
                    gene_bar_radius = inner_radius + lw_to_coord_scale * \
                        (compare_genomes_cnt - (genome_i + 1)) * (gene_bar_lw + genome_ring_spacing)
                    #self.log(console, str(genome_i)+" gene_bar_radius: "+str(gene_bar_radius))  # DEBUG
                    gene_x_radius = 1.0 * gene_bar_radius
                    gene_y_radius = ellipse_to_circle_scaling * gene_bar_radius
                    gene_arc = Arc(ellipse_center, gene_x_radius, gene_y_radius,
                                   theta1=arc_beg, theta2=arc_end,
                                   edgecolor=hit_gene_color, lw=gene_bar_lw, alpha=1.0, zorder=z_level)  # facecolor does nothing (no fill for Arc)
                    ax.add_patch(gene_arc)

        # Add labels
        base_text_fontsize = 10
        if gene_bar_lw < unscaled_ring_lw:
            text_fontsize = int(max_unscaled_rings * base_text_fontsize * gene_bar_lw / unscaled_ring_lw)
            if text_fontsize > base_text_fontsize:
                text_fontsize = base_text_fontsize
        else:
            text_fontsize = base_text_fontsize
        text_color = "#606060"
        label_margin = 0.005
        y_downshift = 0.0075 * ellipse_to_circle_scaling
        #text_y_delta = 0.25
        #label_margin = 0.0
        #y_downshift = 0.0
        #text_y_delta = 0.0

        label_angle = (math.pi / 180) * (90 - origin_gap_angle / 2.0 - (360 - origin_gap_angle))
        #label_radius = inner_radius + 0.5*gene_bar_lw*lw_to_coord_scale
        #label_radius = 0.5*inner_radius
        #label_radius = 0.5*inner_radius + text_y_delta*compare_genomes_cnt*(gene_bar_lw+genome_ring_spacing)*lw_to_coord_scale
        #label_radius = inner_radius + text_y_delta * lw_to_coord_scale * (compare_genomes_cnt + 0.5) * (gene_bar_lw+genome_ring_spacing)
        #label_radius = inner_radius + lw_to_coord_scale * (compare_genomes_cnt + 0.5) * (gene_bar_lw+genome_ring_spacing)
        this_gene_bar_lw = unscaled_ring_lw
        if gene_bar_lw == unscaled_ring_lw:
            label_radius = inner_radius + lw_to_coord_scale * \
                (compare_genomes_cnt) * (gene_bar_lw + genome_ring_spacing)
        else:
            label_radius = inner_radius + lw_to_coord_scale * (compare_genomes_cnt - 1) * (
                gene_bar_lw + genome_ring_spacing) + 0.5 * lw_to_coord_scale * (this_gene_bar_lw + genome_ring_spacing)
        label_radius *= 0.5  # why is this necessary?
        x_shift = label_radius * math.cos(label_angle)
        y_shift = label_radius * math.sin(label_angle)
        label_x_pos = ellipse_center_x + x_shift + label_margin
        label_y_pos = ellipse_center_y + y_shift - y_downshift
        label = str(0)
        ax.text(label_x_pos, label_y_pos, label, verticalalignment="bottom",
                horizontalalignment="left", color=text_color, fontsize=text_fontsize, zorder=1)

        for genome_i, genome_ref in enumerate(compare_genome_refs):
            #label_radius = 0.5*inner_radius + text_y_delta*(compare_genomes_cnt-(genome_i+1))*(gene_bar_lw+genome_ring_spacing)*lw_to_coord_scale
            #label_radius = inner_radius + text_y_delta * lw_to_coord_scale * (compare_genomes_cnt - (genome_i+1) + 0.5) * (gene_bar_lw+genome_ring_spacing)
            #label_radius = inner_radius + lw_to_coord_scale * (compare_genomes_cnt - (genome_i+1) + 0.5) * (gene_bar_lw+genome_ring_spacing)
            #label_radius = inner_radius + lw_to_coord_scale * (compare_genomes_cnt-(genome_i+1+1))*(gene_bar_lw+genome_ring_spacing) + 0.5*lw_to_coord_scale * (gene_bar_lw+genome_ring_spacing)
            label_radius = inner_radius + lw_to_coord_scale * \
                (compare_genomes_cnt - (genome_i + 1)) * (gene_bar_lw + genome_ring_spacing)
            label_radius *= 0.5  # why is this necessary?
            x_shift = label_radius * math.cos(label_angle)
            y_shift = label_radius * math.sin(label_angle)
            label_x_pos = ellipse_center_x + x_shift + label_margin
            label_y_pos = ellipse_center_y + y_shift - y_downshift
            label = str(genome_i + 1)
            ax.text(label_x_pos, label_y_pos, label, verticalalignment="bottom",
                    horizontalalignment="left", color=text_color, fontsize=text_fontsize, zorder=1)

        # Add color key
        key_x_margin = 0.01
        key_y_margin = 0.01
        key_line_spacing = 0.015
        key_x_label_offset = 0.018
        box_gap = key_line_spacing / 6.0
        box_h = key_line_spacing - box_gap
        box_w = box_h

        # base genome key
        ax.text(key_x_margin / 2.0, 1.0 - key_y_margin,
                genome_sci_name_by_ref[base_genome_ref], verticalalignment="bottom", horizontalalignment="left", color=text_color, fontsize=text_fontsize, zorder=1)

        key_config = [{'name': 'base singletons',
                       'y_shift': 1,
                       'color': base_singleton_color
                       },
                      {'name': 'non-core',
                       'y_shift': 2,
                       'color': base_partial_color
                       }
                      ]
        if outgroup_genome_refs_cnt == 0:
            key_config.extend(
                [{'name': 'core',
                    'y_shift': 3,
                    'color': base_nonspecific_core_color
                  }
                 ])
        else:
            key_config.extend(
                [{'name': 'clade-specific core',
                    'y_shift': 3,
                    'color': base_core_color
                  },
                 {'name': 'core + outgroup',
                    'y_shift': 4,
                    'color': base_univ_color
                  }
                 ])
        for k_config in key_config:
            key_box = Rectangle((key_x_margin, 1.0 - (key_y_margin + k_config['y_shift'] * key_line_spacing)),
                                box_w, box_h, facecolor=k_config['color'], edgecolor=text_color, alpha=1.0, zorder=1)
            ax.add_patch(key_box)
            ax.text(key_x_margin + key_x_label_offset, 1.0 - (key_y_margin + box_gap +
                                                              k_config['y_shift'] * key_line_spacing), k_config['name'], verticalalignment="bottom", horizontalalignment="left", color=text_color, fontsize=text_fontsize, zorder=1)

        # rest of pangenome key
        ax.text(key_x_margin / 2.0, 1.0 - (key_y_margin + 5.5 * key_line_spacing), "Pangenome",
                verticalalignment="bottom", horizontalalignment="left", color=text_color, fontsize=text_fontsize, zorder=1)

        key_config = [{'name': 'non-core',
                       'y_shift': 6.5,
                       'color': hit_partial_color
                       }
                      ]
        if outgroup_genome_refs_cnt == 0:
            key_config.extend([
                {'name': 'core',
                 'y_shift': 7.5,
                         'color': hit_nonspecific_core_color
                 }
            ])
        else:
            key_config.extend([
                {'name': 'clade-specific core',
                 'y_shift': 7.5,
                         'color': hit_core_color
                 },
                {'name': 'core + outgroup',
                 'y_shift': 8.5,
                 'color': hit_univ_color
                 }
            ])
        for k_config in key_config:
            key_box = Rectangle((key_x_margin, 1.0 - (key_y_margin + k_config['y_shift'] * key_line_spacing)),
                                box_w, box_h, facecolor=k_config['color'], edgecolor=text_color, alpha=1.0, zorder=1)
            ax.add_patch(key_box)
            ax.text(key_x_margin + key_x_label_offset, 1.0 - (key_y_margin + box_gap +
                                                              k_config['y_shift'] * key_line_spacing), k_config['name'], verticalalignment="bottom", horizontalalignment="left", color=text_color, fontsize=text_fontsize, zorder=1)

        # Save circle plot
        #
        self.log(console, "SAVING CIRCLE PLOT")
        png_file = base_genome_obj_name + '-pangenome_circle.png'
        pdf_file = base_genome_obj_name + '-pangenome_circle.pdf'
        output_png_file_path = os.path.join(html_output_dir, png_file)
        output_pdf_file_path = os.path.join(html_output_dir, pdf_file)
        fig.savefig(output_png_file_path, dpi=img_dpi)
        fig.savefig(output_pdf_file_path, format='pdf')

        # build report object
        #
        self.log(console, "CREATING HTML REPORT")
        reportName = 'kb_phylogenomics_report_' + str(uuid.uuid4())
        reportObj = {'objects_created': [],
                     'direct_html_link_index': 0,
                     'file_links': [],
                     'html_links': [],
                     'workspace_name': params['workspace_name'],
                     'report_object_name': reportName
                     }
        reportObj['objects_created'] = objects_created

        # build html report
        #
        circle_img_height = 1000
        cell_padding = 0
        cell_spacing = 10
        #cell_spacing = 0
        cell_border = 0
        sp = '&nbsp;'
        text_color = "#606060"
        font_size = '3'
        space_fontsize = '1'
        bar_char = '.'
        bar_fontsize = '1'
        bar_width = 50
        num_bars_per_node = 2 + 1

        html_report_lines = []
        html_report_lines += ['<html>']
        html_report_lines += ['<head>']
        html_report_lines += ['<title>KBase Pangenome Homolog Circle Plot</title>']
        html_report_lines += ['</head>']
        html_report_lines += ['<body bgcolor="white">']
        html_report_lines += ['<table cellpadding="' +
                              str(cell_padding) + '" cellspacing="' + str(cell_spacing) + '" border="' + str(cell_border) + '">']

        # add circle image
        circle_rowspan = 2 * (compare_genomes_cnt + outgroup_genome_refs_cnt + 1)
        html_report_lines += ['<tr>']
        html_report_lines += ['<td valign="middle" align="left" rowspan="' + str(circle_rowspan) + '">']
        html_report_lines += ['<img src="' + png_file + '" height=' + str(circle_img_height) + '>']
        html_report_lines += ['</td>']

        # add labels
        for filler_line_i in range((compare_genomes_cnt + outgroup_genome_refs_cnt + 1) // 2):
            if filler_line_i > 0:
                html_report_lines += ['<tr>']
            html_report_lines += ['<td>' + sp + '</td></tr>']
        html_report_lines += ['<td valign="top" align="left"><font color="' + str(text_color) + '" size="' + str(
            font_size) + '"><nobr><b>' + "genome " + str(0) + '</b></nobr></font></td>']
        html_report_lines += ['<td valign="top" align="left"><font color="' + str(text_color) + '" size="' + str(
            font_size) + '"><nobr><b>' + str(genome_sci_name_by_ref[base_genome_ref]) + '</b></nobr></font></td>']
        html_report_lines += ['</tr>']
        for genome_i, genome_ref in enumerate(compare_genome_refs):
            html_report_lines += ['<tr>']
            html_report_lines += ['<td valign="top" align="left"><font color="' + str(text_color) + '" size="' + str(
                font_size) + '"><nobr>' + "genome " + str(genome_i + 1) + '</nobr></font></td>']
            html_report_lines += ['<td valign="top" align="left"><font color="' + str(text_color) + '" size="' + str(
                font_size) + '"><nobr>' + str(genome_sci_name_by_ref[genome_ref]) + '</nobr></font></td>']
            html_report_lines += ['</tr>']
        for genome_i, genome_ref in enumerate(outgroup_genome_refs):
            html_report_lines += ['<tr>']
            html_report_lines += ['<td valign="top" align="left"><font color="' +
                                  str(text_color) + '" size="' + str(font_size) + '"><nobr><i>' + "outgroup" + '</i></nobr></font></td>']
            html_report_lines += ['<td valign="top" align="left"><font color="' + str(text_color) + '" size="' + str(
                font_size) + '"><nobr><i>' + str(genome_sci_name_by_ref[genome_ref]) + '</i></nobr></font></td>']
            html_report_lines += ['</tr>']
        for filler_line_i in range((compare_genomes_cnt + outgroup_genome_refs_cnt + 1) // 2):
            html_report_lines += ['<tr><td>' + sp + '</td></tr>']

        # close
        html_report_lines += ['</table>']
        html_report_lines += ['</body>']
        html_report_lines += ['</html>']

        html_report_str = "\n".join(html_report_lines)
        #reportObj['direct_html'] = html_report_str

        # write html to file and upload
        self.log(console, "SAVING AND UPLOADING HTML REPORT")
        html_file = os.path.join(html_output_dir, 'pan_circle_plot_report.html')
        with open(html_file, 'w', 0) as html_handle:
            html_handle.write(html_report_str)
        dfu = DFUClient(self.callbackURL)
        try:
            png_upload_ret = dfu.file_to_shock({'file_path': output_png_file_path,
                                                'make_handle': 0})
            #'pack': 'zip'})
        except:
            raise ValueError('Logging exception loading png_file to shock')

        try:
            pdf_upload_ret = dfu.file_to_shock({'file_path': output_pdf_file_path,
                                                'make_handle': 0})
            #'pack': 'zip'})
        except:
            raise ValueError('Logging exception loading pdf_file to shock')

        try:
            #upload_ret = dfu.file_to_shock({'file_path': html_file,
            upload_ret = dfu.file_to_shock({'file_path': html_output_dir,
                                            'make_handle': 0,
                                            'pack': 'zip'})
        except:
            raise ValueError('Logging exception loading html_report to shock')

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

        # save report object
        #
        reportClient = KBaseReport(self.callbackURL, token=ctx['token'], service_ver=SERVICE_VER)
        #report_info = report.create({'report':reportObj, 'workspace_name':params['workspace_name']})
        report_info = reportClient.create_extended_report(reportObj)

        output = {'report_name': report_info['name'], 'report_ref': report_info['ref']}

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
        output = {}
        raise NotImplementedError
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
        output = {}
        raise NotImplementedError
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
        output = {}
        raise NotImplementedError
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
           "input_speciesTree_ref" of type "data_obj_ref", parameter
           "save_featuresets" of type "bool", parameter
           "skip_missing_genomes" of type "bool", parameter
           "enforce_genome_version_match" of type "bool"
        :returns: instance of type "view_pan_phylo_Output" -> structure:
           parameter "report_name" of String, parameter "report_ref" of String
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN view_pan_phylo

        ### STEP 0: basic init
        console = []
        self.log(console, 'Running view_pan_phylo(): ')
        self.log(console, "\n" + pformat(params))

        # ws obj info indices
        [OBJID_I, NAME_I, TYPE_I, SAVE_DATE_I, VERSION_I, SAVED_BY_I, WSID_I,
         WORKSPACE_I, CHSUM_I, SIZE_I, META_I] = range(11)  # object_info tuple

        #SERVICE_VER = 'dev'  # DEBUG
        SERVICE_VER = 'release'
        token = ctx['token']
        try:
            wsClient = workspaceService(self.workspaceURL, token=token)
        except:
            raise ValueError("unable to instantiate wsClient")
        headers = {'Authorization': 'OAuth ' + token}
        env = os.environ.copy()
        env['KB_AUTH_TOKEN'] = token

        # param checks
        required_params = ['input_speciesTree_ref',
                           'input_pangenome_ref'
                           ]
        for arg in required_params:
            if arg not in params or params[arg] == None or params[arg] == '':
                raise ValueError("Must define required param: '" + arg + "'")

        # load provenance
        provenance = [{}]
        if 'provenance' in ctx:
            provenance = ctx['provenance']
        provenance[0]['input_ws_objects'] = [str(params['input_speciesTree_ref']),
                                             str(params['input_pangenome_ref'])
                                             ]

        # set the output paths
        timestamp = int((datetime.utcnow() - datetime.utcfromtimestamp(0)).total_seconds() * 1000)
        output_dir = os.path.join(self.scratch, 'output.' + str(timestamp))
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        html_output_dir = os.path.join(output_dir, 'html_output')
        if not os.path.exists(html_output_dir):
            os.makedirs(html_output_dir)

        # get speciesTree
        #
        input_ref = params['input_speciesTree_ref']
        speciesTree_name = None
        try:
            input_obj_info = wsClient.get_object_info_new({'objects': [{'ref': input_ref}]})[0]
            input_obj_type = re.sub('-[0-9]+\.[0-9]+$', "", input_obj_info[TYPE_I])  # remove trailing version
            speciesTree_name = input_obj_info[NAME_I]
        except Exception as e:
            raise ValueError('Unable to get object from workspace: (' + input_ref + ')' + str(e))
        accepted_input_types = ["KBaseTrees.Tree"]
        if input_obj_type not in accepted_input_types:
            raise ValueError("Input object of type '" + input_obj_type +
                             "' not accepted.  Must be one of " + ", ".join(accepted_input_types))
        if len(wsClient.get_objects([{'ref': input_ref}])[0]['data']['default_node_labels']) <= 3:
            raise ValueError("Input species tree must have more than two species.")

        # get set obj
        try:
            speciesTree_obj = wsClient.get_objects([{'ref': input_ref}])[0]['data']
        except:
            raise ValueError("unable to fetch speciesTree: " + input_ref)

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

        genome_ref_by_versionless = dict()
        for genome_ref in genome_refs:
            (ws_id, obj_id, version) = genome_ref.split('/')
            genome_ref_by_versionless[ws_id+'/'+obj_id] = genome_ref


        # get object names, sci names, protein-coding gene counts, and SEED annot
        #
        genome_obj_name_by_ref = dict()
        genome_sci_name_by_ref = dict()
        genome_sci_name_by_id = dict()
        uniq_genome_ws_ids = dict()


        # get names from genome object
        #
        for genome_ref in genome_refs:

            # get genome object name
            input_ref = genome_ref
            try:
                input_obj_info = wsClient.get_object_info_new({'objects': [{'ref': input_ref}]})[0]
                input_obj_type = re.sub('-[0-9]+\.[0-9]+$', "", input_obj_info[TYPE_I])  # remove trailing version
                input_name = input_obj_info[NAME_I]
                uniq_genome_ws_ids[input_obj_info[WSID_I]] = True

            except Exception as e:
                raise ValueError('Unable to get object from workspace: (' + input_ref + ')' + str(e))
            accepted_input_types = ["KBaseGenomes.Genome"]
            if input_obj_type not in accepted_input_types:
                raise ValueError("Input object of type '" + input_obj_type +
                                 "' not accepted.  Must be one of " + ", ".join(accepted_input_types))

            genome_obj_name_by_ref[genome_ref] = input_name

            try:
                genome_obj = wsClient.get_objects([{'ref': input_ref}])[0]['data']
            except:
                raise ValueError("unable to fetch genome: " + input_ref)

            # sci name
            genome_sci_name_by_ref[genome_ref] = genome_obj['scientific_name']
            genome_sci_name_by_id[genome_id_by_ref[genome_ref]] = genome_obj['scientific_name']


        # get pangenome
        #
        self.log(console, "GETTING PANGENOME OBJECT")
        input_ref = params['input_pangenome_ref']
        try:
            input_obj_info = wsClient.get_object_info_new({'objects': [{'ref': input_ref}]})[0]
            input_obj_type = re.sub('-[0-9]+\.[0-9]+$', "", input_obj_info[TYPE_I])  # remove trailing version
            pg_obj_name = input_obj_info[NAME_I]
            pg_obj_name = pg_obj_name.replace(" ", "_")
        except Exception as e:
            raise ValueError('Unable to get object from workspace: (' + input_ref + ')' + str(e))
        accepted_input_types = ["KBaseGenomes.Pangenome"]
        if input_obj_type not in accepted_input_types:
            raise ValueError("Input object of type '" + input_obj_type +
                             "' not accepted.  Must be one of " + ", ".join(accepted_input_types))

        try:
            pg_obj = wsClient.get_objects([{'ref': input_ref}])[0]['data']
        except:
            raise ValueError("unable to fetch genome: " + input_ref)


        # check for each species tree genome in pangenome, and possibly adjust
        #    species tree if skipping allowed (reverse not required)
        #
        missing_in_pangenome = []
        missing_msg = []
        updated_pg_genome_refs = []
        for pg_genome_ref in pg_obj['genome_refs']:
            (ws_id, obj_id, version) = pg_genome_ref.split('/')
            genome_ref_versionless = ws_id+'/'+obj_id
            if genome_ref_versionless in genome_ref_by_versionless:
                updated_pg_genome_refs.append(genome_ref_by_versionless[genome_ref_versionless])
        for genome_ref in genome_refs:
            if params.get('enforce_genome_version_match') and int(params.get('enforce_genome_version_match')) == 1:
                if genome_ref not in pg_obj['genome_refs']:
                    missing_in_pangenome.append(genome_ref)
            else:
                if genome_ref not in updated_pg_genome_refs:
                    missing_in_pangenome.append(genome_ref)

        # at least one genome is missing
        if len(missing_in_pangenome) > 0:
            for genome_ref in missing_in_pangenome:
                missing_msg.append("\t" + 'MISSING PANGENOME CALCULATION FOR: ' + 'ref: '+genome_ref + ', obj_name: '+genome_obj_name_by_ref[genome_ref]+', sci_name: '+genome_sci_name_by_ref[genome_ref])

            # if strict, then abort
            if not params.get('skip_missing_genomes') or int(params.get('skip_missing_genomes')) != 1:
                error_msg = "ABORT: You must include the following additional Genomes in the Pangenome Calculation first (or select the SKIP option)\n<p>\n"
                error_msg += "\n<br>\n".join(missing_msg)
                raise ValueError(error_msg)

            # if skipping, then remove from genome_refs list and from tree
            else:

                # update list
                new_genome_refs = []
                for genome_ref in genome_refs:
                    if genome_ref in missing_in_pangenome:
                        continue
                    new_genome_refs.append(genome_ref)
                genome_refs = new_genome_refs
                self.log(console, "SKIP option selected. If you wish to include the below Genomes, you must include in Pangenome Calculation first\n")
                self.log(console, "\n".join(missing_msg))

                # update tree
                prune_list = []
                for n in species_tree.traverse():
                    if n.is_leaf():
                        genome_id = n.name
                        if genome_ref_by_id[genome_id] in missing_in_pangenome:
                            prune_list.append(n.name)
                # remove skipped genomes
                if len(prune_list) > 0:
                    species_tree.prune (prune_list)


        # get internal node ids based on sorted genome_refs of children
        #
        node_ids_by_refs = dict()
        genome_ref_to_node_ids_by_refs = dict()
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
            node_ids_by_refs[node_ref_id] = node_num_id

            # point each genome at its nodes
            for genome_ref in leaf_refs:
                if genome_ref not in genome_ref_to_node_ids_by_refs:
                    genome_ref_to_node_ids_by_refs[genome_ref] = []
                genome_ref_to_node_ids_by_refs[genome_ref].append(node_ref_id)


        # determine pangenome accumulations of core, partial, and singleton
        #
        cluster_hits = dict()
        nodes_hit_by_gene = dict()
        for node_ref_id in node_ids_by_refs.keys():
            cluster_hits[node_ref_id] = []

        cluster_num = -1  # cluster ids themselves start from 1
        for homolog_cluster in pg_obj['orthologs']:
            cluster_num += 1
            for node_ref_id in node_ids_by_refs.keys():
                cluster_hits[node_ref_id].append(0)

            nodes_hit = dict()
            for gene in homolog_cluster['orthologs']:
                gene_id = gene[0]
                probably_gene_len_dont_need = gene[1]
                genome_ref = gene[2]
                (ws_id, obj_id, version) = genome_ref.split('/')
                genome_ref = genome_ref_by_versionless[ws_id+'/'+obj_id]

                if genome_ref not in genome_ref_to_node_ids_by_refs:
                    continue
                for node_ref_id in genome_ref_to_node_ids_by_refs[genome_ref]:
                    if node_ref_id not in nodes_hit:
                        nodes_hit[node_ref_id] = dict()
                    nodes_hit[node_ref_id][genome_ref] = True

                    # store features
                    if node_ref_id not in nodes_hit_by_gene:
                        nodes_hit_by_gene[node_ref_id] = dict()
                    if cluster_num not in nodes_hit_by_gene[node_ref_id]:
                        nodes_hit_by_gene[node_ref_id][cluster_num] = dict()
                    if genome_ref not in nodes_hit_by_gene[node_ref_id][cluster_num]:
                        nodes_hit_by_gene[node_ref_id][cluster_num][genome_ref] = []

                    nodes_hit_by_gene[node_ref_id][cluster_num][genome_ref].append(gene_id)

            # sum counts
            for node_ref_id in nodes_hit.keys():
                for genome_ref in nodes_hit[node_ref_id].keys():
                    cluster_hits[node_ref_id][cluster_num] += 1

        # calc accumulations
        clusters_total = dict()
        clusters_singletons = dict()
        clusters_core = dict()
        clusters_partial = dict()
        clusters_singletons_by_node_and_cluster_flag = dict()
        clusters_core_by_node_and_cluster_flag = dict()
        clusters_partial_by_node_and_cluster_flag = dict()
        for node_ref_id in node_ids_by_refs.keys():
            clusters_total[node_ref_id] = 0
            clusters_singletons[node_ref_id] = 0
            clusters_core[node_ref_id] = 0
            clusters_partial[node_ref_id] = 0
            clusters_singletons_by_node_and_cluster_flag[node_ref_id] = dict()
            clusters_core_by_node_and_cluster_flag[node_ref_id] = dict()
            clusters_partial_by_node_and_cluster_flag[node_ref_id] = dict()

            for cluster_num, hit_cnt in enumerate(cluster_hits[node_ref_id]):
                if hit_cnt > 0:
                    clusters_total[node_ref_id] += 1
                    if hit_cnt == 1:
                        clusters_singletons[node_ref_id] += 1
                        clusters_singletons_by_node_and_cluster_flag[node_ref_id][cluster_num] = True

                    elif hit_cnt == node_size[node_ref_id]:
                        clusters_core[node_ref_id] += 1
                        clusters_core_by_node_and_cluster_flag[node_ref_id][cluster_num] = True
                    else:
                        clusters_partial[node_ref_id] += 1
                        clusters_partial_by_node_and_cluster_flag[node_ref_id][cluster_num] = True

        # get min and max cluster cnts
        INSANE_VALUE = 10000000000000000
        max_clusters_cnt = -INSANE_VALUE
        min_clusters_cnt = INSANE_VALUE
        for node_ref_id in node_ids_by_refs.keys():
            if clusters_total[node_ref_id] > max_clusters_cnt:
                max_clusters_cnt = clusters_total[node_ref_id]
            if clusters_total[node_ref_id] < min_clusters_cnt:
                min_clusters_cnt = clusters_total[node_ref_id]

            self.log(console, "NODE: " + node_ref_id + " MIN: " +
                     str(min_clusters_cnt) + " MAX: " + str(max_clusters_cnt))  # DEBUG

        # Create FeatureSet objects for nodes
        #
        objects_created = []
        if 'save_featuresets' not in params or params['save_featuresets'] == None or params['save_featuresets'] == '' or int(params['save_featuresets']) != 1:
            self.log(console, "SKIPPING FEATURESETS")
        else:
            self.log(console, "SAVING FEATURESETS")

            for node_ref_id in sorted(node_ids_by_refs, key=node_ids_by_refs.get):

                node_num_id = str(node_ids_by_refs[node_ref_id])

                self.log(console, "calculating feature sets for node " + str(node_num_id))

                # Core
                if clusters_core[node_ref_id] > 0:

                    self.log(console, "\t" + "adding CORE.  Num clusters: " + str(clusters_core[node_ref_id]))

                    # build core featureset elements
                    core_featureSet_elements = {}
                    for cluster_num in sorted(clusters_core_by_node_and_cluster_flag[node_ref_id].keys()):
                        for genome_ref in nodes_hit_by_gene[node_ref_id][cluster_num].keys():
                            for gene_id in nodes_hit_by_gene[node_ref_id][cluster_num][genome_ref]:
                                if gene_id in core_featureSet_elements:
                                    core_featureSet_elements[gene_id].append(genome_ref)
                                else:
                                    core_featureSet_elements[gene_id] = [genome_ref]

                    # build object
                    fs_name = pg_obj_name + ".node-" + str(node_num_id) + ".core_pangenome.FeatureSet"
                    fs_desc = pg_obj_name + ".node-" + str(node_num_id) + " core pangenome features"
                    core_obj = {'description': fs_desc,
                                'elements': core_featureSet_elements
                                }
                    new_obj_info = wsClient.save_objects({
                        'workspace': params['workspace_name'],
                        'objects': [
                            {'type': 'KBaseCollections.FeatureSet',
                             'data': core_obj,
                             'name': fs_name,
                             'meta': {},
                             'provenance': provenance
                             }]
                    })[0]
                    objects_created.append(
                        {'ref': str(new_obj_info[6]) + '/' + str(new_obj_info[0]) + '/' + str(new_obj_info[4]), 'description': fs_desc})
                    core_featureSet_elements = {}  # free memory
                    core_obj = {}  # free memory

                # Singletons
                if clusters_singletons[node_ref_id] > 0:

                    self.log(console, "\t" + "adding SINGLETON.  Num clusters: " +
                             str(clusters_singletons[node_ref_id]))

                    # build singleton featureset elements
                    singleton_featureSet_elements = {}
                    for cluster_num in sorted(clusters_singletons_by_node_and_cluster_flag[node_ref_id].keys()):
                        for genome_ref in nodes_hit_by_gene[node_ref_id][cluster_num].keys():
                            for gene_id in nodes_hit_by_gene[node_ref_id][cluster_num][genome_ref]:
                                if gene_id in singleton_featureSet_elements:
                                    singleton_featureSet_elements[gene_id].append(genome_ref)
                                else:
                                    singleton_featureSet_elements[gene_id] = [genome_ref]

                    # build object
                    fs_name = pg_obj_name + ".node-" + str(node_num_id) + ".singleton_pangenome.FeatureSet"
                    fs_desc = pg_obj_name + ".node-" + str(node_num_id) + " singleton pangenome features"
                    singleton_obj = {'description': fs_desc,
                                     'elements': singleton_featureSet_elements
                                     }
                    new_obj_info = wsClient.save_objects({
                        'workspace': params['workspace_name'],
                        'objects': [
                            {'type': 'KBaseCollections.FeatureSet',
                             'data': singleton_obj,
                             'name': fs_name,
                             'meta': {},
                             'provenance': provenance
                             }]
                    })[0]
                    objects_created.append(
                        {'ref': str(new_obj_info[6]) + '/' + str(new_obj_info[0]) + '/' + str(new_obj_info[4]), 'description': fs_desc})
                    singleton_featureSet_elements = {}  # free memory
                    singleton_obj = {}  # free memory

                # Partial pangenome
                if clusters_partial[node_ref_id] > 0:

                    self.log(console, "\t" + "adding PARTIAL.  Num clusters: " + str(clusters_partial[node_ref_id]))

                    # build partial featureset elements
                    partial_featureSet_elements = {}
                    for cluster_num in sorted(clusters_partial_by_node_and_cluster_flag[node_ref_id].keys()):
                        for genome_ref in nodes_hit_by_gene[node_ref_id][cluster_num].keys():
                            for gene_id in nodes_hit_by_gene[node_ref_id][cluster_num][genome_ref]:
                                if gene_id in partial_featureSet_elements:
                                    partial_featureSet_elements[gene_id].append(genome_ref)
                                else:
                                    partial_featureSet_elements[gene_id] = [genome_ref]

                    # build object
                    fs_name = pg_obj_name + ".node-" + str(node_num_id) + ".non-core_pangenome.FeatureSet"
                    fs_desc = pg_obj_name + ".node-" + str(node_num_id) + " non-core pangenome features"
                    partial_obj = {'description': fs_desc,
                                   'elements': partial_featureSet_elements
                                   }
                    new_obj_info = wsClient.save_objects({
                        'workspace': params['workspace_name'],
                        'objects': [
                            {'type': 'KBaseCollections.FeatureSet',
                             'data': partial_obj,
                             'name': fs_name,
                             'meta': {},
                             'provenance': provenance
                             }]
                    })[0]
                    objects_created.append(
                        {'ref': str(new_obj_info[6]) + '/' + str(new_obj_info[0]) + '/' + str(new_obj_info[4]), 'description': fs_desc})
                    partial_featureSet_elements = {}  # free memory
                    partial_obj = {}  # free memory

        # Draw tree (we already instantiated Tree above)
        #
        png_file = speciesTree_name + '-pangenome.png'
        pdf_file = speciesTree_name + '-pangenome.pdf'
        output_png_file_path = os.path.join(html_output_dir, png_file)
        output_pdf_file_path = os.path.join(html_output_dir, pdf_file)

        # init ETE3 accessory objects
        ts = ete3.TreeStyle()

        # customize
        min_pie_size = 1000
        max_pie_size = 2000
        # scale of everything is goofy in circle tree mode, and pie size affects type size and line thickness.  ugh.
        leaf_fontsize = 500
        node_fontsize = 500
        ts.mode = "c"  # circular tree graph
        #ts.arc_start = -180 # 0 degrees = 3 o'clock
        #ts.arc_span = 180
        ts.show_leaf_name = True
        ts.show_branch_length = False
        ts.show_branch_support = True
        #ts.scale = 50 # 50 pixels per branch length unit
        ts.branch_vertical_margin = 5  # pixels between adjacent branches
        #ts.title.add_face(ete3.TextFace(params['output_name']+": "+params['desc'], fsize=10), column=0)

        node_style = ete3.NodeStyle()
        node_style["fgcolor"] = "#606060"  # for node balls
        node_style["size"] = 10  # for node balls (gets reset based on support)
        node_style["vt_line_color"] = "#606060"
        node_style["hz_line_color"] = "#606060"
        node_style["vt_line_width"] = 100  # 2
        node_style["hz_line_width"] = 100  # 2
        node_style["vt_line_type"] = 0  # 0 solid, 1 dashed, 2 dotted
        node_style["hz_line_type"] = 0

        leaf_style = ete3.NodeStyle()
        leaf_style["fgcolor"] = "#ffffff"  # for node balls
        leaf_style["size"] = 100  # for node balls (we're using it to add space)
        leaf_style["vt_line_color"] = "#606060"  # unecessary
        leaf_style["hz_line_color"] = "#606060"
        leaf_style["vt_line_width"] = 100  # 2
        leaf_style["hz_line_width"] = 100  # 2
        leaf_style["vt_line_type"] = 0  # 0 solid, 1 dashed, 2 dotted
        leaf_style["hz_line_type"] = 0

        for n in species_tree.traverse("preorder"):
            if n.is_leaf():
                style = leaf_style
                genome_id = n.name
                #n.name = genome_sci_name_by_id[genome_id]
                n.name = None
                leaf_name_disp = genome_sci_name_by_id[genome_id]
                n.add_face(ete3.TextFace(leaf_name_disp, fsize=leaf_fontsize), column=0, position="branch-right")

            else:
                leaf_refs = []
                for genome_id in n.get_leaf_names():
                    leaf_refs.append(genome_ref_by_id[genome_id])
                node_ref_id = "+".join(sorted(leaf_refs))
                node_num_id = node_ids_by_refs[node_ref_id]
                node_name_disp = str(node_num_id)
                #n.add_face (ete3.TextFace(node_name_disp, fsize=node_fontsize),column=0, position="branch-right")
                n.add_face(ete3.TextFace(' ' + node_name_disp + ' ', fsize=node_fontsize), column=0)

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
                pie_size = int(min_pie_size + float(max_pie_size - min_pie_size) *
                               float(clusters_total[node_ref_id] - min_clusters_cnt) / float(max_clusters_cnt - min_clusters_cnt))
                singleton_perc = round(
                    100.0 * float(clusters_singletons[node_ref_id]) / float(clusters_total[node_ref_id]), 1)
                core_perc = round(100.0 * float(clusters_core[node_ref_id]) / float(clusters_total[node_ref_id]), 1)
                partial_perc = round(100.0 - core_perc - singleton_perc, 1)

                pie_w = pie_h = pie_size
                pie_percs = [singleton_perc, partial_perc, core_perc]
                pie_colors = ["IndianRed", "Orchid", "DodgerBlue"]
                pie_line_color = "White"

                this_pieFace = ete3.PieChartFace(pie_percs, pie_w, pie_h, pie_colors, pie_line_color)
                n.add_face(this_pieFace, column=1)

            n.set_style(style)

        # save images
        dpi = 300
        img_units = "in"
        img_pix_width = 1200
        img_in_width = round(float(img_pix_width) / float(dpi), 1)
        img_html_width = img_pix_width // 2
        species_tree.render(output_png_file_path, w=img_in_width, units=img_units, dpi=dpi, tree_style=ts)
        species_tree.render(output_pdf_file_path, w=img_in_width, units=img_units, tree_style=ts)  # dpi irrelevant

        # build report object
        #
        reportName = 'kb_phylogenomics_report_' + str(uuid.uuid4())
        reportObj = {'objects_created': [],
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
        horiz_sp = sp + sp + sp + sp
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
        html_report_lines += ['<table cellpadding="' +
                              str(cell_padding) + '" cellspacing="' + str(cell_spacing) + '" border="' + str(cell_border) + '">']

        # add tree image
        html_report_lines += ['<tr>']
        html_report_lines += ['<td valign="top" align="left" rowspan="' +
                              str(num_bars_per_node * len(node_ids_by_refs)) + '">']
        html_report_lines += ['<img src="' + png_file + '" height=' + str(tree_img_height) + '>']
        html_report_lines += ['</td>']

        # add key and bar graph
        max_cnt = 0
        for node_ref_id in node_order_by_ref:
            if clusters_total[node_ref_id] > max_cnt:
                max_cnt = clusters_total[node_ref_id]

        for node_i, node_ref_id in enumerate(node_order_by_ref):
            node_id = node_ids_by_refs[node_ref_id]
            if node_i > 0:
                html_report_lines += ['<tr>']

            # vals
            cat_cnts = dict()
            cat_percs = dict()
            cat_cnts['TOTAL'] = clusters_total[node_ref_id]
            cat_cnts['singleton'] = clusters_singletons[node_ref_id]
            cat_cnts['perfect core'] = clusters_core[node_ref_id]
            cat_cnts['partial'] = clusters_total[node_ref_id] - \
                clusters_singletons[node_ref_id] - clusters_core[node_ref_id]
            cat_percs['TOTAL'] = '100'
            cat_percs['singleton'] = round(100.0 * float(clusters_singletons[node_ref_id]
                                                         ) / float(clusters_total[node_ref_id]), 1)
            cat_percs['perfect core'] = round(100.0 * float(clusters_core[node_ref_id]
                                                            ) / float(clusters_total[node_ref_id]), 1)
            if cat_cnts['partial'] == 0:
                cat_percs['partial'] = 0.0
            else:
                cat_percs['partial'] = round(100.0 - cat_percs['perfect core'] - cat_percs['singleton'], 1)

            # node id
            node_label = 'NODE ' + str(node_id)
            html_report_lines += ['<td rowspan="' + str(num_bars_per_node) + '" valign="top" align="right"><font color="' + str(
                text_color) + '" size="' + str(font_size) + '"><b><nobr>' + str(node_label) + '</nobr></b></font></td>']
            html_report_lines += ['<td rowspan="' + str(num_bars_per_node) +
                                  '"><font size="' + str(space_fontsize) + '">' + horiz_sp + '</font></td>']

            for cat_i, cat in enumerate(cat_order):
                if cat_i > 0:
                    html_report_lines += ['<tr>']
                # cat name
                html_report_lines += ['<td valign="top" align="right"><font color="' +
                                      str(text_color) + '" size="' + str(font_size) + '"><nobr>' + cat + '</nobr></font></td>']
                html_report_lines += ['<td><font size="' + str(space_fontsize) + '">' + horiz_sp + '</font></td>']

                # cnt
                html_report_lines += ['<td valign="top" align="right"><font color="' +
                                      str(text_color) + '" size="' + str(font_size) + '">' + str(cat_cnts[cat]) + '</font></td>']
                html_report_lines += ['<td><font size="' + str(space_fontsize) + '">' + horiz_sp + '</font></td>']

                #perc
                html_report_lines += ['<td valign="top" align="right"><font color="' +
                                      str(text_color) + '" size="' + str(font_size) + '">' + str(cat_percs[cat]) + '%' + '</font></td>']
                html_report_lines += ['<td><font size="' + str(space_fontsize) + '">' + horiz_sp + '</font></td>']

                # bar
                this_width = int(round(float(bar_width) * (float(cat_cnts[cat]) / float(max_cnt)), 0))
                for cell_i in range(this_width):
                    html_report_lines += ['<td bgcolor="' + str(cat_colors[cat_i]) + '"><font size="' + str(
                        bar_fontsize) + '" color="' + str(cat_colors[cat_i]) + '">' + bar_char + '</font></td>']

                html_report_lines += ['</tr>']
                #html_report_lines += ['<tr><td><font size="'+str(space_fontsize)+'">'+sp+'</font></td></tr>']  # space for blank row
            html_report_lines += ['<tr><td><font size="' +
                                  str(space_fontsize) + '">' + sp + '</font></td></tr>']  # space for blank row

        # close
        html_report_lines += ['</table>']
        html_report_lines += ['</body>']
        html_report_lines += ['</html>']

        html_report_str = "\n".join(html_report_lines)
        #reportObj['direct_html'] = html_report_str

        # write html to file and upload
        html_file = os.path.join(html_output_dir, 'pan_phylo_report.html')
        with open(html_file, 'w', 0) as html_handle:
            html_handle.write(html_report_str)
        dfu = DFUClient(self.callbackURL)
        try:
            png_upload_ret = dfu.file_to_shock({'file_path': output_png_file_path,
                                                'make_handle': 0})
            #'pack': 'zip'})
        except:
            raise ValueError('Logging exception loading png_file to shock')

        try:
            pdf_upload_ret = dfu.file_to_shock({'file_path': output_pdf_file_path,
                                                'make_handle': 0})
            #'pack': 'zip'})
        except:
            raise ValueError('Logging exception loading pdf_file to shock')

        try:
            #upload_ret = dfu.file_to_shock({'file_path': html_file,
            upload_ret = dfu.file_to_shock({'file_path': html_output_dir,
                                            'make_handle': 0,
                                            'pack': 'zip'})
        except:
            raise ValueError('Logging exception loading html_report to shock')

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

        # attach any created objects
        reportObj['objects_created'] = objects_created

        # save report object
        #
        reportClient = KBaseReport(self.callbackURL, token=ctx['token'], service_ver=SERVICE_VER)
        #report_info = report.create({'report':reportObj, 'workspace_name':params['workspace_name']})
        report_info = reportClient.create_extended_report(reportObj)

        output = {'report_name': report_info['name'], 'report_ref': report_info['ref']}

        #END view_pan_phylo

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method view_pan_phylo return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]

    def find_homologs_with_genome_context(self, ctx, params):
        """
        :param params: instance of type
           "find_homologs_with_genome_context_Input"
           (find_homologs_with_genome_context() ** ** show homolgous genes
           across multiple genomes within genome context against species
           tree) -> structure: parameter "workspace_name" of type
           "workspace_name" (** Common types), parameter
           "input_featureSet_ref" of type "data_obj_ref", parameter
           "input_speciesTree_ref" of type "data_obj_ref", parameter
           "save_per_genome_featureSets" of type "bool", parameter
           "neighbor_thresh" of Long, parameter "ident_thresh" of Double,
           parameter "overlap_fraction" of Double, parameter "e_value" of
           Double, parameter "bitscore" of Double, parameter "color_seed" of
           Double
        :returns: instance of type "find_homologs_with_genome_context_Output"
           -> structure: parameter "report_name" of String, parameter
           "report_ref" of String
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN find_homologs_with_genome_context

        #### STEP 0: init
        ##
        console = []
        invalid_msgs = []
        created_objects = []
        report = ''
        self.log(console, 'Running find_homologs_with_genome_context() with params=')
        self.log(console, "\n" + pformat(params))

        # ws obj info indices
        [OBJID_I, NAME_I, TYPE_I, SAVE_DATE_I, VERSION_I, SAVED_BY_I, WSID_I,
         WORKSPACE_I, CHSUM_I, SIZE_I, META_I] = range(11)  # object_info tuple

        # paths
        timestamp = int((datetime.utcnow() - datetime.utcfromtimestamp(0)).total_seconds() * 1000)
        output_dir = os.path.join(self.scratch, 'output_' + str(timestamp))
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # clients
        #SERVICE_VER = 'dev'  # DEBUG
        SERVICE_VER = 'beta'
        #SERVICE_VER = 'release'
        token = ctx['token']
        try:
            wsClient = workspaceService(self.workspaceURL, token=token)
        except:
            raise ValueError("unable to instantiate wsClient")
        headers = {'Authorization': 'OAuth ' + token}
        env = os.environ.copy()
        env['KB_AUTH_TOKEN'] = token

        # additional clients
        try:
            dfuClient = DFUClient(self.callbackURL)
        except:
            raise ValueError("unable to instantiate dfuClient")
        try:
            blastClient = kb_blast(url=self.callbackURL, token=token, service_ver=SERVICE_VER)  # SDK Local
            #blastClient = kb_blast(url=self.serviceWizardURL, token=token, service_ver=SERVICE_VER)  # Dynamic service
        except:
            raise ValueError("unable to instantiate blastClient")


        #### STEP 1: do some basic checks
        ##
        # param checks
        required_params = ['workspace_name',
                           'input_featureSet_ref',
                           'input_speciesTree_ref',
                           'ident_thresh',
                           'e_value',
                           'bitscore',
                           'overlap_fraction',
                           'neighbor_thresh'
                           ]
        for arg in required_params:
            if arg not in params or params[arg] == None or params[arg] == '':
                raise ValueError("Must define required param: '" + arg + "'")


        #### STEP 2: load the method provenance from the context object
        ##
        self.log(console, "SETTING PROVENANCE")  # DEBUG
        provenance = [{}]
        if 'provenance' in ctx:
            provenance = ctx['provenance']
        # add additional info to provenance here, in this case the input data object reference
        provenance[0]['input_ws_objects'] = []
        provenance[0]['input_ws_objects'].append(params['input_featureSet_ref'])
        provenance[0]['input_ws_objects'].append(params['input_speciesTree_ref'])
        provenance[0]['service'] = 'kb_phylogenomics'
        provenance[0]['method'] = 'find_homologs_with_genome_context'


        #### STEP 3: Get tree and save as newick file and create GenomeSet object
        ##
        intree_ws_id = None
        try:
            objects = wsClient.get_objects([{'ref': params['input_speciesTree_ref']}])
            data = objects[0]['data']
            info = objects[0]['info']
            intree_name = info[NAME_I]
            intree_type_name = info[TYPE_I].split('.')[1].split('-')[0]
            intree_ws_id = info[WSID_I]

        except Exception as e:
            raise ValueError('Unable to fetch input_speciesTree_ref object from workspace: ' + str(e))
            #to get the full stack trace: traceback.format_exc()

        if intree_type_name == 'Tree':
            tree_in = data
        else:
            raise ValueError('Cannot yet handle input_tree type of: ' + intree_type_name)

        # store which genomes are in tree and save in GenomeSet object, store order
        genomes_in_tree = dict()
        genome_node_id_to_ref = dict()
        genome_ref_to_node_id = dict()
        tree_GS_name = intree_name+'.GenomeSet'
        tree_GS_obj = {'description': 'GenomeSet for '+intree_name,
                       'elements': dict()
                      }
        if 'ws_refs' not in tree_in:
            raise ValueError ("Species Tree missing ws_refs field.  Cannot continue.  Exiting...")
        for node_id in tree_in['ws_refs'].keys():
            genome_ref = tree_in['ws_refs'][node_id]['g'][0]
            genomes_in_tree[genome_ref] = node_id
            tree_GS_obj['elements'][node_id] = {'ref': genome_ref}
            genome_node_id_to_ref[node_id] = genome_ref
            genome_ref_to_node_id[genome_ref] = node_id

        # save newick file
        intree_newick_file_path = os.path.join(output_dir, intree_name + ".newick")
        self.log(console, 'writing intree file: ' + intree_newick_file_path)
        with open(intree_newick_file_path, 'w', 0) as intree_newick_file_handle:
            intree_newick_file_handle.write(tree_in['tree'])

        """
        # upload newick
        try:
            newick_upload_ret = dfuClient.file_to_shock({'file_path': intree_newick_file_path,
                                                  #'pack': 'zip'})
                                                   'make_handle': 0})
        except:
            raise ValueError('error uploading newick file to shock')
        """
        # save GenomeSet object for Tree
        try:
            genomeSet_obj_info_list = wsClient.list_objects(
                    {'ids': [intree_ws_id], 'type': "KBaseSearch.GenomeSet"})
        except Exception as e:
            raise ValueError("Unable to list GenomeSet objects from workspace: " + str(intree_ws_id) + " " + str(e))
        genomeSet_repeat = False
        genomeSet_ref = None
        for info in genomeSet_obj_info_list:
            if info[NAME_I] == tree_GS_name:
                genomeSet_repeat = True
                genomeSet_ref = '/'.join([str(info[WSID_I]),str(info[OBJID_I]),str(info[VERSION_I])])
                break
        if not genomeSet_repeat:
            try:
                genomeSet_obj_info = wsClient.save_objects({'workspace': params['workspace_name'],
                                                            'objects': [
                                                                {
                                                                    'type':'KBaseSearch.GenomeSet',
                                                                    'data':tree_GS_obj,
                                                                    'name':tree_GS_name,
                                                                    'meta':{},
                                                                    'provenance':[
                                                                        {
                                                                            'service':'kb_phylogenomics',
                                                                            'method':'find_homologs_with_genome_context',
                                                                            'input_ws_objects': [params['input_speciesTree_ref']]

                                                                        }
                                                                    ]
                                                                }]
                                                        })[0]
                tree_derived_genomeSet_ref = str(genomeSet_obj_info[WSID_I])+'/'+str(genomeSet_obj_info[OBJID_I])+'/'+str(genomeSet_obj_info[VERSION_I])

            except Exception as e:
                raise ValueError ("unable to save GenomeSet from Tree object: " + str(e))
                #to get the full stack trace: traceback.format_exc()
        else:
            tree_derived_genomeSet_ref = genomeSet_ref


        #### STEP 4: get genome names from tree
        ##
        genome_names = dict()
        for genome_ref in genomes_in_tree.keys():
            try:
                genome_obj_info = wsClient.get_object_info_new({'objects': [{'ref': genome_ref}]})[0]
                genome_names[genome_ref] = genome_obj_info[NAME_I]
            except Exception as e:
                raise ValueError('Unable to get genome object from workspace: (' + genome_ref + ')' + str(e))


        #### STEP 5: if labels defined, make separate newick-labels file
        ##     (NOTE: adjust IDs so ETE3 parse doesn't choke on conflicting chars)
        ##
        if 'default_node_labels' in tree_in:
            newick_labels_file = intree_name + '-labels.newick'
            output_newick_labels_file_path = os.path.join(output_dir, newick_labels_file)
            #default_row_ids = tree_in['default_row_labels']
            #new_ids = dict()
            #for row_id in default_row_ids.keys():
            #    new_ids[row_id] = default_row_ids[row_id]

            mod_newick_buf = tree_in['tree']
            mod_newick_buf = re.sub('\|', '%' + '|'.encode("hex"), mod_newick_buf)
            #for row_id in new_ids.keys():
            for node_id in tree_in['default_node_labels'].keys():
                label = tree_in['default_node_labels'][node_id]

                #self.log (console, "node "+node_id+" label B4: '"+label+"'")  # DEBUG
                label = re.sub(' \(kb[^\)]*\)', '', label)  # just get rid of problematic (kb|g.1234)
                label = re.sub('\s', '_', label)
                #label = re.sub('\/','%'+'/'.encode("hex"), label)
                #label = re.sub(r'\\','%'+'\\'.encode("hex"), label)
                #label = re.sub('\[','%'+'['.encode("hex"), label)
                #label = re.sub('\]','%'+']'.encode("hex"), label)
                label = re.sub('\(', '[', label)
                label = re.sub('\)', ']', label)
                label = re.sub('\:', '%' + ':'.encode("hex"), label)
                label = re.sub('\;', '%' + ';'.encode("hex"), label)
                label = re.sub('\|', '%' + '|'.encode("hex"), label)
                #self.log (console, "node "+node_id+" label AF: '"+label+"'")  # DEBUG
                #self.log (console, "NEWICK B4: '"+mod_newick_buf+"'")  # DEBUG
                mod_node_id = re.sub('\|', '%' + '|'.encode("hex"), node_id)
                mod_newick_buf = re.sub('\(' + mod_node_id + '\:', '(' + label + ':', mod_newick_buf)
                mod_newick_buf = re.sub('\,' + mod_node_id + '\:', ',' + label + ':', mod_newick_buf)
                #self.log (console, "NEWICK AF: '"+mod_newick_buf+"'")  # DEBUG

                #self.log(console, "new_id: '"+new_id+"' label: '"+label+"'")  # DEBUG

            mod_newick_buf = re.sub('_', ' ', mod_newick_buf)
            with open(output_newick_labels_file_path, 'w', 0) as output_newick_labels_file_handle:
                output_newick_labels_file_handle.write(mod_newick_buf)

            """
            # upload
            try:
                newick_labels_upload_ret = dfuClient.file_to_shock({'file_path': output_newick_labels_file_path,
                                                              #'pack': 'zip'})
                                                              'make_handle': 0})
            except:
                raise ValueError('error uploading newick labels file to shock')
            """


        #### STEP 6: read genome order in tree, ladderize to make row order consistent
        ##
        genome_ref_order = []
        newick_buf = tree_in['tree']
        t_without_labels = ete3.Tree(newick_buf)
        t_without_labels.ladderize()
        for genome_id in t_without_labels.get_leaf_names():
            genome_ref_order.append(genome_node_id_to_ref[genome_id])
        N_genomes = len(genome_ref_order)


        #### STEP 7: get query features from featureSet object
        ##
        input_ref = params['input_featureSet_ref']
        input_featureSet_name = None
        try:
            input_obj_info = wsClient.get_object_info_new({'objects': [{'ref': input_ref}]})[0]
            input_obj_type = re.sub('-[0-9]+\.[0-9]+$', "", input_obj_info[TYPE_I])  # remove trailing version
            input_featureSet_name = input_obj_info[NAME_I]
        except Exception as e:
            raise ValueError('Unable to get object from workspace: (' + input_ref + ')' + str(e))
        accepted_input_types = ["KBaseCollections.FeatureSet"]
        if input_obj_type not in accepted_input_types:
            raise ValueError("Input object " + input_featureSet_name + " of type '" + input_obj_type +
                             "' not accepted.  Must be one of " + ", ".join(accepted_input_types))
        try:
            featureSet_obj = wsClient.get_objects([{'ref': input_ref}])[0]['data']
        except:
            raise ValueError("unable to fetch featureSet: " + input_ref)

        # validate all genomes can be found in species tree
        genome_refs = []
        genome_ref_seen = dict()
        for element_id in featureSet_obj['elements'].keys():
            for genome_ref in featureSet_obj['elements'][element_id]:
                if genome_ref not in genome_ref_seen:
                    genome_ref_seen[genome_ref] = True
                    genome_refs.append(genome_ref)
        genomes_missing_from_tree = []
        for genome_ref in genome_ref_seen.keys():
            try:
                found_in_tree = genomes_in_tree[genome_ref]
            except:
                missing_genome_message = genomes_in_tree[genome_ref]+" ("+str(genome_ref)+")"
                if 'default_node_labels' in tree_in:
                    node_id = genomes_in_tree[genome_ref]
                    missing_genome_message += ' '+tree_in['default_node_labels'][node_id]
                genomes_missing_from_tree.append(missing_genome_message)

        if len(genomes_missing_from_tree) > 0:
            raise ValueError ("Species Tree missing genomes from FeatureSet.  Missing Genomes: "+", ".join(genomes_missing_from_tree))

        # store query features for later function lookup when genomes are pulled
        query_feature_function = dict()
        for element_id in featureSet_obj['elements'].keys():
            for genome_ref in featureSet_obj['elements'][element_id]:
                if genome_ref not in query_feature_function:
                    query_feature_function[genome_ref] = dict()
                query_feature_function[genome_ref][element_id] = 'unknown'


        #### STEP 8: determine feature order
        ##
        contig_id_by_genome_by_fid                = dict()
        sorted_contig_ids_by_genome               = dict()
        gene_fid_by_genome_by_contig_by_start_pos = dict()
        gene_order_by_genome_by_contig            = dict()
        [CONTIG_ID_I, BEG_I, STRAND_I, END_I]     = range(4)  # location tuple (string,int,string,int)

        for genome_ref in genome_ref_order:
            contig_id_by_genome_by_fid[genome_ref]                = dict()
            sorted_contig_ids_by_genome[genome_ref]               = []
            gene_fid_by_genome_by_contig_by_start_pos[genome_ref] = dict()

            try:
                self.log (console, "reading Genome "+str(genome_ref))
                genome_obj = wsClient.get_objects([{'ref': genome_ref}])[0]['data']
            except:
                raise ValueError("unable to fetch genome: " + genome_ref)


            # get Contig IDs and lengths
            contig_ids = []
            contig_lens = []
            if genome_obj.get('contig_ids') and genome_obj.get('contig_lengths'):
                contig_ids = genome_obj['contig_ids']
                contig_lens = genome_obj['contig_lengths']

            # else need to get contig IDs and lengths from assembly or contig_set
            else:
                # Get genome_assembly_refs
                this_genome_assemby_ref = None
                this_genome_assembly_type = None
                if not genome_obj.get('contigset_ref') and not genome_obj.get('assembly_ref'):
                    msg = "Genome ref:" + genome_ref + \
                          " MISSING BOTH contigset_ref AND assembly_ref.  Cannot process.  Exiting."
                    self.log(console, msg)
                    #self.log(invalid_msgs, msg)
                    #continue
                    raise ValueError(msg)
                elif genome_obj.get('assembly_ref'):
                    msg = "Genome ref:" + genome_ref + \
                          " USING assembly_ref: " + str(genome_obj['assembly_ref'])
                    self.log(console, msg)
                    this_genome_assembly_ref = genome_obj['assembly_ref']
                    this_genome_assembly_type = 'assembly'
                elif genome_obj.get('contigset_ref'):
                    msg = "Genome ref:" + genome_ref + \
                          " USING contigset_ref: " + str(genome_obj['contigset_ref'])
                    self.log(console, msg)
                    this_genome_assembly_ref = genome_obj['contigset_ref']
                    this_genome_assembly_type = 'contigset'

                # get assembly obj and read contig ids and lengths (both contigset obj and assembly obj have list of contigs that
                try:
                    #objects_list = wsClient.get_objects2({'objects':[{'ref':input_ref}]})['data']
                    ass_obj = wsClient.get_objects([{'ref': this_genome_assembly_ref}])[0]['data']
                except:
                    raise ValueError("unable to fetch assembly: " + this_genome_assembly_ref)

                if this_genome_assembly_type == 'assembly':
                    for contig_key in sorted(ass_obj['contigs'].keys()):
                        contig_ids.append(ass_obj['contigs'][contig_key]['contig_id'])
                        contig_lens.append(ass_obj['contigs'][contig_key]['length'])
                        #print ("CONTIG_ID: '"+str(contig_id)+"' CONTIG_LEN: '"+str(contig_len)+"'\n")  # DEBUG
                else:  # contigset obj
                    for contig in ass_obj['contigs']:
                        contig_ids.append(contig['id'])
                        contig_lens.append(contig['length'])

            # put contig ids in order by length
            contig_ids_by_len = dict()
            for contig_i,contig_id in enumerate(contig_ids):
                contig_len = contig_lens[contig_i]
                try:
                    len_seen = contig_ids_by_len[contig_len][0]
                except:
                    contig_ids_by_len[contig_len] = []
                contig_ids_by_len[contig_len].append(contig_id)
            for contig_len in sorted(contig_ids_by_len.keys(), reverse=True):
                for contig_id in contig_ids_by_len[contig_len]:
                    sorted_contig_ids_by_genome[genome_ref].append(contig_id)

            # read features
            for f in genome_obj['features']:
                fid = f['id']
                contig_id = f['location'][0][CONTIG_ID_I]
                start_pos = f['location'][0][BEG_I]
                """ note END_I is actually nucleotide length of gene, not stop pos
                if f['location'][0][BEG_I] < f['location'][0][END_I]:
                    start_pos = f['location'][0][BEG_I]
                    #stop_pos  = f['location'][0][END_I]
                else:
                    start_pos = f['location'][0][END_I]
                    #stop_pos  = f['location'][0][BEG_I]
                # DEBUG
                #if fid.startswith('DVU084'):
                #    self.log(console,"INITIAL GENE READ "+fid+" START_POS: "+str(start_pos))
                """
                if contig_id not in gene_fid_by_genome_by_contig_by_start_pos[genome_ref]:
                    gene_fid_by_genome_by_contig_by_start_pos[genome_ref][contig_id] = dict()
                if start_pos not in gene_fid_by_genome_by_contig_by_start_pos[genome_ref][contig_id]:
                    gene_fid_by_genome_by_contig_by_start_pos[genome_ref][contig_id][start_pos] = []

                gene_fid_by_genome_by_contig_by_start_pos[genome_ref][contig_id][start_pos].append(fid)
                contig_id_by_genome_by_fid[genome_ref][fid] = contig_id

                # capture function if a query gene
                if genome_ref in query_feature_function:
                    if fid in query_feature_function[genome_ref]:
                        query_feature_function[genome_ref][fid] = f['functions'][0]

            # sort genes by start pos within each contig
            gene_order_by_genome_by_contig[genome_ref] = dict()
            for contig_id in gene_fid_by_genome_by_contig_by_start_pos[genome_ref].keys():
                gene_order_by_genome_by_contig[genome_ref][contig_id] = []
                for start_pos in sorted(gene_fid_by_genome_by_contig_by_start_pos[genome_ref][contig_id].keys()):
                    for fid in gene_fid_by_genome_by_contig_by_start_pos[genome_ref][contig_id][start_pos]:
                        gene_order_by_genome_by_contig[genome_ref][contig_id].append(fid)
                        # DEBUG
                        #if fid.startswith('DVU084'):
                        #    self.log(console, "GENE "+fid+" STARTPOS: "+str(start_pos))

        #### STEP 9: make a separate featureSet with a single feature to run searches
        ##  Kludge until change BLASTp to accept multi-feature FeatureSet queries
        ##
        input_full_feature_ids = []
        individual_featureSet_refs = []
        individual_featureSet_names = []
        genome_ref_feature_id_delim = '.f:'

        for element_id in sorted(featureSet_obj['elements'].keys()):
            for genome_ref in featureSet_obj['elements'][element_id]:
                full_feature_id = genome_ref + genome_ref_feature_id_delim + element_id
                individual_FS_name = genome_ref.replace('/','_')+'_'+element_id+'.FeatureSet'

                individual_FS_prov = [{}]
                if 'provenance' in ctx:
                    individual_FS_prov = ctx['provenance']
                # add additional info to provenance here, in this case the input data object reference
                individual_FS_prov[0]['input_ws_objects'] = []
                individual_FS_prov[0]['input_ws_objects'].append(params['input_featureSet_ref'])
                individual_FS_prov[0]['service'] = 'kb_phylogenomics'
                individual_FS_prov[0]['method'] = 'find_homologs_with_genome_context'

                individual_FS_obj = {
                    'description': featureSet_obj['description']+' - '+element_id,
                    'elements': {
                        element_id: [genome_ref]
                    }
                }

                individual_FS_obj_info = wsClient.save_objects({'workspace': params['workspace_name'],
                                                                'objects': [
                                                                    {
                                                                        'type':'KBaseCollections.FeatureSet',
                                                                        'data':individual_FS_obj,
                                                                        'name':individual_FS_name,
                                                                        'meta':{},
                                                                        'provenance':individual_FS_prov,
                                                                        'hidden':1  # 1=True
                                                                    }]
                                                            })[0]
                #pprint(individual_FS_obj_info)
                self.log(console, "saved query feature as FS "+str(individual_FS_name))
                #self.log(console, "OBJ_INFO: "+pformat(individual_FS_obj_info))
                #self.log(console, "OBJ_DATA: "+pformat(individual_FS_obj))

                individual_FS_ref = str(individual_FS_obj_info[WSID_I])+'/'+str(individual_FS_obj_info[OBJID_I])+'/'+str(individual_FS_obj_info[VERSION_I])

                individual_featureSet_refs.append (individual_FS_ref)
                individual_featureSet_names.append (individual_FS_name)
                input_full_feature_ids.append (full_feature_id)


        #### STEP 10: run BLASTp searches to get homologs
        ##
        hits_by_query_and_genome_ref = dict()
        longest_feature_id_by_query = dict()
        max_hit_cnt = 0
        #hits_by_full_feature_id = dict()
        #feature_included = dict()
        #for query_i,individual_FS_ref in enumerate(individual_featureSet_refs):
        for query_i,query_full_feature_id in enumerate(input_full_feature_ids):
            longest_feature_id_by_query[query_full_feature_id] = 0

            [query_genome_ref, query_feature_id] = query_full_feature_id.split(genome_ref_feature_id_delim)

            #hits_by_full_feature_id[query_full_feature_id] = dict()

            input_individual_FS_ref = individual_featureSet_refs[query_i]
            input_individual_FS_name = individual_featureSet_names[query_i]
            output_individual_FS_name = input_individual_FS_name+'-'+intree_name+'.BLASTp_homologs'

            BLASTp_Params = {'workspace_name':       params['workspace_name'],
                             'input_one_ref':        input_individual_FS_ref,
                             'input_many_ref':       tree_derived_genomeSet_ref,
                             'output_filtered_name': output_individual_FS_name,
                             'ident_thresh':         params['ident_thresh'],
                             'e_value':              params['e_value'],
                             'bitscore':             params['bitscore'],
                             'overlap_fraction':     params['overlap_fraction'],
                             'maxaccepts':           1000  # hopefully won't exceed 1000 genomes!
                             }

            self.log (console, "running BLASTp for "+input_individual_FS_name)
            #self.log(console, "\n" + pformat(BLASTp_Params))

            blast_retVal = blastClient.BLASTp_Search(BLASTp_Params)
            this_report_name = blast_retVal['report_name']
            this_report_ref = blast_retVal['report_ref']

            try:
                this_report_obj = wsClient.get_objects([{'ref': this_report_ref}])[0]['data']
            except:
                raise ValueError("unable to fetch report: " + this_report_ref)

            # read hits and store hits for each genome
            if not this_report_obj.get('objects_created'):
                self.log (console, 'NO HITS within thresholds for query '+query_feature_id+' from genome '+query_genome_ref+'.  Consider relaxing BLASTp thresolds to get more hits')
                continue

            hits_ref = this_report_obj['objects_created'][0]['ref']
            created_objects.append({'ref': hits_ref, 'description': 'Homologs of '+genome_names[query_genome_ref]+' '+query_feature_id})
            try:
                hits_obj = wsClient.get_objects([{'ref': hits_ref}])[0]['data']
            except:
                raise ValueError("unable to fetch hits for " + output_individual_FS_name+'('+hits_ref+')')
            hits_by_query_and_genome_ref[query_full_feature_id] = dict()
            this_query_hit_cnt_by_genome_ref = dict()
            for hit_feature_id in hits_obj['elements'].keys():

                # record string length of feature ids
                if longest_feature_id_by_query[query_full_feature_id] < len(hit_feature_id):
                    longest_feature_id_by_query[query_full_feature_id] = len(hit_feature_id)


                # store hits by query and record number of hits to each genome
                for genome_ref in hits_obj['elements'][hit_feature_id]:
                    if genome_ref not in hits_by_query_and_genome_ref[query_full_feature_id].keys():
                        hits_by_query_and_genome_ref[query_full_feature_id][genome_ref] = []
                        this_query_hit_cnt_by_genome_ref[genome_ref] = 0

                    hits_by_query_and_genome_ref[query_full_feature_id][genome_ref].append(hit_feature_id)
                    this_query_hit_cnt_by_genome_ref[genome_ref] += 1
                    """
                    # handle duplicate queries
                    hit_full_feature_id = genome_ref + genome_ref_feature_id_delim + hit_feature_id
                    try:
                        included = feature_included[hit_full_feature_id]
                    except:
                        feature_included[hit_full_feature_id] = True
                        hits_by_full_feature_id[query_full_feature_id][hit_full_feature_id] = True
                    """
            for genome_ref in genome_ref_order:
                if genome_ref in this_query_hit_cnt_by_genome_ref:
                    if this_query_hit_cnt_by_genome_ref[genome_ref] > max_hit_cnt:
                        max_hit_cnt = this_query_hit_cnt_by_genome_ref[genome_ref]


        #### STEP 11: Determine proximity-based clusters within each contig
        ##
        cluster_by_genome_by_fid = dict()
        hits_by_genome_ref = dict()
        cluster_size_by_cluster_id = dict()

        # store hits by genome
        for query_full_feature_id in hits_by_query_and_genome_ref.keys():
            for genome_ref in hits_by_query_and_genome_ref[query_full_feature_id].keys():
                try:
                    hit_list = hits_by_genome_ref[genome_ref]
                except:
                    hits_by_genome_ref[genome_ref] = dict()
                for fid in hits_by_query_and_genome_ref[query_full_feature_id][genome_ref]:
                    hits_by_genome_ref[genome_ref][fid] = True

        # go through genomes and increment cluster when find hit fids
        cluster_n = 0
        cluster_size_by_cluster_id[cluster_n] = 0
        prox_i = 0
        prox_thresh = int(params['neighbor_thresh'])
        for genome_ref in sorted(gene_order_by_genome_by_contig.keys()):
            for contig_id in sorted(gene_order_by_genome_by_contig[genome_ref].keys()):
                #for fid in gene_order_by_genome_by_contig[genome_ref][contig_id]:
                for f_i,fid in enumerate(gene_order_by_genome_by_contig[genome_ref][contig_id]):

                    # DEBUG
                    #if fid.startswith('DVU084'):
                    #    self.log(console,"GENE ORDER "+genome_ref+" "+str(contig_id)+" "+fid+" "+str(f_i))

                    try:
                        hit = hits_by_genome_ref[genome_ref][fid]
                    except:
                        prox_i += 1
                        continue

                    if prox_i > prox_thresh:
                        cluster_n += 1
                        cluster_size_by_cluster_id[cluster_n] = 0
                    try:
                        genome_ref_hit_set = cluster_by_genome_by_fid[genome_ref]
                    except:
                        cluster_by_genome_by_fid[genome_ref] = dict()

                    cluster_by_genome_by_fid[genome_ref][fid] = cluster_n
                    cluster_size_by_cluster_id[cluster_n] += 1
                    prox_i = 0


        #### STEP 12: Create tree image in html dir
        ##
        html_output_dir = os.path.join(output_dir, 'output_html.' + str(timestamp))
        if not os.path.exists(html_output_dir):
            os.makedirs(html_output_dir)
        png_file = intree_name + '.png'
        #pdf_file = intree_name + '.pdf'
        output_png_file_path = os.path.join(html_output_dir, png_file)
        #output_pdf_file_path = os.path.join(output_dir, pdf_file)
        newick_buf = tree_in['tree']

        # switch to labels
        if 'default_node_labels' in tree_in:
            newick_buf = mod_newick_buf
        self.log(console, "NEWICK_BUF: '" + newick_buf + "'")

        # init ETE3 objects
        t = ete3.Tree(newick_buf)
        ts = ete3.TreeStyle()

        # ladderize to make row order consistent
        t.ladderize()

        # customize
        dpi = 300
        img_units = "in"
        img_pix_width = 1200
        height_to_genome_scaling = 1.00
        img_in_height = round(height_to_genome_scaling * max_hit_cnt * len(genome_ref_order) * float(img_pix_width) / float(dpi), 1)
        img_in_width = round(float(img_pix_width) / float(dpi), 1)
        img_html_width = img_pix_width // 4

        ##branch_vertical_margin = 31
        #branch_vertical_margin = 35

        # y: branch_vertical_margin
        # x: N_genomes
        # y = mg * x + bg
        # 35 = mg * 6 + bg
        # y2 = mg * 21 + bg
        # 35 - mg*6 = y2 - mg*21 -> mg*15 = y2 - 35 -> mg = (y2 - 35) / 15
        # bg = 35 - mg*6 = 35 - 6*(y2 - 35) / 15

        # guess y2=40
        y2 = 44.0
        mg = (y2 - 35.0) / 15.0
        bg = 35.0 - 6.0 * (y2 - 35.0) / 15.0
        branch_vertical_margin_float = mg * N_genomes + bg

        if max_hit_cnt > 1:
            ##hit_cnt_scaling = 0.65
            #hit_cnt_scaling = 0.6475

            # y: hit_cnt_scaling
            # x: max_hit_cnt
            # y = mh * x + bh
            # 0.6475*6 = 3.885 = mh * 6 + bh
            # y2 = mh * 5 + bh
            # 3.885 - mh*6 = y2 - mh*5 -> mh = 3.885 - y2
            # bh = 3.885 - mh*6 = 3.885 - 6*(3.885 - y2) = 6*y2 - 5*3.885 = 6*y2 - 19.425

            # guess y2=3.2375
            # guess y2=3.25
            # guess y2=3.20
            y2 = 3.20
            mh = 3.885 - y2
            bh = 6*y2 - 19.425
            hit_cnt_scaling = mh * max_hit_cnt + bh

            ##branch_vertical_margin_float = mg * N_genomes * max_hit_cnt * hit_cnt_scaling + bg
            #branch_vertical_margin_float = (mg * N_genomes + bg) * max_hit_cnt * hit_cnt_scaling
            branch_vertical_margin_float *= hit_cnt_scaling

        branch_vertical_margin = int(branch_vertical_margin_float + 0.5)

        #ts.show_leaf_name = True
        ts.show_leaf_name = False
        ts.show_branch_length = False
        ts.show_branch_support = True
        #ts.scale = 50 # 50 pixels per branch length unit
        ts.branch_vertical_margin = branch_vertical_margin
        #if max_hit_cnt > 1:
        #    ts.branch_vertical_margin = int(branch_vertical_margin * max_hit_cnt * hit_cnt_scaling + 0.5)  # pixels between adjacent branches
        #ts.branch_vertical_margin = branch_vertical_margin # pixels between adjacent branches

        title_disp = intree_name
        if 'desc' in params and params['desc'] != None and params['desc'] != '':
            title_disp += ': ' + params['desc']
        ts.title.add_face(ete3.TextFace(title_disp, fsize=10), column=0)

        node_style = ete3.NodeStyle()
        node_style["fgcolor"] = "#606060"  # for node balls
        node_style["size"] = 10  # for node balls (gets reset based on support)
        node_style["vt_line_color"] = "#606060"
        node_style["hz_line_color"] = "#606060"
        node_style["vt_line_width"] = 2
        node_style["hz_line_width"] = 2
        node_style["vt_line_type"] = 0  # 0 solid, 1 dashed, 2 dotted
        node_style["hz_line_type"] = 0

        leaf_style = ete3.NodeStyle()
        leaf_style["fgcolor"] = "#ffffff"  # for node balls
        leaf_style["size"] = 2  # for node balls (we're using it to add space)
        leaf_style["vt_line_color"] = "#606060"  # unecessary
        leaf_style["hz_line_color"] = "#606060"
        leaf_style["vt_line_width"] = 2
        leaf_style["hz_line_width"] = 2
        leaf_style["vt_line_type"] = 0  # 0 solid, 1 dashed, 2 dotted
        leaf_style["hz_line_type"] = 0

        for n in t.traverse():
            if n.is_leaf():
                style = copy.copy(leaf_style)
                #if "User Genome" in n.name:
                #    style["bgcolor"] = "#fafcc2"
            else:
                style = copy.copy(node_style)

                if n.support > 0.95:
                    style["size"] = 6
                elif n.support > 0.90:
                    style["size"] = 5
                elif n.support > 0.80:
                    style["size"] = 4
                else:
                    style["size"] = 2

            n.set_style(style)

        # save tree images
        #t.render(output_png_file_path, h=img_in_height, units=img_units, dpi=dpi, tree_style=ts)
        t.render(output_png_file_path, w=img_in_width, units=img_units, dpi=dpi, tree_style=ts)
        #t.render(output_pdf_file_path, w=img_in_width, units=img_units, tree_style=ts)  # dpi irrelevant


        #### STEP 13: build HTML table for hits
        ##
        border=0
        cellpadding=5
        cellspacing=5
        hit_cellpadding=5
        hit_cellspacing=2
        #fontsize=2
        header_fontsize=2
        genome_fontsize=3
        hit_fontsize=3
        genome_text_color='black'
        hit_text_color="#ffffff"
        #header_row_color="#ccccff"
        header_row_color="#eeeeee"
        #even_row_color="#ffffff"
        #odd_row_color="#eeeeee"
        hit_table_html = []
        hit_table_html += ['<table border='+str(border)+' cellpadding='+str(cellpadding)+' cellspacing='+str(cellspacing)+'>']

        # add header row with bait genes
        row_bg_color = header_row_color
        hit_table_html += ['<tr>']
        hit_table_html += ['<td></td>']
        hit_table_html += ['<td bgcolor='+'#ffffff'+' valign=middle align=right><b><font size='+str(header_fontsize)+'>'+'BAIT GENE'+'</font></b></td>']
        sorted_input_full_feature_ids = sorted(input_full_feature_ids)
        for query_i,query_full_feature_id in enumerate(sorted_input_full_feature_ids):
            [genome_ref,query_feature_id] = query_full_feature_id.split(genome_ref_feature_id_delim)
            bait_function = query_feature_function[genome_ref][query_feature_id]
            bait_function = bait_function.replace('(EC ','<br>(EC ')
            hit_table_html += ['<td bgcolor='+row_bg_color+' valign=middle align=center>'+'<font size='+str(header_fontsize)+'>'+'<b>'+query_feature_id+'</b>'+'<br>'+bait_function+'</font>'+'</td>']
        hit_table_html += ['</tr>']

        # add tree image
        tree_top_row_buffer = 1
        tree_bottom_row_buffer = 2
        #hit_table_html += ['<tr><td valign=top rowspan='+str(len(tree_GS_obj['elements'].keys()))+'>']
        hit_table_html += ['<tr><td colspan=1 rowspan='+str(len(genome_ref_order)+tree_top_row_buffer+tree_bottom_row_buffer+max_hit_cnt)+' valign=top align=left>']
        hit_table_html += ['<img width=' + str(img_html_width) + ' src="' + png_file + '">']
        hit_table_html += ['</td>']

        # add blank rows to get the vert spacing of the tree image against the hit rows right
        hit_table_html += ['<td rowspan=1 colspan='+str(len(input_full_feature_ids)+1)+'>&nbsp;</td>']
        hit_table_html += ['</tr>']
        for row_i in range(tree_top_row_buffer-1):
            hit_table_html += ['<tr>']
            hit_table_html += ['<td rowspan=1 colspan='+str(len(input_full_feature_ids)+1)+'>&nbsp;</td>']
            hit_table_html += ['</tr>']
        extra_rows = int(max_hit_cnt/2) - 1
        for row_i in range(extra_rows):
            hit_table_html += ['<tr>']
            hit_table_html += ['<td rowspan=1 colspan='+str(len(input_full_feature_ids)+1)+'>&nbsp;</td>']
            hit_table_html += ['</tr>']


        # add genome rows
        for genome_i,genome_ref in enumerate(genome_ref_order):
            #row_bg_color = odd_row_color
            #if (genome_i % 2) == 0:
            #    row_bg_color = even_row_color
            row_bg_color='#ffffff'
            node_id = genome_ref_to_node_id[genome_ref]
            if 'default_node_labels' in tree_in:
                label = tree_in['default_node_labels'][node_id]
            else:
                label = node_id

            hit_table_html += ['<tr>']
            #hit_table_html += ['<td bgcolor='+'#ffffff'+'></td>']
            disp_label = label
            if '(' in label:
                [part_1, part_2] = label.split('(')
                disp_label = '<b><i>'+part_1+'</i></b>'+'<br>'+'('+part_2
            else:
                disp_label = '<b><i>'+label+'</i></b>'
            link_open = '<A HREF="'+'https://narrative.kbase.us/#dataview/'+str(genome_ref)+'" target="'+str(genome_ref)+'" style="color:'+genome_text_color+';text-decoration:none">'
            link_close = '</A>'

            hit_table_html += ['<td bgcolor='+str('#ffffff')+' valign=top align=left>'+'<font size='+str(genome_fontsize)+'>'+link_open + disp_label + link_close+'</font>'+'</td>']
            for query_i,query_full_feature_id in enumerate(sorted_input_full_feature_ids):
                if query_full_feature_id not in hits_by_query_and_genome_ref \
                   or genome_ref not in hits_by_query_and_genome_ref[query_full_feature_id].keys():
                    hit_table_html += ['<td valign=top align=center bgcolor='+row_bg_color+'>']
                    hit_table_html += ['<table border=0 cellpadding='+str(hit_cellpadding)+' cellspacing='+str(hit_cellspacing)+'>']
                    hit_table_html += ['<tr><td valign=top align=center bgcolor='+row_bg_color+'> --- </td></tr>']
                    for blank_cell_i in range(max_hit_cnt-1):
                        hit_table_html += ['<tr><td bgcolor='+str(row_bg_color)+'><font size='+str(hit_fontsize)+'>&nbsp;</font></td></tr>']
                    hit_table_html += ['</table></td>']
                else:
                    hit_table_html += ['<td valign=top align=center bgcolor='+row_bg_color+'>']
                    hit_table_html += ['<table border=0 cellpadding='+str(hit_cellpadding)+' cellspacing='+str(hit_cellspacing)+'>']
                    hit_ids = []
                    for hit_id in hits_by_query_and_genome_ref[query_full_feature_id][genome_ref]:
                        hit_ids.append(hit_id)
                        #cell_bg_color = cell_bg_color[hit_id]
                        #cell_bg_color = '#cccccc'
                        if 'color_seed' in params:
                            color_seed = int(params['color_seed'])
                        else:
                            color_seed = 1
                        cluster_index = cluster_by_genome_by_fid[genome_ref][hit_id]
                        #self.log(console, "CLUSTER_INDEX for "+genome_ref+" HIT ID "+hit_id+": "+str(cluster_index))  # DEBUG
                        if cluster_size_by_cluster_id[cluster_index] > 1:
                            cell_bg_color = self._get_dark_pretty_html_color(cluster_index, color_seed)
                        else:
                            cell_bg_color = 'Gray'

                        disp_hit_id = hit_id
                        if len(hit_id) < longest_feature_id_by_query[query_full_feature_id]:
                            space_margin = longest_feature_id_by_query[query_full_feature_id] - len(hit_id)
                            if (space_margin % 2) == 1:
                                space_margin += 1
                            spaces = ''
                            for space_i in range(int(space_margin/2)):
                                spaces += '&nbsp;'
                            #spaces = '<pre>'+spaces+'</pre>'
                            disp_hit_id = '<nobr>'+spaces + disp_hit_id + spaces+'</nobr>'

                        disp_hit_id = '<pre>' + disp_hit_id + '</pre>'
                        if genome_ref+genome_ref_feature_id_delim+hit_id == query_full_feature_id:
                            cell_border_color = 'DarkGray'
                            cell_border = 2
                            bordered_cell_padding = hit_cellpadding-cell_border
                            bordered_cell_spacing = 0
                            #bordered_cell_padding = hit_cellpadding
                            #bordered_cell_spacing = cell_border
                            hit_table_html += ['<tr>']
                            hit_table_html += ['<td valign=middle align=center bgcolor='+cell_border_color+'>']
                            hit_table_html += ['<table border=0 cellpadding='+str(bordered_cell_padding)+' cellspacing='+str(bordered_cell_spacing)+' bgcolor='+cell_border_color+'>']
                            hit_table_html += ['<tr><td valign=middle align=center bgcolor='+cell_bg_color+'>'+'<font size='+str(hit_fontsize)+' color='+hit_text_color+'>'+disp_hit_id+'</font>'+'</td></tr>']
                            hit_table_html += ['</table>']
                            hit_table_html += ['</tr>']
                        else:
                            hit_table_html += ['<tr><td valign=middle align=center bgcolor='+cell_bg_color+' >'+'<font size='+str(hit_fontsize)+' color='+hit_text_color+'>'+disp_hit_id+'</font>'+'</td></tr>']
                    if len(hit_ids) < max_hit_cnt:
                        for blank_cell_i in range(max_hit_cnt-len(hit_ids)):
                            hit_table_html += ['<tr><td bgcolor='+str(row_bg_color)+'><font size='+str(hit_fontsize)+'>&nbsp;</font></td></tr>']
                    hit_table_html += ['</table></td>']
            hit_table_html += ['</tr>']

        # add bottom buffer to stretch to tree image
        for row_i in range(tree_bottom_row_buffer):
            hit_table_html += ['<tr>']
            hit_table_html += ['<td rowspan=1 colspan='+str(len(input_full_feature_ids)+1)+'>&nbsp;</td>']
            hit_table_html += ['</tr>']

        hit_table_html += ['</table>']


        #### STEP 14: make html report
        ##
        html_file = intree_name + '-homologs_chromosomal_context' + '.html'
        output_html_file_path = os.path.join(html_output_dir, html_file)
        html_report_lines = []
        html_report_lines += ['<html>']
        html_report_lines += ['<head><title>KBase Homologs Chromosomal Context: ' + intree_name + '</title></head>']
        html_report_lines += ['<body bgcolor="white">']
        html_report_lines += hit_table_html
        html_report_lines += ['</body>']
        html_report_lines += ['</html>']

        html_report_str = "\n".join(html_report_lines)
        with open(output_html_file_path, 'w', 0) as html_handle:
            html_handle.write(html_report_str)

        """
        # upload images and html
        try:
            png_upload_ret = dfuClient.file_to_shock({'file_path': output_png_file_path,
                                                #'pack': 'zip'})
                                                'make_handle': 0})
        except:
            raise ValueError('error uploading png file to shock')
        try:
            pdf_upload_ret = dfuClient.file_to_shock({'file_path': output_pdf_file_path,
                                                #'pack': 'zip'})
                                                'make_handle': 0})
        except:
            raise ValueError('error uploading pdf file to shock')
        """
        try:
            html_upload_ret = dfuClient.file_to_shock({'file_path': html_output_dir,
                                                       'make_handle': 0,
                                                       'pack': 'zip'})
        except:
            raise ValueError('error uploading html report to shock')


        #### STEP 15: Create per-genome featureSets
        ##
        if int(params.get('save_per_genome_featureSets')) == 1:
            for genome_ref in genome_ref_order:
                per_genome_featureSet_elements = {}
                try:
                    hits_to_this_genome = hits_by_genome_ref[genome_ref]
                except:
                    continue
                for hit_id in sorted(hits_by_genome_ref[genome_ref]):
                    per_genome_featureSet_elements[hit_id] = [genome_ref]

                per_genome_FS_prov = [{}]
                if 'provenance' in ctx:
                    per_genome_FS_prov = ctx['provenance']
                # add additional info to provenance here, in this case the input data object reference
                per_genome_FS_prov[0]['input_ws_objects'] = []
                per_genome_FS_prov[0]['input_ws_objects'].append(params['input_featureSet_ref'])
                per_genome_FS_prov[0]['input_ws_objects'].append(genome_ref)
                per_genome_FS_prov[0]['service'] = 'kb_phylogenomics'
                per_genome_FS_prov[0]['method'] = 'find_homologs_with_genome_context'

                per_genome_FS_obj = {
                    'description': 'Hits to Genome '+genome_ref+' by '+input_featureSet_name,
                    'elements': per_genome_featureSet_elements
                }
                per_genome_FS_name = genome_names[genome_ref]+'-Homologs_of-'+input_featureSet_name
                try:
                    per_genome_FS_obj_info = wsClient.save_objects({'workspace': params['workspace_name'],
                                                                    'objects': [
                                                                        {
                                                                            'type':'KBaseCollections.FeatureSet',
                                                                            'data':per_genome_FS_obj,
                                                                            'name':per_genome_FS_name,
                                                                            'meta':{},
                                                                            'provenance':per_genome_FS_prov,
                                                                            'hidden':0  # 1=True
                                                                        }]
                                                                })[0]
                except Exception as e:
                    raise ValueError('Unable to save per genome featureSet object to workspace: (' + per_genome_FS_name + ')' + str(e))
                self.log(console, "saved per genome hits as FS "+str(per_genome_FS_name))
                per_genome_FS_ref = str(per_genome_FS_obj_info[WSID_I])+'/'+str(per_genome_FS_obj_info[OBJID_I])+'/'+str(per_genome_FS_obj_info[VERSION_I])

                created_objects.append({'ref': per_genome_FS_ref, 'description': 'Hits to Genome '+genome_names[genome_ref]})


        #### STEP 16: Create report obj
        ##
        reportName = 'genome_homolog_context_report_' + str(uuid.uuid4())
        #report += output_newick_buf+"\n"
        reportObj = {'objects_created': [],
                     'direct_html_link_index': 0,
                     'file_links': [],
                     'html_links': [],
                     'workspace_name': params['workspace_name'],
                     'report_object_name': reportName
                     }
        #reportObj['objects_created'].append({'ref': str(params['workspace_name'])+'/'+str(params['output_name']),'description': params['output_name']+' Tree'})
        reportObj['objects_created'] = created_objects
        reportObj['html_links'] = [{'shock_id': html_upload_ret['shock_id'],
                                    'name': html_file,
                                    'label': intree_name + ' scanned by '+ input_featureSet_name + ' HTML'
                                    }
                                   ]
        """
        reportObj['file_links'] = [{'shock_id': newick_upload_ret['shock_id'],
                                    'name': intree_name + '.newick',
                                    'label': intree_name + ' NEWICK'
                                    }
                                   ]
        if 'default_node_labels' in tree_in:
            reportObj['file_links'].append({'shock_id': newick_labels_upload_ret['shock_id'],
                                            'name': intree_name + '-labels.newick',
                                            'label': intree_name + ' NEWICK (with labels)'
                                            })

        reportObj['file_links'].extend([{'shock_id': png_upload_ret['shock_id'],
                                         'name': intree_name + '.png',
                                         'label': intree_name + ' PNG'
                                         },
                                        {'shock_id': pdf_upload_ret['shock_id'],
                                         'name': intree_name + '.pdf',
                                         'label': intree_name + ' PDF'
                                         }])
        """

        reportClient = KBaseReport(self.callbackURL, token=ctx['token'], service_ver=SERVICE_VER)
        report_info = reportClient.create_extended_report(reportObj)


        # Done
        #
        self.log(console, "BUILDING RETURN OBJECT")
        output = {'report_name': report_info['name'],
                  'report_ref': report_info['ref']
                  }

        self.log(console, "find_homologs_with_genome_context() DONE")
        #END find_homologs_with_genome_context

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method find_homologs_with_genome_context return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]

    def get_configure_categories(self, ctx, params):
        """
        :param params: instance of type "get_configure_categories_Input"
           (get_configure_categories() ** ** configure the domain categorie
           names and descriptions) -> structure: parameter "params" of type
           "view_fxn_profile_Input" (view_fxn_profile() ** ** show a
           table/heatmap of general categories or custom gene families for a
           set of Genomes) -> structure: parameter "workspace_name" of type
           "workspace_name" (** Common types), parameter
           "input_genomeSet_ref" of type "data_obj_ref", parameter
           "namespace" of String, parameter "custom_target_fams" of type
           "CustomTargetFams" (parameter groups) -> structure: parameter
           "target_fams" of list of String, parameter
           "extra_target_fam_groups_COG" of list of String, parameter
           "extra_target_fam_groups_PFAM" of list of String, parameter
           "extra_target_fam_groups_TIGR" of list of String, parameter
           "extra_target_fam_groups_SEED" of list of String, parameter
           "genome_disp_name_config" of String, parameter "count_category" of
           String, parameter "heatmap" of type "bool", parameter "vertical"
           of type "bool", parameter "top_hit" of type "bool", parameter
           "e_value" of Double, parameter "log_base" of Double, parameter
           "required_COG_annot_perc" of Double, parameter
           "required_PFAM_annot_perc" of Double, parameter
           "required_TIGR_annot_perc" of Double, parameter
           "required_SEED_annot_perc" of Double, parameter
           "count_hypothetical" of type "bool", parameter "show_blanks" of
           type "bool", parameter "skip_missing_genomes" of type "bool",
           parameter "enforce_genome_version_match" of type "bool"
        :returns: instance of type "get_configure_categories_Output" ->
           structure: parameter "cats" of list of String, parameter
           "cat2name" of type "Cat2Name" (category to name) -> structure:
           parameter "namespace" of type "domain_source" (COG, PF, TIGR,
           SEED), parameter "cat" of type "category" (Categories), parameter
           "cat2group" of type "Cat2Group" (category to group) -> structure:
           parameter "namespace" of type "domain_source" (COG, PF, TIGR,
           SEED), parameter "cat" of type "category" (Categories), parameter
           "domfam2cat" of type "DomFam2Cat" (domain family to category) ->
           structure: parameter "namespace" of type "domain_source" (COG, PF,
           TIGR, SEED), parameter "domfam" of type "domainfamily" (Domains),
           parameter "cat2domfams" of type "Cat2DomFams" (category to domain
           family) -> structure: parameter "namespace" of type
           "domain_source" (COG, PF, TIGR, SEED), parameter "cat" of type
           "category" (Categories)
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN get_configure_categories

        # configure categories
        #

        params['namespace'] = 'SEED'
        params['custom_target_fams'] = dict()

        (cats, cat2name, cat2group, domfam2cat, cat2domfams, namespaces_reading, target_fams,
         extra_target_fams, extra_target_fam_groups, domfam2group, domfam2name) = self._configure_categories(params)

        output = dict()
        output['cats'] = cats
        output['cat2name'] = cat2name
        output['cat2group'] = cat2group
        output['domfam2cat'] = domfam2cat
        output['cat2domfams'] = cat2domfams

        #END get_configure_categories

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method get_configure_categories return value ' +
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
