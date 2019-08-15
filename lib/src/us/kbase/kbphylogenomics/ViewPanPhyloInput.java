
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
 * <p>Original spec-file type: view_pan_phylo_Input</p>
 * <pre>
 * view_pan_phylo()
 * **
 * ** show the pangenome accumulation using a tree
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "workspace_name",
    "input_pangenome_ref",
    "input_speciesTree_ref",
    "save_featuresets",
    "skip_missing_genomes",
    "enforce_genome_version_match"
})
public class ViewPanPhyloInput {

    @JsonProperty("workspace_name")
    private String workspaceName;
    @JsonProperty("input_pangenome_ref")
    private String inputPangenomeRef;
    @JsonProperty("input_speciesTree_ref")
    private String inputSpeciesTreeRef;
    @JsonProperty("save_featuresets")
    private Long saveFeaturesets;
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

    public ViewPanPhyloInput withWorkspaceName(String workspaceName) {
        this.workspaceName = workspaceName;
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

    public ViewPanPhyloInput withInputPangenomeRef(String inputPangenomeRef) {
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

    public ViewPanPhyloInput withInputSpeciesTreeRef(String inputSpeciesTreeRef) {
        this.inputSpeciesTreeRef = inputSpeciesTreeRef;
        return this;
    }

    @JsonProperty("save_featuresets")
    public Long getSaveFeaturesets() {
        return saveFeaturesets;
    }

    @JsonProperty("save_featuresets")
    public void setSaveFeaturesets(Long saveFeaturesets) {
        this.saveFeaturesets = saveFeaturesets;
    }

    public ViewPanPhyloInput withSaveFeaturesets(Long saveFeaturesets) {
        this.saveFeaturesets = saveFeaturesets;
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

    public ViewPanPhyloInput withSkipMissingGenomes(Long skipMissingGenomes) {
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

    public ViewPanPhyloInput withEnforceGenomeVersionMatch(Long enforceGenomeVersionMatch) {
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
        return ((((((((((((((("ViewPanPhyloInput"+" [workspaceName=")+ workspaceName)+", inputPangenomeRef=")+ inputPangenomeRef)+", inputSpeciesTreeRef=")+ inputSpeciesTreeRef)+", saveFeaturesets=")+ saveFeaturesets)+", skipMissingGenomes=")+ skipMissingGenomes)+", enforceGenomeVersionMatch=")+ enforceGenomeVersionMatch)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
