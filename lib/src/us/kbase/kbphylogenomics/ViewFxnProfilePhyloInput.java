
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
    "target_fams",
    "heatmap"
})
public class ViewFxnProfilePhyloInput {

    @JsonProperty("workspace_name")
    private java.lang.String workspaceName;
    @JsonProperty("input_speciesTree_ref")
    private java.lang.String inputSpeciesTreeRef;
    @JsonProperty("target_fams")
    private List<String> targetFams;
    @JsonProperty("heatmap")
    private Long heatmap;
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
        return ((((((((((("ViewFxnProfilePhyloInput"+" [workspaceName=")+ workspaceName)+", inputSpeciesTreeRef=")+ inputSpeciesTreeRef)+", targetFams=")+ targetFams)+", heatmap=")+ heatmap)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
