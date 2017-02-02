
package us.kbase.kbphylogenomics;

import java.util.HashMap;
import java.util.List;
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
    "target_fams",
    "extra_target_fam_groups_COG",
    "extra_target_fam_groups_PFAM",
    "extra_target_fam_groups_TIGR",
    "extra_target_fam_groups_SEED",
    "count_category",
    "heatmap",
    "vertical",
    "top_hit",
    "e_value",
    "log_base",
    "show_blanks"
})
public class ViewFxnProfilePhyloInput {

    @JsonProperty("workspace_name")
    private java.lang.String workspaceName;
    @JsonProperty("input_speciesTree_ref")
    private java.lang.String inputSpeciesTreeRef;
    @JsonProperty("namespace")
    private java.lang.String namespace;
    @JsonProperty("target_fams")
    private List<String> targetFams;
    @JsonProperty("extra_target_fam_groups_COG")
    private List<String> extraTargetFamGroupsCOG;
    @JsonProperty("extra_target_fam_groups_PFAM")
    private List<String> extraTargetFamGroupsPFAM;
    @JsonProperty("extra_target_fam_groups_TIGR")
    private List<String> extraTargetFamGroupsTIGR;
    @JsonProperty("extra_target_fam_groups_SEED")
    private List<String> extraTargetFamGroupsSEED;
    @JsonProperty("count_category")
    private java.lang.String countCategory;
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
    @JsonProperty("show_blanks")
    private Long showBlanks;
    private Map<java.lang.String, Object> additionalProperties = new HashMap<java.lang.String, Object>();

    @JsonProperty("workspace_name")
    public java.lang.String getWorkspaceName() {
        return workspaceName;
    }

    @JsonProperty("workspace_name")
    public void setWorkspaceName(java.lang.String workspaceName) {
        this.workspaceName = workspaceName;
    }

    public ViewFxnProfilePhyloInput withWorkspaceName(java.lang.String workspaceName) {
        this.workspaceName = workspaceName;
        return this;
    }

    @JsonProperty("input_speciesTree_ref")
    public java.lang.String getInputSpeciesTreeRef() {
        return inputSpeciesTreeRef;
    }

    @JsonProperty("input_speciesTree_ref")
    public void setInputSpeciesTreeRef(java.lang.String inputSpeciesTreeRef) {
        this.inputSpeciesTreeRef = inputSpeciesTreeRef;
    }

    public ViewFxnProfilePhyloInput withInputSpeciesTreeRef(java.lang.String inputSpeciesTreeRef) {
        this.inputSpeciesTreeRef = inputSpeciesTreeRef;
        return this;
    }

    @JsonProperty("namespace")
    public java.lang.String getNamespace() {
        return namespace;
    }

    @JsonProperty("namespace")
    public void setNamespace(java.lang.String namespace) {
        this.namespace = namespace;
    }

    public ViewFxnProfilePhyloInput withNamespace(java.lang.String namespace) {
        this.namespace = namespace;
        return this;
    }

    @JsonProperty("target_fams")
    public List<String> getTargetFams() {
        return targetFams;
    }

    @JsonProperty("target_fams")
    public void setTargetFams(List<String> targetFams) {
        this.targetFams = targetFams;
    }

    public ViewFxnProfilePhyloInput withTargetFams(List<String> targetFams) {
        this.targetFams = targetFams;
        return this;
    }

    @JsonProperty("extra_target_fam_groups_COG")
    public List<String> getExtraTargetFamGroupsCOG() {
        return extraTargetFamGroupsCOG;
    }

    @JsonProperty("extra_target_fam_groups_COG")
    public void setExtraTargetFamGroupsCOG(List<String> extraTargetFamGroupsCOG) {
        this.extraTargetFamGroupsCOG = extraTargetFamGroupsCOG;
    }

    public ViewFxnProfilePhyloInput withExtraTargetFamGroupsCOG(List<String> extraTargetFamGroupsCOG) {
        this.extraTargetFamGroupsCOG = extraTargetFamGroupsCOG;
        return this;
    }

    @JsonProperty("extra_target_fam_groups_PFAM")
    public List<String> getExtraTargetFamGroupsPFAM() {
        return extraTargetFamGroupsPFAM;
    }

    @JsonProperty("extra_target_fam_groups_PFAM")
    public void setExtraTargetFamGroupsPFAM(List<String> extraTargetFamGroupsPFAM) {
        this.extraTargetFamGroupsPFAM = extraTargetFamGroupsPFAM;
    }

    public ViewFxnProfilePhyloInput withExtraTargetFamGroupsPFAM(List<String> extraTargetFamGroupsPFAM) {
        this.extraTargetFamGroupsPFAM = extraTargetFamGroupsPFAM;
        return this;
    }

    @JsonProperty("extra_target_fam_groups_TIGR")
    public List<String> getExtraTargetFamGroupsTIGR() {
        return extraTargetFamGroupsTIGR;
    }

    @JsonProperty("extra_target_fam_groups_TIGR")
    public void setExtraTargetFamGroupsTIGR(List<String> extraTargetFamGroupsTIGR) {
        this.extraTargetFamGroupsTIGR = extraTargetFamGroupsTIGR;
    }

    public ViewFxnProfilePhyloInput withExtraTargetFamGroupsTIGR(List<String> extraTargetFamGroupsTIGR) {
        this.extraTargetFamGroupsTIGR = extraTargetFamGroupsTIGR;
        return this;
    }

    @JsonProperty("extra_target_fam_groups_SEED")
    public List<String> getExtraTargetFamGroupsSEED() {
        return extraTargetFamGroupsSEED;
    }

    @JsonProperty("extra_target_fam_groups_SEED")
    public void setExtraTargetFamGroupsSEED(List<String> extraTargetFamGroupsSEED) {
        this.extraTargetFamGroupsSEED = extraTargetFamGroupsSEED;
    }

    public ViewFxnProfilePhyloInput withExtraTargetFamGroupsSEED(List<String> extraTargetFamGroupsSEED) {
        this.extraTargetFamGroupsSEED = extraTargetFamGroupsSEED;
        return this;
    }

    @JsonProperty("count_category")
    public java.lang.String getCountCategory() {
        return countCategory;
    }

    @JsonProperty("count_category")
    public void setCountCategory(java.lang.String countCategory) {
        this.countCategory = countCategory;
    }

    public ViewFxnProfilePhyloInput withCountCategory(java.lang.String countCategory) {
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

    @JsonAnyGetter
    public Map<java.lang.String, Object> getAdditionalProperties() {
        return this.additionalProperties;
    }

    @JsonAnySetter
    public void setAdditionalProperties(java.lang.String name, Object value) {
        this.additionalProperties.put(name, value);
    }

    @Override
    public java.lang.String toString() {
        return ((((((((((((((((((((((((((((((((("ViewFxnProfilePhyloInput"+" [workspaceName=")+ workspaceName)+", inputSpeciesTreeRef=")+ inputSpeciesTreeRef)+", namespace=")+ namespace)+", targetFams=")+ targetFams)+", extraTargetFamGroupsCOG=")+ extraTargetFamGroupsCOG)+", extraTargetFamGroupsPFAM=")+ extraTargetFamGroupsPFAM)+", extraTargetFamGroupsTIGR=")+ extraTargetFamGroupsTIGR)+", extraTargetFamGroupsSEED=")+ extraTargetFamGroupsSEED)+", countCategory=")+ countCategory)+", heatmap=")+ heatmap)+", vertical=")+ vertical)+", topHit=")+ topHit)+", eValue=")+ eValue)+", logBase=")+ logBase)+", showBlanks=")+ showBlanks)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
