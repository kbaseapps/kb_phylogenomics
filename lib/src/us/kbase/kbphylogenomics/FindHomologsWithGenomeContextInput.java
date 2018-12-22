
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
 * <p>Original spec-file type: find_homologs_with_genome_context_Input</p>
 * <pre>
 * find_homologs_with_genome_context()
 * **
 * ** show homolgous genes across multiple genomes within genome context against species tree
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "workspace_name",
    "input_featureSet_ref",
    "input_speciesTree_ref",
    "save_per_genome_featureSets"
})
public class FindHomologsWithGenomeContextInput {

    @JsonProperty("workspace_name")
    private String workspaceName;
    @JsonProperty("input_featureSet_ref")
    private String inputFeatureSetRef;
    @JsonProperty("input_speciesTree_ref")
    private String inputSpeciesTreeRef;
    @JsonProperty("save_per_genome_featureSets")
    private Long savePerGenomeFeatureSets;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("workspace_name")
    public String getWorkspaceName() {
        return workspaceName;
    }

    @JsonProperty("workspace_name")
    public void setWorkspaceName(String workspaceName) {
        this.workspaceName = workspaceName;
    }

    public FindHomologsWithGenomeContextInput withWorkspaceName(String workspaceName) {
        this.workspaceName = workspaceName;
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

    public FindHomologsWithGenomeContextInput withInputFeatureSetRef(String inputFeatureSetRef) {
        this.inputFeatureSetRef = inputFeatureSetRef;
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

    public FindHomologsWithGenomeContextInput withInputSpeciesTreeRef(String inputSpeciesTreeRef) {
        this.inputSpeciesTreeRef = inputSpeciesTreeRef;
        return this;
    }

    @JsonProperty("save_per_genome_featureSets")
    public Long getSavePerGenomeFeatureSets() {
        return savePerGenomeFeatureSets;
    }

    @JsonProperty("save_per_genome_featureSets")
    public void setSavePerGenomeFeatureSets(Long savePerGenomeFeatureSets) {
        this.savePerGenomeFeatureSets = savePerGenomeFeatureSets;
    }

    public FindHomologsWithGenomeContextInput withSavePerGenomeFeatureSets(Long savePerGenomeFeatureSets) {
        this.savePerGenomeFeatureSets = savePerGenomeFeatureSets;
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
        return ((((((((((("FindHomologsWithGenomeContextInput"+" [workspaceName=")+ workspaceName)+", inputFeatureSetRef=")+ inputFeatureSetRef)+", inputSpeciesTreeRef=")+ inputSpeciesTreeRef)+", savePerGenomeFeatureSets=")+ savePerGenomeFeatureSets)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
