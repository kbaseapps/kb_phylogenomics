
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
 * <p>Original spec-file type: viz_pan_phylo_Input</p>
 * <pre>
 * viz_pan_phylo()
 * **
 * ** show the pangenome accumulation using a tree
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "workspace_name",
    "input_genome_ref",
    "input_pangenome_ref",
    "input_speciesTree_ref"
})
public class VizPanPhyloInput {

    @JsonProperty("workspace_name")
    private String workspaceName;
    @JsonProperty("input_genome_ref")
    private String inputGenomeRef;
    @JsonProperty("input_pangenome_ref")
    private String inputPangenomeRef;
    @JsonProperty("input_speciesTree_ref")
    private String inputSpeciesTreeRef;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("workspace_name")
    public String getWorkspaceName() {
        return workspaceName;
    }

    @JsonProperty("workspace_name")
    public void setWorkspaceName(String workspaceName) {
        this.workspaceName = workspaceName;
    }

    public VizPanPhyloInput withWorkspaceName(String workspaceName) {
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

    public VizPanPhyloInput withInputGenomeRef(String inputGenomeRef) {
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

    public VizPanPhyloInput withInputPangenomeRef(String inputPangenomeRef) {
        this.inputPangenomeRef = inputPangenomeRef;
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

    public VizPanPhyloInput withInputSpeciesTreeRef(String inputSpeciesTreeRef) {
        this.inputSpeciesTreeRef = inputSpeciesTreeRef;
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
        return ((((((((((("VizPanPhyloInput"+" [workspaceName=")+ workspaceName)+", inputGenomeRef=")+ inputGenomeRef)+", inputPangenomeRef=")+ inputPangenomeRef)+", inputSpeciesTreeRef=")+ inputSpeciesTreeRef)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
