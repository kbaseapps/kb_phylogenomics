
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
 * <p>Original spec-file type: view_tree_Input</p>
 * <pre>
 * view_tree()
 * **
 * ** show a KBase Tree and make newick and images downloadable
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "workspace_name",
    "input_tree_ref"
})
public class ViewTreeInput {

    @JsonProperty("workspace_name")
    private String workspaceName;
    @JsonProperty("input_tree_ref")
    private String inputTreeRef;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("workspace_name")
    public String getWorkspaceName() {
        return workspaceName;
    }

    @JsonProperty("workspace_name")
    public void setWorkspaceName(String workspaceName) {
        this.workspaceName = workspaceName;
    }

    public ViewTreeInput withWorkspaceName(String workspaceName) {
        this.workspaceName = workspaceName;
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

    public ViewTreeInput withInputTreeRef(String inputTreeRef) {
        this.inputTreeRef = inputTreeRef;
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
        return ((((((("ViewTreeInput"+" [workspaceName=")+ workspaceName)+", inputTreeRef=")+ inputTreeRef)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
