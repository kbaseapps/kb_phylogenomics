
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


    /* view_tree()
    **
    ** show a KBase Tree and make newick and images downloadable
    */
    typedef structure {
        workspace_name workspace_name;
        /*data_obj_ref   input_genomeSet_ref;*/
	data_obj_ref   input_tree_ref;
	string         desc;
    } view_tree_Input;

    typedef structure {
        string report_name;
        string report_ref;
    } view_tree_Output;

    funcdef view_tree(view_tree_Input params) 
        returns (view_tree_Output output) 
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
