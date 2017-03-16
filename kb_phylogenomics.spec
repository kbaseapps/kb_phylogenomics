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
	string           count_category;
	bool             heatmap;
	bool             vertical;
	bool             top_hit;
	float            e_value;
	float            log_base;
	bool             show_blanks;
    } view_fxn_profile_Input;

    typedef structure {
        string report_name;
        string report_ref;
    } view_fxn_profile_Output;

    funcdef view_fxn_profile(view_fxn_profile_Input params) 
        returns (view_fxn_profile_Output output) 
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
	string           count_category;
	bool             heatmap;
	bool             vertical;
	bool             top_hit;
	float            e_value;
	float            log_base;
	bool             show_blanks;
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
	string         input_compare_all_flag;
        data_obj_ref   input_compare_genome_refs;
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
    } view_pan_phylo_Input;

    typedef structure {
        string report_name;
        string report_ref;
    } view_pan_phylo_Output;

    funcdef view_pan_phylo(view_pan_phylo_Input params) 
        returns (view_pan_phylo_Output output) 
        authentication required;

};