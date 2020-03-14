/*
A KBase module: kb_phylogenomics

This module contains methods for running and visualizing results of phylogenomics and comparative genomics analyses
*/

module kb_phylogenomics {
    
    /*
    ** Common types
    */
    typedef string workspace_name;
    typedef string data_obj_ref;
    typedef string data_obj_name;
    typedef int    bool;


    /* build_gene_tree()
    **
    ** build a gene tree for a featureset
    */
    typedef structure {
        workspace_name  workspace_name;
        string         desc;
        data_obj_ref   input_featureSet_ref;
        data_obj_name  output_tree_name;

        int            muscle_maxiters;
        float          muscle_maxhours;

        int            gblocks_trim_level;                   /* 0=no gaps allowed, 1=half gaps allowed, 2=all gaps allowed */
        int            gblocks_min_seqs_for_conserved;       /* 0=use MSA-depth-derived default */
        int            gblocks_min_seqs_for_flank;           /* 0=use MSA-depth-derived default */
        int            gblocks_max_pos_contig_nonconserved;  /* 8=default */
        int            gblocks_min_block_len;                /* 10=default */
        int            gblocks_remove_mask_positions_flag;   /* 0=false,1=true default=0 */

        int            fasttree_fastest;  /* boolean */
        int            fasttree_pseudo;   /* boolean */
        int            fasttree_gtr;      /* boolean */
        int            fasttree_wag;      /* boolean */
        int            fasttree_noml;     /* boolean */
        int            fasttree_nome;     /* boolean */
        int            fasttree_cat;      /* actually is an int */
        int            fasttree_nocat;    /* boolean */
        int            fasttree_gamma;    /* boolean */
    } build_gene_tree_Input;

    typedef structure {
        string report_name;
        string report_ref;
    } build_gene_tree_Output;

    funcdef build_gene_tree(build_gene_tree_Input params) 
        returns (build_gene_tree_Output output) 
        authentication required;


    /* view_tree()
    **
    ** show a KBase Tree and make newick and images downloadable
    */
    typedef structure {
        workspace_name  workspace_name;
	data_obj_ref    input_tree_ref;
	string          desc;
        string          genome_disp_name_config;
        bool            show_skeleton_genome_sci_name;

	mapping<data_obj_ref,mapping<string,string>> reference_genome_disp;
	mapping<data_obj_ref,mapping<string,string>> skeleton_genome_disp;
	mapping<data_obj_ref,mapping<string,string>> user_genome_disp;
	mapping<data_obj_ref,mapping<string,string>> user2_genome_disp;
	string          color_for_reference_genomes;
	string          color_for_skeleton_genomes;
	string          color_for_user_genomes;
	string          color_for_user2_genomes;
	string          tree_shape;  /* circle, wedge, rect */
    } view_tree_Input;

    typedef structure {
        string report_name;
        string report_ref;
    } view_tree_Output;

    funcdef view_tree(view_tree_Input params) 
        returns (view_tree_Output output) 
        authentication required;


    /* trim_speciestree_to_genomeset()
    **
    ** reduce tree to match genomes found in genomeset
    */
    typedef structure {
        workspace_name  workspace_name;
        data_obj_ref    input_genomeSet_ref;
	data_obj_ref    input_tree_ref;
	data_obj_name   output_tree_name;
	string          desc;
        string          genome_disp_name_config;
        bool            show_skeleton_genome_sci_name;

	bool            enforce_genome_version_match;
	mapping<data_obj_ref,mapping<string,string>> reference_genome_disp;
	mapping<data_obj_ref,mapping<string,string>> skeleton_genome_disp;
	mapping<data_obj_ref,mapping<string,string>> user_genome_disp;
	mapping<data_obj_ref,mapping<string,string>> user2_genome_disp;
        string          color_for_reference_genomes;
	string          color_for_skeleton_genomes;
	string          color_for_user_genomes;
	string          color_for_user2_genomes;
	string          tree_shape;  /* circle, wedge, rect */
    } trim_speciestree_to_genomeset_Input;

    typedef structure {
        string report_name;
        string report_ref;
    } trim_speciestree_to_genomeset_Output;

    funcdef trim_speciestree_to_genomeset(trim_speciestree_to_genomeset_Input params) 
        returns (trim_speciestree_to_genomeset_Output output) 
        authentication required;


    /* build_microbial_speciestree()
    **
    ** run Insert Set of Genomes into Species Tree with extra features
    */
    typedef structure {
        workspace_name workspace_name;
        data_obj_ref   input_genome_refs;  /* list of refs can be Genome, GenomeSet, or SpeciesTree */
        data_obj_ref   input_genome2_refs;  /* list of refs can be Genome, GenomeSet, or SpeciesTree */
	data_obj_name  output_tree_name;
	string         desc;
        string         genome_disp_name_config;
        bool           show_skeleton_genome_sci_name;

	string         skeleton_set;  /* RefSeq-Isolates, RefSeq+MAGs, GTDB? */
	int            num_proximal_sisters;
	float          proximal_sisters_ANI_spacing;
	string         color_for_reference_genomes;
	string         color_for_skeleton_genomes;
	string         color_for_user_genomes;
	string         color_for_user2_genomes;
	string         tree_shape;  /* circle, wedge, rect */
    } build_microbial_speciestree_Input;

    typedef structure {
        string report_name;
        string report_ref;
    } build_microbial_speciestree_Output;

    funcdef build_microbial_speciestree(build_microbial_speciestree_Input params) 
        returns (build_microbial_speciestree_Output output) 
        authentication required;


    /* localize_DomainAnnotations()
    **
    ** point all DomainAnnotations at local copies of Genome Objects
    */
    typedef structure {
        workspace_name workspace_name;
	data_obj_ref input_DomainAnnotation_refs;
    } localize_DomainAnnotations_Input;

    typedef structure {
        string report_name;
        string report_ref;
    } localize_DomainAnnotations_Output;

    funcdef localize_DomainAnnotations(localize_DomainAnnotations_Input params) 
        returns (localize_DomainAnnotations_Output output) 
        authentication required;


    /* run_DomainAnnotation_Sets()
    **
    ** run the DomainAnnotation App against a GenomeSet
    */
    typedef structure {
        workspace_name workspace_name;
        data_obj_ref   input_genomeSet_ref;
	bool           override_annot;
	/*data_obj_name  output_name;*/
    } run_DomainAnnotation_Sets_Input;

    typedef structure {
        string report_name;
        string report_ref;
    } run_DomainAnnotation_Sets_Output;

    funcdef run_DomainAnnotation_Sets(run_DomainAnnotation_Sets_Input params) 
        returns (run_DomainAnnotation_Sets_Output output) 
        authentication required;


    /* parameter groups
    */
    typedef structure {
	list<string> target_fams;
	list<string> extra_target_fam_groups_COG;
	list<string> extra_target_fam_groups_PFAM;
	list<string> extra_target_fam_groups_TIGR;
	list<string> extra_target_fam_groups_SEED;
    } CustomTargetFams;


    /* view_fxn_profile()
    **
    ** show a table/heatmap of general categories or custom gene families for a set of Genomes
    */
    typedef structure {
        workspace_name workspace_name;
        data_obj_ref   input_genomeSet_ref;
	/*data_obj_ref   DomainAnnotation_Set;*/ /*reads workspace to find domain annot*/

	string           namespace;
	CustomTargetFams custom_target_fams;
        string           genome_disp_name_config;
	string           count_category;
	bool             heatmap;

	bool             vertical;
	bool             top_hit;
	float            e_value;
	float            log_base;
	float            required_COG_annot_perc;
	float            required_PFAM_annot_perc;
	float            required_TIGR_annot_perc;
	float            required_SEED_annot_perc;
	bool             count_hypothetical;
	bool             show_blanks;
	bool             skip_missing_genomes;
	bool             enforce_genome_version_match;
    } view_fxn_profile_Input;

    typedef structure {
        string report_name;
        string report_ref;
    } view_fxn_profile_Output;

    funcdef view_fxn_profile(view_fxn_profile_Input params) 
        returns (view_fxn_profile_Output output) 
        authentication required;


    /* view_fxn_profile_featureSet()
    **
    ** show a table/heatmap of general categories or custom gene families for a set of Genomes
    */
    typedef structure {
        workspace_name workspace_name;
        data_obj_ref   input_featureSet_ref;
	/*data_obj_ref   DomainAnnotation_Set;*/ /*reads workspace to find domain annot*/

	string           namespace;
	CustomTargetFams custom_target_fams;
        string           genome_disp_name_config;
	string           count_category;
	bool             heatmap;

	bool             vertical;
	bool             top_hit;
	float            e_value;
	float            log_base;
	float            required_COG_annot_perc;
	float            required_PFAM_annot_perc;
	float            required_TIGR_annot_perc;
	float            required_SEED_annot_perc;
	bool             count_hypothetical;
	bool             show_blanks;
	bool             skip_missing_genomes;
	bool             enforce_genome_version_match;
    } view_fxn_profile_featureSet_Input;

    typedef structure {
        string report_name;
        string report_ref;
    } view_fxn_profile_featureSet_Output;

    funcdef view_fxn_profile_featureSet(view_fxn_profile_featureSet_Input params) 
        returns (view_fxn_profile_featureSet_Output output) 
        authentication required;


    /* view_fxn_profile_phylo()
    **
    ** show a table/heatmap of general categories or custom gene families for a set of Genomes using the species tree
    */
    typedef structure {
        workspace_name workspace_name;
        /*data_obj_ref   input_genomeSet_ref;*/
	data_obj_ref   input_speciesTree_ref;
	/*data_obj_ref   DomainAnnotation_Set;*/

	string           namespace;
	CustomTargetFams custom_target_fams;
        string           genome_disp_name_config;
	string           count_category;
	bool             heatmap;

	bool             vertical;
	bool             top_hit;
	float            e_value;
	float            log_base;
	float            required_COG_annot_perc;
	float            required_PFAM_annot_perc;
	float            required_TIGR_annot_perc;
	float            required_SEED_annot_perc;
	bool             count_hypothetical;
	bool             show_blanks;
	bool             skip_missing_genomes;
	bool             enforce_genome_version_match;
    } view_fxn_profile_phylo_Input;

    typedef structure {
        string report_name;
        string report_ref;
    } view_fxn_profile_phylo_Output;

    funcdef view_fxn_profile_phylo(view_fxn_profile_phylo_Input params) 
        returns (view_fxn_profile_phylo_Output output) 
        authentication required;


    /* view_genome_circle_plot()
    **
    ** build a circle plot of a microbial genome
    */
    typedef structure {
        workspace_name workspace_name;
        data_obj_ref   input_genome_ref;
    } view_genome_circle_plot_Input;

    typedef structure {
        string report_name;
        string report_ref;
    } view_genome_circle_plot_Output;

    funcdef view_genome_circle_plot(view_genome_circle_plot_Input params) 
        returns (view_genome_circle_plot_Output output) 
        authentication required;


    /* view_pan_circle_plot()
    **
    ** build a circle plot of a microbial genome with its pangenome members
    */
    typedef structure {
        workspace_name workspace_name;
        data_obj_ref   input_genome_ref;
	data_obj_ref   input_pangenome_ref;
        data_obj_ref   input_compare_genome_refs;
        data_obj_ref   input_outgroup_genome_refs;
	bool           save_featuresets;
    } view_pan_circle_plot_Input;

    typedef structure {
        string report_name;
        string report_ref;
    } view_pan_circle_plot_Output;

    funcdef view_pan_circle_plot(view_pan_circle_plot_Input params) 
        returns (view_pan_circle_plot_Output output) 
        authentication required;


    /* view_pan_accumulation_plot()
    **
    ** build an accumulation plot of a pangenome
    */
    typedef structure {
        workspace_name workspace_name;
        data_obj_ref   input_genome_ref;
	data_obj_ref   input_pangenome_ref;
    } view_pan_accumulation_plot_Input;

    typedef structure {
        string report_name;
        string report_ref;
    } view_pan_accumulation_plot_Output;

    funcdef view_pan_accumulation_plot(view_pan_accumulation_plot_Input params) 
        returns (view_pan_accumulation_plot_Output output) 
        authentication required;


    /* view_pan_flower_venn()
    **
    ** build a multi-member pangenome flower venn diagram
    */
    typedef structure {
        workspace_name workspace_name;
        data_obj_ref   input_genome_ref;
	data_obj_ref   input_pangenome_ref;
    } view_pan_flower_venn_Input;

    typedef structure {
        string report_name;
        string report_ref;
    } view_pan_flower_venn_Output;

    funcdef view_pan_flower_venn(view_pan_flower_venn_Input params) 
        returns (view_pan_flower_venn_Output output) 
        authentication required;


    /* view_pan_pairwise_overlap()
    **
    ** build a multi-member pangenome pairwise overlap plot
    */
    typedef structure {
        workspace_name workspace_name;
        data_obj_ref   input_genome_ref;
	data_obj_ref   input_pangenome_ref;
    } view_pan_pairwise_overlap_Input;

    typedef structure {
        string report_name;
        string report_ref;
    } view_pan_pairwise_overlap_Output;

    funcdef view_pan_pairwise_overlap(view_pan_pairwise_overlap_Input params) 
        returns (view_pan_pairwise_overlap_Output output) 
        authentication required;


    /* view_pan_phylo()
    **
    ** show the pangenome accumulation using a tree
    */
    typedef structure {
        workspace_name workspace_name;
	data_obj_ref   input_pangenome_ref;
	data_obj_ref   input_speciesTree_ref;
	bool           save_featuresets;
	bool           skip_missing_genomes;
	bool           enforce_genome_version_match;
    } view_pan_phylo_Input;

    typedef structure {
        string report_name;
        string report_ref;
    } view_pan_phylo_Output;

    funcdef view_pan_phylo(view_pan_phylo_Input params) 
        returns (view_pan_phylo_Output output) 
        authentication required;


    /* find_homologs_with_genome_context()
    **
    ** show homolgous genes across multiple genomes within genome context against species tree
    */
    typedef structure {
        workspace_name workspace_name;
	data_obj_ref   input_featureSet_ref;
	data_obj_ref   input_speciesTree_ref;
	bool           save_per_genome_featureSets;
	int            neighbor_thresh;
	float          ident_thresh;
	float          overlap_fraction;
	float          e_value;
	float          bitscore;
	float          color_seed;
    } find_homologs_with_genome_context_Input;

    typedef structure {
        string report_name;
        string report_ref;
    } find_homologs_with_genome_context_Output;

    funcdef find_homologs_with_genome_context(find_homologs_with_genome_context_Input params) 
        returns (find_homologs_with_genome_context_Output output) 
        authentication required;

    /*
    COG, PF, TIGR, SEED
    */
        typedef string domain_source;
    /*
    Categories
    */
        typedef string category;
    /*
    Domains
    */
        typedef string domainfamily;
 
    /*  category to name
    */
    typedef structure {
        domain_source namespace;
        category   cat;
    } Cat2Name;
    
    /* category to group
    */
    typedef structure {
        domain_source namespace;
        category      cat;
    } Cat2Group;
 
    /* domain family to category
    */
    typedef structure {
        domain_source namespace;
        domainfamily      domfam;
    } DomFam2Cat;
 
    /*  category to domain family
    */
    typedef structure {
        domain_source namespace;
        category      cat;
    } Cat2DomFams;
   
    /* get_configure_categories()
    **
    ** configure the domain categorie names and descriptions
    */
    typedef structure {
        view_fxn_profile_Input params;
    } get_configure_categories_Input;

    typedef structure {
        list<string> cats;
        Cat2Name     cat2name;
        Cat2Group    cat2group;
        DomFam2Cat   domfam2cat;
        Cat2DomFams  cat2domfams;
    } get_configure_categories_Output;

    funcdef get_configure_categories(get_configure_categories_Input params) 
        returns (get_configure_categories_Output output) 
        authentication required;

};
