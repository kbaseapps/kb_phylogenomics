### Version 1.4.0
__Changes__
- View Functional Profile [aka VFP / view_fxn_profile*()] Apps: skip Genomes for which a DomainAnnotation is not found
- VFP Apps: add option to not require perfect agreement of version of Genome and DomainAnnotation object
- VFP Apps: fixed bug with Custom Domains that are all SEED not to fail if missing DomainAnnotation object
- Phylogenetic Pangenome Accumulation [view_pan_phylo()] App: skip Genomes from tree not found in Pangenome
- Phylogenetic Pangenome Accumulation App: add option to not require perfect agreement of version of Genome in Species Tree and Pangenome object

### Version 1.3.2
__Changes__
- Change the category configuration into a function for use by other apps

### Version 1.3.1
__Changes__
- patched SDK_LOCAL client libs

### Version 1.3.0
__Changes__
- added find_homologs_with_genome_context() method

### Version 1.2.4
__Changes__
- added proper citations to Annotate Domains in a GenomeSet

### Version 1.2.3
__Changes__
- changed citations to PLOS format

### Version 1.2.2
__Changes__
- read 'functions' field in view functional profile apps (in KBaseGenomes.Genome-9.0 data typedef)
- removed incomplete trim_tree_to_genomeSet() method

### Version 1.2.1
__Changes__
- In view_tree, leafs prefixed with "user" are highlighted

### Version 1.2.0
__Changes__
- Create FeatureSet output objects for each node in species tree from view_pan_phylo()
- fixes to report generation call

### Version 1.1.2
__Changes__
- Got view_tree() App working (trim_tree_to_genomeSet() has to wait)

### Version 1.1.1
__Changes__
- Dockerfile updates to handle python SSL and cert issues

### Version 1.1.0
__Changes__
- Added view_tree() App

### Version 1.0.1
__Changes__
- Fixed FeatureSet ids to stop appending genome_ref.  Applies to "Pangenome Circle Plot" and "View Functional Profile for FeatureSet"
