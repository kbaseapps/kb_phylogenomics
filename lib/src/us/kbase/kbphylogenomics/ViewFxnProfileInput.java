
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
    "custom_target_fams",
    "count_category",
    "heatmap",
    "vertical",
    "top_hit",
    "e_value",
    "log_base",
    "show_blanks",
    "display_genome_object_name",
    "skip_missing_genomes",
    "enforce_genome_version_match"
})
public class ViewFxnProfileInput {

    @JsonProperty("workspace_name")
    private String workspaceName;
    @JsonProperty("input_genomeSet_ref")
    private String inputGenomeSetRef;
    @JsonProperty("namespace")
    private String namespace;
    /**
     * <p>Original spec-file type: CustomTargetFams</p>
     * <pre>
     * parameter groups
     * </pre>
     * 
     */
    @JsonProperty("custom_target_fams")
    private CustomTargetFams customTargetFams;
    @JsonProperty("count_category")
    private String countCategory;
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
    @JsonProperty("display_genome_object_name")
    private Long displayGenomeObjectName;
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

    public ViewFxnProfileInput withWorkspaceName(String workspaceName) {
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

    public ViewFxnProfileInput withInputGenomeSetRef(String inputGenomeSetRef) {
        this.inputGenomeSetRef = inputGenomeSetRef;
        return this;
    }

    @JsonProperty("namespace")
    public String getNamespace() {
        return namespace;
    }

    @JsonProperty("namespace")
    public void setNamespace(String namespace) {
        this.namespace = namespace;
    }

    public ViewFxnProfileInput withNamespace(String namespace) {
        this.namespace = namespace;
        return this;
    }

    /**
     * <p>Original spec-file type: CustomTargetFams</p>
     * <pre>
     * parameter groups
     * </pre>
     * 
     */
    @JsonProperty("custom_target_fams")
    public CustomTargetFams getCustomTargetFams() {
        return customTargetFams;
    }

    /**
     * <p>Original spec-file type: CustomTargetFams</p>
     * <pre>
     * parameter groups
     * </pre>
     * 
     */
    @JsonProperty("custom_target_fams")
    public void setCustomTargetFams(CustomTargetFams customTargetFams) {
        this.customTargetFams = customTargetFams;
    }

    public ViewFxnProfileInput withCustomTargetFams(CustomTargetFams customTargetFams) {
        this.customTargetFams = customTargetFams;
        return this;
    }

    @JsonProperty("count_category")
    public String getCountCategory() {
        return countCategory;
    }

    @JsonProperty("count_category")
    public void setCountCategory(String countCategory) {
        this.countCategory = countCategory;
    }

    public ViewFxnProfileInput withCountCategory(String countCategory) {
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

    @JsonProperty("log_base")
    public Double getLogBase() {
        return logBase;
    }

    @JsonProperty("log_base")
    public void setLogBase(Double logBase) {
        this.logBase = logBase;
    }

    public ViewFxnProfileInput withLogBase(Double logBase) {
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

    public ViewFxnProfileInput withShowBlanks(Long showBlanks) {
        this.showBlanks = showBlanks;
        return this;
    }

    @JsonProperty("display_genome_object_name")
    public Long getDisplayGenomeObjectName() {
        return displayGenomeObjectName;
    }

    @JsonProperty("display_genome_object_name")
    public void setDisplayGenomeObjectName(Long displayGenomeObjectName) {
        this.displayGenomeObjectName = displayGenomeObjectName;
    }

    public ViewFxnProfileInput withDisplayGenomeObjectName(Long displayGenomeObjectName) {
        this.displayGenomeObjectName = displayGenomeObjectName;
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

    public ViewFxnProfileInput withSkipMissingGenomes(Long skipMissingGenomes) {
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

    public ViewFxnProfileInput withEnforceGenomeVersionMatch(Long enforceGenomeVersionMatch) {
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
        return ((((((((((((((((((((((((((((((("ViewFxnProfileInput"+" [workspaceName=")+ workspaceName)+", inputGenomeSetRef=")+ inputGenomeSetRef)+", namespace=")+ namespace)+", customTargetFams=")+ customTargetFams)+", countCategory=")+ countCategory)+", heatmap=")+ heatmap)+", vertical=")+ vertical)+", topHit=")+ topHit)+", eValue=")+ eValue)+", logBase=")+ logBase)+", showBlanks=")+ showBlanks)+", displayGenomeObjectName=")+ displayGenomeObjectName)+", skipMissingGenomes=")+ skipMissingGenomes)+", enforceGenomeVersionMatch=")+ enforceGenomeVersionMatch)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
