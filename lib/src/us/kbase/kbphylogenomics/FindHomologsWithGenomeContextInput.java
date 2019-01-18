
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
    "save_per_genome_featureSets",
    "neighbor_thresh",
    "ident_thresh",
    "overlap_fraction",
    "e_value",
    "bitscore"
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
    @JsonProperty("neighbor_thresh")
    private Long neighborThresh;
    @JsonProperty("ident_thresh")
    private Double identThresh;
    @JsonProperty("overlap_fraction")
    private Double overlapFraction;
    @JsonProperty("e_value")
    private Double eValue;
    @JsonProperty("bitscore")
    private Double bitscore;
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

    @JsonProperty("neighbor_thresh")
    public Long getNeighborThresh() {
        return neighborThresh;
    }

    @JsonProperty("neighbor_thresh")
    public void setNeighborThresh(Long neighborThresh) {
        this.neighborThresh = neighborThresh;
    }

    public FindHomologsWithGenomeContextInput withNeighborThresh(Long neighborThresh) {
        this.neighborThresh = neighborThresh;
        return this;
    }

    @JsonProperty("ident_thresh")
    public Double getIdentThresh() {
        return identThresh;
    }

    @JsonProperty("ident_thresh")
    public void setIdentThresh(Double identThresh) {
        this.identThresh = identThresh;
    }

    public FindHomologsWithGenomeContextInput withIdentThresh(Double identThresh) {
        this.identThresh = identThresh;
        return this;
    }

    @JsonProperty("overlap_fraction")
    public Double getOverlapFraction() {
        return overlapFraction;
    }

    @JsonProperty("overlap_fraction")
    public void setOverlapFraction(Double overlapFraction) {
        this.overlapFraction = overlapFraction;
    }

    public FindHomologsWithGenomeContextInput withOverlapFraction(Double overlapFraction) {
        this.overlapFraction = overlapFraction;
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

    public FindHomologsWithGenomeContextInput withEValue(Double eValue) {
        this.eValue = eValue;
        return this;
    }

    @JsonProperty("bitscore")
    public Double getBitscore() {
        return bitscore;
    }

    @JsonProperty("bitscore")
    public void setBitscore(Double bitscore) {
        this.bitscore = bitscore;
    }

    public FindHomologsWithGenomeContextInput withBitscore(Double bitscore) {
        this.bitscore = bitscore;
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
        return ((((((((((((((((((((("FindHomologsWithGenomeContextInput"+" [workspaceName=")+ workspaceName)+", inputFeatureSetRef=")+ inputFeatureSetRef)+", inputSpeciesTreeRef=")+ inputSpeciesTreeRef)+", savePerGenomeFeatureSets=")+ savePerGenomeFeatureSets)+", neighborThresh=")+ neighborThresh)+", identThresh=")+ identThresh)+", overlapFraction=")+ overlapFraction)+", eValue=")+ eValue)+", bitscore=")+ bitscore)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
