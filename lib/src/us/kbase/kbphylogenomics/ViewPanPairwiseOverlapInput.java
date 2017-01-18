
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
 * <p>Original spec-file type: view_pan_pairwise_overlap_Input</p>
 * <pre>
 * view_pan_pairwise_overlap()
 * **
 * ** build a multi-member pangenome pairwise overlap plot
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "workspace_name",
    "input_genome_ref",
    "input_pangenome_ref"
})
public class ViewPanPairwiseOverlapInput {

    @JsonProperty("workspace_name")
    private String workspaceName;
    @JsonProperty("input_genome_ref")
    private String inputGenomeRef;
    @JsonProperty("input_pangenome_ref")
    private String inputPangenomeRef;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("workspace_name")
    public String getWorkspaceName() {
        return workspaceName;
    }

    @JsonProperty("workspace_name")
    public void setWorkspaceName(String workspaceName) {
        this.workspaceName = workspaceName;
    }

    public ViewPanPairwiseOverlapInput withWorkspaceName(String workspaceName) {
        this.workspaceName = workspaceName;
        return this;
    }

    @JsonProperty("input_genome_ref")
    public String getInputGenomeRef() {
        return inputGenomeRef;
    }

    @JsonProperty("input_genome_ref")
    public void setInputGenomeRef(String inputGenomeRef) {
        this.inputGenomeRef = inputGenomeRef;
    }

    public ViewPanPairwiseOverlapInput withInputGenomeRef(String inputGenomeRef) {
        this.inputGenomeRef = inputGenomeRef;
        return this;
    }

    @JsonProperty("input_pangenome_ref")
    public String getInputPangenomeRef() {
        return inputPangenomeRef;
    }

    @JsonProperty("input_pangenome_ref")
    public void setInputPangenomeRef(String inputPangenomeRef) {
        this.inputPangenomeRef = inputPangenomeRef;
    }

    public ViewPanPairwiseOverlapInput withInputPangenomeRef(String inputPangenomeRef) {
        this.inputPangenomeRef = inputPangenomeRef;
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
        return ((((((((("ViewPanPairwiseOverlapInput"+" [workspaceName=")+ workspaceName)+", inputGenomeRef=")+ inputGenomeRef)+", inputPangenomeRef=")+ inputPangenomeRef)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
