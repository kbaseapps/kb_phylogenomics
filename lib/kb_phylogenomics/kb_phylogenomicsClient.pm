package kb_phylogenomics::kb_phylogenomicsClient;

use JSON::RPC::Client;
use POSIX;
use strict;
use Data::Dumper;
use URI;
use Bio::KBase::Exceptions;
my $get_time = sub { time, 0 };
eval {
    require Time::HiRes;
    $get_time = sub { Time::HiRes::gettimeofday() };
};

use Bio::KBase::AuthToken;

# Client version should match Impl version
# This is a Semantic Version number,
# http://semver.org
our $VERSION = "0.1.0";

=head1 NAME

kb_phylogenomics::kb_phylogenomicsClient

=head1 DESCRIPTION


A KBase module: kb_phylogenomics

This module contains methods for running and visualizing results of phylogenomics and comparative genomics analyses


=cut

sub new
{
    my($class, $url, @args) = @_;
    

    my $self = {
	client => kb_phylogenomics::kb_phylogenomicsClient::RpcClient->new,
	url => $url,
	headers => [],
    };

    chomp($self->{hostname} = `hostname`);
    $self->{hostname} ||= 'unknown-host';

    #
    # Set up for propagating KBRPC_TAG and KBRPC_METADATA environment variables through
    # to invoked services. If these values are not set, we create a new tag
    # and a metadata field with basic information about the invoking script.
    #
    if ($ENV{KBRPC_TAG})
    {
	$self->{kbrpc_tag} = $ENV{KBRPC_TAG};
    }
    else
    {
	my ($t, $us) = &$get_time();
	$us = sprintf("%06d", $us);
	my $ts = strftime("%Y-%m-%dT%H:%M:%S.${us}Z", gmtime $t);
	$self->{kbrpc_tag} = "C:$0:$self->{hostname}:$$:$ts";
    }
    push(@{$self->{headers}}, 'Kbrpc-Tag', $self->{kbrpc_tag});

    if ($ENV{KBRPC_METADATA})
    {
	$self->{kbrpc_metadata} = $ENV{KBRPC_METADATA};
	push(@{$self->{headers}}, 'Kbrpc-Metadata', $self->{kbrpc_metadata});
    }

    if ($ENV{KBRPC_ERROR_DEST})
    {
	$self->{kbrpc_error_dest} = $ENV{KBRPC_ERROR_DEST};
	push(@{$self->{headers}}, 'Kbrpc-Errordest', $self->{kbrpc_error_dest});
    }

    #
    # This module requires authentication.
    #
    # We create an auth token, passing through the arguments that we were (hopefully) given.

    {
	my %arg_hash2 = @args;
	if (exists $arg_hash2{"token"}) {
	    $self->{token} = $arg_hash2{"token"};
	} elsif (exists $arg_hash2{"user_id"}) {
	    my $token = Bio::KBase::AuthToken->new(@args);
	    if (!$token->error_message) {
	        $self->{token} = $token->token;
	    }
	}
	
	if (exists $self->{token})
	{
	    $self->{client}->{token} = $self->{token};
	}
    }

    my $ua = $self->{client}->ua;	 
    my $timeout = $ENV{CDMI_TIMEOUT} || (30 * 60);	 
    $ua->timeout($timeout);
    bless $self, $class;
    #    $self->_validate_version();
    return $self;
}




=head2 build_gene_tree

  $output = $obj->build_gene_tree($params)

=over 4

=item Parameter and return types

=begin html

<pre>
$params is a kb_phylogenomics.build_gene_tree_Input
$output is a kb_phylogenomics.build_gene_tree_Output
build_gene_tree_Input is a reference to a hash where the following keys are defined:
	workspace_name has a value which is a kb_phylogenomics.workspace_name
	desc has a value which is a string
	input_featureSet_ref has a value which is a kb_phylogenomics.data_obj_ref
	output_tree_name has a value which is a kb_phylogenomics.data_obj_name
	genome_disp_name_config has a value which is a string
	skip_trimming has a value which is a kb_phylogenomics.bool
	muscle_maxiters has a value which is an int
	muscle_maxhours has a value which is a float
	gblocks_trim_level has a value which is an int
	gblocks_min_seqs_for_conserved has a value which is an int
	gblocks_min_seqs_for_flank has a value which is an int
	gblocks_max_pos_contig_nonconserved has a value which is an int
	gblocks_min_block_len has a value which is an int
	gblocks_remove_mask_positions_flag has a value which is an int
	fasttree_fastest has a value which is an int
	fasttree_pseudo has a value which is an int
	fasttree_gtr has a value which is an int
	fasttree_wag has a value which is an int
	fasttree_noml has a value which is an int
	fasttree_nome has a value which is an int
	fasttree_cat has a value which is an int
	fasttree_nocat has a value which is an int
	fasttree_gamma has a value which is an int
workspace_name is a string
data_obj_ref is a string
data_obj_name is a string
bool is an int
build_gene_tree_Output is a reference to a hash where the following keys are defined:
	report_name has a value which is a string
	report_ref has a value which is a string

</pre>

=end html

=begin text

$params is a kb_phylogenomics.build_gene_tree_Input
$output is a kb_phylogenomics.build_gene_tree_Output
build_gene_tree_Input is a reference to a hash where the following keys are defined:
	workspace_name has a value which is a kb_phylogenomics.workspace_name
	desc has a value which is a string
	input_featureSet_ref has a value which is a kb_phylogenomics.data_obj_ref
	output_tree_name has a value which is a kb_phylogenomics.data_obj_name
	genome_disp_name_config has a value which is a string
	skip_trimming has a value which is a kb_phylogenomics.bool
	muscle_maxiters has a value which is an int
	muscle_maxhours has a value which is a float
	gblocks_trim_level has a value which is an int
	gblocks_min_seqs_for_conserved has a value which is an int
	gblocks_min_seqs_for_flank has a value which is an int
	gblocks_max_pos_contig_nonconserved has a value which is an int
	gblocks_min_block_len has a value which is an int
	gblocks_remove_mask_positions_flag has a value which is an int
	fasttree_fastest has a value which is an int
	fasttree_pseudo has a value which is an int
	fasttree_gtr has a value which is an int
	fasttree_wag has a value which is an int
	fasttree_noml has a value which is an int
	fasttree_nome has a value which is an int
	fasttree_cat has a value which is an int
	fasttree_nocat has a value which is an int
	fasttree_gamma has a value which is an int
workspace_name is a string
data_obj_ref is a string
data_obj_name is a string
bool is an int
build_gene_tree_Output is a reference to a hash where the following keys are defined:
	report_name has a value which is a string
	report_ref has a value which is a string


=end text

=item Description



=back

=cut

 sub build_gene_tree
{
    my($self, @args) = @_;

# Authentication: required

    if ((my $n = @args) != 1)
    {
	Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
							       "Invalid argument count for function build_gene_tree (received $n, expecting 1)");
    }
    {
	my($params) = @args;

	my @_bad_arguments;
        (ref($params) eq 'HASH') or push(@_bad_arguments, "Invalid type for argument 1 \"params\" (value was \"$params\")");
        if (@_bad_arguments) {
	    my $msg = "Invalid arguments passed to build_gene_tree:\n" . join("", map { "\t$_\n" } @_bad_arguments);
	    Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
								   method_name => 'build_gene_tree');
	}
    }

    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
	    method => "kb_phylogenomics.build_gene_tree",
	    params => \@args,
    });
    if ($result) {
	if ($result->is_error) {
	    Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
					       code => $result->content->{error}->{code},
					       method_name => 'build_gene_tree',
					       data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
					      );
	} else {
	    return wantarray ? @{$result->result} : $result->result->[0];
	}
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method build_gene_tree",
					    status_line => $self->{client}->status_line,
					    method_name => 'build_gene_tree',
				       );
    }
}
 


=head2 build_strain_tree

  $output = $obj->build_strain_tree($params)

=over 4

=item Parameter and return types

=begin html

<pre>
$params is a kb_phylogenomics.build_strain_tree_Input
$output is a kb_phylogenomics.build_strain_tree_Output
build_strain_tree_Input is a reference to a hash where the following keys are defined:
	workspace_name has a value which is a kb_phylogenomics.workspace_name
	desc has a value which is a string
	input_genome_refs has a value which is a kb_phylogenomics.data_obj_ref
	output_tree_name has a value which is a kb_phylogenomics.data_obj_name
	genome_disp_name_config has a value which is a string
	skip_trimming has a value which is a kb_phylogenomics.bool
	muscle_maxiters has a value which is an int
	muscle_maxhours has a value which is a float
	gblocks_trim_level has a value which is an int
	gblocks_min_seqs_for_conserved has a value which is an int
	gblocks_min_seqs_for_flank has a value which is an int
	gblocks_max_pos_contig_nonconserved has a value which is an int
	gblocks_min_block_len has a value which is an int
	gblocks_remove_mask_positions_flag has a value which is an int
	fasttree_fastest has a value which is an int
	fasttree_pseudo has a value which is an int
	fasttree_gtr has a value which is an int
	fasttree_wag has a value which is an int
	fasttree_noml has a value which is an int
	fasttree_nome has a value which is an int
	fasttree_cat has a value which is an int
	fasttree_nocat has a value which is an int
	fasttree_gamma has a value which is an int
workspace_name is a string
data_obj_ref is a string
data_obj_name is a string
bool is an int
build_strain_tree_Output is a reference to a hash where the following keys are defined:
	report_name has a value which is a string
	report_ref has a value which is a string

</pre>

=end html

=begin text

$params is a kb_phylogenomics.build_strain_tree_Input
$output is a kb_phylogenomics.build_strain_tree_Output
build_strain_tree_Input is a reference to a hash where the following keys are defined:
	workspace_name has a value which is a kb_phylogenomics.workspace_name
	desc has a value which is a string
	input_genome_refs has a value which is a kb_phylogenomics.data_obj_ref
	output_tree_name has a value which is a kb_phylogenomics.data_obj_name
	genome_disp_name_config has a value which is a string
	skip_trimming has a value which is a kb_phylogenomics.bool
	muscle_maxiters has a value which is an int
	muscle_maxhours has a value which is a float
	gblocks_trim_level has a value which is an int
	gblocks_min_seqs_for_conserved has a value which is an int
	gblocks_min_seqs_for_flank has a value which is an int
	gblocks_max_pos_contig_nonconserved has a value which is an int
	gblocks_min_block_len has a value which is an int
	gblocks_remove_mask_positions_flag has a value which is an int
	fasttree_fastest has a value which is an int
	fasttree_pseudo has a value which is an int
	fasttree_gtr has a value which is an int
	fasttree_wag has a value which is an int
	fasttree_noml has a value which is an int
	fasttree_nome has a value which is an int
	fasttree_cat has a value which is an int
	fasttree_nocat has a value which is an int
	fasttree_gamma has a value which is an int
workspace_name is a string
data_obj_ref is a string
data_obj_name is a string
bool is an int
build_strain_tree_Output is a reference to a hash where the following keys are defined:
	report_name has a value which is a string
	report_ref has a value which is a string


=end text

=item Description



=back

=cut

 sub build_strain_tree
{
    my($self, @args) = @_;

# Authentication: required

    if ((my $n = @args) != 1)
    {
	Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
							       "Invalid argument count for function build_strain_tree (received $n, expecting 1)");
    }
    {
	my($params) = @args;

	my @_bad_arguments;
        (ref($params) eq 'HASH') or push(@_bad_arguments, "Invalid type for argument 1 \"params\" (value was \"$params\")");
        if (@_bad_arguments) {
	    my $msg = "Invalid arguments passed to build_strain_tree:\n" . join("", map { "\t$_\n" } @_bad_arguments);
	    Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
								   method_name => 'build_strain_tree');
	}
    }

    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
	    method => "kb_phylogenomics.build_strain_tree",
	    params => \@args,
    });
    if ($result) {
	if ($result->is_error) {
	    Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
					       code => $result->content->{error}->{code},
					       method_name => 'build_strain_tree',
					       data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
					      );
	} else {
	    return wantarray ? @{$result->result} : $result->result->[0];
	}
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method build_strain_tree",
					    status_line => $self->{client}->status_line,
					    method_name => 'build_strain_tree',
				       );
    }
}
 


=head2 build_pangenome_species_tree

  $output = $obj->build_pangenome_species_tree($params)

=over 4

=item Parameter and return types

=begin html

<pre>
$params is a kb_phylogenomics.build_pangenome_species_tree_Input
$output is a kb_phylogenomics.build_pangenome_species_tree_Output
build_pangenome_species_tree_Input is a reference to a hash where the following keys are defined:
	workspace_name has a value which is a kb_phylogenomics.workspace_name
	desc has a value which is a string
	input_pangenome_ref has a value which is a kb_phylogenomics.data_obj_ref
	output_tree_name has a value which is a kb_phylogenomics.data_obj_name
	genome_disp_name_config has a value which is a string
	skip_trimming has a value which is a kb_phylogenomics.bool
	perc_marker_presence_min has a value which is a float
	muscle_maxiters has a value which is an int
	muscle_maxhours has a value which is a float
	gblocks_trim_level has a value which is an int
	gblocks_min_seqs_for_conserved has a value which is an int
	gblocks_min_seqs_for_flank has a value which is an int
	gblocks_max_pos_contig_nonconserved has a value which is an int
	gblocks_min_block_len has a value which is an int
	gblocks_remove_mask_positions_flag has a value which is an int
	fasttree_fastest has a value which is an int
	fasttree_pseudo has a value which is an int
	fasttree_gtr has a value which is an int
	fasttree_wag has a value which is an int
	fasttree_noml has a value which is an int
	fasttree_nome has a value which is an int
	fasttree_cat has a value which is an int
	fasttree_nocat has a value which is an int
	fasttree_gamma has a value which is an int
workspace_name is a string
data_obj_ref is a string
data_obj_name is a string
bool is an int
build_pangenome_species_tree_Output is a reference to a hash where the following keys are defined:
	report_name has a value which is a string
	report_ref has a value which is a string

</pre>

=end html

=begin text

$params is a kb_phylogenomics.build_pangenome_species_tree_Input
$output is a kb_phylogenomics.build_pangenome_species_tree_Output
build_pangenome_species_tree_Input is a reference to a hash where the following keys are defined:
	workspace_name has a value which is a kb_phylogenomics.workspace_name
	desc has a value which is a string
	input_pangenome_ref has a value which is a kb_phylogenomics.data_obj_ref
	output_tree_name has a value which is a kb_phylogenomics.data_obj_name
	genome_disp_name_config has a value which is a string
	skip_trimming has a value which is a kb_phylogenomics.bool
	perc_marker_presence_min has a value which is a float
	muscle_maxiters has a value which is an int
	muscle_maxhours has a value which is a float
	gblocks_trim_level has a value which is an int
	gblocks_min_seqs_for_conserved has a value which is an int
	gblocks_min_seqs_for_flank has a value which is an int
	gblocks_max_pos_contig_nonconserved has a value which is an int
	gblocks_min_block_len has a value which is an int
	gblocks_remove_mask_positions_flag has a value which is an int
	fasttree_fastest has a value which is an int
	fasttree_pseudo has a value which is an int
	fasttree_gtr has a value which is an int
	fasttree_wag has a value which is an int
	fasttree_noml has a value which is an int
	fasttree_nome has a value which is an int
	fasttree_cat has a value which is an int
	fasttree_nocat has a value which is an int
	fasttree_gamma has a value which is an int
workspace_name is a string
data_obj_ref is a string
data_obj_name is a string
bool is an int
build_pangenome_species_tree_Output is a reference to a hash where the following keys are defined:
	report_name has a value which is a string
	report_ref has a value which is a string


=end text

=item Description



=back

=cut

 sub build_pangenome_species_tree
{
    my($self, @args) = @_;

# Authentication: required

    if ((my $n = @args) != 1)
    {
	Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
							       "Invalid argument count for function build_pangenome_species_tree (received $n, expecting 1)");
    }
    {
	my($params) = @args;

	my @_bad_arguments;
        (ref($params) eq 'HASH') or push(@_bad_arguments, "Invalid type for argument 1 \"params\" (value was \"$params\")");
        if (@_bad_arguments) {
	    my $msg = "Invalid arguments passed to build_pangenome_species_tree:\n" . join("", map { "\t$_\n" } @_bad_arguments);
	    Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
								   method_name => 'build_pangenome_species_tree');
	}
    }

    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
	    method => "kb_phylogenomics.build_pangenome_species_tree",
	    params => \@args,
    });
    if ($result) {
	if ($result->is_error) {
	    Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
					       code => $result->content->{error}->{code},
					       method_name => 'build_pangenome_species_tree',
					       data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
					      );
	} else {
	    return wantarray ? @{$result->result} : $result->result->[0];
	}
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method build_pangenome_species_tree",
					    status_line => $self->{client}->status_line,
					    method_name => 'build_pangenome_species_tree',
				       );
    }
}
 


=head2 view_tree

  $output = $obj->view_tree($params)

=over 4

=item Parameter and return types

=begin html

<pre>
$params is a kb_phylogenomics.view_tree_Input
$output is a kb_phylogenomics.view_tree_Output
view_tree_Input is a reference to a hash where the following keys are defined:
	workspace_name has a value which is a kb_phylogenomics.workspace_name
	input_tree_ref has a value which is a kb_phylogenomics.data_obj_ref
	desc has a value which is a string
	show_skeleton_genome_sci_name has a value which is a kb_phylogenomics.bool
	reference_genome_disp has a value which is a reference to a hash where the key is a kb_phylogenomics.data_obj_ref and the value is a reference to a hash where the key is a string and the value is a string
	skeleton_genome_disp has a value which is a reference to a hash where the key is a kb_phylogenomics.data_obj_ref and the value is a reference to a hash where the key is a string and the value is a string
	user_genome_disp has a value which is a reference to a hash where the key is a kb_phylogenomics.data_obj_ref and the value is a reference to a hash where the key is a string and the value is a string
	user2_genome_disp has a value which is a reference to a hash where the key is a kb_phylogenomics.data_obj_ref and the value is a reference to a hash where the key is a string and the value is a string
	color_for_reference_genomes has a value which is a string
	color_for_skeleton_genomes has a value which is a string
	color_for_user_genomes has a value which is a string
	color_for_user2_genomes has a value which is a string
	tree_shape has a value which is a string
workspace_name is a string
data_obj_ref is a string
bool is an int
view_tree_Output is a reference to a hash where the following keys are defined:
	report_name has a value which is a string
	report_ref has a value which is a string

</pre>

=end html

=begin text

$params is a kb_phylogenomics.view_tree_Input
$output is a kb_phylogenomics.view_tree_Output
view_tree_Input is a reference to a hash where the following keys are defined:
	workspace_name has a value which is a kb_phylogenomics.workspace_name
	input_tree_ref has a value which is a kb_phylogenomics.data_obj_ref
	desc has a value which is a string
	show_skeleton_genome_sci_name has a value which is a kb_phylogenomics.bool
	reference_genome_disp has a value which is a reference to a hash where the key is a kb_phylogenomics.data_obj_ref and the value is a reference to a hash where the key is a string and the value is a string
	skeleton_genome_disp has a value which is a reference to a hash where the key is a kb_phylogenomics.data_obj_ref and the value is a reference to a hash where the key is a string and the value is a string
	user_genome_disp has a value which is a reference to a hash where the key is a kb_phylogenomics.data_obj_ref and the value is a reference to a hash where the key is a string and the value is a string
	user2_genome_disp has a value which is a reference to a hash where the key is a kb_phylogenomics.data_obj_ref and the value is a reference to a hash where the key is a string and the value is a string
	color_for_reference_genomes has a value which is a string
	color_for_skeleton_genomes has a value which is a string
	color_for_user_genomes has a value which is a string
	color_for_user2_genomes has a value which is a string
	tree_shape has a value which is a string
workspace_name is a string
data_obj_ref is a string
bool is an int
view_tree_Output is a reference to a hash where the following keys are defined:
	report_name has a value which is a string
	report_ref has a value which is a string


=end text

=item Description



=back

=cut

 sub view_tree
{
    my($self, @args) = @_;

# Authentication: required

    if ((my $n = @args) != 1)
    {
	Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
							       "Invalid argument count for function view_tree (received $n, expecting 1)");
    }
    {
	my($params) = @args;

	my @_bad_arguments;
        (ref($params) eq 'HASH') or push(@_bad_arguments, "Invalid type for argument 1 \"params\" (value was \"$params\")");
        if (@_bad_arguments) {
	    my $msg = "Invalid arguments passed to view_tree:\n" . join("", map { "\t$_\n" } @_bad_arguments);
	    Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
								   method_name => 'view_tree');
	}
    }

    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
	    method => "kb_phylogenomics.view_tree",
	    params => \@args,
    });
    if ($result) {
	if ($result->is_error) {
	    Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
					       code => $result->content->{error}->{code},
					       method_name => 'view_tree',
					       data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
					      );
	} else {
	    return wantarray ? @{$result->result} : $result->result->[0];
	}
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method view_tree",
					    status_line => $self->{client}->status_line,
					    method_name => 'view_tree',
				       );
    }
}
 


=head2 trim_speciestree_to_genomeset

  $output = $obj->trim_speciestree_to_genomeset($params)

=over 4

=item Parameter and return types

=begin html

<pre>
$params is a kb_phylogenomics.trim_speciestree_to_genomeset_Input
$output is a kb_phylogenomics.trim_speciestree_to_genomeset_Output
trim_speciestree_to_genomeset_Input is a reference to a hash where the following keys are defined:
	workspace_name has a value which is a kb_phylogenomics.workspace_name
	input_genomeSet_ref has a value which is a kb_phylogenomics.data_obj_ref
	input_tree_ref has a value which is a kb_phylogenomics.data_obj_ref
	output_tree_name has a value which is a kb_phylogenomics.data_obj_name
	desc has a value which is a string
	show_skeleton_genome_sci_name has a value which is a kb_phylogenomics.bool
	enforce_genome_version_match has a value which is a kb_phylogenomics.bool
	reference_genome_disp has a value which is a reference to a hash where the key is a kb_phylogenomics.data_obj_ref and the value is a reference to a hash where the key is a string and the value is a string
	skeleton_genome_disp has a value which is a reference to a hash where the key is a kb_phylogenomics.data_obj_ref and the value is a reference to a hash where the key is a string and the value is a string
	user_genome_disp has a value which is a reference to a hash where the key is a kb_phylogenomics.data_obj_ref and the value is a reference to a hash where the key is a string and the value is a string
	user2_genome_disp has a value which is a reference to a hash where the key is a kb_phylogenomics.data_obj_ref and the value is a reference to a hash where the key is a string and the value is a string
	color_for_reference_genomes has a value which is a string
	color_for_skeleton_genomes has a value which is a string
	color_for_user_genomes has a value which is a string
	color_for_user2_genomes has a value which is a string
	tree_shape has a value which is a string
workspace_name is a string
data_obj_ref is a string
data_obj_name is a string
bool is an int
trim_speciestree_to_genomeset_Output is a reference to a hash where the following keys are defined:
	report_name has a value which is a string
	report_ref has a value which is a string

</pre>

=end html

=begin text

$params is a kb_phylogenomics.trim_speciestree_to_genomeset_Input
$output is a kb_phylogenomics.trim_speciestree_to_genomeset_Output
trim_speciestree_to_genomeset_Input is a reference to a hash where the following keys are defined:
	workspace_name has a value which is a kb_phylogenomics.workspace_name
	input_genomeSet_ref has a value which is a kb_phylogenomics.data_obj_ref
	input_tree_ref has a value which is a kb_phylogenomics.data_obj_ref
	output_tree_name has a value which is a kb_phylogenomics.data_obj_name
	desc has a value which is a string
	show_skeleton_genome_sci_name has a value which is a kb_phylogenomics.bool
	enforce_genome_version_match has a value which is a kb_phylogenomics.bool
	reference_genome_disp has a value which is a reference to a hash where the key is a kb_phylogenomics.data_obj_ref and the value is a reference to a hash where the key is a string and the value is a string
	skeleton_genome_disp has a value which is a reference to a hash where the key is a kb_phylogenomics.data_obj_ref and the value is a reference to a hash where the key is a string and the value is a string
	user_genome_disp has a value which is a reference to a hash where the key is a kb_phylogenomics.data_obj_ref and the value is a reference to a hash where the key is a string and the value is a string
	user2_genome_disp has a value which is a reference to a hash where the key is a kb_phylogenomics.data_obj_ref and the value is a reference to a hash where the key is a string and the value is a string
	color_for_reference_genomes has a value which is a string
	color_for_skeleton_genomes has a value which is a string
	color_for_user_genomes has a value which is a string
	color_for_user2_genomes has a value which is a string
	tree_shape has a value which is a string
workspace_name is a string
data_obj_ref is a string
data_obj_name is a string
bool is an int
trim_speciestree_to_genomeset_Output is a reference to a hash where the following keys are defined:
	report_name has a value which is a string
	report_ref has a value which is a string


=end text

=item Description



=back

=cut

 sub trim_speciestree_to_genomeset
{
    my($self, @args) = @_;

# Authentication: required

    if ((my $n = @args) != 1)
    {
	Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
							       "Invalid argument count for function trim_speciestree_to_genomeset (received $n, expecting 1)");
    }
    {
	my($params) = @args;

	my @_bad_arguments;
        (ref($params) eq 'HASH') or push(@_bad_arguments, "Invalid type for argument 1 \"params\" (value was \"$params\")");
        if (@_bad_arguments) {
	    my $msg = "Invalid arguments passed to trim_speciestree_to_genomeset:\n" . join("", map { "\t$_\n" } @_bad_arguments);
	    Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
								   method_name => 'trim_speciestree_to_genomeset');
	}
    }

    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
	    method => "kb_phylogenomics.trim_speciestree_to_genomeset",
	    params => \@args,
    });
    if ($result) {
	if ($result->is_error) {
	    Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
					       code => $result->content->{error}->{code},
					       method_name => 'trim_speciestree_to_genomeset',
					       data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
					      );
	} else {
	    return wantarray ? @{$result->result} : $result->result->[0];
	}
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method trim_speciestree_to_genomeset",
					    status_line => $self->{client}->status_line,
					    method_name => 'trim_speciestree_to_genomeset',
				       );
    }
}
 


=head2 trim_genetree_to_genomeset

  $output = $obj->trim_genetree_to_genomeset($params)

=over 4

=item Parameter and return types

=begin html

<pre>
$params is a kb_phylogenomics.trim_genetree_to_genomeset_Input
$output is a kb_phylogenomics.trim_genetree_to_genomeset_Output
trim_genetree_to_genomeset_Input is a reference to a hash where the following keys are defined:
	workspace_name has a value which is a kb_phylogenomics.workspace_name
	input_genomeSet_ref has a value which is a kb_phylogenomics.data_obj_ref
	input_tree_ref has a value which is a kb_phylogenomics.data_obj_ref
	output_tree_name has a value which is a kb_phylogenomics.data_obj_name
	desc has a value which is a string
	enforce_genome_version_match has a value which is a kb_phylogenomics.bool
	keep_ama_genes has a value which is a kb_phylogenomics.bool
workspace_name is a string
data_obj_ref is a string
data_obj_name is a string
bool is an int
trim_genetree_to_genomeset_Output is a reference to a hash where the following keys are defined:
	report_name has a value which is a string
	report_ref has a value which is a string

</pre>

=end html

=begin text

$params is a kb_phylogenomics.trim_genetree_to_genomeset_Input
$output is a kb_phylogenomics.trim_genetree_to_genomeset_Output
trim_genetree_to_genomeset_Input is a reference to a hash where the following keys are defined:
	workspace_name has a value which is a kb_phylogenomics.workspace_name
	input_genomeSet_ref has a value which is a kb_phylogenomics.data_obj_ref
	input_tree_ref has a value which is a kb_phylogenomics.data_obj_ref
	output_tree_name has a value which is a kb_phylogenomics.data_obj_name
	desc has a value which is a string
	enforce_genome_version_match has a value which is a kb_phylogenomics.bool
	keep_ama_genes has a value which is a kb_phylogenomics.bool
workspace_name is a string
data_obj_ref is a string
data_obj_name is a string
bool is an int
trim_genetree_to_genomeset_Output is a reference to a hash where the following keys are defined:
	report_name has a value which is a string
	report_ref has a value which is a string


=end text

=item Description



=back

=cut

 sub trim_genetree_to_genomeset
{
    my($self, @args) = @_;

# Authentication: required

    if ((my $n = @args) != 1)
    {
	Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
							       "Invalid argument count for function trim_genetree_to_genomeset (received $n, expecting 1)");
    }
    {
	my($params) = @args;

	my @_bad_arguments;
        (ref($params) eq 'HASH') or push(@_bad_arguments, "Invalid type for argument 1 \"params\" (value was \"$params\")");
        if (@_bad_arguments) {
	    my $msg = "Invalid arguments passed to trim_genetree_to_genomeset:\n" . join("", map { "\t$_\n" } @_bad_arguments);
	    Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
								   method_name => 'trim_genetree_to_genomeset');
	}
    }

    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
	    method => "kb_phylogenomics.trim_genetree_to_genomeset",
	    params => \@args,
    });
    if ($result) {
	if ($result->is_error) {
	    Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
					       code => $result->content->{error}->{code},
					       method_name => 'trim_genetree_to_genomeset',
					       data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
					      );
	} else {
	    return wantarray ? @{$result->result} : $result->result->[0];
	}
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method trim_genetree_to_genomeset",
					    status_line => $self->{client}->status_line,
					    method_name => 'trim_genetree_to_genomeset',
				       );
    }
}
 


=head2 build_microbial_speciestree

  $output = $obj->build_microbial_speciestree($params)

=over 4

=item Parameter and return types

=begin html

<pre>
$params is a kb_phylogenomics.build_microbial_speciestree_Input
$output is a kb_phylogenomics.build_microbial_speciestree_Output
build_microbial_speciestree_Input is a reference to a hash where the following keys are defined:
	workspace_name has a value which is a kb_phylogenomics.workspace_name
	input_genome_refs has a value which is a kb_phylogenomics.data_obj_ref
	input_genome2_refs has a value which is a kb_phylogenomics.data_obj_ref
	output_tree_name has a value which is a kb_phylogenomics.data_obj_name
	desc has a value which is a string
	show_skeleton_genome_sci_name has a value which is a kb_phylogenomics.bool
	skeleton_set has a value which is a string
	color_for_skeleton_genomes has a value which is a string
	color_for_user_genomes has a value which is a string
	color_for_user2_genomes has a value which is a string
workspace_name is a string
data_obj_ref is a string
data_obj_name is a string
bool is an int
build_microbial_speciestree_Output is a reference to a hash where the following keys are defined:
	report_name has a value which is a string
	report_ref has a value which is a string

</pre>

=end html

=begin text

$params is a kb_phylogenomics.build_microbial_speciestree_Input
$output is a kb_phylogenomics.build_microbial_speciestree_Output
build_microbial_speciestree_Input is a reference to a hash where the following keys are defined:
	workspace_name has a value which is a kb_phylogenomics.workspace_name
	input_genome_refs has a value which is a kb_phylogenomics.data_obj_ref
	input_genome2_refs has a value which is a kb_phylogenomics.data_obj_ref
	output_tree_name has a value which is a kb_phylogenomics.data_obj_name
	desc has a value which is a string
	show_skeleton_genome_sci_name has a value which is a kb_phylogenomics.bool
	skeleton_set has a value which is a string
	color_for_skeleton_genomes has a value which is a string
	color_for_user_genomes has a value which is a string
	color_for_user2_genomes has a value which is a string
workspace_name is a string
data_obj_ref is a string
data_obj_name is a string
bool is an int
build_microbial_speciestree_Output is a reference to a hash where the following keys are defined:
	report_name has a value which is a string
	report_ref has a value which is a string


=end text

=item Description



=back

=cut

 sub build_microbial_speciestree
{
    my($self, @args) = @_;

# Authentication: required

    if ((my $n = @args) != 1)
    {
	Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
							       "Invalid argument count for function build_microbial_speciestree (received $n, expecting 1)");
    }
    {
	my($params) = @args;

	my @_bad_arguments;
        (ref($params) eq 'HASH') or push(@_bad_arguments, "Invalid type for argument 1 \"params\" (value was \"$params\")");
        if (@_bad_arguments) {
	    my $msg = "Invalid arguments passed to build_microbial_speciestree:\n" . join("", map { "\t$_\n" } @_bad_arguments);
	    Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
								   method_name => 'build_microbial_speciestree');
	}
    }

    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
	    method => "kb_phylogenomics.build_microbial_speciestree",
	    params => \@args,
    });
    if ($result) {
	if ($result->is_error) {
	    Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
					       code => $result->content->{error}->{code},
					       method_name => 'build_microbial_speciestree',
					       data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
					      );
	} else {
	    return wantarray ? @{$result->result} : $result->result->[0];
	}
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method build_microbial_speciestree",
					    status_line => $self->{client}->status_line,
					    method_name => 'build_microbial_speciestree',
				       );
    }
}
 


=head2 localize_DomainAnnotations

  $output = $obj->localize_DomainAnnotations($params)

=over 4

=item Parameter and return types

=begin html

<pre>
$params is a kb_phylogenomics.localize_DomainAnnotations_Input
$output is a kb_phylogenomics.localize_DomainAnnotations_Output
localize_DomainAnnotations_Input is a reference to a hash where the following keys are defined:
	workspace_name has a value which is a kb_phylogenomics.workspace_name
	input_DomainAnnotation_refs has a value which is a kb_phylogenomics.data_obj_ref
workspace_name is a string
data_obj_ref is a string
localize_DomainAnnotations_Output is a reference to a hash where the following keys are defined:
	report_name has a value which is a string
	report_ref has a value which is a string

</pre>

=end html

=begin text

$params is a kb_phylogenomics.localize_DomainAnnotations_Input
$output is a kb_phylogenomics.localize_DomainAnnotations_Output
localize_DomainAnnotations_Input is a reference to a hash where the following keys are defined:
	workspace_name has a value which is a kb_phylogenomics.workspace_name
	input_DomainAnnotation_refs has a value which is a kb_phylogenomics.data_obj_ref
workspace_name is a string
data_obj_ref is a string
localize_DomainAnnotations_Output is a reference to a hash where the following keys are defined:
	report_name has a value which is a string
	report_ref has a value which is a string


=end text

=item Description



=back

=cut

 sub localize_DomainAnnotations
{
    my($self, @args) = @_;

# Authentication: required

    if ((my $n = @args) != 1)
    {
	Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
							       "Invalid argument count for function localize_DomainAnnotations (received $n, expecting 1)");
    }
    {
	my($params) = @args;

	my @_bad_arguments;
        (ref($params) eq 'HASH') or push(@_bad_arguments, "Invalid type for argument 1 \"params\" (value was \"$params\")");
        if (@_bad_arguments) {
	    my $msg = "Invalid arguments passed to localize_DomainAnnotations:\n" . join("", map { "\t$_\n" } @_bad_arguments);
	    Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
								   method_name => 'localize_DomainAnnotations');
	}
    }

    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
	    method => "kb_phylogenomics.localize_DomainAnnotations",
	    params => \@args,
    });
    if ($result) {
	if ($result->is_error) {
	    Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
					       code => $result->content->{error}->{code},
					       method_name => 'localize_DomainAnnotations',
					       data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
					      );
	} else {
	    return wantarray ? @{$result->result} : $result->result->[0];
	}
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method localize_DomainAnnotations",
					    status_line => $self->{client}->status_line,
					    method_name => 'localize_DomainAnnotations',
				       );
    }
}
 


=head2 run_DomainAnnotation_Sets

  $output = $obj->run_DomainAnnotation_Sets($params)

=over 4

=item Parameter and return types

=begin html

<pre>
$params is a kb_phylogenomics.run_DomainAnnotation_Sets_Input
$output is a kb_phylogenomics.run_DomainAnnotation_Sets_Output
run_DomainAnnotation_Sets_Input is a reference to a hash where the following keys are defined:
	workspace_name has a value which is a kb_phylogenomics.workspace_name
	input_genomeSet_ref has a value which is a kb_phylogenomics.data_obj_ref
	override_annot has a value which is a kb_phylogenomics.bool
workspace_name is a string
data_obj_ref is a string
bool is an int
run_DomainAnnotation_Sets_Output is a reference to a hash where the following keys are defined:
	report_name has a value which is a string
	report_ref has a value which is a string

</pre>

=end html

=begin text

$params is a kb_phylogenomics.run_DomainAnnotation_Sets_Input
$output is a kb_phylogenomics.run_DomainAnnotation_Sets_Output
run_DomainAnnotation_Sets_Input is a reference to a hash where the following keys are defined:
	workspace_name has a value which is a kb_phylogenomics.workspace_name
	input_genomeSet_ref has a value which is a kb_phylogenomics.data_obj_ref
	override_annot has a value which is a kb_phylogenomics.bool
workspace_name is a string
data_obj_ref is a string
bool is an int
run_DomainAnnotation_Sets_Output is a reference to a hash where the following keys are defined:
	report_name has a value which is a string
	report_ref has a value which is a string


=end text

=item Description



=back

=cut

 sub run_DomainAnnotation_Sets
{
    my($self, @args) = @_;

# Authentication: required

    if ((my $n = @args) != 1)
    {
	Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
							       "Invalid argument count for function run_DomainAnnotation_Sets (received $n, expecting 1)");
    }
    {
	my($params) = @args;

	my @_bad_arguments;
        (ref($params) eq 'HASH') or push(@_bad_arguments, "Invalid type for argument 1 \"params\" (value was \"$params\")");
        if (@_bad_arguments) {
	    my $msg = "Invalid arguments passed to run_DomainAnnotation_Sets:\n" . join("", map { "\t$_\n" } @_bad_arguments);
	    Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
								   method_name => 'run_DomainAnnotation_Sets');
	}
    }

    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
	    method => "kb_phylogenomics.run_DomainAnnotation_Sets",
	    params => \@args,
    });
    if ($result) {
	if ($result->is_error) {
	    Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
					       code => $result->content->{error}->{code},
					       method_name => 'run_DomainAnnotation_Sets',
					       data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
					      );
	} else {
	    return wantarray ? @{$result->result} : $result->result->[0];
	}
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method run_DomainAnnotation_Sets",
					    status_line => $self->{client}->status_line,
					    method_name => 'run_DomainAnnotation_Sets',
				       );
    }
}
 


=head2 view_fxn_profile

  $output = $obj->view_fxn_profile($params)

=over 4

=item Parameter and return types

=begin html

<pre>
$params is a kb_phylogenomics.view_fxn_profile_Input
$output is a kb_phylogenomics.view_fxn_profile_Output
view_fxn_profile_Input is a reference to a hash where the following keys are defined:
	workspace_name has a value which is a kb_phylogenomics.workspace_name
	input_genomeSet_ref has a value which is a kb_phylogenomics.data_obj_ref
	namespace has a value which is a string
	custom_target_fams has a value which is a kb_phylogenomics.CustomTargetFams
	genome_disp_name_config has a value which is a string
	count_category has a value which is a string
	heatmap has a value which is a kb_phylogenomics.bool
	vertical has a value which is a kb_phylogenomics.bool
	top_hit has a value which is a kb_phylogenomics.bool
	e_value has a value which is a float
	log_base has a value which is a float
	required_COG_annot_perc has a value which is a float
	required_PFAM_annot_perc has a value which is a float
	required_TIGR_annot_perc has a value which is a float
	required_SEED_annot_perc has a value which is a float
	count_hypothetical has a value which is a kb_phylogenomics.bool
	show_blanks has a value which is a kb_phylogenomics.bool
	skip_missing_genomes has a value which is a kb_phylogenomics.bool
	enforce_genome_version_match has a value which is a kb_phylogenomics.bool
workspace_name is a string
data_obj_ref is a string
CustomTargetFams is a reference to a hash where the following keys are defined:
	target_fams has a value which is a reference to a list where each element is a string
	extra_target_fam_groups_COG has a value which is a reference to a list where each element is a string
	extra_target_fam_groups_PFAM has a value which is a reference to a list where each element is a string
	extra_target_fam_groups_TIGR has a value which is a reference to a list where each element is a string
	extra_target_fam_groups_SEED has a value which is a reference to a list where each element is a string
bool is an int
view_fxn_profile_Output is a reference to a hash where the following keys are defined:
	report_name has a value which is a string
	report_ref has a value which is a string

</pre>

=end html

=begin text

$params is a kb_phylogenomics.view_fxn_profile_Input
$output is a kb_phylogenomics.view_fxn_profile_Output
view_fxn_profile_Input is a reference to a hash where the following keys are defined:
	workspace_name has a value which is a kb_phylogenomics.workspace_name
	input_genomeSet_ref has a value which is a kb_phylogenomics.data_obj_ref
	namespace has a value which is a string
	custom_target_fams has a value which is a kb_phylogenomics.CustomTargetFams
	genome_disp_name_config has a value which is a string
	count_category has a value which is a string
	heatmap has a value which is a kb_phylogenomics.bool
	vertical has a value which is a kb_phylogenomics.bool
	top_hit has a value which is a kb_phylogenomics.bool
	e_value has a value which is a float
	log_base has a value which is a float
	required_COG_annot_perc has a value which is a float
	required_PFAM_annot_perc has a value which is a float
	required_TIGR_annot_perc has a value which is a float
	required_SEED_annot_perc has a value which is a float
	count_hypothetical has a value which is a kb_phylogenomics.bool
	show_blanks has a value which is a kb_phylogenomics.bool
	skip_missing_genomes has a value which is a kb_phylogenomics.bool
	enforce_genome_version_match has a value which is a kb_phylogenomics.bool
workspace_name is a string
data_obj_ref is a string
CustomTargetFams is a reference to a hash where the following keys are defined:
	target_fams has a value which is a reference to a list where each element is a string
	extra_target_fam_groups_COG has a value which is a reference to a list where each element is a string
	extra_target_fam_groups_PFAM has a value which is a reference to a list where each element is a string
	extra_target_fam_groups_TIGR has a value which is a reference to a list where each element is a string
	extra_target_fam_groups_SEED has a value which is a reference to a list where each element is a string
bool is an int
view_fxn_profile_Output is a reference to a hash where the following keys are defined:
	report_name has a value which is a string
	report_ref has a value which is a string


=end text

=item Description



=back

=cut

 sub view_fxn_profile
{
    my($self, @args) = @_;

# Authentication: required

    if ((my $n = @args) != 1)
    {
	Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
							       "Invalid argument count for function view_fxn_profile (received $n, expecting 1)");
    }
    {
	my($params) = @args;

	my @_bad_arguments;
        (ref($params) eq 'HASH') or push(@_bad_arguments, "Invalid type for argument 1 \"params\" (value was \"$params\")");
        if (@_bad_arguments) {
	    my $msg = "Invalid arguments passed to view_fxn_profile:\n" . join("", map { "\t$_\n" } @_bad_arguments);
	    Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
								   method_name => 'view_fxn_profile');
	}
    }

    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
	    method => "kb_phylogenomics.view_fxn_profile",
	    params => \@args,
    });
    if ($result) {
	if ($result->is_error) {
	    Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
					       code => $result->content->{error}->{code},
					       method_name => 'view_fxn_profile',
					       data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
					      );
	} else {
	    return wantarray ? @{$result->result} : $result->result->[0];
	}
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method view_fxn_profile",
					    status_line => $self->{client}->status_line,
					    method_name => 'view_fxn_profile',
				       );
    }
}
 


=head2 view_fxn_profile_featureSet

  $output = $obj->view_fxn_profile_featureSet($params)

=over 4

=item Parameter and return types

=begin html

<pre>
$params is a kb_phylogenomics.view_fxn_profile_featureSet_Input
$output is a kb_phylogenomics.view_fxn_profile_featureSet_Output
view_fxn_profile_featureSet_Input is a reference to a hash where the following keys are defined:
	workspace_name has a value which is a kb_phylogenomics.workspace_name
	input_featureSet_ref has a value which is a kb_phylogenomics.data_obj_ref
	namespace has a value which is a string
	custom_target_fams has a value which is a kb_phylogenomics.CustomTargetFams
	genome_disp_name_config has a value which is a string
	count_category has a value which is a string
	heatmap has a value which is a kb_phylogenomics.bool
	vertical has a value which is a kb_phylogenomics.bool
	top_hit has a value which is a kb_phylogenomics.bool
	e_value has a value which is a float
	log_base has a value which is a float
	required_COG_annot_perc has a value which is a float
	required_PFAM_annot_perc has a value which is a float
	required_TIGR_annot_perc has a value which is a float
	required_SEED_annot_perc has a value which is a float
	count_hypothetical has a value which is a kb_phylogenomics.bool
	show_blanks has a value which is a kb_phylogenomics.bool
	skip_missing_genomes has a value which is a kb_phylogenomics.bool
	enforce_genome_version_match has a value which is a kb_phylogenomics.bool
workspace_name is a string
data_obj_ref is a string
CustomTargetFams is a reference to a hash where the following keys are defined:
	target_fams has a value which is a reference to a list where each element is a string
	extra_target_fam_groups_COG has a value which is a reference to a list where each element is a string
	extra_target_fam_groups_PFAM has a value which is a reference to a list where each element is a string
	extra_target_fam_groups_TIGR has a value which is a reference to a list where each element is a string
	extra_target_fam_groups_SEED has a value which is a reference to a list where each element is a string
bool is an int
view_fxn_profile_featureSet_Output is a reference to a hash where the following keys are defined:
	report_name has a value which is a string
	report_ref has a value which is a string

</pre>

=end html

=begin text

$params is a kb_phylogenomics.view_fxn_profile_featureSet_Input
$output is a kb_phylogenomics.view_fxn_profile_featureSet_Output
view_fxn_profile_featureSet_Input is a reference to a hash where the following keys are defined:
	workspace_name has a value which is a kb_phylogenomics.workspace_name
	input_featureSet_ref has a value which is a kb_phylogenomics.data_obj_ref
	namespace has a value which is a string
	custom_target_fams has a value which is a kb_phylogenomics.CustomTargetFams
	genome_disp_name_config has a value which is a string
	count_category has a value which is a string
	heatmap has a value which is a kb_phylogenomics.bool
	vertical has a value which is a kb_phylogenomics.bool
	top_hit has a value which is a kb_phylogenomics.bool
	e_value has a value which is a float
	log_base has a value which is a float
	required_COG_annot_perc has a value which is a float
	required_PFAM_annot_perc has a value which is a float
	required_TIGR_annot_perc has a value which is a float
	required_SEED_annot_perc has a value which is a float
	count_hypothetical has a value which is a kb_phylogenomics.bool
	show_blanks has a value which is a kb_phylogenomics.bool
	skip_missing_genomes has a value which is a kb_phylogenomics.bool
	enforce_genome_version_match has a value which is a kb_phylogenomics.bool
workspace_name is a string
data_obj_ref is a string
CustomTargetFams is a reference to a hash where the following keys are defined:
	target_fams has a value which is a reference to a list where each element is a string
	extra_target_fam_groups_COG has a value which is a reference to a list where each element is a string
	extra_target_fam_groups_PFAM has a value which is a reference to a list where each element is a string
	extra_target_fam_groups_TIGR has a value which is a reference to a list where each element is a string
	extra_target_fam_groups_SEED has a value which is a reference to a list where each element is a string
bool is an int
view_fxn_profile_featureSet_Output is a reference to a hash where the following keys are defined:
	report_name has a value which is a string
	report_ref has a value which is a string


=end text

=item Description



=back

=cut

 sub view_fxn_profile_featureSet
{
    my($self, @args) = @_;

# Authentication: required

    if ((my $n = @args) != 1)
    {
	Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
							       "Invalid argument count for function view_fxn_profile_featureSet (received $n, expecting 1)");
    }
    {
	my($params) = @args;

	my @_bad_arguments;
        (ref($params) eq 'HASH') or push(@_bad_arguments, "Invalid type for argument 1 \"params\" (value was \"$params\")");
        if (@_bad_arguments) {
	    my $msg = "Invalid arguments passed to view_fxn_profile_featureSet:\n" . join("", map { "\t$_\n" } @_bad_arguments);
	    Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
								   method_name => 'view_fxn_profile_featureSet');
	}
    }

    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
	    method => "kb_phylogenomics.view_fxn_profile_featureSet",
	    params => \@args,
    });
    if ($result) {
	if ($result->is_error) {
	    Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
					       code => $result->content->{error}->{code},
					       method_name => 'view_fxn_profile_featureSet',
					       data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
					      );
	} else {
	    return wantarray ? @{$result->result} : $result->result->[0];
	}
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method view_fxn_profile_featureSet",
					    status_line => $self->{client}->status_line,
					    method_name => 'view_fxn_profile_featureSet',
				       );
    }
}
 


=head2 view_fxn_profile_phylo

  $output = $obj->view_fxn_profile_phylo($params)

=over 4

=item Parameter and return types

=begin html

<pre>
$params is a kb_phylogenomics.view_fxn_profile_phylo_Input
$output is a kb_phylogenomics.view_fxn_profile_phylo_Output
view_fxn_profile_phylo_Input is a reference to a hash where the following keys are defined:
	workspace_name has a value which is a kb_phylogenomics.workspace_name
	input_speciesTree_ref has a value which is a kb_phylogenomics.data_obj_ref
	namespace has a value which is a string
	custom_target_fams has a value which is a kb_phylogenomics.CustomTargetFams
	genome_disp_name_config has a value which is a string
	count_category has a value which is a string
	heatmap has a value which is a kb_phylogenomics.bool
	vertical has a value which is a kb_phylogenomics.bool
	top_hit has a value which is a kb_phylogenomics.bool
	e_value has a value which is a float
	log_base has a value which is a float
	required_COG_annot_perc has a value which is a float
	required_PFAM_annot_perc has a value which is a float
	required_TIGR_annot_perc has a value which is a float
	required_SEED_annot_perc has a value which is a float
	count_hypothetical has a value which is a kb_phylogenomics.bool
	show_blanks has a value which is a kb_phylogenomics.bool
	skip_missing_genomes has a value which is a kb_phylogenomics.bool
	enforce_genome_version_match has a value which is a kb_phylogenomics.bool
workspace_name is a string
data_obj_ref is a string
CustomTargetFams is a reference to a hash where the following keys are defined:
	target_fams has a value which is a reference to a list where each element is a string
	extra_target_fam_groups_COG has a value which is a reference to a list where each element is a string
	extra_target_fam_groups_PFAM has a value which is a reference to a list where each element is a string
	extra_target_fam_groups_TIGR has a value which is a reference to a list where each element is a string
	extra_target_fam_groups_SEED has a value which is a reference to a list where each element is a string
bool is an int
view_fxn_profile_phylo_Output is a reference to a hash where the following keys are defined:
	report_name has a value which is a string
	report_ref has a value which is a string

</pre>

=end html

=begin text

$params is a kb_phylogenomics.view_fxn_profile_phylo_Input
$output is a kb_phylogenomics.view_fxn_profile_phylo_Output
view_fxn_profile_phylo_Input is a reference to a hash where the following keys are defined:
	workspace_name has a value which is a kb_phylogenomics.workspace_name
	input_speciesTree_ref has a value which is a kb_phylogenomics.data_obj_ref
	namespace has a value which is a string
	custom_target_fams has a value which is a kb_phylogenomics.CustomTargetFams
	genome_disp_name_config has a value which is a string
	count_category has a value which is a string
	heatmap has a value which is a kb_phylogenomics.bool
	vertical has a value which is a kb_phylogenomics.bool
	top_hit has a value which is a kb_phylogenomics.bool
	e_value has a value which is a float
	log_base has a value which is a float
	required_COG_annot_perc has a value which is a float
	required_PFAM_annot_perc has a value which is a float
	required_TIGR_annot_perc has a value which is a float
	required_SEED_annot_perc has a value which is a float
	count_hypothetical has a value which is a kb_phylogenomics.bool
	show_blanks has a value which is a kb_phylogenomics.bool
	skip_missing_genomes has a value which is a kb_phylogenomics.bool
	enforce_genome_version_match has a value which is a kb_phylogenomics.bool
workspace_name is a string
data_obj_ref is a string
CustomTargetFams is a reference to a hash where the following keys are defined:
	target_fams has a value which is a reference to a list where each element is a string
	extra_target_fam_groups_COG has a value which is a reference to a list where each element is a string
	extra_target_fam_groups_PFAM has a value which is a reference to a list where each element is a string
	extra_target_fam_groups_TIGR has a value which is a reference to a list where each element is a string
	extra_target_fam_groups_SEED has a value which is a reference to a list where each element is a string
bool is an int
view_fxn_profile_phylo_Output is a reference to a hash where the following keys are defined:
	report_name has a value which is a string
	report_ref has a value which is a string


=end text

=item Description



=back

=cut

 sub view_fxn_profile_phylo
{
    my($self, @args) = @_;

# Authentication: required

    if ((my $n = @args) != 1)
    {
	Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
							       "Invalid argument count for function view_fxn_profile_phylo (received $n, expecting 1)");
    }
    {
	my($params) = @args;

	my @_bad_arguments;
        (ref($params) eq 'HASH') or push(@_bad_arguments, "Invalid type for argument 1 \"params\" (value was \"$params\")");
        if (@_bad_arguments) {
	    my $msg = "Invalid arguments passed to view_fxn_profile_phylo:\n" . join("", map { "\t$_\n" } @_bad_arguments);
	    Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
								   method_name => 'view_fxn_profile_phylo');
	}
    }

    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
	    method => "kb_phylogenomics.view_fxn_profile_phylo",
	    params => \@args,
    });
    if ($result) {
	if ($result->is_error) {
	    Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
					       code => $result->content->{error}->{code},
					       method_name => 'view_fxn_profile_phylo',
					       data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
					      );
	} else {
	    return wantarray ? @{$result->result} : $result->result->[0];
	}
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method view_fxn_profile_phylo",
					    status_line => $self->{client}->status_line,
					    method_name => 'view_fxn_profile_phylo',
				       );
    }
}
 


=head2 view_genome_circle_plot

  $output = $obj->view_genome_circle_plot($params)

=over 4

=item Parameter and return types

=begin html

<pre>
$params is a kb_phylogenomics.view_genome_circle_plot_Input
$output is a kb_phylogenomics.view_genome_circle_plot_Output
view_genome_circle_plot_Input is a reference to a hash where the following keys are defined:
	workspace_name has a value which is a kb_phylogenomics.workspace_name
	input_genome_ref has a value which is a kb_phylogenomics.data_obj_ref
workspace_name is a string
data_obj_ref is a string
view_genome_circle_plot_Output is a reference to a hash where the following keys are defined:
	report_name has a value which is a string
	report_ref has a value which is a string

</pre>

=end html

=begin text

$params is a kb_phylogenomics.view_genome_circle_plot_Input
$output is a kb_phylogenomics.view_genome_circle_plot_Output
view_genome_circle_plot_Input is a reference to a hash where the following keys are defined:
	workspace_name has a value which is a kb_phylogenomics.workspace_name
	input_genome_ref has a value which is a kb_phylogenomics.data_obj_ref
workspace_name is a string
data_obj_ref is a string
view_genome_circle_plot_Output is a reference to a hash where the following keys are defined:
	report_name has a value which is a string
	report_ref has a value which is a string


=end text

=item Description



=back

=cut

 sub view_genome_circle_plot
{
    my($self, @args) = @_;

# Authentication: required

    if ((my $n = @args) != 1)
    {
	Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
							       "Invalid argument count for function view_genome_circle_plot (received $n, expecting 1)");
    }
    {
	my($params) = @args;

	my @_bad_arguments;
        (ref($params) eq 'HASH') or push(@_bad_arguments, "Invalid type for argument 1 \"params\" (value was \"$params\")");
        if (@_bad_arguments) {
	    my $msg = "Invalid arguments passed to view_genome_circle_plot:\n" . join("", map { "\t$_\n" } @_bad_arguments);
	    Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
								   method_name => 'view_genome_circle_plot');
	}
    }

    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
	    method => "kb_phylogenomics.view_genome_circle_plot",
	    params => \@args,
    });
    if ($result) {
	if ($result->is_error) {
	    Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
					       code => $result->content->{error}->{code},
					       method_name => 'view_genome_circle_plot',
					       data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
					      );
	} else {
	    return wantarray ? @{$result->result} : $result->result->[0];
	}
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method view_genome_circle_plot",
					    status_line => $self->{client}->status_line,
					    method_name => 'view_genome_circle_plot',
				       );
    }
}
 


=head2 view_pan_circle_plot

  $output = $obj->view_pan_circle_plot($params)

=over 4

=item Parameter and return types

=begin html

<pre>
$params is a kb_phylogenomics.view_pan_circle_plot_Input
$output is a kb_phylogenomics.view_pan_circle_plot_Output
view_pan_circle_plot_Input is a reference to a hash where the following keys are defined:
	workspace_name has a value which is a kb_phylogenomics.workspace_name
	input_genome_ref has a value which is a kb_phylogenomics.data_obj_ref
	input_pangenome_ref has a value which is a kb_phylogenomics.data_obj_ref
	input_compare_genome_refs has a value which is a kb_phylogenomics.data_obj_ref
	input_outgroup_genome_refs has a value which is a kb_phylogenomics.data_obj_ref
	save_featuresets has a value which is a kb_phylogenomics.bool
	genome_disp_name_config has a value which is a string
workspace_name is a string
data_obj_ref is a string
bool is an int
view_pan_circle_plot_Output is a reference to a hash where the following keys are defined:
	report_name has a value which is a string
	report_ref has a value which is a string

</pre>

=end html

=begin text

$params is a kb_phylogenomics.view_pan_circle_plot_Input
$output is a kb_phylogenomics.view_pan_circle_plot_Output
view_pan_circle_plot_Input is a reference to a hash where the following keys are defined:
	workspace_name has a value which is a kb_phylogenomics.workspace_name
	input_genome_ref has a value which is a kb_phylogenomics.data_obj_ref
	input_pangenome_ref has a value which is a kb_phylogenomics.data_obj_ref
	input_compare_genome_refs has a value which is a kb_phylogenomics.data_obj_ref
	input_outgroup_genome_refs has a value which is a kb_phylogenomics.data_obj_ref
	save_featuresets has a value which is a kb_phylogenomics.bool
	genome_disp_name_config has a value which is a string
workspace_name is a string
data_obj_ref is a string
bool is an int
view_pan_circle_plot_Output is a reference to a hash where the following keys are defined:
	report_name has a value which is a string
	report_ref has a value which is a string


=end text

=item Description



=back

=cut

 sub view_pan_circle_plot
{
    my($self, @args) = @_;

# Authentication: required

    if ((my $n = @args) != 1)
    {
	Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
							       "Invalid argument count for function view_pan_circle_plot (received $n, expecting 1)");
    }
    {
	my($params) = @args;

	my @_bad_arguments;
        (ref($params) eq 'HASH') or push(@_bad_arguments, "Invalid type for argument 1 \"params\" (value was \"$params\")");
        if (@_bad_arguments) {
	    my $msg = "Invalid arguments passed to view_pan_circle_plot:\n" . join("", map { "\t$_\n" } @_bad_arguments);
	    Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
								   method_name => 'view_pan_circle_plot');
	}
    }

    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
	    method => "kb_phylogenomics.view_pan_circle_plot",
	    params => \@args,
    });
    if ($result) {
	if ($result->is_error) {
	    Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
					       code => $result->content->{error}->{code},
					       method_name => 'view_pan_circle_plot',
					       data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
					      );
	} else {
	    return wantarray ? @{$result->result} : $result->result->[0];
	}
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method view_pan_circle_plot",
					    status_line => $self->{client}->status_line,
					    method_name => 'view_pan_circle_plot',
				       );
    }
}
 


=head2 view_pan_accumulation_plot

  $output = $obj->view_pan_accumulation_plot($params)

=over 4

=item Parameter and return types

=begin html

<pre>
$params is a kb_phylogenomics.view_pan_accumulation_plot_Input
$output is a kb_phylogenomics.view_pan_accumulation_plot_Output
view_pan_accumulation_plot_Input is a reference to a hash where the following keys are defined:
	workspace_name has a value which is a kb_phylogenomics.workspace_name
	input_genome_ref has a value which is a kb_phylogenomics.data_obj_ref
	input_pangenome_ref has a value which is a kb_phylogenomics.data_obj_ref
workspace_name is a string
data_obj_ref is a string
view_pan_accumulation_plot_Output is a reference to a hash where the following keys are defined:
	report_name has a value which is a string
	report_ref has a value which is a string

</pre>

=end html

=begin text

$params is a kb_phylogenomics.view_pan_accumulation_plot_Input
$output is a kb_phylogenomics.view_pan_accumulation_plot_Output
view_pan_accumulation_plot_Input is a reference to a hash where the following keys are defined:
	workspace_name has a value which is a kb_phylogenomics.workspace_name
	input_genome_ref has a value which is a kb_phylogenomics.data_obj_ref
	input_pangenome_ref has a value which is a kb_phylogenomics.data_obj_ref
workspace_name is a string
data_obj_ref is a string
view_pan_accumulation_plot_Output is a reference to a hash where the following keys are defined:
	report_name has a value which is a string
	report_ref has a value which is a string


=end text

=item Description



=back

=cut

 sub view_pan_accumulation_plot
{
    my($self, @args) = @_;

# Authentication: required

    if ((my $n = @args) != 1)
    {
	Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
							       "Invalid argument count for function view_pan_accumulation_plot (received $n, expecting 1)");
    }
    {
	my($params) = @args;

	my @_bad_arguments;
        (ref($params) eq 'HASH') or push(@_bad_arguments, "Invalid type for argument 1 \"params\" (value was \"$params\")");
        if (@_bad_arguments) {
	    my $msg = "Invalid arguments passed to view_pan_accumulation_plot:\n" . join("", map { "\t$_\n" } @_bad_arguments);
	    Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
								   method_name => 'view_pan_accumulation_plot');
	}
    }

    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
	    method => "kb_phylogenomics.view_pan_accumulation_plot",
	    params => \@args,
    });
    if ($result) {
	if ($result->is_error) {
	    Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
					       code => $result->content->{error}->{code},
					       method_name => 'view_pan_accumulation_plot',
					       data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
					      );
	} else {
	    return wantarray ? @{$result->result} : $result->result->[0];
	}
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method view_pan_accumulation_plot",
					    status_line => $self->{client}->status_line,
					    method_name => 'view_pan_accumulation_plot',
				       );
    }
}
 


=head2 view_pan_flower_venn

  $output = $obj->view_pan_flower_venn($params)

=over 4

=item Parameter and return types

=begin html

<pre>
$params is a kb_phylogenomics.view_pan_flower_venn_Input
$output is a kb_phylogenomics.view_pan_flower_venn_Output
view_pan_flower_venn_Input is a reference to a hash where the following keys are defined:
	workspace_name has a value which is a kb_phylogenomics.workspace_name
	input_genome_ref has a value which is a kb_phylogenomics.data_obj_ref
	input_pangenome_ref has a value which is a kb_phylogenomics.data_obj_ref
workspace_name is a string
data_obj_ref is a string
view_pan_flower_venn_Output is a reference to a hash where the following keys are defined:
	report_name has a value which is a string
	report_ref has a value which is a string

</pre>

=end html

=begin text

$params is a kb_phylogenomics.view_pan_flower_venn_Input
$output is a kb_phylogenomics.view_pan_flower_venn_Output
view_pan_flower_venn_Input is a reference to a hash where the following keys are defined:
	workspace_name has a value which is a kb_phylogenomics.workspace_name
	input_genome_ref has a value which is a kb_phylogenomics.data_obj_ref
	input_pangenome_ref has a value which is a kb_phylogenomics.data_obj_ref
workspace_name is a string
data_obj_ref is a string
view_pan_flower_venn_Output is a reference to a hash where the following keys are defined:
	report_name has a value which is a string
	report_ref has a value which is a string


=end text

=item Description



=back

=cut

 sub view_pan_flower_venn
{
    my($self, @args) = @_;

# Authentication: required

    if ((my $n = @args) != 1)
    {
	Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
							       "Invalid argument count for function view_pan_flower_venn (received $n, expecting 1)");
    }
    {
	my($params) = @args;

	my @_bad_arguments;
        (ref($params) eq 'HASH') or push(@_bad_arguments, "Invalid type for argument 1 \"params\" (value was \"$params\")");
        if (@_bad_arguments) {
	    my $msg = "Invalid arguments passed to view_pan_flower_venn:\n" . join("", map { "\t$_\n" } @_bad_arguments);
	    Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
								   method_name => 'view_pan_flower_venn');
	}
    }

    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
	    method => "kb_phylogenomics.view_pan_flower_venn",
	    params => \@args,
    });
    if ($result) {
	if ($result->is_error) {
	    Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
					       code => $result->content->{error}->{code},
					       method_name => 'view_pan_flower_venn',
					       data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
					      );
	} else {
	    return wantarray ? @{$result->result} : $result->result->[0];
	}
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method view_pan_flower_venn",
					    status_line => $self->{client}->status_line,
					    method_name => 'view_pan_flower_venn',
				       );
    }
}
 


=head2 view_pan_pairwise_overlap

  $output = $obj->view_pan_pairwise_overlap($params)

=over 4

=item Parameter and return types

=begin html

<pre>
$params is a kb_phylogenomics.view_pan_pairwise_overlap_Input
$output is a kb_phylogenomics.view_pan_pairwise_overlap_Output
view_pan_pairwise_overlap_Input is a reference to a hash where the following keys are defined:
	workspace_name has a value which is a kb_phylogenomics.workspace_name
	input_genome_ref has a value which is a kb_phylogenomics.data_obj_ref
	input_pangenome_ref has a value which is a kb_phylogenomics.data_obj_ref
workspace_name is a string
data_obj_ref is a string
view_pan_pairwise_overlap_Output is a reference to a hash where the following keys are defined:
	report_name has a value which is a string
	report_ref has a value which is a string

</pre>

=end html

=begin text

$params is a kb_phylogenomics.view_pan_pairwise_overlap_Input
$output is a kb_phylogenomics.view_pan_pairwise_overlap_Output
view_pan_pairwise_overlap_Input is a reference to a hash where the following keys are defined:
	workspace_name has a value which is a kb_phylogenomics.workspace_name
	input_genome_ref has a value which is a kb_phylogenomics.data_obj_ref
	input_pangenome_ref has a value which is a kb_phylogenomics.data_obj_ref
workspace_name is a string
data_obj_ref is a string
view_pan_pairwise_overlap_Output is a reference to a hash where the following keys are defined:
	report_name has a value which is a string
	report_ref has a value which is a string


=end text

=item Description



=back

=cut

 sub view_pan_pairwise_overlap
{
    my($self, @args) = @_;

# Authentication: required

    if ((my $n = @args) != 1)
    {
	Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
							       "Invalid argument count for function view_pan_pairwise_overlap (received $n, expecting 1)");
    }
    {
	my($params) = @args;

	my @_bad_arguments;
        (ref($params) eq 'HASH') or push(@_bad_arguments, "Invalid type for argument 1 \"params\" (value was \"$params\")");
        if (@_bad_arguments) {
	    my $msg = "Invalid arguments passed to view_pan_pairwise_overlap:\n" . join("", map { "\t$_\n" } @_bad_arguments);
	    Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
								   method_name => 'view_pan_pairwise_overlap');
	}
    }

    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
	    method => "kb_phylogenomics.view_pan_pairwise_overlap",
	    params => \@args,
    });
    if ($result) {
	if ($result->is_error) {
	    Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
					       code => $result->content->{error}->{code},
					       method_name => 'view_pan_pairwise_overlap',
					       data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
					      );
	} else {
	    return wantarray ? @{$result->result} : $result->result->[0];
	}
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method view_pan_pairwise_overlap",
					    status_line => $self->{client}->status_line,
					    method_name => 'view_pan_pairwise_overlap',
				       );
    }
}
 


=head2 view_pan_phylo

  $output = $obj->view_pan_phylo($params)

=over 4

=item Parameter and return types

=begin html

<pre>
$params is a kb_phylogenomics.view_pan_phylo_Input
$output is a kb_phylogenomics.view_pan_phylo_Output
view_pan_phylo_Input is a reference to a hash where the following keys are defined:
	workspace_name has a value which is a kb_phylogenomics.workspace_name
	input_pangenome_ref has a value which is a kb_phylogenomics.data_obj_ref
	input_speciesTree_ref has a value which is a kb_phylogenomics.data_obj_ref
	save_featuresets has a value which is a kb_phylogenomics.bool
	skip_missing_genomes has a value which is a kb_phylogenomics.bool
	enforce_genome_version_match has a value which is a kb_phylogenomics.bool
	genome_disp_name_config has a value which is a string
workspace_name is a string
data_obj_ref is a string
bool is an int
view_pan_phylo_Output is a reference to a hash where the following keys are defined:
	report_name has a value which is a string
	report_ref has a value which is a string

</pre>

=end html

=begin text

$params is a kb_phylogenomics.view_pan_phylo_Input
$output is a kb_phylogenomics.view_pan_phylo_Output
view_pan_phylo_Input is a reference to a hash where the following keys are defined:
	workspace_name has a value which is a kb_phylogenomics.workspace_name
	input_pangenome_ref has a value which is a kb_phylogenomics.data_obj_ref
	input_speciesTree_ref has a value which is a kb_phylogenomics.data_obj_ref
	save_featuresets has a value which is a kb_phylogenomics.bool
	skip_missing_genomes has a value which is a kb_phylogenomics.bool
	enforce_genome_version_match has a value which is a kb_phylogenomics.bool
	genome_disp_name_config has a value which is a string
workspace_name is a string
data_obj_ref is a string
bool is an int
view_pan_phylo_Output is a reference to a hash where the following keys are defined:
	report_name has a value which is a string
	report_ref has a value which is a string


=end text

=item Description



=back

=cut

 sub view_pan_phylo
{
    my($self, @args) = @_;

# Authentication: required

    if ((my $n = @args) != 1)
    {
	Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
							       "Invalid argument count for function view_pan_phylo (received $n, expecting 1)");
    }
    {
	my($params) = @args;

	my @_bad_arguments;
        (ref($params) eq 'HASH') or push(@_bad_arguments, "Invalid type for argument 1 \"params\" (value was \"$params\")");
        if (@_bad_arguments) {
	    my $msg = "Invalid arguments passed to view_pan_phylo:\n" . join("", map { "\t$_\n" } @_bad_arguments);
	    Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
								   method_name => 'view_pan_phylo');
	}
    }

    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
	    method => "kb_phylogenomics.view_pan_phylo",
	    params => \@args,
    });
    if ($result) {
	if ($result->is_error) {
	    Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
					       code => $result->content->{error}->{code},
					       method_name => 'view_pan_phylo',
					       data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
					      );
	} else {
	    return wantarray ? @{$result->result} : $result->result->[0];
	}
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method view_pan_phylo",
					    status_line => $self->{client}->status_line,
					    method_name => 'view_pan_phylo',
				       );
    }
}
 


=head2 score_orthologs_evolutionary_rates

  $output = $obj->score_orthologs_evolutionary_rates($params)

=over 4

=item Parameter and return types

=begin html

<pre>
$params is a kb_phylogenomics.score_orthologs_evolutionary_rates_Input
$output is a kb_phylogenomics.score_orthologs_evolutionary_rates_Output
score_orthologs_evolutionary_rates_Input is a reference to a hash where the following keys are defined:
	workspace_name has a value which is a kb_phylogenomics.workspace_name
	input_genome_ref has a value which is a kb_phylogenomics.data_obj_ref
	input_pangenome_ref has a value which is a kb_phylogenomics.data_obj_ref
	input_compare_genome_refs has a value which is a kb_phylogenomics.data_obj_ref
	conserved_featureset_nuc_identity_zscore has a value which is a float
	divergent_featureset_nuc_identity_zscore has a value which is a float
	conserved_featureset_aa_identity_zscore has a value which is a float
	divergent_featureset_aa_identity_zscore has a value which is a float
	conserved_featureset_dNdS has a value which is a float
	divergent_featureset_dNdS has a value which is a float
	save_featuresets has a value which is a kb_phylogenomics.bool
	genome_disp_name_config has a value which is a string
workspace_name is a string
data_obj_ref is a string
bool is an int
score_orthologs_evolutionary_rates_Output is a reference to a hash where the following keys are defined:
	report_name has a value which is a string
	report_ref has a value which is a string

</pre>

=end html

=begin text

$params is a kb_phylogenomics.score_orthologs_evolutionary_rates_Input
$output is a kb_phylogenomics.score_orthologs_evolutionary_rates_Output
score_orthologs_evolutionary_rates_Input is a reference to a hash where the following keys are defined:
	workspace_name has a value which is a kb_phylogenomics.workspace_name
	input_genome_ref has a value which is a kb_phylogenomics.data_obj_ref
	input_pangenome_ref has a value which is a kb_phylogenomics.data_obj_ref
	input_compare_genome_refs has a value which is a kb_phylogenomics.data_obj_ref
	conserved_featureset_nuc_identity_zscore has a value which is a float
	divergent_featureset_nuc_identity_zscore has a value which is a float
	conserved_featureset_aa_identity_zscore has a value which is a float
	divergent_featureset_aa_identity_zscore has a value which is a float
	conserved_featureset_dNdS has a value which is a float
	divergent_featureset_dNdS has a value which is a float
	save_featuresets has a value which is a kb_phylogenomics.bool
	genome_disp_name_config has a value which is a string
workspace_name is a string
data_obj_ref is a string
bool is an int
score_orthologs_evolutionary_rates_Output is a reference to a hash where the following keys are defined:
	report_name has a value which is a string
	report_ref has a value which is a string


=end text

=item Description



=back

=cut

 sub score_orthologs_evolutionary_rates
{
    my($self, @args) = @_;

# Authentication: required

    if ((my $n = @args) != 1)
    {
	Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
							       "Invalid argument count for function score_orthologs_evolutionary_rates (received $n, expecting 1)");
    }
    {
	my($params) = @args;

	my @_bad_arguments;
        (ref($params) eq 'HASH') or push(@_bad_arguments, "Invalid type for argument 1 \"params\" (value was \"$params\")");
        if (@_bad_arguments) {
	    my $msg = "Invalid arguments passed to score_orthologs_evolutionary_rates:\n" . join("", map { "\t$_\n" } @_bad_arguments);
	    Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
								   method_name => 'score_orthologs_evolutionary_rates');
	}
    }

    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
	    method => "kb_phylogenomics.score_orthologs_evolutionary_rates",
	    params => \@args,
    });
    if ($result) {
	if ($result->is_error) {
	    Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
					       code => $result->content->{error}->{code},
					       method_name => 'score_orthologs_evolutionary_rates',
					       data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
					      );
	} else {
	    return wantarray ? @{$result->result} : $result->result->[0];
	}
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method score_orthologs_evolutionary_rates",
					    status_line => $self->{client}->status_line,
					    method_name => 'score_orthologs_evolutionary_rates',
				       );
    }
}
 


=head2 find_homologs_with_genome_context

  $output = $obj->find_homologs_with_genome_context($params)

=over 4

=item Parameter and return types

=begin html

<pre>
$params is a kb_phylogenomics.find_homologs_with_genome_context_Input
$output is a kb_phylogenomics.find_homologs_with_genome_context_Output
find_homologs_with_genome_context_Input is a reference to a hash where the following keys are defined:
	workspace_name has a value which is a kb_phylogenomics.workspace_name
	input_featureSet_ref has a value which is a kb_phylogenomics.data_obj_ref
	input_speciesTree_ref has a value which is a kb_phylogenomics.data_obj_ref
	save_per_genome_featureSets has a value which is a kb_phylogenomics.bool
	neighbor_thresh has a value which is an int
	ident_thresh has a value which is a float
	overlap_fraction has a value which is a float
	e_value has a value which is a float
	bitscore has a value which is a float
	color_seed has a value which is a float
workspace_name is a string
data_obj_ref is a string
bool is an int
find_homologs_with_genome_context_Output is a reference to a hash where the following keys are defined:
	report_name has a value which is a string
	report_ref has a value which is a string

</pre>

=end html

=begin text

$params is a kb_phylogenomics.find_homologs_with_genome_context_Input
$output is a kb_phylogenomics.find_homologs_with_genome_context_Output
find_homologs_with_genome_context_Input is a reference to a hash where the following keys are defined:
	workspace_name has a value which is a kb_phylogenomics.workspace_name
	input_featureSet_ref has a value which is a kb_phylogenomics.data_obj_ref
	input_speciesTree_ref has a value which is a kb_phylogenomics.data_obj_ref
	save_per_genome_featureSets has a value which is a kb_phylogenomics.bool
	neighbor_thresh has a value which is an int
	ident_thresh has a value which is a float
	overlap_fraction has a value which is a float
	e_value has a value which is a float
	bitscore has a value which is a float
	color_seed has a value which is a float
workspace_name is a string
data_obj_ref is a string
bool is an int
find_homologs_with_genome_context_Output is a reference to a hash where the following keys are defined:
	report_name has a value which is a string
	report_ref has a value which is a string


=end text

=item Description



=back

=cut

 sub find_homologs_with_genome_context
{
    my($self, @args) = @_;

# Authentication: required

    if ((my $n = @args) != 1)
    {
	Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
							       "Invalid argument count for function find_homologs_with_genome_context (received $n, expecting 1)");
    }
    {
	my($params) = @args;

	my @_bad_arguments;
        (ref($params) eq 'HASH') or push(@_bad_arguments, "Invalid type for argument 1 \"params\" (value was \"$params\")");
        if (@_bad_arguments) {
	    my $msg = "Invalid arguments passed to find_homologs_with_genome_context:\n" . join("", map { "\t$_\n" } @_bad_arguments);
	    Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
								   method_name => 'find_homologs_with_genome_context');
	}
    }

    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
	    method => "kb_phylogenomics.find_homologs_with_genome_context",
	    params => \@args,
    });
    if ($result) {
	if ($result->is_error) {
	    Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
					       code => $result->content->{error}->{code},
					       method_name => 'find_homologs_with_genome_context',
					       data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
					      );
	} else {
	    return wantarray ? @{$result->result} : $result->result->[0];
	}
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method find_homologs_with_genome_context",
					    status_line => $self->{client}->status_line,
					    method_name => 'find_homologs_with_genome_context',
				       );
    }
}
 


=head2 get_configure_categories

  $output = $obj->get_configure_categories($params)

=over 4

=item Parameter and return types

=begin html

<pre>
$params is a kb_phylogenomics.get_configure_categories_Input
$output is a kb_phylogenomics.get_configure_categories_Output
get_configure_categories_Input is a reference to a hash where the following keys are defined:
	params has a value which is a kb_phylogenomics.view_fxn_profile_Input
view_fxn_profile_Input is a reference to a hash where the following keys are defined:
	workspace_name has a value which is a kb_phylogenomics.workspace_name
	input_genomeSet_ref has a value which is a kb_phylogenomics.data_obj_ref
	namespace has a value which is a string
	custom_target_fams has a value which is a kb_phylogenomics.CustomTargetFams
	genome_disp_name_config has a value which is a string
	count_category has a value which is a string
	heatmap has a value which is a kb_phylogenomics.bool
	vertical has a value which is a kb_phylogenomics.bool
	top_hit has a value which is a kb_phylogenomics.bool
	e_value has a value which is a float
	log_base has a value which is a float
	required_COG_annot_perc has a value which is a float
	required_PFAM_annot_perc has a value which is a float
	required_TIGR_annot_perc has a value which is a float
	required_SEED_annot_perc has a value which is a float
	count_hypothetical has a value which is a kb_phylogenomics.bool
	show_blanks has a value which is a kb_phylogenomics.bool
	skip_missing_genomes has a value which is a kb_phylogenomics.bool
	enforce_genome_version_match has a value which is a kb_phylogenomics.bool
workspace_name is a string
data_obj_ref is a string
CustomTargetFams is a reference to a hash where the following keys are defined:
	target_fams has a value which is a reference to a list where each element is a string
	extra_target_fam_groups_COG has a value which is a reference to a list where each element is a string
	extra_target_fam_groups_PFAM has a value which is a reference to a list where each element is a string
	extra_target_fam_groups_TIGR has a value which is a reference to a list where each element is a string
	extra_target_fam_groups_SEED has a value which is a reference to a list where each element is a string
bool is an int
get_configure_categories_Output is a reference to a hash where the following keys are defined:
	cats has a value which is a reference to a list where each element is a string
	cat2name has a value which is a kb_phylogenomics.Cat2Name
	cat2group has a value which is a kb_phylogenomics.Cat2Group
	domfam2cat has a value which is a kb_phylogenomics.DomFam2Cat
	cat2domfams has a value which is a kb_phylogenomics.Cat2DomFams
Cat2Name is a reference to a hash where the following keys are defined:
	namespace has a value which is a kb_phylogenomics.domain_source
	cat has a value which is a kb_phylogenomics.category
domain_source is a string
category is a string
Cat2Group is a reference to a hash where the following keys are defined:
	namespace has a value which is a kb_phylogenomics.domain_source
	cat has a value which is a kb_phylogenomics.category
DomFam2Cat is a reference to a hash where the following keys are defined:
	namespace has a value which is a kb_phylogenomics.domain_source
	domfam has a value which is a kb_phylogenomics.domainfamily
domainfamily is a string
Cat2DomFams is a reference to a hash where the following keys are defined:
	namespace has a value which is a kb_phylogenomics.domain_source
	cat has a value which is a kb_phylogenomics.category

</pre>

=end html

=begin text

$params is a kb_phylogenomics.get_configure_categories_Input
$output is a kb_phylogenomics.get_configure_categories_Output
get_configure_categories_Input is a reference to a hash where the following keys are defined:
	params has a value which is a kb_phylogenomics.view_fxn_profile_Input
view_fxn_profile_Input is a reference to a hash where the following keys are defined:
	workspace_name has a value which is a kb_phylogenomics.workspace_name
	input_genomeSet_ref has a value which is a kb_phylogenomics.data_obj_ref
	namespace has a value which is a string
	custom_target_fams has a value which is a kb_phylogenomics.CustomTargetFams
	genome_disp_name_config has a value which is a string
	count_category has a value which is a string
	heatmap has a value which is a kb_phylogenomics.bool
	vertical has a value which is a kb_phylogenomics.bool
	top_hit has a value which is a kb_phylogenomics.bool
	e_value has a value which is a float
	log_base has a value which is a float
	required_COG_annot_perc has a value which is a float
	required_PFAM_annot_perc has a value which is a float
	required_TIGR_annot_perc has a value which is a float
	required_SEED_annot_perc has a value which is a float
	count_hypothetical has a value which is a kb_phylogenomics.bool
	show_blanks has a value which is a kb_phylogenomics.bool
	skip_missing_genomes has a value which is a kb_phylogenomics.bool
	enforce_genome_version_match has a value which is a kb_phylogenomics.bool
workspace_name is a string
data_obj_ref is a string
CustomTargetFams is a reference to a hash where the following keys are defined:
	target_fams has a value which is a reference to a list where each element is a string
	extra_target_fam_groups_COG has a value which is a reference to a list where each element is a string
	extra_target_fam_groups_PFAM has a value which is a reference to a list where each element is a string
	extra_target_fam_groups_TIGR has a value which is a reference to a list where each element is a string
	extra_target_fam_groups_SEED has a value which is a reference to a list where each element is a string
bool is an int
get_configure_categories_Output is a reference to a hash where the following keys are defined:
	cats has a value which is a reference to a list where each element is a string
	cat2name has a value which is a kb_phylogenomics.Cat2Name
	cat2group has a value which is a kb_phylogenomics.Cat2Group
	domfam2cat has a value which is a kb_phylogenomics.DomFam2Cat
	cat2domfams has a value which is a kb_phylogenomics.Cat2DomFams
Cat2Name is a reference to a hash where the following keys are defined:
	namespace has a value which is a kb_phylogenomics.domain_source
	cat has a value which is a kb_phylogenomics.category
domain_source is a string
category is a string
Cat2Group is a reference to a hash where the following keys are defined:
	namespace has a value which is a kb_phylogenomics.domain_source
	cat has a value which is a kb_phylogenomics.category
DomFam2Cat is a reference to a hash where the following keys are defined:
	namespace has a value which is a kb_phylogenomics.domain_source
	domfam has a value which is a kb_phylogenomics.domainfamily
domainfamily is a string
Cat2DomFams is a reference to a hash where the following keys are defined:
	namespace has a value which is a kb_phylogenomics.domain_source
	cat has a value which is a kb_phylogenomics.category


=end text

=item Description



=back

=cut

 sub get_configure_categories
{
    my($self, @args) = @_;

# Authentication: required

    if ((my $n = @args) != 1)
    {
	Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
							       "Invalid argument count for function get_configure_categories (received $n, expecting 1)");
    }
    {
	my($params) = @args;

	my @_bad_arguments;
        (ref($params) eq 'HASH') or push(@_bad_arguments, "Invalid type for argument 1 \"params\" (value was \"$params\")");
        if (@_bad_arguments) {
	    my $msg = "Invalid arguments passed to get_configure_categories:\n" . join("", map { "\t$_\n" } @_bad_arguments);
	    Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
								   method_name => 'get_configure_categories');
	}
    }

    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
	    method => "kb_phylogenomics.get_configure_categories",
	    params => \@args,
    });
    if ($result) {
	if ($result->is_error) {
	    Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
					       code => $result->content->{error}->{code},
					       method_name => 'get_configure_categories',
					       data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
					      );
	} else {
	    return wantarray ? @{$result->result} : $result->result->[0];
	}
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method get_configure_categories",
					    status_line => $self->{client}->status_line,
					    method_name => 'get_configure_categories',
				       );
    }
}
 
  
sub status
{
    my($self, @args) = @_;
    if ((my $n = @args) != 0) {
        Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
                                   "Invalid argument count for function status (received $n, expecting 0)");
    }
    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
        method => "kb_phylogenomics.status",
        params => \@args,
    });
    if ($result) {
        if ($result->is_error) {
            Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
                           code => $result->content->{error}->{code},
                           method_name => 'status',
                           data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
                          );
        } else {
            return wantarray ? @{$result->result} : $result->result->[0];
        }
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method status",
                        status_line => $self->{client}->status_line,
                        method_name => 'status',
                       );
    }
}
   

sub version {
    my ($self) = @_;
    my $result = $self->{client}->call($self->{url}, $self->{headers}, {
        method => "kb_phylogenomics.version",
        params => [],
    });
    if ($result) {
        if ($result->is_error) {
            Bio::KBase::Exceptions::JSONRPC->throw(
                error => $result->error_message,
                code => $result->content->{code},
                method_name => 'get_configure_categories',
            );
        } else {
            return wantarray ? @{$result->result} : $result->result->[0];
        }
    } else {
        Bio::KBase::Exceptions::HTTP->throw(
            error => "Error invoking method get_configure_categories",
            status_line => $self->{client}->status_line,
            method_name => 'get_configure_categories',
        );
    }
}

sub _validate_version {
    my ($self) = @_;
    my $svr_version = $self->version();
    my $client_version = $VERSION;
    my ($cMajor, $cMinor) = split(/\./, $client_version);
    my ($sMajor, $sMinor) = split(/\./, $svr_version);
    if ($sMajor != $cMajor) {
        Bio::KBase::Exceptions::ClientServerIncompatible->throw(
            error => "Major version numbers differ.",
            server_version => $svr_version,
            client_version => $client_version
        );
    }
    if ($sMinor < $cMinor) {
        Bio::KBase::Exceptions::ClientServerIncompatible->throw(
            error => "Client minor version greater than Server minor version.",
            server_version => $svr_version,
            client_version => $client_version
        );
    }
    if ($sMinor > $cMinor) {
        warn "New client version available for kb_phylogenomics::kb_phylogenomicsClient\n";
    }
    if ($sMajor == 0) {
        warn "kb_phylogenomics::kb_phylogenomicsClient version is $svr_version. API subject to change.\n";
    }
}

=head1 TYPES



=head2 workspace_name

=over 4



=item Description

** Common types


=item Definition

=begin html

<pre>
a string
</pre>

=end html

=begin text

a string

=end text

=back



=head2 data_obj_ref

=over 4



=item Definition

=begin html

<pre>
a string
</pre>

=end html

=begin text

a string

=end text

=back



=head2 data_obj_name

=over 4



=item Definition

=begin html

<pre>
a string
</pre>

=end html

=begin text

a string

=end text

=back



=head2 bool

=over 4



=item Definition

=begin html

<pre>
an int
</pre>

=end html

=begin text

an int

=end text

=back



=head2 build_gene_tree_Input

=over 4



=item Description

build_gene_tree()
**
** build a gene tree for a featureset


=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
workspace_name has a value which is a kb_phylogenomics.workspace_name
desc has a value which is a string
input_featureSet_ref has a value which is a kb_phylogenomics.data_obj_ref
output_tree_name has a value which is a kb_phylogenomics.data_obj_name
genome_disp_name_config has a value which is a string
skip_trimming has a value which is a kb_phylogenomics.bool
muscle_maxiters has a value which is an int
muscle_maxhours has a value which is a float
gblocks_trim_level has a value which is an int
gblocks_min_seqs_for_conserved has a value which is an int
gblocks_min_seqs_for_flank has a value which is an int
gblocks_max_pos_contig_nonconserved has a value which is an int
gblocks_min_block_len has a value which is an int
gblocks_remove_mask_positions_flag has a value which is an int
fasttree_fastest has a value which is an int
fasttree_pseudo has a value which is an int
fasttree_gtr has a value which is an int
fasttree_wag has a value which is an int
fasttree_noml has a value which is an int
fasttree_nome has a value which is an int
fasttree_cat has a value which is an int
fasttree_nocat has a value which is an int
fasttree_gamma has a value which is an int

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
workspace_name has a value which is a kb_phylogenomics.workspace_name
desc has a value which is a string
input_featureSet_ref has a value which is a kb_phylogenomics.data_obj_ref
output_tree_name has a value which is a kb_phylogenomics.data_obj_name
genome_disp_name_config has a value which is a string
skip_trimming has a value which is a kb_phylogenomics.bool
muscle_maxiters has a value which is an int
muscle_maxhours has a value which is a float
gblocks_trim_level has a value which is an int
gblocks_min_seqs_for_conserved has a value which is an int
gblocks_min_seqs_for_flank has a value which is an int
gblocks_max_pos_contig_nonconserved has a value which is an int
gblocks_min_block_len has a value which is an int
gblocks_remove_mask_positions_flag has a value which is an int
fasttree_fastest has a value which is an int
fasttree_pseudo has a value which is an int
fasttree_gtr has a value which is an int
fasttree_wag has a value which is an int
fasttree_noml has a value which is an int
fasttree_nome has a value which is an int
fasttree_cat has a value which is an int
fasttree_nocat has a value which is an int
fasttree_gamma has a value which is an int


=end text

=back



=head2 build_gene_tree_Output

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
report_name has a value which is a string
report_ref has a value which is a string

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
report_name has a value which is a string
report_ref has a value which is a string


=end text

=back



=head2 build_strain_tree_Input

=over 4



=item Description

build_strain_tree()
**
** build a species tree for a collection of strain genomes


=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
workspace_name has a value which is a kb_phylogenomics.workspace_name
desc has a value which is a string
input_genome_refs has a value which is a kb_phylogenomics.data_obj_ref
output_tree_name has a value which is a kb_phylogenomics.data_obj_name
genome_disp_name_config has a value which is a string
skip_trimming has a value which is a kb_phylogenomics.bool
muscle_maxiters has a value which is an int
muscle_maxhours has a value which is a float
gblocks_trim_level has a value which is an int
gblocks_min_seqs_for_conserved has a value which is an int
gblocks_min_seqs_for_flank has a value which is an int
gblocks_max_pos_contig_nonconserved has a value which is an int
gblocks_min_block_len has a value which is an int
gblocks_remove_mask_positions_flag has a value which is an int
fasttree_fastest has a value which is an int
fasttree_pseudo has a value which is an int
fasttree_gtr has a value which is an int
fasttree_wag has a value which is an int
fasttree_noml has a value which is an int
fasttree_nome has a value which is an int
fasttree_cat has a value which is an int
fasttree_nocat has a value which is an int
fasttree_gamma has a value which is an int

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
workspace_name has a value which is a kb_phylogenomics.workspace_name
desc has a value which is a string
input_genome_refs has a value which is a kb_phylogenomics.data_obj_ref
output_tree_name has a value which is a kb_phylogenomics.data_obj_name
genome_disp_name_config has a value which is a string
skip_trimming has a value which is a kb_phylogenomics.bool
muscle_maxiters has a value which is an int
muscle_maxhours has a value which is a float
gblocks_trim_level has a value which is an int
gblocks_min_seqs_for_conserved has a value which is an int
gblocks_min_seqs_for_flank has a value which is an int
gblocks_max_pos_contig_nonconserved has a value which is an int
gblocks_min_block_len has a value which is an int
gblocks_remove_mask_positions_flag has a value which is an int
fasttree_fastest has a value which is an int
fasttree_pseudo has a value which is an int
fasttree_gtr has a value which is an int
fasttree_wag has a value which is an int
fasttree_noml has a value which is an int
fasttree_nome has a value which is an int
fasttree_cat has a value which is an int
fasttree_nocat has a value which is an int
fasttree_gamma has a value which is an int


=end text

=back



=head2 build_strain_tree_Output

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
report_name has a value which is a string
report_ref has a value which is a string

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
report_name has a value which is a string
report_ref has a value which is a string


=end text

=back



=head2 build_pangenome_species_tree_Input

=over 4



=item Description

build_pangenome_species_tree()
**
** build a species tree using the single copy genes from a pangenome


=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
workspace_name has a value which is a kb_phylogenomics.workspace_name
desc has a value which is a string
input_pangenome_ref has a value which is a kb_phylogenomics.data_obj_ref
output_tree_name has a value which is a kb_phylogenomics.data_obj_name
genome_disp_name_config has a value which is a string
skip_trimming has a value which is a kb_phylogenomics.bool
perc_marker_presence_min has a value which is a float
muscle_maxiters has a value which is an int
muscle_maxhours has a value which is a float
gblocks_trim_level has a value which is an int
gblocks_min_seqs_for_conserved has a value which is an int
gblocks_min_seqs_for_flank has a value which is an int
gblocks_max_pos_contig_nonconserved has a value which is an int
gblocks_min_block_len has a value which is an int
gblocks_remove_mask_positions_flag has a value which is an int
fasttree_fastest has a value which is an int
fasttree_pseudo has a value which is an int
fasttree_gtr has a value which is an int
fasttree_wag has a value which is an int
fasttree_noml has a value which is an int
fasttree_nome has a value which is an int
fasttree_cat has a value which is an int
fasttree_nocat has a value which is an int
fasttree_gamma has a value which is an int

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
workspace_name has a value which is a kb_phylogenomics.workspace_name
desc has a value which is a string
input_pangenome_ref has a value which is a kb_phylogenomics.data_obj_ref
output_tree_name has a value which is a kb_phylogenomics.data_obj_name
genome_disp_name_config has a value which is a string
skip_trimming has a value which is a kb_phylogenomics.bool
perc_marker_presence_min has a value which is a float
muscle_maxiters has a value which is an int
muscle_maxhours has a value which is a float
gblocks_trim_level has a value which is an int
gblocks_min_seqs_for_conserved has a value which is an int
gblocks_min_seqs_for_flank has a value which is an int
gblocks_max_pos_contig_nonconserved has a value which is an int
gblocks_min_block_len has a value which is an int
gblocks_remove_mask_positions_flag has a value which is an int
fasttree_fastest has a value which is an int
fasttree_pseudo has a value which is an int
fasttree_gtr has a value which is an int
fasttree_wag has a value which is an int
fasttree_noml has a value which is an int
fasttree_nome has a value which is an int
fasttree_cat has a value which is an int
fasttree_nocat has a value which is an int
fasttree_gamma has a value which is an int


=end text

=back



=head2 build_pangenome_species_tree_Output

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
report_name has a value which is a string
report_ref has a value which is a string

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
report_name has a value which is a string
report_ref has a value which is a string


=end text

=back



=head2 view_tree_Input

=over 4



=item Description

view_tree()
**
** show a KBase Tree and make newick and images downloadable


=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
workspace_name has a value which is a kb_phylogenomics.workspace_name
input_tree_ref has a value which is a kb_phylogenomics.data_obj_ref
desc has a value which is a string
show_skeleton_genome_sci_name has a value which is a kb_phylogenomics.bool
reference_genome_disp has a value which is a reference to a hash where the key is a kb_phylogenomics.data_obj_ref and the value is a reference to a hash where the key is a string and the value is a string
skeleton_genome_disp has a value which is a reference to a hash where the key is a kb_phylogenomics.data_obj_ref and the value is a reference to a hash where the key is a string and the value is a string
user_genome_disp has a value which is a reference to a hash where the key is a kb_phylogenomics.data_obj_ref and the value is a reference to a hash where the key is a string and the value is a string
user2_genome_disp has a value which is a reference to a hash where the key is a kb_phylogenomics.data_obj_ref and the value is a reference to a hash where the key is a string and the value is a string
color_for_reference_genomes has a value which is a string
color_for_skeleton_genomes has a value which is a string
color_for_user_genomes has a value which is a string
color_for_user2_genomes has a value which is a string
tree_shape has a value which is a string

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
workspace_name has a value which is a kb_phylogenomics.workspace_name
input_tree_ref has a value which is a kb_phylogenomics.data_obj_ref
desc has a value which is a string
show_skeleton_genome_sci_name has a value which is a kb_phylogenomics.bool
reference_genome_disp has a value which is a reference to a hash where the key is a kb_phylogenomics.data_obj_ref and the value is a reference to a hash where the key is a string and the value is a string
skeleton_genome_disp has a value which is a reference to a hash where the key is a kb_phylogenomics.data_obj_ref and the value is a reference to a hash where the key is a string and the value is a string
user_genome_disp has a value which is a reference to a hash where the key is a kb_phylogenomics.data_obj_ref and the value is a reference to a hash where the key is a string and the value is a string
user2_genome_disp has a value which is a reference to a hash where the key is a kb_phylogenomics.data_obj_ref and the value is a reference to a hash where the key is a string and the value is a string
color_for_reference_genomes has a value which is a string
color_for_skeleton_genomes has a value which is a string
color_for_user_genomes has a value which is a string
color_for_user2_genomes has a value which is a string
tree_shape has a value which is a string


=end text

=back



=head2 view_tree_Output

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
report_name has a value which is a string
report_ref has a value which is a string

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
report_name has a value which is a string
report_ref has a value which is a string


=end text

=back



=head2 trim_speciestree_to_genomeset_Input

=over 4



=item Description

trim_speciestree_to_genomeset()
**
** reduce tree to match genomes found in genomeset


=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
workspace_name has a value which is a kb_phylogenomics.workspace_name
input_genomeSet_ref has a value which is a kb_phylogenomics.data_obj_ref
input_tree_ref has a value which is a kb_phylogenomics.data_obj_ref
output_tree_name has a value which is a kb_phylogenomics.data_obj_name
desc has a value which is a string
show_skeleton_genome_sci_name has a value which is a kb_phylogenomics.bool
enforce_genome_version_match has a value which is a kb_phylogenomics.bool
reference_genome_disp has a value which is a reference to a hash where the key is a kb_phylogenomics.data_obj_ref and the value is a reference to a hash where the key is a string and the value is a string
skeleton_genome_disp has a value which is a reference to a hash where the key is a kb_phylogenomics.data_obj_ref and the value is a reference to a hash where the key is a string and the value is a string
user_genome_disp has a value which is a reference to a hash where the key is a kb_phylogenomics.data_obj_ref and the value is a reference to a hash where the key is a string and the value is a string
user2_genome_disp has a value which is a reference to a hash where the key is a kb_phylogenomics.data_obj_ref and the value is a reference to a hash where the key is a string and the value is a string
color_for_reference_genomes has a value which is a string
color_for_skeleton_genomes has a value which is a string
color_for_user_genomes has a value which is a string
color_for_user2_genomes has a value which is a string
tree_shape has a value which is a string

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
workspace_name has a value which is a kb_phylogenomics.workspace_name
input_genomeSet_ref has a value which is a kb_phylogenomics.data_obj_ref
input_tree_ref has a value which is a kb_phylogenomics.data_obj_ref
output_tree_name has a value which is a kb_phylogenomics.data_obj_name
desc has a value which is a string
show_skeleton_genome_sci_name has a value which is a kb_phylogenomics.bool
enforce_genome_version_match has a value which is a kb_phylogenomics.bool
reference_genome_disp has a value which is a reference to a hash where the key is a kb_phylogenomics.data_obj_ref and the value is a reference to a hash where the key is a string and the value is a string
skeleton_genome_disp has a value which is a reference to a hash where the key is a kb_phylogenomics.data_obj_ref and the value is a reference to a hash where the key is a string and the value is a string
user_genome_disp has a value which is a reference to a hash where the key is a kb_phylogenomics.data_obj_ref and the value is a reference to a hash where the key is a string and the value is a string
user2_genome_disp has a value which is a reference to a hash where the key is a kb_phylogenomics.data_obj_ref and the value is a reference to a hash where the key is a string and the value is a string
color_for_reference_genomes has a value which is a string
color_for_skeleton_genomes has a value which is a string
color_for_user_genomes has a value which is a string
color_for_user2_genomes has a value which is a string
tree_shape has a value which is a string


=end text

=back



=head2 trim_speciestree_to_genomeset_Output

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
report_name has a value which is a string
report_ref has a value which is a string

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
report_name has a value which is a string
report_ref has a value which is a string


=end text

=back



=head2 trim_genetree_to_genomeset_Input

=over 4



=item Description

trim_genetree_to_genomeset()
**
** reduce tree to match genomes found in genomeset (optionally skip AMA genes)


=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
workspace_name has a value which is a kb_phylogenomics.workspace_name
input_genomeSet_ref has a value which is a kb_phylogenomics.data_obj_ref
input_tree_ref has a value which is a kb_phylogenomics.data_obj_ref
output_tree_name has a value which is a kb_phylogenomics.data_obj_name
desc has a value which is a string
enforce_genome_version_match has a value which is a kb_phylogenomics.bool
keep_ama_genes has a value which is a kb_phylogenomics.bool

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
workspace_name has a value which is a kb_phylogenomics.workspace_name
input_genomeSet_ref has a value which is a kb_phylogenomics.data_obj_ref
input_tree_ref has a value which is a kb_phylogenomics.data_obj_ref
output_tree_name has a value which is a kb_phylogenomics.data_obj_name
desc has a value which is a string
enforce_genome_version_match has a value which is a kb_phylogenomics.bool
keep_ama_genes has a value which is a kb_phylogenomics.bool


=end text

=back



=head2 trim_genetree_to_genomeset_Output

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
report_name has a value which is a string
report_ref has a value which is a string

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
report_name has a value which is a string
report_ref has a value which is a string


=end text

=back



=head2 build_microbial_speciestree_Input

=over 4



=item Description

build_microbial_speciestree()
**
** run Insert Set of Genomes into Species Tree with extra features


=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
workspace_name has a value which is a kb_phylogenomics.workspace_name
input_genome_refs has a value which is a kb_phylogenomics.data_obj_ref
input_genome2_refs has a value which is a kb_phylogenomics.data_obj_ref
output_tree_name has a value which is a kb_phylogenomics.data_obj_name
desc has a value which is a string
show_skeleton_genome_sci_name has a value which is a kb_phylogenomics.bool
skeleton_set has a value which is a string
color_for_skeleton_genomes has a value which is a string
color_for_user_genomes has a value which is a string
color_for_user2_genomes has a value which is a string

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
workspace_name has a value which is a kb_phylogenomics.workspace_name
input_genome_refs has a value which is a kb_phylogenomics.data_obj_ref
input_genome2_refs has a value which is a kb_phylogenomics.data_obj_ref
output_tree_name has a value which is a kb_phylogenomics.data_obj_name
desc has a value which is a string
show_skeleton_genome_sci_name has a value which is a kb_phylogenomics.bool
skeleton_set has a value which is a string
color_for_skeleton_genomes has a value which is a string
color_for_user_genomes has a value which is a string
color_for_user2_genomes has a value which is a string


=end text

=back



=head2 build_microbial_speciestree_Output

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
report_name has a value which is a string
report_ref has a value which is a string

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
report_name has a value which is a string
report_ref has a value which is a string


=end text

=back



=head2 localize_DomainAnnotations_Input

=over 4



=item Description

localize_DomainAnnotations()
**
** point all DomainAnnotations at local copies of Genome Objects


=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
workspace_name has a value which is a kb_phylogenomics.workspace_name
input_DomainAnnotation_refs has a value which is a kb_phylogenomics.data_obj_ref

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
workspace_name has a value which is a kb_phylogenomics.workspace_name
input_DomainAnnotation_refs has a value which is a kb_phylogenomics.data_obj_ref


=end text

=back



=head2 localize_DomainAnnotations_Output

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
report_name has a value which is a string
report_ref has a value which is a string

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
report_name has a value which is a string
report_ref has a value which is a string


=end text

=back



=head2 run_DomainAnnotation_Sets_Input

=over 4



=item Description

run_DomainAnnotation_Sets()
**
** run the DomainAnnotation App against a GenomeSet


=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
workspace_name has a value which is a kb_phylogenomics.workspace_name
input_genomeSet_ref has a value which is a kb_phylogenomics.data_obj_ref
override_annot has a value which is a kb_phylogenomics.bool

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
workspace_name has a value which is a kb_phylogenomics.workspace_name
input_genomeSet_ref has a value which is a kb_phylogenomics.data_obj_ref
override_annot has a value which is a kb_phylogenomics.bool


=end text

=back



=head2 run_DomainAnnotation_Sets_Output

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
report_name has a value which is a string
report_ref has a value which is a string

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
report_name has a value which is a string
report_ref has a value which is a string


=end text

=back



=head2 CustomTargetFams

=over 4



=item Description

parameter groups


=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
target_fams has a value which is a reference to a list where each element is a string
extra_target_fam_groups_COG has a value which is a reference to a list where each element is a string
extra_target_fam_groups_PFAM has a value which is a reference to a list where each element is a string
extra_target_fam_groups_TIGR has a value which is a reference to a list where each element is a string
extra_target_fam_groups_SEED has a value which is a reference to a list where each element is a string

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
target_fams has a value which is a reference to a list where each element is a string
extra_target_fam_groups_COG has a value which is a reference to a list where each element is a string
extra_target_fam_groups_PFAM has a value which is a reference to a list where each element is a string
extra_target_fam_groups_TIGR has a value which is a reference to a list where each element is a string
extra_target_fam_groups_SEED has a value which is a reference to a list where each element is a string


=end text

=back



=head2 view_fxn_profile_Input

=over 4



=item Description

view_fxn_profile()
**
** show a table/heatmap of general categories or custom gene families for a set of Genomes


=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
workspace_name has a value which is a kb_phylogenomics.workspace_name
input_genomeSet_ref has a value which is a kb_phylogenomics.data_obj_ref
namespace has a value which is a string
custom_target_fams has a value which is a kb_phylogenomics.CustomTargetFams
genome_disp_name_config has a value which is a string
count_category has a value which is a string
heatmap has a value which is a kb_phylogenomics.bool
vertical has a value which is a kb_phylogenomics.bool
top_hit has a value which is a kb_phylogenomics.bool
e_value has a value which is a float
log_base has a value which is a float
required_COG_annot_perc has a value which is a float
required_PFAM_annot_perc has a value which is a float
required_TIGR_annot_perc has a value which is a float
required_SEED_annot_perc has a value which is a float
count_hypothetical has a value which is a kb_phylogenomics.bool
show_blanks has a value which is a kb_phylogenomics.bool
skip_missing_genomes has a value which is a kb_phylogenomics.bool
enforce_genome_version_match has a value which is a kb_phylogenomics.bool

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
workspace_name has a value which is a kb_phylogenomics.workspace_name
input_genomeSet_ref has a value which is a kb_phylogenomics.data_obj_ref
namespace has a value which is a string
custom_target_fams has a value which is a kb_phylogenomics.CustomTargetFams
genome_disp_name_config has a value which is a string
count_category has a value which is a string
heatmap has a value which is a kb_phylogenomics.bool
vertical has a value which is a kb_phylogenomics.bool
top_hit has a value which is a kb_phylogenomics.bool
e_value has a value which is a float
log_base has a value which is a float
required_COG_annot_perc has a value which is a float
required_PFAM_annot_perc has a value which is a float
required_TIGR_annot_perc has a value which is a float
required_SEED_annot_perc has a value which is a float
count_hypothetical has a value which is a kb_phylogenomics.bool
show_blanks has a value which is a kb_phylogenomics.bool
skip_missing_genomes has a value which is a kb_phylogenomics.bool
enforce_genome_version_match has a value which is a kb_phylogenomics.bool


=end text

=back



=head2 view_fxn_profile_Output

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
report_name has a value which is a string
report_ref has a value which is a string

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
report_name has a value which is a string
report_ref has a value which is a string


=end text

=back



=head2 view_fxn_profile_featureSet_Input

=over 4



=item Description

view_fxn_profile_featureSet()
**
** show a table/heatmap of general categories or custom gene families for a set of Genomes


=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
workspace_name has a value which is a kb_phylogenomics.workspace_name
input_featureSet_ref has a value which is a kb_phylogenomics.data_obj_ref
namespace has a value which is a string
custom_target_fams has a value which is a kb_phylogenomics.CustomTargetFams
genome_disp_name_config has a value which is a string
count_category has a value which is a string
heatmap has a value which is a kb_phylogenomics.bool
vertical has a value which is a kb_phylogenomics.bool
top_hit has a value which is a kb_phylogenomics.bool
e_value has a value which is a float
log_base has a value which is a float
required_COG_annot_perc has a value which is a float
required_PFAM_annot_perc has a value which is a float
required_TIGR_annot_perc has a value which is a float
required_SEED_annot_perc has a value which is a float
count_hypothetical has a value which is a kb_phylogenomics.bool
show_blanks has a value which is a kb_phylogenomics.bool
skip_missing_genomes has a value which is a kb_phylogenomics.bool
enforce_genome_version_match has a value which is a kb_phylogenomics.bool

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
workspace_name has a value which is a kb_phylogenomics.workspace_name
input_featureSet_ref has a value which is a kb_phylogenomics.data_obj_ref
namespace has a value which is a string
custom_target_fams has a value which is a kb_phylogenomics.CustomTargetFams
genome_disp_name_config has a value which is a string
count_category has a value which is a string
heatmap has a value which is a kb_phylogenomics.bool
vertical has a value which is a kb_phylogenomics.bool
top_hit has a value which is a kb_phylogenomics.bool
e_value has a value which is a float
log_base has a value which is a float
required_COG_annot_perc has a value which is a float
required_PFAM_annot_perc has a value which is a float
required_TIGR_annot_perc has a value which is a float
required_SEED_annot_perc has a value which is a float
count_hypothetical has a value which is a kb_phylogenomics.bool
show_blanks has a value which is a kb_phylogenomics.bool
skip_missing_genomes has a value which is a kb_phylogenomics.bool
enforce_genome_version_match has a value which is a kb_phylogenomics.bool


=end text

=back



=head2 view_fxn_profile_featureSet_Output

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
report_name has a value which is a string
report_ref has a value which is a string

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
report_name has a value which is a string
report_ref has a value which is a string


=end text

=back



=head2 view_fxn_profile_phylo_Input

=over 4



=item Description

view_fxn_profile_phylo()
**
** show a table/heatmap of general categories or custom gene families for a set of Genomes using the species tree


=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
workspace_name has a value which is a kb_phylogenomics.workspace_name
input_speciesTree_ref has a value which is a kb_phylogenomics.data_obj_ref
namespace has a value which is a string
custom_target_fams has a value which is a kb_phylogenomics.CustomTargetFams
genome_disp_name_config has a value which is a string
count_category has a value which is a string
heatmap has a value which is a kb_phylogenomics.bool
vertical has a value which is a kb_phylogenomics.bool
top_hit has a value which is a kb_phylogenomics.bool
e_value has a value which is a float
log_base has a value which is a float
required_COG_annot_perc has a value which is a float
required_PFAM_annot_perc has a value which is a float
required_TIGR_annot_perc has a value which is a float
required_SEED_annot_perc has a value which is a float
count_hypothetical has a value which is a kb_phylogenomics.bool
show_blanks has a value which is a kb_phylogenomics.bool
skip_missing_genomes has a value which is a kb_phylogenomics.bool
enforce_genome_version_match has a value which is a kb_phylogenomics.bool

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
workspace_name has a value which is a kb_phylogenomics.workspace_name
input_speciesTree_ref has a value which is a kb_phylogenomics.data_obj_ref
namespace has a value which is a string
custom_target_fams has a value which is a kb_phylogenomics.CustomTargetFams
genome_disp_name_config has a value which is a string
count_category has a value which is a string
heatmap has a value which is a kb_phylogenomics.bool
vertical has a value which is a kb_phylogenomics.bool
top_hit has a value which is a kb_phylogenomics.bool
e_value has a value which is a float
log_base has a value which is a float
required_COG_annot_perc has a value which is a float
required_PFAM_annot_perc has a value which is a float
required_TIGR_annot_perc has a value which is a float
required_SEED_annot_perc has a value which is a float
count_hypothetical has a value which is a kb_phylogenomics.bool
show_blanks has a value which is a kb_phylogenomics.bool
skip_missing_genomes has a value which is a kb_phylogenomics.bool
enforce_genome_version_match has a value which is a kb_phylogenomics.bool


=end text

=back



=head2 view_fxn_profile_phylo_Output

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
report_name has a value which is a string
report_ref has a value which is a string

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
report_name has a value which is a string
report_ref has a value which is a string


=end text

=back



=head2 view_genome_circle_plot_Input

=over 4



=item Description

view_genome_circle_plot()
**
** build a circle plot of a microbial genome


=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
workspace_name has a value which is a kb_phylogenomics.workspace_name
input_genome_ref has a value which is a kb_phylogenomics.data_obj_ref

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
workspace_name has a value which is a kb_phylogenomics.workspace_name
input_genome_ref has a value which is a kb_phylogenomics.data_obj_ref


=end text

=back



=head2 view_genome_circle_plot_Output

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
report_name has a value which is a string
report_ref has a value which is a string

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
report_name has a value which is a string
report_ref has a value which is a string


=end text

=back



=head2 view_pan_circle_plot_Input

=over 4



=item Description

view_pan_circle_plot()
**
** build a circle plot of a microbial genome with its pangenome members


=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
workspace_name has a value which is a kb_phylogenomics.workspace_name
input_genome_ref has a value which is a kb_phylogenomics.data_obj_ref
input_pangenome_ref has a value which is a kb_phylogenomics.data_obj_ref
input_compare_genome_refs has a value which is a kb_phylogenomics.data_obj_ref
input_outgroup_genome_refs has a value which is a kb_phylogenomics.data_obj_ref
save_featuresets has a value which is a kb_phylogenomics.bool
genome_disp_name_config has a value which is a string

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
workspace_name has a value which is a kb_phylogenomics.workspace_name
input_genome_ref has a value which is a kb_phylogenomics.data_obj_ref
input_pangenome_ref has a value which is a kb_phylogenomics.data_obj_ref
input_compare_genome_refs has a value which is a kb_phylogenomics.data_obj_ref
input_outgroup_genome_refs has a value which is a kb_phylogenomics.data_obj_ref
save_featuresets has a value which is a kb_phylogenomics.bool
genome_disp_name_config has a value which is a string


=end text

=back



=head2 view_pan_circle_plot_Output

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
report_name has a value which is a string
report_ref has a value which is a string

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
report_name has a value which is a string
report_ref has a value which is a string


=end text

=back



=head2 view_pan_accumulation_plot_Input

=over 4



=item Description

view_pan_accumulation_plot()
**
** build an accumulation plot of a pangenome


=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
workspace_name has a value which is a kb_phylogenomics.workspace_name
input_genome_ref has a value which is a kb_phylogenomics.data_obj_ref
input_pangenome_ref has a value which is a kb_phylogenomics.data_obj_ref

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
workspace_name has a value which is a kb_phylogenomics.workspace_name
input_genome_ref has a value which is a kb_phylogenomics.data_obj_ref
input_pangenome_ref has a value which is a kb_phylogenomics.data_obj_ref


=end text

=back



=head2 view_pan_accumulation_plot_Output

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
report_name has a value which is a string
report_ref has a value which is a string

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
report_name has a value which is a string
report_ref has a value which is a string


=end text

=back



=head2 view_pan_flower_venn_Input

=over 4



=item Description

view_pan_flower_venn()
**
** build a multi-member pangenome flower venn diagram


=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
workspace_name has a value which is a kb_phylogenomics.workspace_name
input_genome_ref has a value which is a kb_phylogenomics.data_obj_ref
input_pangenome_ref has a value which is a kb_phylogenomics.data_obj_ref

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
workspace_name has a value which is a kb_phylogenomics.workspace_name
input_genome_ref has a value which is a kb_phylogenomics.data_obj_ref
input_pangenome_ref has a value which is a kb_phylogenomics.data_obj_ref


=end text

=back



=head2 view_pan_flower_venn_Output

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
report_name has a value which is a string
report_ref has a value which is a string

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
report_name has a value which is a string
report_ref has a value which is a string


=end text

=back



=head2 view_pan_pairwise_overlap_Input

=over 4



=item Description

view_pan_pairwise_overlap()
**
** build a multi-member pangenome pairwise overlap plot


=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
workspace_name has a value which is a kb_phylogenomics.workspace_name
input_genome_ref has a value which is a kb_phylogenomics.data_obj_ref
input_pangenome_ref has a value which is a kb_phylogenomics.data_obj_ref

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
workspace_name has a value which is a kb_phylogenomics.workspace_name
input_genome_ref has a value which is a kb_phylogenomics.data_obj_ref
input_pangenome_ref has a value which is a kb_phylogenomics.data_obj_ref


=end text

=back



=head2 view_pan_pairwise_overlap_Output

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
report_name has a value which is a string
report_ref has a value which is a string

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
report_name has a value which is a string
report_ref has a value which is a string


=end text

=back



=head2 view_pan_phylo_Input

=over 4



=item Description

view_pan_phylo()
**
** show the pangenome accumulation using a tree


=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
workspace_name has a value which is a kb_phylogenomics.workspace_name
input_pangenome_ref has a value which is a kb_phylogenomics.data_obj_ref
input_speciesTree_ref has a value which is a kb_phylogenomics.data_obj_ref
save_featuresets has a value which is a kb_phylogenomics.bool
skip_missing_genomes has a value which is a kb_phylogenomics.bool
enforce_genome_version_match has a value which is a kb_phylogenomics.bool
genome_disp_name_config has a value which is a string

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
workspace_name has a value which is a kb_phylogenomics.workspace_name
input_pangenome_ref has a value which is a kb_phylogenomics.data_obj_ref
input_speciesTree_ref has a value which is a kb_phylogenomics.data_obj_ref
save_featuresets has a value which is a kb_phylogenomics.bool
skip_missing_genomes has a value which is a kb_phylogenomics.bool
enforce_genome_version_match has a value which is a kb_phylogenomics.bool
genome_disp_name_config has a value which is a string


=end text

=back



=head2 view_pan_phylo_Output

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
report_name has a value which is a string
report_ref has a value which is a string

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
report_name has a value which is a string
report_ref has a value which is a string


=end text

=back



=head2 score_orthologs_evolutionary_rates_Input

=over 4



=item Description

score_orthologs_evolutionary_rates()
**
** score mutations between a base genome and additional genomes
**   using the Pangenome to determine orthologs
**   (split paralogs in larger clusters)


=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
workspace_name has a value which is a kb_phylogenomics.workspace_name
input_genome_ref has a value which is a kb_phylogenomics.data_obj_ref
input_pangenome_ref has a value which is a kb_phylogenomics.data_obj_ref
input_compare_genome_refs has a value which is a kb_phylogenomics.data_obj_ref
conserved_featureset_nuc_identity_zscore has a value which is a float
divergent_featureset_nuc_identity_zscore has a value which is a float
conserved_featureset_aa_identity_zscore has a value which is a float
divergent_featureset_aa_identity_zscore has a value which is a float
conserved_featureset_dNdS has a value which is a float
divergent_featureset_dNdS has a value which is a float
save_featuresets has a value which is a kb_phylogenomics.bool
genome_disp_name_config has a value which is a string

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
workspace_name has a value which is a kb_phylogenomics.workspace_name
input_genome_ref has a value which is a kb_phylogenomics.data_obj_ref
input_pangenome_ref has a value which is a kb_phylogenomics.data_obj_ref
input_compare_genome_refs has a value which is a kb_phylogenomics.data_obj_ref
conserved_featureset_nuc_identity_zscore has a value which is a float
divergent_featureset_nuc_identity_zscore has a value which is a float
conserved_featureset_aa_identity_zscore has a value which is a float
divergent_featureset_aa_identity_zscore has a value which is a float
conserved_featureset_dNdS has a value which is a float
divergent_featureset_dNdS has a value which is a float
save_featuresets has a value which is a kb_phylogenomics.bool
genome_disp_name_config has a value which is a string


=end text

=back



=head2 score_orthologs_evolutionary_rates_Output

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
report_name has a value which is a string
report_ref has a value which is a string

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
report_name has a value which is a string
report_ref has a value which is a string


=end text

=back



=head2 find_homologs_with_genome_context_Input

=over 4



=item Description

find_homologs_with_genome_context()
**
** show homolgous genes across multiple genomes within genome context against species tree


=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
workspace_name has a value which is a kb_phylogenomics.workspace_name
input_featureSet_ref has a value which is a kb_phylogenomics.data_obj_ref
input_speciesTree_ref has a value which is a kb_phylogenomics.data_obj_ref
save_per_genome_featureSets has a value which is a kb_phylogenomics.bool
neighbor_thresh has a value which is an int
ident_thresh has a value which is a float
overlap_fraction has a value which is a float
e_value has a value which is a float
bitscore has a value which is a float
color_seed has a value which is a float

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
workspace_name has a value which is a kb_phylogenomics.workspace_name
input_featureSet_ref has a value which is a kb_phylogenomics.data_obj_ref
input_speciesTree_ref has a value which is a kb_phylogenomics.data_obj_ref
save_per_genome_featureSets has a value which is a kb_phylogenomics.bool
neighbor_thresh has a value which is an int
ident_thresh has a value which is a float
overlap_fraction has a value which is a float
e_value has a value which is a float
bitscore has a value which is a float
color_seed has a value which is a float


=end text

=back



=head2 find_homologs_with_genome_context_Output

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
report_name has a value which is a string
report_ref has a value which is a string

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
report_name has a value which is a string
report_ref has a value which is a string


=end text

=back



=head2 domain_source

=over 4



=item Description

COG, PF, TIGR, SEED


=item Definition

=begin html

<pre>
a string
</pre>

=end html

=begin text

a string

=end text

=back



=head2 category

=over 4



=item Description

Categories


=item Definition

=begin html

<pre>
a string
</pre>

=end html

=begin text

a string

=end text

=back



=head2 domainfamily

=over 4



=item Description

Domains


=item Definition

=begin html

<pre>
a string
</pre>

=end html

=begin text

a string

=end text

=back



=head2 Cat2Name

=over 4



=item Description

category to name


=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
namespace has a value which is a kb_phylogenomics.domain_source
cat has a value which is a kb_phylogenomics.category

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
namespace has a value which is a kb_phylogenomics.domain_source
cat has a value which is a kb_phylogenomics.category


=end text

=back



=head2 Cat2Group

=over 4



=item Description

category to group


=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
namespace has a value which is a kb_phylogenomics.domain_source
cat has a value which is a kb_phylogenomics.category

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
namespace has a value which is a kb_phylogenomics.domain_source
cat has a value which is a kb_phylogenomics.category


=end text

=back



=head2 DomFam2Cat

=over 4



=item Description

domain family to category


=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
namespace has a value which is a kb_phylogenomics.domain_source
domfam has a value which is a kb_phylogenomics.domainfamily

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
namespace has a value which is a kb_phylogenomics.domain_source
domfam has a value which is a kb_phylogenomics.domainfamily


=end text

=back



=head2 Cat2DomFams

=over 4



=item Description

category to domain family


=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
namespace has a value which is a kb_phylogenomics.domain_source
cat has a value which is a kb_phylogenomics.category

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
namespace has a value which is a kb_phylogenomics.domain_source
cat has a value which is a kb_phylogenomics.category


=end text

=back



=head2 get_configure_categories_Input

=over 4



=item Description

get_configure_categories()
**
** configure the domain categorie names and descriptions


=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
params has a value which is a kb_phylogenomics.view_fxn_profile_Input

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
params has a value which is a kb_phylogenomics.view_fxn_profile_Input


=end text

=back



=head2 get_configure_categories_Output

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
cats has a value which is a reference to a list where each element is a string
cat2name has a value which is a kb_phylogenomics.Cat2Name
cat2group has a value which is a kb_phylogenomics.Cat2Group
domfam2cat has a value which is a kb_phylogenomics.DomFam2Cat
cat2domfams has a value which is a kb_phylogenomics.Cat2DomFams

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
cats has a value which is a reference to a list where each element is a string
cat2name has a value which is a kb_phylogenomics.Cat2Name
cat2group has a value which is a kb_phylogenomics.Cat2Group
domfam2cat has a value which is a kb_phylogenomics.DomFam2Cat
cat2domfams has a value which is a kb_phylogenomics.Cat2DomFams


=end text

=back



=cut

package kb_phylogenomics::kb_phylogenomicsClient::RpcClient;
use base 'JSON::RPC::Client';
use POSIX;
use strict;

#
# Override JSON::RPC::Client::call because it doesn't handle error returns properly.
#

sub call {
    my ($self, $uri, $headers, $obj) = @_;
    my $result;


    {
	if ($uri =~ /\?/) {
	    $result = $self->_get($uri);
	}
	else {
	    Carp::croak "not hashref." unless (ref $obj eq 'HASH');
	    $result = $self->_post($uri, $headers, $obj);
	}

    }

    my $service = $obj->{method} =~ /^system\./ if ( $obj );

    $self->status_line($result->status_line);

    if ($result->is_success) {

        return unless($result->content); # notification?

        if ($service) {
            return JSON::RPC::ServiceObject->new($result, $self->json);
        }

        return JSON::RPC::ReturnObject->new($result, $self->json);
    }
    elsif ($result->content_type eq 'application/json')
    {
        return JSON::RPC::ReturnObject->new($result, $self->json);
    }
    else {
        return;
    }
}


sub _post {
    my ($self, $uri, $headers, $obj) = @_;
    my $json = $self->json;

    $obj->{version} ||= $self->{version} || '1.1';

    if ($obj->{version} eq '1.0') {
        delete $obj->{version};
        if (exists $obj->{id}) {
            $self->id($obj->{id}) if ($obj->{id}); # if undef, it is notification.
        }
        else {
            $obj->{id} = $self->id || ($self->id('JSON::RPC::Client'));
        }
    }
    else {
        # $obj->{id} = $self->id if (defined $self->id);
	# Assign a random number to the id if one hasn't been set
	$obj->{id} = (defined $self->id) ? $self->id : substr(rand(),2);
    }

    my $content = $json->encode($obj);

    $self->ua->post(
        $uri,
        Content_Type   => $self->{content_type},
        Content        => $content,
        Accept         => 'application/json',
	@$headers,
	($self->{token} ? (Authorization => $self->{token}) : ()),
    );
}



1;
