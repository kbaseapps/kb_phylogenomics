
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
 * <p>Original spec-file type: view_pan_circle_plot_Input</p>
 * <pre>
 * view_pan_circle_plot()
 * **
 * ** build a circle plot of a microbial genome with its pangenome members
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "workspace_name",
    "input_genome_ref",
    "input_pangenome_ref",
    "input_compare_all_flag",
    "input_compare_genome_refs"
})
public class ViewPanCirclePlotInput {

    @JsonProperty("workspace_name")
    private String workspaceName;
    @JsonProperty("input_genome_ref")
    private String inputGenomeRef;
    @JsonProperty("input_pangenome_ref")
    private String inputPangenomeRef;
    @JsonProperty("input_compare_all_flag")
    private String inputCompareAllFlag;
    @JsonProperty("input_compare_genome_refs")
    private String inputCompareGenomeRefs;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("workspace_name")
    public String getWorkspaceName() {
        return workspaceName;
    }

    @JsonProperty("workspace_name")
    public void setWorkspaceName(String workspaceName) {
        this.workspaceName = workspaceName;
    }

    public ViewPanCirclePlotInput withWorkspaceName(String workspaceName) {
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

    public ViewPanCirclePlotInput withInputGenomeRef(String inputGenomeRef) {
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

    public ViewPanCirclePlotInput withInputPangenomeRef(String inputPangenomeRef) {
        this.inputPangenomeRef = inputPangenomeRef;
        return this;
    }

    @JsonProperty("input_compare_all_flag")
    public String getInputCompareAllFlag() {
        return inputCompareAllFlag;
    }

    @JsonProperty("input_compare_all_flag")
    public void setInputCompareAllFlag(String inputCompareAllFlag) {
        this.inputCompareAllFlag = inputCompareAllFlag;
    }

    public ViewPanCirclePlotInput withInputCompareAllFlag(String inputCompareAllFlag) {
        this.inputCompareAllFlag = inputCompareAllFlag;
        return this;
    }

    @JsonProperty("input_compare_genome_refs")
    public String getInputCompareGenomeRefs() {
        return inputCompareGenomeRefs;
    }

    @JsonProperty("input_compare_genome_refs")
    public void setInputCompareGenomeRefs(String inputCompareGenomeRefs) {
        this.inputCompareGenomeRefs = inputCompareGenomeRefs;
    }

    public ViewPanCirclePlotInput withInputCompareGenomeRefs(String inputCompareGenomeRefs) {
        this.inputCompareGenomeRefs = inputCompareGenomeRefs;
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
        return ((((((((((((("ViewPanCirclePlotInput"+" [workspaceName=")+ workspaceName)+", inputGenomeRef=")+ inputGenomeRef)+", inputPangenomeRef=")+ inputPangenomeRef)+", inputCompareAllFlag=")+ inputCompareAllFlag)+", inputCompareGenomeRefs=")+ inputCompareGenomeRefs)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
