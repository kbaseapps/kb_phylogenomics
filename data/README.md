Doman Categories and Descriptive names downloaded from the below sources


* SEED
  ftp://ftp.theseed.org/ (FTP server is no longer supported)

  need to use API to obtain updated configuration files
  


* COG
  v2003-2014 (from CDD v3.16)
  ftp://ftp.ncbi.nih.gov/pub/COG/COG2014/data
  (NOTE: Not expected to be updated)

  - ftp://ftp.ncbi.nih.gov/pub/COG/COG2014/data/cognames2003-2014.tab
  - ftp://ftp.ncbi.nih.gov/pub/COG/COG2014/data/fun2003-2014.tab

  processing to create domain_desc files:
    1. rename cognames2003-2014.tab to COG_2014.tsv and remove comment header line

    2. rename fun2003-2014.tab to COG_2014_funcat.tsv and removed comment header line

    3. add middle column to COG_2014_funcat to add super groups 'CELLULAR PROCESSES AND SIGNALING', 'INFORMATION STORAGE AND PROCESSING', 'METABOLISM', and 'POOR CHAR'


* PFAM 
  v31.0
  ftp://ftp.ebi.ac.uk/pub/databases/Pfam/current_release
  ftp://ftp.ebi.ac.uk/pub/databases/Pfam/releases/Pfam31.0

  - ftp://ftp.ebi.ac.uk/pub/databases/Pfam/current_release/Pfam-A.clans.tsv.gz

  processing to create domain_desc files:
    1. gunzip Pfam-A.clans.tsv.gz

    2. extract clan IDs and names from Pfam-A.clans.tsv to Pfam-A.clans_names.tsv with command:
       > cat Pfam-A.clans.tsv | awk '{ print $2 "\t" $3 }' | sort | uniq > Pfam-A.clans_names.tsv


* TIGRFAMs
  v15.0
  ftp://ftp.jcvi.org/pub/data/TIGRFAMs/
  (NOTE: Not expected to be updated)

  - ftp://ftp.jcvi.org/pub/data/TIGRFAMs/TIGRFAMs_15.0_INFO.tar.gz
  - ftp://ftp.jcvi.org/pub/data/TIGRFAMs/TIGRFAMS_ROLE_LINK
  - ftp://ftp.jcvi.org/pub/data/TIGRFAMs/TIGRFAMS_GO_LINK

  processing to	create domain_desc files:
    1. gunzip and untar TIGRFAMs_15.0_INFO.tar.gz

    2. parse the TIGRFAMS_ROLE_LINK and store the mapping of TIGRFAMs ID to ROLE ID (used in 3. below)

    3. take the contents from each separate *.INFO file to create a row in the TIGRInfo.tsv file, with the following row structure:

      "ID  AC IT   ROLE	GS	 EC   EN"  (where ROLE is taken from the TIGRFAMS_ROLE_LINK)

      for example, the file TIGRFAMs_15.0_INFO/TIGR03220.INFO has contents:
----------------------------------
ID  catechol_dmpE
AC  TIGR03220
DE  2-oxopent-4-enoate hydratase
AU  Haft DH
TC  408.80 408.80
NC  247.25 247.25
AL  muscle
IT  equivalog
EN  2-oxopent-4-enoate hydratase
GS  dmpE
EC  4.2.-.-
TP  TIGRFAMs
CC  Members of this protein family are 2-oxopent-4-enoate hydratase, which is also called 2-hydroxypent-2,4-dienoate hydratase. It is closely related to another gene found in the same operon, 4-oxalocrotonate decarboxylase, with which it interacts closely.
RN  [1]
RM  PMID: 1732207
RT  Nucleotide sequence and functional analysis of the complete phenol/3,4-dimethylphenol catabolic pathway of Pseudomonas sp. strain CF600.
RA  Shingler V, Powlowski J, Marklund U
RL  J Bacteriol. 1992 Feb;174(3):711-24.
----------------------------------

      and should produce the row:
----------------------------------
catechol_dmpE	   TIGR03220	equivalog	0	dmpE	4.2.-.-	2-oxopent-4-enoate hydratase
----------------------------------

      in the collected TIGRInfo.tsv file

    3. Generate the tigrrole2go.txt file.  The process for this has been lost and the existing file should not be destroyed.
