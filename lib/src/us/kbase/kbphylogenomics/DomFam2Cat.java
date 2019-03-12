
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
 * <p>Original spec-file type: DomFam2Cat</p>
 * <pre>
 * domain family to category
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "namespace",
    "domfam"
})
public class DomFam2Cat {

    @JsonProperty("namespace")
    private String namespace;
    @JsonProperty("domfam")
    private String domfam;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("namespace")
    public String getNamespace() {
        return namespace;
    }

    @JsonProperty("namespace")
    public void setNamespace(String namespace) {
        this.namespace = namespace;
    }

    public DomFam2Cat withNamespace(String namespace) {
        this.namespace = namespace;
        return this;
    }

    @JsonProperty("domfam")
    public String getDomfam() {
        return domfam;
    }

    @JsonProperty("domfam")
    public void setDomfam(String domfam) {
        this.domfam = domfam;
    }

    public DomFam2Cat withDomfam(String domfam) {
        this.domfam = domfam;
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
        return ((((((("DomFam2Cat"+" [namespace=")+ namespace)+", domfam=")+ domfam)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
