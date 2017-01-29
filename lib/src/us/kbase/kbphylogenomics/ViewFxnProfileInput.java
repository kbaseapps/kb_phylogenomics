
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
 * <p>Original spec-file type: view_fxn_profile_Input</p>
 * <pre>
 * view_fxn_profile()
 * **
 * ** show a table/heatmap of general categories or custom gene families for a set of Genomes
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "workspace_name",
    "input_genomeSet_ref",
    "namespace",
    "target_fams",
    "count_category",
    "heatmap",
    "vertical",
    "top_hit",
    "e_value",
    "show_blanks"
})
public class ViewFxnProfileInput {

    @JsonProperty("workspace_name")
    private java.lang.String workspaceName;
    @JsonProperty("input_genomeSet_ref")
    private java.lang.String inputGenomeSetRef;
    @JsonProperty("namespace")
    private java.lang.String namespace;
    @JsonProperty("target_fams")
    private List<String> targetFams;
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

    public ViewFxnProfileInput withWorkspaceName(java.lang.String workspaceName) {
        this.workspaceName = workspaceName;
        return this;
    }

    @JsonProperty("input_genomeSet_ref")
    public java.lang.String getInputGenomeSetRef() {
        return inputGenomeSetRef;
    }

    @JsonProperty("input_genomeSet_ref")
    public void setInputGenomeSetRef(java.lang.String inputGenomeSetRef) {
        this.inputGenomeSetRef = inputGenomeSetRef;
    }

    public ViewFxnProfileInput withInputGenomeSetRef(java.lang.String inputGenomeSetRef) {
        this.inputGenomeSetRef = inputGenomeSetRef;
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

    public ViewFxnProfileInput withNamespace(java.lang.String namespace) {
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

    public ViewFxnProfileInput withTargetFams(List<String> targetFams) {
        this.targetFams = targetFams;
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

    public ViewFxnProfileInput withCountCategory(java.lang.String countCategory) {
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

    public ViewFxnProfileInput withHeatmap(Long heatmap) {
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

    public ViewFxnProfileInput withVertical(Long vertical) {
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

    public ViewFxnProfileInput withTopHit(Long topHit) {
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

    public ViewFxnProfileInput withEValue(Double eValue) {
        this.eValue = eValue;
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

    public ViewFxnProfileInput withShowBlanks(Long showBlanks) {
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
        return ((((((((((((((((((((((("ViewFxnProfileInput"+" [workspaceName=")+ workspaceName)+", inputGenomeSetRef=")+ inputGenomeSetRef)+", namespace=")+ namespace)+", targetFams=")+ targetFams)+", countCategory=")+ countCategory)+", heatmap=")+ heatmap)+", vertical=")+ vertical)+", topHit=")+ topHit)+", eValue=")+ eValue)+", showBlanks=")+ showBlanks)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
