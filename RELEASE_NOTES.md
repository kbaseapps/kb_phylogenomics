### Version 1.6.0
__Changes__
- updated Pfam version to 32.0 in VFP apps
- added Build Gene Tree App
- added Build Strain Tree App
- added Build Pangenome Species Tree App
- added Genome Object name instead of Species Name option for report display to Build Gene Tree, Build Strain Tree, Build Pangenome Species Tree, View Pangenome Circle Plot, View Phylogenetic Pangenome, but not VFP Apps because they already had the option.

### Version 1.5.1
__Changes__
- Handle query genes with zero results in Homolog Genome Context App
- Add query_2 input option to Build Microbial SpeciesTree App

### Version 1.5.0
__Changes__
- Added Build Microbial SpeciesTree App
- Fixed ContigSet/Assembly bug in Homolog Genome Context App

### Version 1.4.0
__Changes__
- View Functional Profile [aka VFP / view_fxn_profile*()] Apps: skip Genomes for which a DomainAnnotation is not found
- VFP Apps: add option to not require perfect agreement of version of Genome and DomainAnnotation object
- VFP Apps: fixed bug with Custom Domains that are all SEED not to fail if missing DomainAnnotation object
- VFP Apps: generate FeatureSets if explicit custom domains are members of query
- VFP Apps: added option to check for reasonable fraction of annotated genes with validated SEED vocabulary if query includes SEED subsystems
- VFP Apps: added options to check for reasonable fraction of ALL genes receiving annotations within each Domain Namespace
- VFP Apps: removed duplicate TIGR roles from input options
- VFP Apps: added SEED functional categories to displayed SEED role input options
- VFP Apps: added option to specify Genome Obj Name, Obj Ver, and/or Sci name in report
- VFP Apps: check for Domain Annotation in current workspace first
- VFP GenomeSet and FeatureSet: sort by genome disp name and require unique
- VFP Apps: updated App Docs to reflect changes
- Domain Annotation for Genomes App: allow Species Tree as input
- View Tree App: color user genome or reference genome, whichever there are fewer of
- Trim SpeciesTree to GenomeSet App: added

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
