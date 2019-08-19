
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
 * <p>Original spec-file type: view_fxn_profile_phylo_Input</p>
 * <pre>
 * view_fxn_profile_phylo()
 * **
 * ** show a table/heatmap of general categories or custom gene families for a set of Genomes using the species tree
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "workspace_name",
    "input_speciesTree_ref",
    "namespace",
    "custom_target_fams",
    "count_category",
    "heatmap",
    "vertical",
    "top_hit",
    "e_value",
    "log_base",
    "required_COG_annot_perc",
    "required_PFAM_annot_perc",
    "required_TIGR_annot_perc",
    "required_SEED_annot_perc",
    "count_hypothetical",
    "show_blanks",
    "display_genome_object_name",
    "skip_missing_genomes",
    "enforce_genome_version_match"
})
public class ViewFxnProfilePhyloInput {

    @JsonProperty("workspace_name")
    private String workspaceName;
    @JsonProperty("input_speciesTree_ref")
    private String inputSpeciesTreeRef;
    @JsonProperty("namespace")
    private String namespace;
    /**
     * <p>Original spec-file type: CustomTargetFams</p>
     * <pre>
     * parameter groups
     * </pre>
     * 
     */
    @JsonProperty("custom_target_fams")
    private CustomTargetFams customTargetFams;
    @JsonProperty("count_category")
    private String countCategory;
    @JsonProperty("heatmap")
    private Long heatmap;
    @JsonProperty("vertical")
    private Long vertical;
    @JsonProperty("top_hit")
    private Long topHit;
    @JsonProperty("e_value")
    private Double eValue;
    @JsonProperty("log_base")
    private Double logBase;
    @JsonProperty("required_COG_annot_perc")
    private Double requiredCOGAnnotPerc;
    @JsonProperty("required_PFAM_annot_perc")
    private Double requiredPFAMAnnotPerc;
    @JsonProperty("required_TIGR_annot_perc")
    private Double requiredTIGRAnnotPerc;
    @JsonProperty("required_SEED_annot_perc")
    private Double requiredSEEDAnnotPerc;
    @JsonProperty("count_hypothetical")
    private Long countHypothetical;
    @JsonProperty("show_blanks")
    private Long showBlanks;
    @JsonProperty("display_genome_object_name")
    private Long displayGenomeObjectName;
    @JsonProperty("skip_missing_genomes")
    private Long skipMissingGenomes;
    @JsonProperty("enforce_genome_version_match")
    private Long enforceGenomeVersionMatch;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("workspace_name")
    public String getWorkspaceName() {
        return workspaceName;
    }

    @JsonProperty("workspace_name")
    public void setWorkspaceName(String workspaceName) {
        this.workspaceName = workspaceName;
    }

    public ViewFxnProfilePhyloInput withWorkspaceName(String workspaceName) {
        this.workspaceName = workspaceName;
        return this;
    }

    @JsonProperty("input_speciesTree_ref")
    public String getInputSpeciesTreeRef() {
        return inputSpeciesTreeRef;
    }

    @JsonProperty("input_speciesTree_ref")
    public void setInputSpeciesTreeRef(String inputSpeciesTreeRef) {
        this.inputSpeciesTreeRef = inputSpeciesTreeRef;
    }

    public ViewFxnProfilePhyloInput withInputSpeciesTreeRef(String inputSpeciesTreeRef) {
        this.inputSpeciesTreeRef = inputSpeciesTreeRef;
        return this;
    }

    @JsonProperty("namespace")
    public String getNamespace() {
        return namespace;
    }

    @JsonProperty("namespace")
    public void setNamespace(String namespace) {
        this.namespace = namespace;
    }

    public ViewFxnProfilePhyloInput withNamespace(String namespace) {
        this.namespace = namespace;
        return this;
    }

    /**
     * <p>Original spec-file type: CustomTargetFams</p>
     * <pre>
     * parameter groups
     * </pre>
     * 
     */
    @JsonProperty("custom_target_fams")
    public CustomTargetFams getCustomTargetFams() {
        return customTargetFams;
    }

    /**
     * <p>Original spec-file type: CustomTargetFams</p>
     * <pre>
     * parameter groups
     * </pre>
     * 
     */
    @JsonProperty("custom_target_fams")
    public void setCustomTargetFams(CustomTargetFams customTargetFams) {
        this.customTargetFams = customTargetFams;
    }

    public ViewFxnProfilePhyloInput withCustomTargetFams(CustomTargetFams customTargetFams) {
        this.customTargetFams = customTargetFams;
        return this;
    }

    @JsonProperty("count_category")
    public String getCountCategory() {
        return countCategory;
    }

    @JsonProperty("count_category")
    public void setCountCategory(String countCategory) {
        this.countCategory = countCategory;
    }

    public ViewFxnProfilePhyloInput withCountCategory(String countCategory) {
        this.countCategory = countCategory;
        return this;
    }

    @JsonProperty("heatmap")
    public Long getHeatmap() {
        return heatmap;
    }

    @JsonProperty("heatmap")
    public void setHeatmap(Long heatmap) {
        this.heatmap = heatmap;
    }

    public ViewFxnProfilePhyloInput withHeatmap(Long heatmap) {
        this.heatmap = heatmap;
        return this;
    }

    @JsonProperty("vertical")
    public Long getVertical() {
        return vertical;
    }

    @JsonProperty("vertical")
    public void setVertical(Long vertical) {
        this.vertical = vertical;
    }

    public ViewFxnProfilePhyloInput withVertical(Long vertical) {
        this.vertical = vertical;
        return this;
    }

    @JsonProperty("top_hit")
    public Long getTopHit() {
        return topHit;
    }

    @JsonProperty("top_hit")
    public void setTopHit(Long topHit) {
        this.topHit = topHit;
    }

    public ViewFxnProfilePhyloInput withTopHit(Long topHit) {
        this.topHit = topHit;
        return this;
    }

    @JsonProperty("e_value")
    public Double getEValue() {
        return eValue;
    }

    @JsonProperty("e_value")
    public void setEValue(Double eValue) {
        this.eValue = eValue;
    }

    public ViewFxnProfilePhyloInput withEValue(Double eValue) {
        this.eValue = eValue;
        return this;
    }

    @JsonProperty("log_base")
    public Double getLogBase() {
        return logBase;
    }

    @JsonProperty("log_base")
    public void setLogBase(Double logBase) {
        this.logBase = logBase;
    }

    public ViewFxnProfilePhyloInput withLogBase(Double logBase) {
        this.logBase = logBase;
        return this;
    }

    @JsonProperty("required_COG_annot_perc")
    public Double getRequiredCOGAnnotPerc() {
        return requiredCOGAnnotPerc;
    }

    @JsonProperty("required_COG_annot_perc")
    public void setRequiredCOGAnnotPerc(Double requiredCOGAnnotPerc) {
        this.requiredCOGAnnotPerc = requiredCOGAnnotPerc;
    }

    public ViewFxnProfilePhyloInput withRequiredCOGAnnotPerc(Double requiredCOGAnnotPerc) {
        this.requiredCOGAnnotPerc = requiredCOGAnnotPerc;
        return this;
    }

    @JsonProperty("required_PFAM_annot_perc")
    public Double getRequiredPFAMAnnotPerc() {
        return requiredPFAMAnnotPerc;
    }

    @JsonProperty("required_PFAM_annot_perc")
    public void setRequiredPFAMAnnotPerc(Double requiredPFAMAnnotPerc) {
        this.requiredPFAMAnnotPerc = requiredPFAMAnnotPerc;
    }

    public ViewFxnProfilePhyloInput withRequiredPFAMAnnotPerc(Double requiredPFAMAnnotPerc) {
        this.requiredPFAMAnnotPerc = requiredPFAMAnnotPerc;
        return this;
    }

    @JsonProperty("required_TIGR_annot_perc")
    public Double getRequiredTIGRAnnotPerc() {
        return requiredTIGRAnnotPerc;
    }

    @JsonProperty("required_TIGR_annot_perc")
    public void setRequiredTIGRAnnotPerc(Double requiredTIGRAnnotPerc) {
        this.requiredTIGRAnnotPerc = requiredTIGRAnnotPerc;
    }

    public ViewFxnProfilePhyloInput withRequiredTIGRAnnotPerc(Double requiredTIGRAnnotPerc) {
        this.requiredTIGRAnnotPerc = requiredTIGRAnnotPerc;
        return this;
    }

    @JsonProperty("required_SEED_annot_perc")
    public Double getRequiredSEEDAnnotPerc() {
        return requiredSEEDAnnotPerc;
    }

    @JsonProperty("required_SEED_annot_perc")
    public void setRequiredSEEDAnnotPerc(Double requiredSEEDAnnotPerc) {
        this.requiredSEEDAnnotPerc = requiredSEEDAnnotPerc;
    }

    public ViewFxnProfilePhyloInput withRequiredSEEDAnnotPerc(Double requiredSEEDAnnotPerc) {
        this.requiredSEEDAnnotPerc = requiredSEEDAnnotPerc;
        return this;
    }

    @JsonProperty("count_hypothetical")
    public Long getCountHypothetical() {
        return countHypothetical;
    }

    @JsonProperty("count_hypothetical")
    public void setCountHypothetical(Long countHypothetical) {
        this.countHypothetical = countHypothetical;
    }

    public ViewFxnProfilePhyloInput withCountHypothetical(Long countHypothetical) {
        this.countHypothetical = countHypothetical;
        return this;
    }

    @JsonProperty("show_blanks")
    public Long getShowBlanks() {
        return showBlanks;
    }

    @JsonProperty("show_blanks")
    public void setShowBlanks(Long showBlanks) {
        this.showBlanks = showBlanks;
    }

    public ViewFxnProfilePhyloInput withShowBlanks(Long showBlanks) {
        this.showBlanks = showBlanks;
        return this;
    }

    @JsonProperty("display_genome_object_name")
    public Long getDisplayGenomeObjectName() {
        return displayGenomeObjectName;
    }

    @JsonProperty("display_genome_object_name")
    public void setDisplayGenomeObjectName(Long displayGenomeObjectName) {
        this.displayGenomeObjectName = displayGenomeObjectName;
    }

    public ViewFxnProfilePhyloInput withDisplayGenomeObjectName(Long displayGenomeObjectName) {
        this.displayGenomeObjectName = displayGenomeObjectName;
        return this;
    }

    @JsonProperty("skip_missing_genomes")
    public Long getSkipMissingGenomes() {
        return skipMissingGenomes;
    }

    @JsonProperty("skip_missing_genomes")
    public void setSkipMissingGenomes(Long skipMissingGenomes) {
        this.skipMissingGenomes = skipMissingGenomes;
    }

    public ViewFxnProfilePhyloInput withSkipMissingGenomes(Long skipMissingGenomes) {
        this.skipMissingGenomes = skipMissingGenomes;
        return this;
    }

    @JsonProperty("enforce_genome_version_match")
    public Long getEnforceGenomeVersionMatch() {
        return enforceGenomeVersionMatch;
    }

    @JsonProperty("enforce_genome_version_match")
    public void setEnforceGenomeVersionMatch(Long enforceGenomeVersionMatch) {
        this.enforceGenomeVersionMatch = enforceGenomeVersionMatch;
    }

    public ViewFxnProfilePhyloInput withEnforceGenomeVersionMatch(Long enforceGenomeVersionMatch) {
        this.enforceGenomeVersionMatch = enforceGenomeVersionMatch;
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
        return ((((((((((((((((((((((((((((((((((((((((("ViewFxnProfilePhyloInput"+" [workspaceName=")+ workspaceName)+", inputSpeciesTreeRef=")+ inputSpeciesTreeRef)+", namespace=")+ namespace)+", customTargetFams=")+ customTargetFams)+", countCategory=")+ countCategory)+", heatmap=")+ heatmap)+", vertical=")+ vertical)+", topHit=")+ topHit)+", eValue=")+ eValue)+", logBase=")+ logBase)+", requiredCOGAnnotPerc=")+ requiredCOGAnnotPerc)+", requiredPFAMAnnotPerc=")+ requiredPFAMAnnotPerc)+", requiredTIGRAnnotPerc=")+ requiredTIGRAnnotPerc)+", requiredSEEDAnnotPerc=")+ requiredSEEDAnnotPerc)+", countHypothetical=")+ countHypothetical)+", showBlanks=")+ showBlanks)+", displayGenomeObjectName=")+ displayGenomeObjectName)+", skipMissingGenomes=")+ skipMissingGenomes)+", enforceGenomeVersionMatch=")+ enforceGenomeVersionMatch)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
