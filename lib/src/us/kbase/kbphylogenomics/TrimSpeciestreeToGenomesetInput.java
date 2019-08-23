
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
 * <p>Original spec-file type: trim_speciestree_to_genomeset_Input</p>
 * <pre>
 * trim_speciestree_to_genomeset()
 * **
 * ** reduce tree to match genomes found in genomeset
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "workspace_name",
    "input_genomeSet_ref",
    "input_tree_ref",
    "output_tree_name",
    "desc",
    "enforce_genome_version_match"
})
public class TrimSpeciestreeToGenomesetInput {

    @JsonProperty("workspace_name")
    private String workspaceName;
    @JsonProperty("input_genomeSet_ref")
    private String inputGenomeSetRef;
    @JsonProperty("input_tree_ref")
    private String inputTreeRef;
    @JsonProperty("output_tree_name")
    private String outputTreeName;
    @JsonProperty("desc")
    private String desc;
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

    public TrimSpeciestreeToGenomesetInput withWorkspaceName(String workspaceName) {
        this.workspaceName = workspaceName;
        return this;
    }

    @JsonProperty("input_genomeSet_ref")
    public String getInputGenomeSetRef() {
        return inputGenomeSetRef;
    }

    @JsonProperty("input_genomeSet_ref")
    public void setInputGenomeSetRef(String inputGenomeSetRef) {
        this.inputGenomeSetRef = inputGenomeSetRef;
    }

    public TrimSpeciestreeToGenomesetInput withInputGenomeSetRef(String inputGenomeSetRef) {
        this.inputGenomeSetRef = inputGenomeSetRef;
        return this;
    }

    @JsonProperty("input_tree_ref")
    public String getInputTreeRef() {
        return inputTreeRef;
    }

    @JsonProperty("input_tree_ref")
    public void setInputTreeRef(String inputTreeRef) {
        this.inputTreeRef = inputTreeRef;
    }

    public TrimSpeciestreeToGenomesetInput withInputTreeRef(String inputTreeRef) {
        this.inputTreeRef = inputTreeRef;
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

    public TrimSpeciestreeToGenomesetInput withOutputTreeName(String outputTreeName) {
        this.outputTreeName = outputTreeName;
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

    public TrimSpeciestreeToGenomesetInput withDesc(String desc) {
        this.desc = desc;
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

    public TrimSpeciestreeToGenomesetInput withEnforceGenomeVersionMatch(Long enforceGenomeVersionMatch) {
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
        return ((((((((((((((("TrimSpeciestreeToGenomesetInput"+" [workspaceName=")+ workspaceName)+", inputGenomeSetRef=")+ inputGenomeSetRef)+", inputTreeRef=")+ inputTreeRef)+", outputTreeName=")+ outputTreeName)+", desc=")+ desc)+", enforceGenomeVersionMatch=")+ enforceGenomeVersionMatch)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
