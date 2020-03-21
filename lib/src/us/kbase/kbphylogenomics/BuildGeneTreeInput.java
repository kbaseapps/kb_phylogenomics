
package us.kbase.kbphylogenomics;

import java.util.HashMap;
import java.util.Map;
import javax.annotation.Generated;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;


/**
 * <p>Original spec-file type: build_gene_tree_Input</p>
 * <pre>
 * build_gene_tree()
 * **
 * ** build a gene tree for a featureset
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "workspace_name",
    "desc",
    "input_featureSet_ref",
    "output_tree_name",
    "genome_disp_name_config",
    "skip_trimming",
    "muscle_maxiters",
    "muscle_maxhours",
    "gblocks_trim_level",
    "gblocks_min_seqs_for_conserved",
    "gblocks_min_seqs_for_flank",
    "gblocks_max_pos_contig_nonconserved",
    "gblocks_min_block_len",
    "gblocks_remove_mask_positions_flag",
    "fasttree_fastest",
    "fasttree_pseudo",
    "fasttree_gtr",
    "fasttree_wag",
    "fasttree_noml",
    "fasttree_nome",
    "fasttree_cat",
    "fasttree_nocat",
    "fasttree_gamma"
})
public class BuildGeneTreeInput {

    @JsonProperty("workspace_name")
    private String workspaceName;
    @JsonProperty("desc")
    private String desc;
    @JsonProperty("input_featureSet_ref")
    private String inputFeatureSetRef;
    @JsonProperty("output_tree_name")
    private String outputTreeName;
    @JsonProperty("genome_disp_name_config")
    private String genomeDispNameConfig;
    @JsonProperty("skip_trimming")
    private Long skipTrimming;
    @JsonProperty("muscle_maxiters")
    private Long muscleMaxiters;
    @JsonProperty("muscle_maxhours")
    private Double muscleMaxhours;
    @JsonProperty("gblocks_trim_level")
    private Long gblocksTrimLevel;
    @JsonProperty("gblocks_min_seqs_for_conserved")
    private Long gblocksMinSeqsForConserved;
    @JsonProperty("gblocks_min_seqs_for_flank")
    private Long gblocksMinSeqsForFlank;
    @JsonProperty("gblocks_max_pos_contig_nonconserved")
    private Long gblocksMaxPosContigNonconserved;
    @JsonProperty("gblocks_min_block_len")
    private Long gblocksMinBlockLen;
    @JsonProperty("gblocks_remove_mask_positions_flag")
    private Long gblocksRemoveMaskPositionsFlag;
    @JsonProperty("fasttree_fastest")
    private Long fasttreeFastest;
    @JsonProperty("fasttree_pseudo")
    private Long fasttreePseudo;
    @JsonProperty("fasttree_gtr")
    private Long fasttreeGtr;
    @JsonProperty("fasttree_wag")
    private Long fasttreeWag;
    @JsonProperty("fasttree_noml")
    private Long fasttreeNoml;
    @JsonProperty("fasttree_nome")
    private Long fasttreeNome;
    @JsonProperty("fasttree_cat")
    private Long fasttreeCat;
    @JsonProperty("fasttree_nocat")
    private Long fasttreeNocat;
    @JsonProperty("fasttree_gamma")
    private Long fasttreeGamma;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("workspace_name")
    public String getWorkspaceName() {
        return workspaceName;
    }

    @JsonProperty("workspace_name")
    public void setWorkspaceName(String workspaceName) {
        this.workspaceName = workspaceName;
    }

    public BuildGeneTreeInput withWorkspaceName(String workspaceName) {
        this.workspaceName = workspaceName;
        return this;
    }

    @JsonProperty("desc")
    public String getDesc() {
        return desc;
    }

    @JsonProperty("desc")
    public void setDesc(String desc) {
        this.desc = desc;
    }

    public BuildGeneTreeInput withDesc(String desc) {
        this.desc = desc;
        return this;
    }

    @JsonProperty("input_featureSet_ref")
    public String getInputFeatureSetRef() {
        return inputFeatureSetRef;
    }

    @JsonProperty("input_featureSet_ref")
    public void setInputFeatureSetRef(String inputFeatureSetRef) {
        this.inputFeatureSetRef = inputFeatureSetRef;
    }

    public BuildGeneTreeInput withInputFeatureSetRef(String inputFeatureSetRef) {
        this.inputFeatureSetRef = inputFeatureSetRef;
        return this;
    }

    @JsonProperty("output_tree_name")
    public String getOutputTreeName() {
        return outputTreeName;
    }

    @JsonProperty("output_tree_name")
    public void setOutputTreeName(String outputTreeName) {
        this.outputTreeName = outputTreeName;
    }

    public BuildGeneTreeInput withOutputTreeName(String outputTreeName) {
        this.outputTreeName = outputTreeName;
        return this;
    }

    @JsonProperty("genome_disp_name_config")
    public String getGenomeDispNameConfig() {
        return genomeDispNameConfig;
    }

    @JsonProperty("genome_disp_name_config")
    public void setGenomeDispNameConfig(String genomeDispNameConfig) {
        this.genomeDispNameConfig = genomeDispNameConfig;
    }

    public BuildGeneTreeInput withGenomeDispNameConfig(String genomeDispNameConfig) {
        this.genomeDispNameConfig = genomeDispNameConfig;
        return this;
    }

    @JsonProperty("skip_trimming")
    public Long getSkipTrimming() {
        return skipTrimming;
    }

    @JsonProperty("skip_trimming")
    public void setSkipTrimming(Long skipTrimming) {
        this.skipTrimming = skipTrimming;
    }

    public BuildGeneTreeInput withSkipTrimming(Long skipTrimming) {
        this.skipTrimming = skipTrimming;
        return this;
    }

    @JsonProperty("muscle_maxiters")
    public Long getMuscleMaxiters() {
        return muscleMaxiters;
    }

    @JsonProperty("muscle_maxiters")
    public void setMuscleMaxiters(Long muscleMaxiters) {
        this.muscleMaxiters = muscleMaxiters;
    }

    public BuildGeneTreeInput withMuscleMaxiters(Long muscleMaxiters) {
        this.muscleMaxiters = muscleMaxiters;
        return this;
    }

    @JsonProperty("muscle_maxhours")
    public Double getMuscleMaxhours() {
        return muscleMaxhours;
    }

    @JsonProperty("muscle_maxhours")
    public void setMuscleMaxhours(Double muscleMaxhours) {
        this.muscleMaxhours = muscleMaxhours;
    }

    public BuildGeneTreeInput withMuscleMaxhours(Double muscleMaxhours) {
        this.muscleMaxhours = muscleMaxhours;
        return this;
    }

    @JsonProperty("gblocks_trim_level")
    public Long getGblocksTrimLevel() {
        return gblocksTrimLevel;
    }

    @JsonProperty("gblocks_trim_level")
    public void setGblocksTrimLevel(Long gblocksTrimLevel) {
        this.gblocksTrimLevel = gblocksTrimLevel;
    }

    public BuildGeneTreeInput withGblocksTrimLevel(Long gblocksTrimLevel) {
        this.gblocksTrimLevel = gblocksTrimLevel;
        return this;
    }

    @JsonProperty("gblocks_min_seqs_for_conserved")
    public Long getGblocksMinSeqsForConserved() {
        return gblocksMinSeqsForConserved;
    }

    @JsonProperty("gblocks_min_seqs_for_conserved")
    public void setGblocksMinSeqsForConserved(Long gblocksMinSeqsForConserved) {
        this.gblocksMinSeqsForConserved = gblocksMinSeqsForConserved;
    }

    public BuildGeneTreeInput withGblocksMinSeqsForConserved(Long gblocksMinSeqsForConserved) {
        this.gblocksMinSeqsForConserved = gblocksMinSeqsForConserved;
        return this;
    }

    @JsonProperty("gblocks_min_seqs_for_flank")
    public Long getGblocksMinSeqsForFlank() {
        return gblocksMinSeqsForFlank;
    }

    @JsonProperty("gblocks_min_seqs_for_flank")
    public void setGblocksMinSeqsForFlank(Long gblocksMinSeqsForFlank) {
        this.gblocksMinSeqsForFlank = gblocksMinSeqsForFlank;
    }

    public BuildGeneTreeInput withGblocksMinSeqsForFlank(Long gblocksMinSeqsForFlank) {
        this.gblocksMinSeqsForFlank = gblocksMinSeqsForFlank;
        return this;
    }

    @JsonProperty("gblocks_max_pos_contig_nonconserved")
    public Long getGblocksMaxPosContigNonconserved() {
        return gblocksMaxPosContigNonconserved;
    }

    @JsonProperty("gblocks_max_pos_contig_nonconserved")
    public void setGblocksMaxPosContigNonconserved(Long gblocksMaxPosContigNonconserved) {
        this.gblocksMaxPosContigNonconserved = gblocksMaxPosContigNonconserved;
    }

    public BuildGeneTreeInput withGblocksMaxPosContigNonconserved(Long gblocksMaxPosContigNonconserved) {
        this.gblocksMaxPosContigNonconserved = gblocksMaxPosContigNonconserved;
        return this;
    }

    @JsonProperty("gblocks_min_block_len")
    public Long getGblocksMinBlockLen() {
        return gblocksMinBlockLen;
    }

    @JsonProperty("gblocks_min_block_len")
    public void setGblocksMinBlockLen(Long gblocksMinBlockLen) {
        this.gblocksMinBlockLen = gblocksMinBlockLen;
    }

    public BuildGeneTreeInput withGblocksMinBlockLen(Long gblocksMinBlockLen) {
        this.gblocksMinBlockLen = gblocksMinBlockLen;
        return this;
    }

    @JsonProperty("gblocks_remove_mask_positions_flag")
    public Long getGblocksRemoveMaskPositionsFlag() {
        return gblocksRemoveMaskPositionsFlag;
    }

    @JsonProperty("gblocks_remove_mask_positions_flag")
    public void setGblocksRemoveMaskPositionsFlag(Long gblocksRemoveMaskPositionsFlag) {
        this.gblocksRemoveMaskPositionsFlag = gblocksRemoveMaskPositionsFlag;
    }

    public BuildGeneTreeInput withGblocksRemoveMaskPositionsFlag(Long gblocksRemoveMaskPositionsFlag) {
        this.gblocksRemoveMaskPositionsFlag = gblocksRemoveMaskPositionsFlag;
        return this;
    }

    @JsonProperty("fasttree_fastest")
    public Long getFasttreeFastest() {
        return fasttreeFastest;
    }

    @JsonProperty("fasttree_fastest")
    public void setFasttreeFastest(Long fasttreeFastest) {
        this.fasttreeFastest = fasttreeFastest;
    }

    public BuildGeneTreeInput withFasttreeFastest(Long fasttreeFastest) {
        this.fasttreeFastest = fasttreeFastest;
        return this;
    }

    @JsonProperty("fasttree_pseudo")
    public Long getFasttreePseudo() {
        return fasttreePseudo;
    }

    @JsonProperty("fasttree_pseudo")
    public void setFasttreePseudo(Long fasttreePseudo) {
        this.fasttreePseudo = fasttreePseudo;
    }

    public BuildGeneTreeInput withFasttreePseudo(Long fasttreePseudo) {
        this.fasttreePseudo = fasttreePseudo;
        return this;
    }

    @JsonProperty("fasttree_gtr")
    public Long getFasttreeGtr() {
        return fasttreeGtr;
    }

    @JsonProperty("fasttree_gtr")
    public void setFasttreeGtr(Long fasttreeGtr) {
        this.fasttreeGtr = fasttreeGtr;
    }

    public BuildGeneTreeInput withFasttreeGtr(Long fasttreeGtr) {
        this.fasttreeGtr = fasttreeGtr;
        return this;
    }

    @JsonProperty("fasttree_wag")
    public Long getFasttreeWag() {
        return fasttreeWag;
    }

    @JsonProperty("fasttree_wag")
    public void setFasttreeWag(Long fasttreeWag) {
        this.fasttreeWag = fasttreeWag;
    }

    public BuildGeneTreeInput withFasttreeWag(Long fasttreeWag) {
        this.fasttreeWag = fasttreeWag;
        return this;
    }

    @JsonProperty("fasttree_noml")
    public Long getFasttreeNoml() {
        return fasttreeNoml;
    }

    @JsonProperty("fasttree_noml")
    public void setFasttreeNoml(Long fasttreeNoml) {
        this.fasttreeNoml = fasttreeNoml;
    }

    public BuildGeneTreeInput withFasttreeNoml(Long fasttreeNoml) {
        this.fasttreeNoml = fasttreeNoml;
        return this;
    }

    @JsonProperty("fasttree_nome")
    public Long getFasttreeNome() {
        return fasttreeNome;
    }

    @JsonProperty("fasttree_nome")
    public void setFasttreeNome(Long fasttreeNome) {
        this.fasttreeNome = fasttreeNome;
    }

    public BuildGeneTreeInput withFasttreeNome(Long fasttreeNome) {
        this.fasttreeNome = fasttreeNome;
        return this;
    }

    @JsonProperty("fasttree_cat")
    public Long getFasttreeCat() {
        return fasttreeCat;
    }

    @JsonProperty("fasttree_cat")
    public void setFasttreeCat(Long fasttreeCat) {
        this.fasttreeCat = fasttreeCat;
    }

    public BuildGeneTreeInput withFasttreeCat(Long fasttreeCat) {
        this.fasttreeCat = fasttreeCat;
        return this;
    }

    @JsonProperty("fasttree_nocat")
    public Long getFasttreeNocat() {
        return fasttreeNocat;
    }

    @JsonProperty("fasttree_nocat")
    public void setFasttreeNocat(Long fasttreeNocat) {
        this.fasttreeNocat = fasttreeNocat;
    }

    public BuildGeneTreeInput withFasttreeNocat(Long fasttreeNocat) {
        this.fasttreeNocat = fasttreeNocat;
        return this;
    }

    @JsonProperty("fasttree_gamma")
    public Long getFasttreeGamma() {
        return fasttreeGamma;
    }

    @JsonProperty("fasttree_gamma")
    public void setFasttreeGamma(Long fasttreeGamma) {
        this.fasttreeGamma = fasttreeGamma;
    }

    public BuildGeneTreeInput withFasttreeGamma(Long fasttreeGamma) {
        this.fasttreeGamma = fasttreeGamma;
        return this;
    }

    @JsonAnyGetter
    public Map<String, Object> getAdditionalProperties() {
        return this.additionalProperties;
    }

    @JsonAnySetter
    public void setAdditionalProperties(String name, Object value) {
        this.additionalProperties.put(name, value);
    }

    @Override
    public String toString() {
        return ((((((((((((((((((((((((((((((((((((((((((((((((("BuildGeneTreeInput"+" [workspaceName=")+ workspaceName)+", desc=")+ desc)+", inputFeatureSetRef=")+ inputFeatureSetRef)+", outputTreeName=")+ outputTreeName)+", genomeDispNameConfig=")+ genomeDispNameConfig)+", skipTrimming=")+ skipTrimming)+", muscleMaxiters=")+ muscleMaxiters)+", muscleMaxhours=")+ muscleMaxhours)+", gblocksTrimLevel=")+ gblocksTrimLevel)+", gblocksMinSeqsForConserved=")+ gblocksMinSeqsForConserved)+", gblocksMinSeqsForFlank=")+ gblocksMinSeqsForFlank)+", gblocksMaxPosContigNonconserved=")+ gblocksMaxPosContigNonconserved)+", gblocksMinBlockLen=")+ gblocksMinBlockLen)+", gblocksRemoveMaskPositionsFlag=")+ gblocksRemoveMaskPositionsFlag)+", fasttreeFastest=")+ fasttreeFastest)+", fasttreePseudo=")+ fasttreePseudo)+", fasttreeGtr=")+ fasttreeGtr)+", fasttreeWag=")+ fasttreeWag)+", fasttreeNoml=")+ fasttreeNoml)+", fasttreeNome=")+ fasttreeNome)+", fasttreeCat=")+ fasttreeCat)+", fasttreeNocat=")+ fasttreeNocat)+", fasttreeGamma=")+ fasttreeGamma)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
