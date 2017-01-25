
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
    "top_level_namespace",
    "target_fams",
    "count_category",
    "heatmap",
    "vertical"
})
public class ViewFxnProfileInput {

    @JsonProperty("workspace_name")
    private java.lang.String workspaceName;
    @JsonProperty("input_genomeSet_ref")
    private java.lang.String inputGenomeSetRef;
    @JsonProperty("top_level_namespace")
    private java.lang.String topLevelNamespace;
    @JsonProperty("target_fams")
    private List<String> targetFams;
    @JsonProperty("count_category")
    private java.lang.String countCategory;
    @JsonProperty("heatmap")
    private Long heatmap;
    @JsonProperty("vertical")
    private Long vertical;
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

    @JsonProperty("top_level_namespace")
    public java.lang.String getTopLevelNamespace() {
        return topLevelNamespace;
    }

    @JsonProperty("top_level_namespace")
    public void setTopLevelNamespace(java.lang.String topLevelNamespace) {
        this.topLevelNamespace = topLevelNamespace;
    }

    public ViewFxnProfileInput withTopLevelNamespace(java.lang.String topLevelNamespace) {
        this.topLevelNamespace = topLevelNamespace;
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
        return ((((((((((((((((("ViewFxnProfileInput"+" [workspaceName=")+ workspaceName)+", inputGenomeSetRef=")+ inputGenomeSetRef)+", topLevelNamespace=")+ topLevelNamespace)+", targetFams=")+ targetFams)+", countCategory=")+ countCategory)+", heatmap=")+ heatmap)+", vertical=")+ vertical)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
