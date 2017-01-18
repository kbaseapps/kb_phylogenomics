
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
 * <p>Original spec-file type: view_genome_circle_plot_Input</p>
 * <pre>
 * view_genome_circle_plot()
 * **
 * ** build a circle plot of a microbial genome
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "workspace_name",
    "input_genome_ref"
})
public class ViewGenomeCirclePlotInput {

    @JsonProperty("workspace_name")
    private String workspaceName;
    @JsonProperty("input_genome_ref")
    private String inputGenomeRef;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("workspace_name")
    public String getWorkspaceName() {
        return workspaceName;
    }

    @JsonProperty("workspace_name")
    public void setWorkspaceName(String workspaceName) {
        this.workspaceName = workspaceName;
    }

    public ViewGenomeCirclePlotInput withWorkspaceName(String workspaceName) {
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

    public ViewGenomeCirclePlotInput withInputGenomeRef(String inputGenomeRef) {
        this.inputGenomeRef = inputGenomeRef;
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
        return ((((((("ViewGenomeCirclePlotInput"+" [workspaceName=")+ workspaceName)+", inputGenomeRef=")+ inputGenomeRef)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
