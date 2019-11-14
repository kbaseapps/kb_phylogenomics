
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
 * <p>Original spec-file type: localize_DomainAnnotations_Input</p>
 * <pre>
 * localize_DomainAnnotations()
 * **
 * ** point all DomainAnnotations at local copies of Genome Objects
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "workspace_name",
    "input_DomainAnnotation_refs"
})
public class LocalizeDomainAnnotationsInput {

    @JsonProperty("workspace_name")
    private String workspaceName;
    @JsonProperty("input_DomainAnnotation_refs")
    private String inputDomainAnnotationRefs;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("workspace_name")
    public String getWorkspaceName() {
        return workspaceName;
    }

    @JsonProperty("workspace_name")
    public void setWorkspaceName(String workspaceName) {
        this.workspaceName = workspaceName;
    }

    public LocalizeDomainAnnotationsInput withWorkspaceName(String workspaceName) {
        this.workspaceName = workspaceName;
        return this;
    }

    @JsonProperty("input_DomainAnnotation_refs")
    public String getInputDomainAnnotationRefs() {
        return inputDomainAnnotationRefs;
    }

    @JsonProperty("input_DomainAnnotation_refs")
    public void setInputDomainAnnotationRefs(String inputDomainAnnotationRefs) {
        this.inputDomainAnnotationRefs = inputDomainAnnotationRefs;
    }

    public LocalizeDomainAnnotationsInput withInputDomainAnnotationRefs(String inputDomainAnnotationRefs) {
        this.inputDomainAnnotationRefs = inputDomainAnnotationRefs;
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
        return ((((((("LocalizeDomainAnnotationsInput"+" [workspaceName=")+ workspaceName)+", inputDomainAnnotationRefs=")+ inputDomainAnnotationRefs)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
